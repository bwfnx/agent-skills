#!/bin/sh
# guardrails hook launcher. Usage: sh run.sh <script.py>
# Picks the first Python that runs (python3, then the Windows py launcher, then
# python) and execs the hook script with the JSON payload still on stdin.
# A machine with no working Python gets a one-line stderr note and exit 0, so
# a missing interpreter never blocks a session.
here="$(cd "$(dirname "$0")" && pwd)"
script="$here/scripts/$1"
shift
for py in "python3" "py -3" "python"; do
  if $py -c "import sys" >/dev/null 2>&1; then
    exec $py "$script" "$@"
  fi
done
echo "guardrails: no working Python (tried python3, py -3, python); skipped $(basename "$script")" >&2
exit 0
