// SBDC Workshops: follow-up email, sent automatically when someone submits the class worksheet.
// Paste into the SAME bound script as the form (after buildWorksheet is done, delete buildWorksheet from the file
// so nobody reruns it over live responses). Edit EMAIL below, save, then:
//   1. run installTrigger once (turns on sending; Brandon approves the permission prompt)
//   2. run sendTestEmail (sample answers, to you only)
//   3. after one real submission, run sendLatestToMe (real answers, to you only)
// If Gmail hiccups mid-class: run resendFailed.

var EMAIL = {
  subject: 'Your Session 2 worksheet, the links, and what comes next',
  heading: 'Team Roles and Responsibilities',
  subline: 'Winning That Government Contracting Award &middot; Session 2 &middot; Sept 30, 2026',
  // [label shown in the email, exact form question title]; blank answers are skipped
  rows: [
    ['Roles you cover today', 'Which roles do you cover yourself right now?'],
    ['Who could fill a gap', 'Who could fill one gap for you?'],
    ['Your review plan', 'Who will read your next proposal before you submit?'],
    ['Your one step this month', 'The one step I will take this month']
  ],
  // Optional: if the form has a 1-5 grid, flag when 2+ rows score below 3. Blank = no flag.
  gridFlag: '',   // e.g. "You scored {n} of the Four C's below 3. That is the red-flag zone we talked about."
  next: '<b>Session 3: How to Read an RFP</b>, Friday, Oct 2, 10:00 a.m., same Zoom series.',
  templateFileId: '',  // Drive ID of the handout (xlsx/pdf). Blank = not attached.
  deckFileId: '',      // Drive ID of the deck PDF. Blank = not attached.
  attachedLabel: ['the template from today', "today's slides"]
};
var REPLY_TO = 'bwmason@umd.edu';
var SIGNUP_URL = 'https://mdsbdc.ecenterdirect.com/signup';
var LINKS = [
  ['SAM.gov', 'https://sam.gov', 'Federal opportunities and your entity registration'],
  ['eMaryland Marketplace Advantage (eMMA)', 'https://emma.maryland.gov', 'Maryland state procurements, $30k+'],
  ['Acquisition Gateway forecasts', 'https://acquisitiongateway.gov/forecast', 'What federal agencies plan to buy next'],
  ['SBA Dynamic Small Business Search', 'https://search.certifications.sba.gov', 'How primes find small subs (keep your profile current)'],
  ['SBA certifications', 'https://certify.sba.gov', '8(a), WOSB/EDWOSB, HUBZone, VOSB/SDVOSB']
];

function installTrigger() {
  var form = FormApp.getActiveForm();
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'onFormSubmit') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('onFormSubmit').forForm(form).onFormSubmit().create();
  Logger.log('Trigger installed. Every new submission now gets the follow-up email.');
}

function onFormSubmit(e) { sendFor_(e.response); }

function sendFor_(response) {
  var a = answers_(response);
  var to = a['Your email'];
  if (!to) { Logger.log('No email on response ' + response.getId()); return; }
  try {
    send_(to, EMAIL.subject, a);
    markFailed_(response.getId(), false);
    Logger.log('SENT ' + to);
  } catch (err) {
    markFailed_(response.getId(), true);
    Logger.log('FAILED ' + to + ': ' + err);
  }
}

function send_(to, subject, a) {
  var opts = { name: 'Brandon Mason, Maryland SBDC', replyTo: REPLY_TO, htmlBody: html_(a) };
  var files = attachments_();
  if (files.length) opts.attachments = files;
  MailApp.sendEmail(to, subject, text_(a), opts);
  return files.length;
}

function answers_(response) {
  var out = {};
  response.getItemResponses().forEach(function (ir) {
    var v = ir.getResponse();
    if (ir.getItem().getType() === FormApp.ItemType.GRID) {
      out['__grid'] = ir.getItem().asGridItem().getRows().map(function (r, i) { return [r, v[i] || '']; });
    } else {
      out[ir.getItem().getTitle()] = Array.isArray(v) ? v.join(', ') : v;
    }
  });
  return out;
}

function attachments_() {
  return [EMAIL.templateFileId, EMAIL.deckFileId].filter(String).map(function (id) { return DriveApp.getFileById(id).getBlob(); });
}

function markFailed_(id, failed) {
  var p = PropertiesService.getScriptProperties();
  var list = JSON.parse(p.getProperty('failed') || '[]').filter(function (x) { return x !== id; });
  if (failed) list.push(id);
  p.setProperty('failed', JSON.stringify(list));
}

function resendFailed() {
  var form = FormApp.getActiveForm();
  var ids = JSON.parse(PropertiesService.getScriptProperties().getProperty('failed') || '[]');
  ids.forEach(function (id) { sendFor_(form.getResponse(id)); });
  Logger.log('Retried ' + ids.length);
}

// Preview: the real email for the newest form response, sent only to you.
function sendLatestToMe() {
  var rs = FormApp.getActiveForm().getResponses();
  if (!rs.length) { Logger.log('No responses yet.'); return; }
  var me = Session.getActiveUser().getEmail();
  var n = send_(me, '[PREVIEW] ' + EMAIL.subject, answers_(rs[rs.length - 1]));
  Logger.log('Preview of the newest of ' + rs.length + ' response(s) sent to ' + me + ' with ' + n + ' attachment(s).');
}

// Test: sample answers built from EMAIL.rows, sent only to you.
function sendTestEmail() {
  var me = Session.getActiveUser().getEmail();
  var a = { 'Your name': 'Test Person', 'Your email': me,
            'Would you like free one-on-one advising from a Maryland SBDC consultant?': 'Yes, send me the sign-up link' };
  EMAIL.rows.forEach(function (r) { a[r[1]] = '(sample answer)'; });
  var n = send_(me, '[TEST] ' + EMAIL.subject, a);
  Logger.log('Test sent to ' + me + ' with ' + n + ' attachment(s).');
}

// ----------------------------- content -----------------------------

function first_(a) { return String(a['Your name'] || '').trim().split(/\s+/)[0] || 'there'; }
function esc_(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

function html_(a) {
  var blue = '#002d62', red = '#d11142', ink = '#313438', mute = '#6a6d71', line = '#e2e4e7';
  var row = function (k, v) {
    return v ? '<tr><td style="padding:10px 0;border-top:1px solid ' + line + ';color:' + mute + ';font-size:13px;width:38%;vertical-align:top">' + esc_(k) +
      '</td><td style="padding:10px 0;border-top:1px solid ' + line + ';color:' + ink + ';font-size:15px">' + esc_(v) + '</td></tr>' : '';
  };
  var rows = EMAIL.rows.map(function (r) { return row(r[0], a[r[1]]); }).join('') +
    (a['__grid'] || []).map(function (r) { return row(r[0], r[1] ? r[1] + ' / 5' : ''); }).join('');
  var weak = (a['__grid'] || []).filter(function (r) { return r[1] && Number(r[1]) < 3; }).length;
  var flag = EMAIL.gridFlag && weak >= 2 ? '<p style="margin:14px 0 0;padding:12px 14px;background:#fceef2;border-left:4px solid ' + red + ';font-size:14px;color:' + ink + '">' +
    esc_(EMAIL.gridFlag.replace('{n}', weak)) + '</p>' : '';
  var links = LINKS.map(function (l) {
    return '<li style="margin:0 0 10px"><a href="' + l[1] + '" style="color:' + red + ';font-weight:bold">' + esc_(l[0]) + '</a><br><span style="color:' + mute + ';font-size:13px">' + esc_(l[2]) + '</span></li>';
  }).join('');
  var advising = /^Yes/.test(a['Would you like free one-on-one advising from a Maryland SBDC consultant?'] || '')
    ? '<p style="margin:0 0 8px;font-size:15px;color:' + ink + '">You asked for free one-on-one advising. Register here and we will match you with a consultant:</p>' +
      '<p style="margin:0 0 4px"><a href="' + SIGNUP_URL + '" style="display:inline-block;background:' + red + ';color:#fff;text-decoration:none;font-weight:bold;padding:12px 20px">Register for advising</a></p>'
    : '<p style="margin:0;font-size:15px;color:' + ink + '">Free, confidential one-on-one advising is always open: <a href="' + SIGNUP_URL + '" style="color:' + red + '">' + SIGNUP_URL.replace('https://', '') + '</a></p>';
  var attached = [EMAIL.templateFileId ? EMAIL.attachedLabel[0] : '', EMAIL.deckFileId ? EMAIL.attachedLabel[1] : ''].filter(String);
  var attachLine = attached.length ? '<p style="margin:0 0 18px;font-size:15px;color:' + ink + '">Attached: ' + attached.join(' and ') + '. Drop them into NotebookLM or ChatGPT and ask it questions.</p>' : '';

  return '<div style="background:#f4f6f8;padding:24px 12px;font-family:Arial,Helvetica,sans-serif">' +
    '<div style="max-width:600px;margin:0 auto;background:#fff">' +
    '<div style="background:' + blue + ';padding:22px 28px"><span style="display:inline-block;background:' + red + ';color:#fff;font-weight:bold;font-size:12px;letter-spacing:2px;padding:5px 10px">MARYLAND SBDC</span>' +
    '<div style="color:#fff;font-size:24px;font-weight:bold;margin-top:14px">' + EMAIL.heading + '</div>' +
    '<div style="color:#b8c8dd;font-size:13px;margin-top:4px">' + EMAIL.subline + '</div></div>' +
    '<div style="padding:26px 28px">' +
    '<p style="margin:0 0 14px;font-size:16px;color:' + ink + '">Thanks for joining today, ' + esc_(first_(a)) + '. Here is what you wrote, so you can act on it this week.</p>' +
    attachLine +
    '<div style="font-size:12px;font-weight:bold;letter-spacing:1.5px;color:' + red + ';margin:22px 0 4px">YOUR WORKSHEET</div>' +
    '<table style="width:100%;border-collapse:collapse">' + rows + '</table>' + flag +
    '<div style="font-size:12px;font-weight:bold;letter-spacing:1.5px;color:' + red + ';margin:26px 0 10px">WHERE TO LOOK</div>' +
    '<ul style="margin:0;padding-left:18px;font-size:15px">' + links +
    '<li style="margin:0"><b>Your county and city</b><br><span style="color:' + mute + ';font-size:13px">Search "[your county] procurement bid opportunities". Local buys start around $15k.</span></li></ul>' +
    '<div style="font-size:12px;font-weight:bold;letter-spacing:1.5px;color:' + red + ';margin:26px 0 10px">NEXT</div>' +
    '<p style="margin:0 0 14px;font-size:15px;color:' + ink + '">' + EMAIL.next + '</p>' + advising +
    '<p style="margin:22px 0 0;font-size:15px;color:' + ink + '">Questions? Just reply to this email.<br>Brandon Mason, Maryland SBDC</p>' +
    '</div>' +
    '<div style="padding:16px 28px;border-top:1px solid ' + line + ';color:' + mute + ';font-size:11px;line-height:1.5">Funded in part through a Cooperative Agreement with the U.S. Small Business Administration. All opinions, conclusions, and/or recommendations expressed herein are those of the author(s) and do not necessarily reflect the views of the SBA.</div>' +
    '</div></div>';
}

function text_(a) {
  var lines = ['Thanks for joining today, ' + first_(a) + '.', '', 'YOUR WORKSHEET'];
  EMAIL.rows.forEach(function (r) { if (a[r[1]]) lines.push(r[0] + ': ' + a[r[1]]); });
  (a['__grid'] || []).forEach(function (r) { lines.push(r[0] + ' ' + (r[1] || '-') + '/5'); });
  lines.push('', 'WHERE TO LOOK');
  LINKS.forEach(function (l) { lines.push(l[0] + ': ' + l[1]); });
  lines.push('', 'NEXT: ' + EMAIL.next.replace(/<[^>]+>/g, ''), 'Free one-on-one advising: ' + SIGNUP_URL, '', 'Brandon Mason, Maryland SBDC');
  return lines.join('\n');
}
