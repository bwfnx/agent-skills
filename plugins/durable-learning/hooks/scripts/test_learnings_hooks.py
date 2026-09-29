#!/usr/bin/env python3
"""Self-check: builds a throwaway store with learnings.py, then drives both hooks. Prints ok."""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "learnings_hooks.py")
CLI = os.path.normpath(os.path.join(
    HERE, "..", "..", "skills", "durable-learning-protocol", "scripts", "learnings.py"))


def run(args, root, stdin=""):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=root, LEARNINGS_ROOT=root)
    r = subprocess.run([sys.executable, *args], input=stdin, capture_output=True,
                       text=True, cwd=root, env=env)
    assert r.returncode == 0, r.stderr
    return r.stdout


def decision(root, tool, **tool_input):
    out = run([HOOK, "guard"], root, json.dumps({"tool_name": tool, "tool_input": tool_input}))
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out.strip() else "allow"


with tempfile.TemporaryDirectory() as root:
    assert run([HOOK, "session_start"], root) == "", "silent without a store"

    run([CLI, "add", "--namespace", "work", "--key", "crm-bcc-postbox", "--type", "pitfall",
         "--insight", "The CRM logs a meeting only if the email BCCs its postbox."], root)
    run([CLI, "add", "--namespace", "personal", "--key", "short-emails",
         "--insight", "Keep emails under five sentences."], root)
    run([CLI, "compile"], root)
    try:
        run([CLI, "add", "--namespace", "Bad Name", "--key", "x", "--insight", "x"], root)
        raise SystemExit("bad namespace was accepted")
    except AssertionError:
        pass

    ctx = json.loads(run([HOOK, "session_start"], root))["hookSpecificOutput"]["additionalContext"]
    assert "2 active" in ctx and "personal, work" in ctx and "crm-bcc-postbox" in ctx, ctx
    assert "2 learning(s)" in run([CLI, "list"], root)
    run([CLI, "retire", "short-emails", "--by", "crm-bcc-postbox"], root)
    assert "1 learning(s)" in run([CLI, "list"], root)
    assert "superseded" in run([CLI, "prune"], root)

    store = os.path.join(root, "memory", "learnings", "work", "x.json")
    view = os.path.join(root, "memory", "learnings", "_views", "work.jsonl")
    assert decision(root, "Write", file_path=store) == "deny"
    assert decision(root, "Edit", file_path=store) == "deny"
    assert decision(root, "Write", file_path=os.path.join(root, "notes.md")) == "allow"
    assert decision(root, "Read", file_path=view) == "deny"
    assert decision(root, "Read", file_path=store) == "allow"
    assert decision(root, "Bash", command="echo hi >> memory/learnings/work/x.json") == "deny"
    assert decision(root, "PowerShell", command="Set-Content memory\\learnings\\work\\x.json 'x'") == "deny"
    assert decision(root, "Bash", command="cat memory/learnings/_views/work.jsonl") == "deny"
    assert decision(root, "Bash", command="grep -i crm memory/learnings/_views/work.jsonl") == "allow"
    assert decision(root, "Bash", command="git add memory/learnings/work") == "allow"
    assert decision(root, "Bash", command="py learnings.py list --grep crm") == "allow"

print("ok")
