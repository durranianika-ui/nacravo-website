/* Nacravo click attribution — vanilla JS, no dependencies, no third-party calls.
 *
 * Captures paid-click and campaign attribution on landing and keeps it in
 * localStorage so a later lead (form -> WhatsApp handover, WhatsApp tap or
 * phone call) can be traced back to the click that produced it:
 *
 *   gclid / gbraid / wbraid, utm_* params, landing page, first-seen timestamp
 *
 * plus a short human-readable reference token (e.g. "NCR-GA-K7Q2Z-4X") that is
 * appended to every WhatsApp prefill. The token encodes source + campaign +
 * click time, so a WhatsApp conversation can be attributed even before any
 * lookup: char1 source (G google ads/paid, M meta, X other tagged, R referral,
 * D direct), char2 campaign (C cleaning, A ac, O office, U upholstery,
 * X unknown-tagged, 0 untagged), then base-36 minutes since 2026-01-01 UTC,
 * then 2 random chars.
 *
 * Rules:
 *  - first-touch record is written once and never overwritten while valid;
 *  - last-touch record updates ONLY when a new visit actually carries
 *    attribution (a plain internal navigation never clobbers a stored gclid);
 *  - the reference token is stable for the lifetime of the record;
 *  - nothing here sends data anywhere: it only stores locally, decorates
 *    wa.me links, and exposes window.nacravoAttr for the tracking layer.
 */
(function () {
  "use strict";

  var KEY = "nacravo_attr";
  var TTL_MS = 90 * 24 * 60 * 60 * 1000; // 90 days, matching Google's click window
  var EPOCH = Date.UTC(2026, 0, 1);
  // Google Ads campaign ids -> single-letter campaign codes for the token.
  // utm_campaign carries {campaignid} via the account-level final URL suffix.
  var CAMPAIGNS = {
    "24026947888": "C", // NCR-Search-Cleaning-3Areas
    "24059561727": "A", // NCR | Search | AC Services | Dubai
    "24086406701": "O", // NCR | Search | Office & Commercial | Dubai
    "24057101882": "U"  // NCR – Search – Upholstery Cleaning – Dubai
  };
  var RAND_SET = "23456789ABCDEFGHJKMNPQRSTVWXYZ"; // no 0/O/1/I lookalikes

  function now() { return Date.now(); }

  function readStore() {
    try {
      var a = JSON.parse(localStorage.getItem(KEY));
      if (a && a.ref && a.first && (now() - (a.first.at || 0)) < TTL_MS) return a;
    } catch (e) {}
    return null;
  }
  function writeStore(a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} }

  function parseTouch() {
    var t = { at: now(), lp: location.pathname };
    try {
      var q = new URLSearchParams(location.search);
      ["gclid", "gbraid", "wbraid", "utm_source", "utm_medium", "utm_campaign",
       "utm_term", "utm_content"].forEach(function (k) {
        var v = q.get(k); if (v) t[k] = v.slice(0, 200);
      });
    } catch (e) {}
    t.tagged = !!(t.gclid || t.gbraid || t.wbraid || t.utm_source);
    return t;
  }

  function srcChar(t) {
    if (t.gclid || t.gbraid || t.wbraid) return "G";
    var s = (t.utm_source || "").toLowerCase();
    if (s === "google") return "G";
    if (/^(meta|facebook|fb|instagram|ig)$/.test(s)) return "M";
    if (s) return "X";
    try {
      if (document.referrer && new URL(document.referrer).host !== location.host) return "R";
    } catch (e) {}
    return "D";
  }
  function campChar(t) {
    if (t.utm_campaign && CAMPAIGNS[t.utm_campaign]) return CAMPAIGNS[t.utm_campaign];
    return t.tagged ? "X" : "0";
  }
  function makeRef(t) {
    var mins = Math.max(0, Math.floor((t.at - EPOCH) / 60000)).toString(36).toUpperCase();
    var rnd = "";
    for (var i = 0; i < 2; i++) rnd += RAND_SET.charAt(Math.floor(Math.random() * RAND_SET.length));
    return "NCR-" + srcChar(t) + campChar(t) + "-" + mins + "-" + rnd;
  }

  // ---- build / update the record ------------------------------------------
  var touch = parseTouch();
  var attr = readStore();
  if (!attr) {
    attr = { v: 1, ref: makeRef(touch), first: touch };
    if (touch.tagged) attr.last = touch;
    writeStore(attr);
  } else if (touch.tagged) {
    // A new tagged click: update last-touch and re-mint the reference so its
    // source/campaign characters describe the click that will produce the
    // lead. First-touch stays immutable. Re-minting is safe because a ref
    // only leaves the device inside a WhatsApp message sent AFTER this point.
    var prev = attr.last || attr.first;
    var newClick = touch.gclid && touch.gclid !== (prev.gclid || "");
    var newCampaign = touch.utm_campaign && touch.utm_campaign !== (prev.utm_campaign || "");
    if (newClick || newCampaign || !attr.last) {
      attr.last = touch;
      attr.ref = makeRef(touch);
      writeStore(attr);
    }
  }

  // The touch a new lead should be attributed to: the latest tagged touch,
  // falling back to the first visit.
  function active() { return attr.last || attr.first; }

  window.nacravoAttr = {
    ref: attr.ref,
    get: function () { return attr; },
    waLine: function () { return "Ref: " + attr.ref; },
    // Flat, non-PII payload for dataLayer events and the local lead record.
    leadParams: function () {
      var a = active(), p = { lead_ref: attr.ref };
      ["gclid", "gbraid", "wbraid", "utm_source", "utm_medium", "utm_campaign",
       "utm_term", "utm_content"].forEach(function (k) { if (a[k]) p[k] = a[k]; });
      p.landing_page = a.lp;
      p.landed_at = new Date(a.at).toISOString();
      return p;
    }
  };

  // ---- decorate WhatsApp links with the reference --------------------------
  function decorate(aEl) {
    try {
      var href = aEl.getAttribute("href") || "";
      if (!/wa\.me|api\.whatsapp\.com|web\.whatsapp\.com/i.test(href)) return;
      if (/Ref%3A|Ref:\s*NCR-/i.test(href)) return; // already tagged (any encoding)
      var u = new URL(href, location.href);
      var text = u.searchParams.get("text") || "";
      u.searchParams.set("text", (text ? text + "\n\n" : "Hello Nacravo,\n") + "Ref: " + attr.ref);
      aEl.setAttribute("href", u.toString());
    } catch (e) {}
  }
  function decorateAll() {
    var links = document.querySelectorAll('a[href*="wa.me"],a[href*="api.whatsapp.com"],a[href*="web.whatsapp.com"]');
    for (var i = 0; i < links.length; i++) decorate(links[i]);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", decorateAll);
  else decorateAll();
  // Late-added or re-rendered anchors: patch at click time, before navigation.
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a") : null;
    if (a) decorate(a);
  }, true);

  // Surface the attribution once per page for any future GTM/GA4 wiring.
  // No GTM trigger listens for this today, so it is inert until mapped.
  try {
    window.dataLayer = window.dataLayer || [];
    var evt = { event: "lead_attribution_ready" }, lp = window.nacravoAttr.leadParams();
    for (var k in lp) { if (Object.prototype.hasOwnProperty.call(lp, k)) evt[k] = lp[k]; }
    window.dataLayer.push(evt);
  } catch (e) {}
})();
