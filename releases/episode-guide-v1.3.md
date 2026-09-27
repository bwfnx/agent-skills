# Release Note

## Skill
- Skill slug: episode-guide
- Display name: Episode Guide
- Version: v1.3
- Release date: 2026-09-27
- Owner: BW Mason

## What changed
- Optional family flag for watching with kids, calibrated to the child's age: Kid pick, Not for this age (with a one-line reason), or unmarked
- The flag is separate from quality tiers, so a God Mode episode can still carry a warning, and an average episode can be a top kid pick
- New Family Path output: kid picks in air order plus a "hold off until they're older" list
- Parent-focused sources added to research (Common Sense Media, IMDb Parents Guide, "best episodes for kids" lists); no kid call is made on a guess

## Why this release matters
- Quality and suitability are different questions. The best Star Trek episodes include some of its scariest.

## Testing completed
- Example prompt/file tested: Star Trek: The Next Generation for a 6-year-old (178 episodes). 8 kid picks, 9 hold-off warnings including two God Mode episodes. Community run confirmed the v1.2 clip-show parody exception ("Paradigms of Human Memory" tiered God Mode, not skipped).
- Output reviewed by: BW Mason
- Known limitations: parent sources cover a small share of episodes, so most entries stay unmarked for kids

## Deployment status
- Packaged `skill.zip`: No
- Uploaded to personal workspace: Yes (Claude, via repo pull)
- Uploaded to enterprise/UMD workspace: No
- Shared with colleagues: No

## Notes for future revision
- Test on a podcast and a movie franchise
- Consider age bands (under 7, 7–10, 11+) if multiple kids watch together
