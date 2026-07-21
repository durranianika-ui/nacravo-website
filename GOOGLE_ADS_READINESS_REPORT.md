# Google Ads Readiness Report

**Prepared:** 20 July 2026
**Scope:** the ten service landing pages, assessed as PPC destinations.
**Conversion setup:** Google Ads conversion ID `18246691744`, label `J2SlCMja0M0cEKDX2fxD`,
fired from GTM on the custom `generate_lead` event. Verified single-fire.

---

## 1. Executive assessment

The ten landing pages are **ready to receive paid traffic.** Ad-group-to-page mapping is clean,
message match is strong, and the conversion path is short and instrumented correctly.

Two things hold the account back from being fully production-ready, and **neither is a landing
page problem**:

1. **Conversion value is 0** — Smart Bidding cannot optimise toward value.
2. **A duplicate GA4 tag** inflates GA4 lead reporting 2× (Google Ads conversions themselves are
   clean — see `GTM_AUDIT_REPORT.md`).

---

## 2. Landing page analysis

Assessed per page against the factors Google actually evaluates.

| Page | Message match | Hero clarity | CTA | Trust | Form | Mobile | Speed | Overall |
|---|---|---|---|---|---|---|---|---|
| `/home-cleaning` | Strong | Strong | Strong | Good | Strong | Strong | Strong | **Ready** |
| `/deep-cleaning` | Strong | Strong | Strong | Good | Strong | Strong | Strong | **Ready** |
| `/move-in-out-cleaning` | Strong | Strong | Strong | Good | Strong | Strong | Strong | **Ready** |
| `/holiday-home-cleaning` | Strong | Strong | Strong | Good | Strong | Strong | Strong | **Ready** |
| `/office-commercial-cleaning` | Strong | Strong | Strong | Good | Strong | Strong | Strong | **Ready** |
| `/specialized-cleaning` | Strong | Strong | Strong | Good | Strong | Strong | Strong | **Ready** |
| `/pest-control` | Strong | **Weak visual** | Strong | Moderate | Strong | Strong | Strong | **Ready, weakest** |
| `/ac-service-dubai` | Strong | **No hero image** | Strong | Strong | Strong | Strong | Strong | **Ready** |
| `/handyman-services` | Strong | Strong | Good | Good | Strong | Strong | Strong | **Ready** |
| `/annual-maintenance` | Strong | Strong | Good | Good | Strong | Strong | Strong | **Ready** |

### Message match

Every page's H1 names the exact service and the city — `Home Cleaning in Dubai`,
`Pest Control Services in Dubai`, `AC Service in Dubai`. A visitor arriving on a
"deep cleaning Dubai" query sees those words in the first line, in the title tag, and in the
preselected form field.

**Sub-service anchors extend this to ad-group depth.** 77 anchor sections exist. An ad group for
"AC chemical wash" can point at `/ac-service-dubai#chemical-wash`, and the visitor lands on
matching copy with **both** the service and sub-service preselected in the form. This is the
single strongest Quality Score asset in the build.

### Above the fold — measured, not assumed

| Viewport | Form visible | CTAs visible | Trust badges |
|---|---|---|---|
| 1280×720 desktop | Bottom at 610px ✅ | 561px ✅ | 491px ✅ |
| 768×1024 tablet | Bottom at 863px ✅ | ✅ | ✅ |
| 375×812 mobile | Heading + first two fields ✅ | Below form (by design) | Below form |

Mobile deliberately orders **H1 → description → form**, so the form is the first interactive
element after the pitch.

---

## 3. Quality Score assessment

Google scores three components. Landing pages influence one directly and one indirectly.

### Landing Page Experience — expected "Above average"

| Factor | Status |
|---|---|
| Relevant, specific content | 2,016–3,608 words per page, service-specific |
| Transparency | Clear about what is offered; no fake claims, no hidden pricing tricks |
| Navigability | Breadcrumbs, jump links, header dropdown, related services |
| Load speed | Text-first LCP, shared cached CSS/JS, lazy images |
| Mobile usability | No horizontal scroll, 44px+ targets, form-first ordering |
| Original content | Written for this site; not scraped or spun |

**Baseline comparison:** previously all paid traffic landed on the homepage regardless of query.
Moving to ten dedicated pages is the largest single Quality Score improvement available, and it
is done.

### Ad Relevance — supported, but owned by ad copy

The pages give ad copy the keywords to mirror. Recommended: use the H1 phrasing in Headline 1 and
sub-service names in Headline 2 so the ad and page read as one unit.

### Expected CTR — not a landing page factor

Driven by ad copy, extensions and position. Landing pages contribute only indirectly. **No CTR
figure is projected here** — any number would be invented.

---

## 4. Keyword alignment

| Ad group | Landing page | Deep-link opportunity |
|---|---|---|
| Home / regular cleaning | `/home-cleaning` | `#weekly-cleaning`, `#monthly-cleaning`, `#hourly-cleaning` |
| Deep cleaning | `/deep-cleaning` | `#kitchen-deep-cleaning`, `#bathroom-deep-cleaning`, `#post-construction` |
| Move out / end of tenancy | `/move-in-out-cleaning` | `#end-of-tenancy`, `#oven-cleaning`, `#empty-property` |
| Airbnb / holiday home | `/holiday-home-cleaning` | `#airbnb-cleaning`, `#linen-replacement` |
| Office / commercial | `/office-commercial-cleaning` | `#daily-contracts`, `#office-carpet-shampoo`, `#fit-out` |
| Sofa / carpet / mattress | `/specialized-cleaning` | `#sofa-cleaning`, `#carpet-cleaning`, `#mattress-cleaning` |
| Pest control | `/pest-control` | `#bed-bugs`, `#cockroach-control`, `#rodent-control` |
| AC service / chemical wash | `/ac-service-dubai` | `#chemical-wash`, `#duct-cleaning`, `#repair`, `#gas-top-up` |
| Handyman / plumber / electrician | `/handyman-services` | `#plumbing`, `#electrical`, `#painting`, `#tv-mounting` |
| AMC / maintenance contract | `/annual-maintenance` | `#villa-amc`, `#apartment-amc`, `#mep-inspection` |

**Geo targeting note.** `/ac-service-dubai` states coverage of **Downtown Dubai, Business Bay and
DIFC only**. The AC campaign's location targeting must match, or the ad will promise a service
the page declines. All other pages state Dubai-wide availability and can be targeted broadly.

**Vanity redirects are live** for `/sofa-cleaning`, `/plumbing`, `/electrical`, `/painting`,
`/amc`, `/airbnb-cleaning`, `/office-cleaning`, `/move-in-cleaning`, `/move-out-cleaning`,
`/ac-services`. These are useful in ad copy display paths but **final URLs should point at the
real destination**, not the redirect — Google Ads penalises unnecessary redirects on final URLs.

---

## 5. Conversion optimisation

### What is working

| Element | Implementation |
|---|---|
| Lead form above the fold | Verified at three viewports |
| Friction | 4 required fields (Name, Phone, Service, Location). Email removed entirely |
| Service preselection | Per page, plus sub-service from the anchor |
| Three conversion routes | Form, WhatsApp, phone — on every page |
| CTA repetition | Hero, per sub-service section, mid-page band, closing band, sticky mobile bar, desktop floating button |
| Trust above the fold | 4 badges: employed vetted team, fixed price upfront, photo report, materials included |
| Objection handling | Pricing explainer, 4-step process, 6–23 FAQs per page |
| WhatsApp handover | Structured, pre-filled enquiry — reduces drop-off between form and conversation |

### Remaining conversion friction, ranked

| # | Issue | Impact | Fix |
|---|---|---|---|
| 1 | **No prices anywhere** | Price-sensitive searchers bounce to competitors showing ranges. In Dubai home services, "from AED X" is the norm. | Publish verified starting ranges per service |
| 2 | **No reviews or ratings** | Weakest trust signal on the page. Competitors show Google star ratings in ads via seller ratings and on-page | Collect Google reviews (see §7) |
| 3 | Conversion value 0 | Blocks value-based bidding | See §6 |
| 4 | Pest control has one image | Lowest visual trust of the ten | Commission photography |
| 5 | AC page has no hero image | Slightly weaker first impression on the highest-intent page | Commission photography |
| 6 | No live chat / callback | WhatsApp partly covers this | Optional |

**Ranked #1 for a reason.** Of everything remaining, publishing price ranges is most likely to
move conversion rate. The pages currently explain *how* pricing works — fixed quote, per-unit,
parts shown first — which is honest and good, but a searcher comparing three companies still
cannot tell whether Nacravo is in their budget.

---

## 6. Conversion values — recommendation

**Current state:** the site pushes `value: 0, currency: "AED"`. The Ads tag reads `{{value}}`.
Every conversion is therefore worth zero, and value-based bidding cannot function.

### Option 1 — Static value per conversion action *(recommended starting point)*

Set one default value in Google Ads (Goals → Conversions → edit action → Value).

- **Pros:** no code change, works immediately, sufficient for tROAS to have *something* to optimise.
- **Cons:** treats an AMC contract enquiry the same as a one-off hourly clean.
- **How to set it:** average lead value = average job value × lead-to-customer close rate.
  Nacravo must supply both. Do not guess them.

### Option 2 — Dynamic value per service *(recommended once Option 1 is stable)*

Push a per-service estimated value in the `generate_lead` event, so an AMC or villa deep-clean
lead is weighted above an hourly clean.

- **Site change required:** one small addition to the lead handler mapping service → value.
- **GTM change required:** none — the tag already reads `{{value}}`.
- **Pros:** Smart Bidding shifts budget toward high-value services.
- **Cons:** needs a realistic value table from the business; wrong numbers actively misdirect spend.

### Option 3 — Offline conversion import *(the accurate one, later)*

Capture GCLID at form submit, store it against the lead, and upload actual closed revenue back
to Google Ads.

- **Pros:** optimises to real revenue, not estimates. The genuine end state.
- **Cons:** requires a CRM or at minimum a structured lead log, plus a recurring upload process.
  The current lead flow hands over to WhatsApp and stores a local browser record — **not
  sufficient** for this without a CRM step.

### Option 4 — Revenue import via GA4

Only relevant if transactions are recorded in GA4, which they are not — Nacravo does not
transact on-site. **Not applicable.**

### Recommended bidding progression

| Stage | Conditions | Strategy |
|---|---|---|
| Launch | No conversion history | **Maximise Clicks** with a CPC cap, purely to gather data |
| ~15–30 conversions/month | History exists, value still static | **Maximise Conversions**, then add a target CPA |
| Values implemented (Option 1 or 2) | Values differentiated | **Maximise Conversion Value**, then target ROAS |
| Offline import running | Real revenue flowing back | **Target ROAS** on true revenue |

**Do not start on tROAS.** With every conversion valued at 0 — or all valued identically — the
algorithm has nothing to optimise and will underperform Maximise Conversions.

---

## 7. Review strategy

**No fake reviews. No invented ratings. No fabricated testimonials.** Five unverified
testimonials were already removed from the AC page during this project.

### Why this matters commercially

Review schema is the single highest-leverage trust addition still available, and it is blocked
purely on collecting genuine reviews.

### Workflow

1. **Ask at the right moment** — immediately after the photo report is sent, which is the point
   of peak satisfaction and already an existing touchpoint in the service flow.
2. **Ask on WhatsApp**, the channel the customer already uses. A short message with a direct
   Google review link converts far better than email.
3. **Make it one tap** — use the Google "write a review" short link from the Business Profile.
4. **Never incentivise.** Paying or discounting for reviews violates Google's policies and risks
   the profile.
5. **Respond to every review**, positive and negative. Response rate is a visible quality signal.

### Then, and only then — schema activation

Once a genuine corpus exists (**suggested minimum: 20+ reviews with a stable average**):

- Add `AggregateRating` to the `Organization` / `HomeAndConstructionBusiness` schema on the
  homepage, reflecting the **real** Google rating and count.
- Optionally add `Review` markup for individually consented, attributable reviews.
- **Do not** mark up reviews that are not displayed on the page — Google requires the marked-up
  content to be visible to users.

### On-page trust improvements available now, without reviews

The AC page's "Our standards" section is the model: employed and vetted technicians, documented
photo reports, priced before work, focused coverage. Extending that pattern to the other nine
pages adds trust without a single unverifiable claim.

Also available now: trade licence number and VAT TRN, currently placeholder comments in the
footer. In the UAE market these are meaningful legitimacy signals.

---

## 8. Google Business Profile plan

GBP is the highest-leverage local asset **not** in this repository, and it directly supports paid
performance through location extensions and local ads.

### Categories

| | |
|---|---|
| **Primary** | House Cleaning Service |
| **Secondary** | Commercial Cleaning Service · Air Conditioning Repair Service · Handyman · Pest Control Service · Carpet Cleaning Service · Upholstery Cleaning Service · Building Maintenance |

Primary category carries the most ranking weight — set it to the highest-volume, highest-margin
service. If AC servicing is the commercial priority rather than cleaning, make that primary
instead. That is a business call.

### Services — map one-to-one with landing pages

Each GBP service entry should carry a short description and link to its page:

| GBP service | Landing page |
|---|---|
| Home Cleaning | `/home-cleaning` |
| Deep Cleaning | `/deep-cleaning` |
| Move In / Move Out Cleaning | `/move-in-out-cleaning` |
| Holiday Home Cleaning | `/holiday-home-cleaning` |
| Office & Commercial Cleaning | `/office-commercial-cleaning` |
| Sofa & Carpet Cleaning | `/specialized-cleaning` |
| Pest Control | `/pest-control` |
| AC Service & Chemical Wash | `/ac-service-dubai` |
| Handyman Services | `/handyman-services` |
| Annual Maintenance Contract | `/annual-maintenance` |

### Business description (750 char limit)

Draft, using only verified facts:

> Nacravo provides home cleaning and property maintenance across Dubai. Our technicians are
> employed by us, background-checked, uniformed and trained to one checklist — not dispatched
> from a marketplace. Services include regular and deep cleaning, move-in and move-out cleaning,
> holiday home turnovers, office and commercial cleaning, sofa and carpet cleaning, pest control,
> handyman work and annual maintenance contracts. Premium AC servicing, chemical washing and duct
> cleaning currently focus on Downtown Dubai, Business Bay and DIFC. Materials and equipment are
> included, you approve a fixed price before work begins, and every visit ends with a
> before-and-after photo report. Book on WhatsApp, by phone or through our website.

### Service area

Set to **Dubai** generally. Do **not** list AC-specific districts at profile level — it would
contradict the site. Handle AC scoping in the AC service description instead.

### Photos required

GBP rewards regular, genuine photo uploads. Current gaps mirror the site's:

| Type | Have? | Note |
|---|---|---|
| Logo + cover | Yes | Use the green brand logo |
| Team | Yes | `hero4`, `team-quality`, `hero-team` |
| Cleaning at work | Yes | `svc-cleaning`, `svc-cleaning2`, `hero3` |
| Maintenance at work | Yes | `svc-maintenance`, `svc-maintenance2` |
| Before/after | Yes | The `ba-*` set |
| **AC servicing** | **No** | Commission |
| **Pest control** | **No** | Commission |
| Vehicles / branding | Unknown | Add if branded vehicles exist |

### Posts

Weekly cadence, each linking to the relevant landing page. Seasonal angles that are genuinely
useful: AC servicing before summer, deep cleaning before Ramadan and Eid, move-out cleaning at
month and quarter end when tenancy dates cluster.

### Q&A

Seed the Q&A with real questions already answered in the site FAQs — coverage areas, what a
service includes, how pricing works, how to book. Owner-posted Q&A is permitted and useful; do
**not** post fake questions from fake accounts.

### Local citations

Consistent NAP across UAE directories. The prerequisite is done: the site now uses exactly one
phone number, one email and one WhatsApp number sitewide.

---

## 9. Expected strengths and remaining improvements

### Strengths going into launch

- Ten dedicated, deep, service-specific landing pages replacing a single homepage destination
- Sub-service anchors enabling true ad-group-level message match
- Form above the fold with service preselection and only four required fields
- Three conversion routes with a WhatsApp handover suited to the Dubai market
- Conversion tracking verified single-fire, with a dedupe guard against double clicks
- Honest content — no fabricated claims that could trigger a policy issue

### Remaining improvements, ranked

| Priority | Item | Owner |
|---|---|---|
| **Critical** | Set a conversion value (Option 1 minimum) | Marketing |
| **Critical** | Pause the duplicate GA4 tag so lead reporting is accurate | GTM admin |
| **Critical** | Verify no GA4-imported conversion double-counts against tag 49 in Ads | Marketing |
| High | Publish price ranges | Business owner |
| High | Start review collection | Operations |
| High | Google Business Profile completion | Marketing |
| High | Commission pest control + AC photography | Marketing |
| Medium | Align AC campaign geo targeting to the three districts | Marketing |
| Medium | Point final URLs at real pages, not vanity redirects | Marketing |
| Medium | Add trade licence + VAT TRN to the footer | Business owner |
| Low | Consider callback / live chat | Marketing |
