# Release Note

## Skill
- Skill slug: episode-guide
- Display name: Episode Guide
- Version: v1.2
- Release date: 2026-09-27
- Owner: BW Mason

## What changed
- Series Best must be a regular episode; retrospective and reunion specials can only be Fan Favorites
- Clip shows that reuse aired footage are Skippable by default
- Clip-show parodies made of new material are tiered like normal episodes

## Why this release matters
- On MythBusters, nostalgia specials outscored every real episode on IMDb, and the only defensible skips were recap clip shows. This makes both calls consistent.

## Testing completed
- Example prompt/file tested: MythBusters (docuseries, calendar-year seasons); Community queued to test the clip-show parody exception
- Output reviewed by: BW Mason
- Known limitations: docuseries often lack worst-episode lists, so skip lists stay short

## Deployment status
- Packaged `skill.zip`: No
- Uploaded to personal workspace: Yes (Claude, via repo pull)
- Uploaded to enterprise/UMD workspace: No
- Shared with colleagues: No

## Notes for future revision
- Test on a podcast and a movie franchise
