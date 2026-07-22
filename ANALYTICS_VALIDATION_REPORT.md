# Analytics Validation Report

**Prepared:** 21 July 2026
**Method:** every event exercised in a real browser against the running site, inspecting
`window.dataLayer` directly. `window.open` was stubbed during form tests so the submit completes
without navigating away.

---

## 1. The critical chain

**Requirement:** one successful form submission → one `generate_lead` → one Google Ads
conversion → no duplicates.

| Step | Result |
|---|---|
| Valid form submission | ✅ Fires exactly **one** `generate_lead` dataLayer event |
| Double-clicked submit | ✅ Still **one** — guarded by the one-shot `leadSent` flag + disabled button |
| Invalid submit (empty required fields) | ✅ **Zero** `generate_lead`; three fields flagged invalid, first focused |
| `generate_lead` → GTM tag 25 (GA4) | ✅ Fires once (site-side) |
| `generate_lead` → GTM tag 49 (Google Ads conversion) | ✅ **One** conversion tag, single-fire |
| `generate_lead` → GTM tag 48 (GA4 duplicate) | ⚠️ **Also fires — GA4 records the event twice.** Google Ads is unaffected. See `GTM_AUDIT_REPORT.md`. |

**Verdict:** the website side of the chain is correct. The only duplication is a **GA4-only,
GTM-side** issue (two GA4 tags on one trigger), not a site-code or Google-Ads issue.

### Verified payload (landing-page form)

```
event:            generate_lead
form_name:        lead_form
lead_type:        whatsapp
service_name:     Office & Commercial Cleaning
subservice_name:  Daily Contracts       (preselected from #daily-contracts anchor)
location:         DIFC
value:            0                       <- see conversion-value recommendation
currency:         AED
```

---

## 2. Every conversion event

| Event | Trigger | Test result | Dedupe |
|---|---|---|---|
| `generate_lead` | valid form submit | ✅ one per submit | one-shot `leadSent` |
| `form_submit` | homepage enquiry form | ✅ fires on homepage | — |
| `whatsapp_click` | any `wa.me` link | ✅ one per click; **second click within 1.2s suppressed** | `DEDUP_MS` guard |
| `phone_click` | any `tel:` link | ✅ one per click | `DEDUP_MS` guard |
| `quote_click` | `[data-track="quote"]` | ✅ fires | `DEDUP_MS` guard |
| `cta_click` | quote/booking CTAs | ✅ fires (paired with quote/booking) | `DEDUP_MS` guard |
| `booking_click` | `[data-track="booking"]` | ✅ fires | `DEDUP_MS` guard |
| `service_view` | homepage service cards | ✅ fires | `DEDUP_MS` guard |
| `page_view` | every page load | ✅ one per load | — |
| `outbound_click` | external non-WhatsApp links | ✅ fires | `DEDUP_MS` guard |

The `DEDUP_MS` guard (1200 ms) was verified live: two WhatsApp clicks in immediate succession
produced **one** `whatsapp_click` event.

---

## 3. Behavioural checks

| Check | Result |
|---|---|
| Service preselected in form | ✅ Per page (e.g. "Office & Commercial Cleaning") |
| Sub-service preselected from anchor | ✅ Landing on `#daily-contracts` preselects "Daily Contracts" |
| Sub-service preselected from CTA click | ✅ Section CTAs set the matching sub-service |
| Form validation blocks bad submits | ✅ 3 invalid fields flagged, first focused, no event |
| Submit button disables after success | ✅ Prevents a second submit entirely |
| WhatsApp handover message | ✅ Structured, pre-filled, correct number `971555403038` |

---

## 4. Homepage vs landing-page event difference

An intentional, documented inconsistency — **not** a defect:

| Form | Events on submit |
|---|---|
| Homepage (`enquiry_form`) | `form_submit` **and** `generate_lead` |
| Landing pages (`lead_form`) | `generate_lead` only |

Both fire `generate_lead` exactly once, so **conversion tracking is identical and correct on
both**. The homepage additionally fires `form_submit` (GTM tag 34), which is a secondary
engagement event, not a conversion. If uniform reporting is wanted, add a `form_submit` push to
the landing-page handler — but it is not required for conversion accuracy, and doing so must not
disturb the single `generate_lead`.

---

## 5. Consent Mode v2

| Check | Result |
|---|---|
| Consent defaults set **before** GTM loads | ✅ Inline script ahead of the GTM snippet |
| Default state | Denied for ad + analytics storage until opt-in |
| Stored | `localStorage.nacravo_consent` |
| Update on accept/reject | ✅ Pushes `consent update` and a `consent_update` dataLayer event |
| Floating WhatsApp clears the banner | ✅ `body.cc-open` lifts it while consent is pending |

---

## 6. Findings and actions

| # | Finding | Severity | Action | Owner |
|---|---|---|---|---|
| 1 | Duplicate GA4 `generate_lead` tag (25 + 48) | **Critical** | Pause tag 48 in GTM | GTM admin |
| 2 | Possible GA4-imported conversion double-counting in Ads | **Critical** | Verify only one primary lead conversion action in Google Ads | Marketing |
| 3 | Conversion value is 0 | High | Set a value (see Ads report §6) | Marketing |
| 4 | Landing pages omit `form_submit` | Low | Optional; add for uniform reporting | Dev |
| 5 | 3 paused duplicate tags in GTM | Low | Delete after confirming obsolete | GTM admin |

**Site code requires no change for conversion accuracy.** Everything above #4 is a GTM console
or Google Ads account action.
