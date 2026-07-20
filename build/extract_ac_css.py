"""Lift the AC-page-only CSS out of the current ac-service-dubai.html.

The AC page is being regenerated through the shared template so it stops
carrying its own duplicate copy of the tracker and consent code. Its genuinely
unique components (comparison table, problems grid, before/after slider,
chemical-wash comparison, property types, brands) are worth keeping, so their
styles are extracted here into a page-scoped stylesheet rather than rewritten.

The reviews-carousel styles are deliberately NOT carried over: those
testimonials are unverified and are being removed from the page.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "ac-service-dubai.html"

# Comment banners inside the page's <style> that mark each block. We take the
# AC-specific ones and stop before the reviews carousel.
WANTED = [
    "/* AC service highlight cards */",
    "/* comparison (why choose) */",
    "/* areas */",
    "/* problems */",
    "/* steps (6) */",
    "/* before / after slider */",
    "/* chemical wash */",
    "/* residential services */",
    "/* brands */",
]
STOP = "/* reviews carousel */"
FINAL_START = "/* final cta */"
FINAL_STOP = "/* footer */"

EXTRA = """

/* ---- AC page: mobile ---- */
@media(max-width:600px){
  .ac-card,.res-card,.chem-card{border-radius:20px}
  .ac-grid,.res-grid,.area-grid,.prob-grid,.steps6,.brand-grid{gap:12px}
  .final h2{font-size:26px}
  .final .hero-cta{flex-direction:column}
  .final .btn{width:100%;min-height:52px;justify-content:center;border-radius:14px}
}
"""


def main():
    text = SRC.read_text(encoding="utf-8")
    style = re.search(r"<style>\n(.*?)\n</style>", text, re.S)
    if not style:
        print(
            "Nothing to do: ac-service-dubai.html no longer has an inline <style>.\n"
            "This is a ONE-SHOT migration script — it has already run and\n"
            "assets/nacravo-ac.css is now the source of truth. Edit that file instead."
        )
        return 0
    css = style.group(1)

    start = css.index(WANTED[0])
    stop = css.index(STOP)
    main_block = css[start:stop].rstrip()

    fstart = css.index(FINAL_START)
    fstop = css.index(FINAL_STOP)
    final_block = css[fstart:fstop].rstrip()

    missing = [w for w in WANTED if w not in main_block]
    if missing:
        print(f"FAILED: expected blocks not inside extracted range: {missing}")
        return 1
    if "rev-card" in main_block or "rev-track" in main_block:
        print("FAILED: reviews styles leaked into the extract")
        return 1

    out = (
        "/* AC landing page — page-scoped components.\n"
        " * Extracted from the previous inline <style> of ac-service-dubai.html by\n"
        " * build/extract_ac_css.py. Loaded only by that page, on top of nacravo.css.\n"
        " * The reviews-carousel styles were intentionally dropped with the\n"
        " * unverified testimonials they belonged to.\n"
        " */\n\n"
        + main_block
        + "\n\n"
        + final_block
        + EXTRA
    )

    dest = ROOT / "assets" / "nacravo-ac.css"
    dest.write_text(out, encoding="utf-8", newline="\n")
    print(f"assets/nacravo-ac.css written — {out.count(chr(10))} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
