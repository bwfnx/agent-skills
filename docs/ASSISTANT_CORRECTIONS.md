# Assistant Corrections Registry

This file is the central registry for recurring corrections, gotchas, and implementation rules that should be applied in future skill work.

## Purpose
Use this file to capture corrections the user had to make after review so the same mistake is not repeated.

## How to use this registry
- Add one entry per correction.
- Make the rule explicit and operational.
- Include the affected area, example of the mistake, the corrected form, and the preventive rule.
- Prefer short, testable rules over vague advice.
- When a correction changes packaging, naming, formatting, or release behavior, update the relevant templates or repo docs too.

## Correction entries

### COR-001 — SKILL.md frontmatter name must use slug format
- Date logged: 2026-03-25
- Area: skill packaging and validation
- Mistake: used a spaced frontmatter name such as `competitive research analyst`
- Correct form: use a hyphenated slug such as `competitive-research-analyst`
- Preventive rule: the `name` field in `SKILL.md` frontmatter must always match slug format `your-skill-name`
- Validation check: before packaging or handing off a skill, confirm that `SKILL.md` frontmatter `name` is lowercase and hyphenated with no spaces
- Example:
  - correct: `name: competitive-research-analyst`
  - incorrect: `name: competitive research analyst`
- Follow-up action: treat this as a required pre-package checklist item for every skill

## Suggested next corrections to log
- packaging assumptions that caused install failures
- repo conventions that were missed during conversion
- metadata fields that need stricter validation before handoff
- repeated connector or tool limitations that require workaround steps
