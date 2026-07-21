# Post-Launch Checklist — Nacravo

**Prepared:** 21 July 2026
**Use:** run these after `git push` deploys to Vercel. Times are from go-live.

---

## First 24 hours

### Smoke test (first hour)
- [ ] `https://www.nacravo.com/` returns 200
- [ ] All 11 commercial pages return 200 (10 landing + `/services`)
- [ ] `https://www.nacravo.com/ac-services` → 301 → `/ac-service-dubai`
- [ ] Spot-check 3 more redirects (`/sofa-cleaning`, `/plumbing`, `/amc`)
- [ ] `sitemap.xml` and `robots.txt` return 200
- [ ] Non-`www` request 301s to `www`
- [ ] Submit a real test lead on desktop and mobile; confirm WhatsApp opens with the prefilled
      message

### Analytics (first 24h)
- [ ] GA4 realtime shows `page_view`, `generate_lead`, `whatsapp_click`, `phone_click`
- [ ] **Pause the duplicate GA4 tag (48)** if not already done; add the GA4 annotation
- [ ] After pausing, confirm one test lead = **one** `generate_lead` in DebugView
- [ ] Google Ads shows the conversion recording (if campaigns are live)
- [ ] Confirm only one primary lead conversion action in Google Ads (no GA4-import double-count)
- [ ] No spike in 404s (Vercel logs / analytics)

### Search Console (first 24h)
- [ ] Domain + `www` properties added and verified
- [ ] Sitemap submitted (status Success, 23 URLs)
- [ ] Request indexing for the 12 core pages

---

## First 3 days
- [ ] Confirm daily `generate_lead` count is ~half the pre-fix level (the correction landed)
- [ ] Watch Search Console **Coverage** — pages beginning to index; no unexpected errors
- [ ] Run **Rich Results Test** on 3 pages (Service, Breadcrumb, FAQ) — 0 errors
- [ ] Run **Lighthouse** on 3–4 landing pages; record LCP/CLS/INP in the KPI dashboard
- [ ] Facebook Sharing Debugger on 2 pages — og:image resolves
- [ ] Real-device pass: iPhone Safari + one Android; confirm forms, sticky bar, WhatsApp
- [ ] Firefox desktop quick pass
- [ ] Google Business Profile live and linked; first review requests sent

---

## First 7 days
- [ ] Search Console **Performance** shows first impressions for the primary keywords
- [ ] Check **Query × Page** — right queries landing on right pages (catch cannibalisation early)
- [ ] Confirm indexed count climbing toward 23
- [ ] Google Ads: Quality Score column added; check landing-page-experience component
- [ ] First blog post(s) published (Q1 content start)
- [ ] Review lead volume and route split (form vs WhatsApp vs phone)
- [ ] Address any console errors or broken-link reports from real traffic

---

## First 14 days
- [ ] CWV field data may begin appearing in Search Console — check
- [ ] Refine metadata on any page with high impressions but low CTR
- [ ] Google Ads: pause underperforming keywords; check search-terms report; add negatives
- [ ] Confirm conversion value is set (if moving toward value bidding)
- [ ] GBP: first reviews arriving; respond to all; first weekly post published
- [ ] Re-run `audit_final.py` against the live site's assets if any hotfix shipped

---

## First 30 days
- [ ] Full **month-1 KPI review** — populate `SEO_KPI_DASHBOARD.xlsx` (organic clicks,
      impressions, CTR, position, leads by route, Ads cost/leads, CPL, reviews, CWV)
- [ ] Search Console: indexing stable at ~23; no manual actions
- [ ] Rankings: primary keywords tracked; note movement in the Keyword Rankings sheet
- [ ] Google Ads: enough conversions to consider moving from Maximise Clicks/Conversions toward a
      target CPA (only if value not yet set) 
- [ ] Content: 3–4 posts live; plan month-2 cadence
- [ ] Reviews: progress toward a 20+ base; activate `AggregateRating` if reached
- [ ] Decision closed on button contrast (accessibility); `/accessibility` wording matches reality
- [ ] Retro: what broke, what surprised, what to change

---

## First 90 days
- [ ] **Quarter-1 review** against `SEO_ROADMAP_12_MONTHS.md` Q1 success signals
- [ ] Core Web Vitals field data reviewed; act on any "needs improvement" URLs
- [ ] ~15 posts published; identify early winners to expand
- [ ] Reviews: stable base with `AggregateRating` live; steady monthly growth
- [ ] Google Ads: value-based bidding running if values implemented; ROAS in the dashboard
- [ ] Local: GBP Insights reviewed (which posts/photos/services drove actions)
- [ ] Backlinks: first earned links from partnership outreach
- [ ] Identify data-backed candidates for Q3 location pages (do not build speculatively)
- [ ] Full technical re-audit (`qa.py`, `audit_final.py`, fresh Lighthouse)
- [ ] Plan Q2 from real data

---

## Standing weekly (throughout)
- [ ] Search Console Performance review
- [ ] Lead volume + route split
- [ ] Ads spend, CPL, conversions
- [ ] New reviews responded to
- [ ] One GBP post published
- [ ] KPI dashboard updated (monthly at minimum)

---

## If something goes wrong
- **Site issue:** promote the previous Vercel deployment (instant) or `git revert` + push.
- **GTM issue:** restore the previous container version in GTM (independent of the site).
- **Indexing issue:** URL Inspection → "Test live URL" to see what Googlebot renders.
- **Conversion mis-count:** re-check the GTM tag state and the Ads conversion actions (§ first 24h).
Full rollback detail in `DEPLOYMENT_SIGNOFF.md`.
