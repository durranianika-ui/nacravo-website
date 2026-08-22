/* POST /api/leads — create a real Nacravo lead record, server-side.
 *
 * This endpoint is the system of record for a website enquiry. Before it
 * existed the "quote form" validated locally, pushed a conversion event and
 * then opened WhatsApp: if the visitor never sent the WhatsApp message,
 * Nacravo received nothing while the ad platforms had already recorded a
 * conversion. Now the lead is written to the CRM FIRST and the WhatsApp /
 * phone handover is an optional continuation.
 *
 * Contract
 *   201 { ok, lead_id, lead_ref, submission_id, summary }   new lead stored
 *   200 { ok, dup:true, lead_id, lead_ref, ... }            idempotent replay
 *   400 { error:"validation", fields:{ field: code } }      fixable by the user
 *   405 { error }                                           wrong method
 *   413 { error }                                           body too large
 *   429 { error, retry_after }                              rate limited
 *   503 { error:"lead store not configured" }               MONDAY_API_TOKEN unset
 *   502 { error:"lead store unavailable" }                  CRM write failed
 *
 * Privacy: name / phone / building never leave this function except to the
 * Monday CRM. The response carries no attribution identifiers, and the client
 * is expected to send only non-PII to analytics.
 *
 * Destination: Monday board "01 - Lead Register" (5101496395) — the board the
 * business already runs on. No parallel database is created.
 */

const BOARD_ID = "5101496395";
const GROUP_ID = "group_mm5w5m6"; // "New"

const COL = {
  contact:      "text_mm5wf3sp",     // Contact Person
  mobile:       "phone_mm5wvz9c",    // Mobile
  email:        "email_mm5wrabz",    // Email
  company:      "text_mm5wv9yx",     // Company
  area:         "text_mm5wzykz",     // Area / Location
  source:       "dropdown_mm5w5bc8", // Source
  channel:      "dropdown_mm5w1g5r", // Channel
  direction:    "color_mm5we74n",    // Lead Direction
  leadType:     "color_mm5w1pyp",    // Lead Type
  leadStatus:   "color_mm5ws61p",    // Lead Status
  stage:        "color_mm5x9yxn",    // Current Stage
  serviceReq:   "dropdown_mm5w394k", // Service Required
  notes:        "long_text_mm5x1f64",// Notes
  campaign:     "text_mm5wk3ch",     // Campaign
  ref:          "text_mm6f2dkq",     // Attribution Ref
  gclid:        "text_mm6fd15v",     // GCLID
  keyword:      "text_mm6fq31j",     // Keyword
  landingPage:  "text_mm6f4gdz",     // Landing Page
  clickTime:    "text_mm6fqrdn",     // Click Time
  webLeadId:    "text_mm6f4mgc",     // Web Lead ID   (system-managed)
  submissionId: "text_mm6fxhqb",     // Submission ID (system-managed, idempotency)
};

const REF_RE = /^NCR-[A-Z0-9]{2}-[A-Z0-9]{1,8}-[A-Z0-9]{2}$/;
const SUBMISSION_RE = /^[A-Za-z0-9_-]{8,64}$/;
const CONTROL_RE = /[\u0000-\u001F\u007F]/g;
const EPOCH = Date.UTC(2026, 0, 1);
const RAND_SET = "23456789ABCDEFGHJKMNPQRSTVWXYZ";

const VERTICALS = { cleaning: "cleaning", ac: "ac", general: "general" };

/* Allow-listed vocabularies. Anything outside them is dropped rather than
   echoed into the CRM, so a crafted request cannot inject free text through a
   field that is supposed to be a choice. */
const CLEANING_SERVICES = [
  "Apartment Cleaning", "Villa Cleaning", "Deep Cleaning", "Move In/Out Cleaning",
  "Office Cleaning", "Sofa & Upholstery Cleaning", "Holiday Home Cleaning",
  "Specialized Cleaning", "Home Cleaning", "Maid Service",
];
const AC_PROBLEMS = [
  "Not cooling", "Leaking", "Strange noise", "Bad smell", "Service",
  "Chemical clean", "Duct cleaning", "Installation", "Maintenance contract", "Not sure",
];
const SIZES = [
  "Studio", "1 bedroom", "2 bedrooms", "3 bedrooms", "4+ bedrooms",
  "1 Bedroom", "2 Bedrooms", "3 Bedrooms", "4 Bedrooms", "5+ Bedrooms", "N/A",
  "Under 1,000 sq ft", "1,000 - 3,000 sq ft", "3,000 - 7,000 sq ft",
  "7,000 - 15,000 sq ft", "Over 15,000 sq ft",
];
const FREQUENCIES = [
  "One-off", "Weekly", "Fortnightly", "Monthly", "Daily (6-7 days a week)",
  "5 days a week", "3 days a week",
];
/* The homepage and the non-corridor service pages (handyman, pest control,
   annual maintenance) submit under the "general" vertical. Their choices are
   allow-listed the same way, so no free text reaches the CRM through a field
   that is a menu on the page. */
const GENERAL_SERVICES = [
  "Handyman Services", "Pest Control", "Annual Maintenance Contract",
  "Home cleaning", "Deep cleaning", "Move-in / move-out",
  "Post-construction cleaning", "Sofa & carpet cleaning",
  "AC service / chemical wash", "Plumbing", "Electrical", "Handyman",
  "Painting", "Gold Club membership", "Landlord / AMC",
];

const PROPERTY_TYPES = [
  "Apartment", "Villa", "Townhouse", "Office", "Retail", "Warehouse", "Other",
];

/* ------------------------------------------------------------------ utils */

function str(v, max) {
  if (typeof v !== "string") return "";
  const s = v.replace(CONTROL_RE, " ").trim();
  return s.length > max ? s.slice(0, max) : s;
}

function pick(v, allowed, max) {
  const s = str(v, max || 60);
  if (!s) return "";
  return allowed.find((a) => a.toLowerCase() === s.toLowerCase()) || "";
}

/* UAE-aware E.164 normalisation that never rejects a valid international
   number: local formats expand to +971, anything already carrying a country
   code is kept as-is. */
function toE164(raw) {
  const s = String(raw || "").trim();
  if (!s) return "";
  const explicit = s.startsWith("+") || s.startsWith("00");
  let d = s.replace(/\D/g, "");
  if (s.startsWith("00")) d = d.replace(/^00/, "");
  if (!d) return "";
  if (!explicit) {
    if (/^0\d{8,9}$/.test(d)) d = "971" + d.slice(1);   // 055 540 3038
    else if (/^5\d{8}$/.test(d)) d = "971" + d;         // 55 540 3038
  }
  if (d.length < 8 || d.length > 15) return "";
  return "+" + d;
}

function mintRef() {
  const mins = Math.max(0, Math.floor((Date.now() - EPOCH) / 60000)).toString(36).toUpperCase();
  let rnd = "";
  for (let i = 0; i < 2; i++) rnd += RAND_SET.charAt(Math.floor(Math.random() * RAND_SET.length));
  return "NCR-S0-" + mins + "-" + rnd;
}

function mintLeadId() {
  try {
    return "L-" + require("crypto").randomUUID();
  } catch (e) {
    return "L-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 10);
  }
}

/* Best-effort in-memory rate limit. A serverless instance is not a shared
   store, so this throttles the common case (one abusive client hitting one
   warm instance) without pretending to be a distributed limiter. */
const HITS = new Map();
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 8;

function rateLimited(ip) {
  const now = Date.now();
  if (HITS.size > 5000) HITS.clear(); // bound memory on a long-lived instance
  const list = (HITS.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (list.length >= MAX_PER_WINDOW) {
    HITS.set(ip, list);
    return Math.ceil((WINDOW_MS - (now - list[0])) / 1000);
  }
  list.push(now);
  HITS.set(ip, list);
  return 0;
}

function clientIp(req) {
  const h = req.headers || {};
  const fwd = String(h["x-forwarded-for"] || "").split(",")[0].trim();
  return fwd || String(h["x-real-ip"] || "") || "unknown";
}

async function monday(token, query, variables) {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 9000);
  try {
    const r = await fetch("https://api.monday.com/v2", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: token, "API-Version": "2024-10" },
      body: JSON.stringify({ query, variables }),
      signal: ctl.signal,
    });
    const j = await r.json();
    if (j.errors) throw new Error(JSON.stringify(j.errors).slice(0, 400));
    return j.data;
  } finally {
    clearTimeout(timer);
  }
}


/* A native form POST (scripting disabled) arrives as urlencoded and expects a
   page back, not JSON. Everything else about the request is handled the same. */
function wantsHtml(req) {
  const h = req.headers || {};
  const ct = String(h["content-type"] || "");
  if (ct.indexOf("application/json") > -1) return false;
  return ct.indexOf("form-urlencoded") > -1 || ct.indexOf("multipart/form-data") > -1;
}

function escapeHtml(v) {
  return String(v || "").replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
}

function htmlPage(title, heading, bodyHtml, code) {
  return [
    "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">",
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
    "<meta name=\"robots\" content=\"noindex\">",
    "<title>" + escapeHtml(title) + " | Nacravo</title>",
    "<style>body{margin:0;padding:40px 20px;font:16px/1.6 system-ui,sans-serif;",
    "background:#F7F4EC;color:#2E372B}main{max-width:34rem;margin:0 auto}",
    "h1{font-size:1.5rem;margin:0 0 .6rem}code{background:#ECE6D8;border:1px dashed #8B9A7B;",
    "border-radius:8px;padding:.5rem .8rem;display:inline-block;font-size:1.05rem}",
    "a.btn{display:block;text-align:center;margin:.6rem 0;padding:.9rem;border-radius:10px;",
    "text-decoration:none;font-weight:600}.wa{background:#25D366;color:#fff}",
    ".call{background:#2E372B;color:#F7F4EC}.back{color:#5C6B4F}</style></head><body><main>",
    "<h1>" + escapeHtml(heading) + "</h1>", bodyHtml,
    '<p class="back"><a href="/">Back to Nacravo</a></p>',
    "</main></body></html>",
  ].join("");
}

const WA_HREF = "https://wa.me/971555403038";
const TEL_HREF = "tel:+971555403038";

/* ------------------------------------------------------------------ shape */

function readLead(b) {
  const vertical = VERTICALS[str(b.vertical, 16).toLowerCase()] || "";
  const isAc = vertical === "ac";

  const lead = {
    vertical,
    service: isAc ? "" : pick(b.service, vertical === "general"
      ? GENERAL_SERVICES.concat(CLEANING_SERVICES) : CLEANING_SERVICES),
    problem: isAc ? pick(b.problem, AC_PROBLEMS) : "",
    property_type: pick(b.property_type, PROPERTY_TYPES),
    size: pick(b.size, SIZES),
    units: /^\d{1,3}$/.test(str(b.units, 3)) ? str(b.units, 3) : "",
    frequency: pick(b.frequency, FREQUENCIES),
    area: str(b.area, 120),
    name: str(b.name, 80),
    company: str(b.company, 120),
    email: str(b.email, 120),
    phone: toE164(b.phone),
    preferred_date: /^\d{4}-\d{2}-\d{2}$/.test(str(b.preferred_date, 10)) ? str(b.preferred_date, 10) : "",
    notes: str(b.notes, 600),
    landing_page: str(b.landing_page, 160),
    page_url: str(b.page_url, 200),
    experiment: str(b.experiment, 40),
    consent_marketing: b.consent_marketing === true,
    privacy_version: str(b.privacy_version, 12) || "1.0",
  };

  lead.attribution = {
    ref: REF_RE.test(str(b.lead_ref, 24)) ? str(b.lead_ref, 24) : "",
    gclid: str(b.gclid, 200),
    gbraid: str(b.gbraid, 200),
    wbraid: str(b.wbraid, 200),
    utm_source: str(b.utm_source, 40),
    utm_medium: str(b.utm_medium, 40),
    utm_campaign: str(b.utm_campaign, 60),
    utm_term: str(b.utm_term, 120),
    utm_content: str(b.utm_content, 120),
    click_time: str(b.click_time, 40),
    first_source: str(b.first_utm_source, 40),
    first_campaign: str(b.first_utm_campaign, 60),
    first_landing: str(b.first_landing_page, 160),
    first_seen: str(b.first_seen, 40),
  };

  return lead;
}

function validate(lead) {
  const f = {};
  if (!lead.vertical) f.vertical = "required";
  if (!lead.phone) f.phone = "invalid";
  if (!lead.area || lead.area.length < 2) f.area = "required";
  if (lead.vertical !== "ac" && !lead.service) f.service = "required";
  if (lead.vertical === "ac" && !lead.problem) f.problem = "required";
  if (lead.email && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(lead.email)) f.email = "invalid";
  return f;
}

function paidSource(a) {
  if (a.gclid || a.gbraid || a.wbraid) return "Google Ads";
  const s = (a.utm_source || "").toLowerCase();
  if (s === "google") return "Google Ads";
  if (/^(meta|facebook|fb|instagram|ig)$/.test(s)) return "Meta Ads";
  return "Website";
}

function isCommercial(lead) {
  if (lead.company) return true;
  const p = (lead.property_type || "").toLowerCase();
  const s = (lead.service || "").toLowerCase();
  return /office|retail|commercial|warehouse/.test(p) || /office/.test(s) || /sq ft/.test(lead.size || "");
}

function buildNotes(lead, leadId) {
  const L = [];
  L.push(lead.vertical === "ac" ? "AC enquiry (website form)" : "Cleaning enquiry (website form)");
  if (lead.service) L.push("Service: " + lead.service);
  if (lead.problem) L.push("Problem: " + lead.problem);
  if (lead.property_type) L.push("Property type: " + lead.property_type);
  if (lead.size) L.push("Size: " + lead.size);
  if (lead.units) L.push("AC units: " + lead.units);
  if (lead.frequency) L.push("Frequency: " + lead.frequency);
  if (lead.preferred_date) L.push("Preferred date: " + lead.preferred_date);
  if (lead.notes) L.push("Customer note: " + lead.notes);
  L.push("");
  L.push("Web Lead ID: " + leadId);
  if (lead.page_url) L.push("Submitted from: " + lead.page_url);
  if (lead.experiment) L.push("Experiment: " + lead.experiment);
  const a = lead.attribution;
  if (a.utm_medium) L.push("UTM medium: " + a.utm_medium);
  if (a.utm_content) L.push("UTM content: " + a.utm_content);
  if (a.gbraid) L.push("GBRAID: " + a.gbraid);
  if (a.wbraid) L.push("WBRAID: " + a.wbraid);
  if (a.first_source || a.first_campaign) {
    L.push("First touch: " + (a.first_source || "?") + " / " + (a.first_campaign || "?") +
      (a.first_landing ? " / " + a.first_landing : "") + (a.first_seen ? " / " + a.first_seen : ""));
  }
  L.push("Marketing consent: " + (lead.consent_marketing ? "yes" : "not given") +
    " (service-request processing under privacy notice v" + lead.privacy_version + ")");
  return L.join("\n");
}

function columnValues(lead, leadId, submissionId) {
  const a = lead.attribution;
  const commercial = isCommercial(lead);
  const v = {};

  v[COL.contact] = lead.name || "Not given";
  v[COL.mobile] = { phone: lead.phone, countryShortName: lead.phone.startsWith("+971") ? "AE" : "" };
  if (lead.email) v[COL.email] = { email: lead.email, text: lead.email };
  if (lead.company) v[COL.company] = lead.company;
  v[COL.area] = lead.area;
  v[COL.direction] = { label: "Inbound" };
  v[COL.leadStatus] = { label: "New" };
  v[COL.stage] = { label: "New" };
  v[COL.leadType] = { label: commercial ? "B2B Retail" : "Residential" };
  v[COL.serviceReq] = { labels: [commercial ? "B2B Cleaning/Maintenance" : "Residential Cleaning/Maintenance"] };
  const src = paidSource(a);
  v[COL.source] = { labels: [src] };
  v[COL.channel] = { labels: [src] };
  v[COL.notes] = buildNotes(lead, leadId);
  v[COL.webLeadId] = leadId;
  v[COL.submissionId] = submissionId;
  if (a.ref) v[COL.ref] = a.ref;
  if (a.gclid || a.gbraid || a.wbraid) v[COL.gclid] = a.gclid || a.gbraid || a.wbraid;
  if (a.utm_campaign) v[COL.campaign] = a.utm_campaign;
  if (a.utm_term) v[COL.keyword] = a.utm_term;
  if (lead.landing_page) v[COL.landingPage] = lead.landing_page;
  if (a.click_time) v[COL.clickTime] = a.click_time;
  return v;
}

function itemName(lead, ref) {
  const what = lead.problem ? "AC " + lead.problem : (lead.service || "Enquiry");
  const who = lead.name || ref;
  return (who + " - " + what + (lead.area ? " - " + lead.area : "")).slice(0, 250);
}

/* ----------------------------------------------------------------- handler */

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "POST only" }); return; }

  // Same-origin only. The form is first-party; there is no cross-origin caller.
  const origin = String((req.headers || {}).origin || "");
  if (origin && !/^https?:\/\/([a-z0-9-]+\.)*(nacravo\.com|vercel\.app)$|^http:\/\/localhost(:\d+)?$|^http:\/\/127\.0\.0\.1(:\d+)?$/i.test(origin)) {
    res.status(403).json({ error: "forbidden origin" }); return;
  }

  const b = req.body && typeof req.body === "object" ? req.body : {};
  if (JSON.stringify(b).length > 8000) { res.status(413).json({ error: "payload too large" }); return; }

  // Honeypot: a hidden field only an automated filler completes. Answer 201
  // with a synthetic id so a bot cannot tell acceptance from rejection.
  if (str(b.website, 200)) {
    res.status(201).json({ ok: true, lead_id: mintLeadId(), lead_ref: mintRef(), summary: {} });
    return;
  }

  const lead = readLead(b);
  const fields = validate(lead);
  if (Object.keys(fields).length) {
    if (wantsHtml(req) && typeof res.send === "function") {
      const missing = Object.keys(fields).map((k) => "<li>" + escapeHtml(k.replace(/_/g, " ")) + "</li>").join("");
      res.setHeader("Content-Type", "text/html; charset=utf-8");
      res.status(400).send(htmlPage("Check your details", "We need a little more",
        "<p>Please go back and check:</p><ul>" + missing + "</ul>" +
        '<p>Or contact us directly:</p><a class="btn wa" href="' + WA_HREF + '">Message us on WhatsApp</a>' +
        '<a class="btn call" href="' + TEL_HREF + '">Call +971 55 540 3038</a>'));
      return;
    }
    res.status(400).json({ error: "validation", fields });
    return;
  }

  const submissionId = SUBMISSION_RE.test(str(b.submission_id, 64))
    ? str(b.submission_id, 64)
    : mintLeadId().slice(2);

  const wait = rateLimited(clientIp(req));
  if (wait) {
    res.setHeader("Retry-After", String(wait));
    res.status(429).json({ error: "too many requests", retry_after: wait });
    return;
  }

  const token = process.env.MONDAY_API_TOKEN;
  if (!token) {
    // Fail loudly rather than silently accepting a lead nothing will receive.
    console.error("[leads] MONDAY_API_TOKEN missing - lead rejected", { submissionId });
    res.status(503).json({ error: "lead store not configured" });
    return;
  }

  const leadRef = lead.attribution.ref || mintRef();
  const leadId = mintLeadId();

  try {
    // Idempotency: one item per submission id. A retry, a double-click or a
    // resubmitted page returns the original lead instead of creating a second.
    const found = await monday(token,
      `query ($board: ID!, $val: CompareValue!, $col: String!) {
         items_page_by_column_values (board_id: $board, limit: 1,
           columns: [{column_id: $col, column_values: [$val]}]) {
           items { id column_values (ids: ["${COL.webLeadId}", "${COL.ref}"]) { id text } } } }`,
      { board: BOARD_ID, val: submissionId, col: COL.submissionId });

    const hit = found && found.items_page_by_column_values && found.items_page_by_column_values.items[0];
    if (hit) {
      const cv = {};
      (hit.column_values || []).forEach((c) => { cv[c.id] = c.text; });
      res.status(200).json({
        ok: true, dup: true,
        lead_id: cv[COL.webLeadId] || leadId,
        lead_ref: cv[COL.ref] || leadRef,
        submission_id: submissionId,
      });
      return;
    }

    await monday(token,
      `mutation ($board: ID!, $group: String!, $name: String!, $vals: JSON!) {
         create_item (board_id: $board, group_id: $group, item_name: $name,
                      column_values: $vals, create_labels_if_missing: false) { id } }`,
      {
        board: BOARD_ID,
        group: GROUP_ID,
        name: itemName(lead, leadRef),
        vals: JSON.stringify(columnValues(lead, leadId, submissionId)),
      });

    if (wantsHtml(req) && typeof res.send === "function") {
      res.setHeader("Content-Type", "text/html; charset=utf-8");
      res.status(201).send(htmlPage(
        "Request received", "Thanks \u2014 your request is with Nacravo.",
        "<p>We have your details and will come back to you during opening hours " +
        "(open daily, 7\u00a0AM\u201310\u00a0PM). Quote this reference if you contact us:</p>" +
        "<p><code>" + escapeHtml(leadRef) + "</code></p>" +
        '<a class="btn wa" href="' + WA_HREF + "?text=" +
        encodeURIComponent("Hi Nacravo - following up on my request. Ref: " + leadRef) +
        '">Continue on WhatsApp</a>' +
        '<a class="btn call" href="' + TEL_HREF + '">Call +971 55 540 3038</a>' +
        "<p>Continuing on WhatsApp is optional \u2014 your request has already reached us.</p>"));
      return;
    }
    res.status(201).json({
      ok: true,
      lead_id: leadId,
      lead_ref: leadRef,
      submission_id: submissionId,
      summary: { vertical: lead.vertical, service: lead.service || lead.problem, area: lead.area },
    });
  } catch (e) {
    console.error("[leads] CRM write failed", String(e && e.message).slice(0, 300));
    res.status(502).json({ error: "lead store unavailable" });
  }
};
