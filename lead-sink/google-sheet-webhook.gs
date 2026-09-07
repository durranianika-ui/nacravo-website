/**
 * Nacravo lead sink — appends every website enquiry to a Google Sheet.
 *
 * This is the durable lead log. It is deliberately not a CRM: it is an
 * append-only record of what the website received, owned by Nacravo, readable
 * on a phone, and exportable anywhere. Nothing about the website depends on it
 * being up — /api/leads treats a failure here as "not stored" and still hands
 * the customer to WhatsApp.
 *
 * ── Deploy (about three minutes, once) ─────────────────────────────────────
 *  1. Create a Google Sheet. Name the first tab   Leads
 *  2. Extensions → Apps Script. Delete the placeholder, paste this file, Save.
 *  3. Edit SHARED_SECRET below to a long random string of your choosing.
 *  4. Deploy → New deployment → type "Web app"
 *       Execute as:        Me
 *       Who has access:    Anyone
 *     Deploy, authorise, and copy the /exec URL.
 *  5. In Vercel → nacravo-website → Settings → Environment Variables, add:
 *       LEAD_WEBHOOK_URL    = the /exec URL from step 4
 *       LEAD_WEBHOOK_TOKEN  = the same string as SHARED_SECRET
 *     Redeploy the site so the new variables are picked up.
 *
 * "Anyone" is required because Vercel calls this unauthenticated; the shared
 * secret is what actually guards it, which is why it must not be guessable.
 *
 * Verify with (note the secret goes in the BODY — a web app cannot read
 * request headers):
 *   curl -sL -X POST "<exec-url>" -H "Content-Type: application/json" \
 *     -d '{"token":"<secret>","lead_ref":"TEST-1","phone":"+971500000000","area":"Business Bay"}'
 * Expect {"ok":true,...,"message":"stored"} and one row. Delete the row after.
 * -L matters: Apps Script answers on a redirect.
 */

var SHARED_SECRET = 'CHANGE-ME-to-a-long-random-string';
var SHEET_NAME = 'Leads';

/* Column order is the contract. Append new fields at the END only — inserting
   in the middle would silently shift every historical row's meaning. */
var COLUMNS = [
  'received_at', 'lead_ref', 'lead_id', 'submission_id',
  'name', 'phone', 'email', 'area',
  'vertical', 'service', 'property_type', 'size', 'units', 'frequency',
  'preferred_date', 'customer_note', 'page_url',
  'gclid', 'gbraid', 'wbraid',
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
  'click_time', 'first_source', 'first_campaign', 'first_landing', 'first_seen',
  'experiment', 'marketing_consent', 'privacy_version', 'delivery_status'
];

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) return reply(400, 'no body');

    var lead = JSON.parse(e.postData.contents);

    /* A web app never sees request headers, so the secret arrives in the body
       (or the query string for manual testing). /api/leads sends both. */
    var auth = (lead && lead.token) || (e.parameter && e.parameter.token) || '';
    if (SHARED_SECRET && auth !== SHARED_SECRET) return reply(401, 'unauthorised');
    if (lead) delete lead.token;               // never write the secret to the sheet

    if (!lead || !lead.lead_ref) return reply(400, 'lead_ref required');

    /* Serialise appends. Two enquiries landing in the same second must not
       race for the same row. */
    var lock = LockService.getScriptLock();
    lock.waitLock(20000);
    try {
      var sheet = openSheet_();

      /* Idempotent on lead_ref: a retried delivery updates the existing row
         rather than logging the same enquiry twice. */
      var refCol = COLUMNS.indexOf('lead_ref') + 1;
      var last = sheet.getLastRow();
      var existing = 0;
      if (last > 1) {
        var refs = sheet.getRange(2, refCol, last - 1, 1).getValues();
        for (var i = 0; i < refs.length; i++) {
          if (String(refs[i][0]) === String(lead.lead_ref)) { existing = i + 2; break; }
        }
      }

      var row = COLUMNS.map(function (k) {
        var v = lead[k];
        if (v === null || v === undefined) return '';
        /* A leading + or = would be read as a formula. Keep phone numbers and
           anything else the customer typed as literal text. */
        v = String(v);
        return /^[=+\-@]/.test(v) ? "'" + v : v;
      });

      if (existing) sheet.getRange(existing, 1, 1, COLUMNS.length).setValues([row]);
      else sheet.appendRow(row);

      return reply(200, existing ? 'updated' : 'stored', lead.lead_ref);
    } finally {
      lock.releaseLock();
    }
  } catch (err) {
    return reply(500, String(err && err.message).slice(0, 200));
  }
}

function doGet() { return reply(200, 'nacravo lead sink ready'); }

function openSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(COLUMNS);
    sheet.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function reply(code, message, ref) {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: code === 200, code: code, message: message, lead_ref: ref || '' }))
    .setMimeType(ContentService.MimeType.JSON);
}
