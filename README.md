# agent-skills — Brandon Mason's Claude setup

People kept asking how to make Claude work the way mine does. This repo is the answer: a plugin marketplace with the hooks, skills, and scheduled-task loops I run every day. One add command, then install what you want.

## Quick start (Claude Code)

```bash
claude plugin marketplace add bwfnx/agent-skills
claude plugin install guardrails@bwfnx
claude plugin install advisor-skills@bwfnx
```

Optional:

```bash
claude plugin install loops@bwfnx
claude plugin install sbdc-toolkit@bwfnx
```

**Cowork / Claude Desktop:** Settings → Plugins → Add marketplace → `bwfnx/agent-skills`, then enable the plugins you want. Hooks (`guardrails`) run in Claude Code only; everything else works in both.

## The four plugins

| Plugin | What you get | Docs |
|---|---|---|
| `guardrails` | Hooks: destructive git asks first, line-ending-churn commits are refused, session start/end protocol, protected paths, big-file read guard. Per-project rules via `.claude/guardrails.json`. | [plugins/guardrails](plugins/guardrails/README.md) |
| `advisor-skills` | Ten skills: SBIR proposal review, funding match packet, wiki interview, teardown, build verification audit, durable learning protocol, AI analyst, transcript-to-wiki pipeline, chief of staff, email follow-ups. | [plugins/advisor-skills](plugins/advisor-skills/README.md) |
| `loops` | Twenty-three scheduled-task templates (daily brief, post-meeting sweep, weekly reports, wiki audits) with placeholders for your email, CRM, and workspace. | [plugins/loops](plugins/loops/README.md) |
| `sbdc-toolkit` | The Maryland SBDC advisor toolkit, 14 client-facing skills. Lives in its own repo, [bwfnx/sbdc-toolkit](https://github.com/bwfnx/sbdc-toolkit); this marketplace points at it. | that repo's README |

## Third-party marketplaces I also run

These are not mine; they're what fills the other 10%.

```bash
claude plugin marketplace add obra/superpowers          # brainstorming, planning, TDD, debugging workflow
claude plugin marketplace add mvanhorn/last30days-skill  # what people are saying about a topic right now
claude plugin marketplace add coreyhaines31/marketingskills
claude plugin marketplace add wshobson/agents
claude plugin marketplace add jamie-bitflight/claude_skills
claude plugin marketplace add sickn33/agentic-awesome-skills
claude plugin marketplace add Imbad0202/academic-research-skills
```
Ponytail (lazy-senior-developer mode) comes from the Claude Desktop plugin directory.

## Starter `CLAUDE.md`

Drop this at the root of any workspace you want Claude to treat as a shared, long-lived knowledge base:

```markdown
## Rules
- `raw/` holds unprocessed source material. Never modify an existing file there; add new ones.
- `wiki/` is maintained by the AI. Every article opens with a one-paragraph summary and is listed in `wiki/INDEX.md`.
- `outputs/` holds generated reports and drafts.
- Durable learnings live in `memory/learnings/<namespace>/` and are managed only by `scripts/learnings.py` (from the durable-learning-protocol skill). Query with `py learnings.py list --grep <term>`; never dump the store whole.
- Before stopping: commit as your identity, prepend a dated entry to `HANDOFF-LOG.md` (what changed, what's next, files touched, open questions), push.
```

With `guardrails` installed, copy `plugins/guardrails/guardrails.example.json` to `.claude/guardrails.json` and those rules are enforced, not just requested.

## Settings snippet

`~/.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "guardrails@bwfnx": true,
    "advisor-skills@bwfnx": true,
    "loops@bwfnx": false,
    "sbdc-toolkit@bwfnx": true
  }
}
```

## License

MIT. The skills describe how I work; adapt freely.
