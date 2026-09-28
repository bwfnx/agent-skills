# Release Note

## Skill
- Skill slug: sbdc-workshops
- Display name: SBDC Workshops
- Version: v1.0
- Release date: 2026-09-28
- Owner: BW Mason

## What changed
- Added a new canonical skill under `skills/sbdc-workshops/`
- Deck engine, form builder and follow-up email templates, run-sheet example, and the full workflow in `SKILL.md`

## Why this release matters
- The Winning That Government Contracting Award series has three more sessions in eight days (Sept 30, Oct 2, Oct 5). Each one now follows the same proven build instead of being reinvented.

## Testing completed
- Example tested: Session 1, Business Development Lifecycle (Sept 28, 2026, Zoom)
- Engine regenerates the Session 1 deck byte-identical; form published and publicly reachable; test email and real-response preview both arrived with the handout and deck PDF attached
- Output reviewed by: BW Mason
- Known limitations: the Apps Script permission prompts and Drive uploads need Brandon's clicks; the Make a copy dialog does not take a typed name

## Deployment status
- Packaged `skill.zip`: No
- Uploaded to personal workspace: Yes (Claude Code, ~/.claude/skills)
- Uploaded to enterprise/UMD workspace: No
- Shared with colleagues: No

## Notes for future revision
- After Session 2, record what the second run needed that v1.0 did not cover
- Consider a class-file generator that drafts slides straight from the source script
