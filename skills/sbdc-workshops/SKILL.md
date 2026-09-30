---
name: sbdc-workshops
description: rebuild a maryland sbdc class (e.g. the "winning that government contracting award" series) the new way - html deck in the maryland sbdc design system with click-by-click reveal, a google form worksheet behind qr checkpoints, an automatic branded follow-up email with the attendee's own answers plus the handout and slides attached, a pdf of the deck, and a run sheet. use when brandon says "sbdc workshops", "do the next session", "rebuild the class for wednesday/friday", or hands over an old deck/script for a workshop.
---

# SBDC Workshops

One class = five deliverables, built the same way every time. Session 1 (Business Development Lifecycle, 2026-09-28) is the worked example; everything here was proven on it.

| # | Deliverable | Where it comes from |
|---|---|---|
| 1 | Deck: single HTML file, 16:9 stage, Maryland SBDC design, one bullet/graphic per click, P = presenter notes + timer, prints to PDF | `scripts/deck/engine.py` + a class file copied from `scripts/deck/session1_example.py` |
| 2 | Worksheet: Google Form, page 1 intake + one section per checkpoint slide + before-you-leave + staying-in-touch | copy of the Session 1 form + `scripts/apps-script/form_builder.gs` |
| 3 | Follow-up email: sent on submit, their answers, links, advising button, handout + slides PDF attached | `scripts/apps-script/followup_email.gs` in the same bound script |
| 4 | Deck PDF (for the email attachment) | headless Edge, see step 6 |
| 5 | Run sheet artifact: tonight / 20-min-before checklists, run of show, chat message for Diane, after-class steps | adapt `assets/run-sheet-example.html`, publish with the Artifact tool |

Output folder per class: `Claude Playground\sbdc-advising\outputs\<YYYY-MM-DD>-govcon-s<N>\`. Commit the class `.py`, `.gs` copies and any `.md`; the generated `.html`/`.png` are gitignored there.

## The series (source scripts are read-only in `sbdc-advising\raw\training-materials\GOVCON WORKSHOP APRIL 2026\`)

| Session | When (Zoom, host Diane McFarland) | Source script |
|---|---|---|
| 1 Business Development Lifecycle | Mon Sep 28, 10:00-11:30 | `2026-04-28-session-1-business-development-lifecycle.md` (done) |
| 2 Team Roles and Responsibilities | Wed Sep 30, 10:00-11:30 | `2026-04-29-session-2-team-roles-and-responsibilities.md` |
| 3 How to Read an RFP | Fri Oct 2, 10:00-11:30 | `2026-04-30-session-3-how-to-read-an-rfp.md` |
| 4 Basics of Proposal Writing | Mon Oct 5, 10:00-11:30 | `2026-05-01-session-4-basics-of-proposal-writing.md` |

Confirm the date and Zoom link on the UMD calendar before trusting this table. Handouts for each session sit in `FINAL DRAFT PRESENTATIONS AND HANDOUTS\`.

## Steps (about 2-3 hours of Claude time; Brandon's hands-on time is about 10 minutes, marked BRANDON)

1. **Read** the session's source script (slides + speaker notes + graphic suggestions) and the calendar event. Run `py learnings.py list --grep workshop` and `--skill sbdc-workshops` first.
2. **Deck.** Copy `scripts/deck/session1_example.py` into the class output folder as `build.py`. Keep the header lines and `engine.render(...)`; replace every slide between them. Rules that make it match:
   - Speaker notes come from the script; slide text is short (1-3 lines or 4-6 bullets). Turn each "Graphic Suggestion" into a real layout from the engine's CSS vocabulary: `tiers`, `stairs`, `timeline`, `phases`, `colorflow`, `four`, `gng`, `split`, `tiles`, `funnel`, `roles`, `stat`, `curve`, `compare`, `callout`, `cols2`, `card`. Read `session1_example.py` for how each is used.
   - Structure: title (QR) -> scan slide -> agenda -> section dividers per part -> 2 or 3 `checkpoint("Section A", ...)` slides at natural pauses -> takeaways -> "Submit your worksheet" -> Questions (signup QR + SBA notice). Checkpoint names must match the form sections (A, B, ...), and the last content slide points to the before-you-leave section.
   - Footer text: `"Session N &middot; <Title>"`. Title slide eyebrow: `"Winning That Government Contracting Award &middot; Session N of 4"`, date spelled out.
   - Contact on slides is `bwmason@umd.edu` (the April decks said bw@fnxpearl.com - do not carry that over).
   - Build with a placeholder form URL first (`engine.setup("https://forms.gle/REPLACE-ME")`), then rebuild after step 3.
3. **Form.** In Brandon's Chrome (claude-in-chrome, signed in as bwmason@umd.edu): open the Session 1 form editor `https://docs.google.com/forms/d/1fktLVyhvAlNcZtlDmwSIRHHyYo83DyJ829kXfnFQH-A/edit` -> More -> Make a copy -> Make a copy. It opens in a new tab. Close the tab holding the original so nothing edits it. In the copy: More -> Apps Script. The copy brings along Session 1's bound script (the email code with Session 1 settings); its trigger does not copy, so nothing sends yet. Replace the whole file with `scripts/apps-script/form_builder.gs`, edit `CLASS` (title, session, checkpoints that match the deck, remaining series sessions), save, run `buildWorksheet`. **BRANDON**: approve the permission prompt (Review permissions -> bwmason@umd.edu -> Allow) - never click it yourself.
   - The run publishes the form. Verify from PowerShell: `Invoke-WebRequest <viewform link>` returns 200 and contains "Your name" (no sign-in wall).
   - Put the live link into `build.py` (`engine.setup(<link>)`) and rebuild. Label stays "Link is in the Zoom chat".
4. **Email.** Delete `buildWorksheet`/`addItem_`/`CLASS` from the bound script (the form is built; a rerun over live responses would orphan them - the builder also refuses once responses exist). Paste `scripts/apps-script/followup_email.gs`, edit `EMAIL` (subject, heading, subline, `rows` = [label, exact form question title], `next`, file IDs), save, run `installTrigger`, then `sendTestEmail`. **BRANDON** approves the second permission prompt (mail, Drive, triggers).
5. **Handout ID.** **BRANDON** drags the session handout (xlsx/pdf) into Drive and pastes the link; put the ID in `EMAIL.templateFileId`. Before wiring any pasted ID, read its Drive title (`get_file_metadata`) and confirm it is the file the label names. Session 2 shipped the capture template labeled as the compliance matrix because the pasted link was the wrong file.
6. **Deck PDF.** Headless Edge, fresh profile, write to %TEMP% then copy (Edge will not write into the outputs folder, and a PDF open in a viewer silently does not get overwritten - use a new filename):
   ```powershell
   $edge="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"; $tmp="$env:TEMP\deck-$(Get-Random).pdf"
   $src="file:///" + ((Resolve-Path "<deck>.html").Path -replace '\\','/' -replace ' ','%20')
   Start-Process $edge -ArgumentList @('--headless','--disable-gpu','--no-pdf-header-footer','--virtual-time-budget=4000',"--user-data-dir=$env:TEMP\edgepdf-$(Get-Random)","--print-to-pdf=$tmp",$src) -Wait -WindowStyle Hidden
   Copy-Item $tmp ".\Session-N-<Title>-slides.pdf"
   ```
   Check page count = slide count and render 2 pages with PyMuPDF (`fitz`) to confirm every reveal step prints. **BRANDON** uploads it to Drive and pastes the link -> `EMAIL.deckFileId`. Once a real submission exists, run `sendLatestToMe` so Brandon sees the exact attendee email.
7. **Run sheet.** Adapt `assets/run-sheet-example.html` (dates, Zoom link from the calendar event, run of show with checkpoint rows shaded, chat message with the live link, handout path, next session) and publish it as a private artifact. Apply every rule in "Delivery rules" below; for Session 2 onward, also read the previous session's Zoom transcript + chat and its responses sheet, and add a "Last session's leftovers" block (unanswered chat questions, promised follow-ups) as a 4-minute row right after the welcome.
8. **Close out.** Commit the class `build.py` and `.gs` copies (explicit paths only), prepend the HANDOFF-LOG entry via `handoff_prepend.py`, push.

## Verification (do all of it; it is what "same criteria" means)
- Every slide screenshotted once at 1280x720 in the Browser pane: no overlap, no text past the frame. Drive slides with `javascript_tool` (`dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight'}))`); real key presses in the pane break on the `data:` URL.
- Reveal: step counts per slide look sane (roughly 3-11), back arrow lands on the fully built slide, dark/scan slides show everything at once (QR never hidden).
- Form opens publicly; question titles match `EMAIL.rows` exactly.
- Test email received, and each attachment's **filename** matches its `attachedLabel` (read the [TEST] thread with `get_thread`; a count of 2 is not enough).
- PDF complete.

## Apps Script editor mechanics (learned the hard way)
- Set code with `monaco.editor.getModels()[0].setValue(code)` via `javascript_tool` on the editor tab. Pass code through `String.raw` with a template literal; the code must contain no backticks or `${`.
- Save with the "Save project to Drive" button (find it by name). Ctrl+S often does not register. An account popup ("You're currently signed in as...") can swallow the click; press its OK first.
- The function dropdown ignores clicks on options. It defaults to the first function in the file, so put the function you need to run first - or temporarily append `yourFn(); // TEMP` inside the selected function, run, then remove it and save again.
- Reading another project's source (e.g. the VOSBTC `Code.gs`) through `javascript_tool` is blocked by the safety classifier. Do not try to route around it; these templates replace it.
- The Make a copy dialog ignores a typed name and Drive renames through the browser tools fail; the respondent-facing title comes from `CLASS.title`, so only Brandon's Drive list shows "Copy of ...". Tell him to rename it.
- Do not push binaries into Drive by base64 through tool calls (transcription errors); Brandon drags files in and pastes links.

## Delivery rules (from the Session 1 and 2 audits, 2026-09-28 / 09-30)
Session 1 ran 15 minutes over. Both checkpoints were skipped, the chat link landed 19 minutes in, and only 1 of 3 worksheets came back complete. Bake these into every deck and run sheet:
- **Link in chat at minute 0.** The run sheet's 20-minutes-before list ends with "At 10:00, paste the chat message yourself, before you say hello."
- **"Don't hit Submit until the last slide"** goes in the chat message, the slide 1 speaker note, and every checkpoint note. The follow-up email fires on submit, so an early submit mails the attendee a near-empty worksheet.
- **Checkpoints are the last thing cut.** The run sheet's "behind?" note names the content slides to drop, and says to pause the full 2-3 minutes at each checkpoint.
- **Hard stop 5 minutes before the end.** The run sheet carries "At :20 go straight to takeaways and Submit."
- **Leftovers row:** Session 2 onward opens with 4 minutes on the previous session's unanswered chat questions (see step 7).
- **Term check:** it is a *compliance* matrix, not a "capability matrix."
- **Fact-check the speaker notes** for thresholds and program rules before the build, and put the checked number in the note. Session 1 misstated on air: the EDWOSB net-worth cap ($850K; $6.5M is the assets cap), who certifies Maryland MBEs (since Oct 1, 2025: the Office of Minority Business Enterprise inside the Department of Social and Economic Mobility, DoSEM; not MDOT), the Maryland MBE goal (29%), and the OSDBU name.
- **One question per form field.** "Which hat are you skipping, and who could cover it" got answered as "Sub" and "Contractor" (Session 2). Split two-part prompts into two fields.
- **Checkpoints need a script, not a mention.** Session 2 named checkpoint B and kept talking. The run sheet says the literal line ("Take three minutes, I'll wait") and to watch the Responses tab until names move.
- **Call Submit at :20, then take questions.** Session 2 called it at :27 and Q&A vanished. Collect the forms while people ask.
- **Leftovers stay at 4 minutes;** personal stories go elsewhere. Say weekdays on air, never "tomorrow," in a Mon/Wed/Fri series.
- **After class:** run the audit. Inputs are the Zoom `.transcript.vtt` + chat `.txt` from Downloads, the responses (a copied form has no linked sheet; the sent follow-up emails in Gmail carry each attendee's answers), and the deck. Check what the follow-up emails actually attached. Output is `outputs/<class>/audit-session-N.md`: plan vs actual, form signals, open loops owed, facts to fix, and changes for the next session.
