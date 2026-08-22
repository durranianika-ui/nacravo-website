/* Nacravo lead flow — three-screen qualification with server-side capture.
 *
 * Replaces the old behaviour, where the "quote form" validated locally, pushed
 * a conversion event and then opened WhatsApp. If the visitor never sent the
 * WhatsApp message Nacravo received nothing, while the ad platforms had already
 * counted a conversion.
 *
 * Order of operations now:
 *   1. the visitor answers three short screens (what / scope / where + number);
 *   2. the browser POSTs to /api/leads, which writes the lead to the CRM;
 *   3. ONLY after a 2xx do we announce success and push the conversion event;
 *   4. WhatsApp and Call are offered as optional continuations, tracked
 *      separately (wa_opened) so a handover is never counted as a second lead.
 *
 * Analytics contract (see also assets/nacravo.js):
 *   lead_form_started   observation  — first meaningful interaction
 *   service_selected /
 *   problem_selected    observation  — step 1 answer
 *   lead_created        PRIMARY      — server accepted a unique lead
 *   generate_lead       PRIMARY      — same moment, kept so the existing GTM
 *                                      Google Ads tag keeps working unchanged
 *   wa_opened           observation  — post-capture WhatsApp handover
 * No name, phone, building, note or WhatsApp message text is ever pushed.
 *
 * Markup contract (built by build/template.py):
 *   form#leadForm[data-vertical][data-service|data-problem][action=/api/leads]
 *   .lf-step[data-step="1|2|3"], input.lf-radio[data-intent] + label.lf-chip,
 *   [data-lf-next], [data-lf-back], #leadSuccess, #leadRefOut, #leadWaBtn
 */
(function () {
  "use strict";

  var form = document.getElementById("leadForm");
  if (!form) return;

  var PAGE = window.NACRAVO_PAGE || {};
  var WA_NUMBER = "971555403038";
  var ENDPOINT = form.getAttribute("action") || "/api/leads";
  var VERTICAL = form.getAttribute("data-vertical") === "ac" ? "ac" : "cleaning";
  var IS_AC = VERTICAL === "ac";

  var steps = [].slice.call(form.querySelectorAll(".lf-step"));
  var statusEl = document.getElementById("leadStatus");
  var successEl = document.getElementById("leadSuccess");
  var refOut = document.getElementById("leadRefOut");
  var waBtn = document.getElementById("leadWaBtn");
  var errSummary = document.getElementById("leadErrors");
  var fallbackEl = document.getElementById("leadFallback");
  var fallbackWa = document.getElementById("leadFallbackWa");
  var progressEl = form.querySelector(".lf-progress");

  var current = 1;
  var startedPushed = false;
  var submitting = false;
  var done = false;
  /* One idempotency key per submission attempt. Reused across retries so a
     failed-then-retried POST can never create two CRM leads. */
  var submissionId = null;

  /* ------------------------------------------------------------- utilities */

  function track(event, params) {
    try {
      window.dataLayer = window.dataLayer || [];
      var o = { event: event, vertical: VERTICAL, page_path: location.pathname };
      if (params) for (var k in params) if (Object.prototype.hasOwnProperty.call(params, k) && params[k] !== undefined) o[k] = params[k];
      window.dataLayer.push(o);
    } catch (e) {}
  }

  function newSubmissionId() {
    try { return crypto.randomUUID().replace(/-/g, ""); } catch (e) {}
    return "s" + Date.now().toString(36) + Math.random().toString(36).slice(2, 12);
  }

  /* "" while no experiment is running, so the parameter is simply absent. */
  function experimentId() {
    var e = (window.nacravoExperiment && window.nacravoExperiment.id()) || "";
    return e || form.getAttribute("data-experiment") || undefined;
  }

  function field(name) { return form.elements[name] || null; }

  function value(name) {
    var el = field(name);
    if (!el) return "";
    // form.elements[name] returns a collection whenever several controls share
    // the name. Two cases, and they must not be confused:
    //   - the chip groups are radios, where the collection's .value is already
    //     the checked value;
    //   - "size" exists twice, once for residential bedrooms and once for
    //     commercial floor area, and only one of the pair is ever enabled.
    //     Reading .value there returns "" and silently drops the answer.
    if (typeof el.length === "number" && !el.tagName) {
      var allRadio = true;
      for (var i = 0; i < el.length; i++) if (el[i].type !== "radio") { allRadio = false; break; }
      if (!allRadio) {
        for (var j = 0; j < el.length; j++) {
          var c = el[j];
          if (!c.disabled && String(c.value || "").trim()) return String(c.value).trim();
        }
        return "";
      }
    }
    if (el.type === "checkbox") return el.checked ? "1" : "";
    return String(el.value || "").trim();
  }

  /* Bucketed, non-identifying zone for analytics. The full area/building text
     goes to the CRM only — never to GA4, Google Ads or Meta. */
  function areaZone(area) {
    var a = (area || "").toLowerCase();
    if (/business\s*bay/.test(a)) return "business-bay";
    if (/downtown|burj|dubai\s*mall/.test(a)) return "downtown";
    if (/difc|financial\s*cent/.test(a)) return "difc";
    if (/marina|jbr|jlt|jumeirah\s*lake/.test(a)) return "marina-jlt";
    if (/palm|jumeirah/.test(a)) return "jumeirah-palm";
    if (a) return "other-dubai";
    return "unknown";
  }

  function announce(msg, kind) {
    if (!statusEl) return;
    statusEl.textContent = msg || "";
    statusEl.className = "form-status" + (kind ? " " + kind : "") + (msg ? " show" : "");
  }

  function showErrors(list) {
    if (!errSummary) return;
    if (!list || !list.length) { errSummary.hidden = true; errSummary.innerHTML = ""; return; }
    var html = '<h3 tabindex="-1">Please check the following</h3><ul>';
    list.forEach(function (e) {
      html += '<li><a href="#' + e.id + '">' + e.msg + "</a></li>";
    });
    errSummary.innerHTML = html + "</ul>";
    errSummary.hidden = false;
    var h = errSummary.querySelector("h3");
    if (h) h.focus();
  }

  function setInvalid(el, invalid, msg) {
    if (!el) return;
    var wrap = el.closest(".field") || el.closest(".lf-choice");
    if (wrap) wrap.classList.toggle("invalid", !!invalid);
    el.setAttribute("aria-invalid", invalid ? "true" : "false");
    if (msg) {
      var m = wrap && wrap.querySelector(".err-msg");
      if (m) m.textContent = msg;
    }
  }

  /* ------------------------------------------------------------------ steps */

  function showStep(n, focus) {
    current = n;
    steps.forEach(function (s) {
      var on = Number(s.getAttribute("data-step")) === n;
      s.classList.toggle("is-current", on);
      s.hidden = !on;
      s.setAttribute("aria-hidden", on ? "false" : "true");
    });
    if (progressEl) {
      progressEl.textContent = "Step " + n + " of 3";
      progressEl.setAttribute("data-step", String(n));
    }
    showErrors(null);
    announce("");
    if (focus !== false) {
      var target = steps[n - 1] && steps[n - 1].querySelector(
        ".lf-radio:checked, .lf-radio, input:not([type=hidden]), select, textarea, button"
      );
      if (target) { try { target.focus({ preventScroll: true }); } catch (e) { target.focus(); } }
      var head = form.querySelector(".lf-head");
      if (head && n > 1) {
        var r = form.getBoundingClientRect();
        if (r.top < 0 || r.top > window.innerHeight * 0.6) {
          form.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }
    }
  }

  function markStarted() {
    if (startedPushed) return;
    startedPushed = true;
    track("lead_form_started", {
      service: IS_AC ? undefined : (value("service") || undefined),
      problem: IS_AC ? (value("problem") || undefined) : undefined,
      experiment_id: experimentId(),
    });
  }

  /* --------------------------------------------------------------- chips */

  function radioFor(key) {
    return form.querySelector('.lf-radio[data-intent~="' + key.replace(/["\\]/g, "") + '"]');
  }

  function onChoice(radio, silent) {
    if (!radio) return;
    radio.checked = true;
    var group = radio.closest(".lf-choice");
    if (group) group.classList.remove("invalid");
    setInvalid(radio, false);
    applyConditional();
    if (!silent) {
      markStarted();
      if (radio.name === "problem") track("problem_selected", { problem: radio.value, cta_location: "hero_selector" });
      else track("service_selected", { service: radio.value, cta_location: "hero_selector" });
    }
  }

  /* Scope questions that only make sense for some answers: an office enquiry
     is not asked how many bedrooms, and only AC work asks unit count. */
  function applyConditional() {
    var svc = value("service");
    var commercial = /office/i.test(svc);
    form.querySelectorAll("[data-when]").forEach(function (el) {
      var rule = el.getAttribute("data-when");
      var on = rule === "commercial" ? commercial : rule === "residential" ? !commercial : true;
      el.hidden = !on;
      el.querySelectorAll("input,select,textarea").forEach(function (i) { i.disabled = !on; });
    });
  }

  form.addEventListener("change", function (e) {
    if (e.target && e.target.classList && e.target.classList.contains("lf-radio")) onChoice(e.target);
  });

  form.addEventListener("click", function (e) {
    var next = e.target.closest ? e.target.closest("[data-lf-next]") : null;
    if (next) { e.preventDefault(); if (validateStep(current)) showStep(Math.min(3, current + 1)); return; }

    var back = e.target.closest ? e.target.closest("[data-lf-back]") : null;
    if (back) { e.preventDefault(); showStep(Math.max(1, current - 1)); return; }
  });

  form.addEventListener("input", function (e) {
    markStarted();
    if (e.target && e.target.closest && e.target.closest(".field.invalid")) setInvalid(e.target, false);
  });

  /* ----------------------------------------------------------- validation */

  function validPhone(v) {
    var d = String(v || "").replace(/\D/g, "");
    return d.length >= 8 && d.length <= 15;
  }

  function validateStep(n) {
    var errs = [];
    if (n === 1) {
      var key = IS_AC ? "problem" : "service";
      if (!value(key)) {
        var grp = form.querySelector('.lf-choice[data-name="' + key + '"]');
        if (grp) grp.classList.add("invalid");
        var first = grp && grp.querySelector(".lf-radio");
        errs.push({ id: first ? first.id : "leadForm",
                    msg: IS_AC ? "Choose what your AC is doing." : "Choose what you need cleaned." });
      }
    }
    if (n === 3) {
      var area = field("area"), phone = field("phone");
      if (!area || area.value.trim().length < 2) {
        setInvalid(area, true, "Tell us the area or building so we can check coverage.");
        errs.push({ id: "area", msg: "Enter the area or building." });
      }
      if (!phone || !validPhone(phone.value)) {
        setInvalid(phone, true, "Enter a valid number we can reach you on.");
        errs.push({ id: "phone", msg: "Enter a valid contact number." });
      }
      var email = field("email");
      if (email && email.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email.value.trim())) {
        setInvalid(email, true, "Enter a valid email address, or leave it blank.");
        errs.push({ id: "email", msg: "Check the email address." });
      }
    }
    showErrors(errs);
    if (errs.length) {
      var target = document.getElementById(errs[0].id);
      if (target && !errSummary) target.focus();
      return false;
    }
    return true;
  }

  /* --------------------------------------------------------------- payload */

  function collect() {
    var p = {
      vertical: VERTICAL,
      service: IS_AC ? undefined : value("service"),
      problem: IS_AC ? value("problem") : undefined,
      property_type: value("property_type") || undefined,
      size: value("size") || undefined,
      units: value("units") || undefined,
      frequency: value("frequency") || undefined,
      area: value("area"),
      name: value("name") || undefined,
      company: value("company") || undefined,
      email: value("email") || undefined,
      phone: value("phone"),
      preferred_date: value("preferred_date") || undefined,
      notes: value("notes") || undefined,
      website: value("website") || undefined, // honeypot
      page_url: location.origin + location.pathname,
      consent_marketing: !!(field("consent_marketing") && field("consent_marketing").checked),
      privacy_version: "1.0",
      experiment: experimentId(),
      submission_id: submissionId,
    };
    if (window.nacravoAttr && window.nacravoAttr.serverParams) {
      var a = window.nacravoAttr.serverParams();
      for (var k in a) if (Object.prototype.hasOwnProperty.call(a, k) && p[k] === undefined) p[k] = a[k];
    }
    return p;
  }

  /* Customer-facing WhatsApp text. Carries the short reference and nothing
     else from the attribution layer — no GCLID, GBRAID, WBRAID or UTMs. */
  /* Each AC answer needs its own phrasing: "my AC is bad smell" is not a
     sentence a customer would send. */
  var AC_PHRASE = {
    "Not cooling": "my AC is not cooling",
    "Leaking": "my AC is leaking",
    "Strange noise": "my AC is making a strange noise",
    "Bad smell": "my AC has a bad smell",
    "Service": "I need an AC service",
    "Chemical clean": "I need an AC chemical clean",
    "Duct cleaning": "I need AC duct cleaning",
    "Installation": "I need an AC installation",
    "Maintenance contract": "I would like an AC maintenance contract",
    "Not sure": "I have an AC problem I cannot identify",
  };

  function waMessage(ref) {
    var area = value("area"), lines;
    if (IS_AC) {
      var units = value("units");
      var problem = value("problem");
      lines = "Hi Nacravo - " + (AC_PHRASE[problem] || "I need help with my AC") +
        " in " + (area || "Dubai") + "." +
        (value("property_type") ? " Property: " + value("property_type") + "." : "") +
        (units ? " Units: " + units + "." : "") +
        (value("preferred_date") ? " I need " + value("preferred_date") + "." : " I need this as soon as possible.");
    } else {
      lines = "Hi Nacravo - I need " + (value("service") || "cleaning") +
        (value("size") ? " for a " + value("size") : "") +
        (value("property_type") ? " " + value("property_type").toLowerCase() : "") +
        " in " + (area || "Dubai") + "." +
        (value("frequency") ? " Frequency: " + value("frequency") + "." : "") +
        (value("preferred_date") ? " Preferred date: " + value("preferred_date") + "." : "");
    }
    return lines + "\n\nRef: " + ref;
  }

  /* ---------------------------------------------------------------- submit */

  function fail(msg, kind) {
    submitting = false;
    var btn = form.querySelector("[data-lf-submit]");
    if (btn) { btn.disabled = false; btn.removeAttribute("aria-busy"); }
    announce(msg, kind || "err");
  }

  /* The lead store is unreachable. Hand the visitor a WhatsApp message that
     already contains their answers, and record that capture failed — as an
     observation, never as a conversion: no lead exists to count. */
  function offerFallback() {
    if (!fallbackEl) return;
    var ref = (window.nacravoAttr && window.nacravoAttr.ref) || "";
    if (fallbackWa) {
      fallbackWa.setAttribute("href",
        "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(waMessage(ref)));
    }
    fallbackEl.hidden = false;
    track("lead_capture_unavailable", {
      service: IS_AC ? value("problem") : value("service"),
      area_zone: areaZone(value("area")),
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (submitting || done) return;
    if (!validateStep(1)) { showStep(1); return; }
    if (!validateStep(3)) return;

    submitting = true;
    if (!submissionId) submissionId = newSubmissionId();
    var btn = form.querySelector("[data-lf-submit]");
    if (btn) { btn.disabled = true; btn.setAttribute("aria-busy", "true"); }
    announce("Sending your request to Nacravo…", "busy");

    var ctl = null, timer = null;
    try {
      ctl = new AbortController();
      timer = setTimeout(function () { ctl.abort(); }, 12000);
    } catch (err) {}

    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(collect()),
      signal: ctl ? ctl.signal : undefined,
    })
      .then(function (r) {
        if (timer) clearTimeout(timer);
        return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; });
      })
      .then(function (out) {
        if (out.status === 201 || out.status === 200) return succeed(out.body, out.status);
        if (out.status === 400) {
          var f = (out.body && out.body.fields) || {};
          var errs = Object.keys(f).map(function (k) {
            var el = field(k);
            if (el) setInvalid(el, true);
            return { id: el ? k : "leadForm", msg: "Check the " + k.replace(/_/g, " ") + " you entered." };
          });
          showErrors(errs);
          if (f.service || f.problem) showStep(1);
          return fail("Please correct the highlighted answers and try again.");
        }
        if (out.status === 429) {
          return fail("We have already received several requests from this device. Please call or message us on WhatsApp instead.");
        }
        offerFallback();
        return fail(out.status === 503
          ? "Our request system is temporarily unavailable. Send us the details directly and we will pick them up straight away."
          : "We could not save your request just now. Please try again, or send it to us directly below.");
      })
      .catch(function () {
        if (timer) clearTimeout(timer);
        offerFallback();
        fail("Your request did not reach us \u2014 check your connection and try again, or send the details directly below.");
      });
  });

  function succeed(body, status) {
    done = true;
    submitting = false;
    var ref = (body && body.lead_ref) || (window.nacravoAttr && window.nacravoAttr.ref) || "";
    var leadId = (body && body.lead_id) || "";
    var isDup = !!(body && body.dup);

    /* ONE conversion per lead. A 200/dup replay is the same customer action as
       the 201 that preceded it, so it must not fire a second conversion. */
    if (!isDup && status === 201) {
      var payload = {
        lead_id: leadId,
        lead_ref: ref,
        event_id: leadId,               // browser/server/CRM dedup key
        service: IS_AC ? value("problem") : value("service"),
        area_zone: areaZone(value("area")),
        vertical: VERTICAL,
        experiment_id: experimentId(),
        lead_type: "form",
        form_name: "lead_flow",
      };
      track("lead_created", payload);
      /* Kept so the existing GTM Google Ads conversion tag keeps working
         unchanged — but now it fires only AFTER the CRM has the lead. */
      var legacy = {};
      for (var k in payload) if (Object.prototype.hasOwnProperty.call(payload, k)) legacy[k] = payload[k];
      legacy.service_name = payload.service;
      legacy.value = 0;
      legacy.currency = "AED";
      track("generate_lead", legacy);
    }

    var waURL = "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(waMessage(ref));
    if (waBtn) {
      waBtn.setAttribute("href", waURL);
      waBtn.setAttribute("data-no-track", "");   // counted as wa_opened, not whatsapp_click
      waBtn.addEventListener("click", function () {
        track("wa_opened", { lead_id: leadId, service: IS_AC ? value("problem") : value("service"), cta_location: "lead_success" });
      });
    }
    if (refOut) refOut.textContent = ref;
    announce("");

    if (fallbackEl) fallbackEl.hidden = true;
    steps.forEach(function (s) { s.hidden = true; s.classList.remove("is-current"); });
    var chrome = form.querySelector(".lf-chrome");
    if (chrome) chrome.hidden = true;
    if (progressEl) progressEl.hidden = true;
    if (successEl) {
      successEl.hidden = false;
      var h = successEl.querySelector("h2, h3");
      if (h) { h.setAttribute("tabindex", "-1"); try { h.focus(); } catch (e) {} }
    }
  }

  /* ------------------------------------------------- preselection & wiring */

  /* Allow-listed intent preselection. Only a value that already exists as a
     chip on this page can be selected, so nothing from the query string is
     ever written into the document. */
  function preselect() {
    var wanted = "";
    try {
      var q = new URLSearchParams(location.search);
      wanted = (q.get("intent") || "").slice(0, 40);
    } catch (e) {}
    if (!wanted && location.hash) wanted = location.hash.slice(1);
    if (!wanted) return;                       // the page default is already checked
    var key = wanted.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    onChoice(radioFor(key), true);
  }

  /* Chips or links elsewhere on the page can jump into the flow with the answer
     already set. Only a value that exists as a radio on this page can be
     chosen, so nothing from the query string is ever written into the page. */
  document.addEventListener("click", function (e) {
    var jump = e.target.closest ? e.target.closest("[data-lf-jump]") : null;
    if (!jump) return;
    e.preventDefault();
    var r = radioFor(jump.getAttribute("data-lf-jump"));
    if (r) onChoice(r);
    form.scrollIntoView({ behavior: "smooth", block: "start" });
    showStep(r ? 2 : 1);
  });

  preselect();
  applyConditional();
  showStep(1, false);
})();
