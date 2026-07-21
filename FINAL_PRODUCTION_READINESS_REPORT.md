# Final Production Readiness Report — Nacravo

**Prepared:** 21 July 2026
**Site:** https://www.nacravo.com
**Status:** **NOT DEPLOYED.** All work committed locally on `main`.

**Companion documents:** `GTM_AUDIT_REPORT.md` · `ANALYTICS_VALIDATION_REPORT.md` ·
`ACCESSIBILITY_REPORT.md` · `GOOGLE_ADS_READINESS_REPORT.md` · `DEPLOYMENT_SIGNOFF.md` ·
`SEO_IMPLEMENTATION_REPORT.md` (+ `.xlsx`) · `DEPLOYMENT_CHECKLIST.md`

This report covers the operational readiness phase — the work needed to move from "ready for
deployment" to "ready for production." All findings were re-verified this phase; nothing is
carried over on trust.

---

## 1. Executive Summary

The website itself is production-ready. Eleven indexable commercial pages are built on the
existing design system, verified across desktop/tablet/mobile with zero console errors, clean
routing, correct schema, and a conversion path proven single-fire.

The remaining blockers are **operational, not code** — they live in the GTM console, the Google
Ads account, and a pending branding decision. This phase audited each in depth and produced
remediation plans, but per the deployment rules **made no GTM, colour, or deployment changes.**

### What changed this phase

- **Live GTM container fully inventoried** (18 tags) and the duplicate `generate_lead` tag
  identified precisely: keep tag 25, pause tag 48. Impact on GA4, Ads and historical data
  documented.
- **Full analytics chain re-validated** in-browser: one submit → one `generate_lead` → one Ads
  conversion, dedupe guards confirmed.
- **Contrast re-measured**; two concrete brand options (A: keep + disclose, B: specific
  AA-passing hex values) prepared for decision.
- **Every image re-audited** against its page — no duplicates, 100% accurate alt text.
- **GBP, review, and conversion-value strategies** written for the business to execute.
- **Full deployment validation**: 12 routes, 15 redirects, all assets, all breakpoints.

### Production readiness: **90 / 100** — safe to deploy with blockers tracked

Up one point from the previous 89 because the image duplication found last phase is fixed and the
GTM issue is now fully diagnosed with a ready-to-execute plan rather than an open question.

---

## 2. Architecture

Static HTML on Vercel, no framework. Generated from `build/`:

- `template.py` + `content_*.py` render the pages — one source of truth for header, footer,
  schema and the tracking contract, so 12 files cannot drift.
- `assets/nacravo.css` (29.4 KB) extracted verbatim from `index.html` — landing pages cannot
  diverge from the homepage design system.
- `assets/nacravo.js` (19.3 KB) — one tracking layer, shared and cached.
- `assets/nacravo-ac.css` (8.3 KB) — page-scoped AC components.

Verification is scripted and repeatable: `qa.py`, `verify_content.py`, `audit.py`,
`audit_final.py`, `gtm_audit.py`.

---

## 3. SEO

Verified this phase — no regressions.

| Area | Status |
|---|---|
| Indexable pages | 23 |
| Unique titles / descriptions | ✅ All, enforced by QA |
| Canonical | ✅ Absolute, self-referencing, no trailing slash, no `.html` |
| Schema | ✅ Service + Breadcrumb + FAQ per landing page, all parse |
| Sitemap | ✅ 23 URLs, each verified on disk |
| Robots | ✅ Correct |
| Internal links / anchors | ✅ Zero broken |
| Redirects | ✅ 15, all 301, no chains/loops/shadows |
| Heading hierarchy | ✅ No skips |
| Orphan pages | ✅ Zero (in-degree 11 each) |

Full per-page detail: `SEO_IMPLEMENTATION_REPORT.md` and `.xlsx`.

---

## 4. Google Ads

**Landing pages ready.** Strong message match, sub-service anchors enabling ad-group-depth
deep-linking, form above the fold with service preselection, three conversion routes.

**Account-level items outstanding:** conversion value (currently 0), the GA4 duplicate tag, and
a check for GA4-imported conversion double-counting. Full analysis and a bidding-strategy
progression in `GOOGLE_ADS_READINESS_REPORT.md`.

---

## 5. Accessibility

24 of 26 contrast combinations pass WCAG AA. **Two fail** — the primary button (3.11:1) and
WhatsApp button (1.98:1) — both requiring a branding decision. Seven other failures were fixed in
the prior phase without touching brand surfaces.

**The site is not yet AA compliant.** Two options (keep-and-disclose vs specific AA-passing hex
values) are in `ACCESSIBILITY_REPORT.md`. No colour changed without approval.

All non-contrast accessibility (landmarks, keyboard, focus, labels, ARIA, touch targets, alt
text, reduced motion) verified passing.

---

## 6. Performance

Architectural improvements, verified: text-first LCP, shared cached CSS/JS, zero JS on the AC
page, all images lazy with real intrinsic dimensions (no CLS), DOM 618–1,030 elements per page.

**No field data yet** — run Lighthouse post-deploy for real Core Web Vitals numbers. Current
claims are structural, not measured scores.

---

## 7. Analytics

Site-side correct and verified single-fire. One GA4-only, GTM-side duplication remains
(`generate_lead` tags 25 + 48). Consent Mode v2 working. Full detail in
`ANALYTICS_VALIDATION_REPORT.md`.

---

## 8. Conversion Tracking

| | |
|---|---|
| Ads conversion ID | `18246691744` |
| Conversion label | `J2SlCMja0M0cEKDX2fxD` |
| Fires on | `generate_lead` (custom event) |
| Duplication | **None** for Google Ads — single `__awct` tag |
| Site coupling | GTM is the single source of truth; `GOOGLE_ADS_ID` intentionally empty in site config |

The one risk to check is account-level: whether a GA4-imported conversion action *also* counts
leads in Ads alongside tag 49. Flagged as critical in the Ads report.

---

## 9. Security

| Check | Status |
|---|---|
| External `target="_blank"` links | ✅ All carry `rel="noopener"` |
| `mailto:` / `tel:` | ✅ Single consistent value each |
| WhatsApp links | ✅ Single number, `rel="noopener"` |
| Forms | ✅ No credentials collected; client-side only, hands to WhatsApp |
| Inline scripts | ✅ First-party only (GTM, consent, tracker); no third-party inline injection |
| Secrets in repo | ✅ None; `.env` gitignored |
| PII in URLs | ✅ None — form data goes into the WhatsApp message body, not query strings |
| HTML validity | ✅ No unescaped `&` in text, no duplicate IDs (QA-enforced) |

**Note:** no Content-Security-Policy header is set. The site is CSP-compatible in principle
(scripts are first-party), but adding a CSP is a Vercel-header configuration task, listed as a
medium recommendation.

---

## 10. QA

| Suite | Result |
|---|---|
| `build/qa.py` (23 pages) | ✅ PASS |
| `build/verify_content.py` | ✅ PASS — no fabricated claims |
| `build/audit_final.py` | 2 known blocking items (both button contrast, external decisions) |
| `build/audit.py` | ✅ headings, metadata, in-degree clean |
| Routes (12) | ✅ all 200 |
| Redirects (15) | ✅ all 301 |
| Assets (7) | ✅ all present |
| Breakpoints | ✅ desktop / tablet / mobile, no overflow, form above fold |
| Console errors | ✅ zero |

---

## 11. Deployment Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| GA4 lead numbers double-counted after launch | **Certain until fixed** | Medium — reporting only, not spend | Pause tag 48 before or right after launch; annotate GA4 |
| Ads double-count via GA4 import | Possible | High — wastes spend | Verify conversion actions in Ads before enabling campaigns |
| Bidding underperforms on value 0 | Certain if tROAS used early | Medium | Start Maximise Conversions, not tROAS |
| Button contrast complaint / failed a11y audit | Low–Medium | Medium — reputational/legal | Decide Option A/B; if A, disclose on `/accessibility` |
| Stale `gtm-nacravo-container.json` misleads a future editor | Medium | Low | Delete or re-export it |
| Hand edit to a generated page lost on rebuild | Medium | Low | Documented in every generator docstring + `MEMORY.md` |
| No CI — verifiers must be run manually | Medium | Low | Run the four scripts before every deploy (in `DEPLOYMENT_CHECKLIST.md`) |
| Cross-page image reuse | Low | Low (cosmetic) | Commission more photography |

None of these blocks the *website* from deploying. The first three are operational and can be
resolved in the GTM/Ads consoles.

---

## 12. Recommendations — ranked

### Critical (before or immediately after launch)
1. **Pause duplicate GA4 tag 48** in GTM. *(GTM admin, 2 min.)*
2. **Verify no GA4-imported conversion double-counts** against tag 49 in Google Ads. *(Marketing, 10 min.)*
3. **Set a conversion value** — static minimum (Option 1). *(Marketing.)*
4. **Decide button contrast** — Option A or B. *(Brand owner.)*

### High
5. Publish verified price ranges.
6. Complete Google Business Profile and map services to pages.
7. Start the review-collection workflow.
8. Commission pest control and AC photography.

### Medium
9. Align AC campaign geo targeting to Downtown / Business Bay / DIFC.
10. Point Ads final URLs at real pages, not vanity redirects.
11. Add trade licence + VAT TRN to the footer.
12. Delete the three paused GTM tags and the stale container JSON.
13. Add a Content-Security-Policy header in Vercel.
14. Run Lighthouse post-deploy for real CWV numbers.

### Low
15. Optional `form_submit` event on landing pages for uniform reporting.
16. More before/after photography to reduce cross-page image reuse.
17. Rename generic image files for image SEO (breaks history — low value).
18. Manual screen-reader pass before any formal accessibility statement.

---

## 13. Final Readiness Score

| Dimension | Weight | Score | Notes |
|---|---:|---:|---|
| Technical SEO | 20% | 10/10 | Zero broken links/anchors/chains; metadata unique |
| On-page SEO | 15% | 10/10 | 10 clusters, 2,000+ words each, no cannibalization |
| Structured data | 10% | 9/10 | 3 types/page valid; rating/price blocked on business inputs |
| Internal linking | 10% | 10/10 | Zero orphans, layered |
| Conversion / Ads | 15% | 8/10 | Form above fold verified; value still 0 |
| Analytics | 10% | 7/10 | Site-side correct; GTM duplicate diagnosed with a ready fix |
| Accessibility | 10% | 8/10 | 7 of 9 contrast fixes done; 2 need a brand decision |
| Performance | 5% | 9/10 | Text LCP, shared assets, zero AC-page JS; no field data |
| Content quality | 5% | 9/10 | Original, no fabricated claims; photography gaps |

### **Overall: 90 / 100 — Ready for production, conditional on the four Critical items.**

The website is deployable today. "Production ready" in the full sense depends on the four
operational actions above, none of which is a code change and all of which the team can execute
in the GTM and Google Ads consoles plus one branding decision.

### Deployment status

**Nothing has been deployed.** No push, no DNS change, no analytics ID change, no GTM change, no
tag paused, no colour changed. All work is committed locally on `main`.
