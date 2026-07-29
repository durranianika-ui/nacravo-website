"""Rebuild /ac-service-dubai as the AC Services HUB.

The URL and canonical are unchanged, and it still captures broad "AC services
Dubai" intent — but it no longer tries to be the Google Ads landing page for
every individual AC service. That job now belongs to the six dedicated pages
(build_ac_pages.py). This page's job is to explain Nacravo's overall AC
capability, help a visitor identify the right service, and route them to it.

Structure (deliberately much shorter than the previous page):
  hero + lead form
  -> service selection cards (link to the six dedicated pages)
  -> "Which AC service do I need?" decision guide
  -> side-by-side comparison of servicing / chemical cleaning / duct cleaning / repair
  -> why-Nacravo trust table + standards
  -> brief six-step process
  -> pricing explanation + coverage
  -> condensed GENERAL AC FAQs (service-specific FAQs live on the dedicated pages)
  -> brands + related services

Removed vs the old page: the ten deep sub-service anchor sections, the problems
grid, the standalone before/after (now owned by the duct-cleaning page), the deep
chemical-wash block (owned by the chemical-cleaning page) and the property-types
block. Preserved: the honest trust section, the comparison table, the process and
the brand list. The unverified testimonials and the fake before/after slider stay
gone, guarded below.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import ac_blocks
import links
import template as T
from content_ac import PAGE

ROOT = pathlib.Path(__file__).resolve().parent.parent

PAGE["og_image"] = "ba-ducts-1080.jpg"
PAGE["contextual"] = links.CONTEXTUAL["ac-service-dubai"]

# The hub routes rather than anchors down its own body, so the hero jump-nav and
# the sub-service form options point at the hub's own sections and stay short.
PAGE["jump_links"] = [
    ("Choose a service", "choose"),
    ("Which do I need?", "which"),
    ("Compare", "compare"),
    ("Coverage", "areas"),
]
# A hub-level enquiry: the form's specific-service select offers the six services,
# so a broad visitor can still pick one without leaving the page.
PAGE["subservices"] = {
    "servicing": "AC Servicing",
    "chemical-cleaning": "AC Chemical Cleaning",
    "duct-cleaning": "AC Duct Cleaning",
    "repair": "AC Repair",
    "installation": "AC Installation",
    "maintenance-contract": "AC Maintenance Contract",
}

# Condensed, GENERAL FAQs only. Service-specific questions now live on the six
# dedicated pages, so the hub does not compete with them for those long-tail
# queries. Schema FAQ is generated from this same list, so it matches what is
# visible on the page.
_faq = dict(PAGE["faq"])
GENERAL_FAQ_QUESTIONS = [
    "How often should AC be serviced in Dubai?",
    "What is the difference between AC maintenance and a chemical wash?",
    "How long does an AC service take?",
    "Which areas do you cover for AC service?",
    "Do you service apartments and villas?",
    "What AC brands do you service?",
    "Do you offer same-day AC service?",
    "Is your AC pricing transparent?",
    "Are your AC technicians licensed and insured?",
    "How do I book an AC service?",
]
PAGE["faq"] = [(q, _faq[q]) for q in GENERAL_FAQ_QUESTIONS if q in _faq]
PAGE["faq_heading"] = "General AC questions, answered"

# For schema hasOfferCatalog, list the six real services rather than the old ten
# overlapping anchors.
PAGE["sections"] = [
    {"title": "AC Servicing"}, {"title": "AC Chemical Cleaning"},
    {"title": "AC Duct Cleaning"}, {"title": "AC Repair"},
    {"title": "AC Installation"}, {"title": "AC Maintenance Contract"},
]

# The related grid points at the specialist AC pages first.
PAGE["related"] = [
    ("AC Servicing", "/ac-servicing-dubai",
     "Routine maintenance that restores cooling, airflow and drainage."),
    ("AC Chemical Cleaning", "/ac-chemical-cleaning-dubai",
     "Deep coil restoration for smells and weak cooling a service won't fix."),
    ("AC Repair", "/ac-repair-dubai",
     "Leaks, no cooling, noise and faults diagnosed and priced before work."),
    ("AC Maintenance Contracts", "/ac-maintenance-contract-dubai",
     "Scheduled preventive cover for homes, landlords and businesses."),
]


def _icon(path):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + "</svg>")


# ------------------------------------------------------------- service selection
_SERVICES = [
    ("/ac-servicing-dubai", "AC Servicing",
     "Routine maintenance for weak cooling, poor airflow, dirty filters and blocked drainage.",
     '<path d="M12 20h9M3 20l1.5-4.5L15 5l4 4L8.5 19.5z"/>'),
    ("/ac-chemical-cleaning-dubai", "AC Chemical Cleaning",
     "Deep coil restoration for persistent smells, mould and cooling a service can't fix.",
     '<path d="M7 21c-2 0-3-1.5-3-3.5 0-2 3-6.5 3-6.5s3 4.5 3 6.5S9 21 7 21z"/><path d="M14 4l6 6M9.5 8.5 15 3l6 6-5.5 5.5z"/>'),
    ("/ac-duct-cleaning-dubai", "AC Duct Cleaning",
     "Accessible duct and grille cleaning for dust blowing from the vents and weak airflow.",
     '<circle cx="6" cy="8" r="1"/><circle cx="12" cy="6" r="1"/><circle cx="18" cy="9" r="1"/><circle cx="9" cy="13" r="1"/><circle cx="16" cy="15" r="1"/><circle cx="7" cy="18" r="1"/>'),
    ("/ac-repair-dubai", "AC Repair",
     "Leaks, no cooling, tripping breakers, noise and faults — diagnosed and priced first.",
     '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.3 2.3-2-2z"/>'),
    ("/ac-installation-dubai", "AC Installation",
     "Split and window units sized, fitted, pressure-tested and commissioned properly.",
     '<path d="M3 21h18M6 21V7l7-4v18M13 21V9l5 3v9"/>'),
    ("/ac-maintenance-contract-dubai", "AC Maintenance Contracts",
     "Scheduled preventive cover with per-unit records and photo reports across the year.",
     '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M8 14l2 2 4-4"/>'),
]


def service_selection():
    cards = "".join(
        f"""
      <a class="ac-card" href="{url}">
        <div class="ac-ic">{_icon(icon)}</div>
        <h3>{T.esc(title)}</h3>
        <p>{T.esc(desc)}</p>
        <span class="ac-go">View service →</span>
      </a>""" for url, title, desc, icon in _SERVICES)
    return f"""
<section id="choose">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Choose your AC service</span>
      <h2>Six specialist AC services, one accountable team</h2>
      <p>Pick the service that matches your problem — each has its own page with the full detail, pricing approach and FAQs.</p>
    </div>
    <div class="ac-grid">{cards}
    </div>
  </div>
</section>
"""


# --------------------------------------------------------------- decision guide
_DECISION = [
    ("Cooling has slowly weakened",
     'Usually dust on the filters, coils or the outdoor condenser. Start with <a href="/ac-servicing-dubai">AC servicing</a> — it restores most units.'),
    ("Bad smell, or weak straight after a service",
     'The coils are contaminated. That is an <a href="/ac-chemical-cleaning-dubai">AC chemical cleaning</a>, where the coils are removed and deep-treated.'),
    ("Dust blowing from the vents",
     'Debris in the accessible ductwork. Book an <a href="/ac-duct-cleaning-dubai">AC duct cleaning</a> assessment — we inspect before recommending work.'),
    ("Leaking, tripping the breaker or not cooling",
     'An active fault, not routine wear. That is an <a href="/ac-repair-dubai">AC repair</a> — diagnosed and priced before any work starts.'),
    ("Fitting a new unit or replacing an old one",
     'An <a href="/ac-installation-dubai">AC installation</a>: correctly sized, drainage set to a proper fall, pipework pressure-tested and commissioned.'),
    ("Tired of surprise breakdowns",
     'Put cooling on a schedule with an <a href="/ac-maintenance-contract-dubai">AC maintenance contract</a> — planned visits and per-unit records.'),
]


def decision_guide():
    cards = "".join(
        f"""
      <div class="anchor-card">
        <h3>{T.esc(symptom)}</h3>
        <p>{answer}</p>
      </div>""" for symptom, answer in _DECISION)
    return f"""
<section id="which" style="background:var(--sand)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Not sure which you need?</span>
      <h2>Which AC service do I need?</h2>
      <p>Match the symptom to the service. If you are still unsure, send a photo on WhatsApp and we will tell you honestly.</p>
    </div>
    <div class="anchor-grid">{cards}
    </div>
  </div>
</section>
"""


# ------------------------------------------------------------------- comparison
def comparison_table():
    rows = [
        ("AC Servicing", "/ac-servicing-dubai", "Routine care; weak cooling from dust",
         "Cleans filters, coils and drain; checks gas, thermostat and airflow", "Every 3-4 months"),
        ("AC Chemical Cleaning", "/ac-chemical-cleaning-dubai", "Smells, mould, weak cooling after a service",
         "Removes and deep-treats the coils; flushes blower and drain pan", "Every 8-12 months"),
        ("AC Duct Cleaning", "/ac-duct-cleaning-dubai", "Dust from the vents; restricted airflow",
         "Cleans accessible ducts and grilles after inspection", "As needed / on inspection"),
        ("AC Repair", "/ac-repair-dubai", "An active fault — leak, no cooling, noise",
         "Diagnoses the cause and repairs it, parts approved first", "When a fault occurs"),
    ]
    body = "".join(
        f"""
        <tr>
          <th scope="row"><a href="{url}">{T.esc(name)}</a></th>
          <td>{T.esc(best)}</td>
          <td>{T.esc(does)}</td>
          <td>{T.esc(freq)}</td>
        </tr>""" for name, url, best, does, freq in rows)
    return f"""
<section id="compare" style="border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#fff">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Compare</span>
      <h2>Servicing, chemical cleaning, duct cleaning or repair?</h2>
      <p>The names overlap across this industry. Here is the plain version so you book the right one.</p>
    </div>
    <div class="svc-compare-wrap">
      <table class="svc-compare">
        <thead>
          <tr><th scope="col">Service</th><th scope="col">Best for</th><th scope="col">What it does</th><th scope="col">Typical frequency</th></tr>
        </thead>
        <tbody>{body}
        </tbody>
      </table>
    </div>
  </div>
</section>
"""


# Reused from the previous page. States only what can be substantiated — no
# customer quotes, ratings or review counts.
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


def main():
    head = T.render_head(PAGE)
    head = head.replace(
        '<link rel="stylesheet" href="/assets/nacravo.css">',
        '<link rel="stylesheet" href="/assets/nacravo.css">\n'
        '<link rel="stylesheet" href="/assets/nacravo-ac.css">',
    )

    body = (
        T.render_header(PAGE)
        + T.render_hero(PAGE)
        + service_selection()
        + decision_guide()
        + comparison_table()
        + ac_blocks.COMPARISON
        + TRUST_SECTION
        + ac_blocks.PROCESS
        + T.render_pricing(PAGE)
        + T.render_areas(PAGE)
        + ac_blocks.BRANDS
        + T.render_faq(PAGE)
        + T.render_related(PAGE)
        + T.render_cta_band(PAGE, PAGE["band2_heading"], PAGE["band2_body"], "book")
    )

    footer = T.render_footer(PAGE)
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
    for banned in ("bawRange", "bawBefore", "bawHandle", "Drag the slider"):
        if banned in html:
            raise SystemExit(f"FAILED: simulated before/after slider markup '{banned}' is present")
    if html.count("<h1") != 1:
        raise SystemExit(f"FAILED: expected exactly one h1, found {html.count('<h1')}")
    # the hub must link to every dedicated AC page
    for slug in ("ac-servicing-dubai", "ac-chemical-cleaning-dubai", "ac-duct-cleaning-dubai",
                 "ac-repair-dubai", "ac-installation-dubai", "ac-maintenance-contract-dubai"):
        if f"/{slug}" not in html:
            raise SystemExit(f"FAILED: hub does not link to /{slug}")

    out = ROOT / "ac-service-dubai.html"
    out.write_text(html, encoding="utf-8", newline="\n")
    print(f"ac-service-dubai.html rebuilt as hub — {len(html)/1024:.1f} KB")
    print(f"  links to all 6 dedicated AC pages")
    print(f"  {len(PAGE['faq'])} general FAQ entries")
    print("  testimonials removed, service-area claims corrected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
