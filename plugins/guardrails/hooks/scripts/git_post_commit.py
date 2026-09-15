#!/usr/bin/env python3
"""PostToolUse check — after `git commit`, show what actually landed.

Surfaces `git log -1 --stat` as a systemMessage so the model verifies its files
are in ITS commit (another writer on a shared repo can sweep a staged index
into their own commit). Flags a commit that produced nothing, and a HEAD author
that does not match `commit_identities` in .claude/guardrails.json when set.

Never blocks. Configured in .claude/settings.json under "PostToolUse" with
matcher "Bash|PowerShell".
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load as load_config  # noqa: E402


def git(args, cwd, timeout=30):
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "").strip()
    except Exception:  # noqa: BLE001
        return 1, ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        sys.exit(0)
    if data.get("tool_name") not in ("Bash", "PowerShell"):
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if not re.search(r"\bgit\s+commit\b", cmd) or "--help" in cmd:
        sys.exit(0)
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

    resp = data.get("tool_response")
    resp_txt = resp if isinstance(resp, str) else json.dumps(resp or "")

    notes = []
    if re.search(r"nothing to commit|no changes added to commit|nothing added to commit", resp_txt):
        notes.append("the commit produced NOTHING - check `git log -3 --stat`: another writer "
                     "may have swept your staged index into its own commit. "
                     "If so, record your rationale with `git commit --allow-empty` referencing that hash.")

    code, head = git(["log", "-1", "--format=%an <%ae> %h %s"], cwd)
    if code != 0 or not head:
        sys.exit(0)
    author = head.split(" <", 1)[0]
    ident = load_config(cwd).get("commit_identities")
    if ident and not re.match(ident, author):
        notes.append(f"HEAD author '{author}' does not match commit_identities {ident!r}.")

    _, stat = git(["log", "-1", "--stat=100", "--format="], cwd)
    files = [l.strip() for l in stat.splitlines() if "|" in l]
    summary = [l.strip() for l in stat.splitlines() if "changed" in l]
    shown = files[:12] + ([f"... +{len(files) - 12} more"] if len(files) > 12 else [])

    msg = "Post-commit check - HEAD: " + head
    if summary:
        msg += f" ({summary[0]})"
    if shown:
        msg += "\n  " + "\n  ".join(shown)
    if notes:
        msg += "\n  WARNING: " + "\n  WARNING: ".join(notes)
    print(json.dumps({"systemMessage": msg}))
    sys.exit(0)


if __name__ == "__main__":
    main()
