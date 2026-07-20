"""Rebuild /ac-service-dubai as the consolidated AC landing page.

The URL and canonical are unchanged. The page is re-composed from the shared
template so it uses ONE tracking layer (assets/nacravo.js) instead of its own
inline copy — keeping its inline tracker while adding the shared one would have
fired every event twice.

Preserved verbatim from the old page: the comparison table, problems grid,
before/after slider, chemical-wash comparison, six-step process, property types
and brands, plus all of its FAQ content.

Removed: the five unverified testimonials and the carousel that carried them,
replaced by a trust section that makes no customer-quote claims.

Corrected: service-area statements, which previously advertised communities
outside the AC team's current coverage.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import ac_blocks
import links
import media
import template as T
from content_ac import PAGE

PAGE["hero_image"] = media.HEROES["ac-service-dubai"]
# Contextual links yes; community list NO — AC coverage is three districts only.
PAGE["contextual"] = links.CONTEXTUAL["ac-service-dubai"]
PAGE["og_image"] = PAGE["hero_image"][0]

# No separate gallery on this page: the before/after section below already shows
# the duct comparison, and repeating the same image twice would be padding.

ROOT = pathlib.Path(__file__).resolve().parent.parent

# --- service-area corrections applied to the preserved blocks -----------------
# The old copy promoted Marina, JLT, Dubai Hills, JVC and Motor City. AC
# servicing is currently focused on Downtown Dubai, Business Bay and DIFC, so
# these claims are corrected rather than left to contradict the rest of the site.
AREA_FIXES = [
    ("Split and FCU units in high-rises across Business Bay, Marina, JLT and Downtown.",
     "Split and fan-coil units in high-rise towers across Downtown Dubai, Business Bay and DIFC."),
    ("Efficient servicing for community townhouses in Dubai Hills, JVC and Motor City.",
     "Efficient servicing for townhouses and low-rise homes inside our current coverage area."),
    ("Low-disruption servicing scheduled around your working hours in DIFC and beyond.",
     "Low-disruption servicing scheduled around your working hours in DIFC and Business Bay."),
]

# Replaces the removed reviews carousel. States only what we can substantiate.
TRUST_SECTION = """
<section id="standards" style="background:var(--sand)">
  <div class="wrap">
    <div class="sec-head center">
      <span class="eyebrow">Our standards</span>
      <h2>How we keep AC work consistent</h2>
      <p style="margin:0 auto">Every visit follows the same checklist, carried out by technicians we employ directly.</p>
    </div>
    <div class="anchor-grid">
      <div class="anchor-card">
        <h3>Employed, trained technicians</h3>
        <p>Every technician is on the Nacravo payroll, background-checked, uniformed and trained to one checklist. We do not dispatch jobs to a marketplace, so the standard does not change between visits.</p>
      </div>
      <div class="anchor-card">
        <h3>Documented, not just described</h3>
        <p>Each visit ends with a before-and-after photo report covering the coils, drain and unit condition. If something is not right afterwards, we can pull the report and put it right.</p>
      </div>
      <div class="anchor-card">
        <h3>Priced before the work, not after</h3>
        <p>You approve a fixed price before a technician starts. Any part that needs replacing is shown to you before it is fitted, and any urgency surcharge appears in the quote rather than on the invoice.</p>
      </div>
      <div class="anchor-card">
        <h3>Focused coverage</h3>
        <p>Our AC team concentrates on Downtown Dubai, Business Bay and DIFC. Staying inside a tight area is how we keep arrival windows realistic and quality consistent across every job.</p>
      </div>
    </div>
  </div>
</section>
"""

# The original page carried a drag-to-compare slider. It has been removed, and
# with it all of this page's remaining JavaScript.
#
# Why: the slider loaded ba-ducts-1080.jpg as BOTH its "before" and "after"
# layer and simulated the "before" state with a CSS grayscale/brightness filter.
# That file is already a single side-by-side Before | After composite with those
# labels printed into the image, so the widget stacked its own duplicate labels
# on top, and dragging it revealed the composite's own "Before" half beneath an
# "After" tag. Beyond being broken, presenting a colour-filtered copy of a photo
# as a genuine "before" image misrepresents the evidence.
#
# The composite is now shown as-is, which is what it was made for.
SLIDER_JS = ""

BEFORE_AFTER = """
<section id="before-after" style="background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Before vs after</span>
      <h2>The difference a proper service makes</h2>
      <p>A neglected AC duct against the same duct after a Nacravo clean. Clean coils and ducts mean stronger cooling and cleaner air.</p>
    </div>
    <div class="ba-wrap">
      <figure class="ba-static">
        <img src="images/ba-ducts-1080.jpg" srcset="images/ba-ducts-600.jpg 600w, images/ba-ducts-1080.jpg 1080w"
             sizes="(max-width:760px) 92vw, 560px"
             alt="Before and after comparison of an air conditioning duct interior: heavy dust build-up on the left, clean bare metal on the right"
             width="1080" height="720" loading="lazy" decoding="async">
        <figcaption>Duct interior before and after a Nacravo clean.</figcaption>
      </figure>
      <div class="ba-side">
        <div class="benefit"><div class="bi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></svg></div><div><h3>Better cooling</h3><p>Clean coils exchange heat efficiently, so rooms reach temperature faster.</p></div></div>
        <div class="benefit"><div class="bi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12c2-2 5 2 7 0s5 2 7 0M5 8c2-2 5 2 7 0s5 2 7 0"/></svg></div><div><h3>Cleaner air</h3><p>Removing mould and bacteria from coils improves the air your family breathes.</p></div></div>
        <div class="benefit"><div class="bi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7z"/></svg></div><div><h3>Lower energy consumption</h3><p>A system that isn't fighting dirt draws less power to hold the same temperature.</p></div></div>
        <div class="benefit"><div class="bi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 2"/></svg></div><div><h3>Longer equipment life</h3><p>Regular servicing prevents strain and premature compressor failure.</p></div></div>
        <div class="benefit"><div class="bi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h11a3 3 0 1 0-3-3"/><path d="M3 12h15a3 3 0 1 1-3 3"/></svg></div><div><h3>Improved airflow</h3><p>Unblocked filters and vents deliver even, quiet airflow to every room.</p></div></div>
      </div>
    </div>
  </div>
</section>
"""


def apply_area_fixes(html):
    for old, new in AREA_FIXES:
        if old not in html:
            raise SystemExit(f"FAILED: expected phrase not found for correction:\n  {old}")
        html = html.replace(old, new)
    return html


def main():
    property_types = apply_area_fixes(ac_blocks.PROPERTY_TYPES)

    head = T.render_head(PAGE)
    # page-scoped stylesheet for the preserved AC-only components
    head = head.replace(
        '<link rel="stylesheet" href="/assets/nacravo.css">',
        '<link rel="stylesheet" href="/assets/nacravo.css">\n'
        '<link rel="stylesheet" href="/assets/nacravo-ac.css">',
    )

    body = (
        T.render_header(PAGE)
        + T.render_hero(PAGE)
        + T.render_sections(PAGE)
        # alias anchor so /ac-service-dubai#maintenance resolves as well
        + '<span id="maintenance" aria-hidden="true"></span>\n'
        + T.render_cta_band(PAGE, PAGE["band1_heading"], PAGE["band1_body"], "quote")
        + ac_blocks.COMPARISON
        + ac_blocks.PROBLEMS
        + BEFORE_AFTER
        + ac_blocks.CHEMICAL
        + ac_blocks.PROCESS
        + T.render_pricing(PAGE)
        + T.render_areas(PAGE)
        + property_types
        + ac_blocks.BRANDS
        + TRUST_SECTION
        + T.render_faq(PAGE)
        + T.render_related(PAGE)
        + T.render_cta_band(PAGE, PAGE["band2_heading"], PAGE["band2_body"], "book")
    )

    footer = T.render_footer(PAGE).replace("</body>", SLIDER_JS + "</body>")

    html = head + body + footer

    # --- guards -------------------------------------------------------------
    for name in ("Sara A.", "Rahul M.", "Layla K.", "Omar T.", "Fatima H."):
        if name in html:
            raise SystemExit(f"FAILED: removed testimonial name '{name}' still present")
    for banned in ("rev-card", "rev-track", "blockquote", "What Dubai residents say"):
        if banned in html:
            raise SystemExit(f"FAILED: reviews markup '{banned}' still present")
    if "Dubai-wide coverage" in html:
        raise SystemExit("FAILED: page still claims Dubai-wide AC coverage")
    # the fake before/after slider must not come back
    for banned in ("bawRange", "bawBefore", "bawHandle", "Drag the slider"):
        if banned in html:
            raise SystemExit(f"FAILED: simulated before/after slider markup '{banned}' is present")
    if html.count("<h1") != 1:
        raise SystemExit(f"FAILED: expected exactly one h1, found {html.count('<h1')}")

    out = ROOT / "ac-service-dubai.html"
    out.write_text(html, encoding="utf-8", newline="\n")
    print(f"ac-service-dubai.html rebuilt — {len(html)/1024:.1f} KB")
    print(f"  {len(PAGE['sections'])} sub-service anchor sections")
    print(f"  {len(PAGE['faq'])} FAQ entries preserved")
    print("  testimonials removed, service-area claims corrected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
