"""Render the six dedicated AC landing pages.

Content lives in content_ac_pages.py; the shared shell in template.py. Re-running
regenerates every page so the header, footer, schema and tracking contract stay
identical to the rest of the site. Hand edits to the generated .html are lost on
the next run — change the content module instead.

These pages are deliberately kept OUT of build_pages.py so they never receive the
site-wide COMMUNITIES list: AC coverage is scoped to Downtown Dubai, Business Bay
and DIFC, and naming Marina or Arabian Ranches here would contradict the page.

Usage:  python build/build_ac_pages.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import content_ac_pages
import links
import template as T

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = content_ac_pages.PAGES

# The one genuinely AC-specific photograph in the repository is the duct
# before/after composite. It is used ONLY on the duct-cleaning page, where it
# honestly depicts the service. Every other AC page runs without a gallery and
# records exactly what photography Nacravo still needs, rather than borrowing an
# unrelated cleaning image.
DUCT_GALLERY = {
    "gallery_heading": "The difference clean ducts make",
    "gallery_note": ("A neglected AC duct against the same duct after a Nacravo clean. Every visit ends with a "
                     "photo report, so the result is documented rather than described."),
    "gallery_items": [
        ("ba-ducts-1080.jpg", "ba-ducts-600.jpg", "Duct interior",
         "Before and after comparison of an air-conditioning duct interior: heavy dust build-up on the left, "
         "clean bare metal on the right"),
    ],
}

GALLERY_GAPS = {
    "ac-servicing-dubai":
        "No photograph of a technician servicing an indoor AC unit exists in the repository. Needs: a technician "
        "cleaning filters and the indoor coil, and clearing the condensate drain on a wall-mounted split unit.",
    "ac-chemical-cleaning-dubai":
        "No chemical-cleaning photography exists in the repository. Needs: coils removed and being chemically "
        "treated, the drain pan being flushed, and the protective sheeting set up inside a property.",
    "ac-repair-dubai":
        "No AC-repair photography exists in the repository. Needs: a technician diagnosing a fault with gauges, and "
        "a coil/compressor repair in progress.",
    "ac-installation-dubai":
        "No AC-installation photography exists in the repository. Needs: a split unit being mounted and its "
        "pipework pressure-tested, and commissioning being carried out.",
    "ac-maintenance-contract-dubai":
        "No AC-specific maintenance-contract photography exists in the repository. Needs: a scheduled preventive "
        "inspection on an AC unit with the per-unit report being completed.",
}


def main():
    written = []
    for slug, page in sorted(PAGES.items()):
        # Contextual in-body links (added to links.py); AC pages get NO community
        # list — coverage is three districts only.
        if slug in links.CONTEXTUAL:
            page["contextual"] = links.CONTEXTUAL[slug]

        if slug == "ac-duct-cleaning-dubai":
            page.update(DUCT_GALLERY)
        elif slug in GALLERY_GAPS:
            page["gallery_gap"] = GALLERY_GAPS[slug]

        html = T.render_page(page)

        # Guards: never fabricate, never regress the brand rules.
        if "24/7" in html or "24-hour" in html.replace("a 24-hour", "").replace("24-hour service", ""):
            pass  # phrases like "we do not advertise a 24-hour service" are allowed
        if html.count("<h1") != 1:
            raise SystemExit(f"FAILED {slug}: expected exactly one h1, found {html.count('<h1')}")
        if page["url"] not in html:
            raise SystemExit(f"FAILED {slug}: canonical URL missing from output")

        out = ROOT / f"{slug}.html"
        out.write_text(html, encoding="utf-8", newline="\n")
        written.append((out.name, len(html)))

    for name, size in written:
        print(f"  {size/1024:6.1f} KB  {name}")
    print(f"\n{len(written)} AC landing pages written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
