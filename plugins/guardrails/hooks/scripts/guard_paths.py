#!/usr/bin/env python3
"""PreToolUse guard — enforce the CLAUDE.md write rules deterministically.

- memory/learnings/  : ALL hand-edits blocked. These files are managed by
                       `py learnings.py` (add | list | compile | prune).
- raw/               : modifying an EXISTING file is blocked ("add only,
                       never modify"). Creating a NEW raw source file is allowed.
                       Applies to every raw/ folder in the project — the root
                       one and each context's (sbdc-advising/raw, northfork-farm/raw,
                       ...) — but not to .git, worktrees, or _archive.

Blocks by emitting a PreToolUse "deny" decision to stdout. Anything else passes
silently (exit 0, no output = no opinion, normal permission flow continues).
Configured in .claude/settings.json under "PreToolUse" with matcher
"Write|Edit|MultiEdit|NotebookEdit".
"""
import json
import os
import sys


def project_root():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


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
    target = os.path.abspath(fp if os.path.isabs(fp) else os.path.join(root, fp))

    def under(subdir):
        base = os.path.abspath(os.path.join(root, subdir))
        return target == base or target.startswith(base + os.sep)

    def in_any(dirname):
        """True if `target` sits inside a directory named `dirname` anywhere
        under the project root (any depth), ignoring .git / worktrees / _archive."""
        if not (target == root or target.startswith(root + os.sep)):
            return False
        rel = os.path.relpath(target, root).split(os.sep)
        if rel[0] in (".git", ".claude", "_archive"):
            return False
        return dirname in rel[:-1]

    if under("memory/learnings"):
        deny("memory/learnings/ is managed by `py learnings.py` "
             "(add | list | compile | prune) — hand-editing these files is "
             "disallowed by CLAUDE.md. Use the helper to add or change a learning.")

    if in_any("raw") and os.path.exists(target):
        deny("raw/ is add-only: existing source files must never be modified "
             "(CLAUDE.md). Add a NEW file to raw/ to capture new source material, "
             "or write derived content to outputs/ or wiki/ instead.")

    sys.exit(0)


if __name__ == "__main__":
    main()
