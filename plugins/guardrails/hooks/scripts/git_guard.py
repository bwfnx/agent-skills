#!/usr/bin/env python3
"""PreToolUse guard for git on the shared Playground repo.

Three checks on Bash / PowerShell commands:

1. History-rewriting or working-tree-destroying git  -> "ask"
   push --force / -f, reset --hard, checkout -- <path>, restore (non --staged),
   clean -f/-d/-x, branch -D, filter-repo / filter-branch.
   Four agents share this repo; these are never auto-approved.

2. `git commit` identity  -> "deny" unless the author name matches the
   `commit_identities` regex in .claude/guardrails.json. Skipped when that key
   is absent. Satisfied by --author=... on the command or `git config user.name`.

3. `git commit` CRLF churn  -> "deny" if any file the commit will contain has a
   `git diff --numstat` that disagrees with `--numstat -w` (a line-ending
   rewrite disguised as an edit). Scoped to the commit's own files. Add the
   token [crlf-ok] anywhere in the command to bypass once.

Wired by hooks/hooks.json under "PreToolUse" with matcher "Bash|PowerShell".
"""
import json
import os
import re
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load as load_config  # noqa: E402

DESTRUCTIVE = [
    (r"\bgit\s+push\b[^|;&]*\s(--force\b|-f\b|--force-with-lease\b)", "git push --force"),
    (r"\bgit\s+reset\s+(?:[^|;&]*\s)?--hard\b", "git reset --hard"),
    (r"\bgit\s+checkout\s+(?:[^|;&]*\s)?--\s", "git checkout -- <path>"),
    (r"\bgit\s+restore\b(?![^|;&]*--staged)", "git restore (discards working-tree changes)"),
    (r"\bgit\s+clean\s+-\w*[fdx]", "git clean"),
    (r"\bgit\s+branch\s+(?:[^|;&]*\s)?(-D\b|--delete\s+--force|--force\s+--delete)", "git branch -D"),
    (r"\bgit\s+(filter-repo|filter-branch)\b|\bgit_filter_repo\b", "history rewrite (filter-repo/filter-branch)"),
]


def out(decision, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def git(args, cwd, timeout=30):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "").strip()
    except Exception:  # noqa: BLE001
        return 1, ""


def numstat_paths(cwd, extra):
    """Return {path: (added, deleted)} for `git diff --numstat <extra>`."""
    code, txt = git(["diff", "--numstat", *extra], cwd)
    res = {}
    if code != 0:
        return res
    for ln in txt.splitlines():
        parts = ln.split("\t")
        if len(parts) >= 3:
            res["\t".join(parts[2:])] = (parts[0], parts[1])
    return res


VALUE_FLAGS = {"-m", "-F", "-C", "-c", "-t", "--author", "--date", "--message", "--file",
               "--template", "--fixup", "--squash", "--reuse-message", "--reedit-message",
               "--trailer", "--cleanup", "--gpg-sign"}


def _tokens(seg):
    try:
        return shlex.split(seg, posix=True)
    except ValueError:
        return seg.split()


def commit_scope(cmd):
    """What will the commit contain?  -> (whole, added, pathspecs)

    whole     : every tracked change (commit -a, add -A / -u / . / --renormalize)
    added     : paths a `git add` in the same command stages on top of the index
    pathspecs : paths given to `git commit` itself (--only / `-- <path>`), which
                restrict the commit to those paths
    Parsing is per shell segment (split on && || ; |), so `git add X && git
    commit --only X` is scoped to X, not to the whole dirty tree.
    """
    whole, added, pathspecs = False, [], []
    for seg in re.split(r"&&|\|\||;|\|", cmd):
        toks = _tokens(seg)
        if "git" not in toks:
            continue
        sub = toks[toks.index("git") + 1:]
        if not sub:
            continue
        verb, args = sub[0], sub[1:]
        if verb == "add":
            if any(a in ("-A", "--all", "-u", "--update", ".", "--renormalize")
                   or (a.startswith("-") and not a.startswith("--") and ("A" in a or "u" in a))
                   for a in args):
                whole = True
            added += [a for a in args if not a.startswith("-")]
        elif verb == "commit":
            i, after_dd = 0, False
            while i < len(args):
                a = args[i]
                i += 1
                if after_dd:
                    pathspecs.append(a)
                elif a == "--":
                    after_dd = True
                elif a.startswith("--"):
                    if a in ("--all",):
                        whole = True
                    elif a in VALUE_FLAGS:
                        i += 1
                elif a.startswith("-"):
                    letters = a[1:]
                    if "a" in letters:
                        whole = True
                    if letters and letters[-1] in "mFCct":
                        i += 1  # -m "msg", -am "msg", -F file ...
                else:
                    pathspecs.append(a)
    return whole, added, pathspecs


def _root_rel(cwd, p):
    """Turn a cwd-relative pathspec into the repo-root-relative form numstat prints."""
    _, top = git(["rev-parse", "--show-toplevel"], cwd)
    full = os.path.abspath(os.path.join(cwd, p))
    try:
        rel = os.path.relpath(full, top or cwd)
    except ValueError:  # different drive on Windows
        rel = p
    return rel.replace("\\", "/")


def effective_cwd(cmd, cwd):
    """Directory the `git commit` will run in: the last `cd <path>` in the
    command before the commit segment, resolved against the payload cwd.
    The hook payload's cwd is the session's, not the command's."""
    for seg in re.split(r"&&|\|\||;", cmd):
        toks = _tokens(seg)
        if toks and toks[0] == "git" and "commit" in toks[1:2]:
            break
        if len(toks) >= 2 and toks[0] == "cd":
            target = os.path.expanduser(toks[1])
            m = re.match(r"^/([A-Za-z])(/.*)?$", target)  # Git Bash /c/... -> C:/...
            if m:
                target = f"{m.group(1).upper()}:{m.group(2) or '/'}"
            cwd = target if (os.path.isabs(target) or target.startswith("/")) else os.path.join(cwd, target)
    return cwd


def crlf_churn(cmd, cwd):
    """Files the commit would contain whose diff is line-ending churn.

    Compares `git diff --numstat` against `--numstat -w` over exactly the files
    the commit will carry: the index, plus whatever the same command `git add`s,
    or the whole tracked tree for `commit -a` / `add -A`; then narrowed to the
    commit's own pathspecs. Scoping to the whole dirty tree flagged 22 files
    another agent was editing when one LF file was committed with --only
    (2026-09-14), so the scope is now the commit's, not the checkout's.
    """
    whole, added, pathspecs = commit_scope(cmd)
    if whole:
        raw, ws = numstat_paths(cwd, ["HEAD"]), numstat_paths(cwd, ["HEAD", "-w"])
    else:
        raw, ws = numstat_paths(cwd, ["--cached"]), numstat_paths(cwd, ["--cached", "-w"])
        if added:
            raw.update(numstat_paths(cwd, ["HEAD", "--", *added]))
            ws.update(numstat_paths(cwd, ["HEAD", "-w", "--", *added]))
    churn = [p for p, v in raw.items() if ws.get(p) != v]
    if pathspecs:
        specs = [_root_rel(cwd, p).rstrip("/") for p in pathspecs]
        churn = [p for p in churn if any(p == s or p.startswith(s + "/") for s in specs)]
    return sorted(churn)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        sys.exit(0)
    if data.get("tool_name") not in ("Bash", "PowerShell"):
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if "git" not in cmd:
        sys.exit(0)
    cwd = effective_cwd(cmd, data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())

    # 1. destructive -> ask
    for pat, label in DESTRUCTIVE:
        if re.search(pat, cmd):
            out("ask", f"`{label}` rewrites history or discards work in the working tree. "
                       "Confirm this is intended.")

    if not re.search(r"\bgit\s+commit\b", cmd) or re.search(r"\bgit\s+commit\s+--help\b", cmd):
        sys.exit(0)

    # 2. identity (only when configured)
    cfg = load_config(cwd)
    ident = cfg.get("commit_identities")
    if ident:
        m = re.search(r"--author[=\s]+[\"']?([^\"'<]+?)\s*(?:<|[\"']|$)", cmd)
        if m:
            name = m.group(1).strip()
        else:
            _, name = git(["config", "user.name"], cwd)
        if not re.match(ident, name or ""):
            out("deny",
                f"Commit would be authored as '{name or '(unset)'}', which does not match "
                f"commit_identities {ident!r} in .claude/guardrails.json. Add --author=\"<Name> <email>\" "
                "to the commit or set `git config user.name` for this repo.")

    # 3. CRLF churn
    if "[crlf-ok]" not in cmd:
        churn = crlf_churn(cmd, cwd)
        if churn:
            shown = ", ".join(churn[:8]) + (f" (+{len(churn) - 8} more)" if len(churn) > 8 else "")
            out("deny",
                f"Line-ending churn in files to be committed: {shown}. `git diff --numstat` and "
                "`--numstat -w` disagree, so the diff carries CRLF<->LF rewrites, not just your edit "
                "(a whole-file rewrite hiding a small edit). Restore the original "
                "line endings (rewrite in binary: data.replace(b'\\r\\n', b'\\n').replace(b'\\n', b'\\r\\n') "
                "for CRLF files) and retry, or add [crlf-ok] to the command if the churn is intended.")

    sys.exit(0)


if __name__ == "__main__":
    main()
