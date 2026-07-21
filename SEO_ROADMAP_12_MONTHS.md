# 12-Month SEO Roadmap — Nacravo

**Prepared:** 21 July 2026
**Starting point:** 11 indexable commercial pages live, technically sound, not yet deployed.
**Premise:** the on-page foundation is done. The next 12 months are about **off-site authority,
local signals, content depth, and reviews** — the levers that actually move rankings once the
technical base exists.

Each quarter has a theme, concrete tasks, and a success signal. Items already complete in the
build are marked ✅ so effort is not duplicated.

---

## Quarter 1 (Months 1–3) — Launch, index, and local foundation

**Theme:** get indexed, get the local profile working, fix the two operational blockers.

### Technical SEO
- ✅ Metadata, canonicals, schema, sitemap, redirects (done in build)
- [ ] Deploy; submit sitemap in Search Console; request indexing for 12 core pages
- [ ] Confirm `www` canonicalisation and clean-URL behaviour live
- [ ] Run Lighthouse on all 10 landing pages; record real LCP/CLS/INP in the KPI dashboard
- [ ] **Pause the duplicate GA4 tag** (see GTM guide) so lead data is accurate from day one
- [ ] Add a Content-Security-Policy header in Vercel (medium)

### Local SEO
- [ ] Complete Google Business Profile (see GBP plan) — categories, services, description, photos
- [ ] Start the review-request workflow immediately (peak-satisfaction WhatsApp ask)
- [ ] Begin a short list of high-quality UAE citations with consistent NAP

### Content
- [ ] Publish the first 3–4 blog posts (highest-intent topics from `CONTENT_STRATEGY.md`)
- [ ] Add trade licence + VAT TRN to the footer (legitimacy signal)

### Authority
- [ ] Baseline backlink audit (what exists today) to measure against

**Success signal:** 23 pages indexed; GBP live with first reviews arriving; accurate lead
tracking; first blog posts published.

---

## Quarter 2 (Months 4–6) — Content depth and review momentum

**Theme:** build topical authority around each service; grow reviews to a credible base.

### Content
- [ ] Publish 2–3 posts/month (aim ~15 total by end of Q2), each internally linked to its
      service page
- [ ] Build out 1–2 "hub" guides per service cluster (e.g. a complete AC servicing guide, a
      tenancy handover checklist) that link down to the landing pages
- [ ] Refresh landing-page metadata where Search Console shows high impressions but low CTR

### Local SEO
- [ ] Reach a stable review base (target 20+), then keep a steady monthly cadence
- [ ] **Activate `AggregateRating` schema** once reviews are genuine and displayed — reflecting
      the real rating and count
- [ ] Weekly GBP posts tied to seasonality (summer AC, quarter-end move-outs)

### Authority / Digital PR
- [ ] First outreach wave: property managers, holiday-home operators, real-estate agencies in
      covered communities — partners who link naturally
- [ ] Pursue 2–3 genuine local guest posts or supplier/partner listings

### Schema
- [ ] Add `Review` markup for individually consented reviews that are displayed on-page

**Success signal:** ~15 posts live; 20+ real reviews with `AggregateRating` active; first
earned backlinks; primary keywords appearing in Search Console.

---

## Quarter 3 (Months 7–9) — Location expansion and authority building

**Theme:** capture community-level search; deepen the backlink profile.

### Location pages *(data-driven, not speculative)*
- [ ] Using Search Console + GBP + booking data, identify communities with genuine demand
- [ ] Build location pages **only** for those communities (e.g. `/home-cleaning/dubai-marina`
      style) — 3–5 to start, not ten thin pages
- [ ] Each must have unique, useful content (community specifics, access notes), not a
      find-and-replace of the parent page
- [ ] AC location pages remain restricted to Downtown / Business Bay / DIFC — do not create AC
      location pages for uncovered areas

### Content
- [ ] Continue 2 posts/month; begin updating/expanding the best-performing Q1–Q2 posts
- [ ] Add seasonal content ahead of the next peak (e.g. pre-summer AC surge)

### Authority / Digital PR
- [ ] A local data or "state of Dubai home services" style piece for genuine PR pickup
- [ ] Continue partnership link-building; aim for steady, quality links over volume

### Reviews
- [ ] Maintain monthly review growth; respond to all; target a 4.5+ average

**Success signal:** first location pages ranking; backlink profile growing with relevant
domains; several primary keywords in the top 10.

---

## Quarter 4 (Months 10–12) — Consolidate, measure, and plan year 2

**Theme:** double down on what works; prune what doesn't; formalise reporting.

### Technical / performance
- [ ] Full technical re-audit (re-run `qa.py`, `audit_final.py`, `audit.py`; fresh Lighthouse)
- [ ] Review Core Web Vitals field data now that CrUX has history
- [ ] Revisit the button-contrast decision if still open (accessibility)

### Content
- [ ] Refresh and expand top-performing posts; retire or merge underperformers
- [ ] Expand location pages where Q3 ones proved out; hold where they didn't

### Local / reviews
- [ ] Review base should be substantial; keep the cadence
- [ ] Optimise GBP based on a year of Insights data (which posts/photos/services drove actions)

### Authority
- [ ] Assess backlink ROI; concentrate on the outreach types that earned links
- [ ] Consider a signature annual content asset (e.g. Dubai home-maintenance calendar)

### Planning
- [ ] Year-2 plan informed by 12 months of real Search Console, GA4, Ads and GBP data
- [ ] Evaluate Arabic localisation (introduces a genuine `hreflang` requirement)

**Success signal:** a clear, data-backed picture of which services, communities, content and link
sources drive revenue — and a year-2 plan built on it.

---

## Quarterly priorities at a glance

| Quarter | Primary focus | Key deliverable |
|---|---|---|
| Q1 | Launch, index, local foundation | GBP live + accurate tracking + first content |
| Q2 | Content depth + reviews | 15 posts + `AggregateRating` + first backlinks |
| Q3 | Location pages + authority | Data-driven community pages + PR piece |
| Q4 | Consolidate + plan | Re-audit + year-2 plan from real data |

---

## Continuous throughout (all 12 months)

- **Reviews:** ask every satisfied customer, respond to all, never fake or incentivise.
- **GBP posts:** weekly, tied to seasonality.
- **Search Console:** weekly performance review; catch cannibalization and CTR gaps early.
- **KPI dashboard:** update monthly (`SEO_KPI_DASHBOARD.xlsx`).
- **No fabricated claims, ever** — the content-integrity rule that governs the site governs the
  blog and GBP too.

---

## What this roadmap deliberately does NOT do

- No wholesale site redesign — the architecture is sound.
- No mass thin location pages — only communities with proven demand.
- No black-hat link buying — earned, relevant links only.
- No AC expansion in content beyond the three serviced districts until operations expand.
