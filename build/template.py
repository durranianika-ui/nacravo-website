"""Shared page shell for the Nacravo service landing pages.

Static HTML has no include mechanism, so the header, footer, consent banner and
schema would drift across 12 files if maintained by hand. Everything shared
lives here once; build_pages.py renders it per page.

Design rules encoded below:
  * The hero carries NO decorative image — copy on the left, lead form on the
    right, so the form is above the fold on desktop and immediately after the
    description on mobile.
  * Header, footer, buttons, cards, colours and typography come from
    assets/nacravo.css, which is extracted verbatim from index.html.
  * Nothing here invents prices, ratings, testimonials or certifications.
"""

import html
import json
import pathlib
import re

import proof
import struct
from urllib.parse import quote

_IMAGE_DIR = pathlib.Path(__file__).resolve().parent.parent / "images"
_size_cache = {}


def image_size(filename):
    """Real intrinsic size of a JPEG, read from its SOF marker.

    Width/height are emitted from the actual file rather than hardcoded: the
    ba-* set is mostly 3:2 but ba-bathroom is 5:4, and a wrong aspect-ratio
    hint causes exactly the layout shift these attributes exist to prevent.
    """
    if filename in _size_cache:
        return _size_cache[filename]

    path = _IMAGE_DIR / filename
    size = (1080, 720)  # conservative fallback
    try:
        with open(path, "rb") as f:
            f.read(2)  # SOI
            while True:
                b = f.read(1)
                while b and b[0] != 0xFF:
                    b = f.read(1)
                while b and b[0] == 0xFF:
                    b = f.read(1)
                if not b:
                    break
                marker = b[0]
                length = struct.unpack(">H", f.read(2))[0]
                if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                    f.read(1)
                    h, w = struct.unpack(">HH", f.read(4))
                    size = (w, h)
                    break
                f.seek(length - 2, 1)
    except (OSError, struct.error):
        pass

    _size_cache[filename] = size
    return size

SITE = "https://www.nacravo.com"
PHONE_DISPLAY = "+971 55 540 3038"
PHONE_TEL = "+971555403038"
WA_NUMBER = "971555403038"
EMAIL = "info@nacravo.com"
GTM_ID = "GTM-KD4PH4XP"

# Navigation is defined once and rendered into every page's desktop mega-menu,
# mobile accordion and footer, so the three can never disagree.
NAV_CLEANING = [
    ("Home Cleaning", "/home-cleaning"),
    ("Deep Cleaning", "/deep-cleaning"),
    ("Move In / Move Out", "/move-in-out-cleaning"),
    ("Holiday Home Cleaning", "/holiday-home-cleaning"),
    ("Office &amp; Commercial", "/office-commercial-cleaning"),
    ("Specialized Cleaning", "/specialized-cleaning"),
    ("Pest Control", "/pest-control"),
]
# Air conditioning: the hub first, then the six dedicated service pages. Grouped
# in its own mega-menu column so the Maintenance section is not overloaded.
NAV_AC = [
    ("AC Services", "/ac-service-dubai"),
    ("AC Servicing", "/ac-servicing-dubai"),
    ("AC Chemical Cleaning", "/ac-chemical-cleaning-dubai"),
    ("AC Duct Cleaning", "/ac-duct-cleaning-dubai"),
    ("AC Repair", "/ac-repair-dubai"),
    ("AC Installation", "/ac-installation-dubai"),
    ("AC Maintenance Contracts", "/ac-maintenance-contract-dubai"),
]
NAV_MAINTENANCE = [
    ("Handyman Services", "/handyman-services"),
    ("Annual Maintenance", "/annual-maintenance"),
]


# ---------------------------------------------------------------- lead flow
# Operating hours supplied by Nacravo. "Same-day subject to availability" is a
# hedged statement of fact, not a response-time promise: no minute-based SLA is
# published anywhere until inbox and dispatch data can prove one.
HOURS_LINE = "Open daily, 7 AM\u201310 PM \u00b7 Same-day subject to availability"

# Step-1 answers. The values are the CRM vocabulary and must stay inside the
# allow-lists in api/leads.js — a value that is not on the list is dropped
# server-side rather than written to the Lead Register.
CLEAN_CHIPS = {
    "apartment":  ("Apartment", "Apartment Cleaning", "apartment apartment-cleaning home-cleaning maid-service regular-cleaning"),
    "villa":      ("Villa", "Villa Cleaning", "villa villa-cleaning townhouse-cleaning"),
    "deep":       ("Deep clean", "Deep Cleaning", "deep deep-cleaning post-construction"),
    "move":       ("Move in/out", "Move In/Out Cleaning", "move move-in move-out move-in-out move-in-out-cleaning"),
    "office":     ("Office", "Office Cleaning", "office commercial office-commercial-cleaning"),
    "sofa":       ("Sofa / upholstery", "Sofa & Upholstery Cleaning", "sofa upholstery carpet mattress curtain sofa-cleaning"),
    "holiday":    ("Holiday home", "Holiday Home Cleaning", "holiday holiday-home airbnb holiday-home-cleaning"),
    "specialist": ("Specialist clean", "Specialized Cleaning", "specialist specialized specialized-cleaning"),
}
AC_CHIPS = {
    "not-cooling": ("Not cooling", "Not cooling", "not-cooling no-cooling weak-cooling"),
    "leaking":     ("Leaking", "Leaking", "leaking water-leak leak"),
    "noise":       ("Strange noise", "Strange noise", "noise noisy"),
    "smell":       ("Bad smell", "Bad smell", "smell odour odor"),
    "service":     ("Service", "Service", "service servicing maintenance ac-servicing"),
    "chemical":    ("Chemical clean", "Chemical clean", "chemical chemical-wash chemical-cleaning"),
    "duct":        ("Duct cleaning", "Duct cleaning", "duct ducts duct-cleaning"),
    "install":     ("Installation", "Installation", "install installation new-ac"),
    "amc":         ("Maintenance contract", "Maintenance contract", "amc contract maintenance-contract"),
    "unsure":      ("Not sure", "Not sure", "unsure not-sure other"),
}

# url -> (vertical, [chip keys in display order], preselected chip key)
LEAD_FLOWS = {
    "/home-cleaning":               ("cleaning", ["apartment", "villa", "deep", "move", "office", "sofa"], "apartment"),
    "/deep-cleaning":               ("cleaning", ["deep", "apartment", "villa", "move", "office", "sofa"], "deep"),
    "/move-in-out-cleaning":        ("cleaning", ["move", "deep", "apartment", "villa", "office", "sofa"], "move"),
    "/holiday-home-cleaning":       ("cleaning", ["holiday", "apartment", "villa", "deep", "sofa"], "holiday"),
    "/office-commercial-cleaning":  ("cleaning", ["office", "deep", "sofa", "specialist"], "office"),
    "/specialized-cleaning":        ("cleaning", ["sofa", "specialist", "deep", "apartment", "villa"], "sofa"),
    "/ac-service-dubai":            ("ac", ["not-cooling", "leaking", "noise", "smell", "service", "chemical", "unsure"], ""),
    "/ac-servicing-dubai":          ("ac", ["service", "not-cooling", "smell", "leaking", "noise", "unsure"], "service"),
    "/ac-repair-dubai":             ("ac", ["not-cooling", "leaking", "noise", "smell", "service", "unsure"], "not-cooling"),
    "/ac-chemical-cleaning-dubai":  ("ac", ["chemical", "smell", "not-cooling", "service", "unsure"], "chemical"),
    "/ac-duct-cleaning-dubai":      ("ac", ["duct", "smell", "service", "unsure"], "duct"),
    "/ac-installation-dubai":       ("ac", ["install", "service", "unsure"], "install"),
    "/ac-maintenance-contract-dubai": ("ac", ["amc", "service", "chemical", "unsure"], "amc"),
}

# Step-1 question and the CTA vocabulary, per vertical. "Book" and "Submit" are
# deliberately absent: nothing is booked at this point and a generic verb tells
# the visitor nothing about what happens next.
FLOW_COPY = {
    "cleaning": {
        "q1": "What do you need cleaned?",
        "wa_cta": "Get Price on WhatsApp",
        "submit": "Get My Cleaning Price",
        "form_head": "Get your cleaning price",
        "form_sub": "Three short questions. We reply on WhatsApp with a fixed price.",
    },
    "ac": {
        "q1": "What is your AC doing?",
        "wa_cta": "WhatsApp a Technician",
        "submit": "Send My AC Problem",
        "form_head": "Send us the problem",
        "form_sub": "Three short questions. A technician replies on WhatsApp.",
    },
    "general": {
        "q1": "What do you need?",
        "wa_cta": "Get Price on WhatsApp",
        "submit": "Send My Request",
        "form_head": "Request a quote",
        "form_sub": "Three short questions. We reply on WhatsApp with a fixed price.",
    },
}


def lead_flow(page):
    """(vertical, chip list, preselected key) for a page. Pages outside the
    cleaning/AC paid corridors fall back to a single-service general flow so
    every form on the site still creates a real server-side lead."""
    v, keys, pre = LEAD_FLOWS.get(page["url"], (None, None, None))
    if v == "cleaning":
        return v, [(k,) + CLEAN_CHIPS[k] for k in keys], pre
    if v == "ac":
        return v, [(k,) + AC_CHIPS[k] for k in keys], pre
    label = page["service_value"]
    key = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    return "general", [(key, label, label, key)], key


# Sentence boundary: a full stop, question or exclamation mark, whitespace, then
# a capital. Deliberately simple — the hero copy is plain prose with no
# abbreviations, and a missed split only leaves a slightly longer hero.
_SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def lead_split(lead, keep=2):
    """(hero sentences, the rest). The rest is rendered below the hero rather
    than dropped, so no claim and no keyword leaves the page."""
    parts = _SENTENCE.split(lead.strip())
    if len(parts) <= keep:
        return lead, ""
    return " ".join(parts[:keep]), " ".join(parts[keep:])


def wa_link(text):
    return "https://wa.me/" + WA_NUMBER + "?text=" + quote(text)


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- icons
WA_ICON = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
           '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 '
           '4.79 1.22h.01c5.46 0 9.9-4.45 9.9-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm4.52 '
           '11.99c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.8-.79.97-.14.16-.29.18-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.48c-.16 '
           '0-.42.06-.64.31-.22.25-.84.82-.84 2 0 1.18.86 2.32.98 2.48.12.16 1.69 2.58 4.1 3.62.57.25 1.02.4 '
           '1.37.51.57.18 1.1.16 1.51.1.46-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.11-.22-.17-.47-.29Z"/></svg>')

PHONE_ICON = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
              '<path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 '
              '3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 '
              '1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2Z"/></svg>')

KEYSTONE_DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
                 '<symbol id="ks" viewBox="0 0 100 100"><path d="M28,30 Q28,18 50,18 Q72,18 72,30 L78,82 L22,82 Z" fill="currentColor"/>'
                 '<path d="M44,54 L49,61 L60,46" stroke="#F5F2EC" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></symbol>'
                 '<symbol id="ksf" viewBox="0 0 100 100"><path d="M28,30 Q28,18 50,18 Q72,18 72,30 L78,82 L22,82 Z" fill="currentColor"/>'
                 '<path d="M44,54 L49,61 L60,46" stroke="#2E372B" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></symbol></svg>')

TRUST_ICONS = {
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "camera": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "team": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "tag": '<path d="M20.59 13.41 13.42 20.58a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82Z"/><circle cx="7" cy="7" r="1.4" fill="currentColor" stroke="none"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>',
}


def trust_pill(icon, label):
    path = TRUST_ICONS.get(icon, TRUST_ICONS["check"])
    return ('<span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + "</svg>" + esc(label) + "</span>")


# ---------------------------------------------------------------- head
def _derivative(filename, ext):
    """images/foo-1080.jpg -> foo-1080.avif, but only if it was actually built."""
    cand = _IMAGE_DIR / (pathlib.Path(filename).stem + "." + ext)
    return cand.name if cand.exists() else None


def picture(big, small, sizes, alt, load_attrs, cls=""):
    """<picture> with AVIF and WebP sources over the original JPEG.

    Width and height come from the real JPEG, so the box is reserved before any
    format loads and there is no layout shift. A format is only offered when
    both derivatives exist; a half-built set falls back to the JPEG cleanly.
    """
    w, h = image_size(big)
    sw, _ = image_size(small)
    sources = ""
    for ext, mime in (("avif", "image/avif"), ("webp", "image/webp")):
        b, sm = _derivative(big, ext), _derivative(small, ext)
        if b and sm:
            sources += (f'\n        <source type="{mime}" '
                        f'srcset="images/{sm} {sw}w, images/{b} {w}w" sizes="{sizes}">')
    klass = f' class="{cls}"' if cls else ""
    return (f'<picture{klass}>{sources}\n'
            f'        <img src="images/{big}" srcset="images/{small} {sw}w, images/{big} {w}w"\n'
            f'             sizes="{sizes}" alt="{esc(alt)}"\n'
            f'             width="{w}" height="{h}" {load_attrs} decoding="async">\n'
            f'      </picture>')


def render_head(page):
    canonical = SITE + page["url"]
    og_image = SITE + "/images/" + page.get("og_image", "hero4-lg.jpg")

    schema_blocks = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": page["service_schema_name"],
            "serviceType": page["service_schema_name"],
            "description": page["meta_description"],
            "url": canonical,
            "areaServed": page["area_served_schema"],
            "provider": {
                "@type": "HomeAndConstructionBusiness",
                "name": "Nacravo",
                "url": SITE + "/",
                "telephone": PHONE_TEL,
                "email": EMAIL,
                "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE"},
            },
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": page["h1"],
                "itemListElement": [
                    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"]}}
                    for s in page["sections"]
                ],
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "/services"},
                {"@type": "ListItem", "position": 3, "name": page["breadcrumb"], "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in page["faq"]
            ],
        },
    ]

    schema_html = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(b, indent=2, ensure_ascii=False) + "\n</script>"
        for b in schema_blocks
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google Consent Mode v2 — defaults set BEFORE GTM loads -->
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
(function(){{var c=null;try{{c=JSON.parse(localStorage.getItem('nacravo_consent'));}}catch(e){{}}
 var a=(c&&c.analytics)?'granted':'denied',d=(c&&c.ad)?'granted':'denied';
 gtag('consent','default',{{ad_storage:d,ad_user_data:d,ad_personalization:d,analytics_storage:a,functionality_storage:'granted',security_storage:'granted',wait_for_update:500}});
 if(c){{gtag('consent','update',{{ad_storage:d,ad_user_data:d,ad_personalization:d,analytics_storage:a}});}}
}})();
</script>
<!-- Central tracking configuration — IDs live in one place, identical to index.html -->
<script>
  window.NACRAVO_TRACKING = {{
    GTM_ID: "{GTM_ID}",
    GA4_ID: "G-N2VGBEBELF",
    GOOGLE_ADS_ID: "",
    ADS_FORM_LABEL: "",
    ADS_WHATSAPP_LABEL: "",
    ADS_CALL_LABEL: "",
    META_PIXEL_ID: "",
    CLARITY_ID: "",
    LINKEDIN_PARTNER_ID: "",
    TIKTOK_PIXEL_ID: "",
    PINTEREST_TAG_ID: "",
    LOAD_PIXELS_DIRECTLY: false
  }};
</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(page['title'])}</title>

<meta name="description" content="{esc(page['meta_description'])}">
<meta name="author" content="Nacravo">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#3B4636">

<meta property="og:type" content="website">
<meta property="og:title" content="{esc(page['og_title'])}">
<meta property="og:description" content="{esc(page['og_description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Nacravo">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="en_AE">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page['og_title'])}">
<meta name="twitter:description" content="{esc(page['og_description'])}">
<meta name="twitter:image" content="{og_image}">

<meta name="geo.region" content="AE-DU">
<meta name="geo.placename" content="Dubai">

<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/nacravo.css">
<script>
/* Paid landing mode, decided before first paint so the browse chrome never
   flashes. Applies only to the view that actually carries the ad click:
   land from an ad and the page drops the navigation that would leak the
   click away; choose to browse on and the full site comes back. Crawlers
   never carry a click id, so the indexed page is always the complete one. */
document.documentElement.className+=" lf-js";
(function(){{try{{var q=new URLSearchParams(location.search);
if(q.get("gclid")||q.get("gbraid")||q.get("wbraid")||/^(cpc|ppc|paid|paidsearch|paid_social)$/i.test(q.get("utm_medium")||"")){{document.documentElement.setAttribute("data-paid","1");}}}}catch(e){{}}}})();
</script>

{schema_html}
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip-link" href="#main">Skip to main content</a>
{KEYSTONE_DEFS}
"""


# ---------------------------------------------------------------- header
def render_header(page):
    def links(items):
        return "".join(f'<a href="{u}">{t}</a>' for t, u in items)

    wa = wa_link(page["wa_text"])

    return f"""
<header class="nav">
  <div class="wrap nav-in">
    <a href="/" class="brand" aria-label="Nacravo — home"><svg class="keystone" width="30" height="30" style="color:var(--moss)" aria-hidden="true"><use href="#ks"/></svg>nacravo</a>
    <nav class="nav-links" aria-label="Primary">
      <div class="has-drop">
        <button type="button" class="drop-toggle" aria-expanded="false" aria-controls="svcDrop">Services
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
        </button>
        <div class="drop-panel" id="svcDrop" role="menu" aria-label="Services">
          <div class="drop-col"><div class="drop-h">Cleaning</div>{links(NAV_CLEANING)}</div>
          <div class="drop-col"><div class="drop-h">Air Conditioning</div>{links(NAV_AC)}</div>
          <div class="drop-col"><div class="drop-h">Maintenance</div>{links(NAV_MAINTENANCE)}</div>
        </div>
      </div>
      <a href="/services">All services</a>
      <a href="/#why">Why us</a>
      <a href="/#packages">Membership</a>
      <a href="#faq">FAQ</a>
    </nav>
    <div class="nav-cta">
      <a href="tel:{PHONE_TEL}" class="btn btn-ghost" aria-label="Call Nacravo on {PHONE_DISPLAY}">Call now</a>
      <a href="{wa}" target="_blank" rel="noopener" class="btn btn-primary nav-wa" aria-label="Message Nacravo on WhatsApp">{WA_ICON.format(s=17)}<span class="lbl-full">Message on WhatsApp</span><span class="lbl-short">WhatsApp</span></a>
      <button type="button" class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <div class="wrap">
      <details class="mm-group">
        <summary>Services <span class="pl">+</span></summary>
        <div class="mm-links">
          <div class="mm-sub">Cleaning</div>{links(NAV_CLEANING)}
          <div class="mm-sub">Air Conditioning</div>{links(NAV_AC)}
          <div class="mm-sub">Maintenance</div>{links(NAV_MAINTENANCE)}
        </div>
      </details>
      <a href="/services">All services</a>
      <a href="/#why">Why Nacravo</a>
      <a href="/#packages">Membership</a>
      <a href="#faq">FAQ</a>
      <a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</header>

<nav class="crumb" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li class="sep" aria-hidden="true">/</li>
    <li><a href="/services">Services</a></li>
    <li class="sep" aria-hidden="true">/</li>
    <li aria-current="page">{esc(page['breadcrumb'])}</li>
  </ol>
</nav>
"""


# ---------------------------------------------------------------- hero + lead form
def render_hero(page):
    """Copy and both direct CTAs first, then a three-step qualification flow.

    The old single form asked for name, phone, service and location before the
    visitor had said what the job actually was, validated locally, pushed a
    conversion and then handed over to WhatsApp — so a visitor who never sent
    the message produced a counted conversion and no lead. The flow below asks
    what / scope / where-and-number, and POSTs to /api/leads before anything is
    announced or counted (see assets/nacravo-lead.js).
    """
    trust = "".join(trust_pill(i, l) for i, l in page["trust"])
    wa = wa_link(page["wa_text"])
    vertical, chips, preselect = lead_flow(page)
    copy = FLOW_COPY[vertical]
    is_ac = vertical == "ac"
    field_name = "problem" if is_ac else "service"

    # Real radios: native arrow-key navigation and ARIA, and a step 1 that still
    # works with JavaScript off. The visible chip is the <label>.
    chip_html = "".join(
        '<input type="radio" class="lf-radio" id="lfo-{key}" name="{name}" value="{val}"'
        ' data-intent="{intent}"{checked}>'
        '<label class="lf-chip" for="lfo-{key}">{label}</label>'.format(
            key=esc(key), name=field_name, val=esc(value), intent=esc(intent),
            label=esc(label), checked=" checked" if key == preselect else "")
        for (key, label, value, intent) in chips
    )

    # ---- step 2: scope. Only questions that change the quote are asked, and a
    # commercial answer never sees a bedroom count (handled by data-when).
    if is_ac:
        step2 = """
          <div class="form-row">
            <div class="field">
              <label for="property_type">Where is the AC?</label>
              <select id="property_type" name="property_type">
                <option value="">Select\u2026</option>
                <option>Apartment</option><option>Villa</option><option>Townhouse</option>
                <option>Office</option><option>Retail</option><option>Other</option>
              </select>
            </div>
            <div class="field">
              <label for="units">How many AC units?</label>
              <input type="number" id="units" name="units" min="1" max="999" inputmode="numeric" placeholder="e.g. 4">
              <span class="lf-hint">Leave blank if you are not sure.</span>
            </div>
          </div>"""
    else:
        step2 = """
          <div class="form-row" data-when="residential">
            <div class="field">
              <label for="property_type">Property type</label>
              <select id="property_type" name="property_type">
                <option value="">Select\u2026</option>
                <option>Apartment</option><option>Villa</option><option>Townhouse</option><option>Other</option>
              </select>
            </div>
            <div class="field">
              <label for="size">How big is it?</label>
              <select id="size" name="size">
                <option value="">Select\u2026</option>
                <option>Studio</option><option>1 bedroom</option><option>2 bedrooms</option>
                <option>3 bedrooms</option><option>4+ bedrooms</option>
              </select>
            </div>
          </div>
          <div class="form-row" data-when="commercial" hidden>
            <div class="field">
              <label for="size_commercial">Approx. size of premises</label>
              <select id="size_commercial" name="size">
                <option value="">Select\u2026</option>
                <option>Under 1,000 sq ft</option><option>1,000 - 3,000 sq ft</option>
                <option>3,000 - 7,000 sq ft</option><option>7,000 - 15,000 sq ft</option>
                <option>Over 15,000 sq ft</option>
              </select>
            </div>
            <div class="field">
              <label for="company">Company name</label>
              <input type="text" id="company" name="company" autocomplete="organization" placeholder="Which business is this for?">
            </div>
          </div>
          <div class="form-row">
            <div class="field full">
              <label for="frequency">How often?</label>
              <select id="frequency" name="frequency">
                <option value="">Not sure yet</option>
                <option>One-off</option><option>Weekly</option><option>Fortnightly</option>
                <option>Monthly</option><option>Daily (6-7 days a week)</option>
                <option>5 days a week</option><option>3 days a week</option>
              </select>
            </div>
          </div>"""

    # Location stays free text so no legitimate Dubai enquiry is ever blocked;
    # the datalist only offers one-tap suggestions on a mostly-mobile audience.
    area_list = ""
    area_datalist = ""
    if page.get("location_suggestions"):
        area_list = ' list="areaOptions"'
        _opts = "".join('<option value="{0}"></option>'.format(esc(o))
                        for o in page["location_suggestions"])
        area_datalist = '<datalist id="areaOptions">' + _opts + "</datalist>"

    media = ""
    if page.get("hero_image"):
        big, small, alt = page["hero_image"]
        load_attrs = ('loading="eager" fetchpriority="high"'
                      if page.get("hero_eager") else 'loading="lazy"')
        media = ('\n      <div class="lp-hero-media">\n        '
                 + picture(big, small, "(max-width:900px) 92vw, 420px", alt, load_attrs)
                 + "\n      </div>")

    jump = ""
    if page.get("jump_links"):
        items = "".join(f'<a href="#{a}">{esc(t)}</a>' for t, a in page["jump_links"])
        jump = f'<div class="wrap" style="padding-bottom:8px"><div class="jump">{items}</div></div>'

    wa_cta = page.get("wa_cta", copy["wa_cta"])
    lead_head, lead_rest = lead_split(page["lead"])
    lead_more = ""
    if lead_rest:
        lead_more = ('<div class="wrap lp-lead-rest"><p>' + esc(lead_rest) + "</p></div>")

    return f"""
<main id="main">
<section class="lp-hero">
  <div class="wrap lp-hero-grid">
    <div class="lp-hero-copy">
      <div class="lp-hero-head">
        <span class="eyebrow">{esc(page['eyebrow'])}</span>
        <h1>{esc(page['h1'])}</h1>
        <p class="lead">{esc(lead_head)}</p>
      </div>
      <div class="lp-hero-rest">
        <div class="lp-hero-cta">
          <a href="{wa}" target="_blank" rel="noopener" class="btn btn-wa" data-track="booking" data-service-name="{esc(page['service_value'])}" data-track-label="Hero: WhatsApp">{WA_ICON.format(s=18)} {esc(wa_cta)}</a>
          <a href="tel:{PHONE_TEL}" class="btn btn-call">{PHONE_ICON} Call {PHONE_DISPLAY}</a>
        </div>
        <p class="lp-hero-avail">{esc(HOURS_LINE)}</p>
        <div class="trust">{trust}</div>
      </div>{media}
    </div>

    <div class="lp-form-wrap">
      <form class="lp-form lf" id="leadForm" action="/api/leads" method="post" novalidate
            data-vertical="{vertical}" data-preselect="{esc(preselect or '')}"
            aria-labelledby="leadFormTitle">
        <div class="lf-chrome">
          <h2 id="leadFormTitle" class="lf-head">{esc(copy['form_head'])}</h2>
          <p class="lp-form-sub">{esc(copy['form_sub'])}</p>
          <p class="lf-progress" data-step="1" aria-hidden="true">Step 1 of 3</p>
        </div>

        <div class="lf-errors" id="leadErrors" role="alert" hidden></div>

        <div class="lf-step" data-step="1">
          <fieldset class="lf-fieldset">
            <legend class="lf-q" id="lfQ1">{esc(copy['q1'])}</legend>
            <div class="lf-choice" data-name="{field_name}">{chip_html}</div>
            <span class="err-msg">Please choose one to continue.</span>
          </fieldset>
          <div class="lf-nav">
            <button type="button" class="btn btn-primary lf-next" data-lf-next>Continue</button>
          </div>
        </div>

        <div class="lf-step" data-step="2" hidden>
          <p class="lf-q">Tell us a little about the job</p>{step2}
          <div class="lf-nav">
            <button type="button" class="btn btn-ghost" data-lf-back>Back</button>
            <button type="button" class="btn btn-primary lf-next" data-lf-next>Continue</button>
          </div>
        </div>

        <div class="lf-step" data-step="3" hidden>
          <p class="lf-q">Where are you, and where should we reply?</p>
          <div class="form-row">
            <div class="field full">
              <label for="area">Area or building <span class="req" aria-hidden="true">*</span></label>
              <input type="text" id="area" name="area" placeholder="e.g. Business Bay" autocomplete="address-level2"{area_list} required aria-describedby="areaHint">
              {area_datalist}
              <span class="lf-hint" id="areaHint">So we can confirm we cover you.</span>
              <span class="err-msg">Please enter the area or building.</span>
            </div>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="phone">WhatsApp / phone number <span class="req" aria-hidden="true">*</span></label>
              <input type="tel" id="phone" name="phone" placeholder="e.g. 055 123 4567" autocomplete="tel" required aria-describedby="phoneHint">
              <span class="lf-hint" id="phoneHint">Used only to answer this request.</span>
              <span class="err-msg">Please enter a valid contact number.</span>
            </div>
            <div class="field">
              <label for="name">Your name <span class="lf-opt">(optional)</span></label>
              <input type="text" id="name" name="name" placeholder="Who should we ask for?" autocomplete="name">
            </div>
          </div>

          <details class="lp-extra">
            <summary class="lp-more">Add a date or a note (optional)</summary>
            <div class="lp-optional">
              <div class="form-row">
                <div class="field">
                  <label for="preferred_date">Preferred date</label>
                  <input type="date" id="preferred_date" name="preferred_date">
                </div>
                <div class="field">
                  <label for="email">Email <span class="lf-opt">(optional)</span></label>
                  <input type="email" id="email" name="email" autocomplete="email" placeholder="you@email.com">
                </div>
              </div>
              <div class="form-row">
                <div class="field full">
                  <label for="notes">Anything we should know?</label>
                  <textarea id="notes" name="notes" rows="3"></textarea>
                </div>
              </div>
            </div>
          </details>

          <input type="hidden" name="vertical" value="{vertical}">
          <p class="lf-hp" aria-hidden="true">
            <label for="website">Leave this field empty</label>
            <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
          </p>

          <div class="lf-nav">
            <button type="button" class="btn btn-ghost" data-lf-back>Back</button>
            <button type="submit" class="btn btn-wa lf-submit" data-lf-submit>{WA_ICON.format(s=18)} {esc(copy['submit'])}</button>
          </div>

          <div class="lf-consent">
            <input type="checkbox" id="consent_marketing" name="consent_marketing">
            <label for="consent_marketing">Send me occasional Nacravo offers. Optional \u2014 you will get an answer to this request either way.</label>
          </div>
        </div>

        <div class="form-status" id="leadStatus" role="status" aria-live="polite"></div>

        <!-- Shown only if the lead store is unreachable. Carries everything the
             visitor already typed, so a backend outage costs an enquiry the
             extra tap, not the enquiry itself. -->
        <div class="lf-fallback" id="leadFallback" hidden>
          <p>We could not store your request automatically. Send it to us directly instead &mdash; everything you filled in is already in the message.</p>
          <a href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener" class="btn btn-wa" id="leadFallbackWa" data-no-track>{WA_ICON.format(s=18)} Send my details on WhatsApp</a>
          <a href="tel:{PHONE_TEL}" class="btn btn-call">{PHONE_ICON} Call {PHONE_DISPLAY}</a>
        </div>

        <div class="lf-success" id="leadSuccess" hidden>
          <h2>Thanks \u2014 your request is with Nacravo.</h2>
          <p>We have your details and will come back to you during opening hours ({esc(HOURS_LINE.split(' \u00b7 ')[0])}). Quote your reference if you contact us:</p>
          <p class="lf-ref"><span id="leadRefOut"></span></p>
          <div class="lf-success-cta">
            <a href="https://wa.me/{WA_NUMBER}" target="_blank" rel="noopener" class="btn btn-wa" id="leadWaBtn">{WA_ICON.format(s=18)} Continue on WhatsApp</a>
            <a href="tel:{PHONE_TEL}" class="btn btn-call">{PHONE_ICON} Call {PHONE_DISPLAY}</a>
          </div>
          <p class="lf-hint">Continuing on WhatsApp is optional \u2014 your request has already reached us.</p>
        </div>

        <p class="lp-fineprint">We use your details only to respond to this enquiry. See our <a href="/privacy-policy">Privacy Policy</a>.</p>
      </form>
    </div>
  </div>
</section>
{lead_more}
{jump}
"""


# ---------------------------------------------------------------- body sections
def render_sections(page):
    """The sub-service anchor sections. Each is a real #anchor target and each
    CTA preselects its sub-service in the hero form via data-subservice."""
    cards = []
    for s in page["sections"]:
        bullets = "".join(f'<li><span class="ck">✓</span>{esc(b)}</li>' for b in s["bullets"])
        wa = wa_link(s.get("wa_text", page["wa_text"]))
        cards.append(f"""
      <article class="anchor-card" id="{s['anchor']}">
        <h3>{esc(s['title'])}</h3>
        <p>{esc(s['body'])}</p>
        <ul>{bullets}</ul>
        <div class="anchor-cta">
          <a href="{wa}" target="_blank" rel="noopener" class="btn btn-wa" data-track="booking" data-service-name="{esc(s.get('service_name', page['service_value']))}" data-track-label="{esc(s['title'])}: WhatsApp">{WA_ICON.format(s=17)} WhatsApp</a>
          <a href="tel:{PHONE_TEL}" class="btn btn-call" data-track-label="{esc(s['title'])}: Call">{PHONE_ICON} Call</a>
          <a href="#leadFormTitle" class="btn btn-ghost" data-subservice="{s['anchor']}" data-track="quote" data-track-label="{esc(s['title'])}: Get a quote">Get a quote</a>
        </div>
      </article>""")

    # Contextual in-body links. Already-escaped HTML by design — the anchors are
    # authored in build/links.py, not user input.
    ctx = f'\n      <p class="ctx-note">{page["contextual"]}</p>' if page.get("contextual") else ""

    return f"""
<section id="services">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">What's included</span>
      <h2>{esc(page['sections_heading'])}</h2>
      <p>{esc(page['sections_intro'])}</p>{ctx}
    </div>
    <div class="anchor-grid">{''.join(cards)}
    </div>
  </div>
</section>
"""


def render_cta_band(page, heading, body, anchor_id="cta"):
    wa = wa_link(page["wa_text"])
    # The services hub has no hero form of its own, so its quote CTA points at
    # the homepage enquiry form instead of a local anchor.
    quote_href = page.get("quote_href", "#leadFormTitle")
    return f"""
<section id="{anchor_id}" style="padding:0 0 56px">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>{esc(heading)}</h2>
        <p>{esc(body)}</p>
      </div>
      <div class="cta-band-btns">
        <a href="{wa}" target="_blank" rel="noopener" class="btn btn-wa" data-track="booking" data-service-name="{esc(page['service_value'])}" data-track-label="Mid-page: WhatsApp">{WA_ICON.format(s=17)} WhatsApp</a>
        <a href="tel:{PHONE_TEL}" class="btn btn-call">{PHONE_ICON} Call {PHONE_DISPLAY}</a>
        <a href="{quote_href}" class="btn btn-ghost" data-track="quote" data-track-label="Mid-page: Get a quote">Get a quote</a>
      </div>
    </div>
  </div>
</section>
"""


def render_why(page):
    pillars = "".join(f"""
      <div class="pillar">
        <div class="pn"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F5F2EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{TRUST_ICONS.get(icon, TRUST_ICONS['check'])}</svg></div>
        <h3>{esc(t)}</h3>
        <p>{esc(b)}</p>
      </div>""" for icon, t, b in page["why"])

    return f"""
<section class="pillars" id="why">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Why Nacravo</span>
      <h2>{esc(page['why_heading'])}</h2>
      <p>{esc(page['why_intro'])}</p>
    </div>
    <div class="pillar-grid">{pillars}
    </div>
  </div>
</section>
"""


def render_process(page):
    steps = "".join(f"""
      <div class="step"><div class="num">{i}</div><h3>{esc(t)}</h3><p>{esc(b)}</p></div>"""
                    for i, (t, b) in enumerate(page["process"], 1))
    return f"""
<section id="process" style="background:var(--sand)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">How it works</span>
      <h2>{esc(page['process_heading'])}</h2>
    </div>
    <div class="steps">{steps}
    </div>
  </div>
</section>
"""


def render_areas(page):
    cards = "".join(f"""
      <div class="serve-card"><h3>{esc(t)}</h3><p>{esc(b)}</p></div>""" for t, b in page["areas"])

    # Named communities, general-service pages only. The AC page deliberately
    # omits this — its coverage is scoped to three districts.
    local = ""
    if page.get("communities"):
        chips = "".join(f"<span>{esc(c)}</span>" for c in page["communities"])
        local = f"""
    <div class="local-areas">
      <p class="local-intro">{esc(page['local_intro'])}</p>
      <div class="area-chips">{chips}</div>
      <p class="local-note">{esc(page['local_note'])}</p>
    </div>"""

    return f"""
<section id="areas">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Coverage</span>
      <h2>{esc(page['areas_heading'])}</h2>
      <p>{esc(page['areas_intro'])}</p>
    </div>
    <div class="serve-grid">{cards}
    </div>{local}
  </div>
</section>
"""


def render_pricing(page):
    """No published prices anywhere on the site, so this explains how pricing
    works rather than inventing numbers."""
    points = "".join(f'<li><span class="ck">✓</span>{esc(p)}</li>' for p in page["pricing_points"])
    return f"""
<section id="pricing" style="background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Pricing</span>
      <h2>{esc(page['pricing_heading'])}</h2>
      <p>{esc(page['pricing_intro'])}</p>
    </div>
    <div class="anchor-grid">
      <div class="anchor-card">
        <h3>How we quote</h3>
        <ul>{points}</ul>
        <div class="anchor-cta">
          <a href="#leadFormTitle" class="btn btn-primary" data-track="quote" data-track-label="Pricing: Get a quote">Get my fixed price</a>
        </div>
      </div>
      <div class="anchor-card">
        <h3>What's included as standard</h3>
        <ul>
          <li><span class="ck">✓</span>Materials and equipment brought by our team</li>
          <li><span class="ck">✓</span>Trained technicians employed by Nacravo</li>
          <li><span class="ck">✓</span>Before-and-after photo report after every visit</li>
          <li><span class="ck">✓</span>One accountable point of contact on WhatsApp</li>
        </ul>
      </div>
    </div>
  </div>
</section>
"""


def render_faq(page):
    items = "".join(f"""
      <details>
        <summary>{esc(q)}<span class="pl" aria-hidden="true">+</span></summary>
        <p>{esc(a)}</p>
      </details>""" for q, a in page["faq"])
    return f"""
<section id="faq">
  <div class="wrap">
    <div class="sec-head center">
      <span class="eyebrow">FAQ</span>
      <h2>{esc(page['faq_heading'])}</h2>
    </div>
    <div class="faq-list">{items}
    </div>
  </div>
</section>
"""


def render_reviews(page):
    """Verified customer proof. Renders only when build/proof.py carries a real
    rating and real quotes — there is no placeholder to forget to replace, so an
    invented rating cannot be published. See build/proof.py for what is needed."""
    if not proof.has(proof.REVIEWS):
        return ""
    r = proof.REVIEWS
    quotes = "".join(f"""
      <figure class="rev-card">
        <blockquote>{esc(q['text'])}</blockquote>
        <figcaption>{esc(q['name'])} \u00b7 {esc(q['date'])}</figcaption>
      </figure>""" for q in r.get("quotes", []))
    return f"""
<section id="reviews">
  <div class="wrap">
    <div class="sec-head center">
      <span class="eyebrow">Reviews</span>
      <h2>What Dubai customers say</h2>
      <p class="rev-rating"><strong>{esc(str(r['rating']))}</strong> from {esc(str(r['count']))} Google reviews \u00b7
        <a href="{esc(r['url'])}" target="_blank" rel="noopener">read them on Google</a></p>
    </div>
    <div class="rev-grid">{quotes}
    </div>
  </div>
</section>
"""


def render_proof_strip(page):
    """The above-the-fold verified-proof row: rating, then the remedy policy.
    Both are omitted entirely while unverified, rather than softened."""
    bits = []
    if proof.has(proof.REVIEWS):
        r = proof.REVIEWS
        bits.append(f'<span class="ps-item"><strong>{esc(str(r["rating"]))}</strong> '
                    f'from {esc(str(r["count"]))} Google reviews</span>')
    if proof.has(proof.WARRANTY):
        bits.append(f'<span class="ps-item">{esc(proof.WARRANTY["heading"])}</span>')
    if not bits:
        return ""
    return ('\n<section class="proof-strip"><div class="wrap">'
            + "".join(bits) + "</div></section>\n")


def render_gallery(page):
    """Proof photos, below the fold and lazy-loaded.

    Only rendered where the photography genuinely depicts the service. A page
    with no honest asset gets an HTML comment recording the gap rather than an
    empty box or a borrowed, misleading photo.

    Items are (large file, small file, caption, alt). Explicit width/height come
    from the real files so there is no layout shift.
    """
    gap = page.get("gallery_gap")
    if gap:
        return (f"\n<!-- GALLERY PLACEHOLDER — {page['url']}\n"
                f"     {gap}\n"
                f"     See build/media.py GALLERY_GAPS. -->\n")

    items = page.get("gallery_items")
    if not items:
        return ""

    cells = []
    for big, small, tag, alt in items:
        img = picture(big, small,
                      "(max-width:480px) 92vw,(max-width:760px) 46vw,360px",
                      alt, 'loading="lazy"')
        cells.append(f"""
      <figure class="gal-cell">
        {img}
        <figcaption class="gal-tag">{esc(tag)}</figcaption>
      </figure>""")

    single = ' style="grid-template-columns:minmax(0,560px)"' if len(cells) == 1 else ""

    return f"""
<section id="proof" style="background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Our work</span>
      <h2>{esc(page['gallery_heading'])}</h2>
      <p>{esc(page['gallery_note'])}</p>
    </div>
    <div class="gallery"{single}>{"".join(cells)}
    </div>
  </div>
</section>
"""


def render_related(page):
    cards = "".join(f"""
      <a class="rel-card" href="{u}">
        <h3>{esc(t)}</h3>
        <p>{esc(d)}</p>
        <span class="rel-go">View service →</span>
      </a>""" for t, u, d in page["related"])
    return f"""
<section id="related" style="background:var(--sand)">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Related services</span>
      <h2>Often booked together</h2>
      <p>One team covers your whole property, so you are not chasing three different companies.</p>
    </div>
    <div class="rel-grid">{cards}
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------- footer
def render_footer(page):
    def links(items):
        return "".join(f'<a href="{u}">{t}</a>' for t, u in items)

    wa = wa_link(page["wa_text"])

    # Cache pin for assets/nacravo.js. Vercel serves the file with
    # must-revalidate + ETag, so this is belt-and-braces rather than the
    # mechanism; it exists on the paid landing page so the tracker revision
    # serving ad traffic is unambiguous. Set "tracker_pin" to the commit that
    # last changed the tracker.
    tracker_pin = f"?v={page['tracker_pin']}" if page.get("tracker_pin") else ""

    return f"""
</main>

<footer>
  <div class="wrap">
    <div class="foot-grid foot-5">
      <div>
        <div class="foot-brand"><svg class="keystone" width="27" height="27" style="color:var(--pearl)" aria-hidden="true"><use href="#ksf"/></svg>nacravo</div>
        <p class="foot-tag">The same standard, every visit. Cleaning and maintenance across Dubai, with a photo report on every job.</p>
        <p class="foot-tag" style="margin-top:12px"><a href="tel:{PHONE_TEL}" style="display:inline">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}" style="display:inline">{EMAIL}</a></p>
      </div>
      <div>
        <h2 class="fh">Cleaning</h2>
        {links(NAV_CLEANING)}
      </div>
      <div>
        <h2 class="fh">Maintenance</h2>
        {links(NAV_AC + NAV_MAINTENANCE)}
      </div>
      <div>
        <h2 class="fh">Company</h2>
        <a href="/services">All services</a><a href="/#why">Why Nacravo</a><a href="/#packages">Membership</a><a href="/#contact">Contact</a><a href="/application">Application Information</a>
      </div>
      <div>
        <h2 class="fh">Legal</h2>
        <a href="/legal">Legal Center</a><a href="/privacy-policy">Privacy Policy</a><a href="/terms-of-service">Terms of Service</a><a href="/cookie-policy">Cookie Policy</a><a href="/sitemap">Sitemap</a>
      </div>
    </div>
    <nav class="foot-legal" aria-label="Legal">
      <a href="/privacy-policy">Privacy Policy</a><a href="/terms-of-service">Terms of Service</a><a href="/cookie-policy">Cookie Policy</a><a href="/refund-policy">Refund &amp; Cancellation</a><a href="/data-deletion">Data Deletion</a><a href="/accessibility">Accessibility</a><a href="/security">Security</a><a href="/acceptable-use">Acceptable Use</a><a href="/legal">Legal Center</a><a href="/sitemap">Sitemap</a><button type="button" onclick="return nacravoCookieSettings()">Cookie settings</button>
    </nav>
    <div class="foot-bottom">
      <span>© 2026 Nacravo LLC · DHH Group. All Rights Reserved.</span>
      <span>Dubai, United Arab Emirates</span>
    </div>
  </div>
</footer>

<!-- Sticky mobile bar (mobile carries the WhatsApp CTA here, so the floating
     button is desktop-only and the two can never overlap) -->
<div class="mbar" role="group" aria-label="Contact Nacravo">
  <a href="tel:{PHONE_TEL}" class="call" aria-label="Call Nacravo on {PHONE_DISPLAY}">{PHONE_ICON} Call</a>
  <a href="{wa}" target="_blank" rel="noopener" class="wa" aria-label="Message Nacravo on WhatsApp">{WA_ICON.format(s=16)} WhatsApp</a>
</div>

<a class="wa-float" href="{wa}" target="_blank" rel="noopener" aria-label="Chat with Nacravo on WhatsApp" data-track="booking" data-service-name="{esc(page['service_value'])}" data-track-label="Floating WhatsApp">{WA_ICON.format(s=30)}</a>

<div class="cc-banner" id="ccBanner" role="dialog" aria-modal="false" aria-label="Cookie consent">
  <h2>We value your privacy</h2>
  <p>We use essential cookies to run this site and, with your consent, analytics and advertising cookies (Google, Meta, Microsoft) to improve our service and marketing. See our <a href="/cookie-policy">Cookie Policy</a>.</p>
  <div class="cc-row">
    <button class="cc-btn primary" id="ccAccept">Accept all</button>
    <button class="cc-btn" id="ccReject">Reject non-essential</button>
    <button class="cc-btn" id="ccPrefs">Preferences</button>
  </div>
</div>
<div class="cc-modal" id="ccModal" role="dialog" aria-modal="true" aria-labelledby="ccModalTitle">
  <div class="cc-card">
    <h2 id="ccModalTitle">Cookie preferences</h2>
    <p>Choose which cookies Nacravo may use. Essential cookies are always on because the site cannot work without them.</p>
    <div class="cc-opt"><div><span class="t">Essential</span><small>Required for security and core functionality. Always active.</small></div><input type="checkbox" checked disabled aria-label="Essential cookies (always on)"></div>
    <div class="cc-opt"><div><span class="t">Analytics</span><small>Google Analytics (GA4) — aggregate usage measurement.</small></div><input type="checkbox" id="ccAnalytics" aria-label="Analytics cookies"></div>
    <div class="cc-opt"><div><span class="t">Advertising</span><small>Google Ads, Meta, Microsoft — ad measurement and personalisation.</small></div><input type="checkbox" id="ccAds" aria-label="Advertising cookies"></div>
    <div class="cc-actions">
      <button class="cc-btn primary" id="ccSave">Save preferences</button>
      <button class="cc-btn" id="ccClose">Cancel</button>
    </div>
  </div>
</div>

<script>
  window.NACRAVO_PAGE = {json.dumps({'service': page['service_value'], 'subservices': page.get('subservices', {})}, ensure_ascii=False)};
</script>
<script src="/assets/nacravo-nav.js" defer></script>
<script src="/assets/nacravo-attr.js{tracker_pin}" defer></script>
<script src="/assets/nacravo.js{tracker_pin}" defer></script>
<script src="/assets/nacravo-lead.js{tracker_pin}" defer></script>
</body>
</html>
"""


def render_page(page):
    return (
        render_head(page)
        + render_header(page)
        + render_hero(page)
        + render_proof_strip(page)
        # Proof before persuasion: real photographs and the employed-team story
        # come ahead of the service grid, so a first-time visitor sees evidence
        # before another page of benefit copy.
        + render_gallery(page)
        + render_why(page)
        + render_sections(page)
        + render_cta_band(page, page["band1_heading"], page["band1_body"], "quote")
        + render_pricing(page)
        + render_process(page)
        + render_reviews(page)
        + render_areas(page)
        + render_faq(page)
        + render_related(page)
        + render_cta_band(page, page["band2_heading"], page["band2_body"], "book")
        + render_footer(page)
    )
