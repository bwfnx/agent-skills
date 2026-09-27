# Release Note

## Skill
- Skill slug: episode-guide
- Display name: Episode Guide
- Version: v1.4
- Release date: 2026-09-27
- Owner: BW Mason

## What changed
- When parent guides rate only the whole show, the guide reports the show-level age in a family note and leaves episodes unmarked instead of guessing
- New optional input for entries already watched: marked "seen," and paths start at the first unseen entry

## Why this release matters
- MythBusters showed the family flag had no fallback when parent sources rate only the show (Common Sense: 9+, no episode-level reviews). Star Wars showed the path should pick up from where a kid already is.

## Testing completed
- Example prompt/file tested: MythBusters (show-level rating only; family note added, no invented episode tags) and all 13 theatrical Star Wars films in release order for a 6-year-old who has seen Episodes IV and V (3 kid picks next, 3 parent's-call PG-13 films, 4 hold-offs)
- Output reviewed by: BW Mason
- Known limitations: "parent's call" is expressed as an unmarked entry with a note, not a formal state; revisit if it comes up again

## Deployment status
- Packaged `skill.zip`: No
- Uploaded to personal workspace: Yes (Claude, via repo pull)
- Uploaded to enterprise/UMD workspace: No
- Shared with colleagues: No

## Notes for future revision
- Consider a formal "parent's call" family state for entries just above the child's calibrated age
- Test on a podcast
