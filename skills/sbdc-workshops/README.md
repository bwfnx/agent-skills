# SBDC Workshops

Version: v1.0

## Purpose

Turns an old SBDC class deck or script into the full modern package: a branded HTML deck that reveals one idea per click, a Google Form worksheet the room fills in through QR codes, an automatic follow-up email with each attendee's own answers plus the handout and slides, a PDF of the deck, and a presenter run sheet.

## Install (Claude Code)

```bash
gh repo clone bwfnx/agent-skills "$TEMP/agent-skills" && cp -r "$TEMP/agent-skills/skills/sbdc-workshops" ~/.claude/skills/
```

Then say "SBDC Workshops, do Session 2" in Claude Code.

Needs: Python with `qrcode` (and `pymupdf` for the PDF check), Microsoft Edge for the PDF export, and Claude in Chrome signed in to the Google account that owns the forms.

## Typical inputs

- the session's source script (slides, speaker notes, graphic suggestions)
- the calendar event (date, time, Zoom link)
- the handout file for that session

## Typical outputs

- `<class>.html` deck in the Maryland SBDC design system, with P for a presenter window and Ctrl+P for a one-slide-per-page PDF
- a published Google Form worksheet whose sections match the deck's checkpoint slides
- an on-submit follow-up email (bound Apps Script) with test, preview and resend functions
- a private run-sheet artifact for the day of the class

## What's inside

- `SKILL.md` - the workflow, the series schedule, verification, and Apps Script editor mechanics
- `scripts/deck/engine.py` - deck engine; `session1_example.py` is the worked example (Session 1, Sept 28, 2026)
- `scripts/apps-script/form_builder.gs`, `followup_email.gs` - form and email templates, configured at the top
- `assets/run-sheet-example.html` - the Session 1 run sheet to adapt
