"""Content for the six dedicated AC landing pages.

Each page answers a distinct customer problem and search intent, so it can be the
direct final URL for its matching Google Ads ad group:

  /ac-servicing-dubai            -> AC servicing Dubai
  /ac-chemical-cleaning-dubai    -> AC chemical cleaning Dubai
  /ac-duct-cleaning-dubai        -> AC duct cleaning Dubai
  /ac-repair-dubai               -> AC repair Dubai
  /ac-installation-dubai         -> AC installation Dubai
  /ac-maintenance-contract-dubai -> AC maintenance contract Dubai

Rules honoured across every page here (same as the AC hub):
  * The premium AC team is described as currently focused on Downtown Dubai,
    Business Bay and DIFC. No page claims guaranteed Dubai-wide same-day cover.
  * Business hours are 7:00 AM-10:00 PM daily. No page advertises 24/7 service.
  * Nothing invents prices, ratings, testimonials, warranties, response-time
    guarantees, brand partnerships or "payment after work" promises.
  * Gas top-up is never positioned as the default fix for weak cooling; duct
    cleaning never claims to cure illness or allergies; chemical cleaning makes
    no medical guarantees; installation does not claim to supply every brand.

These pages render through the shared template (build_ac_pages.py) so the header,
footer, tracking, schema and lead form are identical to the rest of the site.
"""

AC_FOCUS = "Downtown Dubai, Business Bay and DIFC"

# Coverage cards reused across the AC pages — the team genuinely serves the same
# three districts, so the cards are shared while each page keeps its own intro.
CORE_AREAS = [
    ("Downtown Dubai",
     "Split and fan-coil units in Downtown towers, worked around building access rules and service-lift booking windows."),
    ("Business Bay",
     "High-rise apartments and small offices along the canal, scheduled to suit residents and working hours alike."),
    ("DIFC",
     "Offices and residences in and around the centre, serviced with low disruption around the business day."),
]

AREAS_NOTE = (
    "Additional Dubai areas may be available depending on schedule — message us "
    "with your building or community and we will tell you honestly whether we can reach you."
)

# Shared pricing spine — each page overrides the heading, intro and first point.
BASE_PRICING_POINTS = [
    "A fixed quote confirmed before the technician starts — the figure you approve is the figure you pay",
    "Priced per unit, so multi-unit apartments, villas and offices are quoted properly",
    "Any replacement part is shown to you before it is fitted, never added to the invoice afterwards",
    "Any urgency surcharge appears in the quote upfront, never on the bill later",
]


PAGES = {

    # ============================================================ SERVICING
    "ac-servicing-dubai": {
        "url": "/ac-servicing-dubai",
        "breadcrumb": "AC Servicing",
        "title": "AC Servicing Dubai | Restore Cooling & Airflow | Nacravo",
        "meta_description": (
            "AC not cooling properly? Same-day AC servicing (subject to availability) in Downtown Dubai, "
            "Business Bay and DIFC. Filters, coils, drainage and gas checked. Fixed quote first, photo report after."
        ),
        "og_title": "AC Servicing in Dubai — Restore Cooling & Airflow",
        "og_description": (
            "A complete AC service by trained Nacravo technicians — filters, coils, drain line, gas pressure "
            "and thermostat checked. Fixed price agreed before work, photo report after."
        ),
        "og_image": "svc-maintenance2-lg.jpg",
        "h1": "AC Not Cooling Properly?",
        "eyebrow": "AC Servicing in Dubai · Downtown · Business Bay · DIFC",
        "lead": (
            "Same-day AC servicing for apartments, villas and offices, subject to availability. Restore cooling, "
            "airflow and drainage with a complete service by trained Nacravo technicians. Filters are cleaned and "
            "reseated, coils and the drain line cleared, gas pressure and the thermostat checked — you approve a "
            "fixed price before we start and get a photo report when it is done."
        ),
        "trust": [
            ("shield", "Licensed and insured"),
            ("tag", "Fixed price before work"),
            ("camera", "Photo report every visit"),
            ("pin", "Downtown · Bay · DIFC"),
        ],
        "service_value": "AC Servicing",
        "service_schema_name": "AC Servicing Dubai",
        "area_served_schema": ["Downtown Dubai", "Business Bay", "DIFC"],
        "wa_text": "Hello Nacravo, I need AC servicing in Dubai — my AC is not cooling properly.",
        "subservices": {
            "split-service": "Split AC service",
            "window-service": "Window AC service",
            "ducted-service": "Ducted / central AC service",
            "multi-unit": "Multiple units",
        },
        "jump_links": [
            ("Symptoms", "symptoms"),
            ("What's included", "included"),
            ("Servicing vs chemical", "vs-chemical"),
            ("How often", "frequency"),
        ],
        "sections_heading": "Weak cooling usually starts with something you can see",
        "sections_intro": (
            "Most call-outs for poor cooling trace back to routine wear a service resolves. Here are the signs, "
            "what a full service actually covers, and where servicing stops and a deeper job begins."
        ),
        "sections": [
            {
                "anchor": "symptoms",
                "title": "Signs your AC needs a service",
                "body": (
                    "Cooling that has slowly weakened, air that no longer reaches the far side of the room, water "
                    "marks under the indoor unit, a musty edge to the air, a unit that runs constantly without "
                    "reaching temperature, or an electricity bill creeping up month on month. In Dubai's dust and "
                    "year-round running these are normal maintenance signals, not necessarily a fault."
                ),
                "bullets": ["Weak cooling and poor airflow", "Dirty filters restricting air",
                            "Blocked or dripping drainage", "Higher bills and noisy running"],
                "wa_text": "Hello Nacravo, my AC is not cooling well and I think it needs a service.",
            },
            {
                "anchor": "included",
                "title": "What an AC service includes",
                "body": (
                    "A full visit, not a quick spray. Filters are removed, cleaned and reseated; the indoor coil "
                    "is inspected and cleaned; the condensate drain is cleared so it cannot back up and leak; gas "
                    "pressure is measured; the thermostat is tested; and cooling performance is checked at the "
                    "vent before we leave. You receive photos of the work."
                ),
                "bullets": ["Filter clean and reseat", "Coil and drain-line clearing",
                            "Gas pressure and thermostat check", "Cooling performance test with photos"],
                "wa_text": "Hello Nacravo, please quote a full AC service for my unit.",
            },
            {
                "anchor": "vs-chemical",
                "title": "When servicing is enough — and when it isn't",
                "body": (
                    "A routine service restores most units to full cooling. If cooling stays weak straight after a "
                    "clean, if there is a persistent smell, or if the coils are visibly caked or mouldy, the unit "
                    "needs a deeper AC chemical cleaning where the coils are removed and treated. We will tell you "
                    "honestly which one your unit needs rather than upselling by default."
                ),
                "bullets": ["Servicing fixes routine wear", "Chemical cleaning for caked or mouldy coils",
                            "Honest assessment, no default upsell", "Gas top-up only if a leak is found"],
                "wa_text": "Hello Nacravo, is my AC a service or a chemical clean? I can send photos.",
            },
            {
                "anchor": "systems",
                "title": "Apartment, villa and office systems",
                "body": (
                    "We service wall-mounted split units, ducted split systems and chilled-water fan-coil units "
                    "found across Dubai apartments, villas and offices. On split systems we also clean the outdoor "
                    "condenser, which clogs quickly on balconies and rooftops here and is a frequent hidden cause "
                    "of weak cooling owners assume is a gas problem. Multi-unit properties are quoted per unit."
                ),
                "bullets": ["Wall-mounted and ducted splits", "Chilled-water fan-coil units",
                            "Outdoor condenser cleaned too", "Priced per unit for larger homes"],
                "wa_text": "Hello Nacravo, I have several AC units to service — please quote per unit.",
            },
            {
                "anchor": "frequency",
                "title": "How often to service AC in Dubai",
                "body": (
                    "In this climate we recommend a professional service every three to four months, and at minimum "
                    "twice a year. Dust load, humidity and near year-round running wear a unit far faster than in "
                    "milder climates. Holiday homes and heavily used offices benefit from quarterly visits, which "
                    "is usually cheaper than the breakdown a skipped service leads to."
                ),
                "bullets": ["Every 3-4 months in Dubai", "At least twice a year minimum",
                            "Quarterly for holiday homes and offices", "Filters best rinsed every 2-4 weeks"],
                "wa_text": "Hello Nacravo, I'd like to set up regular AC servicing.",
            },
        ],
        "band1_heading": "Cooling not what it used to be?",
        "band1_body": "Send your area and the symptom — weak cooling, a leak, a smell — and we will confirm what it needs and what it costs.",
        "why_heading": "Why book your AC service with Nacravo",
        "why_intro": "Four things that make a service visit predictable rather than a gamble.",
        "why": [
            ("team", "Employed, trained technicians", "Every technician is on the Nacravo payroll, background-checked, uniformed and trained to one checklist — not dispatched from a marketplace, so the standard does not change between visits."),
            ("tag", "Price agreed before work", "You approve a fixed price before a technician starts. No hourly creep and no invoice at the door that does not match the WhatsApp conversation."),
            ("camera", "Documented, not just described", "Each visit ends with a before-and-after photo report of the coils, drain and unit condition, so you can see exactly what was done even if you were not there."),
            ("shield", "Licensed, insured, equipped", "Nacravo is licensed and insured, and technicians arrive with their own tools, gauges, chemicals and protective sheeting. Nothing is needed from you except access to the units."),
        ],
        "process_heading": "How an AC service is booked",
        "process": [
            ("Tell us the units", "Send your area, property type and how many AC units, by WhatsApp, phone or the form. Photos help."),
            ("Get a fixed quote", "We confirm what the visit covers and a fixed price before anything is scheduled, priced per unit."),
            ("Pick a slot", "Choose a time between 7:00 AM and 10:00 PM, any day. Same-day is subject to availability."),
            ("Receive the photo report", "The technician completes the checklist and you get a before-and-after photo report of the work."),
        ],
        "pricing_heading": "How AC servicing is priced",
        "pricing_intro": (
            "Price depends on the system type and how many units you have. A single split unit is quoted "
            "differently from a villa with ducted systems, so you get a fixed figure before any work begins."
        ),
        "pricing_points": [
            "A fixed per-unit quote confirmed before the technician starts",
            "Priced on system type — wall split, ducted or fan-coil",
            "Any replacement part shown to you before it is fitted, never added afterwards",
            "Gas is only recharged if a genuine leak is found and addressed first — a top-up is never the default",
        ],
        "areas_heading": "Where our AC servicing team works",
        "areas_intro": (
            "Our premium AC servicing team currently focuses on " + AC_FOCUS + " so arrival windows stay tight and "
            "quality stays consistent. " + AREAS_NOTE
        ),
        "areas": CORE_AREAS,
        "faq_heading": "AC servicing questions, answered",
        "faq": [
            ("How often should AC be serviced in Dubai?",
             "Every 3 to 4 months, and at minimum twice a year. Dust, humidity and near year-round running wear units faster here than in milder climates, so quarterly servicing keeps cooling strong and bills lower."),
            ("How long does an AC service take?",
             "A standard split-unit service takes about 45 to 90 minutes per unit, depending on access and condition. Multi-unit properties take longer and are quoted per unit."),
            ("Will servicing fix my weak cooling?",
             "Usually, yes. Weak cooling is most often dirty filters and coils, a blocked drain or a clogged outdoor condenser, all of which a service restores. If cooling stays weak after a clean, the unit likely needs a chemical clean or a repair, and we will tell you which."),
            ("Do I need a service or a chemical clean?",
             "If cooling has gently weakened and the coils are only dusty, a service is enough. If cooling is poor straight after a clean, or there is a persistent smell or visible mould on the coils, a chemical clean is the right job. Send photos on WhatsApp and we will advise honestly."),
            ("Do you service apartments, villas and offices?",
             "Yes — wall-mounted splits, ducted splits and chilled-water fan-coil systems in apartments, villas and offices. Larger properties are quoted per unit so the price matches the work."),
            ("Do you offer same-day AC servicing?",
             "Subject to availability. Message us with your area and the issue and we will confirm the earliest slot. We work daily from 7:00 AM to 10:00 PM; we do not advertise a 24-hour service."),
            ("Which areas do you cover for AC servicing?",
             "Our AC team currently focuses on Downtown Dubai, Business Bay and DIFC to keep arrival times tight. Additional Dubai areas may be available depending on schedule — ask us about your building."),
            ("Is the price fixed before you start?",
             "Yes. You get a fixed quote before any work begins, priced per unit. Any part that needs replacing is shown to you first, so nothing is added to the invoice afterwards."),
        ],
        "related": [
            ("AC Chemical Cleaning", "/ac-chemical-cleaning-dubai",
             "When servicing alone will not restore cooling — coils removed and deep-treated."),
            ("AC Repair", "/ac-repair-dubai",
             "Leaking, tripping the breaker or not cooling at all? Fault diagnosed and priced before work."),
            ("AC Maintenance Contracts", "/ac-maintenance-contract-dubai",
             "Scheduled servicing across the year instead of calling when cooling fails in July."),
            ("AC Duct Cleaning", "/ac-duct-cleaning-dubai",
             "Dust blowing from the vents even after a coil clean? Clean the ducts and grilles."),
        ],
        "band2_heading": "Restore your cooling",
        "band2_body": "Send your details and we will come back with a fixed per-unit price and the earliest slot we have.",
    },

    # ==================================================== CHEMICAL CLEANING
    "ac-chemical-cleaning-dubai": {
        "url": "/ac-chemical-cleaning-dubai",
        "breadcrumb": "AC Chemical Cleaning",
        "title": "AC Chemical Cleaning Dubai | Deep Coil Wash | Nacravo",
        "meta_description": (
            "Bad smell or weak cooling after a regular service? Deep AC chemical cleaning in Downtown Dubai, "
            "Business Bay and DIFC removes built-up dirt, mould and bacteria from the coils. Fixed quote, photo report."
        ),
        "og_title": "AC Chemical Cleaning in Dubai — Deep Coil Restoration",
        "og_description": (
            "Coils removed and treated to dissolve caked dirt, mould and bacteria; blower and drain pan flushed. "
            "The job for weak cooling and smells that a normal service will not fix."
        ),
        "og_image": "svc-maintenance2-lg.jpg",
        "h1": "Bad Smell or Weak Cooling After a Regular Service?",
        "eyebrow": "AC Chemical Cleaning Dubai · Downtown · Business Bay · DIFC",
        "lead": (
            "Deep AC chemical cleaning that removes built-up dirt, mould and bacteria a routine service cannot "
            "reach. The coils are removed and treated with specialised chemicals, the blower and drain pan flushed, "
            "and drainage cleared at the source. This is the job for cooling that stays weak after a clean, a "
            "persistent musty smell, or visible mould on the coils. Fixed price first, photo report after."
        ),
        "trust": [
            ("shield", "Licensed and insured"),
            ("leaf", "Property protected during work"),
            ("camera", "Before-and-after photos"),
            ("tag", "Fixed price before work"),
        ],
        "service_value": "AC Chemical Cleaning",
        "service_schema_name": "AC Chemical Cleaning Dubai",
        "area_served_schema": ["Downtown Dubai", "Business Bay", "DIFC"],
        "wa_text": "Hello Nacravo, I need an AC chemical cleaning quote — my AC has a smell / weak cooling.",
        "subservices": {
            "smell": "Persistent bad smell",
            "mould": "Visible mould on coils",
            "weak-after-service": "Weak cooling after a service",
            "deep-restore": "Full deep restoration",
        },
        "jump_links": [
            ("When it's needed", "when"),
            ("What's included", "included"),
            ("Vs regular service", "vs-service"),
            ("Inside your home", "protection"),
        ],
        "sections_heading": "When a chemical clean is the right job",
        "sections_intro": (
            "Chemical cleaning is a deep restoration, not routine care. It is worth doing when a normal service "
            "has stopped delivering — and a waste of money when it has not. Here is how to tell."
        ),
        "sections": [
            {
                "anchor": "when",
                "title": "Signs your AC needs a chemical clean",
                "body": (
                    "A musty or sour smell every time the unit starts, cooling that stays weak right after a "
                    "standard service, visible mould or a thick mat of dirt on the coils, or a unit that has not "
                    "had a deep clean in over a year of heavy use. These point to contamination on the coil and in "
                    "the drain pan that surface cleaning cannot shift."
                ),
                "bullets": ["Persistent bad or musty smell", "Weak cooling after a normal service",
                            "Visible mould on the coils", "Heavy dirt build-up over 8-12 months"],
                "wa_text": "Hello Nacravo, my AC smells and cooling is weak — is it a chemical clean?",
            },
            {
                "anchor": "included",
                "title": "What an AC chemical clean includes",
                "body": (
                    "The indoor coil is removed where the unit allows and treated with specialised coil chemicals "
                    "to dissolve caked dirt, bacteria and mould, then thoroughly rinsed. The blower wheel is "
                    "cleaned, the drain pan and drain line are flushed, and cooling is retested afterwards. It is a "
                    "longer visit than a service because the unit is partially dismantled."
                ),
                "bullets": ["Coils removed and deep-treated", "Blower wheel cleaned",
                            "Drain pan and line flushed", "Cooling retested after"],
                "wa_text": "Hello Nacravo, please quote a full AC chemical clean.",
            },
            {
                "anchor": "vs-service",
                "title": "Chemical cleaning vs a regular service",
                "body": (
                    "A regular service is routine care — filters, a coil wipe-down, drain clearing, gas and airflow "
                    "checks — and is right every three to four months. A chemical clean is a deep restoration where "
                    "the coils are treated at a chemical level to remove what a service leaves behind. Most units "
                    "need servicing several times a year and a chemical clean far less often. If routine care is "
                    "all yours needs, book an AC service instead and keep the cost down."
                ),
                "bullets": ["Service = routine, several times a year", "Chemical clean = deep, occasional",
                            "Coils treated, not just wiped", "We recommend the cheaper option when it fits"],
                "wa_text": "Hello Nacravo, should I book a service or a chemical clean?",
            },
            {
                "anchor": "protection",
                "title": "Protecting your home during the work",
                "body": (
                    "Chemical cleaning is wet work carried out inside your property, so the area under the unit is "
                    "sheeted and protected before we start, furniture nearby is covered or moved clear, and the "
                    "space is left clean at the end. Technicians use appropriate protective equipment and handle "
                    "the cleaning chemicals to the product's safety instructions."
                ),
                "bullets": ["Work area sheeted and protected", "Nearby furniture covered",
                            "Chemicals handled to safety guidance", "Space left clean afterwards"],
                "wa_text": "Hello Nacravo, I'd like a chemical clean — how do you protect the room?",
            },
        ],
        "band1_heading": "Cooling still weak after a service?",
        "band1_body": "Send a photo of the indoor unit and your area — we will tell you whether a chemical clean is genuinely needed and what it costs.",
        "why_heading": "Why book your chemical clean with Nacravo",
        "why": [
            ("team", "Employed, trained technicians", "The same background-checked technicians carry out every chemical clean, so coil removal and refitting is a routine they do properly, not a first attempt on your unit."),
            ("tag", "Priced before the work", "You approve a fixed price before a technician starts. Chemical cleaning is quoted per unit, so a multi-unit home is priced fairly rather than from a flat rate."),
            ("camera", "Before-and-after proof", "The coils are photographed before and after, so the difference is documented. If a unit is only dusty rather than contaminated, we will show you and recommend the cheaper service instead."),
            ("leaf", "Honest scope", "No medical or air-purity guarantees, no scare tactics. A chemical clean restores cooling and removes the source of coil smells — we describe exactly that and nothing more."),
        ],
        "why_intro": "A deep clean done properly, scoped honestly.",
        "process_heading": "How a chemical clean is arranged",
        "process": [
            ("Send photos", "Share a photo of the indoor unit and describe the smell or cooling issue by WhatsApp, phone or form."),
            ("Get a fixed quote", "We confirm whether a chemical clean is the right job and quote a fixed per-unit price before scheduling."),
            ("Book the visit", "Slots run daily from 7:00 AM to 10:00 PM. The visit is longer than a service because the unit is partly dismantled."),
            ("See the result", "You receive before-and-after photos of the coils and drain, and cooling is retested before we leave."),
        ],
        "pricing_heading": "How AC chemical cleaning is priced",
        "pricing_intro": (
            "Chemical cleaning is quoted per unit and reflects the unit type and how contaminated the coils are. "
            "You get a fixed figure before any work begins."
        ),
        "pricing_points": BASE_PRICING_POINTS,
        "areas_heading": "Where our AC team works",
        "areas_intro": (
            "Our premium AC team currently focuses on " + AC_FOCUS + " for tight scheduling and consistent "
            "quality. " + AREAS_NOTE
        ),
        "areas": CORE_AREAS,
        "faq_heading": "AC chemical cleaning questions, answered",
        "faq": [
            ("What is AC chemical cleaning?",
             "A deep clean where the indoor coils are removed where possible and treated with specialised chemicals to dissolve caked dirt, bacteria and mould, then rinsed, with the blower and drain flushed. It restores cooling and removes coil smells that a standard service cannot."),
            ("When does an AC really need a chemical clean?",
             "When cooling stays weak straight after a normal service, when there is a persistent musty smell, when there is visible mould on the coils, or roughly once every 8 to 12 months on heavily used units. If the coils are only dusty, a standard service is enough."),
            ("What is the difference between a service and a chemical clean?",
             "A service is routine care done several times a year — filters, drain, gas and airflow. A chemical clean is a deeper, occasional job where the coils are treated at a chemical level. Most units need far more services than chemical cleans."),
            ("How long does an AC chemical clean take?",
             "Longer than a service — roughly 1.5 to 2.5 hours per unit — because the coil is partially removed, treated, rinsed and refitted, and the drain is flushed."),
            ("Will it get rid of the bad smell?",
             "Musty and sour AC smells come from mould and bacteria on damp coils and in the drain line. A chemical clean plus drain-line flushing removes that source rather than masking it. We do not, however, make medical or health guarantees."),
            ("Is it messy inside the apartment?",
             "It is wet work, so we sheet and protect the area under the unit, cover nearby furniture and leave the space clean. Technicians use protective equipment and handle chemicals to the product's safety instructions."),
            ("Which areas do you cover?",
             "Our AC team currently focuses on Downtown Dubai, Business Bay and DIFC. Additional Dubai areas may be available depending on schedule — ask us about your building."),
            ("Is the price fixed beforehand?",
             "Yes. Chemical cleaning is quoted per unit with a fixed price before work starts. If we find the coils are only dusty, we will recommend the cheaper standard service instead."),
        ],
        "related": [
            ("AC Servicing", "/ac-servicing-dubai",
             "Routine care several times a year — the cheaper job when the coils are only dusty."),
            ("AC Duct Cleaning", "/ac-duct-cleaning-dubai",
             "If dust also blows from the vents, the ducts and grilles may need cleaning too."),
            ("AC Repair", "/ac-repair-dubai",
             "If cooling has failed rather than faded, the unit needs diagnosis and repair."),
            ("AC Maintenance Contracts", "/ac-maintenance-contract-dubai",
             "Keep coils from reaching this state with scheduled preventive visits."),
        ],
        "band2_heading": "Get your AC breathing clean again",
        "band2_body": "Send a photo and your area — we will confirm whether it is a chemical clean and quote a fixed price.",
    },

    # ======================================================= DUCT CLEANING
    "ac-duct-cleaning-dubai": {
        "url": "/ac-duct-cleaning-dubai",
        "breadcrumb": "AC Duct Cleaning",
        "title": "AC Duct Cleaning Dubai | Cleaner Air & Airflow | Nacravo",
        "meta_description": (
            "Dust coming from your AC vents? Professional duct and grille cleaning in Downtown Dubai, Business Bay "
            "and DIFC for cleaner air and better airflow. Inspection first, fixed quote before work."
        ),
        "og_title": "AC Duct Cleaning in Dubai — Cleaner Air, Better Airflow",
        "og_description": (
            "Accessible ducts and grilles cleaned, airflow restored and dust removed at the source. We inspect "
            "before recommending work, and price it before we start."
        ),
        "og_image": "ba-ducts-1080.jpg",
        "h1": "Dust Coming From Your AC Vents?",
        "eyebrow": "AC Duct Cleaning Dubai · Downtown · Business Bay · DIFC",
        "lead": (
            "Professional duct cleaning for cleaner air and better airflow. When fine dust settles inside the "
            "ductwork, the system blows it straight back into the room every time it runs. We inspect the runs "
            "first, clean the accessible ducts and grilles, and check for damp or damaged insulation that would "
            "let the problem return. Inspection before recommendation, fixed price before work."
        ),
        "trust": [
            ("shield", "Licensed and insured"),
            ("check", "Inspection before we recommend"),
            ("camera", "Before-and-after photos"),
            ("tag", "Fixed price before work"),
        ],
        "service_value": "AC Duct Cleaning",
        "service_schema_name": "AC Duct Cleaning Dubai",
        "area_served_schema": ["Downtown Dubai", "Business Bay", "DIFC"],
        "wa_text": "Hello Nacravo, I need an AC duct cleaning assessment — dust is coming from my vents.",
        "subservices": {
            "vent-dust": "Dust around the vents",
            "airflow": "Weak or restricted airflow",
            "odour": "Stale odour from vents",
            "assessment": "Not sure — need an assessment",
        },
        "jump_links": [
            ("Symptoms", "symptoms"),
            ("What's included", "included"),
            ("What isn't", "not-included"),
            ("Suitability", "suitability"),
        ],
        "sections_heading": "What duct cleaning does — and honestly, what it doesn't",
        "sections_intro": (
            "Duct cleaning is worth doing when dust is genuinely coming from the vents. We inspect first so you "
            "only pay for work the ductwork actually needs, and we are clear about what it will and will not do."
        ),
        "sections": [
            {
                "anchor": "symptoms",
                "title": "Signs your ducts need attention",
                "body": (
                    "Grey dust marks fanning out around the supply grilles, a puff of dust when the system first "
                    "starts, visible debris settling on surfaces below the vents, weak airflow even after a coil "
                    "clean, or a stale smell that returns despite servicing. These point to dust and debris held "
                    "in the accessible ductwork and grilles rather than on the coil."
                ),
                "bullets": ["Dust marks around the vents", "Dust blowing into rooms",
                            "Stale odour from the vents", "Restricted airflow after a coil clean"],
                "wa_text": "Hello Nacravo, dust is coming from my AC vents — can you assess the ducts?",
            },
            {
                "anchor": "included",
                "title": "What duct cleaning includes",
                "body": (
                    "We start with an inspection of the accessible duct runs and grilles. Where cleaning is "
                    "warranted, grilles are removed and washed, accessible ductwork is cleaned of dust and debris, "
                    "and the insulation is checked for damp or damage that would reintroduce the problem. Airflow "
                    "is verified afterwards, and you get before-and-after photos of the accessible sections."
                ),
                "bullets": ["Inspection of accessible runs first", "Grilles removed and washed",
                            "Accessible ductwork cleaned", "Airflow verified, photos provided"],
                "wa_text": "Hello Nacravo, please quote duct and grille cleaning after an inspection.",
            },
            {
                "anchor": "not-included",
                "title": "What is and isn't included",
                "body": (
                    "We clean the accessible ductwork and grilles. Sealed, buried or structurally inaccessible duct "
                    "runs cannot be cleaned without opening up the ceiling, and we will say so plainly rather than "
                    "charge for work we cannot verify. Duct cleaning also does not fix coil contamination — if the "
                    "smell or weak cooling is coming from the coil, that is an AC chemical cleaning, and we will "
                    "point you there instead of over-selling ductwork."
                ),
                "bullets": ["Accessible ducts and grilles only", "No claims on sealed or buried runs",
                            "Coil contamination is a separate job", "Straight advice on what will actually help"],
                "wa_text": "Hello Nacravo, are my ducts accessible for cleaning? I can send photos.",
            },
            {
                "anchor": "suitability",
                "title": "Which properties suit duct cleaning",
                "body": (
                    "Ducted split and central systems in apartments, villas and offices with accessible grille runs "
                    "are the usual candidates. Simple wall-mounted split units have no ductwork to clean — their "
                    "equivalent is a coil and blower clean. If you are not sure what system you have, send a photo "
                    "of the indoor unit and vents and we will tell you whether duct cleaning even applies."
                ),
                "bullets": ["Ducted split and central systems", "Apartments, villas and offices",
                            "Wall splits have no ducts to clean", "Send a photo if you're unsure"],
                "wa_text": "Hello Nacravo, do I have ducts that need cleaning? Photo attached.",
            },
        ],
        "band1_heading": "Dust settling below your vents?",
        "band1_body": "Send a photo of the vents and your area — we will book an inspection and quote only the work the ducts actually need.",
        "why_heading": "Why book duct cleaning with Nacravo",
        "why": [
            ("check", "Inspection before recommendation", "We look before we quote. If the ducts are clean and the problem is the coil, we say so — you do not pay for duct work that will not help."),
            ("team", "Employed, trained technicians", "The same background-checked team carries out the inspection and the cleaning, so grilles come off and go back properly and nothing is left rattling."),
            ("camera", "Documented work", "Accessible sections are photographed before and after, so you can see the dust that was removed rather than take it on trust."),
            ("tag", "Fixed price before work", "You approve a fixed price after the inspection and before any cleaning starts, priced to the accessible runs we can genuinely clean."),
        ],
        "why_intro": "Honest scope, documented results.",
        "process_heading": "How duct cleaning is arranged",
        "process": [
            ("Send photos", "Share photos of the vents and describe the dust or airflow issue by WhatsApp, phone or form."),
            ("Inspection and quote", "We inspect the accessible runs, confirm whether cleaning will help, and quote a fixed price before starting."),
            ("Book the visit", "Slots run daily from 7:00 AM to 10:00 PM. Same-day is subject to availability."),
            ("Verify the result", "Grilles and accessible ducts are cleaned, airflow is checked, and you receive before-and-after photos."),
        ],
        "pricing_heading": "How duct cleaning is priced",
        "pricing_intro": (
            "Price depends on the number of grilles, the length of accessible ductwork and the system type. Because "
            "we inspect first, the quote reflects the work that will actually help — you get a fixed figure before "
            "any cleaning begins."
        ),
        "pricing_points": [
            "A fixed quote confirmed after the inspection and before work starts",
            "Priced on grille count, accessible duct length and system type",
            "Only accessible ductwork is quoted — no charge for runs we cannot reach or verify",
            "If the real issue is the coil, we will redirect you to a service or chemical clean instead",
        ],
        "areas_heading": "Where our AC team works",
        "areas_intro": (
            "Our premium AC team currently focuses on " + AC_FOCUS + " for tight scheduling and consistent "
            "quality. " + AREAS_NOTE
        ),
        "areas": CORE_AREAS,
        "faq_heading": "AC duct cleaning questions, answered",
        "faq": [
            ("Why is dust coming from my AC vents?",
             "Fine dust settles inside the ductwork and grilles and is pushed back into the room whenever the system runs. Cleaning the accessible ducts and grilles removes that dust at the source. Sometimes the culprit is the coil instead, which is why we inspect before recommending work."),
            ("What does duct cleaning include?",
             "An inspection of the accessible runs, removal and washing of the grilles, cleaning of the accessible ductwork, a check of the insulation for damp or damage, and an airflow verification afterwards, with before-and-after photos of the accessible sections."),
            ("Can you clean all of my ducts?",
             "We clean accessible ductwork and grilles. Sealed, buried or structurally inaccessible runs cannot be cleaned without opening the ceiling, and we will tell you that plainly rather than charge for work we cannot verify."),
            ("Does duct cleaning cure allergies or illness?",
             "No, and we will not claim it does. Duct cleaning removes visible dust and debris from accessible ductwork, which can improve airflow and reduce dust blown into the room. It is not a medical treatment and we make no health guarantees."),
            ("Do wall-mounted split units have ducts?",
             "No. A simple wall-mounted split unit has no ductwork — the equivalent job is a coil and blower clean. Duct cleaning applies to ducted split and central systems. Send a photo of your indoor unit if you are unsure."),
            ("How long does duct cleaning take?",
             "It depends on the number of grilles and the length of accessible ductwork. We confirm expected duration with the quote after the inspection."),
            ("Which areas do you cover?",
             "Our AC team currently focuses on Downtown Dubai, Business Bay and DIFC. Additional Dubai areas may be available depending on schedule — ask us about your building."),
            ("Is the price agreed before work?",
             "Yes. We inspect first, then quote a fixed price for the accessible work before any cleaning starts, so there are no surprises."),
        ],
        "related": [
            ("AC Chemical Cleaning", "/ac-chemical-cleaning-dubai",
             "If the smell or weak cooling is from the coil rather than the ducts, this is the job."),
            ("AC Servicing", "/ac-servicing-dubai",
             "Routine care for filters, coils and drainage — often booked on the same visit."),
            ("AC Maintenance Contracts", "/ac-maintenance-contract-dubai",
             "Keep airflow and air quality consistent with scheduled visits."),
            ("AC Repair", "/ac-repair-dubai",
             "If airflow has dropped because of a fault, the unit needs diagnosis."),
        ],
        "band2_heading": "Clear the dust at its source",
        "band2_body": "Send a photo of your vents and we will book an inspection and quote the accessible duct work honestly.",
    },

    # ============================================================== REPAIR
    "ac-repair-dubai": {
        "url": "/ac-repair-dubai",
        "breadcrumb": "AC Repair",
        "title": "AC Repair Dubai | Leaks, No Cooling, Noise Fixed | Nacravo",
        "meta_description": (
            "AC leaking, noisy or not cooling? Fast AC fault diagnosis and repair in Downtown Dubai, Business Bay "
            "and DIFC, with the price approved before work starts and parts shown before fitting."
        ),
        "og_title": "AC Repair in Dubai — Diagnosis & Repair, Priced First",
        "og_description": (
            "Water leaks, no cooling, tripping breakers, strange noises and error codes diagnosed to the cause. "
            "Parts shown before fitting, repair price approved before work. Daily 7am-10pm."
        ),
        "og_image": "svc-maintenance2-lg.jpg",
        "h1": "AC Leaking, Noisy or Not Cooling?",
        "eyebrow": "AC Repair Dubai · Downtown · Business Bay · DIFC",
        "lead": (
            "Fast AC fault diagnosis and repair, with the price approved before work starts. Water leaks, a unit "
            "that trips the breaker, ice on the pipework, strange noises, error codes or cooling that has stopped "
            "altogether — we trace the actual cause instead of guessing, show you any part before it is fitted, "
            "and confirm the repair price first. We work daily, 7:00 AM to 10:00 PM."
        ),
        "trust": [
            ("shield", "Licensed and insured"),
            ("check", "Parts shown before fitting"),
            ("tag", "Repair price approved first"),
            ("clock", "Daily 7am-10pm, fast slots"),
        ],
        "service_value": "AC Repair",
        "service_schema_name": "AC Repair Dubai",
        "area_served_schema": ["Downtown Dubai", "Business Bay", "DIFC"],
        "wa_text": "Hello Nacravo, my AC is leaking / not cooling and I need a repair in Dubai.",
        "subservices": {
            "not-cooling": "Not cooling at all",
            "leaking": "Water leaking",
            "not-starting": "Won't start / trips breaker",
            "noise": "Strange noise",
            "error-code": "Error code on display",
        },
        "jump_links": [
            ("Faults we fix", "faults"),
            ("Diagnosis process", "diagnosis"),
            ("Repair or replace", "repair-replace"),
            ("Availability", "availability"),
        ],
        "sections_heading": "The faults we are called out for most",
        "sections_intro": (
            "An AC fault is different from weak cooling — something has broken rather than drifted. We diagnose the "
            "cause first so the repair fixes the problem instead of the symptom."
        ),
        "sections": [
            {
                "anchor": "faults",
                "title": "AC faults we diagnose and repair",
                "body": (
                    "Cooling that has stopped, water leaking from the indoor unit, a unit that will not start or "
                    "trips the breaker, ice forming on the pipework, loud or grinding noises, error codes on the "
                    "display, or a thermostat that no longer holds temperature. Each has several possible causes, "
                    "so we test rather than assume."
                ),
                "bullets": ["Not cooling or won't start", "Water leakage from the indoor unit",
                            "Breaker tripping or frozen coils", "Strange noise, error codes, thermostat faults"],
                "wa_text": "Hello Nacravo, my AC has a fault — here is what it's doing:",
            },
            {
                "anchor": "diagnosis",
                "title": "How the diagnosis works",
                "body": (
                    "A technician tests the system to find the actual cause — checking pressures, electricals, the "
                    "drain, the coil and the controls rather than swapping parts on a hunch. You then get a clear "
                    "explanation of what is wrong and a fixed repair price. Any part that needs replacing is shown "
                    "to you before it is fitted, so you approve both the part and the price first."
                ),
                "bullets": ["Fault traced to the real cause", "Clear explanation of the problem",
                            "Fixed repair price before work", "Parts shown and approved before fitting"],
                "wa_text": "Hello Nacravo, please diagnose my AC fault and quote the repair.",
            },
            {
                "anchor": "repair-replace",
                "title": "Repair or replace — honest guidance",
                "body": (
                    "Not every fault is worth repairing. On an older unit with a failing compressor, a repair can "
                    "cost more than it is worth, and we will tell you when replacement is the better value rather "
                    "than quoting a repair we do not believe in. If replacement is the sensible route, we can quote "
                    "a correctly sized new installation instead."
                ),
                "bullets": ["Repair quoted when it makes sense", "Replacement advised when it doesn't",
                            "No repairs we don't believe in", "New installation quoted if better value"],
                "wa_text": "Hello Nacravo, is my AC worth repairing or should I replace it?",
            },
            {
                "anchor": "availability",
                "title": "Fast slots, honestly described",
                "body": (
                    "We know a failed AC in a Dubai summer cannot wait, so we prioritise repair call-outs and offer "
                    "same-day slots subject to availability. We work every day from 7:00 AM to 10:00 PM. We do not "
                    "advertise a 24-hour emergency service — message us with the fault and your area and we will "
                    "give you the earliest realistic slot rather than a promise we cannot keep."
                ),
                "bullets": ["Repairs prioritised", "Same-day subject to availability",
                            "Open daily 7:00 AM - 10:00 PM", "No false 24/7 claims"],
                "wa_text": "Hello Nacravo, what is the earliest slot for an AC repair in my area?",
            },
        ],
        "band1_heading": "AC stopped working?",
        "band1_body": "Message us the fault and your area — we will give you the earliest realistic slot and diagnose the cause before quoting.",
        "why_heading": "Why book your AC repair with Nacravo",
        "why": [
            ("check", "Diagnosis, not guesswork", "We test to find the cause before quoting, so the repair fixes the fault rather than replacing parts on a hunch and hoping."),
            ("tag", "Approved before we proceed", "You approve the repair price, and any part, before it is fitted. Nothing is added to the invoice that you did not agree to first."),
            ("team", "Employed, insured technicians", "Every technician is on the Nacravo payroll, background-checked and insured — one accountable company if anything needs revisiting, not a rotating cast."),
            ("camera", "Documented repair", "The fault and the completed repair are photographed, and cooling is retested before we leave, so you have a record of what was done."),
        ],
        "why_intro": "Faults fixed at the cause, priced before the work.",
        "process_heading": "How an AC repair works",
        "process": [
            ("Describe the fault", "Tell us what the AC is doing and your area, by WhatsApp, phone or form. A short video of the fault helps."),
            ("Diagnosis on site", "A technician tests the system, identifies the cause and explains it plainly."),
            ("Approve the price", "You get a fixed repair price, with any part shown to you before it is fitted, and approve before work starts."),
            ("Repair and retest", "The repair is completed, cooling is retested and you receive photos of the work."),
        ],
        "pricing_heading": "How AC repair is priced",
        "pricing_intro": (
            "Repair pricing depends on the fault and any parts required, which is why we diagnose first. You get a "
            "fixed repair price before work starts, and parts are shown to you before fitting."
        ),
        "pricing_points": [
            "A fixed repair price confirmed after diagnosis and before work starts",
            "Any part is shown to you and approved before it is fitted",
            "A diagnosis or call-out fee, where it applies, is stated upfront — never a surprise",
            "Any same-day or urgency surcharge appears in the quote, never added to the bill later",
        ],
        "areas_heading": "Where our AC repair team works",
        "areas_intro": (
            "Our AC repair team currently focuses on " + AC_FOCUS + " so we can reach a failed unit quickly. "
            + AREAS_NOTE
        ),
        "areas": CORE_AREAS,
        "faq_heading": "AC repair questions, answered",
        "faq": [
            ("Why is my AC leaking water?",
             "Most often a blocked or dirty drain line, a full drain pan, a frozen coil that has thawed, or poor installation slope. A technician clears the drain, inspects the pan and diagnoses the root cause during the visit rather than just mopping up."),
            ("Why has my AC stopped cooling?",
             "It can be a failing compressor, a refrigerant leak, an electrical fault, a frozen coil or a controls problem. These need diagnosis, not a guess — we test the system to find the actual cause before quoting a repair."),
            ("Why does my AC trip the breaker?",
             "A tripping breaker usually points to an electrical fault, a failing compressor or capacitor, or a wiring issue, and should not be repeatedly reset. We diagnose it safely and quote the repair before proceeding."),
            ("Do you offer same-day AC repair?",
             "Subject to availability. We prioritise repair call-outs and work daily from 7:00 AM to 10:00 PM. Message us the fault and your area and we will give you the earliest realistic slot. We do not advertise a 24-hour service."),
            ("Will I know the price before you start?",
             "Yes. We diagnose the fault, explain it, and give you a fixed repair price before any work begins. Any part that needs replacing is shown to you before it is fitted."),
            ("Should I repair or replace my AC?",
             "It depends on the unit's age and the fault. On an older unit with a major failure, a repair can cost more than it is worth, and we will tell you honestly when replacement is better value — and quote a correctly sized installation if you want one."),
            ("My AC is noisy — can you fix it?",
             "Usually. Noise often comes from a loose or unbalanced fan, worn bearings, debris in the blower or vibrating panels. We diagnose the source during the visit and quote any repair before proceeding."),
            ("Which areas do you cover for AC repair?",
             "Our repair team currently focuses on Downtown Dubai, Business Bay and DIFC so we can reach a failed unit quickly. Additional Dubai areas may be available depending on schedule — ask us about your building."),
        ],
        "related": [
            ("AC Servicing", "/ac-servicing-dubai",
             "If cooling has faded rather than failed, a service may be all it needs."),
            ("AC Installation", "/ac-installation-dubai",
             "When repair isn't worth it, a correctly sized replacement, installed and commissioned."),
            ("AC Maintenance Contracts", "/ac-maintenance-contract-dubai",
             "Catch faults early with scheduled preventive visits and priority booking."),
            ("AC Chemical Cleaning", "/ac-chemical-cleaning-dubai",
             "If a smell or contamination is behind the problem, a deep coil clean."),
        ],
        "band2_heading": "Get your AC working again",
        "band2_body": "Send the fault and your area and we will confirm the earliest slot and diagnose before we quote.",
    },

    # ======================================================== INSTALLATION
    "ac-installation-dubai": {
        "url": "/ac-installation-dubai",
        "breadcrumb": "AC Installation",
        "title": "AC Installation Dubai | Fitted, Tested, Commissioned | Nacravo",
        "meta_description": (
            "Need a new AC installed correctly? Professional AC installation, testing and commissioning in "
            "Downtown Dubai, Business Bay and DIFC. Correct sizing, proper drainage slope, pressure-tested pipework."
        ),
        "og_title": "AC Installation in Dubai — Installed, Tested, Commissioned",
        "og_description": (
            "Split and window AC installation, replacement and reinstallation. Correct sizing, drain set to a "
            "proper fall, pipework pressure-tested and the unit commissioned before handover."
        ),
        "og_image": "svc-maintenance2-lg.jpg",
        "h1": "Need a New AC Installed Correctly?",
        "eyebrow": "AC Installation Dubai · Downtown · Business Bay · DIFC",
        "lead": (
            "Professional AC installation, testing and commissioning for Dubai properties. We check the unit is "
            "correctly sized for the room, set the drain line to a proper fall so it cannot back up later, "
            "pressure-test the pipework and commission the system before handover. Poor installation slope is one "
            "of the most common causes of leaks we are later called out to fix — so we get it right first time."
        ),
        "trust": [
            ("shield", "Licensed and insured"),
            ("check", "Sized, tested, commissioned"),
            ("camera", "Installation documented"),
            ("tag", "Fixed price before work"),
        ],
        "service_value": "AC Installation",
        "service_schema_name": "AC Installation Dubai",
        "area_served_schema": ["Downtown Dubai", "Business Bay", "DIFC"],
        "wa_text": "Hello Nacravo, I'd like a quote for AC installation in Dubai.",
        "subservices": {
            "split-install": "New split AC installation",
            "window-install": "Window AC installation",
            "replacement": "Replacement of an old unit",
            "reinstall": "Reinstallation after a move",
        },
        "jump_links": [
            ("What we install", "types"),
            ("Done correctly", "correct"),
            ("The process", "process-detail"),
            ("For a quote", "quote-info"),
        ],
        "sections_heading": "Installed properly, so you're not calling us back to fix it",
        "sections_intro": (
            "Most AC leaks and weak-cooling call-outs on newer units trace back to a rushed installation. The work "
            "below is what a correct installation actually involves."
        ),
        "sections": [
            {
                "anchor": "types",
                "title": "What we install",
                "body": (
                    "Supply and fitting of new split AC units, window AC installation where the opening and building "
                    "rules support it, replacement of an old or failed unit, and reinstallation after a move or a "
                    "refurbishment. We fit units you have bought as well as supplying suitable units — tell us which "
                    "you need and we will quote accordingly."
                ),
                "bullets": ["New split AC installation", "Window AC where operationally supported",
                            "Replacement of an old unit", "Reinstallation after a move"],
                "wa_text": "Hello Nacravo, I need a new AC installed — here are the details:",
            },
            {
                "anchor": "correct",
                "title": "What 'installed correctly' means",
                "body": (
                    "The unit is sized to the room so it can actually hold temperature without running flat out. "
                    "The drain line is set to a proper fall so condensate runs away instead of backing up into the "
                    "room. Pipework is run cleanly, flared properly and pressure-tested for leaks. Mounting is "
                    "secure and level, and the electrical connection and safety checks are done before power-up."
                ),
                "bullets": ["Correct unit sizing for the room", "Drain line set to a proper fall",
                            "Pipework mounted and pressure-tested", "Electrical and safety checks"],
                "wa_text": "Hello Nacravo, I want the installation done properly — can you quote?",
            },
            {
                "anchor": "process-detail",
                "title": "Testing and commissioning",
                "body": (
                    "Installation is not finished when the unit is on the wall. We pressure-test the pipework, "
                    "check for refrigerant leaks, verify the drain runs freely, then commission the system — "
                    "confirming it reaches temperature, the airflow is right and the controls work — before we hand "
                    "it over. You get documentation of the commissioning checks."
                ),
                "bullets": ["Pipework pressure-tested", "Drainage confirmed to run free",
                            "System commissioned to temperature", "Commissioning documented at handover"],
                "wa_text": "Hello Nacravo, please include testing and commissioning in the install quote.",
            },
            {
                "anchor": "quote-info",
                "title": "What we need to quote an installation",
                "body": (
                    "To price an installation accurately, it helps to know the room size, whether you are replacing "
                    "an existing unit or fitting to a new location, the pipe run distance from indoor to outdoor "
                    "unit, and whether you are supplying the unit or want us to. A couple of photos of the space and "
                    "the outdoor location usually let us quote without a site visit."
                ),
                "bullets": ["Room size and unit location", "Replacement or brand-new position",
                            "Pipe run distance", "Whether you supply the unit or we do"],
                "wa_text": "Hello Nacravo, here are photos and room details for an AC installation quote.",
            },
        ],
        "band1_heading": "Planning a new AC?",
        "band1_body": "Send the room size and a couple of photos — we will quote a correctly sized installation, tested and commissioned.",
        "why_heading": "Why install with Nacravo",
        "why": [
            ("check", "Sized and tested, not rushed", "We size the unit to the room and pressure-test the pipework, so you are not calling someone back about leaks or weak cooling a month later."),
            ("tag", "Fixed price before work", "You approve a fixed installation price before we start. If you are supplying the unit, we quote the fitting; if we supply it, the unit is itemised separately."),
            ("team", "Employed, insured technicians", "Installations are carried out by our own background-checked, insured technicians, so there is one accountable company standing behind the work."),
            ("camera", "Commissioning documented", "The commissioning checks are recorded and handed over, so you have proof the system was tested, not just switched on."),
        ],
        "why_intro": "A correct installation is cheaper than the call-outs a bad one causes.",
        "process_heading": "How an AC installation works",
        "process": [
            ("Share the details", "Send room size, photos and whether you are replacing or fitting new, by WhatsApp, phone or form."),
            ("Get a fixed quote", "We confirm the right unit size and a fixed installation price, with the unit itemised if we supply it."),
            ("Book the fit", "Slots run daily from 7:00 AM to 10:00 PM. We agree a time that suits building access rules."),
            ("Commissioned handover", "The unit is fitted, pressure-tested, commissioned to temperature and handed over with the checks documented."),
        ],
        "pricing_heading": "How AC installation is priced",
        "pricing_intro": (
            "Installation price depends on the unit type, the pipe run, the mounting location and whether you "
            "supply the unit. You get a fixed figure before any work begins, with the unit itemised separately if "
            "we supply it."
        ),
        "pricing_points": [
            "A fixed installation quote confirmed before work starts",
            "Priced on unit type, pipe run length and mounting location",
            "The unit is itemised separately from the fitting where we supply it",
            "Any extra materials — brackets, extended pipe runs — are quoted upfront, not added later",
        ],
        "areas_heading": "Where our AC installation team works",
        "areas_intro": (
            "Our AC installation team currently focuses on " + AC_FOCUS + " for tight scheduling and consistent "
            "quality. " + AREAS_NOTE
        ),
        "areas": CORE_AREAS,
        "faq_heading": "AC installation questions, answered",
        "faq": [
            ("Do you supply the AC unit or just install it?",
             "Both. We can fit a unit you have already bought, or supply a suitable unit and itemise it separately in the quote. We do not claim to stock every brand — tell us what you are after and we will confirm what we can supply."),
            ("How do you make sure the AC is the right size?",
             "We size the unit to the room it has to cool, based on the area and use, so it can hold temperature without running flat out. An oversized or undersized unit wastes energy and cools unevenly, so sizing is part of the quote, not an afterthought."),
            ("Why does drainage slope matter?",
             "Condensate has to run away from the indoor unit under gravity. If the drain line is not set to a proper fall, water backs up and leaks into the room — one of the most common faults we are called out to fix on badly installed units. We set the fall correctly at installation."),
            ("Do you pressure-test the pipework?",
             "Yes. After the pipework is run and flared, we pressure-test it and check for refrigerant leaks before commissioning, so the system holds charge and cools properly from day one."),
            ("Can you install a window AC unit?",
             "Where the opening and the building's rules support it, yes. Some buildings and towers do not permit window units — send a photo of the opening and we will confirm whether it is feasible before quoting."),
            ("Do you reinstall an AC after a move?",
             "Yes. We reinstall existing units after a move or refurbishment, including re-running and pressure-testing the pipework, setting the drain fall and recommissioning the system."),
            ("Which areas do you cover for installation?",
             "Our installation team currently focuses on Downtown Dubai, Business Bay and DIFC. Additional Dubai areas may be available depending on schedule — ask us about your building."),
            ("Is the installation price fixed beforehand?",
             "Yes. You get a fixed installation quote before work starts. If we supply the unit it is itemised separately, and any extra materials are quoted upfront rather than added afterwards."),
        ],
        "related": [
            ("AC Repair", "/ac-repair-dubai",
             "If your current unit has failed, we can diagnose whether repair or replacement is better value."),
            ("AC Maintenance Contracts", "/ac-maintenance-contract-dubai",
             "Keep a new installation running well with scheduled preventive visits."),
            ("AC Servicing", "/ac-servicing-dubai",
             "First service for a new or newly reinstalled unit once it has bedded in."),
            ("AC Services", "/ac-service-dubai",
             "See the full range of AC services Nacravo provides across Dubai."),
        ],
        "band2_heading": "Install it right the first time",
        "band2_body": "Send the room details and photos and we will quote a correctly sized installation, tested and commissioned.",
    },

    # =============================================== MAINTENANCE CONTRACT
    "ac-maintenance-contract-dubai": {
        "url": "/ac-maintenance-contract-dubai",
        "breadcrumb": "AC Maintenance Contracts",
        "title": "AC Maintenance Contract Dubai | Preventive Cover | Nacravo",
        "meta_description": (
            "Stop waiting for your AC to break down. Scheduled preventive AC maintenance contracts in Downtown "
            "Dubai, Business Bay and DIFC for homes, landlords and businesses. Per-unit records, photo reports."
        ),
        "og_title": "AC Maintenance Contracts in Dubai — Preventive Cover",
        "og_description": (
            "Planned AC visits across the year with per-unit records, preventive inspection, photo reports and "
            "priority scheduling. For apartments, villas, landlords, holiday homes and businesses."
        ),
        "og_image": "svc-maintenance2-lg.jpg",
        "h1": "Stop Waiting for Your AC to Break Down",
        "eyebrow": "AC Maintenance Contracts Dubai · Downtown · Business Bay · DIFC",
        "lead": (
            "Scheduled preventive AC maintenance for homes, landlords and businesses. Instead of calling someone "
            "when the cooling fails in July, we agree a visit frequency to suit your units, keep a record of each "
            "one's condition, and flag parts that are wearing before they fail. Contract properties get priority "
            "scheduling where operationally supported, and a photo report after every visit."
        ),
        "trust": [
            ("clock", "Planned visits year-round"),
            ("camera", "Photo report every visit"),
            ("shield", "Licensed and insured"),
            ("tag", "Custom quote per units"),
        ],
        "service_value": "AC Maintenance Contract",
        "service_schema_name": "AC Maintenance Contract Dubai",
        "area_served_schema": ["Downtown Dubai", "Business Bay", "DIFC"],
        "wa_text": "Hello Nacravo, I'd like a quote for an AC maintenance contract in Dubai.",
        "contract_fields": True,   # renders the extra contract fields in the lead form
        "subservices": {
            "apartment": "Apartment owner",
            "villa": "Villa owner",
            "landlord": "Landlord / multiple properties",
            "holiday-home": "Holiday home",
            "office": "Office",
            "commercial": "Commercial property",
        },
        "jump_links": [
            ("Who it's for", "who"),
            ("What's included", "included"),
            ("How it's quoted", "pricing"),
            ("Vs annual maintenance", "amc"),
        ],
        "sections_heading": "A contract shaped around who you are",
        "sections_intro": (
            "A single apartment and a portfolio of let units need different cover, so a contract is built around "
            "your situation rather than sold as one flat package."
        ),
        "sections": [
            {
                "anchor": "who",
                "title": "Who AC maintenance contracts suit",
                "body": (
                    "Apartment owners who want cooling handled without thinking about it. Villa owners with several "
                    "units to keep on top of. Landlords who need let units maintained and documented between "
                    "tenancies. Holiday-home operators who cannot afford a mid-stay breakdown. Offices and "
                    "commercial properties where warm rooms mean lost work. Each gets a plan matched to the "
                    "number of units and how hard they run."
                ),
                "bullets": ["Apartment and villa owners", "Landlords with let units",
                            "Holiday homes and short-lets", "Offices and commercial properties"],
                "wa_text": "Hello Nacravo, I'd like an AC contract — here is my property type and unit count:",
            },
            {
                "anchor": "included",
                "title": "What a contract includes",
                "body": (
                    "Planned servicing visits scheduled across the year, a preventive inspection at each visit, a "
                    "per-unit service record so each system's history is tracked, and a photo report after every "
                    "visit. We flag parts showing wear before they fail and report faults so you can decide on "
                    "repairs early. Contract properties get priority scheduling where operationally supported."
                ),
                "bullets": ["Planned visits across the year", "Per-unit service records kept",
                            "Preventive inspection and wear reporting", "Photo report and priority scheduling"],
                "wa_text": "Hello Nacravo, what does an AC maintenance contract include for my units?",
            },
            {
                "anchor": "amc",
                "title": "How this fits with Annual Maintenance",
                "body": (
                    "If you want AC cover specifically, this contract is scoped to your air-conditioning units. If "
                    "you would rather one agreement that also covers plumbing, electrical and general repairs, our "
                    "broader annual maintenance contract folds AC servicing into whole-property cover. We will help "
                    "you pick whichever avoids paying twice for the same visits."
                ),
                "bullets": ["AC-focused cover here", "Whole-property cover via annual maintenance",
                            "No paying twice for the same visits", "We help you choose the right one"],
                "wa_text": "Hello Nacravo, should I take an AC contract or full annual maintenance?",
            },
            {
                "anchor": "records",
                "title": "Records and reporting you can rely on",
                "body": (
                    "For landlords and businesses the paperwork matters as much as the cooling. Each unit has its "
                    "own history, every visit is photographed, and faults and wear are written up so you have a "
                    "clear record for tenants, owners or your own budgeting. Nothing is described that is not "
                    "documented."
                ),
                "bullets": ["History tracked per unit", "Every visit photographed",
                            "Faults and wear written up", "Records suited to landlords and offices"],
                "wa_text": "Hello Nacravo, I need documented AC maintenance for let / commercial units.",
            },
        ],
        "band1_heading": "Tired of AC surprises?",
        "band1_body": "Tell us your property type and how many units, and we will build a preventive plan and a custom quote around them.",
        "why_heading": "Why put your AC on a Nacravo contract",
        "why": [
            ("clock", "Problems caught early", "Preventive visits catch a wearing part or a blocking drain before it becomes a failed unit in the hottest week of the year."),
            ("camera", "Documented every time", "A per-unit record and a photo report after each visit give landlords, owners and offices proof of the work, not just an invoice."),
            ("team", "The same accountable team", "Contract visits are carried out by our own employed technicians, so the people maintaining your units already know them, visit after visit."),
            ("tag", "Priced to your units", "A contract is quoted on the number of units and how hard they run, so you are not paying a flat rate that ignores the size of your property."),
        ],
        "why_intro": "Preventive cover that pays for itself in avoided breakdowns.",
        "process_heading": "How a contract is set up",
        "process": [
            ("Tell us the property", "Share whether it is residential or commercial, the number of properties and roughly how many AC units, by WhatsApp, phone or the form."),
            ("Get a custom quote", "We propose a visit frequency and a fixed contract price based on the units and usage — no flat-rate guesswork."),
            ("Schedule the year", "We agree the visit schedule around access and, for lets and holiday homes, around tenancies and bookings."),
            ("Ongoing reporting", "After each visit you get a per-unit update and a photo report, with any wear or fault flagged early."),
        ],
        "pricing_heading": "How an AC maintenance contract is priced",
        "pricing_intro": (
            "A contract is quoted on the number of units, the property type and how hard the systems run — not from "
            "a fixed menu. Send your details and we will build a custom quote, agreed before anything is signed."
        ),
        "pricing_points": [
            "A custom quote built on your unit count, property type and usage",
            "Visit frequency agreed with you, not imposed as a flat package",
            "Any repair or part found during a visit is quoted and approved separately before work",
            "Priority scheduling for contract properties where operationally supported",
        ],
        "areas_heading": "Where our AC contract team works",
        "areas_intro": (
            "Our AC team currently focuses on " + AC_FOCUS + " so scheduled visits stay reliable. " + AREAS_NOTE
        ),
        "areas": CORE_AREAS,
        "faq_heading": "AC maintenance contract questions, answered",
        "faq": [
            ("What is an AC maintenance contract?",
             "An agreement for scheduled preventive AC servicing across the year, with a per-unit service record, a preventive inspection at each visit, a photo report, and early flagging of wear and faults. It replaces waiting for a breakdown with planned visits."),
            ("Who is it for?",
             "Apartment and villa owners, landlords with let units, holiday-home operators, and offices and commercial properties. The plan is scoped to your property type and the number of units, so it suits a single flat as well as a portfolio."),
            ("How is the contract priced?",
             "On the number of units, the property type and how hard the systems run — not a flat rate. Send your details and we will build a custom quote, agreed before anything is signed. Any repair found during a visit is quoted separately and approved before work."),
            ("How often are the visits?",
             "We agree a frequency to suit your units and usage — commonly quarterly in Dubai's climate, more often for heavily used offices or holiday homes. The schedule is set with you, not imposed."),
            ("How is this different from annual maintenance?",
             "This contract is focused on your AC units. Our broader annual maintenance contract covers whole-property upkeep — plumbing, electrical and repairs — with AC servicing included. We will help you choose whichever avoids paying twice for the same visits."),
            ("Do I get records for my tenants or owners?",
             "Yes. Each unit has its own history, every visit is photographed, and faults and wear are written up, which suits landlords and offices that need documentation, not just a cooling system that works."),
            ("Do contract properties get priority?",
             "Contract properties get priority scheduling where operationally supported, so a contract unit is generally seen sooner than an ad-hoc call-out. We describe this as priority, not a guaranteed response time, because we do not make response-time promises we cannot keep."),
            ("Which areas do you cover?",
             "Our AC team currently focuses on Downtown Dubai, Business Bay and DIFC so scheduled visits stay reliable. Additional Dubai areas may be available depending on schedule — ask us about your properties."),
        ],
        "related": [
            ("Annual Maintenance", "/annual-maintenance",
             "Whole-property AMC cover — plumbing, electrical and repairs with AC servicing included."),
            ("AC Servicing", "/ac-servicing-dubai",
             "The routine service that makes up each scheduled contract visit."),
            ("AC Repair", "/ac-repair-dubai",
             "For faults found between or during visits — diagnosed and priced before work."),
            ("AC Services", "/ac-service-dubai",
             "The full range of AC services Nacravo provides across Dubai."),
        ],
        "band2_heading": "Get ahead of the next breakdown",
        "band2_body": "Send your property type and unit count and we will build a preventive plan and a custom quote around them.",
    },
}
