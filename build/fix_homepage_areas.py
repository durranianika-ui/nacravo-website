"""Apply the agreed service-area policy to index.html.

Policy:
  * General cleaning and maintenance — available across Dubai, subject to
    availability. The homepage must not imply every service is restricted to
    three districts.
  * AC servicing — currently focused on Downtown Dubai, Business Bay and DIFC,
    matching the Google Ads targeting for that service.

One-shot script; every replacement is asserted so a silent no-op is impossible.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "index.html"

AREA_LINE = ("General cleaning and maintenance across Dubai, subject to availability. "
             "Premium AC servicing currently focuses on Downtown Dubai, Business Bay and DIFC.")

REPLACEMENTS = [
    # --- head metadata ---
    ('content="Nacravo — premium home cleaning and maintenance in Downtown Dubai, Business Bay and DIFC. One accountable, vetted team. Every job documented with before-and-after photos. Book on WhatsApp."',
     'content="Nacravo — cleaning and maintenance across Dubai, with premium AC servicing in Downtown, Business Bay and DIFC. One vetted team. Every job photo-documented."'),

    ('content="One accountable team for cleaning and maintenance in Downtown Dubai, Business Bay and DIFC. Every job documented with photos. Book on WhatsApp."',
     'content="One accountable team for cleaning and maintenance across Dubai, with AC servicing focused on Downtown, Business Bay and DIFC. Book on WhatsApp."'),

    # --- LocalBusiness schema ---
    ('"description": "Premium home cleaning and maintenance for Downtown Dubai, Business Bay and DIFC.",',
     '"description": "Cleaning and maintenance across Dubai. Premium AC servicing currently focused on Downtown Dubai, Business Bay and DIFC.",'),

    ('"areaServed": ["Downtown Dubai", "Business Bay", "DIFC"],',
     '"areaServed": ["Dubai"],'),

    # --- FAQ schema ---
    ('{"@type":"Question","name":"Which areas do you cover?","acceptedAnswer":{"@type":"Answer","text":"Downtown Dubai, Business Bay and DIFC. We stay focused on these districts on purpose — it\'s how we keep arrival times tight and quality consistent."}}',
     '{"@type":"Question","name":"Which areas do you cover?","acceptedAnswer":{"@type":"Answer","text":"' + AREA_LINE + ' Concentrating our AC team on those districts is how we keep arrival times tight and quality consistent."}}'),

    # --- hero ---
    ('<span class="eyebrow">Cleaning &amp; maintenance · Downtown · Business Bay · DIFC</span>',
     '<span class="eyebrow">Cleaning &amp; maintenance · Across Dubai</span>'),

    ('<span class="d-only">Premium home cleaning and maintenance for Dubai\'s professional core. One accountable team — vetted, trained, and dispatched by us. Every job documented with before-and-after photos.</span>',
     '<span class="d-only">Home cleaning and maintenance across Dubai. One accountable team — vetted, trained, and dispatched by us. Every job documented with before-and-after photos.</span>'),

    # --- who we serve ---
    ('<p>We stay focused on three districts and the people who live and invest in them. Focus is how we keep the standard high.</p>',
     '<p>Cleaning and maintenance across Dubai, subject to availability. Our premium AC servicing team currently focuses on Downtown Dubai, Business Bay and DIFC to keep scheduling tight.</p>'),

    # --- gallery ---
    ('<p>Every visit is documented with photos — here are the spotless spaces our team leaves behind across Downtown, Business Bay and DIFC.</p>',
     '<p>Every visit is documented with photos — here are the spotless spaces our team leaves behind across Dubai.</p>'),

    # --- visible FAQ ---
    ('<details><summary>Which areas do you cover?<span class="pl">+</span></summary><p>Downtown Dubai, Business Bay and DIFC. We stay focused on these districts on purpose — it\'s how we keep arrival times tight and quality consistent.</p></details>',
     '<details><summary>Which areas do you cover?<span class="pl">+</span></summary><p>' + AREA_LINE + ' Concentrating our AC team on those districts is how we keep arrival times tight and quality consistent.</p></details>'),

    # --- contact block ---
    ('<div class="row"><div><div class="lbl">Service area</div><div class="val">Downtown · Business Bay · DIFC</div></div></div>',
     '<div class="row"><div><div class="lbl">Service area</div><div class="val">Across Dubai · AC servicing: Downtown, Business Bay &amp; DIFC</div></div></div>'),

    # --- footer strapline ---
    ('<span>Downtown · Business Bay · DIFC · Dubai, UAE</span>',
     '<span>Dubai, United Arab Emirates</span>'),
]


def main():
    text = TARGET.read_text(encoding="utf-8")
    applied = 0

    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count == 0:
            print(f"FAILED: phrase not found, nothing replaced:\n  {old[:110]}...")
            return 1
        if count > 1:
            print(f"FAILED: phrase appears {count} times, refusing an ambiguous replace:\n  {old[:110]}...")
            return 1
        text = text.replace(old, new)
        applied += 1

    TARGET.write_text(text, encoding="utf-8", newline="\n")
    print(f"index.html — {applied} service-area statements updated")

    leftover = [p for p in ("stay focused on three districts", "professional core. One accountable")
                if p in text]
    if leftover:
        print(f"WARNING: still present: {leftover}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
