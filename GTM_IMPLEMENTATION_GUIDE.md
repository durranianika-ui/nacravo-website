# GTM Implementation Guide — Pause the Duplicate GA4 Lead Tag

**For:** the marketing team / whoever administers GTM container **GTM-KD4PH4XP**
**Prepared:** 21 July 2026
**Estimated time:** 20 minutes including verification
**Risk:** very low, fully reversible

> This is a **step-by-step guide for a human to execute in the GTM UI.** No change has been made
> by the engineering side. The website code does not change and is already compatible with the
> corrected container. See `GTM_AUDIT_REPORT.md` for the full technical analysis this guide is
> based on.

---

## What you are fixing, in one sentence

Two GA4 tags fire the same `generate_lead` event to the same GA4 property on the same trigger, so
**every lead is counted twice in GA4.** You will pause one of them. Google Ads is not affected.

---

## The two tags

| | Tag to KEEP | Tag to PAUSE |
|---|---|---|
| **Tag ID** | **25** | **48** |
| Type | GA4 Event | GA4 Event |
| Event name | `generate_lead` | `generate_lead` |
| Sends to | `G-N2VGBEBELF` | `G-N2VGBEBELF` |
| Trigger | Custom Event = `generate_lead` | Custom Event = `generate_lead` |
| Parameters | `business_name`, `location`, `page_path`, `page_title`, `form_name`, `service_name`, `lead_type` (**7**) | `lead_type`, `service_name`, `currency`, `value` (**4**) |

> **How to find them:** in GTM, open **Tags** in the left sidebar. The list shows a numeric ID
> column. Look for the two tags named for the `generate_lead` GA4 event. If your list shows names
> rather than IDs, open each candidate and confirm the parameter list above — the one with 7
> parameters including `page_path` and `form_name` is **25 (keep)**; the one with 4 parameters
> including `value` and `currency` is **48 (pause)**.

---

## Why pause tag 48 (not tag 25)

1. **Tag 25 matches every other event tag in the container.** All the other GA4 tags
   (`cta_click`, `whatsapp_click`, `phone_click`, etc.) send the same four context parameters —
   `business_name`, `location`, `page_path`, `page_title`. Tag 25 follows that pattern; tag 48
   does not.
2. **Tag 25 tells you which landing page produced the lead.** It sends `page_path` and
   `page_title`. With ten landing pages, "which page converts" is the most valuable report you
   have — and tag 48 cannot answer it.
3. **Tag 25 sends `form_name`**, which distinguishes the homepage form (`enquiry_form`) from the
   landing-page form (`lead_form`).
4. Tag 48 was almost certainly added later, while wiring the Google Ads conversion (tag 49), by
   someone who did not realise tag 25 already fired the event.

**One optional improvement while you are here:** tag 48 is the only lead tag that carries `value`
and `currency`. Today that costs nothing because the site sends `value: 0`. If you want the
richer tag to also carry monetary fields for later, add `value` and `currency` as two event
parameters on **tag 25** before you pause tag 48. This is optional and can be done any time.

---

## Step-by-step

### Step 0 — Before you touch anything (2 min)
1. Open GTM → container **GTM-KD4PH4XP** → make sure you are in a **Workspace** (not a published
   version).
2. Open tag **25** and tag **48**. **Screenshot both** — this is your record of the "before"
   state.
3. Confirm the parameter lists match the table above.

### Step 1 — Reproduce the problem in Preview (5 min)
1. Click **Preview** (top right).
2. Enter a landing page URL, e.g. `https://www.nacravo.com/home-cleaning` (or the local/staging
   URL if testing before launch).
3. In the connected Tag Assistant window, fill in the lead form (Name, Phone, Service, Location)
   and submit.
4. In Tag Assistant, look at the **`generate_lead`** event in the left timeline. Under **Tags
   Fired** you should see **both tag 25 and tag 48**, plus the Google Ads conversion (tag 49).
   **This confirms the duplicate.**

### Step 2 — Pause tag 48 (2 min)
1. Go to **Tags** → open tag **48**.
2. Top-right **⋮ (three-dot menu)** → **Pause**.
3. The tag list will now show a "paused" indicator on tag 48.
4. *(Optional, recommended)* Open tag **25**, and under **Event Parameters** add:
   - `value` → value `{{value}}` (this variable already exists in the container)
   - `currency` → value `{{currency}}`

### Step 3 — Re-verify in Preview (5 min)
1. Click **Preview** again (or refresh the existing preview).
2. Submit another test lead.
3. On the `generate_lead` event, confirm under **Tags Fired**:
   - ✅ Tag **25** fires **once**
   - ✅ Tag **48** does **not** fire (it will appear under "Tags Not Fired")
   - ✅ Tag **49** (Google Ads conversion) still fires **once**

### Step 4 — Publish (2 min)
1. Click **Submit** (top right).
2. **Version Name:** `Pause duplicate GA4 generate_lead tag (48)`
3. **Version Description:**
   > Paused tag 48. Tag 25 retained as the single GA4 generate_lead tag. GA4 lead counts will
   > drop ~50% from this date — this corrects a 2× over-count, it is not a loss of leads. Google
   > Ads conversions unaffected (single conversion tag 49).
4. Click **Publish**.

### Step 5 — Annotate GA4 (2 min)
1. In **GA4 → Admin → (or the Reports timeline) → Annotations**, add an annotation on today's
   date:
   > GTM fix: removed duplicate generate_lead tag. Lead counts before this date are ~2× inflated.

---

## Expected behaviour after pausing

| Where | Before | After |
|---|---|---|
| GA4 `generate_lead` event count | 2 per real lead | **1 per real lead (correct)** |
| GA4 daily lead total | inflated ~2× | **drops ~50% — this is the correction** |
| GA4 conversion rate (if `generate_lead` is a key event) | understated (denominator right, numerator 2×) | **accurate** |
| Google Ads conversions | 1 per lead (already correct) | **unchanged — 1 per lead** |
| Website behaviour | — | **unchanged** |
| GA4 historical data | 2× inflated | **cannot be corrected retroactively** (annotate instead) |

**The GA4 number going down is the whole point.** It will look like leads dropped 50% overnight;
they did not — you stopped double-counting. The annotation is how future analysts understand the
step change.

---

## GA4 DebugView verification (optional, thorough)

1. GA4 → **Admin → DebugView**.
2. With GTM Preview active (it enables debug mode), submit a test lead.
3. In DebugView you should see the `generate_lead` event appear **once**, not twice.
4. Click it and confirm the parameters from tag 25 are present (`page_path`, `page_title`,
   `form_name`, `service_name`, `lead_type`, and — if you added them — `value`, `currency`).

## Google Ads verification (important — separate from GTM)

Pausing tag 48 fixes GA4. **Now confirm Google Ads is not double-counting a different way:**

1. Google Ads → **Goals → Conversions** (or **Tools → Conversions**).
2. Look for **how many conversion actions count leads**:
   - You want **one** action set to **Primary** ("include in Conversions") for a lead.
3. If you see **both** a native tag conversion (from GTM tag 49) **and** a **GA4-imported**
   `generate_lead` conversion, both counting — that is a second, separate double-count that this
   GTM change does **not** fix.
4. Fix: set only **one** of them to Primary (keep the native tag-49 action as Primary and set the
   GA4-imported one to Secondary, or vice versa — but only one Primary).

> This step matters because the GTM container cannot see what conversion actions exist inside the
> Google Ads account. It is the one check that must be done in the Ads UI, not GTM.

---

## Rollback

If anything looks wrong:

1. **Instant:** GTM → **Versions** → open the previous version → **Publish** (republishes the
   old container, tag 48 active again). Takes effect immediately.
2. **Or:** un-pause tag 48 (open it → ⋮ → **Unpause**) → Submit → Publish.

No website deploy or code change is involved in either direction.

---

## What NOT to do

- ❌ Do **not** delete tag 25 or tag 49.
- ❌ Do **not** add a Google Ads conversion script to the website. GTM stays the single source of
  truth. The site's `GOOGLE_ADS_ID` field is intentionally empty — **filling it in would create a
  second Ads conversion path and genuinely double-count Ads conversions.**
- ❌ Do **not** un-pause the three already-paused tags (IDs 17, 19, 40) — they are latent
  duplicates; if anything, delete them after confirming they are obsolete.
- ❌ Do **not** change the GA4 measurement ID or the Google Ads conversion ID.

---

## Optional cleanup (low priority, separate task)

Three tags are already paused and inert: **17** (`generate_lead`), **19** (`phone_click`), **40**
(`whatsapp_click`). They have no effect while paused, but each is a latent duplicate — if a future
editor un-pauses tag 17, GA4 would count leads **three** times. Once you have confirmed they are
obsolete, delete them so no one can re-introduce the problem. Also delete the stale
`gtm-nacravo-container.json` from the website repo, or re-export it, so it stops describing only 3
of the 18 tags.
