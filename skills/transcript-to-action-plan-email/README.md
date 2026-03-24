# Transcript to Action Plan Email

Turns SBDC client meeting transcripts into a NeoSerra-ready follow-up email plus a follow-up deliverables menu.

## Purpose
Use this skill when a consultant has a meeting transcript and wants:
- a polished client follow-up email
- meeting notes organized into the required sections
- milestone extraction
- a tailored follow-up menu for next deliverables

## Expected input
- transcript file or pasted transcript text

## Expected output
- email draft with required headers
- follow-up menu table with lettered options

## Key files
- `SKILL.md` - behavior and trigger description
- `agents/openai.yaml` - display metadata
- `scripts/transcript_extract.py` - helper extractor
- `references/` - formatting, milestones, and follow-up rules

## Release notes
See `CHANGELOG.md`.
