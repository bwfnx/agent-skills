#!/usr/bin/env python3
"""Shared config loader for the guardrails hooks.

Reads <project root>/.claude/guardrails.json if it exists. Every key is
optional; a missing file means "defaults", and the defaults have no opinion
about paths, reads, or commit identity. Only the git-safety checks (destructive
git asks, CRLF churn denied) are always on.
"""
import json
import os
import subprocess

DEFAULTS = {
    "commit_identities": None,      # regex the commit author name must match, or None
    "add_only_paths": [],           # folder names: existing files may not be modified
    "never_edit_paths": [],         # root-relative paths: no hand edits at all
    "never_read_whole": [],         # globs: deny whole-file reads (Read, cat, type, ...)
    "wiki_dirs": ["wiki"],          # folder names whose .md files need a summary + INDEX entry
    "handoff_file": "HANDOFF-LOG.md",
    "tasks_file": "TASKS.md",
}


def project_root():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def _git_toplevel(root):
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root,
                           capture_output=True, text=True, timeout=30)
        top = (r.stdout or "").strip()
        return top if r.returncode == 0 and top else None
    except Exception:  # noqa: BLE001
        return None


def load(root=None):
    """Load guardrails.json from the git top-level of `root` (or `root` itself
    if that lookup fails). `root` may be a subfolder, or a different repo than
    the session's project — callers that run git commands elsewhere (git_guard.py,
    git_post_commit.py) pass the directory the command actually runs in, not
    necessarily CLAUDE_PROJECT_DIR."""
    base = root or project_root()
    top = _git_toplevel(base) or base
    cfg = dict(DEFAULTS)
    p = os.path.join(top, ".claude", "guardrails.json")
    try:
        with open(p, encoding="utf-8") as f:
            cfg.update(json.load(f))
    except Exception:  # noqa: BLE001 - absent or malformed: defaults
        pass
    return cfg
