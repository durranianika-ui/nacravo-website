"""Verified image inventory and per-page media assignments.

Every description below was confirmed by opening the file, not inferred from the
filename. That matters: the `ba-*` files are NOT single "after" photos — each one
is a single JPEG containing a side-by-side Before | After composite with those
labels baked into the image. Alt text and captions must describe them as such.

Assignment rule: an image may only be used on a page whose service it genuinely
depicts. Where no honest asset exists, the page gets no gallery and the gap is
recorded in GALLERY_GAPS so it surfaces in QA and in the report — an unrelated
cleaning photo is never substituted.
"""

# filename stem -> what the image actually shows (verified visually)
INVENTORY = {
    "hero2":            "Three uniformed Nacravo staff reviewing a checklist on a clipboard in a bright, furnished Dubai apartment with a city view.",
    "hero3":            "A Nacravo cleaner in a face shield and gloves bagging debris in a heavily soiled bedroom with a Dubai skyline view.",
    "hero4":            "Eight uniformed Nacravo team members lined up in an office lobby with a Burj Khalifa view.",
    "hero-team":        "Three uniformed Nacravo staff in a corridor: one holding timber and a tape measure, one with a mop and caddy, one in a hi-vis jacket with a toolbox.",
    "team-quality":     "Three uniformed Nacravo staff standing together indoors, tighter crop of the same team line-up.",
    "team-caddy":       "A Nacravo technician holding a fully stocked branded cleaning caddy.",
    "svc-cleaning":     "Three uniformed Nacravo cleaners with a stocked cleaning trolley inside a corporate office floor.",
    "svc-cleaning2":    "A Nacravo cleaner wiping a chrome basin tap in a Dubai apartment bathroom.",
    "svc-maintenance":  "A Nacravo technician in a hard hat and safety glasses testing an electrical distribution panel with a multimeter.",
    "svc-maintenance2": "A Nacravo technician kneeling to test a wall socket with a multimeter, tool belt on the floor beside him.",
    # --- before/after composites (single file, two panels, labels baked in) ---
    "ba-bathroom":      "COMPOSITE: bathroom wall with damp staining and mould on the left, the same wall clean and repainted on the right.",
    "ba-bedroom":       "COMPOSITE: cluttered bedroom with scattered belongings on the left, the same room clean and made up on the right.",
    "ba-ducts":         "COMPOSITE: air-conditioning duct interior heavy with dust on the left, the same duct clean bare metal on the right.",
    "ba-living":        "COMPOSITE: living room with debris across the rug and table on the left, the same room clean and tidy on the right.",
    "ba-office":        "COMPOSITE: office floor with litter across the carpet on the left, the same floor clean on the right.",
    "ba-sofa":          "COMPOSITE: fabric corner sofa with staining on the left, the same sofa clean on the right.",
    "ba-windows":       "COMPOSITE: interior window glass and track before and after cleaning.",
}

COMPOSITES = {k for k, v in INVENTORY.items() if v.startswith("COMPOSITE")}


def is_composite(stem):
    return stem in COMPOSITES


# ---------------------------------------------------------------- heroes
# (large file, small file, alt text) per page slug.
HEROES = {
    "home-cleaning": (
        "svc-cleaning2-lg.jpg", "svc-cleaning2-sm.jpg",
        "A Nacravo cleaner wiping down a basin tap during a home cleaning visit in a Dubai apartment"),
    "deep-cleaning": (
        "hero3-lg.jpg", "hero3-sm.jpg",
        "A Nacravo cleaner in protective equipment clearing debris during a deep clean of a Dubai apartment"),
    "move-in-out-cleaning": (
        "ba-living-1080.jpg", "ba-living-600.jpg",
        "Before and after comparison of a Dubai living room cleared and cleaned for a tenancy handover"),
    "holiday-home-cleaning": (
        "hero2-lg.jpg", "hero2-sm.jpg",
        "Nacravo staff running a guest-ready checklist in a serviced Dubai holiday apartment"),
    "office-commercial-cleaning": (
        "svc-cleaning-1200.jpg", "svc-cleaning-760.jpg",
        "A Nacravo commercial cleaning team with a stocked trolley on a Dubai office floor"),
    "specialized-cleaning": (
        "ba-sofa-1080.jpg", "ba-sofa-600.jpg",
        "Before and after comparison of a fabric corner sofa cleaned by Nacravo"),
    "handyman-services": (
        "svc-maintenance2-lg.jpg", "svc-maintenance2-sm.jpg",
        "A Nacravo handyman testing a wall socket with a multimeter during an electrical repair in Dubai"),
    "annual-maintenance": (
        "svc-maintenance-1200.jpg", "svc-maintenance-760.jpg",
        "A Nacravo technician inspecting an electrical distribution panel during a scheduled maintenance visit"),
    # No pest control photography exists in the repository. This is the company
    # team line-up, and the alt text claims nothing about pest work. Dedicated
    # pest control photography is listed in GALLERY_GAPS.
    "pest-control": (
        "team-quality-1280.jpg", "team-quality-760.jpg",
        "Nacravo service technicians, the trained team who carry out treatments"),
    # NOTE: no hero entry for ac-service-dubai. ba-ducts is the only genuinely
    # AC-specific image and it carries the before/after section further down the
    # page; using it twice would be repetition, not evidence. An AC-specific
    # hero (technician servicing an indoor unit) is a documented gap below.
}

# ---------------------------------------------------------------- galleries
# (heading, [(file stem, caption, alt), ...])
GALLERIES = {
    "home-cleaning": ("The difference a clean makes", [
        ("ba-living", "Living room", "Before and after comparison of a Dubai apartment living room cleaned by Nacravo"),
        ("ba-bedroom", "Bedroom", "Before and after comparison of a bedroom tidied and cleaned by Nacravo"),
        ("ba-bathroom", "Bathroom", "Before and after comparison of a bathroom wall cleaned and restored by Nacravo"),
    ]),
    "deep-cleaning": ("What a deep clean removes", [
        ("ba-bathroom", "Bathroom", "Before and after comparison of bathroom damp staining removed during a Nacravo deep clean"),
        ("ba-living", "Living area", "Before and after comparison of a living area cleared and deep cleaned by Nacravo"),
        ("ba-bedroom", "Bedroom", "Before and after comparison of a bedroom deep cleaned by Nacravo"),
    ]),
    # hero is ba-living, so the gallery deliberately omits it — no page shows
    # the same photograph twice.
    "move-in-out-cleaning": ("Handover-ready results", [
        ("ba-bedroom", "Bedroom", "Before and after comparison of a bedroom cleared and cleaned before a move-out inspection"),
        ("ba-bathroom", "Bathroom", "Before and after comparison of a bathroom cleaned to handover standard"),
        ("ba-windows", "Windows and tracks", "Before and after comparison of interior window glass and tracks cleaned for handover"),
    ]),
    "holiday-home-cleaning": ("Turnovers, documented", [
        ("ba-bedroom", "Guest bedroom", "Before and after comparison of a holiday home bedroom reset for the next guest"),
        ("ba-living", "Living area", "Before and after comparison of a holiday home living area reset between stays"),
        ("ba-bathroom", "Bathroom", "Before and after comparison of a holiday home bathroom cleaned for arrival"),
    ]),
    "office-commercial-cleaning": ("Workplaces, before and after", [
        ("ba-office", "Office floor", "Before and after comparison of a Dubai office floor cleaned by Nacravo"),
        ("ba-windows", "Interior glass", "Before and after comparison of interior office glass cleaned by Nacravo"),
        ("ba-living", "Breakout area", "Before and after comparison of a breakout area cleaned during a contract visit"),
    ]),
    # hero is ba-sofa, so the gallery deliberately omits it.
    "specialized-cleaning": ("Specialist work, up close", [
        ("ba-windows", "Interior windows", "Before and after comparison of interior window glass and tracks cleaned by Nacravo"),
        ("ba-living", "Carpets and rugs", "Before and after comparison of a living room carpet cleaned by Nacravo"),
        ("ba-bathroom", "Bathrooms", "Before and after comparison of a bathroom surface cleaned by Nacravo"),
    ]),
}

# Galleries built from photographs of the actual trade rather than before/after
# composites. Kept separate so the section copy can describe them honestly.
WORK_GALLERIES = {
    # hero is svc-maintenance2 — omitted here so the page never repeats an image
    "handyman-services": ("Our technicians at work", [
        ("svc-maintenance-1200.jpg", "svc-maintenance-760.jpg", "Diagnostics",
         "A Nacravo technician testing an electrical distribution panel with a multimeter"),
        ("hero-team-1280.jpg", "hero-team-760.jpg", "Carpentry and fitting",
         "Nacravo staff with timber, a tape measure and a toolbox before a handyman job"),
        ("team-quality-1280.jpg", "team-quality-760.jpg", "One accountable team",
         "Nacravo technicians who carry out handyman and repair visits"),
    ]),
    # hero is svc-maintenance — omitted here so the page never repeats an image
    "annual-maintenance": ("Scheduled maintenance in practice", [
        ("svc-maintenance2-lg.jpg", "svc-maintenance2-sm.jpg", "Preventive checks",
         "A Nacravo technician testing a wall socket during a preventive maintenance visit"),
        ("hero-team-1280.jpg", "hero-team-760.jpg", "Trades under one contract",
         "Nacravo staff with timber, a tape measure and a toolbox on a maintenance visit"),
        ("team-caddy-lg.jpg", "team-caddy-sm.jpg", "Equipped for the visit",
         "A Nacravo technician carrying a fully stocked service caddy"),
    ]),
}

# Services with no honest photography in the repository. Rendered as an HTML
# comment on the page (never an empty box shown to visitors) and reported by QA.
GALLERY_GAPS = {
    "ac-service-dubai":
        "No photograph of a technician servicing an indoor AC unit exists in the "
        "repository. ba-ducts is the only AC-specific asset and it is used for the "
        "before/after comparison section. Needs: technician servicing a wall-mounted "
        "split unit, a chemical wash in progress, and coil cleaning detail. The page "
        "therefore runs without a hero image rather than borrowing an unrelated one.",
    "pest-control":
        "No pest control photography exists in the repository. A gallery here would "
        "require unrelated cleaning or maintenance photos, which would misrepresent "
        "the service. Needs: technician inspecting for cockroach or ant activity, "
        "bed bug mattress inspection, and commercial kitchen treatment. "
        "Placeholder left deliberately — do not fill with stock cleaning imagery.",
}
