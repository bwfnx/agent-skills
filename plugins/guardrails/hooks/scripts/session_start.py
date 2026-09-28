#!/usr/bin/env python3
"""SessionStart hook — inject the repo's session protocol.

Runs a non-destructive `git fetch`, then feeds the newest entries of the
handoff log and the "Active now" block of the tasks file (names from
.claude/guardrails.json: handoff_file, tasks_file; both optional) into the
model's context via hookSpecificOutput.additionalContext.

Also snapshots the dirty working tree (path -> status + content hash) to
<temp>/claude-guardrails/<session_id>.json so the Stop hook can nag only about
files changed DURING this session.

Never fails the session: any error degrades to a short note.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gitstate import write_snapshot  # noqa: E402
from _config import load as load_config, project_root  # noqa: E402


def run(args, cwd, timeout=30):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout)
        return (r.returncode,
                r.stdout.decode("utf-8", errors="replace").strip(),
                r.stderr.decode("utf-8", errors="replace").strip())
    except Exception as e:  # noqa: BLE001 - never crash the session
        return 1, "", str(e)


def git_status(root):
    code, _, _ = run(["git", "rev-parse", "--is-inside-work-tree"], root)
    if code != 0:
        return "git: not a repository here (skipping pull check)."
    _, branch, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], root)
    _, porcelain, _ = run(["git", "status", "--porcelain"], root)
    dirty = len([l for l in porcelain.splitlines() if l.strip()])
    up_code, _, _ = run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], root)
    if up_code != 0:
        # Don't report "0 behind" when there is nothing to be behind of.
        return (f"git [{branch or '?'}]: no upstream configured (local-only repo, "
                f"{dirty} uncommitted file(s)). Commits cannot be pushed until a remote exists.")
    run(["git", "fetch", "--quiet"], root)  # non-destructive
    _, counts, _ = run(["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"], root)
    ahead = behind = "?"
    if counts and "\t" in counts:
        parts = counts.split("\t")
        if len(parts) >= 2:
            ahead, behind = parts[0], parts[1]
    line = (f"git [{branch or '?'}]: {behind} behind upstream, {ahead} ahead, "
            f"{dirty} uncommitted file(s).")
    try:
        if int(behind) > 0:
            line += " Run `git pull` before writing anything."
    except ValueError:
        pass
    return line


def handoff_tail(root, name, max_entries=2, max_lines=45):
    """HANDOFF-LOG.md prepends newest entries at the TOP, so the 'tail' is the head."""
    p = os.path.join(root, name)
    if not os.path.isfile(p):
        return None
    lines = []
    seen_headers = 0
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            for i, ln in enumerate(f):
                if ln.startswith("## "):
                    seen_headers += 1
                    if seen_headers > max_entries:
                        break
                lines.append(ln.rstrip("\n"))
                if i >= max_lines:
                    break
    except Exception:  # noqa: BLE001
        return None
    return "\n".join(lines).strip() or None


def active_tasks(root, name, max_lines=12):
    p = os.path.join(root, name)
    if not os.path.isfile(p):
        return None
    out = []
    capturing = False
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            for ln in f:
                s = ln.rstrip("\n")
                if s.startswith("## "):
                    capturing = s.lower().startswith("## active")
                    continue
                if capturing and s.strip():
                    out.append(s)
                if len(out) >= max_lines:
                    break
    except Exception:  # noqa: BLE001
        return None
    return "\n".join(out).strip() or None


def main():
    session_id = None
    try:
        payload = json.load(sys.stdin)
        session_id = payload.get("session_id")
    except Exception:  # noqa: BLE001
        pass

    root = project_root()
    write_snapshot(root, session_id)

    cfg = load_config(root)
    parts = [
        "Session protocol (read before writing):",
        "1) pull   2) read the newest handoff + active tasks below   "
        "3) at session end: commit as your identity, prepend a handoff entry, push.",
        "",
        "- " + git_status(root),
    ]
    h = handoff_tail(root, cfg["handoff_file"])
    if h:
        parts += ["", f"Newest {cfg['handoff_file']} entries:", h]
    t = active_tasks(root, cfg["tasks_file"])
    if t:
        parts += ["", f"{cfg['tasks_file']} — Active now:", t]

    context = "\n".join(parts)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
