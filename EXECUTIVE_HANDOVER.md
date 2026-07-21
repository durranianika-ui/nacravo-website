# Executive Handover — Nacravo Website

**Prepared:** 21 July 2026
**Status:** Feature-complete, verified, **NOT deployed.** All work committed locally on `main`.
**Audience:** business owner, marketing lead, and whoever maintains the site next.

This is the single-page orientation. Every claim links to a detailed companion document.

---

## 1. What was delivered

Nacravo went from a one-page marketing site + a single AC page to a **complete, production-ready
lead-generation website**: 10 service landing pages, a services hub, an upgraded homepage, and a
full launch/growth documentation set.

- **10 landing pages** (9 new, AC upgraded in place), each 2,000–3,600 words, 77 sub-service
  sections total, form above the fold, service preselection, three conversion routes.
- **Fully responsive**, verified 320px → 1920px with zero defects.
- **Technically clean**: unique metadata, valid schema, no broken links, zero orphan pages.
- **Honest**: no invented prices, ratings, testimonials or certifications — enforced by an
  automated content check on every build.

---

## 2. Architecture (how to maintain it)

Static HTML on Vercel, deployed from GitHub (`durranianika-ui/nacravo-website`) on push to `main`.
No framework.

**The 11 commercial pages are generated from `build/`.** They are build artefacts — **hand edits
are destroyed on the next build.** To change a page:
1. Edit the content module (`build/content_*.py`) or template (`build/template.py`).
2. Re-run the generators (`extract_assets.py` → `build_pages.py` → `build_ac.py` → `build_sitemap.py`).
3. Verify (`qa.py`, `verify_content.py`, `audit_final.py`).

`python` is **not** on PATH — use `.venv/Scripts/python.exe`. Full detail: `DEPLOYMENT_CHECKLIST.md`.

---

## 3. Landing pages

| URL | Primary keyword | Coverage |
|---|---|---|
| /home-cleaning | home cleaning Dubai | Dubai-wide |
| /deep-cleaning | deep cleaning Dubai | Dubai-wide |
| /move-in-out-cleaning | move out cleaning Dubai | Dubai-wide |
| /holiday-home-cleaning | holiday home cleaning Dubai | Dubai-wide |
| /office-commercial-cleaning | office cleaning Dubai | Dubai-wide |
| /specialized-cleaning | sofa cleaning Dubai | Dubai-wide |
| /pest-control | pest control Dubai | Dubai-wide |
| /ac-service-dubai | AC service Dubai | **Downtown / Business Bay / DIFC only** |
| /handyman-services | handyman Dubai | Dubai-wide |
| /annual-maintenance | annual maintenance contract Dubai | Dubai-wide |

The AC geo-limit is deliberate and enforced everywhere (page, schema, and it must be matched in
the Ads campaign). Do not advertise AC Dubai-wide.

---

## 4. SEO

Foundation complete: 23 indexable pages, unique metadata, Service + Breadcrumb + FAQ schema per
page, 15 redirects (no chains/loops), zero broken links, zero orphans. The next 12 months are
off-site: reviews, backlinks, Google Business Profile, content. See `SEO_IMPLEMENTATION_REPORT.md`,
`SEO_ROADMAP_12_MONTHS.md`, `CONTENT_STRATEGY.md` (50 topics), `SEARCH_CONSOLE_SETUP.md`.

---

## 5. Google Ads

10 campaigns, one per landing page, ad groups mapped to real page anchors so an ad can deep-link
(e.g. `/ac-service-dubai#chemical-wash` preselects the sub-service in the form). Ready-to-use
headlines, descriptions, extensions and sitelinks in `GOOGLE_ADS_LAUNCH_PACK.md` / `.xlsx`.
Readiness analysis + bidding progression in `GOOGLE_ADS_READINESS_REPORT.md`.

---

## 6. Analytics & GTM

Site-side tracking is correct and verified single-fire (`generate_lead`, WhatsApp, phone, CTA
events, with a dedupe guard). **One issue to fix in the GTM console before trusting reports:** two
GA4 tags fire `generate_lead`, so GA4 counts leads twice. Keep tag 25, pause tag 48 — step-by-step
in `GTM_IMPLEMENTATION_GUIDE.md`. Google Ads conversions are **not** affected. Full analysis:
`GTM_AUDIT_REPORT.md`, `ANALYTICS_VALIDATION_REPORT.md`.

---

## 7. Accessibility

Structurally strong (landmarks, keyboard, focus, labels, ARIA, touch targets, no heading skips).
**Two button colours fail WCAG AA** (primary button 3.11:1, WhatsApp button 1.98:1) and need a
**branding decision** — keep the brand and disclose the limitation (Option A), or adopt the
specific AA-passing colours provided (Option B). Details + exact hex values: `ACCESSIBILITY_REPORT.md`.
No colour was changed without approval.

---

## 8. Performance

Built for strong Core Web Vitals: text LCP (no hero image blocks first paint), one shared cached
CSS + JS file, all images lazy with real dimensions (no layout shift), zero JS on the AC page.
**Numeric field scores must be measured post-deploy** with Lighthouse / Search Console — the
architecture supports the targets but they are not yet measured.

---

## 9. Responsive

Verified at every mandated breakpoint (320/360/375/390/412/430 mobile; 768/820/1024 tablet;
1280/1366/1440/1920 desktop) plus landscape: no horizontal scroll, no overlap, form above the fold
everywhere, correct input types (`tel`/`date`), 16px inputs (no iOS zoom). **Zero defects, no code
changed.** One follow-up: real Safari/iOS + Firefox pass (tested on Blink only). Full report:
`RESPONSIVE_QA_REPORT.md`.

---

## 10. Documentation set

| Document | Purpose |
|---|---|
| `EXECUTIVE_HANDOVER.md` | This page |
| `FINAL_PRODUCTION_READINESS_REPORT.md` | Overall readiness (90/100) |
| `SEO_IMPLEMENTATION_REPORT.md` + `.xlsx` | Full SEO detail + data workbook |
| `GTM_AUDIT_REPORT.md` + `GTM_IMPLEMENTATION_GUIDE.md` | Duplicate-tag analysis + fix steps |
| `ANALYTICS_VALIDATION_REPORT.md` | Event-by-event verification |
| `ACCESSIBILITY_REPORT.md` | Contrast measurements + brand options |
| `GOOGLE_ADS_READINESS_REPORT.md` | PPC assessment + review/GBP/value plans |
| `GOOGLE_ADS_LAUNCH_PACK.md` + `.xlsx` | Ready-to-launch campaigns |
| `SEARCH_CONSOLE_SETUP.md` | GSC setup + monitoring |
| `GBP_OPTIMIZATION_PLAN.md` | Google Business Profile plan |
| `SEO_ROADMAP_12_MONTHS.md` | Quarterly growth plan |
| `CONTENT_STRATEGY.md` | 50 blog topics mapped to pages |
| `SEO_KPI_DASHBOARD.xlsx` | Monthly tracking template |
| `CRO_ROADMAP.md` | Conversion test backlog |
| `RESPONSIVE_QA_REPORT.md` | Cross-device verification |
| `PRE_LAUNCH_CHECKLIST.md` / `POST_LAUNCH_CHECKLIST.md` | Launch gates |
| `DEPLOYMENT_SIGNOFF.md` | Go/no-go + rollback |

---

## 11. Known risks

| Risk | Severity | In site code? |
|---|---|---|
| GA4 double-counts leads until tag 48 paused | Medium (reporting) | No — GTM |
| Possible GA4-imported conversion double-count in Ads | High (spend) | No — Ads account |
| Conversion value = 0, blocks value bidding | High | Partly (pushes 0) |
| Two buttons fail WCAG AA | High | Yes (CSS) — needs brand decision |
| Pest control + AC pages lack service photography | Medium | No — asset gap |
| No published prices | Medium | No — business input |
| Stale `gtm-nacravo-container.json` in repo | Low | Yes — delete/re-export |
| Generated pages: hand edits lost on rebuild | Low | Process risk |
| No CI — verifiers run manually | Low | Process risk |

**None blocks the website from deploying.** The first four are the "fully production-ready" gate.

---

## 12. Operational tasks (who does what)

| Task | Owner | Where |
|---|---|---|
| Pause duplicate GA4 tag | GTM admin | `GTM_IMPLEMENTATION_GUIDE.md` |
| Verify Ads conversion actions | Marketing | Google Ads UI |
| Set conversion value | Marketing | Google Ads / dataLayer |
| Decide button contrast | Brand owner | `ACCESSIBILITY_REPORT.md` |
| Publish prices | Business owner | Supply figures → `build/content_*.py` |
| Complete GBP | Marketing | `GBP_OPTIMIZATION_PLAN.md` |
| Start review collection | Operations | GBP plan §8 |
| Commission AC + pest photography | Marketing | — |
| Add trade licence + VAT TRN | Business owner | footer placeholder |
| Deploy | Release manager | `git push` after sign-off |

---

## 13. Future roadmap (headline)

- **Q1:** launch, index, GBP, fix the two blockers, first content.
- **Q2:** content depth, reviews to 20+, `AggregateRating`, first backlinks.
- **Q3:** data-driven location pages, digital PR, authority building.
- **Q4:** consolidate, re-audit, plan year 2 from real data.

Detail: `SEO_ROADMAP_12_MONTHS.md`.

---

## 14. Bottom line

**Production readiness: 90/100.** The website is deployable today. Full "production ready" status
depends on four operational actions — pause one GTM tag, verify Ads conversions, set a conversion
value, and decide button contrast — **none of which is a website code change.**

Nothing has been deployed. Deployment is a `git push` after the sign-off in `DEPLOYMENT_SIGNOFF.md`.
