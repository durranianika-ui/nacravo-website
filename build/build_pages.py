"""Render the Nacravo service landing pages and the /services hub.

Usage:  ./.venv/Scripts/python.exe build/build_pages.py

Content lives in content_a/b/c.py, the shared shell in template.py. Re-running
regenerates every page, so the header, footer, schema and tracking contract stay
identical across the site. Hand edits to the generated .html files are lost on
the next run — change the content module instead.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import content_a
import content_b
import content_c
import links
import media
import template as T

ROOT = pathlib.Path(__file__).resolve().parent.parent

PAGES = {}
for mod in (content_a, content_b, content_c):
    PAGES.update(mod.PAGES)


# Media comes from build/media.py, where every image is described by what it
# actually shows (verified by opening it, not guessed from the filename).
COMPOSITE_NOTE = ("Each image below is a single before-and-after comparison. "
                  "Every visit ends with a photo report sent to you, so the result is "
                  "documented rather than described.")
WORK_NOTE = ("Our own employed technicians, on real Nacravo jobs. Every visit ends with a "
             "photo report sent to you.")

for slug, (heading, images) in media.GALLERIES.items():
    if slug not in PAGES:
        continue
    PAGES[slug]["gallery_heading"] = heading
    PAGES[slug]["gallery_note"] = COMPOSITE_NOTE
    PAGES[slug]["gallery_items"] = [
        (f"{stem}-1080.jpg", f"{stem}-600.jpg", tag, alt) for stem, tag, alt in images
    ]

for slug, (heading, images) in media.WORK_GALLERIES.items():
    PAGES[slug]["gallery_heading"] = heading
    PAGES[slug]["gallery_note"] = WORK_NOTE
    PAGES[slug]["gallery_items"] = [
        (big, small, tag, alt) for big, small, tag, alt in images
    ]

for slug, reason in media.GALLERY_GAPS.items():
    PAGES[slug]["gallery_gap"] = reason

# Hero image beside the form, and the matching social preview image.
for slug, hero in media.HEROES.items():
    if slug in PAGES:
        PAGES[slug]["hero_image"] = hero
        PAGES[slug]["og_image"] = hero[0]

# Contextual in-body links, and named Dubai communities on general-service pages.
# The AC page is handled in build_ac.py and gets contextual links but NOT the
# community list — its coverage is scoped to three districts.
for slug, sentence in links.CONTEXTUAL.items():
    if slug in PAGES:
        PAGES[slug]["contextual"] = sentence

for slug in PAGES:
    PAGES[slug]["communities"] = links.COMMUNITIES
    PAGES[slug]["local_intro"] = links.LOCAL_INTRO
    PAGES[slug]["local_note"] = links.LOCAL_NOTE


# ---------------------------------------------------------------- services hub
def render_services_hub():
    """Grouped hub linking to every landing page — keeps each page within two
    clicks of the homepage and gives the nav dropdown a canonical counterpart."""
    hub = {
        "url": "/services",
        "breadcrumb": "All Services",
        # plain text — render_head escapes it, so no pre-escaped entities here
        "title": "Cleaning & Maintenance Services in Dubai | Nacravo",
        "meta_description": "Every Nacravo service in one place — home, deep, move-in/out, holiday home and office cleaning, plus AC, handyman, pest control and annual maintenance in Dubai.",
        "og_title": "Nacravo Services — Cleaning & Maintenance in Dubai",
        "og_description": "Cleaning and maintenance for Dubai homes, holiday homes and offices, delivered by one accountable team.",
        "og_image": "svc-cleaning2-lg.jpg",
        "h1": "Cleaning and Maintenance Services in Dubai",
        "service_value": "General enquiry",
        "wa_text": "Hello Nacravo, I'd like a quote for a service in Dubai.",
        # no hero form on the hub — send quote CTAs to the homepage enquiry form
        "quote_href": "/#contact",
    }

    def cards(items):
        out = []
        for title, url, desc in items:
            out.append(f"""
        <a class="rel-card" href="{url}">
          <h3>{title}</h3>
          <p>{T.esc(desc)}</p>
          <span class="rel-go">View service →</span>
        </a>""")
        return "".join(out)

    cleaning = [
        ("Home Cleaning", "/home-cleaning", "Regular, weekly, monthly and hourly cleaning for apartments, townhouses and villas."),
        ("Deep Cleaning", "/deep-cleaning", "Top-to-bottom cleaning for kitchens, bathrooms, whole homes and post-construction handovers."),
        ("Move In / Move Out", "/move-in-out-cleaning", "End-of-tenancy and empty-property cleaning built around handover inspections."),
        ("Holiday Home Cleaning", "/holiday-home-cleaning", "Airbnb and holiday home turnovers with linen, restocking and a guest-ready check."),
        ("Office &amp; Commercial", "/office-commercial-cleaning", "Daily contracts, deep cleans, carpet shampoo and post-event cleaning for workplaces."),
        ("Specialized Cleaning", "/specialized-cleaning", "Sofa, carpet, mattress, curtain and interior window cleaning by trained technicians."),
        ("Pest Control", "/pest-control", "Cockroach, bed bug, ant and rodent treatments for homes and commercial premises."),
    ]
    maintenance = [
        ("AC Services", "/ac-service-dubai", "Servicing, chemical wash, duct cleaning, repair and installation for split and window units."),
        ("Handyman Services", "/handyman-services", "Plumbing, electrical, painting, mounting, carpentry and fixture work in one visit."),
        ("Annual Maintenance", "/annual-maintenance", "Apartment and villa AMC with scheduled preventive visits and priority callout."),
    ]

    head = T.render_head({
        **hub,
        "service_schema_name": "Cleaning and Maintenance Services",
        "area_served_schema": ["Dubai"],
        "sections": [{"title": t} for t, _, _ in cleaning + maintenance],
        "faq": [
            ("Which services can Nacravo cover in one booking?",
             "Cleaning and maintenance are delivered by the same company, so a single WhatsApp thread can cover a deep clean, an AC service and a handyman job. You get one fixed quote covering the work and one point of contact rather than coordinating separate contractors."),
            ("Do you serve the whole of Dubai?",
             "General cleaning and maintenance services are available across Dubai, subject to availability. Our premium AC servicing team currently focuses on Downtown Dubai, Business Bay and DIFC so scheduling stays tight and quality stays consistent in those districts."),
            ("How do I get a price?",
             "Send your details through any quote form on the site, message us on WhatsApp or call. We confirm a fixed price before any work begins, so the amount you approve is the amount you pay."),
        ],
    })

    header = T.render_header(hub)
    wa = T.wa_link(hub["wa_text"])

    body = f"""
<main id="main">
<section class="lp-hero" style="padding-bottom:24px">
  <div class="wrap">
    <span class="eyebrow">All services · Dubai</span>
    <h1>{hub['h1']}</h1>
    <p class="lead" style="max-width:640px">One accountable team for cleaning and maintenance. Every service below is delivered by technicians employed by Nacravo, with materials included, a fixed price agreed before work starts and a photo report when the job is done.</p>
    <div class="lp-hero-cta" style="margin-top:18px">
      <a href="{wa}" target="_blank" rel="noopener" class="btn btn-wa" data-track="booking" data-track-label="Services hub: WhatsApp">{T.WA_ICON.format(s=18)} WhatsApp us</a>
      <a href="tel:{T.PHONE_TEL}" class="btn btn-ghost">{T.PHONE_ICON} Call now</a>
      <a href="/#contact" class="btn btn-ghost" data-track="quote" data-track-label="Services hub: Get a quote">Get a quote</a>
    </div>
  </div>
</section>

<section id="cleaning" style="padding-top:24px">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Cleaning</span>
      <h2>Cleaning services</h2>
      <p>From a weekly tidy to a full tenancy handover clean, delivered to the same checklist every visit.</p>
    </div>
    <div class="rel-grid">{cards(cleaning)}
    </div>
  </div>
</section>

<section id="maintenance" style="background:var(--sand)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Maintenance</span>
      <h2>Maintenance services</h2>
      <p>Fixed quotes, parts shown before fitting, and the same technicians you have already met.</p>
    </div>
    <div class="rel-grid">{cards(maintenance)}
    </div>
  </div>
</section>

<section id="choosing" style="border-top:1px solid var(--line)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Choosing</span>
      <h2>Which service do you actually need?</h2>
      <p>The names overlap more than they should across this industry. Here is the plain version.</p>
    </div>
    <div class="anchor-grid">
      <div class="anchor-card">
        <h3>Cleaning that repeats vs cleaning that resets</h3>
        <p><a href="/home-cleaning">Home cleaning</a> is the recurring visit that keeps a property in the state it is already in. <a href="/deep-cleaning">Deep cleaning</a> is a one-off reset that goes after built-up grease, limescale and soiling a routine visit does not touch. If a property has been empty, neglected or recently built, start with the deep clean and move to regular visits afterwards.</p>
      </div>
      <div class="anchor-card">
        <h3>Moving out, or handing over to a guest</h3>
        <p><a href="/move-in-out-cleaning">Move in / move out cleaning</a> is built around a landlord's handover inspection, so it covers the inside of appliances, cupboards and balconies that inspectors check. <a href="/holiday-home-cleaning">Holiday home cleaning</a> is a faster repeating turnover between guests, with linen and consumables handled as part of the visit.</p>
      </div>
      <div class="anchor-card">
        <h3>One job, or a contract</h3>
        <p>Book <a href="/handyman-services">handyman services</a> when you have a specific repair, and <a href="/annual-maintenance">annual maintenance</a> when you are calling someone every few months anyway. A contract schedules preventive visits and gives contract properties priority ordering, which is usually cheaper than repeated callouts.</p>
      </div>
      <div class="anchor-card">
        <h3>Furniture, or the whole property</h3>
        <p><a href="/specialized-cleaning">Specialized cleaning</a> covers sofas, carpets, mattresses and curtains on their own, using extraction rather than surface cleaning. If the whole property needs attention, it is usually better value as an add-on to a <a href="/deep-cleaning">deep clean</a> than as a separate visit.</p>
      </div>
    </div>
  </div>
</section>

{T.render_cta_band(hub, "Not sure which service you need?", "Describe the job on WhatsApp and we will tell you what it needs and what it costs.", "quote")}

<section id="faq">
  <div class="wrap">
    <div class="sec-head center">
      <span class="eyebrow">FAQ</span>
      <h2>Common questions</h2>
    </div>
    <div class="faq-list">
      <details><summary>Which services can Nacravo cover in one booking?<span class="pl" aria-hidden="true">+</span></summary><p>Cleaning and maintenance are delivered by the same company, so a single WhatsApp thread can cover a deep clean, an AC service and a handyman job. You get one fixed quote covering the work and one point of contact rather than coordinating separate contractors.</p></details>
      <details><summary>Do you serve the whole of Dubai?<span class="pl" aria-hidden="true">+</span></summary><p>General cleaning and maintenance services are available across Dubai, subject to availability. Our premium AC servicing team currently focuses on Downtown Dubai, Business Bay and DIFC so scheduling stays tight and quality stays consistent in those districts.</p></details>
      <details><summary>How do I get a price?<span class="pl" aria-hidden="true">+</span></summary><p>Send your details through any quote form on the site, message us on WhatsApp or call. We confirm a fixed price before any work begins, so the amount you approve is the amount you pay.</p></details>
    </div>
  </div>
</section>
"""

    return head + header + body + T.render_footer(hub)


def main():
    written = []

    for slug, page in sorted(PAGES.items()):
        html = T.render_page(page)
        path = ROOT / f"{slug}.html"
        path.write_text(html, encoding="utf-8", newline="\n")
        written.append((path.name, len(html)))

    hub = ROOT / "services.html"
    hub_html = render_services_hub()
    hub.write_text(hub_html, encoding="utf-8", newline="\n")
    written.append((hub.name, len(hub_html)))

    for name, size in written:
        print(f"  {size/1024:6.1f} KB  {name}")
    print(f"\n{len(written)} pages written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
