// SBDC Workshops: class worksheet form builder.
// Paste into the form's bound script (Form editor > More > Apps Script), edit CLASS below, run buildWorksheet once.
// It deletes every question and recreates them; the header image and theme stay.
// Guard: it refuses to run once the form has responses, so live answers are never orphaned.

var CLASS = {
  title: 'Team Roles and Responsibilities — Class Worksheet',
  series: 'Winning That Government Contracting Award',
  session: 'Session 2',
  // One entry per worksheet checkpoint slide, in deck order. Names must match the deck ("Section A", "Section B").
  checkpoints: [
    { title: 'Section A: your team today', help: 'Stop here until we get to proposal roles.',
      items: [
        { type: 'checkbox', title: 'Which roles do you cover yourself right now?', choices: ['Capture manager', 'Proposal manager', 'Solution architect / SME', 'Pricing', 'Business development', 'Writer / editor'] },
        { type: 'text', title: 'Who could fill one gap for you?', help: 'A partner, a contractor, a mentor.' }
      ] },
    { title: 'Section B: your review plan', help: 'Fill this in at the color team checkpoint.',
      items: [
        { type: 'mc', title: 'Who will read your next proposal before you submit?', choices: ['Nobody yet', 'Someone on my team', 'An outside reviewer', 'A teaming partner'] }
      ] }
  ],
  series_sessions: ['Session 3: How to read an RFP (Fri, Oct 2)', 'Session 4: Basics of proposal writing (Mon, Oct 5)'],
  confirmation: 'Thanks — you\'re in. Watch your inbox for the slides, the template, and today\'s links. Questions: bwmason@umd.edu'
};

function buildWorksheet() {
  var f = FormApp.getActiveForm();
  if (f.getResponses().length) throw new Error('This form already has responses. Copy the form and build on the copy instead.');
  f.getItems().forEach(function (i) { f.deleteItem(i); });

  f.setTitle(CLASS.title);
  f.setDescription(CLASS.series + ' · ' + CLASS.session + ' · Maryland SBDC\n\n' +
    'How this works: fill in the first page now, before we begin. Keep this tab open — we come back to it during the class. ' +
    'Hit Submit at the end and we email you the slides, the template, and every link from today.');
  f.setConfirmationMessage(CLASS.confirmation);

  // ---- Page 1: the same every class ----
  f.addSectionHeaderItem().setTitle('Before we start').setHelpText('Two minutes. Answer these now, then wait for us.');
  f.addTextItem().setTitle('Your name').setRequired(true);
  f.addTextItem().setTitle('Your email').setHelpText('This is where we send the slides, the template and the links.')
    .setValidation(FormApp.createTextValidation().requireTextIsEmail().build()).setRequired(true);
  f.addTextItem().setTitle('Business name');
  f.addMultipleChoiceItem().setTitle('Where is your business today?').setRequired(true)
    .setChoiceValues(['Idea stage', 'Just started (under 2 years)', 'Established (2+ years)', 'Already doing government work']);
  f.addListItem().setTitle('County').setRequired(true).setChoiceValues(['Allegany', 'Anne Arundel', 'Baltimore City', 'Baltimore County',
    'Calvert', 'Caroline', 'Carroll', 'Cecil', 'Charles', 'Dorchester', 'Frederick', 'Garrett', 'Harford', 'Howard', 'Kent', 'Montgomery',
    "Prince George's", "Queen Anne's", "St. Mary's", 'Somerset', 'Talbot', 'Washington', 'Wicomico', 'Worcester', 'Outside Maryland']);
  f.addMultipleChoiceItem().setTitle('Have you gone after a government contract before?').setRequired(true)
    .setChoiceValues(['No, this is my first look', "I've searched SAM.gov or eMMA but haven't bid", "I've bid but haven't won yet", "I've won government work"]);
  f.addTextItem().setTitle('Primary NAICS code').setHelpText("If you know it. Leave blank if you don't.");
  f.addCheckboxItem().setTitle('Certifications you hold or are pursuing')
    .setChoiceValues(['8(a)', 'Maryland MBE', 'DBE', 'WOSB / EDWOSB', 'SDVOSB / VOSB', 'HUBZone', 'None yet']).showOtherOption(true);

  // ---- Class-specific checkpoints ----
  CLASS.checkpoints.forEach(function (s) {
    f.addPageBreakItem().setTitle(s.title).setHelpText(s.help || '');
    s.items.forEach(function (q) { addItem_(f, q); });
  });

  // ---- Closing pages: the same every class ----
  var last = String.fromCharCode(65 + CLASS.checkpoints.length);
  f.addPageBreakItem().setTitle('Section ' + last + ': before you leave').setHelpText('Two minutes. The people who write it down do it.');
  f.addParagraphTextItem().setTitle('The one step I will take this month').setRequired(true);
  f.addCheckboxItem().setTitle('What do you want from us?')
    .setChoiceValues(['The template from today', 'Links from today', 'Help with a certification', 'Help with my capability statement']);
  f.addParagraphTextItem().setTitle("What's still unclear?");

  f.addPageBreakItem().setTitle('Staying in touch').setHelpText('Last page. Then hit Submit.');
  f.addMultipleChoiceItem().setTitle('Would you like free one-on-one advising from a Maryland SBDC consultant?').setRequired(true)
    .setHelpText('Free and confidential. No sales pitch.')
    .setChoiceValues(['Yes, send me the sign-up link', "I'm already an SBDC client", 'Not right now']);
  if (CLASS.series_sessions.length) f.addCheckboxItem().setTitle('Joining the rest of the series?').setChoiceValues(CLASS.series_sessions);
  f.addMultipleChoiceItem().setTitle('May we contact you about Maryland SBDC programs?').setRequired(true).setChoiceValues(['Yes', 'No']);

  Logger.log('Built %s items. Live link: %s', f.getItems().length, f.getPublishedUrl());
}

function addItem_(f, q) {
  var it;
  if (q.type === 'mc') it = f.addMultipleChoiceItem().setChoiceValues(q.choices);
  else if (q.type === 'checkbox') it = f.addCheckboxItem().setChoiceValues(q.choices);
  else if (q.type === 'para') it = f.addParagraphTextItem();
  else if (q.type === 'grid') it = f.addGridItem().setRows(q.rows).setColumns(q.cols || ['1', '2', '3', '4', '5']);
  else it = f.addTextItem();
  it.setTitle(q.title);
  if (q.help) it.setHelpText(q.help);
  if (q.required) it.setRequired(true);
}
