#!/usr/bin/env python3
"""PreToolUse guard — never read the learnings store whole.

CLAUDE.md: the flat learnings views (memory/learnings/_views/<ns>.jsonl, and the
retired .gstack learnings*.jsonl) exceed the tool-result cap, keep growing, and a
whole-file read truncates SILENTLY. The only sanctioned access is
`py learnings.py list` (--grep / --skill / --full / --namespace / bare index).

Denies:
  - Read tool on any learnings*.jsonl or memory/learnings/_views/*.jsonl
  - Bash / PowerShell commands that dump one with a whole-file reader
    (cat, type, Get-Content/gc, more, less, Out-String, Import-Csv, ...)
  - head/tail with a count >= 200 lines on the store

Allows targeted access (grep, head/tail with a small count, wc, jq, py scripts).
Configured in .claude/settings.json under "PreToolUse" with matcher
"Read|Bash|PowerShell".
"""
import json
import re
import sys

STORE_RE = re.compile(
    r"(?:learnings[\w.-]*|_views[\\/][\w-]+)\.jsonl(?:\.bak[\w.-]*)?", re.IGNORECASE
)
WHOLE_READERS = re.compile(
    r"(?<![\w-])(cat|type|more|less|gc|Get-Content|Out-String|Import-Csv|"
    r"Out-File|Copy-Item|cp)(?![\w-])",
    re.IGNORECASE,
)
REASON = (
    "learnings*.jsonl / _views/*.jsonl must not be read whole — it exceeds the tool-result cap "
    "and truncates silently (CLAUDE.md). Query it instead, from the Playground root: "
    "py learnings.py list --grep <term> | --skill <task> | --full KEY... | --namespace <ns>."
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


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        sys.exit(0)

    tool = data.get("tool_name") or ""
    ti = data.get("tool_input") or {}

    if tool == "Read":
        fp = ti.get("file_path") or ""
        if STORE_RE.search(fp.replace("\\", "/")):
            deny(REASON)
        sys.exit(0)

    if tool in ("Bash", "PowerShell"):
        cmd = ti.get("command") or ""
        if not STORE_RE.search(cmd):
            sys.exit(0)
        if WHOLE_READERS.search(cmd):
            deny(REASON)
        # head/tail default to 10 lines; a large explicit count is a whole-read in disguise.
        m = re.search(r"\b(head|tail)\b[^|;&]*?-(?:n\s*|c\s*)?(\d+)", cmd)
        if m and int(m.group(2)) >= 200:
            deny(REASON)
    sys.exit(0)


if __name__ == "__main__":
    main()
