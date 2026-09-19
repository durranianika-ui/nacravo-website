/* QA-routing tests for api/leads.js — run with: node build/test_leads_qa.js
 * A test enquiry must land in the QA group and never be reported to Meta;
 * a real enquiry must be completely unaffected. Network is stubbed.
 */
"use strict";
let pass = 0, fail = 0;
const ok = (c, m) => { if (c) { pass++; console.log("PASS " + m); } else { fail++; console.log("FAIL " + m); } };

let calls = [];
global.fetch = async (url, opts) => {
  const body = opts && opts.body ? JSON.parse(opts.body) : {};
  calls.push({ url: String(url), body });
  if (/items_page_by_column_values/.test(body.query || "")) return { ok: true, json: async () => ({ data: { items_page_by_column_values: { items: [] } } }) };
  return { ok: true, json: async () => ({ data: { create_item: { id: "1" } }, events_received: 1 }) };
};
process.env.MONDAY_API_TOKEN = "tkn";
process.env.META_CAPI_TOKEN = "meta";
const handler = require("../api/leads.js");
const res = () => ({ statusCode: 0, body: null, setHeader() { return this; }, status(c) { this.statusCode = c; return this; }, json(b) { this.body = b; return this; }, end() { return this; } });
let n = 0;
const base = { vertical: "general", service: "Pest Control", area: "Business Bay", phone: "0501234567", privacy_version: "1.0",
  lead_ref: "NCR-GP-82E2-AC", utm_source: "google", utm_medium: "cpc", utm_campaign: "24232450550", utm_term: "pest control dubai" };
async function submit(extra) {
  calls = [];
  const r = res();
  await handler({ method: "POST", headers: { "content-type": "application/json", "x-forwarded-for": "10.9.0." + (++n) }, body: Object.assign({ submission_id: "sub-qa-test-" + n }, base, extra) }, r);
  const create = calls.find((c) => /create_item/.test(c.body.query || ""));
  return { r, group: create && create.body.variables.group, meta: calls.some((c) => /graph\.facebook\.com/.test(c.url)) };
}
(async () => {
  let x = await submit({ name: "Real Customer", gclid: "Cj0KCQjwRealClickId" });
  ok(x.r.statusCode === 201 && x.group === "group_mm5w5m6", "real lead -> production 'New' group");
  ok(x.meta === true, "real lead is still reported to Meta");
  x = await submit({ name: "QA TEST - delete me", gclid: "Cj0KCQjwRealClickId" });
  ok(x.group === "group_mm6zbj6s", "name 'QA TEST…' -> QA group");
  ok(x.meta === false, "QA lead never reported to Meta");
  x = await submit({ name: "Someone", gclid: "QA-PROBE-1" });
  ok(x.group === "group_mm6zbj6s" && x.meta === false, "click id 'QA-…' -> QA group, no Meta");
  x = await submit({ name: "Qasim Ali", gclid: "Cj0KCQjwRealClickId" });
  ok(x.group === "group_mm5w5m6", "a real name that merely starts with 'Qa' is NOT treated as QA");
  console.log(`\n${pass} passed, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})();
