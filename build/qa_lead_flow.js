/* Browser-side responsive/accessibility probe for the rebuilt lead flow.
 *
 * Paste-able into any page: returns a compact report the QA runs assert on.
 * Kept in the repo so the same checks can be re-run after a future change
 * instead of being re-derived by hand.
 *
 * Usage in a console:  copy(); JSON.stringify(nacravoLeadProbe(), null, 2)
 */
function nacravoLeadProbe() {
  const de = document.documentElement;
  const f = document.getElementById("leadForm");
  const rect = (el) => (el ? el.getBoundingClientRect() : null);
  const vh = window.innerHeight;

  const overflowing = [...document.querySelectorAll("*")]
    .filter((el) => el.getBoundingClientRect().right > de.clientWidth + 0.5)
    .slice(0, 5)
    .map((el) => el.tagName + "." + (el.className || "").toString().slice(0, 40));

  const mbarLinks = [...document.querySelectorAll(".mbar a")];
  const chips = [...document.querySelectorAll(".lf-chip")];
  const radios = [...document.querySelectorAll(".lf-radio")];
  const small = [...document.querySelectorAll(".mbar a, .lf-chip, .lf-nav .btn, .lp-hero-cta .btn")]
    .filter((el) => {
      const r = el.getBoundingClientRect();
      return r.height > 0 && r.height < 48;
    })
    .map((el) => (el.textContent || "").trim().slice(0, 24) + " h=" + Math.round(el.getBoundingClientRect().height));

  const h1 = rect(document.querySelector("h1"));
  const cta = rect(document.querySelector(".lp-hero-cta"));
  const avail = rect(document.querySelector(".lp-hero-avail"));
  const sel = rect(document.querySelector(".lf-choice"));

  return {
    width: window.innerWidth,
    paid: de.getAttribute("data-paid"),
    horizontalOverflow: de.scrollWidth > de.clientWidth,
    overflowing,
    stickyActions: mbarLinks.map((a) => (a.textContent || "").trim()),
    stickyHasAriaLabels: mbarLinks.every((a) => !!a.getAttribute("aria-label")),
    stickyHeight: Math.round((rect(document.querySelector(".mbar")) || { height: 0 }).height),
    bodyPadBottom: getComputedStyle(document.body).paddingBottom,
    tapTargetsUnder48: small,
    // "in the first screen" is measured against the visual viewport, with the
    // sticky bar's own height excluded from the usable area.
    firstScreen: {
      h1: h1 ? h1.top < vh : null,
      ctas: cta ? cta.bottom < vh : null,
      hours: avail ? avail.bottom < vh : null,
      selector: sel ? sel.top < vh * 1.35 : null,
    },
    form: f
      ? {
          action: f.getAttribute("action"),
          method: f.getAttribute("method"),
          vertical: f.getAttribute("data-vertical"),
          preselected: (document.querySelector(".lf-radio:checked") || {}).value || null,
          steps: document.querySelectorAll(".lf-step").length,
          chipCount: chips.length,
          // Step 1 is native radios with the chip as the <label>, so the browser
          // supplies the radiogroup semantics and keyboard behaviour.
          chipsAreRadios: radios.length === chips.length && radios.every((r) => r.type === "radio"),
          everyChipHasLabel: chips.every((c) => !!c.getAttribute("for")),
          errorRegionIsAlert: (document.getElementById("leadErrors") || {}).getAttribute
            ? document.getElementById("leadErrors").getAttribute("role")
            : null,
          statusIsLive: (document.getElementById("leadStatus") || {}).getAttribute
            ? document.getElementById("leadStatus").getAttribute("aria-live")
            : null,
          everyInputLabelled: [...f.querySelectorAll("input:not([type=hidden]),select,textarea")]
            .filter((i) => i.id && !document.querySelector('label[for="' + i.id + '"]'))
            .map((i) => i.id),
          honeypotOffscreen: (() => {
            const hp = f.querySelector(".lf-hp");
            if (!hp) return null;
            return hp.getBoundingClientRect().right < 0 || getComputedStyle(hp).position === "absolute";
          })(),
        }
      : null,
    navLinksVisible: !!document.querySelector(".nav-links") &&
      getComputedStyle(document.querySelector(".nav-links")).display !== "none",
    breadcrumbVisible: !!document.querySelector(".crumb") &&
      getComputedStyle(document.querySelector(".crumb")).display !== "none",
    floatingWaVisible: !!document.querySelector(".wa-float") &&
      getComputedStyle(document.querySelector(".wa-float")).display !== "none",
  };
}
