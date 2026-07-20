# Nacravo — Deployment Checklist

**Status at time of writing: NOT DEPLOYED.** All work is committed locally on `main`.

This site deploys from the GitHub repo `durranianika-ui/nacravo-website` to Vercel on push to
`main`. Deployment is therefore a `git push` — do not push until the pre-flight section below is
green.

---

## How to re-verify everything

The generated pages are build artefacts. If anything in `build/` changed, regenerate first:

```bash
cd "C:/Users/NASEER KHAN/myproject"

# regenerate (order matters: assets -> pages -> AC page -> sitemap)
./.venv/Scripts/python.exe build/extract_assets.py
./.venv/Scripts/python.exe build/build_pages.py
./.venv/Scripts/python.exe build/build_ac.py
./.venv/Scripts/python.exe build/build_sitemap.py

# verify
./.venv/Scripts/python.exe build/qa.py             # structure, links, schema, a11y
./.venv/Scripts/python.exe build/verify_content.py # fabricated-claim scan
./.venv/Scripts/python.exe build/audit_final.py    # contrast, redirects, images, weight
./.venv/Scripts/python.exe build/audit.py          # headings, metadata, in-degree

# local preview with production-style routing (cleanUrls + redirects)
./.venv/Scripts/python.exe build/devserver.py 4599
```

`python` is **not** on PATH on this machine — always use `.venv/Scripts/python.exe`.

---

## Pre-flight checklist

### Build

- [x] **Build passes** — all four generator scripts run clean
- [x] **QA passes** — `build/qa.py`: 23 pages, 0 errors
- [x] **Content integrity passes** — `build/verify_content.py`: no fabricated claims
- [x] **Final audit passes** — `build/audit_final.py`: 2 known blocking items, both external
- [x] **No hand edits pending** in generated `.html` files (they would be lost)

### Links and routing

- [x] **Links verified** — 0 broken internal links
- [x] **Anchors verified** — every `#fragment` resolves on its target page
- [x] **Images verified** — 34/34 referenced files exist, 0 orphans
- [x] **Redirects verified** — 15 redirects, all 301, no chains, no loops, no shadowed sources
- [x] **Clean URLs** — no `.html` in any internal link
- [x] **Trailing slashes** — none on internal links or canonicals
- [x] **All routes return 200** — 12 commercial routes tested locally

### Forms and contact

- [x] **Forms tested** — validation blocks empty submit, focuses first invalid field
- [x] **Lead flow tested** — one `generate_lead` on double-click, correct payload
- [x] **Service preselection tested** — service and sub-service preselect from anchor URLs
- [x] **WhatsApp tested** — opens `wa.me/971581082601` with structured pre-filled message
- [x] **Phone tested** — `tel:+971581082601`, single value sitewide
- [x] **Email verified** — `info@nacravo.com`, single value sitewide
- [x] **No stale contacts** — old number and `privacy@nacravo.com` fully removed (227 replaced)

### SEO

- [x] **Schema validated** — every JSON-LD block parses; Service + Breadcrumb + FAQ per page
- [x] **Metadata verified** — all titles and descriptions unique and in range
- [x] **Canonicals verified** — absolute, self-referencing, no trailing slash, no `.html`
- [x] **Sitemap updated** — 23 URLs, each verified to exist on disk
- [x] **Robots verified** — `Allow: /`, `Disallow: /thank-you`, sitemap declared
- [x] **Open Graph / Twitter** — unique per page, all referenced images exist
- [x] **Heading hierarchy** — no skipped levels on any page

### Analytics

- [x] **Analytics verified** — GTM + GA4 IDs unchanged (`GTM-KD4PH4XP`, `G-N2VGBEBELF`)
- [x] **Consent Mode v2** — defaults set before GTM loads
- [x] **Single tracking layer per page** — no page has both inline and shared trackers
- [x] **GTM verified** — live container audited; no built-in trigger fires a conversion
- [x] **Google Ads conversion verified** — one `__awct` tag, ID `18246691744`
- [ ] **Duplicate GA4 tag resolved** — ⚠️ **OPEN. Tags 25 and 48 both fire `generate_lead`
      to `G-N2VGBEBELF`. Every lead is double-counted in GA4. Pause one in GTM.**
- [ ] **Conversion value set** — currently 0; blocks value-based bidding

### Responsive

- [x] **Desktop tested** — 1280×720 and 1280×800; form and both CTAs above the fold
- [x] **Tablet tested** — 768×1024; 2-column grids, form above fold, no overflow
- [x] **Mobile tested** — 375×812; H1 → description → form ordering, no overflow
- [x] **No horizontal scroll** at any tested width
- [x] **Touch targets** — none under 44px at 375px

### Accessibility

- [x] **Accessibility reviewed** — landmarks, skip link, labels, ARIA, keyboard, focus
- [x] **Text contrast** — 7 of 9 WCAG AA failures fixed
- [ ] **Button contrast** — ⚠️ **OPEN. Primary button 3.11:1 and WhatsApp button 1.98:1 fail
      WCAG AA. Requires a branding decision — see report Section 12.**

### Performance

- [x] **Performance reviewed** — shared cached CSS/JS, text LCP, lazy images, real dimensions
- [x] **Zero console errors** across tested pages
- [ ] **Lighthouse run** — pending; run post-deploy for real field numbers

### Final

- [x] **Final manual QA completed** — browser-verified across three breakpoints
- [x] **Nothing deployed** — no push, no DNS, no production config, no analytics ID changes

---

## Two open items before claiming "production complete"

| # | Item | Owner | Blocks deploy? | Effort |
|---|---|---|---|---|
| 1 | Duplicate GA4 `generate_lead` tag in live GTM | GTM admin | **No** — but GA4 numbers are wrong until fixed | 15 min |
| 2 | Button contrast WCAG AA failure | Brand owner | **No** — but the site cannot be called AA compliant | 1 hour |

Neither is in site code. Both can be resolved without a rebuild.

---

## Deploy steps

1. Confirm the pre-flight checklist above.
2. Confirm working tree is clean apart from intended changes: `git status`
3. Push: `git push origin main`
4. Wait for the Vercel build to complete.
5. **Post-deploy verification** (below).

---

## Post-deploy verification

- [ ] `https://www.nacravo.com/` returns 200
- [ ] All 10 landing pages + `/services` return 200
- [ ] `https://www.nacravo.com/ac-services` returns 301 → `/ac-service-dubai`
- [ ] Spot-check 3 more redirects (`/sofa-cleaning`, `/plumbing`, `/amc`)
- [ ] `https://www.nacravo.com/sitemap.xml` returns 200 and lists 23 URLs
- [ ] `https://www.nacravo.com/robots.txt` returns 200
- [ ] Submit the sitemap in Google Search Console
- [ ] Request indexing for the 10 landing pages
- [ ] Validate 2–3 pages in Google Rich Results Test (Service, Breadcrumb, FAQ)
- [ ] Validate 2–3 pages in Facebook Sharing Debugger (og:image resolves)
- [ ] GTM Preview mode: submit a test lead, confirm **one** Ads conversion fires
- [ ] Confirm GA4 realtime shows the `generate_lead` event
- [ ] Run Lighthouse on 3 landing pages; record LCP / CLS / INP
- [ ] Confirm Google Ads final URLs point at the new landing pages, not the homepage

---

## Rollback

The previous state is the commit before the SEO work. To roll back:

```bash
git log --oneline          # find the commit before the landing-page work
git revert <commit>        # preferred — preserves history
git push origin main       # Vercel redeploys automatically
```

Vercel also keeps previous deployments; promoting an earlier deployment in the Vercel dashboard
is the fastest rollback and needs no git operation.
