#!/usr/bin/env python3
"""Self-check for the guardrails hooks. Run: python3 test_guardrails.py

Each hook is run as a subprocess with a fake payload, once with no
.claude/guardrails.json (must have no opinion) and once with the example
config (must enforce it). Uses a throwaway git repo.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLE = os.path.join(HERE, "..", "..", "guardrails.example.json")


def hook(name, payload, root):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=root)
    r = subprocess.run([sys.executable, os.path.join(HERE, name)], input=json.dumps(payload),
                       capture_output=True, text=True, env=env, cwd=root, timeout=60)
    assert r.returncode == 0, (name, r.stderr)
    return json.loads(r.stdout) if r.stdout.strip() else {}


def decision(out):
    return (out.get("hookSpecificOutput") or {}).get("permissionDecision")


def sh(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def main():
    d = tempfile.mkdtemp()
    sh(["git", "init", "-q"], d)
    sh(["git", "config", "core.autocrlf", "false"], d)
    sh(["git", "config", "user.email", "t@t"], d)
    sh(["git", "config", "user.name", "Someone"], d)
    os.makedirs(os.path.join(d, "raw"))
    with open(os.path.join(d, "raw", "old.txt"), "w") as f:
        f.write("x\n")
    sh(["git", "add", "-A"], d)
    sh(["git", "commit", "-q", "-m", "init"], d)
    write_raw = {"tool_name": "Write", "tool_input": {"file_path": os.path.join(d, "raw", "old.txt"), "content": "y"}}
    commit = {"tool_name": "Bash", "tool_input": {"command": "git commit -m x"}}
    read_big = {"tool_name": "Read", "tool_input": {"file_path": os.path.join(d, "memory", "learnings", "_views", "global.jsonl")}}
    force = {"tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}}

    # no config: no opinion on paths, reads, or identity; destructive git still asks
    assert decision(hook("guard_paths.py", write_raw, d)) is None
    assert decision(hook("guard_big_reads.py", read_big, d)) is None
    assert decision(hook("git_guard.py", commit, d)) is None
    assert decision(hook("git_guard.py", force, d)) == "ask"
    assert "additionalContext" in hook("session_start.py", {"session_id": "s1"}, d)["hookSpecificOutput"]

    # with the example config: paths and reads denied, identity enforced
    os.makedirs(os.path.join(d, ".claude"))
    shutil.copy(EXAMPLE, os.path.join(d, ".claude", "guardrails.json"))
    assert decision(hook("guard_paths.py", write_raw, d)) == "deny"
    assert decision(hook("guard_big_reads.py", read_big, d)) == "deny"
    assert decision(hook("git_guard.py", commit, d)) == "deny"
    ok = {"tool_name": "Bash", "tool_input": {"command": 'git commit --author="Claude-umd <c@local>" -m x'}}
    assert decision(hook("git_guard.py", ok, d)) is None
    print("ok")


if __name__ == "__main__":
    main()
