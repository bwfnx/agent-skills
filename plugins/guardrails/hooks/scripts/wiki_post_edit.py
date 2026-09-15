#!/usr/bin/env python3
"""PostToolUse check — light wiki hygiene reminder (non-blocking).

After an Edit/Write to a wiki/*.md article, surfaces a note if the file lacks a
one-paragraph summary near the top or isn't listed in that wiki's INDEX.md — the
two rules from CLAUDE.md most easily forgotten. Wikis live per context
(sbdc-advising/wiki, northfork-farm/wiki, ...; symlinked into wikis-git), so the
check matches any `wiki/` folder under the project and looks for INDEX.md in the
same wiki folder as the edited file. Never blocks (the edit already
happened); it only prints a systemMessage the user and model can see.

Configured in .claude/settings.json under "PostToolUse" with matcher
"Write|Edit|MultiEdit".
"""
import json
import os
import sys


def project_root():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


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
    if rel[0] in (".git", ".claude", "_archive") or "wiki" not in rel[:-1]:
        sys.exit(0)
    # The wiki folder is the nearest ancestor named "wiki"; INDEX.md lives there.
    wiki_depth = len(rel) - 1 - rel[:-1][::-1].index("wiki")
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
               ". CLAUDE.md asks every wiki file to open with a one-paragraph "
               "summary, appear in INDEX.md, and link related topics with [[...]].")
        print(json.dumps({"systemMessage": msg}))
    sys.exit(0)


if __name__ == "__main__":
    main()
