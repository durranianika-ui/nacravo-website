# Nacravo — SEO Implementation Report

**Site:** https://www.nacravo.com
**Prepared:** 20 July 2026
**Status:** Complete and committed locally. **Nothing has been deployed.**
**Companion files:** `SEO_IMPLEMENTATION_REPORT.xlsx` (data workbook) · `DEPLOYMENT_CHECKLIST.md`

Every figure below is extracted from the built HTML by `build/audit.py`,
`build/audit_final.py`, `build/qa.py` and `build/verify_content.py` at generation time.
Nothing is estimated. Where a number in an earlier version of this report was wrong, the
correction is called out.

---

## 1. Executive Summary

### What exists now

Nacravo went from a one-page marketing site plus a single AC landing page to **eleven
indexable commercial pages** — ten service landing pages and a services hub — built on the
existing design system, sharing one cached stylesheet and one tracking layer.

| Metric | Value |
|---|---|
| Landing pages | 10 (9 new + AC upgraded in place) |
| Sub-service anchor sections | 77 |
| FAQ pairs on landing pages | 77 (86 sitewide) |
| Words of original service copy | 23,452 |
| Structured data blocks | 33 across landing pages + hub |
| Redirects | 15, all 301, no chains or loops |
| Broken links / anchors / images | 0 |
| Orphan pages | 0 |
| Contact details corrected | 227 occurrences |

### Organic strategy

Each landing page owns one head term and its long-tail cluster. Depth is real rather than
padded — **2,016 to 3,608 words per page**, 5–11 sub-service sections targeting the specific
queries people actually type, and 6–23 FAQs answering genuine pre-purchase questions.

### Google Ads strategy

Every page is built for message match: the H1 names the exact service and city, the lead form
sits above the fold, and the searched service arrives already preselected. Anchor traffic goes
further — `/ac-service-dubai#chemical-wash` preselects **both** the service and the sub-service.

### Expected impact — stated honestly

- **Landing Page Experience** should move from a homepage-based baseline to "Above average":
  dedicated relevant pages, text-first rendering, clear CTAs, low-friction mobile forms.
- **Conversion rate** should benefit soonest. The form moved from page bottom to above the
  fold and required fields dropped from 9 to 4.
- **Organic** results will take 3–6 months and depend materially on the off-site work in
  Section 17 — Google Business Profile, reviews, backlinks — **none of which has been started**.

No traffic or ranking figures are projected, because any such number would be invented.

### Two blocking issues remain, neither in site code

1. **Duplicate GA4 tag in the live GTM container** — every lead is counted twice in GA4.
2. **Two button colour combinations fail WCAG AA** — requires a branding decision.

---

## 2. Technical SEO

| Item | Status | Detail |
|---|---|---|
| Indexable pages | 23 | 11 commercial + homepage + 11 legal/utility |
| Canonical | Complete | Unique, absolute, self-referencing, no trailing slash, no `.html` |
| Robots | Complete | `Allow: /`, `Disallow: /thank-you`, sitemap declared |
| XML sitemap | Complete | 23 URLs, each verified to exist on disk at build time |
| HTML sitemap | Complete | Grouped Cleaning / Maintenance / Legal |
| Schema | Complete | Service + BreadcrumbList + FAQPage per landing page |
| Open Graph | Complete | Unique title, description and image per page |
| Twitter Cards | Complete | `summary_large_image` on all pages |
| Breadcrumbs | Complete | Visible trail + BreadcrumbList schema |
| Redirect chains | **None** | Verified programmatically |
| Redirect loops | **None** | Verified programmatically |
| Shadowed redirects | **None** | No redirect source also exists as a real page |
| Trailing slash | Consistent | No internal link ends in `/` |
| Clean URLs | Consistent | No internal link contains `.html` |
| Broken links / anchors | **0** | Every internal link and `#fragment` resolves |
| Broken images | **0** | 34 of 34 referenced files exist |
| Orphan assets | **0** | Every image in `/images` is referenced |
| hreflang | Not applicable | Single locale (en-AE), no alternate language versions |
| Image indexing | Complete | All images have alt, dimensions, srcset, lazy loading |

### Canonical decision — AC page

`/ac-services` was **not** created. `/ac-service-dubai` was upgraded in place to preserve its
indexing history; `/ac-services` 301-redirects to it. Canonical is
`https://www.nacravo.com/ac-service-dubai`.

### Redirect map (15)

| From | To |
|---|---|
| `/ac-services`, `/ac-service` | `/ac-service-dubai` |
| `/sofa-cleaning`, `/carpet-cleaning`, `/mattress-cleaning`, `/curtain-cleaning` | `/specialized-cleaning#<anchor>` |
| `/plumbing`, `/electrical`, `/painting` | `/handyman-services#<anchor>` |
| `/move-in-cleaning`, `/move-out-cleaning` | `/move-in-out-cleaning` |
| `/airbnb-cleaning` | `/holiday-home-cleaning` |
| `/office-cleaning` | `/office-commercial-cleaning` |
| `/amc` | `/annual-maintenance` |
| `/google-ads-reporting` | `/application` (pre-existing) |

---

## 3. On-Page SEO

Full per-page detail is in the **On-Page SEO** sheet of the companion workbook. Summary:

| Page | Words | H2 | H3 | FAQ | Sub-services | Images | Internal links |
|---|---:|---:|---:|---:|---:|---:|---:|
| `/home-cleaning` | 2,420 | 17 | 27 | 6 | 10 | 4 | 22 |
| `/deep-cleaning` | 2,057 | 17 | 22 | 6 | 5 | 4 | 22 |
| `/move-in-out-cleaning` | 2,403 | 17 | 26 | 6 | 9 | 4 | 22 |
| `/holiday-home-cleaning` | 2,121 | 17 | 23 | 6 | 6 | 4 | 22 |
| `/office-commercial-cleaning` | 2,305 | 17 | 26 | 6 | 9 | 4 | 22 |
| `/specialized-cleaning` | 2,016 | 17 | 22 | 6 | 5 | 4 | 22 |
| `/pest-control` | 2,019 | 16 | 23 | 6 | 6 | 1 | 22 |
| `/ac-service-dubai` | 3,608 | 22 | 54 | 23 | 10 | 1 | 22 |
| `/handyman-services` | 2,409 | 17 | 28 | 6 | 11 | 4 | 22 |
| `/annual-maintenance` | 2,087 | 17 | 23 | 6 | 6 | 4 | 22 |
| `/services` (hub) | 939 | 11 | 14 | 3 | — | 0 | 12 |

All landing pages: single H1, no heading-level skips, 100% image ALT coverage, three schema
types, self-referencing canonical, unique title and meta description.

### Correction to the previous report

The previous version stated **89 FAQ pairs**. The verified figure is **77 across the ten
landing pages** (80 including the services hub, 86 including the homepage). The earlier number
was wrong.

---

## 4. Local SEO

### Coverage policy — two different areas, deliberately

- **General cleaning and maintenance** — available across Dubai, subject to availability. Nine
  pages name ten communities: Downtown Dubai, Business Bay, DIFC, Dubai Marina, JLT, Palm
  Jumeirah, JVC, Dubai Hills, Arabian Ranches, Mirdif.
- **AC servicing** — **Downtown Dubai, Business Bay and DIFC only**, matching Ads targeting.

Enforced and verified: the AC page contains **zero** community chips and zero mentions of
Marina, JVC, JLT, Palm Jumeirah, Arabian Ranches or Mirdif. Three of its FAQ answers and its
property-type cards were rewritten because they previously advertised communities outside that
coverage.

### Location signals

`geo.region = AE-DU`, `geo.placename = Dubai`, `og:locale = en_AE` on every page.
`areaServed` is `["Dubai"]` generally and `["Downtown Dubai","Business Bay","DIFC"]` on AC.

Dubai-specific detail is woven into copy where genuinely relevant: sand dust in window tracks,
humidity and mattress drying times, limescale from local water, DEWA/chiller disconnection on
empty properties, month-end tenancy clustering, service-lift booking in towers.

### NAP consistency — verified

| Field | Value | Occurrences |
|---|---|---|
| Name | Nacravo LLC | Consistent sitewide |
| Phone | `+971 55 540 3038` / `tel:+971555403038` / `wa.me/971555403038` | Single value, 24 files |
| Email | `info@nacravo.com` | Single value, 23 files |
| Address | Dubai, United Arab Emirates | Consistent |

Exactly one `tel:` value, one `mailto:` address and one WhatsApp number exist across the entire
site. The old number and the invalid `privacy@nacravo.com` address were replaced in 227 places.

---

## 5. Google Ads Optimisation

### Quality Score factors

**Landing Page Experience**
- Dedicated page per ad group rather than one homepage for all traffic
- Form measured above the fold: bottom at **610px** on a 720px desktop viewport; on mobile
  (375×812) the H1, description, form heading and first two fields are all above the fold
- LCP element is text, not an image
- No interstitials, autoplay or sliders
- Honest about what is and is not offered — no invented prices or guarantees

**Ad Relevance**
- H1 states the exact service and city
- Searched service preselected in the form; anchor traffic also preselects the sub-service
- Sub-service sections mirror ad-group structure, so a "chemical wash" ad can deep-link to
  `#chemical-wash` and land on matching copy with the form pre-filled

**Conversion tracking** — one `generate_lead` event, single-fire, verified against a
double-click. See Section 14 for the live-container defect.

### Remaining PPC friction

| Issue | Impact | Fix |
|---|---|---|
| Conversion value is 0 | Value-based bidding cannot optimise | Push an estimated lead value per service |
| No prices anywhere | Price-sensitive searchers bounce to competitors who show ranges | Supply verified price ranges |
| No reviews or ratings | Weakest trust signal on the page | Collect Google reviews, then mark up |
| Pest control has no imagery | Lowest visual trust of the ten pages | Commission photography |

---

## 6. Landing Page Optimisation

Every landing page follows the same conversion structure:

1. **Above the fold** — H1, short description, four trust badges, WhatsApp + Call buttons, and
   the lead form. Verified at desktop, tablet and mobile.
2. **Hero image** beside the form on desktop, after the form on mobile — added without
   displacing any conversion element (measured).
3. **Jump links** to the most-searched sub-services.
4. **Sub-service sections**, each with its own quote and WhatsApp CTA that preselects that
   sub-service.
5. **Mid-page CTA band** after the sections.
6. **Why Nacravo** — four substantiated differentiators, no invented claims.
7. **Process** — four steps.
8. **Proof gallery** — before/after comparisons, described accurately.
9. **Pricing explainer** — how quoting works, with no invented numbers.
10. **Coverage** — property types plus named communities.
11. **FAQ** — objection handling.
12. **Related services** — four contextual onward paths.
13. **Closing CTA band**, plus sticky mobile bar and desktop floating WhatsApp.

### Form usability

Four required fields (Name, Phone, Service, Location). Email removed entirely. Property type,
date and message are optional behind a disclosure. Inline validation focuses the first invalid
field. Submission hands over to WhatsApp with a structured, pre-filled enquiry.

---

## 7. Internal Linking Analysis

| Layer | Coverage |
|---|---|
| Header dropdown | All 10 services, grouped |
| Mobile menu | All 10, expandable |
| Footer | All 10 in grouped columns, every page |
| Homepage service cards | All 10, direct links |
| Services hub | All 10 + 8 further contextual links in selection guidance |
| Related services | 4 per landing page |
| Contextual in-body | 2–3 per landing page, inside prose |

**In-degree: 11 inbound pages for every landing page and the hub. Zero orphans.** Every page is
within two clicks of the homepage — one via the header dropdown.

### Contextual link map

| From | Links to |
|---|---|
| home-cleaning | deep-cleaning, move-in-out-cleaning, specialized-cleaning#sofa-cleaning |
| deep-cleaning | home-cleaning, specialized-cleaning, move-in-out-cleaning |
| move-in-out-cleaning | deep-cleaning, handyman-services, pest-control |
| holiday-home-cleaning | deep-cleaning, specialized-cleaning, annual-maintenance |
| office-commercial-cleaning | ac-service-dubai, handyman-services, specialized-cleaning#carpet-cleaning |
| specialized-cleaning | deep-cleaning, move-in-out-cleaning, home-cleaning |
| pest-control | deep-cleaning, move-in-out-cleaning, office-commercial-cleaning |
| handyman-services | ac-service-dubai, annual-maintenance, move-in-out-cleaning |
| annual-maintenance | handyman-services, ac-service-dubai, holiday-home-cleaning |
| ac-service-dubai | annual-maintenance, handyman-services, office-commercial-cleaning |

---

## 8. Structured Data Analysis

| Type | Where | Status |
|---|---|---|
| `Service` + `hasOfferCatalog` | 10 landing pages + hub | Valid |
| `BreadcrumbList` | 10 landing pages + hub | Valid, 3 levels |
| `FAQPage` | 10 landing pages + hub + homepage | Valid, 86 entries sitewide |
| `HomeAndConstructionBusiness` | Homepage | Valid |
| `Organization` + `ContactPoint` | Homepage | Valid |
| `WebSite` | Homepage | Valid |

**Validation:** every `application/ld+json` block is parsed on each build. The build fails on a
parse error, a missing `@context`/`@type`, or an empty FAQ answer.

**Deliberately absent:** `AggregateRating`, `Review`, `Offer`/`priceRange`. No verified review
corpus and no published prices exist — emitting these would be fabricated structured data and a
Google policy violation.

---

## 9. Metadata Summary

All titles 51–59 chars; all descriptions 152–157 chars. Uniqueness enforced across all 23 pages.
Full table in the **Metadata** sheet of the workbook.

---

## 10. Keyword Targeting

| Page | Primary keyword | Intent |
|---|---|---|
| `/home-cleaning` | home cleaning Dubai | Commercial, recurring |
| `/deep-cleaning` | deep cleaning Dubai | Commercial, one-off |
| `/move-in-out-cleaning` | move out cleaning Dubai | Transactional, deadline-driven |
| `/holiday-home-cleaning` | holiday home cleaning Dubai | Commercial, B2B recurring |
| `/office-commercial-cleaning` | office cleaning Dubai | B2B contract |
| `/specialized-cleaning` | sofa cleaning Dubai | Commercial, item-level |
| `/pest-control` | pest control Dubai | Urgent problem-solving |
| `/ac-service-dubai` | AC service Dubai | Commercial + urgent |
| `/handyman-services` | handyman Dubai | Task-specific |
| `/annual-maintenance` | annual maintenance contract Dubai | B2B / landlord |

**Cannibalization review:** overlap analysis found shared terms only in generic CTA words
(`book`, `quote`) and the category noun `cleaning`, which legitimately appears in every cleaning
service's name. `home cleaning` (recurring), `deep cleaning` (one-off reset) and `holiday home
cleaning` (B2B turnover) are separate markets with separate intent. **No action needed.** The
hub is positioned as a navigational parent and competes for no head term.

---

## 11. Search Intent Coverage

| Intent type | Covered by | Gap |
|---|---|---|
| Transactional / urgent | pest-control, ac-service-dubai, move-in-out-cleaning | — |
| Commercial recurring | home-cleaning, holiday-home-cleaning, annual-maintenance | — |
| Commercial one-off | deep-cleaning, specialized-cleaning | — |
| B2B contract | office-commercial-cleaning, annual-maintenance | — |
| Comparison / decision | services hub "Which service do you need?", AC maintenance-vs-chemical-wash | — |
| **Informational / upper funnel** | Partially, via FAQs | **Yes — no blog** |

The landing pages deliberately own commercial intent. Informational queries ("how often should
AC be serviced", "how to prepare for bed bug treatment") are only partially served by FAQ
answers. A small blog cluster is the recommended fix (Section 17).

---

## 12. Accessibility

Contrast was **computed, not assumed** — the previous report explicitly declined to claim AA
compliance, and that caution was justified: **nine combinations failed.**

### Fixed (7)

| Element | Before | After | Change |
|---|---|---|---|
| Eyebrow / kicker text | 3.11:1 | **5.03:1** | `--sage-text #5E6C4F` introduced for text |
| Sage links on white | 3.47:1 | **5.62:1** | same token |
| Fine print on pearl | 3.16:1 | **4.75:1** | `--stone` darkened to `#6F6B63` |
| Fine print on white | 3.53:1 | **5.30:1** | same |
| Form error text | 4.12:1 | **4.98:1** | `#C0574B` → `#B04A3E` |
| Footer strapline | 3.87:1 | **4.73:1** | `#8A9380` → `#9AA391` |
| TOC / step numbers | 3.11:1 | **5.03:1** | `--sage-text` |

Brand surfaces were not touched. Sage remains unchanged where it is decorative (icons,
checkmarks, borders, focus rings) — those are non-text UI components and pass the 3:1 threshold
of WCAG 1.4.11 at 3.11:1.

### Not fixed — requires a branding decision (2)

| Element | Ratio | Required | Why not auto-fixed |
|---|---|---|---|
| Primary button label (pearl on sage) | **3.11:1** | 4.5:1 | Sage is a mid-tone: it fails with light labels **and** with dark ones until the label is nearly black (`#1F2419`, 4.57:1). The only clean fix is darkening the button itself to `#5F6E53` (4.89:1), which changes the brand's main CTA colour. The brief forbids changing branding. |
| WhatsApp button label (white on `#25D366`) | **1.98:1** | 4.5:1 | `#25D366` is WhatsApp's official brand green with white text — the universally recognised pairing. Reaching 4.5:1 needs `#0B7A3B` (5.44:1), which no longer reads as WhatsApp. |

**This is a decision for the brand owner, not an engineering choice.** Both options and exact
ratios are supplied so the trade-off can be made deliberately.

### Other accessibility work

Keyboard reachable throughout, Escape closes the dropdown, 3px `:focus-visible` outline added
sitewide, every form control labelled, `aria-expanded` / `aria-label` / `aria-live` /
`aria-hidden` used correctly, `<main>` / `<header>` / `<footer>` / `<nav aria-label>` landmarks,
skip link on every page, no heading-level skips, no touch target under 44px, 100% ALT coverage,
`prefers-reduced-motion` respected.

---

## 13. Performance

| Change | Effect |
|---|---|
| Shared CSS (29.4 KB) | Cached once, reused across 11 pages, replacing 11 inline copies |
| Shared JS (19.3 KB) | Cached once; AC page's duplicate inline tracker removed |
| AC page JavaScript | **Zero** — slider removed entirely |
| No hero image above the fold | LCP element is text on all 10 landing pages |
| All images lazy-loaded | Below-fold galleries deferred |
| Real intrinsic dimensions | Read from JPEG headers at build time |
| CSS de-duplication bug | Fixed — extractor was re-appending a block it had already read back |

**DOM size:** 618–1,030 elements per landing page, well within budget.
**Render-blocking:** 2 stylesheets per landing page (shared + fonts); 3 on the AC page (plus its
page-scoped CSS).

### Core Web Vitals

- **LCP** — text-first heroes, fonts preconnected with `display=swap`
- **CLS** — every `<img>` carries real width/height; hero media box is ratio-locked. A latent
  bug was caught here: `ba-bathroom` is 1080×864 (5:4) while the rest of the set is 3:2, so
  dimensions are read per file rather than hardcoded
- **INP** — minimal JS, no frameworks, no polling

**No field data exists** (no CrUX history for these URLs). These are architectural improvements,
not measured Lighthouse scores. Run Lighthouse post-deploy for real numbers.

---

## 14. Analytics

### Site-side — correct

One `generate_lead` push with `eventCallback` and a timeout backstop, a `leadSent` one-shot
guard, and a `DEDUP_MS` guard on delegated clicks. **Verified in-browser: a double-clicked
submit produces exactly one `generate_lead`**, with correct `service_name`, `subservice_name`,
`property_type` and `location`. An invalid submit pushes nothing.

Events: `page_view`, `generate_lead`, `form_submit`, `quote_click`, `booking_click`,
`cta_click`, `service_view`, `whatsapp_click`, `phone_click`, `outbound_click`.

### Live GTM container audit — GTM-KD4PH4XP

The repository's `gtm-nacravo-container.json` shows 3 tags. **The live container has 18.** It
was fetched and parsed directly.

| Finding | Severity | Detail |
|---|---|---|
| **Built-in trigger double-counting** | **Resolved — not an issue** | All 12 trigger predicates are custom-event equality checks. **No** `gtm.formSubmit`, `gtm.linkClick` or `gtm.historyChange` trigger fires any tag. The built-in listeners push to dataLayer but nothing consumes them. This closes the open question raised in the previous report. |
| **Duplicate GA4 `generate_lead` tag** | **P1 — Blocking** | Tag 25 **and** tag 48 are both GA4 Event tags named `generate_lead`, both sending to `G-N2VGBEBELF`, both firing on the same trigger. **Every lead is counted twice in GA4.** |
| Google Ads conversion | Correct | Exactly one `__awct` tag (id 49), conversion ID `18246691744`, label `J2SlCMja0M0cEKDX2fxD`, firing on `generate_lead` only. **Ads conversions are not duplicated.** |
| Conversion value is zero | P2 | The tag reads `{{value}}`; the site pushes `value: 0`. Value-based bidding cannot optimise. |
| Six paused tags | Informational | Left over from earlier iterations; harmless but clutter the container. |

### Correction to the previous report

The previous version recommended filling in `GOOGLE_ADS_ID` in `NACRAVO_TRACKING`. **That
recommendation was wrong.** `LOAD_PIXELS_DIRECTLY` is `false`, so the site never loads Google
Ads directly — the conversion is wired in GTM and works. Filling that field in while GTM also
fires the conversion **would create duplicate Ads conversions**. Leave it empty.

---

## 15. Conversion Optimisation

| Element | Implementation |
|---|---|
| Form position | Above the fold, desktop and mobile — measured |
| Form friction | 4 required fields; email removed |
| Service preselection | Per page, plus sub-service from anchor |
| CTA routes | Form, WhatsApp, phone — all three on every page |
| CTA frequency | Hero, per sub-service section, mid-page band, closing band, sticky bar, floating button |
| Trust signals | 4 badges above the fold; employed/vetted team, fixed price, photo report, materials included |
| Objection handling | Pricing explainer, process steps, 6–23 FAQs per page |
| Mobile | Sticky call/WhatsApp bar; floating button suppressed to avoid overlap |
| Guarantees | **Only verified ones.** Honest negative statements retained ("we do not offer a guaranteed response time") |

---

## 16. Content Quality

- 23,452 words of original service copy across 10 landing pages
- 77 sub-service sections; 77 FAQ pairs on landing pages
- Dubai-specific and concrete rather than generic

### Integrity enforcement

`build/verify_content.py` fails the build on any invented price, percentage, years-in-business
claim, customer count, star rating, review count, certification, award, guarantee, warranty,
"24/7" claim or superlative. It is negation-aware, so honest disclaimers pass while the claims
themselves cannot.

**Removed:** five unverified named testimonials from the AC page, replaced with a trust section
making no customer-quote claims.

### Imagery integrity

All seven `ba-*` files are **before/after composites** with labels baked in — verified by
opening each one. Consequences handled:

- Alt text rewritten to describe them as comparisons, not single after-photos
- The AC page's simulated "drag to compare" slider was **removed**: it loaded the same file as
  both layers and faked the "before" with a CSS grayscale filter, which misrepresents evidence
- No page shows the same image twice
- Pest control and the AC hero have **no honest asset** — documented placeholders, never
  borrowed imagery

**Known limitation:** `ba-living` and `ba-bathroom` each appear on 6 pages. Only 7 composites
exist for 6 gallery pages, so cross-page reuse is unavoidable until more photography exists.

---

## 17. Remaining Recommendations

Ranked. Full detail in the **Recommendations** sheet of the workbook.

### P1 — Blocking

1. **Fix the duplicate GA4 `generate_lead` tag.** Pause or delete one of tags 25/48 in GTM.
   *Owner: GTM admin · 15 minutes · No code change.*
2. **Decide on button contrast.** Darken the primary button to `#5F6E53` (4.89:1) and accept a
   deeper green, or accept the risk and document it. *Owner: brand owner · 1 hour.*

### P2 — High

3. Commission pest control photography.
4. Commission AC service photography (technician servicing an indoor unit, chemical wash).
5. Set a conversion value so value-based bidding can work.
6. Google Business Profile alignment — highest-leverage local item not in this repo.

### P3 — Medium

7. Review collection programme, then add genuine `AggregateRating`.
8. 6–8 more before/after pairs so each page carries a distinct set.
9. Run Lighthouse post-deploy for real Core Web Vitals.
10. Publish trade licence and VAT TRN (currently placeholder comments).

### P4 — Later

11. Blog for informational intent.
12. Per-community landing pages — only where booking volume justifies it.
13. Backlink acquisition via property managers and holiday-home operators.

---

## 18. Technical Debt

| Item | Risk | Note |
|---|---|---|
| Generated pages are build artefacts | Medium | Hand edits to the 11 generated `.html` files are destroyed on the next build. Documented in every file's generator docstring and in `MEMORY.md`. |
| `gtm-nacravo-container.json` is stale | Medium | Repo copy shows 3 tags; live container has 18. Re-export or delete it to avoid misleading future audits. |
| Legal pages hand-maintained | Low | Not generated; their inline CSS is a separate copy of the design tokens. |
| `index.html` dual-maintained | Low | Keeps inline CSS for LCP; the shared block is kept in sync via a managed marker region. |
| Six paused GTM tags | Low | Clutter; review and delete if obsolete. |
| Cross-page image reuse | Low | Cosmetic and SEO-dilutive, not incorrect. Blocked on photography. |
| No automated CI | Medium | `qa.py`, `verify_content.py` and `audit_final.py` must be run manually before deploy. |

---

## 19. Future Roadmap

**0–1 month** — Clear the two P1 blockers. Deploy. Submit sitemap in Search Console. Set up
Google Business Profile. Start review collection. Run Lighthouse.

**1–3 months** — Commission pest control and AC photography. Add conversion values. Monitor
Search Console for query/page mismatches and refine metadata. Begin backlink outreach.

**3–6 months** — Add review schema once a genuine corpus exists. Publish the first blog
cluster. Evaluate per-community pages using real booking data.

**6–12 months** — Expand community pages where justified. Consider Arabic localisation
(would introduce a real `hreflang` requirement). Revisit pricing transparency.

---

## 20. Final Production Readiness

| Dimension | Weight | Score | Basis |
|---|---:|---:|---|
| Technical SEO | 20% | 10/10 | Zero broken links, anchors, chains, loops; metadata unique |
| On-page SEO | 15% | 10/10 | 10 distinct clusters, 2,000+ words each, no cannibalization |
| Structured data | 10% | 9/10 | 3 types per page, all valid; rating/price blocked on business inputs |
| Internal linking | 10% | 10/10 | Zero orphans, contextual + navigational layers |
| Conversion / Ads | 15% | 8/10 | Form above fold verified; conversion value still 0 |
| Analytics | 10% | 6/10 | Site-side correct; live GTM has a duplicate GA4 tag |
| Accessibility | 10% | 8/10 | 7 of 9 contrast failures fixed; 2 need a brand decision |
| Performance | 5% | 9/10 | Text LCP, shared cached assets, zero JS on AC page; no field data |
| Content quality | 5% | 9/10 | Original, specific, no fabricated claims; photography gaps |

### **Overall: 89 / 100**

**Recommendation: safe to deploy, with the two blockers tracked.**

Neither blocker lives in site code. The duplicate GA4 tag is a GTM console change that can be
made before or immediately after deploy; it inflates GA4 reporting but does **not** affect
Google Ads conversions or user experience. The button contrast is a genuine WCAG AA failure that
should be decided deliberately rather than silently — until it is, the site should not be
described as WCAG AA compliant.

### Deployment status

**Nothing has been deployed.** No push, no DNS change, no production configuration altered, no
analytics IDs changed. All work is committed locally on `main`.
