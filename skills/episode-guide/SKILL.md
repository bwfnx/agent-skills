---
name: episode-guide
description: build a season-by-season guide to the best and most skippable episodes of any tv series, podcast, or movie franchise — god mode peaks, fan favorites, core arc episodes, skim and skippable filler, an arc-only path for long shows, and the single best episode of the series. use when asked for "best episodes of x", "what can i skip in x", "watch guide for x", or "is x worth finishing".
---

# Episode Guide

Produce a researched, spoiler-light guide that tells the user what to watch, what matters, and what to skip — season by season, in original release order.

## Inputs

- **Title** (required). If ambiguous (remakes, reboots, same-name shows), ask which one before researching.
- **Scope** (optional): whole series, specific seasons, or "just tell me what to skip."
- **Spoiler level**: default spoiler-light (see Rules). Honor "spoilers fine" or "zero spoilers" if the user says so.

Works for:
- **TV series** — seasons and episodes
- **Podcasts** — seasons, or years if the show has no seasons; entries are episodes
- **Movie franchises** — group by era or phase; entries are films

## Tiers

Assign every listed entry exactly one tier. Do not list unremarkable "fine" episodes unless the user asks for a complete list.

| Tier | Meaning | Test |
|---|---|---|
| 👑 **Series Best** | The single best entry of the whole run | Highest combined standing across all sources. Exactly one. |
| ⚡ **God Mode** | The show at its absolute peak | Rated well above the series average (roughly top 5–10%) AND appears on critic or major-outlet best-of lists |
| ❤️ **Fan Favorite** | Beloved rewatch staples | Strong fan ratings/polls or cultural staying power, even if critics are lukewarm |
| 🧵 **Core Arc** | Needed to follow the main story | Advances the central mythology, character arcs, or sets up payoffs. Not necessarily great. |
| 👀 **Skim** | Weak episode with a few scenes that matter | Below average, but contains a key scene, reveal, or introduction. Name what to catch ("watch the last 5 minutes") without spoiling it. |
| ⏭️ **Skippable** | Safe to skip | Below the series average AND standalone with no arc impact. Must meet both. |

If an entry qualifies for multiple tiers, use the highest (Series Best > God Mode > Fan Favorite > Core Arc > Skim). A skippable episode can never also be Core Arc or Skim — if anything in it matters to the story, it is not skippable, however bad it is.

**Arc flag (separate from tier).** Tag every entry the main story needs as `arc: yes`, whatever its tier. A Fan Favorite or God Mode episode can also be arc-essential ("Tall Tales", "Death's Door"), and the tier alone would hide that. Show the flag in the table ("also needed for the arc") and use it to build the Arc-Only Path.

## Research

Blend sources and cite them. Search each separately rather than in one combined query.

1. **Ratings**: IMDb episode ratings (or Rotten Tomatoes / Letterboxd for films; Apple/Spotify ratings and listener rankings for podcasts). Note the series average so "above average" means something.
2. **Critics**: best-episode lists from major outlets (Vulture, The A.V. Club, Rolling Stone, IGN, Collider, etc.).
3. **Fans**: Reddit threads and polls ("best episode of X", "what can I skip in X", "filler episodes X"), fan wikis for arc/mythology tags.
4. **Arc mapping**: fan wikis or episode guides that label mythology vs. standalone ("monster of the week") episodes.

Verify air dates and episode numbers against a reliable episode list (Wikipedia episode list or IMDb). Never guess an air date — if unverified, say so.

When sources disagree, note it briefly ("critics love it, fans are split").

**When a source is blocked or unreadable** (Reddit, Fandom wikis, and IMDb episode pages often refuse automated fetches), move down this fallback order instead of guessing:
1. IMDb-derived articles (Screen Rant, Collider, CheatSheet "highest-rated episodes" pieces) for ratings
2. Wikipedia per-episode pages, which often list critic scores (IGN, TV Fanatic, Den of Geek)
3. Long-form fan viewing guides on Medium, Substack, or fan sites for watch/skip calls
4. Critic "worst episodes" lists to confirm skip candidates

Say in the Sources section which sources were blocked. If a season still has too little data to call skips, leave its skip list empty and say so — never pad it.

## Long-series mode

Trigger when the series has **8+ seasons or 100+ episodes** (e.g., Supernatural, The Simpsons, Grey's Anatomy) or when the user asks for it.

In this mode:
- Be more aggressive about identifying ⏭️ Skippable standalones — this is the main value for long shows.
- Add an **Arc-Only Path**: the minimum list of episodes needed to follow the story — every entry flagged `arc: yes`, plus all ⚡ God Mode and the 👑 Series Best — in release order, with a total episode count and rough runtime saved. Include 👀 Skim entries with their "what to catch" note.
- Flag seasons that are weak overall ("Season 8 is widely considered a dip — arc-only is fine here").

## Output

### 1. Headline
- **👑 Series Best**: title, S#E#, original air date, one spoiler-light line on why.
- One sentence on the show's overall arc quality (e.g., "Peaks in seasons 2–5; later seasons are skim-friendly").

### 2. Season tables
One table per season, entries sorted by **original release date**:

| Ep | Title | Air date | Tier | Arc | Why (spoiler-light) |
|---|---|---|---|---|---|
| S1E03 | ... | 2005-09-27 | ⚡ God Mode | yes | One line that sells it without giving it away |

### 3. Season watch guides
Under each table, 2–4 sentences: how strong the season is overall, which episodes are non-negotiable, and what can safely be skipped. Keep it conversational.

### 4. Arc-Only Path (long-series mode only)
Numbered list in release order, plus: total episodes, episodes skipped, approximate hours saved.

### 5. Sources
Short list of links used.

## Rules

- **Spoiler-light by default**: describe the hook, tone, or stakes — never the twist, death, reveal, or ending. "A case goes sideways in a way that changes the show" is fine; "X dies" is not. Skip the one-liner entirely for episodes whose premise itself is a spoiler.
- **Release order only**: sort by original air/release date, not streaming or production order. Note it if the two differ meaningfully.
- **No filler padding**: if a season has no God Mode episodes, say so instead of stretching the tier.
- **Be honest about thin data**: for niche podcasts or obscure shows with few ratings, say the rankings rest on limited sources.
- **Keep one-liners to one line.**
- If the output is long (big series), offer the full guide as a document the user can keep, and give the headline + Arc-Only Path in chat.
