#!/usr/bin/env python3
"""PreToolUse guard — never read a configured big file whole.

`never_read_whole` in .claude/guardrails.json lists globs (matched against the
path and against its basename) for files that exceed the tool-result cap and
truncate silently when dumped. Denies the Read tool on them, and Bash /
PowerShell commands that dump one with a whole-file reader (cat, type,
Get-Content, more, less, Out-String, Import-Csv, cp, ...) or head/tail with a
count >= 200. Targeted access (grep, jq, small head/tail, scripts) passes.

No config -> no opinion. Wired under "PreToolUse" with matcher
"Read|Bash|PowerShell".
"""
import fnmatch
import json
import os
import re
import shlex
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load as load_config, project_root  # noqa: E402

WHOLE_READERS = re.compile(
    r"(?<![\w-])(cat|type|more|less|gc|Get-Content|Out-String|Import-Csv|"
    r"Out-File|Copy-Item|cp)(?![\w-])",
    re.IGNORECASE,
)


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def matches(path, globs):
    p = path.replace("\\", "/")
    return any(fnmatch.fnmatch(p, g) or fnmatch.fnmatch(os.path.basename(p), os.path.basename(g))
               or fnmatch.fnmatch(p, "*/" + g) for g in globs)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        sys.exit(0)
    globs = load_config(project_root()).get("never_read_whole") or []
    if not globs:
        sys.exit(0)
    reason = (f"This file must not be read whole (guardrails.json never_read_whole: {globs}) — it "
              "exceeds the tool-result cap and truncates silently. Query it with grep, jq, a small "
              "head/tail, or the script that owns it.")

    tool = data.get("tool_name") or ""
    ti = data.get("tool_input") or {}

    if tool == "Read":
        if matches(ti.get("file_path") or "", globs):
            deny(reason)
        sys.exit(0)

    if tool in ("Bash", "PowerShell"):
        cmd = ti.get("command") or ""
        try:
            toks = shlex.split(cmd, posix=True)
        except ValueError:
            toks = cmd.split()
        if not any(matches(t, globs) for t in toks):
            sys.exit(0)
        if WHOLE_READERS.search(cmd):
            deny(reason)
        m = re.search(r"\b(head|tail)\b[^|;&]*?-(?:n\s*|c\s*)?(\d+)", cmd)
        if m and int(m.group(2)) >= 200:
            deny(reason)
    sys.exit(0)


if __name__ == "__main__":
    main()
