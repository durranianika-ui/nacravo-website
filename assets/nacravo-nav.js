/* Nacravo shared navigation behaviour — the ONE header script every page uses.
 *
 * Loaded standalone (not inside nacravo.js) so the self-contained homepage can
 * share the exact same navigation logic without also pulling in the tracking,
 * lead-form and consent code — which would double-fire those events. There is
 * now a single navigation implementation across the whole site instead of one
 * copy inline in index.html and another in nacravo.js.
 *
 * Desktop Services dropdown:
 *   - opens on hover (pointer devices) AND on click/tap of the trigger;
 *   - stays open while the pointer is over the trigger OR the panel — the CSS
 *     `.drop-panel::before` bridge covers the 14px visual gap, so there is no
 *     dead space to fall through (this is the real fix for the disappearing
 *     menu, not the timeout below);
 *   - closes only when the pointer genuinely leaves the whole .has-drop region
 *     (after a short 180ms intent delay), when Escape is pressed, when focus
 *     leaves the region, or when the user clicks elsewhere;
 *   - is fully keyboard operable (Enter/Space/ArrowDown open, arrows move,
 *     Home/End jump, Escape closes and returns focus, Tab/Shift+Tab exit).
 *
 * Mobile menu:
 *   - the menu button toggles the panel and locks body scroll;
 *   - Services is a native <details> accordion (44px+ tap targets in CSS);
 *   - tapping a real link closes the menu; Escape closes it.
 */
(function () {
  "use strict";
  if (window.__nacravoNavInit) return;      // never bind twice
  window.__nacravoNavInit = true;

  var CLOSE_DELAY = 180; // ms — guards accidental pointer slips only

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    setupDesktopDropdown();
    setupMobileMenu();
  });

  /* ------------------------------------------------ desktop dropdown */
  function setupDesktopDropdown() {
    var wrap = document.querySelector(".has-drop");
    if (!wrap) return;
    var toggle = wrap.querySelector(".drop-toggle");
    var panel = wrap.querySelector(".drop-panel");
    if (!toggle || !panel) return;

    var items = Array.prototype.slice.call(panel.querySelectorAll("a"));
    var closeTimer = null;
    var hoverCapable = !!(window.matchMedia && window.matchMedia("(hover:hover)").matches);

    function open() {
      if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
      panel.classList.add("open");
      toggle.setAttribute("aria-expanded", "true");
    }
    function close() {
      if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
      panel.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    }
    function isOpen() { return panel.classList.contains("open"); }
    function scheduleClose() {
      if (closeTimer) clearTimeout(closeTimer);
      closeTimer = setTimeout(close, CLOSE_DELAY);
    }
    function focusItem(i) {
      if (!items.length) return;
      var idx = (i + items.length) % items.length;
      items[idx].focus();
    }

    // Click / tap toggles — works for touch, keyboard activation and as a mouse
    // fallback. stopPropagation keeps the document click-away handler from
    // immediately re-closing it.
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (isOpen()) close(); else open();
    });

    // Hover intent — pointer devices only. The whole .has-drop is the hover
    // region and the ::before bridge means the pointer never crosses dead space.
    if (hoverCapable) {
      wrap.addEventListener("mouseenter", open);
      wrap.addEventListener("mouseleave", scheduleClose);
    }

    // Keyboard on the trigger.
    toggle.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "Down") { e.preventDefault(); open(); focusItem(0); }
      else if (e.key === "ArrowUp" || e.key === "Up") { e.preventDefault(); open(); focusItem(items.length - 1); }
      else if (e.key === "Escape") { if (isOpen()) { e.preventDefault(); close(); } }
    });

    // Keyboard inside the panel.
    panel.addEventListener("keydown", function (e) {
      var current = items.indexOf(document.activeElement);
      if (e.key === "ArrowDown" || e.key === "Down") { e.preventDefault(); focusItem(current + 1); }
      else if (e.key === "ArrowUp" || e.key === "Up") { e.preventDefault(); focusItem(current - 1); }
      else if (e.key === "Home") { e.preventDefault(); focusItem(0); }
      else if (e.key === "End") { e.preventDefault(); focusItem(items.length - 1); }
      else if (e.key === "Escape") { e.preventDefault(); close(); toggle.focus(); }
    });

    // Close when focus leaves the entire region (Tab / Shift+Tab out).
    wrap.addEventListener("focusout", function (e) {
      if (!wrap.contains(e.relatedTarget)) close();
    });

    // Click anywhere outside closes.
    document.addEventListener("click", function (e) {
      if (isOpen() && !wrap.contains(e.target)) close();
    });

    // Escape closes from anywhere while the menu is open (e.g. opened on hover,
    // focus still on the page body). Return focus to the trigger only if focus
    // was inside the component, so we never yank focus away from elsewhere.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen()) {
        var focusInside = wrap.contains(document.activeElement);
        close();
        if (focusInside) toggle.focus();
      }
    });
  }

  /* ------------------------------------------------ mobile menu */
  function setupMobileMenu() {
    var btn = document.querySelector(".menu-btn");
    var menu = document.getElementById("mobileMenu");
    if (!btn || !menu) return;

    function open() {
      menu.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
      document.body.classList.add("nav-open");   // CSS locks body scroll
    }
    function close() {
      menu.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
    }
    function isOpen() { return menu.classList.contains("open"); }

    btn.addEventListener("click", function () { if (isOpen()) close(); else open(); });

    // Tapping a real link navigates away — close first so there is no flash of
    // an open menu on back-navigation. The <summary> accordion toggle is not an
    // <a>, so expanding "Services" does NOT close the menu.
    menu.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest("a") : null;
      if (a) close();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen()) { close(); btn.focus(); }
    });

    // Clean up if the viewport grows back to desktop while the menu is open.
    if (window.matchMedia) {
      var mq = window.matchMedia("(min-width:901px)");
      var onChange = function () { if (mq.matches && isOpen()) close(); };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
      else if (mq.addListener) mq.addListener(onChange);
    }
  }
})();
