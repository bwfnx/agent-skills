# durable-learning

**Your AI agents stop repeating the same mistakes: they save what they learn, score it before keeping it, and read it back at the start of every session.**

What the agent sees when a session opens in a project with a store (real output, fictional data):

```text
Durable learnings: 4 active in memory/learnings/ (client-harbor-bakery, global, work). Query before multi-step work; an entry that contradicts your plan wins.
CLI: python3 ".../durable-learning-protocol/scripts/learnings.py"
  list --grep <term>      full rows matching a term
  list --full KEY [KEY]   full rows by key
  add --namespace <ns> --key <kebab-key> --insight "..."   the only way to write
Known pitfalls (mistakes already made once): crm-bcc-postbox, invoice-export-utf8
```

And one learning, as the agent pulls it with `list --grep crm` (two empty fields trimmed):

```json
{"namespace": "work", "memory_type": "semantic", "type": "pitfall", "key": "crm-bcc-postbox",
 "insight": "The CRM logs a meeting only if the follow-up email BCCs its postbox address.",
 "confidence": 9, "usefulness": 9, "source": "user-stated",
 "evidence": "Two follow-ups went unlogged before this was found.",
 "status": "active", "lifecycle": "stable", "review_after": null, "saved": "2026-09-29"}
```

New to plugins? Read the [plain-language guide](https://bwfnx.github.io/agent-skills/guides/durable-learning.html) first.

## Install

```bash
claude plugin marketplace add bwfnx/agent-skills
claude plugin install durable-learning@bwfnx
```

Then, in any project, ask for it at the end of real work: "save the durable learnings from this." The first `add` creates `memory/learnings/`. From the next session on, the hooks load it automatically.

Needs Python 3 on PATH (`python3`, `py`, or `python`). No other dependencies.

## Why not just a notes file?

Most agent-memory setups are a markdown file the agent appends to. That works until it doesn't: everything gets saved, nothing gets retired, two agents write at once and one loses, and the file grows past what the agent can read in one go. This plugin is the version that survives months of daily use across several agents.

| | Notes file | durable-learning |
|---|---|---|
| **What gets saved** | Whatever the agent felt like writing | Only learnings scoring **8+ on both confidence and usefulness**; the rest are proposed for you to approve |
| **Where it came from** | Unknown | `source`: you said it, the agent observed it, or the agent inferred it (inferred scores lower) |
| **Contexts** | One pile | Namespaces (`work`, `personal`, `client-acme`) so one client's rules never leak into another's |
| **Going stale** | Never noticed | `lifecycle` + `review_after` dates; `prune` lists what's expired, superseded, or deprecated |
| **Changing your mind** | Edit or delete, history lost | `retire OLD --by NEW`: the old entry stays, marked superseded, pointing at its replacement |
| **Several agents at once** | Merge conflicts, lost appends | One file per learning. Parallel agents never touch the same file |
| **Reading it back** | Agent has to remember to look | SessionStart hook injects the count, namespaces, and top pitfalls every session |
| **Keeping it clean** | Agents hand-edit freely | Hooks deny hand edits to the store and whole-file dumps of the compiled views |

## What's inside

| Piece | What it does |
|---|---|
| `durable-learning-protocol` skill | The judgment: what's worth keeping, how to classify it (`semantic`, `episodic`, `procedural`, `investigation` × `preference`, `pattern`, `pitfall`, `tool`, `operational`), how to score it, when to save versus propose |
| `learnings.py` | The only writer. `add`, `list` (index, `--grep`, `--skill`, `--full`), `retire`, `prune`, `compile`, `migrate` (split an old flat JSONL into per-entry files) |
| SessionStart hook | Loads the store summary and the highest-usefulness pitfalls into every new, resumed, cleared, or compacted session |
| PreToolUse hook | Denies Write/Edit and shell writes (`>`, `rm`, `mv`, `sed -i`, `Set-Content`, ...) inside `memory/learnings/`, and whole-file reads of `_views/*.jsonl`. `grep`, `git add`, and the CLI pass |

Both hooks are silent in projects without a `memory/learnings/` folder, so it's safe to install globally.

## Store layout

```text
memory/learnings/
  global/2026-09-29-never-send-without-approval.json
  work/2026-09-29-crm-bcc-postbox.json
  client-harbor-bakery/2026-09-29-harbor-bakery-owner-mornings.json
  _views/work.jsonl        # built by `compile`, read-only, query it, never dump it
```

Commit it with the rest of the project. Plain JSON diffs well, and git history becomes the audit trail. The store resolves from the git top-level of the current directory, or set `LEARNINGS_ROOT`.

## Without Claude Code

The skill runs anywhere skills do: the Claude app, Cowork, Codex (`agents/openai.yaml` is included). Zip `skills/durable-learning-protocol/` and upload it. Hooks are Claude Code only; elsewhere, put this line in your project instructions: "Before multi-step work run `learnings.py list --grep <term>`; write only with `learnings.py add`."

For the full multi-agent setup (commit identities, handoff log, protected raw folders), pair it with [`guardrails`](../guardrails/README.md).

## Self-check

```bash
python3 hooks/scripts/test_learnings_hooks.py
```

Prints `ok`. It builds a throwaway store, then exercises the CLI and both hooks.

## Changelog

- **v1.0** (2026-09-29): split out of `advisor-skills` into its own plugin. Added the SessionStart and guard hooks, `retire`, and open-ended namespaces (previously a fixed list).
