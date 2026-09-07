/* Contract tests for api/leads.js — run with: node build/test_leads_api.js
 *
 * The Monday API is stubbed, so nothing is written to the real CRM and no test
 * lead reaches the operators. What is exercised is the behaviour the landing
 * pages depend on: validation, E.164 normalisation, allow-listing, idempotency,
 * the honeypot, rate limiting, and the rule that an unconfigured lead sink
 * hands the enquiry back as a WhatsApp message instead of destroying it.
 */
"use strict";

const path = require("path");
const MODULE = path.join(__dirname, "..", "api", "leads.js");

let calls = [];
let mondayHandler = null;

global.fetch = async (url, opts) => {
  const body = JSON.parse(opts.body);
  calls.push(body);
  const out = mondayHandler ? mondayHandler(body) : { data: {} };
  return { json: async () => out };
};

function mockRes() {
  const res = {
    statusCode: 0, body: null, headers: {},
    setHeader(k, v) { this.headers[k.toLowerCase()] = v; return this; },
    status(c) { this.statusCode = c; return this; },
    json(b) { this.body = b; return this; },
    end() { return this; },
  };
  return res;
}

function noItem() {
  return { data: { items_page_by_column_values: { items: [] } } };
}
function createdOk() {
  return { data: { create_item: { id: "999" } } };
}

/* Default stub: "not found" for the idempotency query, "created" for the
   mutation. Distinguished by which operation the query string carries. */
function defaultMonday(body) {
  return /items_page_by_column_values/.test(body.query) ? noItem() : createdOk();
}

async function post(payload, opts) {
  opts = opts || {};
  delete require.cache[require.resolve(MODULE)];
  if (opts.freshModule === false) { /* keep module state (rate limit map) */ }
  const handler = require(MODULE);
  const req = {
    method: opts.method || "POST",
    headers: Object.assign({ "x-forwarded-for": opts.ip || "203.0.113.9" }, opts.headers || {}),
    body: payload,
  };
  const res = mockRes();
  await handler(req, res);
  return res;
}

/* A handler kept across calls so the in-memory rate limiter accumulates. */
function stickyHandler() {
  delete require.cache[require.resolve(MODULE)];
  return require(MODULE);
}
async function postWith(handler, payload, ip) {
  const req = { method: "POST", headers: { "x-forwarded-for": ip || "203.0.113.9" }, body: payload };
  const res = mockRes();
  await handler(req, res);
  return res;
}

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; console.log("  PASS  " + name); }
  else { fail++; console.log("  FAIL  " + name + (extra ? "  -> " + JSON.stringify(extra) : "")); }
}

const AC_LEAD = {
  vertical: "ac", problem: "Not cooling", area: "Business Bay",
  phone: "0555403038", units: "3", property_type: "Apartment",
  submission_id: "abcdefgh12345678",
  gclid: "TEST_GCLID_1", utm_campaign: "24059561727", utm_term: "ac repair dubai",
  lead_ref: "NCR-GA-K7Q2Z-4X", landing_page: "/ac-repair-dubai",
};

const CLEAN_LEAD = {
  vertical: "cleaning", service: "Deep Cleaning", area: "Downtown Dubai",
  phone: "+971 55 540 3038", size: "2 bedrooms", property_type: "Apartment",
  name: "Test Person", submission_id: "cleanabcdefgh123",
};

(async function run() {
  console.log("api/leads.js contract tests\n");

  /* ---- no sink configured: hand over, never destroy, never claim -------
     An unconfigured CRM is a valid state, not an outage. The enquiry must
     survive it, the response must not pretend it was stored, and the visitor
     must get their own answers back as a message they only have to send. */
  delete process.env.MONDAY_API_TOKEN;
  delete process.env.LEAD_WEBHOOK_URL;
  mondayHandler = defaultMonday;
  let r = await post(AC_LEAD);
  let noSink = typeof r.body === "string" ? JSON.parse(r.body) : r.body;
  check("200, not 503, when no lead sink is configured (enquiry survives)",
    r.statusCode === 200, r.body);
  check("no sink -> stored:false (never claims a lead was saved)",
    noSink.stored === false && noSink.ok === true, r.body);
  check("no sink -> WhatsApp handover carrying the visitor's own answers",
    noSink.handover === "whatsapp" &&
    /^https:\/\/wa\.me\/971555403038\?text=/.test(noSink.wa_url || "") &&
    decodeURIComponent(noSink.wa_url).indexOf("Business Bay") !== -1 &&
    decodeURIComponent(noSink.wa_url).indexOf(noSink.lead_ref) !== -1, r.body);

  /* ---- webhook sink: architecture-neutral delivery, no CRM required ---- */
  const seen = [];
  const realFetch = globalThis.fetch;
  process.env.LEAD_WEBHOOK_URL = "https://example.invalid/hook";
  globalThis.fetch = async (url, opts) => {
    seen.push({ url: String(url), body: JSON.parse(opts.body) });
    return { ok: true, status: 200, json: async () => ({}), text: async () => "" };
  };
  r = await post(Object.assign({}, AC_LEAD, { submission_id: "hookabcdefgh1234" }));
  check("webhook sink stores the lead and returns 201 stored:true",
    r.statusCode === 201 && (typeof r.body === "string" ? JSON.parse(r.body) : r.body).stored === true, r.body);
  check("webhook receives the enquiry with phone, area and reference",
    seen.length === 1 && seen[0].url === "https://example.invalid/hook" &&
    seen[0].body.phone === "+971555403038" && seen[0].body.area === "Business Bay" &&
    !!seen[0].body.lead_ref, JSON.stringify(seen[0] && seen[0].body).slice(0, 200));

  /* The row has to carry everything needed to reconcile a lead against an ad
     click later, or the log is only half a record. */
  const rec = seen[0].body;
  const need = ["received_at", "lead_ref", "lead_id", "submission_id", "phone", "area",
    "vertical", "service", "page_url", "gclid", "gbraid", "wbraid", "utm_source",
    "utm_medium", "utm_campaign", "utm_term", "utm_content", "click_time",
    "marketing_consent", "delivery_status"];
  const missing = need.filter((k) => !(k in rec));
  check("the record carries every reconciliation field", missing.length === 0, missing);
  check("click ids and campaign survive onto the record",
    rec.gclid === "TEST_GCLID_1" && rec.utm_campaign === "24059561727" &&
    rec.utm_term === "ac repair dubai" && rec.page_url !== undefined &&
    /^\d{4}-\d{2}-\d{2}T/.test(rec.received_at), JSON.stringify({ g: rec.gclid, c: rec.utm_campaign }));

  /* A web app cannot read request headers, so the secret must also be in the
     body — otherwise a Sheet-backed sink rejects every lead. */
  globalThis.fetch = realFetch;
  const seen2 = [];
  process.env.LEAD_WEBHOOK_TOKEN = "s3cret";
  globalThis.fetch = async (url, opts) => {
    seen2.push({ headers: opts.headers, body: JSON.parse(opts.body) });
    return { ok: true, status: 200, json: async () => ({}), text: async () => "" };
  };
  r = await post(Object.assign({}, AC_LEAD, { submission_id: "tokenabcdefgh123" }));
  check("the shared secret travels in the body AND the bearer header",
    seen2[0].body.token === "s3cret" &&
    seen2[0].headers.Authorization === "Bearer s3cret", JSON.stringify(seen2[0] && seen2[0].headers));
  delete process.env.LEAD_WEBHOOK_TOKEN;

  /* A hanging sink must not hold the customer on a spinner. */
  globalThis.fetch = (url, opts) => new Promise((resolve, reject) => {
    opts.signal.addEventListener("abort", () => reject(new Error("aborted")));
  });
  const t0 = Date.now();
  r = await post(Object.assign({}, AC_LEAD, { submission_id: "slowabcdefgh1234" }));
  const slow = typeof r.body === "string" ? JSON.parse(r.body) : r.body;
  check("a hanging sink is abandoned and the customer still gets through",
    r.statusCode === 200 && slow.stored === false && slow.delivery === "failed" &&
    !!slow.wa_url && Date.now() - t0 < 8000, { ms: Date.now() - t0, body: r.body });

  globalThis.fetch = realFetch;
  delete process.env.LEAD_WEBHOOK_URL;

  process.env.MONDAY_API_TOKEN = "test-token";

  /* ---- method + payload guards ---------------------------------------- */
  r = await post(AC_LEAD, { method: "GET" });
  check("405 on GET", r.statusCode === 405);

  r = await post({ vertical: "ac", problem: "Not cooling", area: "x".repeat(9000), phone: "0555403038" });
  check("413 on oversized payload", r.statusCode === 413, r.body);

  r = await post(AC_LEAD, { headers: { origin: "https://evil.example.com" } });
  check("403 on a foreign origin", r.statusCode === 403, r.body);

  r = await post(AC_LEAD, { headers: { origin: "https://www.nacravo.com" } });
  check("201 on the production origin", r.statusCode === 201, r.body);

  /* ---- validation ------------------------------------------------------ */
  r = await post({ vertical: "ac", problem: "Not cooling", area: "Business Bay", phone: "12" });
  check("400 on a too-short phone", r.statusCode === 400 && r.body.fields.phone === "invalid", r.body);

  r = await post({ vertical: "ac", problem: "Not cooling", phone: "0555403038" });
  check("400 when the area is missing", r.statusCode === 400 && r.body.fields.area === "required", r.body);

  r = await post({ vertical: "ac", area: "Business Bay", phone: "0555403038" });
  check("400 when the AC problem is missing", r.statusCode === 400 && r.body.fields.problem === "required", r.body);

  r = await post({ vertical: "cleaning", area: "Marina", phone: "0555403038" });
  check("400 when the cleaning service is missing", r.statusCode === 400 && r.body.fields.service === "required", r.body);

  r = await post(Object.assign({}, CLEAN_LEAD, { email: "not-an-email" }));
  check("400 on a malformed email", r.statusCode === 400 && r.body.fields.email === "invalid", r.body);

  /* ---- E.164 normalisation --------------------------------------------- */
  const cases = [
    ["0555403038", "+971555403038"],
    ["555403038", "+971555403038"],
    ["+971 55 540 3038", "+971555403038"],
    ["00971555403038", "+971555403038"],
    ["+44 7700 900123", "+447700900123"],
  ];
  for (const [input, want] of cases) {
    calls = [];
    r = await post(Object.assign({}, AC_LEAD, { phone: input, submission_id: "sub" + Math.random().toString(36).slice(2, 12) }));
    const vals = JSON.parse(calls[calls.length - 1].variables.vals);
    const got = vals["phone_mm5wvz9c"].phone;
    check("phone " + input + " -> " + want, got === want, got);
  }

  /* ---- allow-listing --------------------------------------------------- */
  calls = [];
  r = await post(Object.assign({}, AC_LEAD, { problem: "<script>alert(1)</script>", submission_id: "injectabcdefg123" }));
  check("400 when the problem is off the allow-list (no injection reaches the CRM)",
    r.statusCode === 400, r.body);

  calls = [];
  r = await post(Object.assign({}, CLEAN_LEAD, { notes: "  line break  ", submission_id: "notesabcdefgh123" }));
  const notesVals = JSON.parse(calls[calls.length - 1].variables.vals);
  check("control characters are stripped from free text",
    !/ /.test(notesVals["long_text_mm5x1f64"]), notesVals["long_text_mm5x1f64"]);

  /* ---- attribution reaches the CRM, and only the CRM ------------------- */
  calls = [];
  r = await post(AC_LEAD);
  const v = JSON.parse(calls[calls.length - 1].variables.vals);
  check("GCLID stored on the lead", v["text_mm6fd15v"] === "TEST_GCLID_1", v["text_mm6fd15v"]);
  check("attribution ref stored on the lead", v["text_mm6f2dkq"] === "NCR-GA-K7Q2Z-4X", v["text_mm6f2dkq"]);
  check("campaign stored on the lead", v["text_mm5wk3ch"] === "24059561727", v["text_mm5wk3ch"]);
  check("keyword stored on the lead", v["text_mm6fq31j"] === "ac repair dubai", v["text_mm6fq31j"]);
  check("landing page stored on the lead", v["text_mm6f4gdz"] === "/ac-repair-dubai", v["text_mm6f4gdz"]);
  check("source classified as Google Ads", JSON.stringify(v["dropdown_mm5w5bc8"]).indexOf("Google Ads") > -1, v["dropdown_mm5w5bc8"]);
  check("lead lands in the New group with status New",
    JSON.stringify(v["color_mm5ws61p"]).indexOf("New") > -1, v["color_mm5ws61p"]);
  check("response carries no attribution identifiers",
    JSON.stringify(r.body).indexOf("TEST_GCLID_1") === -1, r.body);
  check("response carries a lead id and a ref", !!r.body.lead_id && !!r.body.lead_ref, r.body);

  /* ---- commercial classification --------------------------------------- */
  calls = [];
  await post(Object.assign({}, CLEAN_LEAD, {
    service: "Office Cleaning", company: "Acme FZ LLC", size: "3,000 - 7,000 sq ft",
    submission_id: "commercialabc123",
  }));
  const cv = JSON.parse(calls[calls.length - 1].variables.vals);
  check("an office enquiry is classified B2B",
    JSON.stringify(cv["color_mm5w1pyp"]).indexOf("B2B") > -1, cv["color_mm5w1pyp"]);

  /* ---- idempotency ------------------------------------------------------ */
  mondayHandler = (body) => {
    if (/items_page_by_column_values/.test(body.query)) {
      return { data: { items_page_by_column_values: { items: [
        { id: "111", column_values: [
          { id: "text_mm6f4mgc", text: "L-existing" },
          { id: "text_mm6f2dkq", text: "NCR-GA-K7Q2Z-4X" },
        ] } ] } } };
    }
    throw new Error("create_item must not be called on a duplicate");
  };
  r = await post(AC_LEAD);
  check("a replayed submission returns 200 dup, not a second lead",
    r.statusCode === 200 && r.body.dup === true && r.body.lead_id === "L-existing", r.body);
  mondayHandler = defaultMonday;

  /* ---- honeypot --------------------------------------------------------- */
  calls = [];
  r = await post(Object.assign({}, AC_LEAD, { website: "http://spam.example", submission_id: "honeypotabc12345" }));
  check("honeypot submissions are absorbed without a CRM write",
    r.statusCode === 201 && calls.length === 0, { status: r.statusCode, calls: calls.length });

  /* ---- sink failure: degrade, never block -------------------------------
     A secondary store going down is not the customer's problem. The journey
     must complete, the response must not claim a save that did not happen,
     and the enquiry must still have a way to reach Nacravo. */
  mondayHandler = () => { throw new Error("monday is down"); };
  r = await post(Object.assign({}, AC_LEAD, { submission_id: "failureabc123456" }));
  const down = typeof r.body === "string" ? JSON.parse(r.body) : r.body;
  check("a failing sink still lets the customer through (no 502 dead end)",
    r.statusCode === 200 && down.ok === true, r.body);
  check("a failing sink reports stored:false (no false success)",
    down.stored === false && down.delivery === "failed", r.body);
  check("a failing sink still hands over the enquiry on WhatsApp",
    down.handover === "whatsapp" &&
    decodeURIComponent(down.wa_url || "").indexOf("Business Bay") !== -1, r.body);
  mondayHandler = defaultMonday;

  /* ---- Meta Conversions API ------------------------------------------- *
   * The browser's Meta Lead event is dropped for a large share of visitors.
   * The server sends the same event with the same event_id so Meta can dedup,
   * and it must obey exactly the same rule as the browser: only a lead that
   * actually reached Nacravo is reported. */
  const realFetch2 = globalThis.fetch;

  // (a) No token configured -> the endpoint must not talk to Meta at all.
  delete process.env.META_CAPI_TOKEN;
  process.env.LEAD_WEBHOOK_URL = "https://example.invalid/hook";
  let metaCalls = [];
  globalThis.fetch = async (url, opts) => {
    if (String(url).indexOf("graph.facebook.com") !== -1) metaCalls.push({ url: String(url), body: JSON.parse(opts.body) });
    return { ok: true, status: 200, json: async () => ({}), text: async () => "" };
  };
  r = await post(Object.assign({}, AC_LEAD, { submission_id: "capioffabcdefg12" }));
  check("no META_CAPI_TOKEN -> nothing is sent to Meta",
    metaCalls.length === 0 && r.statusCode === 201, metaCalls.length);

  // (b) Token configured and the lead stored -> exactly one Lead event.
  process.env.META_CAPI_TOKEN = "capi-test-token";
  process.env.META_DATASET_ID = "4194940093973084";
  metaCalls = [];
  r = await post(Object.assign({}, AC_LEAD, { submission_id: "capionabcdefgh12" }));
  const stored = typeof r.body === "string" ? JSON.parse(r.body) : r.body;
  const ev = metaCalls[0] && metaCalls[0].body && metaCalls[0].body.data && metaCalls[0].body.data[0];
  check("a stored lead sends exactly one Meta Lead event",
    metaCalls.length === 1 && ev && ev.event_name === "Lead" && ev.action_source === "website",
    JSON.stringify(ev && { n: ev.event_name, a: ev.action_source }));
  check("the Meta event carries the dataset id and an access token",
    metaCalls[0].url.indexOf("/4194940093973084/events") !== -1 &&
    metaCalls[0].body.access_token === "capi-test-token", metaCalls[0].url);
  check("event_id matches the lead_id the browser also reports (dedup key)",
    ev.event_id === stored.lead_id && !!stored.lead_id, { e: ev.event_id, l: stored.lead_id });

  /* Meta must only ever receive hashed identifiers. A plaintext phone or
     email in this payload would be a real privacy defect, not a bug. */
  const raw = JSON.stringify(metaCalls[0].body);
  check("no plaintext phone or email is sent to Meta",
    raw.indexOf("555403038") === -1 && raw.indexOf("@") === -1, raw.slice(0, 200));
  check("phone is sent as a sha256 hash",
    Array.isArray(ev.user_data.ph) && /^[a-f0-9]{64}$/.test(ev.user_data.ph[0]), ev.user_data.ph);

  // (c) fbclid with no _fbc cookie must be rebuilt into Meta's fbc format.
  metaCalls = [];
  r = await post(Object.assign({}, AC_LEAD, {
    submission_id: "capifbclidabcd12", fbclid: "IwAR_test_click_id",
  }));
  const ev2 = metaCalls[0] && metaCalls[0].body.data[0];
  check("fbclid is rebuilt into an fbc value when the cookie is missing",
    !!ev2 && typeof ev2.user_data.fbc === "string" &&
    /^fb\.1\.\d+\.IwAR_test_click_id$/.test(ev2.user_data.fbc), ev2 && ev2.user_data.fbc);

  // (d) An unstored enquiry is NOT reported. The browser counts it on the tap.
  delete process.env.LEAD_WEBHOOK_URL;
  delete process.env.MONDAY_API_TOKEN;
  metaCalls = [];
  r = await post(Object.assign({}, AC_LEAD, { submission_id: "capinosinkabcd12" }));
  const un = typeof r.body === "string" ? JSON.parse(r.body) : r.body;
  check("an unstored enquiry is never reported to Meta (no phantom lead)",
    un.stored === false && metaCalls.length === 0, metaCalls.length);

  delete process.env.META_CAPI_TOKEN;
  delete process.env.META_DATASET_ID;
  globalThis.fetch = realFetch2;
  process.env.MONDAY_API_TOKEN = "test-token";
  mondayHandler = defaultMonday;

  /* ---- rate limiting ---------------------------------------------------- */
  const h = stickyHandler();
  let last = null;
  for (let i = 0; i < 10; i++) {
    last = await postWith(h, Object.assign({}, AC_LEAD, { submission_id: "rate" + i + "abcdefgh" }), "198.51.100.7");
  }
  check("the 9th+ request from one address is rate limited",
    last.statusCode === 429 && last.headers["retry-after"], { s: last.statusCode, h: last.headers });

  /* ---- general vertical (homepage) -------------------------------------- */
  r = await post({
    vertical: "general", service: "AC service / chemical wash", area: "DIFC",
    phone: "0555403038", property_type: "Apartment", size: "2 Bedrooms",
    email: "test@example.com", name: "Homepage Tester", submission_id: "generalabcdefg12",
  });
  check("the homepage form creates a lead under the general vertical", r.statusCode === 201, r.body);

  console.log("\n" + pass + " passed, " + fail + " failed");
  process.exit(fail ? 1 : 0);
})();
