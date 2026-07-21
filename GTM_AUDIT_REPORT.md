# GTM Audit Report — Container GTM-KD4PH4XP

**Prepared:** 20 July 2026
**Container version audited:** 4 (live, published)
**Method:** the published `gtm.js` that GTM serves to browsers was fetched and parsed by
`build/gtm_audit.py`. This is the authoritative record of what actually runs, and is
read-only — **no GTM change has been made.**

> **Note on tag names.** GTM strips human-readable tag and trigger names from the published
> container. This report keys off **tag IDs**, which are what the GTM UI shows in the tag list.
> Names are not invented here; look each ID up in the GTM console.

---

## 1. Container summary

| | |
|---|---|
| Variables / macros | 29 |
| Triggers | 12 predicates across 12 rules |
| Tags | 18 (15 active, 3 paused) |
| GA4 destination | `G-N2VGBEBELF` (single measurement ID) |
| Google Ads conversion ID | `18246691744` |
| Google Ads conversion label | `J2SlCMja0M0cEKDX2fxD` |

**Important:** the repository file `gtm-nacravo-container.json` describes only **3 tags**. It is
stale by 15 tags and must not be used for auditing. See Technical Debt.

---

## 2. Tag inventory

| Tag ID | Type | Event | Destination | Fires on |
|---|---|---|---|---|
| 5 | Conversion Linker | — | — | `gtm.js` |
| **17** | **PAUSED** | — | — | would fire on `generate_lead` |
| **19** | **PAUSED** | — | — | would fire on `phone_click` |
| **25** | **GA4 Event** | **`generate_lead`** | **G-N2VGBEBELF** | **`generate_lead`** |
| 27 | GA4 Event | `cta_click` | G-N2VGBEBELF | `cta_click` |
| 29 | GA4 Event | `booking_click` | G-N2VGBEBELF | `booking_click` |
| 30 | GA4 Event | `quote_click` | G-N2VGBEBELF | `quote_click` |
| 31 | GA4 Event | `service_view` | G-N2VGBEBELF | `service_view` |
| 34 | GA4 Event | `form_submit` | G-N2VGBEBELF | `form_submit` |
| 36 | GA4 Event | `whatsapp_click` | G-N2VGBEBELF | `whatsapp_click` |
| **40** | **PAUSED** | — | — | would fire on `whatsapp_click` |
| 41 | GA4 Event | `page_view` | G-N2VGBEBELF | `page_view` |
| 42 | GA4 Event | `outbound_click` | G-N2VGBEBELF | `outbound_click` |
| 43 | Google Tag (config) | — | G-N2VGBEBELF | `gtm.init` |
| 44 | GA4 Event | `phone_click` | G-N2VGBEBELF | `phone_click` |
| 45 | Conversion Linker | — | — | `gtm.js` |
| **48** | **GA4 Event** | **`generate_lead`** | **G-N2VGBEBELF** | **`generate_lead`** |
| 49 | Google Ads Conversion | — | AW-18246691744 | `generate_lead` |

## 3. Trigger inventory

All 12 triggers are **custom event** triggers using an equality match on the dataLayer `event` key:

`gtm.js` · `gtm.init` · `page_view` · `generate_lead` · `form_submit` · `quote_click` ·
`booking_click` · `cta_click` · `service_view` · `whatsapp_click` · `phone_click` ·
`outbound_click`

**No built-in trigger fires any tag.** There is no Form Submission, Link Click, Click, History
Change, Element Visibility, Scroll Depth or Timer trigger bound to a tag. GTM's built-in
listeners do push `gtm.formSubmit` and `gtm.linkClick` into the dataLayer, but nothing consumes
them. **This closes the concern raised in the earlier audit — built-in triggers are not a source
of duplicate conversions.**

---

## 4. Duplicate event analysis

### The finding

Two GA4 Event tags fire the same event, to the same property, on the same trigger:

| | Tag 25 | Tag 48 |
|---|---|---|
| Event name | `generate_lead` | `generate_lead` |
| Measurement ID | `G-N2VGBEBELF` | `G-N2VGBEBELF` |
| Trigger | `event = generate_lead` | `event = generate_lead` |
| Parameters | `business_name`, `location`, `page_path`, `page_title`, `form_name`, `service_name`, `lead_type` (7) | `lead_type`, `service_name`, `currency`, `value` (4) |
| `sendEcommerceData` | not set | `false` |
| User properties / EUID | enabled | enabled |

**Result: GA4 records two `generate_lead` events for every single real lead.**

### Which is the correct implementation

**Tag 25 should remain. Tag 48 is the duplicate and should be paused.**

Reasoning:

1. **Tag 25 matches the container's house style.** Every other GA4 event tag in this container
   (27, 29, 30, 31, 34, 36, 41, 42, 44) sends the same four context parameters —
   `business_name`, `location`, `page_path`, `page_title` — plus event-specific ones. Tag 25
   follows that convention exactly; tag 48 does not.
2. **Tag 25 carries more useful reporting context.** `page_path` and `page_title` are what allow
   "which landing page produced this lead" analysis — the single most valuable breakdown for
   this project, given ten landing pages. Tag 48 cannot answer that question at all.
3. **`form_name` distinguishes the two forms.** The homepage uses `enquiry_form`; the landing
   pages use `lead_form`. Only tag 25 sends it.
4. **Tag ID ordering suggests intent.** IDs are assigned sequentially. Tag 25 is long-standing;
   tags 48 and 49 were created together — tag 49 being the Google Ads conversion. The most
   likely history is that tag 48 was added while wiring up Ads conversion tracking, without
   noticing that tag 25 already fired the same event.

### What is lost by pausing tag 48

Tag 48 is the only `generate_lead` tag sending `value` and `currency`. Today this costs
**nothing measurable**, because the site pushes `value: 0` on every lead — the parameter carries
no information. See the conversion-value recommendation in the Google Ads report.

**Recommended follow-up (optional, same GTM edit):** add `value` and `currency` as event
parameters on **tag 25** so the richer tag also carries monetary fields once a real value exists.
This produces one tag with the complete parameter set and nothing is lost.

---

## 5. Impact assessment

### GA4 impact

| Aspect | Effect |
|---|---|
| `generate_lead` event count | **Halves.** This is a correction, not a loss — the current number is inflated 2×. |
| GA4 conversion count (if `generate_lead` is marked as a key event) | Halves, same correction. |
| Conversion rate metrics | Halve, becoming accurate. |
| Reports, explorations, Looker dashboards using `generate_lead` | Will show a visible step change on the date of the fix. |
| Audiences built on `generate_lead` | Membership unaffected — a user who fired the event twice is still one user. |
| Event-scoped parameters | `value` / `currency` disappear from `generate_lead` unless added to tag 25. |

### GA4 historical data

**Historical data cannot be corrected.** GA4 does not support retroactive reprocessing or event
deletion. All `generate_lead` data collected before the fix is inflated approximately 2×.

Recommended handling:
- Add a **GA4 annotation** on the fix date so future analysts understand the discontinuity.
- When comparing periods that straddle the fix, either halve the pre-fix figure or compare only
  post-fix periods.
- Note that the inflation factor is *approximately* 2×, not exactly — both tags fire on the same
  trigger, so barring tag-level errors it should be exactly 2×, but this has not been validated
  against historical GA4 data.

### Google Ads impact

**None from pausing tag 48.**

Tag 49 is the only Google Ads conversion tag, it fires on `generate_lead`, and it is entirely
independent of the GA4 tags. Pausing tag 48 does not touch it.

> **One thing to check in the Google Ads UI before assuming Ads data is clean.**
> This audit proves the *GTM-side* Ads conversion is single-fire. It cannot see whether a
> **GA4-imported conversion action** also exists in the Google Ads account. If `generate_lead`
> was additionally imported from GA4 into Google Ads as a conversion action, that imported
> action inherited the 2× inflation, and it may also be double-counting against the native tag-49
> conversion. **Verify in Google Ads → Goals → Conversions** that only one conversion action for
> leads is set to "Primary / include in Conversions".

### Website code impact

**None.** The site pushes one `generate_lead` event. It is already compatible with the corrected
container, and no code change is required or recommended.

Per the standing rule, Google Ads conversion scripts have **not** been added to the site.
`NACRAVO_TRACKING.GOOGLE_ADS_ID` remains intentionally empty and `LOAD_PIXELS_DIRECTLY` remains
`false`, so GTM stays the single source of truth. **Filling in `GOOGLE_ADS_ID` would create a
second Ads conversion path and genuinely duplicate Ads conversions** — do not do it.

---

## 6. Paused tags

Three tags are paused and inert:

| Tag ID | Would fire on | Note |
|---|---|---|
| 17 | `generate_lead` | **If un-paused, GA4 would record three `generate_lead` events per lead.** |
| 19 | `phone_click` | Duplicate of active tag 44 |
| 40 | `whatsapp_click` | Duplicate of active tag 36 |

These have no runtime effect, but all three are latent duplicates. Recommend deleting them after
confirming they are obsolete, so a future editor cannot un-pause one and silently re-introduce
double counting.

---

## 7. Recommended GTM changes

**None of the following has been performed.** Each requires explicit approval and is a GTM
console action, not a code change.

| # | Change | Priority | Risk | Effort |
|---|---|---|---|---|
| 1 | **Pause tag 48** (GA4 Event, `generate_lead`, 4 params) | **Critical** | Very low — GA4 counts become accurate; Ads unaffected | 2 min |
| 2 | Add `value` and `currency` parameters to **tag 25** | High | None | 5 min |
| 3 | Add a GA4 annotation on the fix date | High | None | 2 min |
| 4 | Verify in Google Ads that no GA4-imported lead conversion double-counts against tag 49 | **Critical** | — | 10 min |
| 5 | Delete paused tags 17, 19, 40 after confirming obsolescence | Medium | Low | 5 min |
| 6 | Once lead values exist, set a real conversion value (see Ads report) | Medium | None | — |

---

## 8. Implementation plan

**Step 1 — Prepare (5 min).** In GTM, open the workspace and locate tags by ID. Confirm tag 48
is the 4-parameter `generate_lead` tag and tag 25 is the 7-parameter one. Screenshot both before
changing anything.

**Step 2 — Preview (10 min).** Enter GTM Preview mode, load a landing page, submit a test lead.
Confirm in the Tag Assistant that **tags 25, 48 and 49 all fire** — this reproduces the defect
and proves you are looking at the right tags.

**Step 3 — Change (2 min).** Pause tag 48. Optionally add `value` and `currency` to tag 25.

**Step 4 — Re-preview (10 min).** Submit another test lead. Confirm:
- Tag 25 fires **once**
- Tag 48 does **not** fire
- Tag 49 (Google Ads) still fires **once**

**Step 5 — Publish (2 min).** Publish the container with a clear version note, for example:
*"Paused duplicate GA4 generate_lead tag (48). Tag 25 retained. GA4 lead counts will halve from
this date — this corrects a 2× inflation. Google Ads conversions unaffected."*

**Step 6 — Verify live (24 h).** Check GA4 realtime for a single `generate_lead` per test
submission, then confirm after a day that the daily count has approximately halved and that
Google Ads conversions are unchanged.

**Step 7 — Annotate.** Add the GA4 annotation.

### Rollback

Un-pause tag 48 and republish. GTM keeps every published version, so reverting to the previous
container version is a two-click operation and takes effect immediately.

---

## 9. Website compatibility statement

The website code is compatible with the corrected container **as-is**, verified by test:

- One valid form submission produces exactly **one** `generate_lead` dataLayer push
- A double-clicked submit still produces exactly **one** (guarded by a one-shot `leadSent` flag)
- An invalid submit produces **none**
- The push carries `form_name`, `lead_type`, `service_name`, `subservice_name`, `property_type`,
  `location`, `value`, `currency` — a superset of what both tags consume

No website change is needed for this remediation, and none has been made.
