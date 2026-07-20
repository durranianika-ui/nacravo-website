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
PHONE_DISPLAY = "+971 58 108 2601"
PHONE_TEL = "+971581082601"
WA_NUMBER = "971581082601"
EMAIL = "info@nacravo.com"
GTM_ID = "GTM-KD4PH4XP"

# Navigation is defined once and rendered into every page's desktop dropdown,
# mobile menu and footer, so the three can never disagree.
NAV_CLEANING = [
    ("Home Cleaning", "/home-cleaning"),
    ("Deep Cleaning", "/deep-cleaning"),
    ("Move In / Move Out", "/move-in-out-cleaning"),
    ("Holiday Home Cleaning", "/holiday-home-cleaning"),
    ("Office &amp; Commercial", "/office-commercial-cleaning"),
    ("Specialized Cleaning", "/specialized-cleaning"),
    ("Pest Control", "/pest-control"),
]
NAV_MAINTENANCE = [
    ("AC Services", "/ac-service-dubai"),
    ("Handyman Services", "/handyman-services"),
    ("Annual Maintenance", "/annual-maintenance"),
]


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
        <div class="drop-panel" id="svcDrop">
          <div class="drop-col"><div class="drop-h">Cleaning</div>{links(NAV_CLEANING)}</div>
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
      <a href="{wa}" target="_blank" rel="noopener" class="btn btn-primary nav-wa" aria-label="Book on WhatsApp">{WA_ICON.format(s=17)}<span class="lbl-full">Book on WhatsApp</span><span class="lbl-short">WhatsApp</span></a>
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
    """Copy on the left, lead form on the right. No decorative hero image, so the
    form is visible without scrolling and the LCP element is text."""
    trust = "".join(trust_pill(i, l) for i, l in page["trust"])
    wa = wa_link(page["wa_text"])

    sub_options = ""
    if page.get("subservices"):
        opts = "".join(f"<option>{esc(v)}</option>" for v in page["subservices"].values())
        sub_options = f"""
          <div class="field full">
            <label for="subservice">Which specific service?</label>
            <select id="subservice" name="subservice">
              <option value="">No preference / not sure</option>
              {opts}
            </select>
          </div>"""

    # Hero image: sits below the copy in the left column so it appears beside
    # the form on desktop without displacing it, and after the form on mobile.
    # loading="lazy" is safe here — browsers fetch in-viewport lazy images
    # immediately — and the LCP element on these pages is the H1 text, not an image.
    media = ""
    if page.get("hero_image"):
        big, small, alt = page["hero_image"]
        bw, bh = image_size(big)
        sw, _ = image_size(small)
        media = f"""
      <div class="lp-hero-media">
        <img src="images/{big}" srcset="images/{small} {sw}w, images/{big} {bw}w"
             sizes="(max-width:900px) 92vw, 420px" alt="{esc(alt)}"
             width="{bw}" height="{bh}" loading="lazy" decoding="async">
      </div>"""

    jump = ""
    if page.get("jump_links"):
        items = "".join(f'<a href="#{a}">{esc(t)}</a>' for t, a in page["jump_links"])
        jump = f'<div class="wrap" style="padding-bottom:8px"><div class="jump">{items}</div></div>'

    return f"""
<main id="main">
<section class="lp-hero">
  <div class="wrap lp-hero-grid">
    <div class="lp-hero-copy">
      <div class="lp-hero-head">
        <span class="eyebrow">{esc(page['eyebrow'])}</span>
        <h1>{esc(page['h1'])}</h1>
        <p class="lead">{esc(page['lead'])}</p>
      </div>
      <div class="lp-hero-rest">
        <div class="trust">{trust}</div>
        <div class="lp-hero-cta">
          <a href="{wa}" target="_blank" rel="noopener" class="btn btn-wa" data-track="booking" data-service-name="{esc(page['service_value'])}" data-track-label="Hero: WhatsApp">{WA_ICON.format(s=18)} WhatsApp us</a>
          <a href="tel:{PHONE_TEL}" class="btn btn-ghost">{PHONE_ICON} Call now</a>
        </div>
      </div>{media}
    </div>

    <div class="lp-form-wrap">
      <form class="lp-form" id="leadForm" novalidate aria-labelledby="leadFormTitle">
        <h2 id="leadFormTitle">Get a free quote</h2>
        <p class="lp-form-sub">Tell us what you need — we reply on WhatsApp with a fixed price.</p>

        <div class="form-row">
          <div class="field">
            <label for="name">Name <span class="req" aria-hidden="true">*</span></label>
            <input type="text" id="name" name="name" placeholder="Your name" autocomplete="name" required>
            <span class="err-msg">Please enter your name.</span>
          </div>
          <div class="field">
            <label for="phone">Phone <span class="req" aria-hidden="true">*</span></label>
            <input type="tel" id="phone" name="phone" placeholder="+971…" autocomplete="tel" required>
            <span class="err-msg">Please enter a valid phone number.</span>
          </div>
        </div>

        <div class="form-row">
          <div class="field">
            <label for="service">Service <span class="req" aria-hidden="true">*</span></label>
            <select id="service" name="service" required>
              <option value="{esc(page['service_value'])}" selected>{esc(page['service_value'])}</option>
            </select>
            <span class="err-msg">Please choose a service.</span>
          </div>
          <div class="field">
            <label for="location">Location <span class="req" aria-hidden="true">*</span></label>
            <input type="text" id="location" name="location" placeholder="e.g. Business Bay" autocomplete="address-level2" required>
            <span class="err-msg">Please enter your location.</span>
          </div>
        </div>

        <div class="form-row">{sub_options}
        </div>

        <details class="lp-extra">
          <summary class="lp-more">Add property type, date or a note (optional)</summary>
          <div class="lp-optional">
            <div class="form-row">
              <div class="field">
                <label for="property">Property type</label>
                <select id="property" name="property">
                  <option value="">Select…</option>
                  <option>Apartment</option>
                  <option>Villa</option>
                  <option>Townhouse</option>
                  <option>Office</option>
                  <option>Retail</option>
                  <option>Other</option>
                </select>
              </div>
              <div class="field">
                <label for="date">Preferred date</label>
                <input type="date" id="date" name="date">
              </div>
            </div>
            <div class="form-row">
              <div class="field full">
                <label for="notes">Message</label>
                <textarea id="notes" name="notes" rows="3" placeholder="Anything we should know?"></textarea>
              </div>
            </div>
          </div>
        </details>

        <button type="submit" class="btn btn-wa" style="width:100%;justify-content:center">{WA_ICON.format(s=18)} Get my free quote →</button>
        <div class="form-status" id="leadStatus" role="status" aria-live="polite">Opening WhatsApp with your enquiry…</div>
        <p class="lp-fineprint">We use your details only to respond to this enquiry. See our <a href="/privacy-policy">Privacy Policy</a>.</p>
      </form>
    </div>
  </div>
</section>
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
          <a href="#leadFormTitle" class="btn btn-primary" data-subservice="{s['anchor']}" data-track="quote" data-track-label="{esc(s['title'])}: Get a quote">Get a quote</a>
          <a href="{wa}" target="_blank" rel="noopener" class="btn btn-ghost" data-track="booking" data-service-name="{esc(page['service_value'])}" data-track-label="{esc(s['title'])}: WhatsApp">WhatsApp</a>
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
        <a href="{quote_href}" class="btn btn-primary" data-track="quote" data-track-label="Mid-page: Get a quote">Get a quote</a>
        <a href="tel:{PHONE_TEL}" class="btn btn-ghost">Call now</a>
        <a href="{wa}" target="_blank" rel="noopener" class="btn btn-wa" data-track="booking" data-service-name="{esc(page['service_value'])}" data-track-label="Mid-page: WhatsApp">WhatsApp</a>
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
        w, h = image_size(big)
        sw, _ = image_size(small)
        cells.append(f"""
      <figure class="gal-cell">
        <img src="images/{big}" srcset="images/{small} {sw}w, images/{big} {w}w"
             sizes="(max-width:480px) 92vw,(max-width:760px) 46vw,360px" alt="{esc(alt)}"
             width="{w}" height="{h}" loading="lazy" decoding="async">
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
        {links(NAV_MAINTENANCE)}
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
<div class="mbar">
  <a href="tel:{PHONE_TEL}" class="call">{PHONE_ICON} Call</a>
  <a href="{wa}" target="_blank" rel="noopener" class="wa">{WA_ICON.format(s=16)} WhatsApp</a>
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
<script src="/assets/nacravo.js" defer></script>
</body>
</html>
"""


def render_page(page):
    return (
        render_head(page)
        + render_header(page)
        + render_hero(page)
        + render_sections(page)
        + render_cta_band(page, page["band1_heading"], page["band1_body"], "quote")
        + render_why(page)
        + render_process(page)
        + render_gallery(page)
        + render_pricing(page)
        + render_areas(page)
        + render_faq(page)
        + render_related(page)
        + render_cta_band(page, page["band2_heading"], page["band2_body"], "book")
        + render_footer(page)
    )
