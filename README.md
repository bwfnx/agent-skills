# agent-skills

**Drop-in skills and plugins that make Claude do one job well, the same way every time.**

![Output of the episode-guide skill: a Supernatural watch guide with the Series Best, an Arc-Only Path, and season tables tagged God Mode, Fan Favorite, Core Arc, and Skip](assets/episode-guide-supernatural.png)
<sub>Real output from the <code>episode-guide</code> skill. See more in <a href="https://github.com/bwfnx/watch-guides">watch-guides</a>.</sub>

## Install

**Plugins (Claude Code):** add the marketplace once, then install what you want.

```bash
claude plugin marketplace add bwfnx/agent-skills
claude plugin install durable-learning@bwfnx
claude plugin install guardrails@bwfnx
claude plugin install advisor-skills@bwfnx
```

**A single skill (Claude Code):** copy its folder into your skills directory.

```bash
git clone https://github.com/bwfnx/agent-skills
cp -r agent-skills/skills/episode-guide ~/.claude/skills/
```

**Claude app, Cowork, or ChatGPT:** add the marketplace under Settings → Plugins (`bwfnx/agent-skills`), or zip a skill folder (for example `skills/episode-guide/`) and upload it wherever your app accepts skills. Hooks (`guardrails`) run in Claude Code only.

Then just ask for the job, like "best episodes of Supernatural, and what can I skip?"

## Start here: durable-learning

**Long-term memory your agents actually use.** At the end of real work the agent proposes what it learned, scores each item for confidence and usefulness, and saves only what clears 8/10 on both. Every new session opens with the store loaded, including the pitfalls it has already hit once. Hooks keep the store clean: one file per learning so parallel agents never collide, no hand edits, no dumping it whole.

```text
Durable learnings: 4 active in memory/learnings/ (client-harbor-bakery, global, work). Query before multi-step work; an entry that contradicts your plan wins.
Known pitfalls (mistakes already made once): crm-bcc-postbox, invoice-export-utf8
```

Namespaces per context, lifecycle and review dates, `retire --by` instead of deleting, and a comparison with a plain notes file: [plugins/durable-learning](plugins/durable-learning/README.md). New to plugins? The [plain-language guide](https://bwfnx.github.io/agent-skills/guides/durable-learning.html) walks through setup and what to say.

## Plugins

| Plugin | What you get | Docs |
|---|---|---|
| `durable-learning` | Scored, namespaced long-term memory: the protocol skill, `learnings.py`, and hooks that load it every session and keep it script-owned. | [plugins/durable-learning](plugins/durable-learning/README.md) |
| `guardrails` | Hooks: destructive git asks first, line-ending-churn commits are refused, session start/end protocol, protected paths, big-file read guard. Per-project rules via `.claude/guardrails.json`. | [plugins/guardrails](plugins/guardrails/README.md) |
| `advisor-skills` | Nine skills: SBIR proposal review, funding match packet, wiki interview, teardown, build verification audit, AI analyst, transcript-to-wiki pipeline, chief of staff, email follow-ups. | [plugins/advisor-skills](plugins/advisor-skills/README.md) |
| `loops` | Twenty-three scheduled-task templates (daily brief, post-meeting sweep, weekly reports, wiki audits) with placeholders for your email, CRM, and workspace. | [plugins/loops](plugins/loops/README.md) |
| `sbdc-toolkit` | The Maryland SBDC advisor toolkit, 14 client-facing skills. Lives in its own repo, [bwfnx/sbdc-toolkit](https://github.com/bwfnx/sbdc-toolkit); this marketplace points at it. | that repo's README |

## Standalone skills

| Skill | What it does | Status |
|---|---|---|
| [`episode-guide`](skills/episode-guide/) | Season-by-season guide to the best, essential, and skippable episodes of any show or film series, with an optional kid-safe path by age | Active · v1.5 |
| [`sbdc-workshops`](skills/sbdc-workshops/) | Rebuilds an SBDC class as a branded reveal deck, a QR worksheet form, and an automatic follow-up email | Active · v1.0 |
| [`transcript-to-action-plan-email`](skills/transcript-to-action-plan-email/) | Turns an SBDC client meeting transcript into a Neoserra-ready follow-up email and action plan | Active · v1.0 |
| [`competitive-research-analyst`](skills/competitive-research-analyst/) | Current, web-researched competitor, pricing, and market analysis for small businesses | Draft · v1.0 |

Full inventory: [`SKILLS_INDEX.md`](SKILLS_INDEX.md) · machine-readable: [`skills/manifest.json`](skills/manifest.json)

## How skills are built

Each standalone skill lives in `skills/<skill-slug>/` with a `SKILL.md` (the instructions), `agents/openai.yaml` (ChatGPT settings), a `README.md`, and a `CHANGELOG.md`. Plugins live in `plugins/<name>/` with a `.claude-plugin/plugin.json`, listed in `.claude-plugin/marketplace.json`. Every version is tested on real inputs before release; release notes are in [`releases/`](releases/).

Maintainer docs: [repo conventions](docs/REPO_CONVENTIONS.md) · [release workflow](docs/RELEASE_WORKFLOW.md) · [new-skill checklist](templates/SKILL_CHECKLIST.md)

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
- Durable learnings live in `memory/learnings/<namespace>/` and are managed only by `scripts/learnings.py` (from the `durable-learning` plugin). Query with `py learnings.py list --grep <term>`; never dump the store whole.
- Before stopping: commit as your identity, prepend a dated entry to `HANDOFF-LOG.md` (what changed, what's next, files touched, open questions), push.
```

With `guardrails` installed, copy `plugins/guardrails/guardrails.example.json` to `.claude/guardrails.json` and those rules are enforced, not just requested.

## Settings snippet

`~/.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "durable-learning@bwfnx": true,
    "guardrails@bwfnx": true,
    "advisor-skills@bwfnx": true,
    "loops@bwfnx": false,
    "sbdc-toolkit@bwfnx": true
  }
}
```

## License

MIT. The skills describe how I work; adapt freely.
