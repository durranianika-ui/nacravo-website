# Google Search Console Setup & Monitoring Plan

**Prepared:** 21 July 2026
**Property:** https://www.nacravo.com
**Do first:** everything here is post-deploy. Search Console needs a live, crawlable site.

---

## 1. Property verification

1. Go to **search.google.com/search-console** → **Add property**.
2. Choose **Domain property** (`nacravo.com`) — this covers `www`, non-`www`, `http` and `https`
   in one property. Preferred over a URL-prefix property.
3. Verify via **DNS TXT record**. The site is on Vercel with DNS managed at the domain registrar
   — add the TXT record there. (If DNS access is unavailable, fall back to a URL-prefix property
   verified by the HTML file method — a small verification file can be added to the repo root.)
4. Also add a **URL-prefix property for `https://www.nacravo.com/`** — some reports (like the URL
   Inspection live test and certain enhancement reports) are easiest on the exact canonical
   prefix. Both properties can coexist.

**Canonical note:** the whole site canonicalises to `https://www.nacravo.com/` (with `www`).
Confirm in Search Console that Google's chosen canonical matches — the site's `<link rel=canonical>`
tags all use `www`, and `vercel.json` should enforce the `www` redirect. Verify a non-`www`
request 301s to `www` post-deploy.

---

## 2. Sitemap submission

1. Confirm `https://www.nacravo.com/sitemap.xml` returns 200 and lists **23 URLs**.
2. Search Console → **Sitemaps** → submit `sitemap.xml`.
3. Expected status: **Success**, 23 discovered URLs.
4. `robots.txt` already declares the sitemap, so Google will also find it via crawl.

**Do not** submit `/thank-you` — it is `Disallow`ed in robots and excluded from the sitemap by
design.

---

## 3. Indexing validation

1. **URL Inspection** each of the 11 commercial pages (10 landing + `/services`) plus the
   homepage:
   - Home, /services, /home-cleaning, /deep-cleaning, /move-in-out-cleaning,
     /holiday-home-cleaning, /office-commercial-cleaning, /specialized-cleaning, /pest-control,
     /ac-service-dubai, /handyman-services, /annual-maintenance
2. For each: click **Request Indexing** to accelerate first crawl.
3. Over the first 1–2 weeks, watch **Pages → Indexed** climb toward 23.
4. Investigate anything under **Not indexed**:
   - "Crawled – currently not indexed" is normal for new pages; give it time.
   - "Duplicate without user-selected canonical" would indicate a canonical problem — none is
     expected, since every page self-canonicalises.
   - "Excluded by robots.txt" should only ever be `/thank-you`.

---

## 4. Coverage monitoring

Weekly for the first month, then monthly:

| Report | What to watch |
|---|---|
| **Pages (Indexing)** | Indexed count stable at ~23; no unexpected "Not indexed" growth |
| **Page with redirect** | Should list only the 15 intended redirects |
| **Not found (404)** | Should be empty; investigate any that appear |
| **Crawled – not indexed** | New pages may sit here briefly; escalate if a core page stays >4 weeks |

---

## 5. Enhancement / structured-data reports

The site emits Service, BreadcrumbList and FAQPage schema. Search Console surfaces the ones it
supports:

1. **Breadcrumbs** report — expect all 11 commercial pages valid.
2. **FAQ** (Merchant/rich-result eligibility varies by Google's current policy) — monitor for
   validity errors even if rich results are not granted.
3. Validate individual pages any time in the **Rich Results Test**
   (search.google.com/test/rich-results) — check Service, Breadcrumb and FAQ parse with 0 errors.
4. **Service** schema is not a dedicated Search Console report, but the Rich Results Test and
   Schema.org validator both confirm it parses.

Fix any error Search Console flags at the source in `build/template.py`, rebuild, redeploy — never
hand-edit the generated HTML.

---

## 6. Core Web Vitals

1. **CWV report** appears once Google has enough field (CrUX) data — typically a few weeks after
   real traffic arrives. It will be empty at first; that is expected.
2. Until then, use **PageSpeed Insights** (lab data) on 3–4 landing pages for an early read.
3. Targets: LCP < 2.5s, CLS < 0.1, INP < 200ms (mobile).
4. The architecture is built for this (text LCP, lazy images with fixed dimensions, minimal JS),
   but **only field data confirms it** — this is the one performance claim that must be measured
   post-launch, not assumed.

---

## 7. Manual actions & security

1. Check **Security & Manual actions → Manual actions**: must read "No issues detected."
2. Check **Security issues**: must read "No issues detected."
3. If a manual action ever appears, do not deploy new content until it is understood and a
   reconsideration request is filed. None is expected — the site has original content, no cloaking,
   no fabricated structured data.

---

## 8. URL Inspection (ongoing tool)

Use it whenever you:
- Publish or materially change a page → inspect → Request Indexing.
- Suspect a canonical or crawl problem → "Test live URL" shows what Googlebot sees now.
- Want to confirm the rendered page (Google renders JS) matches expectations — useful given the
  site's small amount of JS.

---

## 9. Performance monitoring (the growth signal)

Weekly, in **Performance → Search results**:

| Dimension | Use |
|---|---|
| **Queries** | Which searches show/click the pages. Watch for the 10 primary keywords entering, then climbing. |
| **Pages** | Clicks and impressions per landing page. Spot underperformers. |
| **Query × Page** | The key report — if a query ranks on the "wrong" page, refine that page's targeting or add an internal link. This is how you catch cannibalization early. |
| **CTR × Position** | A page ranking well (pos 1–5) with low CTR signals a weak title/description — rewrite in `build/content_*.py`. |
| **Countries / Devices** | Confirm UAE dominance and strong mobile share (expected for Dubai home services). |

Feed clicks, impressions, CTR and average position into the **Monthly Tracker** sheet of
`SEO_KPI_DASHBOARD.xlsx`.

---

## 10. Setup checklist

- [ ] Domain property added and DNS-verified
- [ ] URL-prefix `https://www.nacravo.com/` property added
- [ ] `www` canonical confirmed (non-www 301s to www)
- [ ] `sitemap.xml` submitted, 23 URLs, status Success
- [ ] 12 core pages inspected + indexing requested
- [ ] Breadcrumb & FAQ enhancement reports checked
- [ ] No manual actions / security issues
- [ ] Rich Results Test passed on 3 sample pages
- [ ] PageSpeed Insights run on 3 pages (interim CWV)
- [ ] Performance report bookmarked; weekly review scheduled
- [ ] (Optional) Link Search Console to GA4 and to Google Ads for joined reporting
