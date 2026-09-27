# Release Note

## Skill
- Skill slug: episode-guide
- Display name: Episode Guide
- Version: v1.0
- Release date: 2026-09-27
- Owner: BW Mason

## What changed
- Added a new canonical skill under `skills/episode-guide/`
- Tiered season guides (Series Best, God Mode, Fan Favorite, Core Arc, Skim, Skippable) with a separate arc flag
- Long-series mode with an Arc-Only Path, plus a fallback order for blocked sources

## Why this release matters
- One reusable prompt that answers "what's worth watching and what can I skip" for any long-running show, podcast, or franchise.

## Testing completed
- Example prompt/file tested: full run on Supernatural (15 seasons, 327 episodes), published as an HTML watch guide
- Output reviewed by: BW Mason
- Known limitations: Reddit and Fandom pages were blocked during testing, so per-episode IMDb scores came from secondary articles; late seasons of long shows may have too little data to call skips

## Deployment status
- Packaged `skill.zip`: No
- Uploaded to personal workspace: Yes (Claude)
- Uploaded to enterprise/UMD workspace: No
- Shared with colleagues: No

## Notes for future revision
- Consider an optional "watched" checklist output for long series
- Test on a podcast and a movie franchise to validate those paths
