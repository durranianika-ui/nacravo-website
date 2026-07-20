/* Nacravo shared behaviour — vanilla JS, no dependencies.
 *
 * Consolidates what index.html runs inline, so every landing page gets the
 * identical tracking contract from one cached file:
 *   1. dataLayer tracking utility (window.nacravoTrack)
 *   2. optional direct pixel loaders (dormant unless LOAD_PIXELS_DIRECTLY)
 *   3. cookie consent / Consent Mode v2 updates
 *   4. hero lead form -> WhatsApp handover
 *   5. navigation (desktop dropdown + mobile menu) and floating WhatsApp
 *
 * The event names, DEDUP_MS guard and the single generate_lead push with
 * eventCallback are carried over unchanged — GTM triggers keep working and
 * conversions are never double-counted.
 *
 * Per-page configuration comes from window.NACRAVO_PAGE:
 *   { service: "Home Cleaning", waText: "…", subservices: { "chemical-wash": "Chemical Wash" } }
 */
(function () {
  "use strict";

  var PAGE = window.NACRAVO_PAGE || {};
  var WHATSAPP_NUMBER = "971581082601";

  /* ============================================================
     1. TRACKING UTILITY
     ============================================================ */
  var BUSINESS_NAME = "Nacravo", LOCATION = "Dubai";
  window.dataLayer = window.dataLayer || [];

  function push(event, params) {
    try {
      var o = { event: event, business_name: BUSINESS_NAME, location: LOCATION,
                page_path: location.pathname + location.search, page_title: document.title };
      if (PAGE.service) o.service_name = PAGE.service;
      if (params) { for (var k in params) { if (Object.prototype.hasOwnProperty.call(params, k) && params[k] !== undefined) o[k] = params[k]; } }
      window.dataLayer.push(o);
    } catch (e) {}
  }

  var recent = {}, DEDUP_MS = 1200;
  function dup(key) { var now = Date.now(), last = recent[key]; recent[key] = now; return last && (now - last) < DEDUP_MS; }

  function pageView(p) { push("page_view", p); }
  function formSubmit(name, p) {
    if (dup("form:" + name)) return;
    p = p || {}; p.form_name = name; if (!p.lead_type) p.lead_type = "form";
    push("form_submit", p); push("generate_lead", p);
  }
  function whatsapp(p) { p = p || {}; if (dup("wa:" + (p.link_url || p.button_text || "x"))) return; p.lead_type = "whatsapp"; push("whatsapp_click", p); }
  function phone(p)    { p = p || {}; if (dup("tel:" + (p.link_url || p.button_text || "x"))) return; p.lead_type = "phone"; push("phone_click", p); }
  function quote(p)    { p = p || {}; if (dup("quote:" + (p.button_text || "x"))) return; p.lead_type = "quote"; push("quote_click", p); }
  function booking(p)  { p = p || {}; if (dup("book:" + (p.button_text || "x"))) return; p.lead_type = "booking"; push("booking_click", p); }
  function service(name, p) { p = p || {}; if (dup("svc:" + name)) return; p.service_name = name; push("service_view", p); }
  function outbound(url, p) { p = p || {}; if (dup("out:" + url)) return; p.link_url = url; push("outbound_click", p); }
  function cta(type, lbl) { if (dup("cta:" + type + ":" + lbl)) return; push("cta_click", { cta_type: type, button_text: lbl }); }

  window.nacravoTrack = { pageView: pageView, formSubmit: formSubmit, whatsapp: whatsapp,
    phone: phone, quote: quote, booking: booking, service: service, outbound: outbound, cta: cta, push: push };

  function labelOf(el) {
    return (el.getAttribute("data-track-label") || (el.textContent || "").replace(/\s+/g, " ").trim()).slice(0, 80);
  }

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var anchor  = t.closest("a");
    var tracked = t.closest("[data-track]");

    if (tracked) {
      var kind = tracked.getAttribute("data-track"), lbl = labelOf(tracked);
      var svc = tracked.getAttribute("data-service-name") || undefined;
      if (kind === "quote") { quote({ button_text: lbl }); cta("quote", lbl); }
      else if (kind === "booking") { booking({ button_text: lbl, service_name: svc }); cta("booking", lbl); }
      else if (kind === "service") service(svc || lbl, { button_text: lbl });
    }

    if (anchor && !anchor.hasAttribute("data-no-track")) {
      var href = anchor.getAttribute("href") || "", text = labelOf(anchor);
      if (/wa\.me|api\.whatsapp\.com|whatsapp:\/\//i.test(href)) { whatsapp({ link_url: href, button_text: text }); return; }
      if (/^tel:/i.test(href)) { phone({ link_url: href, button_text: text }); return; }
      if (/^mailto:/i.test(href)) { push("generate_lead", { lead_type: "email", link_url: href, button_text: text }); return; }
      if (/^https?:\/\//i.test(href)) {
        try { var u = new URL(href, location.href); if (u.host !== location.host) outbound(u.href, { button_text: text }); } catch (err) {}
      }
    }
  }, true);

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { pageView(); });
  else pageView();

  /* ============================================================
     2. OPTIONAL DIRECT PIXEL LOADERS
     Dormant unless NACRAVO_TRACKING.LOAD_PIXELS_DIRECTLY is true AND the
     platform ID is filled in. Leaving the flag false and wiring platforms as
     GTM tags is the recommended setup — it avoids double-counting.
     ============================================================ */
  (function () {
    var C = window.NACRAVO_TRACKING || {};
    if (!C.LOAD_PIXELS_DIRECTLY) return;
    try {
      if (/^G-/.test(C.GA4_ID || "")) {
        var g = document.createElement("script"); g.async = true;
        g.src = "https://www.googletagmanager.com/gtag/js?id=" + C.GA4_ID;
        document.head.appendChild(g);
        window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
        window.gtag("js", new Date());
        window.gtag("config", C.GA4_ID);
        if (/^AW-/.test(C.GOOGLE_ADS_ID || "")) window.gtag("config", C.GOOGLE_ADS_ID);
      }
      if (C.META_PIXEL_ID) {
        !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0"; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
        window.fbq("init", C.META_PIXEL_ID); window.fbq("track", "PageView");
      }
      if (C.CLARITY_ID) {
        (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments) }; t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, "clarity", "script", C.CLARITY_ID);
      }
      if (C.LINKEDIN_PARTNER_ID) {
        window._linkedin_partner_id = C.LINKEDIN_PARTNER_ID;
        window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
        window._linkedin_data_partner_ids.push(C.LINKEDIN_PARTNER_ID);
        (function (l) { if (!l) { window.lintrk = function (a, b) { window.lintrk.q.push([a, b]) }; window.lintrk.q = [] } var s = document.getElementsByTagName("script")[0]; var b = document.createElement("script"); b.type = "text/javascript"; b.async = true; b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js"; s.parentNode.insertBefore(b, s); })(window.lintrk);
      }
      if (C.TIKTOK_PIXEL_ID) {
        !function (w, d, t) { w.TiktokAnalyticsObject = t; var ttq = w[t] = w[t] || []; ttq.methods = ["page", "track", "identify", "instances", "debug", "on", "off", "once", "ready", "alias", "group", "enableCookie", "disableCookie"]; ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))) } }; for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]); ttq.instance = function (t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e }; ttq.load = function (e, n) { var i = "https://analytics.tiktok.com/i18n/pixel/events.js"; ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = i; ttq._t = ttq._t || {}; ttq._t[e] = +new Date; ttq._o = ttq._o || {}; ttq._o[e] = n || {}; var o = d.createElement("script"); o.type = "text/javascript"; o.async = !0; o.src = i + "?sdkid=" + e + "&lib=" + t; var a = d.getElementsByTagName("script")[0]; a.parentNode.insertBefore(o, a) }; ttq.load(C.TIKTOK_PIXEL_ID); ttq.page(); }(window, document, "ttq");
      }
      if (C.PINTEREST_TAG_ID) {
        !function (e) { if (!window.pintrk) { window.pintrk = function () { window.pintrk.queue.push(Array.prototype.slice.call(arguments)) }; var n = window.pintrk; n.queue = []; n.version = "3.0"; var t = document.createElement("script"); t.async = !0; t.src = e; var r = document.getElementsByTagName("script")[0]; r.parentNode.insertBefore(t, r) } }("https://s.pinimg.com/ct/core.js");
        window.pintrk("load", C.PINTEREST_TAG_ID); window.pintrk("page");
      }
    } catch (e) {}
  })();

  /* ============================================================
     3. COOKIE CONSENT (Google Consent Mode v2)
     Adds body.cc-open while the banner shows so the floating WhatsApp
     button can lift clear of it instead of overlapping.
     ============================================================ */
  (function () {
    var KEY = "nacravo_consent";
    var banner = document.getElementById("ccBanner"), modal = document.getElementById("ccModal");
    if (!banner || !modal) return;

    function get() { try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; } }
    function apply(c) {
      var a = c.analytics ? "granted" : "denied", d = c.ad ? "granted" : "denied";
      if (typeof gtag === "function") { gtag("consent", "update", { ad_storage: d, ad_user_data: d, ad_personalization: d, analytics_storage: a }); }
      try { window.dataLayer = window.dataLayer || []; window.dataLayer.push({ event: "consent_update", consent_analytics: c.analytics, consent_ad: c.ad }); } catch (e) {}
    }
    function save(c) { c.ts = new Date().toISOString(); c.v = "1.0"; try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} apply(c); hide(); }
    function show() { banner.classList.add("show"); document.body.classList.add("cc-open"); }
    function hide() { banner.classList.remove("show"); document.body.classList.remove("cc-open"); }
    function openModal() {
      var c = get() || {};
      var a = document.getElementById("ccAnalytics"), d = document.getElementById("ccAds");
      if (a) a.checked = !!c.analytics;
      if (d) d.checked = !!c.ad;
      modal.classList.add("show");
    }
    function closeModal() { modal.classList.remove("show"); }

    document.getElementById("ccAccept").addEventListener("click", function () { save({ analytics: true, ad: true }); });
    document.getElementById("ccReject").addEventListener("click", function () { save({ analytics: false, ad: false }); });
    document.getElementById("ccPrefs").addEventListener("click", openModal);
    document.getElementById("ccSave").addEventListener("click", function () { save({ analytics: document.getElementById("ccAnalytics").checked, ad: document.getElementById("ccAds").checked }); closeModal(); });
    document.getElementById("ccClose").addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });
    window.nacravoCookieSettings = function () { openModal(); return false; };
    if (!get()) show();
  })();

  /* ============================================================
     4. HERO LEAD FORM -> WHATSAPP
     Mirrors the homepage handler: validate, lock with a one-shot guard,
     push exactly one generate_lead, then hand over to WhatsApp via
     eventCallback with a timeout backstop.
     ============================================================ */
  (function () {
    var form = document.getElementById("leadForm");
    if (!form) return;
    var statusEl = document.getElementById("leadStatus");

    function setInvalid(el, isInvalid) {
      var field = el.closest(".field");
      if (field) field.classList.toggle("invalid", isInvalid);
    }
    function validPhone(v) { return /[0-9]{7,}/.test(v.replace(/[\s()+-]/g, "")); }
    function val(nameAttr) { return form[nameAttr] ? form[nameAttr].value.trim() : ""; }

    var leadSent = false;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (leadSent) return;

      var f = {
        name: val("name"), phone: val("phone"), service: val("service"),
        subservice: val("subservice"), location: val("location"),
        property: val("property"), date: val("date"), notes: val("notes")
      };

      var ok = true;
      function check(el, valid) { if (!el) return; setInvalid(el, !valid); if (!valid) ok = false; }
      check(form.name, f.name.length > 1);
      check(form.phone, validPhone(f.phone));
      check(form.service, f.service !== "");
      check(form.location, f.location.length > 1);

      if (!ok) {
        if (statusEl) statusEl.className = "form-status";
        var firstBad = form.querySelector(".field.invalid input, .field.invalid select");
        if (firstBad) firstBad.focus();
        return;
      }

      var lines = ["Hello Nacravo,", "", "I'd like to request a quotation.", "",
        "Name: " + f.name, "Phone: " + f.phone, "Service Required: " + f.service];
      if (f.subservice) lines.push("Specific Service: " + f.subservice);
      lines.push("Location: " + f.location);
      if (f.property) lines.push("Property Type: " + f.property);
      if (f.date) lines.push("Preferred Date: " + f.date);
      if (f.notes) lines.push("Additional Notes: " + f.notes);
      lines.push("", "Please contact me.");

      var waURL = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(lines.join("\n"));

      leadSent = true;
      var submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      if (statusEl) statusEl.className = "form-status ok";

      // Reserve the tab inside the click gesture so the popup blocker can't stop it.
      var waWin = null;
      try { waWin = window.open("about:blank", "_blank"); } catch (err) {}

      try {
        var store = JSON.parse(localStorage.getItem("nacravo_leads") || "[]");
        store.push({ ts: new Date().toISOString(), name: f.name, phone: f.phone,
                     service: f.service, subservice: f.subservice,
                     property: f.property, location: f.location });
        localStorage.setItem("nacravo_leads", JSON.stringify(store));
      } catch (err) {}

      var opened = false;
      function openWhatsApp() {
        if (opened) return; opened = true;
        if (waWin && !waWin.closed) { try { waWin.location.href = waURL; return; } catch (err) {} }
        window.location.href = waURL;
      }

      // ONE generate_lead drives both the GA4 tag and the Google Ads conversion
      // inside GTM. eventTimeout caps the wait so the handover never hangs.
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: "generate_lead",
        form_name: "lead_form",
        lead_type: "whatsapp",
        service_name: f.service,
        subservice_name: f.subservice || undefined,
        property_type: f.property || undefined,
        location: f.location,
        value: 0,
        currency: "AED",
        eventTimeout: 1200,
        eventCallback: openWhatsApp
      });

      // Backstop if GTM is blocked and eventCallback never runs.
      setTimeout(openWhatsApp, 1500);
    });

    form.addEventListener("input", function (e) {
      if (e.target.closest(".field.invalid")) setInvalid(e.target, false);
    });

    /* ---- Service preselection ----
       The service select is already set server-side per page. This additionally
       preselects the SUB-service when the visitor arrives on, or jumps to, an
       anchor section (e.g. /ac-service-dubai#chemical-wash), and when they use
       a "Get a quote" button inside one of those sections. */
    var subField = form.subservice;
    var map = PAGE.subservices || {};

    function setSub(key) {
      if (!subField || !key) return;
      var label = map[key];
      if (!label) return;
      if (subField.tagName === "SELECT") {
        for (var i = 0; i < subField.options.length; i++) {
          if (subField.options[i].value === label) { subField.selectedIndex = i; break; }
        }
      } else {
        subField.value = label;
      }
    }

    if (location.hash) setSub(location.hash.slice(1));
    window.addEventListener("hashchange", function () { setSub(location.hash.slice(1)); });

    document.addEventListener("click", function (e) {
      var el = e.target.closest ? e.target.closest("[data-subservice]") : null;
      if (el) setSub(el.getAttribute("data-subservice"));
    });
  })();

  /* ============================================================
     5. NAVIGATION + FLOATING WHATSAPP
     ============================================================ */
  (function () {
    // Desktop services dropdown
    var toggle = document.querySelector(".drop-toggle");
    var panel = document.querySelector(".drop-panel");
    if (toggle && panel) {
      function closeDrop() { panel.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
      toggle.addEventListener("click", function (e) {
        e.stopPropagation();
        var open = panel.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
      document.addEventListener("click", function (e) {
        if (!panel.contains(e.target) && e.target !== toggle) closeDrop();
      });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDrop(); });
      // open on hover for pointer users, without breaking keyboard/touch
      var wrap = toggle.closest(".has-drop");
      if (wrap && window.matchMedia("(hover:hover)").matches) {
        wrap.addEventListener("mouseenter", function () { panel.classList.add("open"); toggle.setAttribute("aria-expanded", "true"); });
        wrap.addEventListener("mouseleave", closeDrop);
      }
    }

    // Mobile menu
    var menuBtn = document.querySelector(".menu-btn");
    var mobileMenu = document.getElementById("mobileMenu");
    if (menuBtn && mobileMenu) {
      menuBtn.addEventListener("click", function () {
        var open = mobileMenu.classList.toggle("open");
        menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }
  })();

  /* Reveal-on-scroll — mobile only, progressive enhancement.
     If any check fails the content simply stays visible. */
  (function () {
    if (!("IntersectionObserver" in window)) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (!window.matchMedia("(max-width:600px)").matches) return;

    var els = document.querySelectorAll(
      ".pillar,.svc-card,.serve-card,.step,.pkg,.gal-cell,.quality-img,.sec-head,.anchor-card,.rel-card"
    );
    els.forEach(function (el) { el.classList.add("reveal"); });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });

    els.forEach(function (el) { io.observe(el); });
    setTimeout(function () { els.forEach(function (el) { el.classList.add("in"); }); }, 1400);
  })();
})();
