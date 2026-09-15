# guardrails

Hooks that keep a git repo shared by several AI agents (and you) safe. Install once, then optionally drop a `.claude/guardrails.json` into any project to turn on the project-specific rules.

## Install

```bash
claude plugin marketplace add bwfnx/agent-skills
claude plugin install guardrails@bwfnx
```

Needs a Python 3 on PATH as `python3`, `py`, or `python`. The launcher picks the first that works; with none it logs one line and stays out of the way.

## What runs with no config

| Hook | When | What it does |
|---|---|---|
| git_guard | before Bash/PowerShell | `push --force`, `reset --hard`, `checkout -- <path>`, `restore`, `clean`, `branch -D`, `filter-repo` ask for confirmation. A commit whose diff is a line-ending rewrite (numstat disagrees with numstat -w) is refused; put `[crlf-ok]` in the command to allow it once. |
| git_post_commit | after `git commit` | Shows `git log -1 --stat` so you see what actually landed, and flags an empty commit. |
| session_start | session start/resume | `git fetch`, reports ahead/behind, injects the newest `HANDOFF-LOG.md` entries and the `## Active now` block of `TASKS.md` if those files exist. |
| session_end_check | on stop | One reminder if files changed during this session are still uncommitted. |
| wiki_post_edit | after editing `wiki/*.md` | Reminds you if the article has no opening summary paragraph or is missing from `INDEX.md`. Never blocks. |

`guard_paths` and `guard_big_reads` do nothing until configured.

## Per-project config: `.claude/guardrails.json`

Every key is optional. `guardrails.example.json` is the config the author runs.

| Key | Type | Effect |
|---|---|---|
| `commit_identities` | regex | Commit author name must match, or the commit is denied. Handy when several agents share a repo and each must sign its work. |
| `add_only_paths` | folder names | Existing files in any folder with this name can't be modified; new files can be added. Use for raw source material. |
| `never_edit_paths` | root-relative paths | No hand edits at all. Use for stores a script owns. |
| `never_read_whole` | globs | `Read`, `cat`, `type`, `Get-Content`, `cp`, and `head`/`tail` ≥ 200 lines are denied on matching files. Use for files that exceed the tool-result cap. |
| `wiki_dirs` | folder names | Which folders `wiki_post_edit` treats as wikis. Default `["wiki"]`. |
| `handoff_file` | file name | Default `HANDOFF-LOG.md`. |
| `tasks_file` | file name | Default `TASKS.md`. |

## Self-check

```bash
python3 hooks/scripts/test_guardrails.py
```
Prints `ok`.
