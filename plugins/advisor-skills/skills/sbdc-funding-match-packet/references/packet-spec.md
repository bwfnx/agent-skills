# Packet spec — content, structure, and interactive hooks

Build ONE self-contained HTML file. Inline `design-system.css` in a `<style>` and
`interactivity.js` in a `<script>` at the end of `<body>`. The scripts wire
themselves up by the exact hooks below — if a hook is missing, that feature
silently does nothing. `scaffold.html` in this folder is a minimal working
skeleton with every hook already in place; copy it and fill in real content.

## Header / toolbar (required hooks)
Accessibility toolbar buttons, by `id`:
- `tplus` — increase text size · `tminus` — decrease · `treset` — reset
- `hc` — toggle `.hc` high-contrast class on `<html>`

The CSS drives text size from the `--fs` custom property on `:root`; the JS sets
it. Nothing else to wire for the toolbar.

Header should carry: advisor name + SBDC center, "Weekly Funding Opportunity
Match Packet", the week-of date, the opportunity/client windows, and a visible
**Draft only — review before acting** status.

## The eight sections (in order)

1. **Executive snapshot** — count tiles (new opps, carry-forward, clients
   reviewed, scored matches) and one **"Start here, one thing"** hero naming the
   single most time-sensitive action. Include a short "also time-sensitive" list
   of near deadlines.
2. **New opportunities** (new-this-week window) — one card each: name, funder,
   one-line description, deadline, award, eligibility, source (sender + date).
   Home-geo and state first.
3. **Carry-forward opportunities** — same card format; end with a one-line
   "expired since last review, don't chase" note.
4. **Recently active clients reviewed** — full profiles for clients with real
   records (business, last activity, sector, geography, stage, readiness, and a
   `[not found - confirm]` list of missing eligibility facts). Put intake-only
   clients behind a `<details>` disclosure.
5. **Client–opportunity match table** — see hooks below.
6. **Reach-out checklist** — see hooks below.
7. **Outreach drafts** — in the advisor's voice, short, one clear next step each,
   labeled *Draft · not sent*. Nothing is ever sent.
8. **Internal notes** — advisor-only observations (label noise, timing
   mismatches, handoffs, eligibility rules to screen, data-confidence caveats,
   {{CRM}} housekeeping).

## Deadline countdowns (required hooks)
Any element that should show a live countdown chip:
```html
<div class="deadrow" data-deadline="2026-08-21">
  … opportunity summary …
  <span class="cd"></span>   <!-- JS fills this: "Closes tomorrow", "In five days", "Closed" -->
</div>
```
`data-deadline` must be ISO `YYYY-MM-DD`. The JS recomputes on every open and adds
`is-closed` to past rows; chip classes `cd-now/cd-soon/cd-mid/cd-far/cd-closed`
are styled by the CSS.

## Match table (required hooks)
```html
<section id="matches">
  <div class="controls">
    <button class="chip active" data-geo="all">All</button>
    <button class="chip" data-geo="local">Local</button>
    <button class="chip" data-geo="state">State</button>
    <button class="chip" data-geo="federal">Federal / National</button>
    <label><input type="checkbox" id="condOnly"> Conditional only</label>
    <button id="sortToggle">Sort: highest score</button>
    <span id="matchCount"></span>
  </div>
  <table class="matchtable"><tbody>
    <tr data-score="88" data-geo="local" data-read="strong"> … </tr>
    <tr data-score="87" data-geo="federal" data-read="conditional"> … </tr>
  </tbody></table>
  <details> … lower-scored matches … </details>
</section>
```
Each match `<tr>` needs `data-score` (0–100), `data-geo`
(`local`/`state`/`federal`), and `data-read` (`strong`/`solid`/`developmental`
plus `conditional` when an eligibility fact is open — the "Conditional only"
filter matches `data-read="conditional"`). Columns: Client, Opportunity, Geo,
Score, Read, "Why / what's open".

## Reach-out checklist (required hooks)
```html
<ul id="reachList">
  <li role="checkbox" aria-checked="false" tabindex="0"> … action … </li>
</ul>
<span id="checkProg"></span>   <!-- JS keeps a "two done, three to go" tally -->
```
Items toggle `.done` on click or Space/Enter; `#checkProg` updates automatically.

## Copy guardrails
- Draft only; nothing sent. Outreach drafts say so.
- Conditional matches name exactly what's open; missing facts read
  `[not found - confirm]`.
- Never assert an eligibility rule without verifying it live that run.
- Home geography first, then state, then federal/national.
- Keep the SBDC voice: plain, specific, one next step per action.
