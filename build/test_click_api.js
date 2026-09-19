/* Contract tests for api/click.js and the click beacon in assets/nacravo-attr.js.
 * Run with: node build/test_click_api.js
 * Network is stubbed: nothing reaches Monday, a webhook or Google.
 */
"use strict";
const path = require("path");
const fs = require("fs");
const vm = require("vm");

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log("PASS " + msg); } else { fail++; console.log("FAIL " + msg); } }

let calls = [];
let existing = new Set(); let failNext = 0;
global.fetch = async (url, opts) => {
  const body = JSON.parse(opts.body); calls.push({ url, body });
  if (failNext > 0) { failNext--; throw new Error("transient"); }
  if (/items_page_by_column_values/.test(body.query || "")) return { ok: true, json: async () => ({ data: { items_page_by_column_values: { items: existing.has(body.variables.val) ? [{ id: "9" }] : [] } } }) };
  if (/create_item/.test(body.query || "")) { const v = JSON.parse(body.variables.v); existing.add(v.clk_key); }
  return { ok: true, json: async () => ({ data: { create_item: { id: "1" } } }) };
};
const creates = () => calls.filter((c) => /create_item/.test(c.body.query || ""));

function mockRes() {
  return { statusCode: 0, body: null, headers: {}, setHeader(k, v) { this.headers[k] = v; return this; },
    status(c) { this.statusCode = c; return this; }, json(b) { this.body = b; return this; }, end() { return this; } };
}
function load(env) {
  delete require.cache[require.resolve("../api/click.js")];
  for (const k of ["MONDAY_API_TOKEN", "CLICK_BOARD_ID", "CLICK_WEBHOOK_URL", "CLICK_WEBHOOK_TOKEN"]) delete process.env[k];
  Object.assign(process.env, env || {});
  return require("../api/click.js");
}
let ipN = 0;
async function post(handler, body, headers) {
  const res = mockRes();
  await handler({ method: "POST", body, headers: Object.assign({ "x-forwarded-for": "10.0.0." + (++ipN) }, headers || {}) }, res);
  return res;
}
const good = { ref: "NCR-GP-2QX1A-4K", action: "whatsapp", gclid: "Cj0KCQjw-test_ID.1", utm_source: "google",
  utm_medium: "cpc", utm_campaign: "24232450550", utm_term: "pest control dubai", utm_content: "824023401481",
  ag: "201529659313", mt: "p", net: "g", landing_page: "/pest-control", tap_page: "/pest-control",
  click_time: "2026-09-19T08:00:00.000Z", device: "mobile", ad_consent: "granted",
  name: "SHOULD NOT PASS", phone: "+971500000000", message: "hello" };

(async () => {
  // --- server -------------------------------------------------------------
  let h = load({});
  let r = await post(h, good);
  ok(r.statusCode === 204 && calls.length === 0, "no sink configured -> 204, nothing sent anywhere");

  h = load({ MONDAY_API_TOKEN: "tkn", CLICK_BOARD_ID: "123456" }); calls = [];
  r = await post(h, good);
  ok(r.statusCode === 204 && creates().length === 1 && /monday/.test(calls[0].url), "Monday sink -> dedupe lookup then one create_item");
  const cr = creates()[0];
  const v = JSON.parse(cr.body.variables.v);
  ok(cr.body.variables.n === "NCR-GP-2QX1A-4K" && cr.body.variables.b === "123456", "item named by ref on configured board");
  ok(v.clk_env === "prod" && v.clk_key === "NCR-GP-2QX1A-4K|whatsapp|Cj0KCQjw-test_ID.1", "production row carries env=prod and dedupe key");
  calls = []; r = await post(h, good);
  ok(r.statusCode === 204 && creates().length === 0, "same ref + action + click id is not written twice");
  calls = []; r = await post(h, Object.assign({}, good, { action: "call" }));
  ok(creates().length === 1, "a call tap from the same click is its own row");
  calls = []; failNext = 1; const e0 = console.error; console.error = () => {};
  r = await post(h, Object.assign({}, good, { ref: "NCR-GP-2QX1A-7M" })); console.error = e0;
  ok(r.statusCode === 204 && creates().length === 1, "transient failure is retried once and then stored");
  calls = []; r = await post(h, Object.assign({}, good, { ref: "NCR-GP-2QX1A-8N", gclid: "QA-TEST-CLICK" }));
  const qv = JSON.parse(creates()[0].body.variables.v);
  ok(qv.clk_env === "qa" && /^QA · /.test(creates()[0].body.variables.n), "QA click id -> env=qa and 'QA ·' item name");
  ok(v.clk_gclid === "Cj0KCQjw-test_ID.1" && v.clk_campaign === "24232450550" && v.clk_adgroup === "201529659313" && v.clk_keyword === "pest control dubai" && v.clk_match === "Phrase" && v.clk_landing === "/pest-control" && v.clk_device === "mobile" && v.clk_ad_consent === "granted" && v.clk_action === "whatsapp", "all attribution fields mapped");
  const blob = JSON.stringify(calls[0].body);
  ok(!/SHOULD NOT PASS|\+971500000000|hello/.test(blob), "name / phone / message never forwarded");

  calls = [];
  r = await post(h, Object.assign({}, good, { ref: "NCR-GP-2QX1A-9P", gclid: "", utm_medium: "", utm_source: "", fbclid: "" }));
  ok(r.statusCode === 204 && calls.length === 0, "unpaid visit is acknowledged but not stored");
  r = await post(h, Object.assign({}, good, { ref: "BAD" }));
  ok(r.statusCode === 400, "malformed ref rejected");
  r = await post(h, Object.assign({}, good, { action: "email" }));
  ok(r.statusCode === 400, "unknown action rejected");
  r = await post(h, Object.assign({}, good, { ref: "NCR-GP-2QX1A-QR", gclid: "<script>alert(1)</script>" }));
  ok(r.statusCode === 204 && !JSON.stringify(calls).includes("<script>"), "invalid click id dropped, not echoed");
  r = await post(h, good, { origin: "https://evil.example" });
  ok(r.statusCode === 403, "foreign origin refused");
  r = await post(h, JSON.stringify(good));
  ok(r.statusCode === 204, "string body (sendBeacon Blob) parsed");
  const res = mockRes(); await h({ method: "GET", headers: {} }, res);
  ok(res.statusCode === 405, "GET refused");
  let limited = 0; for (let i = 0; i < 35; i++) { const x = mockRes(); await h({ method: "POST", body: good, headers: { "x-forwarded-for": "9.9.9.9" } }, x); if (x.statusCode === 429) limited++; }
  ok(limited > 0, "rate limit engages on a burst from one IP");

  h = load({ CLICK_WEBHOOK_URL: "https://script.google.com/macros/s/x/exec", CLICK_WEBHOOK_TOKEN: "s3cret" }); calls = [];
  r = await post(h, good);
  ok(calls.length === 1 && calls[0].body.kind === "click" && calls[0].body.token === "s3cret" && calls[0].body.gclid === good.gclid, "webhook sink receives kind=click + token");

  global.fetch = async () => { throw new Error("down"); };
  h = load({ MONDAY_API_TOKEN: "tkn", CLICK_BOARD_ID: "123456" });
  const origErr = console.error; console.error = () => {};
  r = await post(h, good); console.error = origErr;
  ok(r.statusCode === 204, "store failure never surfaces to the visitor");

  // --- browser beacon (assets/nacravo-attr.js in a sandbox) ---------------
  const src = fs.readFileSync(path.join(__dirname, "..", "assets", "nacravo-attr.js"), "utf8");
  function browser(search, consent) {
    const ls = {}, ss = {}, beacons = [], listeners = [];
    if (consent !== undefined) ls.nacravo_consent = JSON.stringify(consent);
    const store = (o) => ({ getItem: (k) => (k in o ? o[k] : null), setItem: (k, v) => { o[k] = String(v); } });
    const document = { readyState: "complete", referrer: "", querySelectorAll: () => [],
      addEventListener: (t, fn) => { if (t === "click") listeners.push(fn); } };
    const win = { location: { search, pathname: "/pest-control", href: "https://www.nacravo.com/pest-control" + search, host: "www.nacravo.com" },
      localStorage: store(ls), sessionStorage: store(ss), document, innerWidth: 390,
      navigator: { userAgent: "Mozilla/5.0 (iPhone) Mobile", sendBeacon: (u, b) => { beacons.push({ u, b }); return true; } },
      URL, URLSearchParams, Blob: class { constructor(p) { this.text = p.join(""); } }, dataLayer: [] };
    win.window = win;
    vm.runInNewContext(src, win);
    const tap = (href) => listeners.forEach((fn) => fn({ target: { closest: () => ({ getAttribute: () => href }) } }));
    return { win, beacons, tap, ls };
  }
  const q = "?gclid=TESTGCLID&utm_source=google&utm_medium=cpc&utm_campaign=24043636201&utm_term=building%20maintenance%20dubai&ag=180000000001&mt=e&net=g";
  let b = browser(q);
  ok(/^NCR-GM-/.test(b.win.nacravoAttr.ref), "AMC click gets campaign code M (" + b.win.nacravoAttr.ref + ")");
  ok(/^NCR-GP-/.test(browser(q.replace("24043636201", "24232450550")).win.nacravoAttr.ref), "Pest click gets campaign code P");
  ok(/^NCR-GA-/.test(browser(q.replace("24043636201", "24262173810")).win.nacravoAttr.ref), "AC V2 click gets campaign code A");
  ok(/^NCR-GC-/.test(browser(q.replace("24043636201", "24026947888")).win.nacravoAttr.ref), "existing Cleaning code C unchanged");
  ok(/^NCR-GX-/.test(browser(q.replace("24043636201", "99999")).win.nacravoAttr.ref), "unknown campaign still X");
  b.tap("https://wa.me/971555403038?text=Hi");
  ok(b.beacons.length === 1 && b.beacons[0].u === "/api/click", "WhatsApp tap on a paid visit sends one beacon");
  const pl = JSON.parse(b.beacons[0].b.text);
  ok(pl.gclid === "TESTGCLID" && pl.ag === "180000000001" && pl.mt === "e" && pl.utm_campaign === "24043636201" && pl.action === "whatsapp" && pl.device === "mobile" && pl.ad_consent === "not_set", "beacon payload carries ids, ad group, match type, device, consent");
  b.tap("https://wa.me/971555403038?text=Hi");
  ok(b.beacons.length === 1, "second WhatsApp tap in same tab is de-duplicated");
  b.tap("tel:+971555403038");
  ok(b.beacons.length === 2 && JSON.parse(b.beacons[1].b.text).action === "call", "phone tap sends its own beacon");
  b.tap("/contact");
  ok(b.beacons.length === 2, "ordinary link sends nothing");
  let d = browser(""); d.tap("https://wa.me/971555403038");
  ok(d.beacons.length === 0, "direct / organic visit sends nothing");
  let rj = browser(q, { analytics: false, ad: false }); rj.tap("https://wa.me/971555403038");
  ok(rj.beacons.length === 0, "rejected ad consent sends nothing");
  let gr = browser(q, { analytics: true, ad: true }); gr.tap("https://wa.me/971555403038");
  ok(gr.beacons.length === 1 && JSON.parse(gr.beacons[0].b.text).ad_consent === "granted", "granted consent recorded as granted");
  ok(!/phone|name|message|text/.test(Object.keys(pl).join(",")), "beacon keys contain no personal fields");

  console.log(`\n${pass} passed, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})();
