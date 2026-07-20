# Nacravo — SEO Implementation Report

**Site:** https://www.nacravo.com
**Prepared:** 20 July 2026
**Status:** Complete and committed locally. **Nothing has been deployed.**

All figures in this report were measured from the built files by `build/audit.py`,
`build/qa.py` and `build/verify_content.py`. Nothing is estimated.

---

## 1. Executive Summary

### What was done

Nacravo previously had a single-page marketing site plus one AC landing page. It now
has **eleven indexable commercial pages** — ten service landing pages and a services
hub — built on the existing design system, sharing one cached stylesheet and one
tracking layer.

The work covered two distinct objectives: making the site rank for the service terms
Dubai customers actually search, and making each page convert paid traffic well enough
to earn a strong Google Ads Quality Score.

### Organic strategy

Each landing page owns one head term and its long-tail cluster (`home cleaning Dubai`,
`deep cleaning Dubai`, `move out cleaning Dubai`, and so on). Depth is real, not padded:
**2,016–3,608 words per page**, each with 5–11 sub-service sections that target the
specific queries people type (`AC chemical wash`, `end of tenancy cleaning`,
`bed bug treatment`), and 6–23 FAQs answering genuine pre-purchase questions.

Every page carries Service, BreadcrumbList and FAQPage structured data. Internal
linking is deliberately layered — navigation, footer, related-services grid, and a
contextual in-body paragraph that links to two or three genuinely related siblings.

### Google Ads strategy

Every landing page is built for message match. The visitor lands on a page whose H1
names the exact service they searched, sees a lead form above the fold, and finds the
service already preselected in that form. Anchor traffic goes further: a click on
`/ac-service-dubai#chemical-wash` arrives with **both** the service and the sub-service
preselected.

### Expected impact

Honest framing: this is foundational work, and outcomes depend on budget, competition
and business follow-through.

- **Landing Page Experience** should move from a homepage-based baseline (where all ad
  traffic hit one generic page) to "Above average" — relevant dedicated pages, fast
  text-first rendering, clear CTAs, mobile-optimised forms.
- **Organic** gains will be gradual. Eleven new pages need crawling, indexing and
  maturing; meaningful movement typically takes 3–6 months, and depends heavily on the
  backlink and Google Business Profile work listed in Section 12, which is **not** done.
- **Conversion rate** should benefit most immediately: the form moved from the page
  bottom to above the fold, with friction cut from 9 fields to 4 required.

No traffic or ranking numbers are projected here, because any such figure would be
invented.

---

## 2. Technical SEO

| Item | Status | Detail |
|---|---|---|
| Indexable pages | 23 | 11 commercial + homepage + 11 legal/utility |
| Canonical | Complete | Unique self-referencing canonical on every page |
| Robots | Complete | `Allow: /`, `Disallow: /thank-you`, sitemap declared |
| XML sitemap | Complete | 23 URLs, each verified to exist on disk at build time |
| HTML sitemap | Complete | `/sitemap` grouped by Cleaning / Maintenance / Legal |
| Schema | Complete | Service + BreadcrumbList + FAQPage per landing page |
| Open Graph | Complete | Unique title, description and image per page |
| Twitter Cards | Complete | `summary_large_image` on all pages |
| Breadcrumbs | Complete | Visible trail + BreadcrumbList schema |
| Redirects | 15 | All verified returning 301 |
| Heading hierarchy | Fixed | No skipped levels on any page (was h2→h4 on all 12) |
| Duplicate metadata | None | Enforced across all 23 pages by `build/qa.py` |
| Broken links | None | Every internal link and `#anchor` resolved at build time |

### Canonical decision — AC page

`/ac-services` was **not** created. The existing `/ac-service-dubai` was upgraded in
place to preserve its indexing history, and `/ac-services` 301-redirects to it. Canonical
is `https://www.nacravo.com/ac-service-dubai`.

### Redirect map

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

Measured per page:

| Page | Words | H2 | H3 | FAQ | Sub-services | Images | Internal links |
|---|---:|---:|---:|---:|---:|---:|---:|
| `/home-cleaning` | 2,420 | 17 | 27 | 6 | 10 | 4 | 22 |
| `/deep-cleaning` | 2,057 | 17 | 22 | 6 | 5 | 4 | 22 |
| `/move-in-out-cleaning` | 2,403 | 17 | 26 | 6 | 9 | 4 | 22 |
| `/holiday-home-cleaning` | 2,121 | 17 | 23 | 6 | 6 | 4 | 22 |
| `/office-commercial-cleaning` | 2,305 | 17 | 26 | 6 | 9 | 4 | 22 |
| `/specialized-cleaning` | 2,016 | 17 | 22 | 6 | 5 | 4 | 22 |
| `/pest-control` | 2,019 | 16 | 23 | 6 | 6 | 1 | 22 |
| `/ac-service-dubai` | 3,608 | 22 | 54 | 23 | 10 | 2 | 22 |
| `/handyman-services` | 2,409 | 17 | 28 | 6 | 11 | 4 | 22 |
| `/annual-maintenance` | 2,087 | 17 | 23 | 6 | 6 | 4 | 22 |
| `/services` (hub) | 939 | 11 | 14 | 3 | — | 0 | 12 |

All pages: single H1, no heading skips, 100% image ALT coverage, Service + Breadcrumb +
FAQ schema, self-referencing canonical, unique title and meta description.

### Keyword clusters and search intent

| Page | Primary keyword | Secondary cluster | Intent |
|---|---|---|---|
| `/home-cleaning` | home cleaning Dubai | regular/weekly/monthly/hourly cleaning, apartment, villa, townhouse, maid service | Commercial, recurring |
| `/deep-cleaning` | deep cleaning Dubai | apartment/villa/kitchen/bathroom deep clean, post-construction | Commercial, one-off |
| `/move-in-out-cleaning` | move out cleaning Dubai | move in cleaning, end of tenancy, empty property, oven/fridge/balcony | Transactional, deadline-driven |
| `/holiday-home-cleaning` | holiday home cleaning Dubai | Airbnb cleaning, turnover, linen, restocking, mid-stay | Commercial, B2B recurring |
| `/office-commercial-cleaning` | office cleaning Dubai | commercial cleaning, daily contracts, carpet shampoo, fit-out, post-event | B2B contract |
| `/specialized-cleaning` | sofa cleaning Dubai | carpet, mattress, curtain, interior window cleaning | Commercial, item-level |
| `/pest-control` | pest control Dubai | cockroach, bed bugs, ants, rodents, residential, commercial | Urgent problem-solving |
| `/ac-service-dubai` | AC service Dubai | chemical wash, duct cleaning, repair, installation, gas top up, split/window | Commercial + urgent |
| `/handyman-services` | handyman Dubai | plumbing, electrical, painting, TV mounting, furniture assembly, locks | Task-specific |
| `/annual-maintenance` | annual maintenance contract Dubai | AMC apartment/villa, preventive maintenance, MEP inspection | B2B / landlord |

**Cannibalization review:** overlap analysis found shared terms only in generic CTA
words (`book`, `quote`) and the category noun `cleaning`, which legitimately appears in
every cleaning service's name. Each page owns a distinct head term with distinct intent
— `home cleaning` (recurring) vs `deep cleaning` (one-off reset) vs `holiday home
cleaning` (B2B turnover) are separate markets, not competing pages. **No action needed.**
The `/services` hub is positioned as a navigational parent and does not compete for any
head term.

---

## 4. Local SEO

### Coverage policy

Two different service areas are stated, because they are genuinely different:

- **General cleaning and maintenance** — available across Dubai, subject to
  availability. Nine pages name communities: Downtown Dubai, Business Bay, DIFC, Dubai
  Marina, JLT, Palm Jumeirah, JVC, Dubai Hills, Arabian Ranches, Mirdif.
- **AC servicing** — currently focused on **Downtown Dubai, Business Bay and DIFC
  only**, matching Ads targeting.

This distinction is enforced in the build: the AC page carries **zero** community chips
and zero mentions of Marina, JVC, JLT, Palm Jumeirah, Arabian Ranches or Mirdif. Three
of its FAQ answers and its property-type cards were rewritten during this work because
they previously advertised communities outside that coverage.

### Location signals

- `geo.region` = `AE-DU`, `geo.placename` = `Dubai` on every page
- `areaServed` in Service schema — `["Dubai"]` generally, `["Downtown Dubai","Business Bay","DIFC"]` on AC
- `og:locale` = `en_AE`
- Dubai-specific content woven into copy where genuinely relevant: sand dust in window
  tracks, humidity and mattress drying, limescale from local water, DEWA/chiller
  disconnection on empty properties, month-end tenancy clustering, service-lift booking
  in towers

### NAP consistency

| Field | Value | Occurrences |
|---|---|---|
| Name | Nacravo LLC | Consistent sitewide |
| Phone | +971 58 108 2601 / `tel:+971581082601` / `wa.me/971581082601` | 24 files |
| Email | info@nacravo.com | 23 files |
| Address | Dubai, United Arab Emirates | Consistent |

The previous number (`+971556365807`) and the invalid `privacy@nacravo.com` address
were replaced in **227 places**; QA fails the build if either reappears.

---

## 5. Google Ads Landing Page Optimisation

### Quality Score factors

**Landing Page Experience**
- Dedicated page per ad group instead of one homepage for all traffic
- Lead form above the fold on desktop *and* mobile — measured: form bottom at 610px on a
  720px desktop viewport; on mobile the heading, description, form heading and first two
  fields all sit above an 812px fold
- Text-first hero — the LCP element is the H1, not an image
- No interstitials, no autoplay, no sliders
- Transparent about what is and isn't offered (no invented prices or guarantees)

**Ad Relevance / message match**
- H1 states the exact service and city
- The searched service is preselected in the form; anchor traffic also preselects the
  sub-service
- Sub-service sections mirror ad-group structure, so a "chemical wash" ad can deep-link
  to `#chemical-wash`

**Expected CTR** is driven by ad copy rather than landing pages, but unique,
benefit-led title tags and meta descriptions were written for each page to support
organic CTR.

### Conversion flow and lead capture

- Required fields cut to four: Name, Phone, Service, Location. Email removed entirely.
- Property type, preferred date and message are optional behind a disclosure
- Three CTA routes on every page: form (primary), WhatsApp, phone
- CTAs repeat after key sections via mid-page bands, plus a closing band
- Sticky mobile call/WhatsApp bar; desktop floating WhatsApp button
- Submission hands over to WhatsApp with a structured, pre-filled enquiry

### Objection handling

Each page addresses the objections that actually block booking: what's included, how
pricing works, who enters your home, what happens if the work is wrong, and — on AC and
pest control — honest statements about what is *not* offered (no round-the-clock cover,
no guaranteed response time, no licence claims).

---

## 6. Internal Linking Report

### Link architecture

| Layer | Coverage |
|---|---|
| Header dropdown | All 10 services, grouped Cleaning / Maintenance |
| Mobile menu | Same 10, expandable |
| Footer | All 10 in grouped columns on every page |
| Homepage service cards | All 10, direct links (no generic text) |
| Services hub | All 10 + selection guidance with 8 more contextual links |
| Related services | 4 per landing page |
| **Contextual in-body** | **2–3 per landing page, inside prose** |

### In-degree (measured)

Every landing page and the hub receive inbound links from **11 other pages**.
**Zero orphan pages.** Every page is within two clicks of the homepage — one via the
header dropdown.

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

## 7. Structured Data Report

| Schema type | Where | Status |
|---|---|---|
| `Service` + `hasOfferCatalog` | 10 landing pages + hub | Valid, parses |
| `BreadcrumbList` | 10 landing pages + hub | Valid, 3 levels |
| `FAQPage` | 10 landing pages + hub | Valid, 89 Q&A pairs total |
| `HomeAndConstructionBusiness` | Homepage | Valid |
| `Organization` + `ContactPoint` | Homepage | Valid |
| `WebSite` | Homepage | Valid |

**Validation:** every `application/ld+json` block is parsed by `build/qa.py` on each
build; the build fails on a parse error, a missing `@context`/`@type`, or an empty FAQ
answer. All blocks currently pass.

**Deliberately not implemented:** `AggregateRating`, `Review` and `Offer`/`priceRange`
at service level. Nacravo has no verified review corpus and no published prices —
emitting these would be fabricated structured data and a Google policy violation.

---

## 8. Performance Report

### Architecture changes

| Change | Effect |
|---|---|
| CSS extracted to one shared file | 27.9 KB cached once, reused across 11 pages, replacing 11 inline copies |
| JS consolidated to one shared file | 19.3 KB cached once; AC page's duplicate inline tracker removed |
| AC page JavaScript | **Reduced to zero** — slider removed, no remaining page JS |
| No hero images | LCP element is text on all 10 landing pages |
| All images lazy-loaded | Below-fold galleries deferred |
| Explicit width/height on every image | Dimensions read from real JPEG headers at build time |

### Core Web Vitals

- **LCP** — text-first heroes. No render-blocking image above the fold. Fonts preconnected
  with `display=swap`.
- **CLS** — every `<img>` carries real intrinsic width/height, and the hero media box is
  ratio-locked. A latent bug was caught here: `ba-bathroom` is 1080×864 (5:4) while the
  rest of the set is 3:2, so dimensions are now read per file rather than hardcoded.
- **INP** — minimal JavaScript. No frameworks, no libraries, no polling. Interactions are
  a nav toggle, `<details>` disclosures, and one form handler.

Field data is not available (no CrUX history for these URLs yet). These are architectural
improvements, not measured Lighthouse scores — run Lighthouse post-deploy for real numbers.

---

## 9. Accessibility Report

| WCAG area | Implementation |
|---|---|
| Keyboard | All interactive elements reachable; Escape closes the dropdown |
| Focus | Visible 3px `:focus-visible` outline added sitewide (base site relied on UA default) |
| Labels | Every form control has a `<label for>`; enforced by QA |
| ARIA | `aria-expanded` on nav toggles, `aria-label` on icon buttons, `role="status"` + `aria-live` on form feedback, `aria-hidden` on decorative SVG |
| Landmarks | `<main id="main">`, `<header>`, `<footer>`, `<nav aria-label>` |
| Skip link | "Skip to main content" on every page |
| Heading hierarchy | **Fixed** — no skipped levels on any page |
| Touch targets | No target under 44px measured at 375px |
| Images | 100% ALT coverage; decorative SVG hidden from AT |
| Reduced motion | `prefers-reduced-motion` respected |
| Contrast | Uses the existing brand palette — see caveat in Section 12 |

---

## 10. Content Report

- **10 landing pages** created or upgraded, 22,445 words of original service copy
- **77 sub-service sections**, each a real anchor target
- **89 FAQ pairs** (23 preserved from the existing AC page, 66 new)
- **10 keyword clusters**, one per page

### Content integrity

`build/verify_content.py` fails the build on any invented price, percentage,
years-in-business claim, customer count, star rating, review count, certification,
award, guarantee, warranty, "24/7" or superlative market claim. It is negation-aware, so
honest disclaimers ("we do **not** offer a guaranteed response time") pass while the
claims themselves cannot.

**Removed during this work:** five unverified named testimonials from the AC page,
replaced with a trust section making no customer-quote claims.

---

## 11. SEO Checklist

| Item | Status |
|---|---|
| Unique title tags | ✅ Completed |
| Unique meta descriptions | ✅ Completed — all 140–160 chars |
| Self-referencing canonicals | ✅ Completed |
| Single H1 per page | ✅ Completed |
| Heading hierarchy, no skips | ✅ Completed — was broken, now fixed |
| Keyword placement in title/H1/lead | ✅ Completed |
| Image ALT text | ✅ Completed — 100% coverage |
| Image ALT accuracy | ✅ Improved — rewritten to describe before/after composites correctly |
| Responsive images (`srcset`/`sizes`) | ✅ Completed |
| Lazy loading | ✅ Completed |
| Explicit image dimensions | ✅ Completed — read from real files |
| Open Graph | ✅ Completed — unique image per page |
| Twitter Cards | ✅ Completed |
| Service schema | ✅ Completed |
| Breadcrumb schema | ✅ Completed |
| FAQ schema | ✅ Completed |
| Robots.txt | ✅ Completed |
| XML sitemap | ✅ Completed |
| HTML sitemap | ✅ Completed |
| Internal linking — navigation | ✅ Completed |
| Internal linking — contextual | ✅ Completed |
| Orphan pages | ✅ Completed — zero |
| Broken links | ✅ Completed — zero |
| Anchor links | ✅ Completed — all resolve |
| Duplicate metadata | ✅ Completed — none |
| Keyword cannibalization | ✅ Reviewed — none material |
| Thin content | ✅ Completed — min 2,016 words on landing pages |
| Semantic HTML | ✅ Completed |
| Accessibility | ✅ Improved |
| Page speed architecture | ✅ Improved |
| Analytics / conversion tracking | ✅ Completed — verified single-fire |
| Hero imagery | ✅ Completed — 10 of 10 pages |
| Service galleries | ⚠️ Improved — 9 of 10; pest control pending photography |
| Local SEO — communities | ✅ Completed |
| Pricing on page | ⚠️ Pending — no verified prices supplied |
| Review / rating schema | ⚠️ Pending — no verified review source |
| Google Business Profile | ⚠️ Pending — outside repository |
| Backlink acquisition | ⚠️ Pending — outside repository |
| Blog / informational content | ⚠️ Pending — recommended below |
| Contrast audit vs WCAG AA | ⚠️ Pending — brand palette not formally measured |

---

## 12. Recommendations

### Content expansion
1. **Pest control photography** is the one genuine gap. The page ships with a documented
   placeholder rather than borrowed cleaning photos. Commission: technician inspecting
   for cockroach/ant activity, bed bug mattress inspection, commercial kitchen treatment.
2. **Per-community landing pages** once the core ten mature — `/home-cleaning/dubai-marina`
   style — but only for communities with genuine booking volume. Do not spin up ten thin
   location pages; that invites a thin-content problem rather than solving one.
3. **Blog for informational intent.** The landing pages own commercial intent; they should
   not chase "how to remove limescale". A small cluster of genuinely useful Dubai-specific
   guides (AC servicing frequency in summer, tenancy handover checklists, bed bug
   preparation) would capture upper-funnel traffic and give the service pages internal
   links from relevant context.

### Local SEO and authority
4. **Google Business Profile** is the highest-leverage item not in this repository.
   Complete the profile, add service categories matching these ten pages, post photos,
   and link each service to its landing page.
5. **Review strategy.** No review schema is implemented because no verified review corpus
   exists. Collect reviews on Google, then surface them — real reviews with real
   `AggregateRating` markup are one of the strongest local ranking and CTR levers.
6. **Local citations** — consistent NAP on UAE directories. The phone number is now
   consistent sitewide, which is the prerequisite.

### Backlinks
7. Target property managers, holiday-home operators and real-estate agencies in the
   covered communities — partners who would link naturally, rather than bought links.

### Technical
8. **Set a Google Ads conversion ID.** `GOOGLE_ADS_ID` and the conversion labels are
   currently empty in `NACRAVO_TRACKING`. The `generate_lead` event fires correctly, but
   nothing is recording it as an Ads conversion until those are filled in.
9. **Audit the live GTM container.** The repository's export shows conversions firing only
   on the custom `generate_lead` event, but the live container also has built-in Form
   Submit and Link Click triggers active. Confirm no live tag fires a conversion on those,
   or WhatsApp clicks and form submits could double-count.
10. **Run Lighthouse after deploy** for real CWV numbers.
11. **Formal contrast audit.** The brand palette (`--sage #7E8F70` on `--pearl #F5F2EC`)
    has not been measured against WCAG AA. Some sage-on-pearl body text may fall short of
    4.5:1 and should be checked before claiming AA compliance.

### Schema enhancements
12. Add `AggregateRating` once reviews exist, `Offer`/`priceRange` once prices are agreed,
    and `LocalBusiness` sub-types per district if per-community pages are built. All three
    are blocked on business inputs, not engineering.

---

## 13. Final Summary

### Pages created
`/home-cleaning`, `/deep-cleaning`, `/move-in-out-cleaning`, `/holiday-home-cleaning`,
`/office-commercial-cleaning`, `/specialized-cleaning`, `/pest-control`,
`/handyman-services`, `/annual-maintenance`, `/services`

### Pages updated
`/ac-service-dubai` (upgraded in place, URL and canonical preserved), homepage,
`/sitemap`, and nine legal pages (contact details and markup validity).

### SEO work completed
Eleven commercial pages with unique metadata, complete structured data, layered internal
linking with zero orphans, corrected heading hierarchy across the whole site, accurate
image ALT text, service-specific hero imagery, local coverage signals, and a consolidated
performance architecture. Contact details corrected in 227 places.

Three defects from the previous implementation round were found and fixed during this
audit: a misleading simulated before/after slider, factually wrong gallery ALT text, and
a sitewide heading-level skip.

### Remaining recommendations
Pest control photography, Google Ads conversion ID, live GTM trigger audit, Google
Business Profile, review collection, contrast audit, and the blog/backlink programme.
All are listed with rationale in Section 12.

### Expected SEO impact
Foundations are complete and technically sound. Organic results will follow indexing and
maturation over 3–6 months and depend materially on the off-site work in Section 12,
which has not been started. Paid performance should improve sooner, because relevance,
message match and form friction — the levers this work actually moved — are the ones
Quality Score responds to.

### Deployment status

**Nothing has been deployed.** No push, no DNS change, no production configuration
altered, no analytics IDs changed. All work is committed locally on `main`.
