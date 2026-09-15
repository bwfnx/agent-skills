# loops

Twenty-three scheduled-task templates that make up a daily and weekly operating rhythm. Install: `claude plugin install loops@bwfnx`.

## Two ways to use a loop

1. **Scheduler.** Open the loop's `SKILL.md`, copy everything below the frontmatter, and paste it as the prompt of a scheduled task in Cowork or claude.ai. The `> **Schedule:**` line tells you the cadence the author runs it on.
2. **By hand.** Run `/loops:<name>` in Claude Code when you want one pass now.

## Before you run one

Each loop opens with three lines: what schedule it expects, which connectors it needs (`Needs:`), and which helper scripts it calls (`Helper scripts (yours, not included):`). The scripts are the author's internal tooling and are **not** shipped; a loop that lists one expects you to substitute your own script or drop that step.

Placeholders to replace, or leave for the loop to ask about:

| Placeholder | Meaning |
|---|---|
| `{{YOUR_EMAIL}}` | Your address |
| `{{COLLEAGUE_EMAIL}}` | A colleague or client address the original loop named |
| `{{CRM}}` | Your CRM or case-management system |
| `{{CRM_LOGGING_ADDRESS}}` | The BCC address your CRM uses to capture email |
| `{{WORKSPACE_ROOT}}` | The folder your notes, wiki, and outputs live in |
| `{{ORG}}` | Your organization |
| `{{USER}}` | You |

## The loops

| Loop | Rhythm | What it does |
|---|---|---|
| daily-central | daily, early morning | Builds and sends the day's brief from the ledger, calendar, and mail follow-ups |
| reply-clear | daily, after the brief | Reads replies to the brief and closes or reopens the items they name |
| sbdc-daily-meeting-prep-neoserra-drafts | daily | Prep packet and CRM drafts for today's client meetings |
| sbdc-post-meeting | daily, midday | Safety-net sweep and dispatcher for post-meeting processing |
| weekly-action-report | Friday afternoon | Weekly action-log entry from mail, calendar, and sessions |
| email-to-playground | weekly | Pulls self-sent tagged emails and attachments into the workspace |
| tasks-open-loop-weekly-reconciliation | weekly | Closes what the evidence proves done, flags what's stale |
| sbdc-weekly-funding-match | weekly | Funding-opportunity to client matching packet |
| sbdc-zoom-pipeline-weekly | Monday evening | Scans the Zoom archive and drafts write-ups for new transcripts |
| sbdc-ai-coworking-agenda-prep | Monday morning | Agenda packet for a weekly AI co-working hour |
| sbdc-ai-coworking-post-session-capture | weekly, after the session | Capture packet for the co-working hour |
| co-working-hour-guide-rebuild | weekly | Refreshes the published co-working guide |
| raw-to-wiki-nightly-ingest | nightly | New raw files → wiki articles → rebuild → publish |
| raw-folder-sensitive-data-scan | weekly | Flags newly added sensitive client data in raw folders |
| sbdc-wiki-weekly-insights | weekly | Incremental wiki synthesis and rebuild |
| fnx-pearl-wiki-weekly-insights | weekly | Same, second knowledge base |
| northfork-wiki-weekly-insights | weekly | Same, third knowledge base |
| personal-wiki-weekly-insights | weekly | Same, personal knowledge base |
| fnx-pearl-weekly-pipeline-cockpit | weekly | Pipeline, proposal, invoice, and follow-up cockpit |
| wiki-biweekly-audit | every two weeks | Wiki content audit |
| wiki-system-biweekly-audit | every two weeks | Wiki health: orphans, broken links, stale entries |
| tech-team-monthly-meeting-prep | monthly | Prep packet for a recurring team meeting |
| playground-monthly-audit | monthly | Workspace completeness, backups, orphaned folders |
