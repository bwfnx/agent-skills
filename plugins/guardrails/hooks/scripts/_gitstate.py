#!/usr/bin/env python3
"""Shared helper for session_start.py / session_end_check.py.

dirty_state(root) -> {path: "XY:<blob-hash>"} for every `git status --porcelain`
entry. The hash is of the working-tree content (empty for deletions), so a file
that was already dirty at session start but edited again during the session is
still detected as changed.

All git I/O is done in BYTES and decoded as UTF-8: text=True would decode with
the Windows cp1252 codec and raise on any non-ASCII filename, silently emptying
the result (observed 2026-09-11 on this repo).
"""
import json
import os
import subprocess
import tempfile

SNAPSHOT_DIR = os.path.join(tempfile.gettempdir(), "claude-guardrails")


def _git(args, root, stdin=None, timeout=120):
    r = subprocess.run(["git", *args], cwd=root, input=stdin, capture_output=True, timeout=timeout)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


def dirty_state(root):
    code, porcelain = _git(["status", "--porcelain", "-z"], root, timeout=60)
    if code != 0:
        return None
    entries = [e for e in porcelain.split("\0") if e]
    paths, status = [], {}
    i = 0
    while i < len(entries):
        e = entries[i]
        xy, path = e[:2], e[3:]
        if xy[0] in ("R", "C"):  # rename/copy: the next entry is the origin path
            i += 1
        status[path] = xy
        if "D" not in xy:
            paths.append(path)
        i += 1
    hashes = {}
    if paths:
        try:
            _, out = _git(["hash-object", "--stdin-paths"], root,
                          stdin=("\n".join(paths) + "\n").encode("utf-8"))
            for path, h in zip(paths, out.split()):
                hashes[path] = h
        except Exception:  # noqa: BLE001 - hashes degrade to "", status still compares
            pass
    return {path: f"{xy}:{hashes.get(path, '')}" for path, xy in status.items()}


def snapshot_path(session_id):
    return os.path.join(SNAPSHOT_DIR, f"{session_id}.json")


def write_snapshot(root, session_id):
    if not session_id:
        return
    try:
        snap = dirty_state(root)
        if snap is None:
            return
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        with open(snapshot_path(session_id), "w", encoding="utf-8") as f:
            json.dump(snap, f)
    except Exception:  # noqa: BLE001 - never fail the session
        pass


def load_snapshot(session_id):
    if not session_id:
        return None
    try:
        with open(snapshot_path(session_id), encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return None
