#!/usr/bin/env python3
"""PreToolUse guard — protected paths, driven by .claude/guardrails.json.

- never_edit_paths : root-relative paths where ALL hand-edits are blocked
                     (e.g. a store managed by a script).
- add_only_paths   : folder NAMES (any depth) where modifying an EXISTING file
                     is blocked but creating a new one is allowed (e.g. raw/).

No config -> no opinion. Blocks by emitting a PreToolUse "deny"; anything else
passes silently. Wired under "PreToolUse" with matcher
"Write|Edit|MultiEdit|NotebookEdit".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load as load_config, project_root  # noqa: E402


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
    except Exception:  # noqa: BLE001 - malformed payload: don't interfere
        sys.exit(0)

    tool_input = data.get("tool_input") or {}
    fp = (tool_input.get("file_path")
          or tool_input.get("path")
          or tool_input.get("notebook_path"))
    if not fp:
        sys.exit(0)

    root = os.path.abspath(project_root())
    cfg = load_config(root)
    target = os.path.abspath(fp if os.path.isabs(fp) else os.path.join(root, fp))
    if not (target == root or target.startswith(root + os.sep)):
        sys.exit(0)
    rel = os.path.relpath(target, root).split(os.sep)
    if rel[0] in (".git", ".claude", "_archive"):
        sys.exit(0)

    for p in cfg.get("never_edit_paths") or []:
        base = os.path.abspath(os.path.join(root, p))
        if target == base or target.startswith(base + os.sep):
            deny(f"{p} is a managed store: hand edits are blocked by .claude/guardrails.json "
                 "(never_edit_paths). Use the script that owns it.")

    for name in cfg.get("add_only_paths") or []:
        if name.strip("/\\") in rel[:-1] and os.path.exists(target):
            deny(f"{name} is add-only (.claude/guardrails.json add_only_paths): existing files "
                 "must never be modified. Add a NEW file instead, or write derived content elsewhere.")

    sys.exit(0)


if __name__ == "__main__":
    main()
