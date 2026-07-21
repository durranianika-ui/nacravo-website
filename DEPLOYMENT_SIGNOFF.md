# Deployment Sign-Off — Nacravo

**Prepared:** 21 July 2026
**Decision status:** ⏸️ **AWAITING SIGN-OFF. NOT DEPLOYED.**

This document is the go/no-go gate. It records what has been verified, what risks are being
knowingly accepted, and who must approve what before `git push`.

Deployment = `git push origin main` → Vercel auto-builds from `durranianika-ui/nacravo-website`.
**No push has been made.**

---

## 1. Production checklist

### Website code — all verified ✅

- [x] Build passes (all generators run clean)
- [x] `qa.py` passes — 23 pages, 0 errors
- [x] `verify_content.py` passes — no fabricated claims
- [x] `audit_final.py` — only the 2 known external blockers
- [x] 12 routes return 200
- [x] 15 redirects return 301 (no chains, loops or shadowed sources)
- [x] All assets return 200 (CSS, JS, sitemap, robots, favicon, manifest)
- [x] Forms tested — validation blocks bad input, one `generate_lead` per valid submit
- [x] WhatsApp tested — correct number, structured pre-filled message
- [x] Phone tested — single `tel:` value sitewide
- [x] Navigation tested — dropdown, mobile menu, all links resolve
- [x] Anchors tested — every `#fragment` resolves; sub-service preselection works
- [x] Schema validated — all JSON-LD parses; Service + Breadcrumb + FAQ per page
- [x] Metadata verified — unique titles and descriptions, in range
- [x] Canonicals verified — absolute, self-referencing
- [x] Sitemap verified — 23 URLs, each on disk
- [x] Robots verified
- [x] Images verified — 34/34 exist, 0 orphans, 100% alt, no duplicates, composites labelled
- [x] Desktop / tablet / mobile tested — form above fold, no overflow
- [x] Zero console errors
- [x] Contact details consistent — one phone, one email, one WhatsApp number
- [x] Analytics site-side verified — single-fire, dedupe guards working
- [x] Consent Mode v2 verified — defaults before GTM

### Operational — NOT complete ⏸️

- [ ] **GTM: duplicate GA4 `generate_lead` tag (48) paused** — GTM admin
- [ ] **Google Ads: confirmed only one primary lead conversion action** — Marketing
- [ ] **Conversion value set** (static minimum) — Marketing
- [ ] **Button contrast decision made** (Option A or B) — Brand owner
- [ ] GA4 annotation added on the GTM fix date — Marketing

---

## 2. Known issues at sign-off

| # | Issue | Severity | In site code? | Blocks website deploy? |
|---|---|---|---|---|
| 1 | Duplicate GA4 `generate_lead` tag inflates GA4 leads 2× | Critical | No (GTM) | No |
| 2 | Possible GA4-imported conversion double-count in Ads | Critical | No (Ads account) | No |
| 3 | Conversion value = 0, blocks value bidding | High | Partly (pushes 0) | No |
| 4 | Primary + WhatsApp button fail WCAG AA | High | Yes (CSS), but needs brand decision | No |
| 5 | Pest control + AC pages lack service photography | Medium | No (asset gap) | No |
| 6 | No published prices | Medium | No (business input) | No |
| 7 | Stale `gtm-nacravo-container.json` in repo | Low | Yes (untracked file) | No |
| 8 | No CSP header | Low | No (Vercel config) | No |

**No known issue blocks the website from being deployed.** Issues 1–4 are the "production
readiness" gate and are the reason this is a conditional sign-off.

---

## 3. Accepted risks

To be explicitly accepted by the approver before deploy. Deploying **before** resolving these
means accepting:

1. **GA4 lead counts will be ~2× inflated** until tag 48 is paused. Reporting only — does not
   affect Google Ads spend or bidding. *Accept if launching before the GTM edit.*
2. **The site is not WCAG AA compliant** on its two primary buttons. *Accept only alongside
   Option A and an honest `/accessibility` disclosure — do not claim AA conformance.*
3. **Bidding cannot use value** until a conversion value exists. Mitigated by starting on
   Maximise Conversions rather than tROAS.
4. **Two landing pages carry weaker imagery** (pest control, AC) until photography is
   commissioned. Documented placeholders, no misleading substitutes.

Sign-off names: _______________________  Date: _______________

---

## 4. Rollback plan

### Fastest — Vercel dashboard (no git)
Promote the previous deployment in the Vercel project. Instant, no repository operation.

### Git revert (preserves history)
```bash
git log --oneline                # identify the pre-launch commit
git revert <commit>..<HEAD>      # revert the range
git push origin main             # Vercel redeploys the reverted state
```

### GTM rollback (independent of the site)
GTM keeps every published version. If a tag change misbehaves, restore the previous container
version in the GTM UI — takes effect immediately, no site deploy needed.

**The site and GTM roll back independently**, which means the GTM fix can be made and reverted
without touching the deployed site, and vice versa.

---

## 5. Deploy sequence (once sign-off is granted)

1. Confirm working tree clean apart from intended changes: `git status`
2. Re-run the four verifiers one final time
3. `git push origin main`
4. Wait for Vercel build to complete
5. Run the **post-launch monitoring** checks below

---

## 6. Post-launch monitoring plan

### First hour
- [ ] Homepage + all 11 commercial pages return 200 on the live domain
- [ ] `https://www.nacravo.com/ac-services` → 301 → `/ac-service-dubai`
- [ ] Spot-check 3 more redirects live
- [ ] `sitemap.xml` and `robots.txt` return 200
- [ ] Submit a real test lead; confirm in GTM Preview / GA4 realtime that **one** Ads conversion
      and (after the fix) **one** GA4 `generate_lead` fire

### First 24 hours
- [ ] GA4 realtime shows `generate_lead`, `whatsapp_click`, `phone_click` arriving
- [ ] After pausing tag 48: confirm the daily `generate_lead` count is ~half the prior day
- [ ] Google Ads shows conversions recording against ID `18246691744`
- [ ] No spike in 404s (Vercel analytics / server logs)
- [ ] Run Lighthouse on 3 landing pages; record LCP / CLS / INP

### First week
- [ ] Submit the sitemap in Google Search Console; request indexing for the 10 landing pages
- [ ] Validate 2–3 pages in the Rich Results Test (Service, Breadcrumb, FAQ)
- [ ] Validate 2–3 pages in the Facebook Sharing Debugger (og:image resolves)
- [ ] Search Console: watch for coverage errors and unexpected canonicalisation
- [ ] Confirm Google Ads final URLs point at the new landing pages, not the homepage
- [ ] Monitor form → WhatsApp completion and first conversion volumes

### First month
- [ ] Review Search Console query/page mapping; refine metadata where intent mismatches
- [ ] Review conversion value data once values are implemented; consider moving toward tROAS
- [ ] Begin review collection; plan `AggregateRating` once a genuine corpus exists

---

## 7. Sign-off record

| Role | Name | Decision | Date |
|---|---|---|---|
| Technical lead | | ⬜ Go / ⬜ No-go | |
| Marketing / Ads owner | | ⬜ Go / ⬜ No-go | |
| Brand owner (contrast decision) | | ⬜ Option A / ⬜ Option B | |
| Business owner (final) | | ⬜ Approved to deploy | |

**Until every row above is signed, the state is NOT DEPLOYED.**
