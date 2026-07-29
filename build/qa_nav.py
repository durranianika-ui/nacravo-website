"""Navigation regression guard.

Permanently protects the fix for the disappearing Services dropdown. The original
defect was a 14px dead-band between the trigger and the panel (`top:calc(100% +
14px)` with no bridge), plus a second, divergent navigation implementation living
inline in index.html while the service pages used a different one in
assets/nacravo.js.

This checks the STRUCTURE that prevents the bug from coming back, across every
generated page and the homepage:

  1. The shared CSS carries the ::before bridge, a z-index and the mobile
     scroll-lock — so the pointer never crosses dead space and the panel renders
     above the hero.
  2. There is ONE navigation script (assets/nacravo-nav.js) with the hover-intent
     delay, focus-out close and Escape handling, and every page that has the
     dropdown loads it.
  3. No page ships the unbridged 14px gap without the matching bridge.
  4. The homepage no longer carries its own inline dropdown handler (which is how
     the two implementations drifted in the first place).

Run:  python build/qa_nav.py
Exit code is non-zero if any check fails, so it can gate a deploy.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "nacravo.css"
NAVJS = ROOT / "assets" / "nacravo-nav.js"

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


def main():
    css = CSS.read_text(encoding="utf-8")
    navjs = NAVJS.read_text(encoding="utf-8")

    # 1. Shared CSS structural fix ------------------------------------------
    check(".drop-panel::before" in css,
          "nacravo.css: missing the ::before bridge over the trigger-to-panel gap")
    check(re.search(r"\.drop-panel\{[^}]*z-index\s*:", css) is not None,
          "nacravo.css: .drop-panel has no z-index (could render under the hero)")
    check("body.nav-open" in css,
          "nacravo.css: missing body.nav-open scroll lock for the mobile menu")
    check(".has-drop:hover .drop-panel" in css,
          "nacravo.css: missing the :hover CSS fallback for the dropdown")

    # 2. One nav script, with the robust behaviour --------------------------
    for token, label in [("focusout", "focus-out close"),
                         ("Escape", "Escape handling"),
                         ("mouseleave", "hover-intent close"),
                         ("nav-open", "mobile scroll-lock toggle")]:
        check(token in navjs, f"nacravo-nav.js: missing {label}")

    # 3. Every page that has the dropdown is correct ------------------------
    html_files = sorted(ROOT.glob("*.html"))
    dropdown_pages = 0
    for f in html_files:
        html = f.read_text(encoding="utf-8")
        if "drop-panel" not in html:
            continue  # legal/compliance pages use a minimal nav with no dropdown
        dropdown_pages += 1
        name = f.name

        # loads the single shared nav script
        check("/assets/nacravo-nav.js" in html,
              f"{name}: does not load the shared /assets/nacravo-nav.js")

        # bridge coverage: either the external stylesheet (which has it) or inline
        has_bridge = ("/assets/nacravo.css" in html) or (".drop-panel::before" in html)
        check(has_bridge, f"{name}: no ::before bridge (neither nacravo.css nor inline)")

        # if the 14px gap is declared INLINE, the inline bridge must be present too
        if re.search(r"\.drop-panel\{[^}]*top:calc\(100% \+ 14px\)", html):
            check(".drop-panel::before" in html,
                  f"{name}: inline 14px gap with no inline ::before bridge — the exact original bug")

        # the AC mega-menu is wired into the nav
        check("/ac-servicing-dubai" in html,
              f"{name}: AC mega-menu link /ac-servicing-dubai missing from the page")

    # 4. Homepage must not re-grow its own inline dropdown handler ----------
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    check("panel.classList.toggle" not in index and "openDrop" not in index,
          "index.html: still contains an inline dropdown handler — remove it and use nacravo-nav.js")

    check(dropdown_pages >= 17,
          f"expected the dropdown on >=17 pages, found {dropdown_pages}")

    if failures:
        print("NAVIGATION REGRESSION CHECK FAILED:")
        for m in failures:
            print(f"  - {m}")
        return 1
    print(f"Navigation regression check PASSED — {dropdown_pages} pages carry the shared, "
          f"bridged, single-implementation dropdown.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
