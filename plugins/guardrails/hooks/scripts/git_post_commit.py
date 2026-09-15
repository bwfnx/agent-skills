#!/usr/bin/env python3
"""PostToolUse check — after `git commit`, show what actually landed.

Learning scheduled-tasks-commit-your-staged-index: a scheduled task swept a
session's staged changes into ITS commit, and the session's own `git commit`
reported "no changes added to commit". Protocol: verify with `git log -1 --stat`
that your files are in YOUR commit. This hook does that automatically and
surfaces the result as a systemMessage, flagging a foreign author on HEAD or a
commit that produced nothing.

Never blocks. Configured in .claude/settings.json under "PostToolUse" with
matcher "Bash|PowerShell".
"""
import json
import os
import re
import subprocess
import sys

IDENTITY_RE = re.compile(r"^(Claude-[\w.-]+|Codex|ChatGPT|Local-[\w.-]+)$")


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
                     "(a scheduled task) may have swept your staged index into its own commit. "
                     "If so, record your rationale with `git commit --allow-empty` referencing that hash.")

    code, head = git(["log", "-1", "--format=%an <%ae> %h %s"], cwd)
    if code != 0 or not head:
        sys.exit(0)
    author = head.split(" <", 1)[0]
    if not IDENTITY_RE.match(author):
        notes.append(f"HEAD author '{author}' is not a contract identity.")

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
