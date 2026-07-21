# Pre-Launch Checklist — Nacravo

**Prepared:** 21 July 2026
**Status:** NOT DEPLOYED. This is the gate to run **before** `git push`.
**Verified items** below were confirmed this phase; **open items** need a human/console action.

Regenerate + verify first if anything in `build/` changed:
```bash
./.venv/Scripts/python.exe build/extract_assets.py && ./.venv/Scripts/python.exe build/build_pages.py \
 && ./.venv/Scripts/python.exe build/build_ac.py && ./.venv/Scripts/python.exe build/build_sitemap.py
./.venv/Scripts/python.exe build/qa.py && ./.venv/Scripts/python.exe build/verify_content.py \
 && ./.venv/Scripts/python.exe build/audit_final.py
```

---

## Website
- [x] Build passes (all generators run clean)
- [x] `qa.py` passes — 23 pages, 0 errors
- [x] `verify_content.py` passes — no fabricated claims
- [x] 12 routes return 200; 15 redirects return 301
- [x] All assets return 200 (CSS, JS, sitemap, robots, favicon, manifest)
- [x] Zero console errors across tested pages
- [x] Contact details consistent (one phone, one email, one WhatsApp)

## Responsive (verified this phase)
- [x] Desktop 1280/1366/1440/1920 — no overflow, content caps at 1140px, spacious
- [x] Tablet 768/820/1024 — no broken layout, nav correct
- [x] Mobile 320/360/375/390/412/430 — form above fold, no overflow
- [x] Mobile landscape (812×375) — no overlap
- [x] Mobile hero: H1 + description + form + Call + WhatsApp in first screen
- [x] Fixed elements never overlap (sticky bar mobile-only, floating WhatsApp desktop-only)
- [ ] **Real iPhone Safari + Firefox pass** (tested on Blink only — verify before launch)

## SEO
- [x] Unique titles / descriptions (all 140–160 chars)
- [x] Self-referencing canonicals, absolute, no trailing slash, no `.html`
- [x] Heading hierarchy — no skips
- [x] Service + Breadcrumb + FAQ schema per page, all parse
- [x] Internal links / anchors — zero broken
- [x] Image alt — 100%, composites labelled, no duplicate imagery per page
- [ ] `www` canonical enforced (confirm non-www 301s to www on live)

## Robots & Sitemap
- [x] `robots.txt` — Allow /, Disallow /thank-you, sitemap declared
- [x] `sitemap.xml` — 23 URLs, each verified on disk
- [ ] Sitemap ready to submit in Search Console (post-deploy)

## Analytics
- [x] GTM + GA4 IDs unchanged and present
- [x] Consent Mode v2 defaults set before GTM
- [x] Single tracking layer per page
- [x] `generate_lead` single-fire verified (double-click guarded, invalid submit fires none)
- [x] WhatsApp / phone / CTA events fire with dedupe guard

## GTM
- [x] Live container audited (18 tags)
- [x] No built-in trigger fires a conversion
- [ ] **Duplicate GA4 `generate_lead` tag (48) paused** — see `GTM_IMPLEMENTATION_GUIDE.md`
- [ ] GA4 annotation prepared for the fix date

## Google Ads
- [x] Single Ads conversion tag (49), ID 18246691744, fires on `generate_lead`
- [ ] **Confirm no GA4-imported conversion double-counts** against tag 49 (Ads UI)
- [ ] **Conversion value set** (static minimum) before value-based bidding
- [ ] Campaigns built from `GOOGLE_ADS_LAUNCH_PACK` (final URLs = real pages, not redirects)
- [ ] AC campaign geo-restricted to Downtown / Business Bay / DIFC
- [ ] Negative keywords added; start on Maximise Conversions (not tROAS)

## Google Search Console
- [ ] Domain property added and verified (post-deploy)
- [ ] URL-prefix `www` property added
- [ ] Sitemap submitted; 12 core pages inspected + indexing requested
- [ ] No manual actions / security issues

## Google Business Profile
- [ ] Claimed and verified
- [ ] Categories, services, description, contact, hours set (see GBP plan)
- [ ] Launch photo batch uploaded
- [ ] Review workflow ready; linked to Ads location extension

## Performance
- [x] Text LCP, shared cached CSS/JS, lazy images with real dimensions
- [ ] Lighthouse run on 3–4 pages (interim CWV; field data post-deploy)

## Accessibility
- [x] Landmarks, skip link, labels, ARIA, keyboard, focus, touch targets
- [x] Text contrast — 7 of 9 fixed
- [ ] **Button contrast decision (Option A or B)** — see `ACCESSIBILITY_REPORT.md`
- [ ] If Option A: update `/accessibility` to disclose the limitation

## Forms / WhatsApp / Phone
- [x] Form validation blocks bad input; one `generate_lead` per valid submit
- [x] Phone input `type=tel` (numeric keyboard); date `type=date`; inputs 16px (no zoom)
- [x] WhatsApp opens with structured prefilled message, number 971581082601
- [x] `tel:+971581082601` single value sitewide

## Legal
- [x] Privacy, Terms, Cookie, Refund, Data Deletion, Accessibility, Security, Acceptable Use live
- [x] Consent banner + Consent Mode v2 working
- [ ] Trade licence + VAT TRN added to footer (currently placeholders)

## Backups & Monitoring
- [x] Everything in git; Vercel keeps previous deployments (instant rollback)
- [ ] Uptime / error monitoring configured (Vercel analytics at minimum)
- [ ] Post-launch monitoring plan reviewed (`DEPLOYMENT_SIGNOFF.md` / `POST_LAUNCH_CHECKLIST.md`)

---

## Go / No-Go

**The website is technically ready to deploy.** The unchecked items are operational (GTM, Ads,
GBP, Search Console, button-contrast decision, real-device browser pass) — none is a website code
change, and most can be done in parallel with or immediately after launch.

**Do not deploy** until the sign-off rows in `DEPLOYMENT_SIGNOFF.md` are signed.
