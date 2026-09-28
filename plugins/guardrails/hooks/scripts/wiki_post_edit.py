#!/usr/bin/env python3
"""PostToolUse check — light wiki hygiene reminder (non-blocking).

After an Edit/Write to a .md file inside a wiki folder (folder names from
.claude/guardrails.json `wiki_dirs`, default ["wiki"]), surfaces a note if the
file lacks a one-paragraph summary near the top or isn't listed in that folder's
INDEX.md. Never blocks; prints a systemMessage only.

Configured in .claude/settings.json under "PostToolUse" with matcher
"Write|Edit|MultiEdit".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load as load_config, project_root  # noqa: E402


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        sys.exit(0)

    tool_input = data.get("tool_input") or {}
    fp = tool_input.get("file_path") or tool_input.get("path")
    if not fp:
        sys.exit(0)

    root = os.path.abspath(project_root())
    target = os.path.abspath(fp if os.path.isabs(fp) else os.path.join(root, fp))

    if not target.lower().endswith(".md"):
        sys.exit(0)
    if not (target == root or target.startswith(root + os.sep)):
        sys.exit(0)
    rel = os.path.relpath(target, root).split(os.sep)
    wiki_dirs = load_config(root).get("wiki_dirs") or ["wiki"]
    hits = [i for i, part in enumerate(rel[:-1]) if part in wiki_dirs]
    if rel[0] in (".git", ".claude", "_archive") or not hits:
        sys.exit(0)
    # The wiki folder is the nearest ancestor with a configured name; INDEX.md lives there.
    wiki_depth = hits[-1] + 1
    wiki = os.path.join(root, *rel[:wiki_depth])

    stem = os.path.splitext(os.path.basename(target))[0]
    if stem.upper() == "INDEX":
        sys.exit(0)

    try:
        with open(target, encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
    except Exception:  # noqa: BLE001
        sys.exit(0)

    # Strip YAML frontmatter, then look for a prose (non-heading) line.
    body = []
    in_fm = False
    for i, ln in enumerate(lines):
        if i == 0 and ln.strip() == "---":
            in_fm = True
            continue
        if in_fm:
            if ln.strip() == "---":
                in_fm = False
            continue
        body.append(ln)
    prose = [l for l in body if l.strip() and not l.lstrip().startswith("#")]

    notes = []
    if not prose:
        notes.append("no one-paragraph summary near the top")

    idx = os.path.join(wiki, "INDEX.md")
    if os.path.isfile(idx):
        try:
            with open(idx, encoding="utf-8", errors="replace") as f:
                idx_txt = f.read()
            if stem not in idx_txt and os.path.basename(target) not in idx_txt:
                notes.append("not listed in wiki/INDEX.md")
        except Exception:  # noqa: BLE001
            pass

    if notes:
        msg = (f"Wiki hygiene — {os.path.basename(target)}: " + "; ".join(notes) +
               ". Every wiki file should open with a one-paragraph "
               "summary, appear in INDEX.md, and link related topics with [[...]].")
        print(json.dumps({"systemMessage": msg}))
    sys.exit(0)


if __name__ == "__main__":
    main()
