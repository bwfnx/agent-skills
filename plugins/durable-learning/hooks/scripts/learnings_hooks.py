#!/usr/bin/env python3
"""durable-learning hooks. Usage: learnings_hooks.py session_start|guard  (hook JSON on stdin)

session_start  If the project has memory/learnings/, tell the agent how many active
               learnings exist, list the highest-value pitfalls by key, and give the
               exact query commands. Silent in projects without a store.
guard          PreToolUse. The store is owned by learnings.py: hand edits to
               memory/learnings/ are denied (Write/Edit, or shell redirects, rm, mv,
               sed -i, Set-Content ...), and so are whole-file reads of the compiled
               _views/*.jsonl, which outgrow the tool-result cap and truncate silently.

Zero config: both do nothing unless the path involved is inside memory/learnings/.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.normpath(os.path.join(
    HERE, "..", "..", "skills", "durable-learning-protocol", "scripts", "learnings.py"))
STORE = re.compile(r"memory[/\\]+learnings(?:[/\\]|$|[\"'\s])", re.IGNORECASE)
VIEWS = re.compile(r"memory[/\\]+learnings[/\\]+_views[/\\]", re.IGNORECASE)
SHELL_WRITE = re.compile(
    r"(>{1,2}|(?<![\w-])(tee|rm|del|erase|mv|move|ren|rename|Set-Content|Add-Content|Out-File|"
    r"Remove-Item|Move-Item|Rename-Item|Clear-Content|New-Item)(?![\w-])|\bsed\b[^|;&]*\s-i)",
    re.IGNORECASE)
WHOLE_READ = re.compile(
    r"(?<![\w-])(cat|type|more|less|gc|Get-Content|Import-Csv|cp|copy|Copy-Item)(?![\w-])",
    re.IGNORECASE)
MAX_PITFALLS = 12


def cli():
    """The exact command to run learnings.py, using the interpreter this hook already runs under."""
    return f'"{sys.executable}" "{SCRIPT}"'


def project_root():
    base = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=base,
                           capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return base


def emit(event, **fields):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, **fields}}))
    sys.exit(0)


def deny(reason):
    emit("PreToolUse", permissionDecision="deny", permissionDecisionReason=reason)


def session_start():
    root = project_root()
    if not os.path.isdir(os.path.join(root, "memory", "learnings")):
        sys.exit(0)
    os.environ["LEARNINGS_ROOT"] = root  # learnings.py resolves its store from this at import
    sys.path.insert(0, os.path.dirname(SCRIPT))
    import learnings  # noqa: E402  (reuse its reader rather than parse the store twice)

    active = [o for _ns, _p, o in learnings.iter_entries()
              if (o.get("status") or "active") == "active"]
    if not active:
        sys.exit(0)
    pitfalls = sorted((o for o in active if o.get("type") == "pitfall"),
                      key=lambda o: -(o.get("usefulness") or 0))[:MAX_PITFALLS]
    run = cli()
    lines = [
        f"Durable learnings: {len(active)} active in memory/learnings/ "
        f"({', '.join(learnings.namespaces())}). Query before multi-step work; "
        "an entry that contradicts your plan wins.",
        f"CLI: {run}",
        "  list --grep <term>      full rows matching a term",
        "  list --full KEY [KEY]   full rows by key",
        "  add --namespace <ns> --key <kebab-key> --insight \"...\"   the only way to write",
    ]
    if pitfalls:
        lines.append("Known pitfalls (mistakes already made once): "
                     + ", ".join(o.get("key", "?") for o in pitfalls))
    emit("SessionStart", additionalContext="\n".join(lines))


def guard():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        sys.exit(0)
    tool = data.get("tool_name") or ""
    ti = data.get("tool_input") or {}
    add_hint = ("The learnings store is written only by learnings.py (one file per entry, "
                f"so parallel agents never collide). Use: {cli()} add ... ; to replace "
                f"an entry, add the new one, then: {cli()} retire OLD_KEY --by NEW_KEY")
    view_hint = ("The compiled _views/*.jsonl files exceed the tool-result cap and truncate "
                 f"silently. Query instead: {cli()} list --grep <term>.")

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if STORE.search(path + " "):
            deny(add_hint)
    elif tool == "Read":
        if VIEWS.search(ti.get("file_path") or ""):
            deny(view_hint)
    elif tool in ("Bash", "PowerShell"):
        cmd = ti.get("command") or ""
        if not STORE.search(cmd + " "):
            sys.exit(0)
        if SHELL_WRITE.search(cmd):
            deny(add_hint)
        if VIEWS.search(cmd) and WHOLE_READ.search(cmd):
            deny(view_hint)
    sys.exit(0)


if __name__ == "__main__":
    {"session_start": session_start, "guard": guard}.get(
        sys.argv[1] if len(sys.argv) > 1 else "", lambda: sys.exit(0))()
