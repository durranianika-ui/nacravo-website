# Conversion Rate Optimisation Roadmap — Nacravo

**Prepared:** 21 July 2026
**Premise:** the pages already convert well by construction (form above the fold, service
preselection, three CTA routes, low friction). CRO from here is **incremental testing**, not
redesign. Do not rebuild pages; test one variable at a time.

**Measurement:** the primary conversion is the `generate_lead` event. **Before running any test,
pause the duplicate GA4 tag** (see GTM guide) or every result will be measured on 2×-inflated
numbers. Also note leads split across three routes (form, WhatsApp, phone) — count all three.

---

## Testing method

- **One variable per test.** Two changes at once = uninterpretable result.
- **Adequate sample.** Home-services lead volume is modest; give each test enough time/traffic to
  reach significance rather than calling it early. If volume is low, prefer sequential tests with
  clear before/after windows over true split tests.
- **Segment desktop vs mobile** — behaviour differs and the fixes often do too.
- **Track the full funnel:** form starts, form completes, WhatsApp clicks, phone clicks — a change
  can shift leads between routes without changing the total.
- **A/B tooling:** since this is static HTML on Vercel, use Google Optimize's successor / a
  lightweight client-side experiment via GTM, or sequential deploys with GA4 annotations. Keep the
  experiment JS out of the critical render path.

---

## Priority 1 — Highest expected impact

### 1. Pricing presence (the biggest gap)
- **Hypothesis:** showing "from AED X" ranges reduces bounce from price-sensitive searchers.
- **Test:** add honest starting ranges to 2–3 pages; compare lead rate vs the no-price versions.
- **Guardrail:** only real, verified prices. Do not invent. This is blocked on the business
  supplying numbers.
- **Why first:** the pages currently explain *how* pricing works but give no figure — the most
  common reason a comparison shopper leaves.

### 2. Trust — reviews once they exist
- **Hypothesis:** a genuine star rating + count lifts conversion more than any copy change.
- **Test:** once 20+ real reviews exist, add a review block above the fold on 2–3 pages; measure.
- **Guardrail:** real reviews only; activate `AggregateRating` schema in parallel.

### 3. Hero headline clarity
- **Hypothesis:** a benefit-led H1 variant converts better than the current descriptive one.
- **Test:** e.g. `/deep-cleaning` "Deep Cleaning Services in Dubai" vs a variant leading with the
  outcome ("A Deep Clean That Passes Inspection — Dubai"). Keep the keyword in both.
- **Measure:** form-start rate.

---

## Priority 2 — Strong candidates

### 4. Primary CTA button copy
- Test "Get my free quote" vs "Get my fixed price" vs "Message us on WhatsApp" as the primary
  button label. Button-copy tests are cheap and often move rates.

### 5. Form length / fields
- **Hypothesis:** the current 4 required fields are near-optimal, but test 3 (drop Location to
  optional, ask it in WhatsApp) vs 4.
- **Measure:** completion rate vs lead quality (fewer fields can mean lower-quality leads —
  watch both).

### 6. Trust badges — which four
- Test the current set (employed team / fixed price / photo report / materials included) against a
  variant swapping one for "licensed & insured" or "same-day subject to availability".
- **Measure:** form-start rate.

### 7. Sticky CTA (mobile)
- Test the current sticky Call+WhatsApp bar against a variant that also surfaces a "Get a quote"
  scroll-to-form button. **Guardrail:** must not overlap the form or floating elements (the
  breakpoint-exclusive design must be preserved).

---

## Priority 3 — Refinements

### 8. FAQ placement and count
- Test moving the 2–3 most common objections (price, who enters your home, what if it's wrong)
  higher up vs the current lower FAQ. Measure scroll depth and lead rate.

### 9. Hero image presence / choice
- **Hypothesis:** the image beside the form aids or distracts.
- **Test:** with-image vs without on 1–2 pages; and test the specific image on pest control / AC
  once real photography exists.
- **Guardrail:** must not push the form or CTAs below the fold (the current layout keeps all
  conversion elements above the fold — any variant must preserve that; re-measure).

### 10. Mid-page vs closing CTA density
- Test whether the current CTA repetition (hero → per-section → mid-band → closing band) is
  optimal or whether one fewer band reduces fatigue.

### 11. WhatsApp prefilled message
- Test the current structured message vs a shorter one; a shorter prefill can increase send-through
  while a structured one improves lead quality. Measure both.

### 12. Review placement (once reviews exist)
- Test a review strip directly under the form vs lower on the page.

---

## What NOT to test / change

- ❌ Do not remove the above-the-fold form — it is the core conversion asset.
- ❌ Do not add the WhatsApp floating + sticky bar to the same breakpoint (they are mutually
  exclusive by design to avoid overlap).
- ❌ Do not introduce autoplay video, sliders, or heavy interstitials — they hurt both CWV and
  Landing Page Experience.
- ❌ Do not fabricate urgency ("only 2 slots left"), fake reviews, or invented guarantees.
- ❌ Do not change branding as part of a CTA test (the button-contrast decision is separate — see
  accessibility report).

---

## Measurement checklist per test

- [ ] Duplicate GA4 tag already paused (clean baseline)
- [ ] One variable changed
- [ ] Desktop and mobile segmented
- [ ] All three lead routes counted (form / WhatsApp / phone)
- [ ] Lead **quality** checked, not just quantity (WhatsApp conversations → real jobs)
- [ ] GA4 annotation added on the change date
- [ ] Result recorded; winner rolled into `build/` source (never hand-edit generated HTML)

---

## Sequencing

1. **Pre-req:** pause the duplicate GA4 tag; set a conversion value.
2. **Months 1–2:** pricing presence + CTA copy (fastest to run).
3. **Months 3–4:** reviews block (once reviews exist) + headline clarity.
4. **Months 5–6:** form length + trust badges + FAQ placement.
5. **Ongoing:** fold winners back into the generator; re-test seasonally.
