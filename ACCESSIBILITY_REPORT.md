# Accessibility Report

**Prepared:** 20 July 2026
**Standard:** WCAG 2.1 Level AA
**Method:** contrast ratios computed with the official relative-luminance formula by
`build/audit_final.py`, from the live hex values in the stylesheets. **Measured, not assumed.**

---

## 1. Current status

| | |
|---|---|
| Combinations measured | 26 |
| Passing WCAG AA | 24 |
| **Failing WCAG AA** | **2** |
| Failures fixed in this project | 7 |

**The site cannot yet be described as WCAG 2.1 AA compliant.** Two button text combinations
fail, and both require a branding decision that has not been made. No colour has been changed
without approval.

---

## 2. Full contrast measurements

AA thresholds: **4.5:1** for normal text, **3:1** for large text (≥24px, or ≥19px bold) and for
non-text UI components (WCAG 1.4.11).

### Passing — text

| Element | Foreground | Background | Ratio | Level |
|---|---|---|---|---|
| Body text | `#3B4636` | `#F5F2EC` | 8.89:1 | AAA |
| Body text on cards | `#3B4636` | `#FFFFFF` | 9.93:1 | AAA |
| Section / lead copy | `#54594C` | `#F5F2EC` | 6.46:1 | AA |
| Card body copy | `#54594C` | `#FFFFFF` | 7.22:1 | AAA |
| List items | `#44483D` | `#FFFFFF` | 9.37:1 | AAA |
| Eyebrow / kicker | `#5E6C4F` | `#F5F2EC` | 5.03:1 | AA |
| Dropdown column heading | `#5E6C4F` | `#FFFFFF` | 5.62:1 | AA |
| Contextual links | `#5E6C4F` | `#FFFFFF` | 5.62:1 | AA |
| Fine print / captions | `#6F6B63` | `#F5F2EC` | 4.75:1 | AA |
| Form fine print | `#6F6B63` | `#FFFFFF` | 5.30:1 | AA |
| Navigation links | `#5A5F52` | `#F5F2EC` | 5.89:1 | AA |
| Form error text | `#B04A3E` | `#FDF4F2` | 4.98:1 | AA |
| Trust pill text | `#54594C` | `#ECE6D8` | 5.80:1 | AA |
| Area chip text | `#44483D` | `#FFFFFF` | 9.37:1 | AAA |
| Ghost button label | `#3B4636` | `#F5F2EC` | 8.89:1 | AAA |
| Headings (large) | `#3B4636` | `#F5F2EC` | 8.89:1 | AAA |

### Passing — dark surfaces

| Element | Foreground | Background | Ratio | Level |
|---|---|---|---|---|
| Footer links | `#BBC4B0` | `#2E372B` | 6.85:1 | AA |
| Footer legal links | `#9AA391` | `#2E372B` | 4.73:1 | AA |
| Footer strapline | `#9AA391` | `#2E372B` | 4.73:1 | AA |
| Footer column headings | `#F5F2EC` | `#2E372B` | 11.07:1 | AAA |
| Pillar body copy | `#BBC4B0` | `#2E372B` | 6.85:1 | AA |
| Pillar body on moss | `#BBC4B0` | `#3B4636` | 5.50:1 | AA |
| CTA band body | `#C9D2BF` | `#3B4636` | 6.36:1 | AA |
| Gallery caption overlay | `#F5F2EC` | `#2E372B` | 11.07:1 | AAA |

### Passing — non-text UI (3:1 threshold)

| Element | Foreground | Background | Ratio | Level |
|---|---|---|---|---|
| Sage icons, checkmarks, borders, focus ring | `#7E8F70` | `#F5F2EC` | 3.11:1 | AA (1.4.11) |

### ❌ Failing

| Element | Foreground | Background | Ratio | Required | Shortfall |
|---|---|---|---|---|---|
| **Primary button label** | `#F5F2EC` | `#7E8F70` | **3.11:1** | 4.5:1 | 1.39 |
| **WhatsApp button label** | `#FFFFFF` | `#25D366` | **1.98:1** | 4.5:1 | 2.52 |

**Where these appear:** the primary button is the main CTA sitewide — "Get a quote", "Get my free
quote", nav CTA, mid-page and closing CTA bands, cookie-consent "Accept all". The WhatsApp button
is the secondary CTA on every page plus the sticky mobile bar and the desktop floating button.

These are the **most-clicked elements on the site**, which is what makes the failure material
rather than cosmetic.

---

## 3. Why this cannot be fixed without a decision

Sage `#7E8F70` is a **mid-tone**. It fails against light labels *and* against dark ones:

| Label on `#7E8F70` | Ratio | Result |
|---|---|---|
| `#F5F2EC` pearl (current) | 3.11:1 | Fail |
| `#3B4636` moss | 2.86:1 | Fail (worse) |
| `#2E372B` moss-deep | 3.56:1 | Fail |
| `#1F2419` near-black | 4.57:1 | Pass, but looks like a rendering error on a green button |
| `#000000` black | 6.05:1 | Pass, visually harsh |

There is no label colour that both passes and looks like the Nacravo brand. **The button colour
itself has to change**, which is a branding decision, not an engineering one.

---

## 4. Two options

### OPTION A — Maintain branding, document the limitation

**Change nothing.** Keep `--sage #7E8F70` and WhatsApp `#25D366` exactly as they are.

| Aspect | Detail |
|---|---|
| Brand impact | **Zero.** Palette untouched. |
| Visual impact | **Zero.** |
| Accessibility | Site remains **WCAG 2.1 AA non-compliant** on button text. |
| Legal / procurement | Cannot claim AA conformance. Relevant if Nacravo bids for government, banking or DIFC corporate contracts, which commonly require an accessibility statement. |
| Real-world effect | Users with low vision, colour vision deficiency, or on a phone screen in Dubai daylight will find the main CTA label harder to read. This is the primary conversion element. |
| Required action | Update `/accessibility` to state the known limitation honestly rather than implying full AA conformance. |

**Note:** the WhatsApp button case is genuinely common practice — `#25D366` with white text is
WhatsApp's own official pairing and appears at 1.98:1 on a very large number of sites worldwide.
Deviating from it slightly reduces instant brand recognition of the button.

### OPTION B — Achieve WCAG AA

Two focused colour changes. **Nothing else in the palette moves** — sage stays the brand colour
for pillars, icons, borders, accents and the focus ring.

#### B1 — Primary button

| | Current | Proposed |
|---|---|---|
| Background | `#7E8F70` | **`#5F6E53`** |
| Label | `#F5F2EC` | `#F5F2EC` (unchanged) |
| Ratio | 3.11:1 ❌ | **4.89:1** ✅ |
| Hover | `#6E7E61` (3.90:1 ❌) | **`#525E43`** (6.18:1 ✅) |

Alternatives if `#5F6E53` reads too dark:

| Hex | Ratio | Note |
|---|---|---|
| `#647454` | 4.51:1 | Minimum viable — only 0.01 above threshold, no margin for rounding |
| **`#5F6E53`** | **4.89:1** | **Recommended** — comfortable margin, closest to current sage |
| `#5A6A4E` | 5.21:1 | Extra margin, visibly deeper |

- **Visual impact:** moderate. The button becomes a deeper, more saturated forest green. Still
  unmistakably the same colour family.
- **Brand impact:** low-to-moderate. `--sage` itself is unchanged, so every other sage element
  on the site is untouched; only the filled button surface darkens. Printed collateral and the
  logo are unaffected.

#### B2 — WhatsApp button

| Option | Background | Label | Ratio | Trade-off |
|---|---|---|---|---|
| **B2-i (recommended)** | **`#0B7A3B`** | `#FFFFFF` | **5.44:1** ✅ | Reads as a deeper green; loses some instant WhatsApp recognition |
| B2-ii | `#075E54` | `#FFFFFF` | 7.67:1 ✅ | WhatsApp's *own* dark brand green — defensible as on-brand for WhatsApp |
| B2-iii | `#25D366` (unchanged) | `#062611` | 8.19:1 ✅ | **Keeps the exact WhatsApp green**; near-black label is unusual but the button stays instantly recognisable |
| B2-iv | `#25D366` (unchanged) | `#0A3D1C` | 6.24:1 ✅ | Same idea, dark green label, slightly softer |

**B2-iii deserves consideration.** It is the only option that keeps WhatsApp's official green
pixel-for-pixel while passing AA, because it changes only the label. The icon can stay white if
it is treated as a decorative graphic — though for consistency the icon should darken with the
text.

Rejected: `#128C7E` (4.14:1) and `#0E8C44` (4.33:1) both look like they should work but **fail**.

---

## 5. Recommendation

**Option B, with B1 = `#5F6E53` and B2 = B2-iii (keep the green, darken the label).**

This reaches AA on both buttons while changing the brand's own green not at all and the WhatsApp
green not at all — only the primary button surface darkens by one step. It is the smallest change
that removes the compliance blocker.

**If brand consistency outranks compliance, Option A is legitimate** — provided `/accessibility`
is updated to disclose the limitation rather than implying conformance. Silently claiming AA
while two primary CTAs fail is the one outcome that should be avoided.

**No change has been made. This requires explicit approval.**

---

## 6. Non-contrast accessibility — verified

| Area | Status | Evidence |
|---|---|---|
| Heading hierarchy | ✅ Pass | No skipped levels on any page; enforced by `build/qa.py` |
| Landmarks | ✅ Pass | `<main id="main">`, `<header>`, `<footer>`, `<nav aria-label>` on every page |
| Skip link | ✅ Pass | "Skip to main content" first focusable element |
| Keyboard navigation | ✅ Pass | All controls reachable; Escape closes the services dropdown |
| Focus visibility | ✅ Pass | 3px `:focus-visible` outline added sitewide (base site used the UA default) |
| Focus order | ✅ Pass | Follows DOM order; no positive `tabindex` anywhere |
| Form labels | ✅ Pass | Every control has `<label for>`; enforced by QA |
| Form validation | ✅ Pass | Invalid fields flagged, first invalid focused, `role="status"` + `aria-live="polite"` on the result |
| Button names | ✅ Pass | Every `<button>` has text or `aria-label`; enforced by QA |
| ARIA | ✅ Pass | `aria-expanded` on nav toggles, `aria-label` on icon-only controls, `aria-hidden` on decorative SVG |
| Image alt | ✅ Pass | 100% coverage; composites explicitly described as before/after comparisons |
| Decorative images | ✅ Pass | Inline SVG icons marked `aria-hidden="true"` |
| Touch targets | ✅ Pass | None under 44px measured at 375px |
| Reduced motion | ✅ Pass | `prefers-reduced-motion` respected; reveal animation disabled |
| Zoom / reflow | ✅ Pass | No horizontal scroll at 375px, 768px or 1280px |
| Language | ✅ Pass | `<html lang="en">` on every page |

---

## 7. Remaining issues, ranked

| Priority | Issue | Action |
|---|---|---|
| **Critical** | Primary button label 3.11:1 | Decide Option A or B |
| **Critical** | WhatsApp button label 1.98:1 | Decide Option A or B |
| Medium | `/accessibility` page wording | If Option A is chosen, disclose the limitation there |
| Low | No screen-reader testing performed | Manual NVDA/VoiceOver pass recommended before claiming conformance |
| Low | No automated axe/Lighthouse a11y run | Run post-deploy alongside performance testing |

**Scope note:** this audit covers contrast computation and structural/semantic review. It does
**not** include manual assistive-technology testing. A NVDA or VoiceOver pass is recommended
before any formal accessibility statement is published.
