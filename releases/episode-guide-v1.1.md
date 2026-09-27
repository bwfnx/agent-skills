# Release Note

## Skill
- Skill slug: episode-guide
- Display name: Episode Guide
- Version: v1.1
- Release date: 2026-09-27
- Owner: BW Mason

## What changed
- Long-series mode now picks a path by show type: Arc-Only Path for serialized shows, Best-Of Path for episodic ones (sitcoms, procedurals, docuseries), with mixed shows getting the arc path plus an offer
- Multi-part episodes that aired as one block are a single entry with a code range (e.g. S7E12–13)
- New rule for sources that disagree on season/episode numbering: pick one list, name it, stay consistent

## Why this release matters
- The v1.0 Arc-Only Path was pointless for episodic comedies; the Best-Of Path is the shortcut people actually want for those shows.

## Testing completed
- Example prompt/file tested: 30 Rock (7 seasons, 138 episodes), published as an HTML watch guide; MythBusters queued as the first docuseries test
- Output reviewed by: BW Mason
- Known limitations: few sources rank every episode of a sitcom, so skip lists stay short

## Deployment status
- Packaged `skill.zip`: No
- Uploaded to personal workspace: Yes (Claude, via repo pull)
- Uploaded to enterprise/UMD workspace: No
- Shared with colleagues: No

## Notes for future revision
- Validate the Best-Of Path on a docuseries (MythBusters) and a procedural
- Test on a podcast and a movie franchise
