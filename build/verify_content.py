"""Independent verification of the landing page content.

Written to distrust the drafting step: it re-checks the schema, scans for
fabricated claims (prices, ratings, guarantees, certifications) and enforces
metadata uniqueness ACROSS ALL pages, which per-batch checks cannot see.
"""

import re
import sys

sys.path.insert(0, "build")

import content_a
import content_b
import content_c

PAGES = {}
for mod in (content_a, content_b, content_c):
    PAGES.update(mod.PAGES)

REQUIRED = [
    "url", "breadcrumb", "title", "meta_description", "og_title", "og_description",
    "og_image", "h1", "eyebrow", "lead", "trust", "service_value", "service_schema_name",
    "area_served_schema", "wa_text", "subservices", "jump_links", "sections_heading",
    "sections_intro", "sections", "band1_heading", "band1_body", "why_heading", "why_intro",
    "why", "process_heading", "process", "pricing_heading", "pricing_intro", "pricing_points",
    "areas_heading", "areas_intro", "areas", "faq_heading", "faq", "related",
    "band2_heading", "band2_body",
]

VALID_ICONS = {"shield", "check", "camera", "team", "tag", "pin", "clock", "leaf"}

# Claims we cannot substantiate and must never ship.
FABRICATION = [
    (r"\bAED\s*\d", "a price in AED"),
    (r"\bd(?:hs|irhams?)\s*\d", "a price in dirhams"),
    (r"\b\d+\s*%", "a percentage claim"),
    (r"\b\d+\+?\s*(?:years?|yrs)\s+(?:of\s+)?experience", "a years-in-business claim"),
    (r"\b\d[\d,]*\+?\s*(?:happy\s+)?(?:customers|clients|homes|jobs|villas)\b", "a customer/job count"),
    (r"\b\d(?:\.\d)?\s*(?:out of|/)\s*5\b", "a star rating"),
    (r"\b\d+\s*(?:star|reviews?)\b", "a rating or review count"),
    (r"\b24/7\b", "a 24/7 availability claim"),
    (r"\bround[- ]the[- ]clock\b(?!\s+cover)", "a round-the-clock claim"),
    (r"\bmunicipality[- ]approved\b", "a municipality approval claim"),
    (r"\bcertified\b", "a certification claim"),
    (r"\bISO\b", "an ISO claim"),
    (r"\bguarantee[ds]?\b", "a guarantee"),
    (r"\bwarrant(?:y|ies|ied)\b", "a warranty claim"),
    (r"\bno\.?\s*1\b|\bnumber one\b|\bbest in dubai\b", "a superlative market claim"),
    (r"\baward[- ]winning\b", "an award claim"),
]

# A claim that is explicitly negated ("we do not offer a guaranteed response
# time") is honest copy, not a fabricated claim — don't flag those.
NEGATED = re.compile(
    r"(?:\bno\b|\bnot\b|\bnever\b|\bwithout\b|\bcannot\b|\bcan't\b|\bdon't\b|\bdo not\b)"
    r"[^.]{0,60}$"
)

FILLER = [
    "in today's fast-paced", "nestled", "elevate your", "look no further",
    "we understand that", "rest assured", "unparalleled", "cutting-edge",
    "world-class", "one-stop shop", "tailored to your needs",
]

errors = []
warnings = []


def walk_strings(obj, path=""):
    """Yield every human-readable string in the page tree."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")


def main():
    if len(PAGES) != 9:
        errors.append(f"expected 9 pages, got {len(PAGES)}")

    seen = {"title": {}, "meta_description": {}, "h1": {}, "lead": {}, "url": {}}

    for slug, p in sorted(PAGES.items()):
        for key in REQUIRED:
            if key not in p:
                errors.append(f"{slug}: missing key '{key}'")
        if any(k not in REQUIRED for k in p):
            extra = [k for k in p if k not in REQUIRED]
            errors.append(f"{slug}: unexpected keys {extra}")

        # --- cross-page uniqueness ---
        for key in seen:
            v = p.get(key, "")
            norm = re.sub(r"\s+", " ", v.strip().lower())
            if norm in seen[key]:
                errors.append(f"{slug}: {key} duplicates {seen[key][norm]}")
            seen[key][norm] = slug

        # --- metadata lengths ---
        t, d = p.get("title", ""), p.get("meta_description", "")
        if not (45 <= len(t) <= 65):
            warnings.append(f"{slug}: title is {len(t)} chars — {t!r}")
        if not (135 <= len(d) <= 162):
            warnings.append(f"{slug}: meta_description is {len(d)} chars")
        if "Dubai" not in t:
            errors.append(f"{slug}: title missing 'Dubai'")

        # --- structural integrity ---
        anchors = [s["anchor"] for s in p.get("sections", [])]
        if len(anchors) != len(set(anchors)):
            errors.append(f"{slug}: duplicate section anchors")
        for a in anchors:
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a):
                errors.append(f"{slug}: anchor '{a}' is not kebab-case")

        if set(p.get("subservices", {})) != set(anchors):
            errors.append(f"{slug}: subservices keys do not match section anchors")

        for _, a in p.get("jump_links", []):
            if a not in anchors:
                errors.append(f"{slug}: jump link -> '#{a}' has no matching section")

        for icon, _ in p.get("trust", []):
            if icon not in VALID_ICONS:
                errors.append(f"{slug}: invalid trust icon '{icon}'")
        for entry in p.get("why", []):
            if entry[0] not in VALID_ICONS:
                errors.append(f"{slug}: invalid why icon '{entry[0]}'")

        for count_key, expected in [("trust", 4), ("why", 4), ("process", 4),
                                    ("areas", 3), ("faq", 6), ("related", 4),
                                    ("pricing_points", 4)]:
            got = len(p.get(count_key, []))
            if got != expected:
                errors.append(f"{slug}: {count_key} has {got}, expected {expected}")

        for s in p.get("sections", []):
            if len(s.get("bullets", [])) != 4:
                warnings.append(f"{slug}/{s['anchor']}: {len(s.get('bullets', []))} bullets")

        # --- fabrication + filler scan over every string ---
        for path, text in walk_strings(p, slug):
            low = text.lower()
            for pattern, label in FABRICATION:
                m = re.search(pattern, low)
                if m and not NEGATED.search(low[:m.start()]):
                    errors.append(f"{slug}{path}: contains {label} -> ...{text[max(0,m.start()-40):m.end()+40]}...")
            for f in FILLER:
                if f in low:
                    warnings.append(f"{slug}{path}: filler phrase '{f}'")

        # pricing copy must contain no digits at all
        for pt in p.get("pricing_points", []) + [p.get("pricing_intro", "")]:
            if re.search(r"\d", pt):
                errors.append(f"{slug}: digit in pricing copy -> {pt!r}")

    # --- related links must resolve to a real page or a known existing route ---
    known = {"/" + s for s in PAGES} | {"/ac-service-dubai", "/services", "/"}
    for slug, p in PAGES.items():
        for title, url, desc in p.get("related", []):
            if url not in known:
                errors.append(f"{slug}: related link '{url}' does not resolve")
            if url == p["url"]:
                errors.append(f"{slug}: related links to itself")

    print(f"Checked {len(PAGES)} pages\n")
    if warnings:
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print("  ! " + w)
        print()
    if errors:
        print(f"{len(errors)} ERROR(s):")
        for e in errors:
            print("  x " + e)
        return 1
    print("PASS — schema complete, metadata unique across all pages, no fabricated claims found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
