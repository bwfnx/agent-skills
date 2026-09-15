#!/usr/bin/env python3
"""Stop hook — nudge the session-end protocol beat.

If the working tree has uncommitted changes that appeared or changed DURING
this session, this fires ONE blocking reminder to commit the work authored as
your identity and to prepend a HANDOFF-LOG.md entry before stopping. Files that
were already dirty when the session started (the pre-existing backlog) are
ignored, using the snapshot session_start.py wrote for this session_id. With
no snapshot (session started before that hook existed) it falls back to
nagging about every dirty file. Guarded by `stop_hook_active` so it fires at
most once and can never loop.

Configured in .claude/settings.json under "Stop".
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gitstate import dirty_state, load_snapshot  # noqa: E402
from _config import load as load_config, project_root  # noqa: E402


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        data = {}

    # Already re-entered from a prior Stop-hook block: don't nag again.
    if data.get("stop_hook_active"):
        sys.exit(0)

    root = project_root()
    try:
        now = dirty_state(root)
    except Exception:  # noqa: BLE001
        sys.exit(0)
    if not now:
        sys.exit(0)

    snap = load_snapshot(data.get("session_id"))
    if snap is None:
        changed = sorted(now)           # no baseline: fall back to everything dirty
        scope = "uncommitted file(s)"
    else:
        changed = sorted(p for p, v in now.items() if snap.get(p) != v)
        scope = "file(s) changed during this session"
    if not changed:
        sys.exit(0)

    n = len(changed)
    listed = ", ".join(changed[:10]) + (f" (+{n - 10} more)" if n > 10 else "")
    handoff = load_config(root).get("handoff_file") or "HANDOFF-LOG.md"
    reason = (
        f"Session-end protocol not complete: {n} {scope}: {listed}. "
        "Before finishing: (1) commit the changes authored as your identity, "
        f"(2) prepend a dated {handoff} entry describing what changed, what's next, "
        "files touched, and any open question, then (3) push. "
        "If the work is intentionally left uncommitted, say so briefly and stop."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


if __name__ == "__main__":
    main()
