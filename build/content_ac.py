"""Content for the consolidated AC landing page at /ac-service-dubai.

The URL, canonical and existing high-value content are preserved. What changes:
  * a lead form is added above the fold
  * the ten required sub-service anchor sections are added
  * unverified testimonials are removed (replaced by a non-quote trust section)
  * service-area claims are corrected to Downtown Dubai / Business Bay / DIFC

Wording rule for this page only: AC servicing is described as currently focused
on Downtown Dubai, Business Bay and DIFC. It must NOT claim Dubai-wide cover.
"""

AC_FOCUS = "Downtown Dubai, Business Bay and DIFC"

PAGE = {
    "url": "/ac-service-dubai",
    "breadcrumb": "AC Services",
    "title": "AC Service Dubai | Servicing, Chemical Wash & Repair",
    "meta_description": "AC servicing, chemical wash, duct cleaning and repair in Downtown Dubai, Business Bay and DIFC. Fixed quote before work, photo report after. Get a quote.",
    "og_title": "AC Service in Dubai — Nacravo",
    "og_description": "Servicing, chemical wash, duct cleaning, repair and installation by licensed technicians. Fixed quotes, photo reports.",
    "og_image": "svc-maintenance2-lg.jpg",
    "h1": "AC Service in Dubai",
    "eyebrow": "AC servicing · Chemical wash · Repair · Downtown · Business Bay · DIFC",
    "lead": (
        "Servicing, chemical washing, duct cleaning, diagnostics, repair and installation for split, "
        "window and ducted systems. Our AC team currently focuses on " + AC_FOCUS + " so arrival times "
        "stay tight. You approve a fixed price before work starts and get a photo report when it is done."
    ),
    "trust": [
        ("shield", "Licensed and insured"),
        ("tag", "Fixed price upfront"),
        ("camera", "Photo report every visit"),
        ("pin", "Downtown · Bay · DIFC"),
    ],
    "service_value": "AC Services",
    "service_schema_name": "AC Service Dubai",
    "area_served_schema": ["Downtown Dubai", "Business Bay", "DIFC"],
    "wa_text": "Hello Nacravo, I'd like a quote for AC service in Dubai.",

    "sections_heading": "Complete AC service, done properly",
    "sections_intro": (
        "From routine servicing to deep chemical cleaning and repair, every visit follows the same "
        "checklist and ends with a photo report — so you can see exactly what was done."
    ),
    "sections": [
        {
            "anchor": "servicing",
            "title": "AC Servicing",
            "body": (
                "Scheduled maintenance that keeps cooling strong. Filters are cleaned and reseated, coils "
                "inspected, the condensate drain cleared, gas pressure checked and the thermostat tested. "
                "In Dubai's climate most systems need this every three to four months, and at minimum twice "
                "a year, because dust load and year-round running wear a unit far faster than in milder climates."
            ),
            "bullets": ["Filter clean and reseat", "Coil and drain inspection",
                        "Gas pressure and thermostat check", "Cooling performance test"],
            "wa_text": "Hello Nacravo, I'd like a quote for AC servicing in Dubai.",
        },
        {
            "anchor": "chemical-wash",
            "title": "AC Chemical Wash",
            "body": (
                "A deep restoration for a unit that servicing alone will not fix. Coils are removed and "
                "treated with specialised chemicals to dissolve caked dirt, bacteria and mould, then the "
                "blower and drain pan are flushed. This is the job for weak cooling that persists after a "
                "clean, a persistent musty smell, or visible mould on the coils."
            ),
            "bullets": ["Coils removed and deep-treated", "Mould and bacteria dissolved",
                        "Blower and drain pan flushed", "Smells removed at the source"],
            "wa_text": "Hello Nacravo, I'd like a quote for an AC chemical wash in Dubai.",
        },
        {
            "anchor": "duct-cleaning",
            "title": "AC Duct Cleaning",
            "body": (
                "Ductwork collects fine dust that then blows back into the room every time the system runs. "
                "We inspect the runs, clean accessible ducts and grilles, and check for damp or damaged "
                "insulation that would let the problem return. Useful if you see dust marks around vents or "
                "the air smells stale even after a coil clean."
            ),
            "bullets": ["Duct and grille cleaning", "Dust and debris removal",
                        "Insulation and damp check", "Airflow verified after"],
            "wa_text": "Hello Nacravo, I'd like a quote for AC duct cleaning in Dubai.",
        },
        {
            "anchor": "repair",
            "title": "AC Repair",
            "body": (
                "Water leaking from the indoor unit, a system that trips the breaker, ice on the pipework or "
                "cooling that has stopped altogether. We diagnose the actual cause rather than guessing, show "
                "you any part that needs replacing before it is fitted, and confirm the repair price before "
                "starting work."
            ),
            "bullets": ["Fault traced to the cause", "Parts shown before fitting",
                        "Fixed repair price agreed first", "Cooling retested before we leave"],
            "wa_text": "Hello Nacravo, my AC needs repair in Dubai.",
        },
        {
            "anchor": "installation",
            "title": "AC Installation",
            "body": (
                "Supply and fitting of split and window units, or reinstallation after a move. We check that "
                "the unit is correctly sized for the room, set the drain line to a proper fall so it cannot "
                "back up later, and pressure-test the pipework before commissioning. Poor installation slope "
                "is one of the most common causes of leaks we are later called out to fix."
            ),
            "bullets": ["Correct sizing for the room", "Drain line set to proper fall",
                        "Pipework pressure-tested", "Commissioned and handed over"],
            "wa_text": "Hello Nacravo, I'd like a quote for AC installation in Dubai.",
        },
        {
            "anchor": "diagnostics",
            "title": "AC Diagnostics & Inspection",
            "body": (
                "A standalone inspection when you need to know the condition of a system rather than service "
                "it. We measure temperature drop across the coil, check operating pressures, test the "
                "thermostat and inspect drainage, then write up the findings with photos. Useful before "
                "summer, before moving in, or when assessing a property."
            ),
            "bullets": ["Temperature-drop measurement", "Operating pressure check",
                        "Leak and drainage inspection", "Written report with photos"],
            "wa_text": "Hello Nacravo, I'd like an AC inspection in Dubai.",
        },
        {
            "anchor": "gas-top-up",
            "title": "AC Gas Top Up",
            "body": (
                "Refrigerant does not get consumed in normal running, so a unit that is low on gas has a leak "
                "somewhere. We trace and address the leak first, then recharge to the manufacturer's stated "
                "pressure and retest cooling. Topping up without finding the leak only buys a few weeks, so "
                "we will tell you if that is all a top-up would achieve."
            ),
            "bullets": ["Leak traced before recharging", "Charged to manufacturer pressure",
                        "Cooling retested after", "Honest advice if a repair is the better fix"],
            "wa_text": "Hello Nacravo, I think my AC needs a gas top up in Dubai.",
        },
        {
            "anchor": "split-ac",
            "title": "Split AC Service",
            "body": (
                "The most common system in Dubai apartments and villas. We service the indoor unit's filters, "
                "coil, blower wheel and drain, and check the outdoor condenser for dust blockage and fan "
                "condition. Condenser units on balconies and rooftops clog quickly here, and a blocked "
                "condenser is a frequent cause of weak cooling that owners assume is a gas problem."
            ),
            "bullets": ["Indoor coil, blower and drain", "Outdoor condenser cleaned",
                        "Fan and capacitor checked", "Both units tested together"],
            "wa_text": "Hello Nacravo, I'd like a quote for split AC service in Dubai.",
        },
        {
            "anchor": "window-ac",
            "title": "Window AC Service",
            "body": (
                "Window units are a single sealed box, so servicing means removing the casing to reach the "
                "coil, blower and drain tray properly. We clean the filter and coil, clear the drainage path, "
                "check the fan motor and reseal the unit in its opening so warm air and dust are not drawn "
                "back in around the frame."
            ),
            "bullets": ["Casing removed for a full clean", "Coil and blower cleaned",
                        "Drain tray cleared", "Unit resealed in the opening"],
            "wa_text": "Hello Nacravo, I'd like a quote for window AC service in Dubai.",
        },
        {
            "anchor": "preventive-maintenance",
            "title": "Preventive Maintenance Plans",
            "body": (
                "Scheduled visits through the year instead of calling someone when the cooling fails in July. "
                "We agree a visit frequency based on how many units you have and how hard they run, keep a "
                "record of each unit's condition, and flag parts that are wearing before they fail. Available "
                "for single apartments through to multi-unit villas and offices."
            ),
            "bullets": ["Visits scheduled through the year", "Per-unit service history kept",
                        "Wear flagged before failure", "Priority booking for contract properties"],
            "wa_text": "Hello Nacravo, I'd like a quote for an AC maintenance plan in Dubai.",
        },
    ],

    "band1_heading": "Cooling not what it should be?",
    "band1_body": "Tell us the symptom and your area — we will confirm what it needs and what it costs.",

    "pricing_heading": "Transparent AC pricing",
    "pricing_intro": (
        "Price depends on the system type, how many units you have and whether the job is routine servicing "
        "or a deep chemical wash. You get a fixed figure before any work begins."
    ),
    "pricing_points": [
        "A fixed quote confirmed before the technician starts",
        "Priced per unit, so multi-unit villas and offices are quoted properly",
        "Any part shown to you before it is fitted",
        "Any urgency surcharge shown upfront in the quote, never added later",
    ],

    "areas_heading": "Where our AC team works",
    "areas_intro": (
        "Our premium AC servicing team currently focuses on " + AC_FOCUS + " to deliver faster scheduling "
        "and consistent service quality."
    ),
    "areas": [
        ("Downtown Dubai",
         "Apartment split and fan-coil units in Downtown towers, serviced around building access rules and service-lift booking windows."),
        ("Business Bay",
         "High-rise apartments and small offices along the canal, with visits scheduled to suit residents and working hours alike."),
        ("DIFC",
         "Offices and residences in and around the centre, serviced with low disruption and scheduling that works around the business day."),
    ],

    "faq_heading": "AC service questions, answered",
    # Preserved from the existing page. Three answers were rewritten where they
    # listed communities outside the AC team's current coverage.
    "faq": [
        ("How often should AC be serviced in Dubai?",
         "In Dubai's climate we recommend a professional AC service every 3 to 4 months, and at minimum twice a year. Heavy year-round use, dusty locations and holiday homes benefit from quarterly maintenance to keep cooling strong and energy bills low."),
        ("How long does an AC service take?",
         "A standard maintenance visit for a split AC takes about 45 to 90 minutes per unit. A full chemical wash takes longer, roughly 1.5 to 2.5 hours per unit, because coils are removed, deep-cleaned and flushed."),
        ("What is included in an AC service?",
         "A standard service includes filter cleaning, coil inspection and cleaning, drain-line clearing, gas and pressure check, thermostat testing, airflow check and a general cooling performance inspection. You receive a photo report of the work."),
        ("When is an AC chemical wash needed?",
         "A chemical wash is needed when cooling is weak despite regular cleaning, when there is a persistent bad smell, mould or heavy dust build-up on the coils, or once every 8 to 12 months for heavily used units. It deep-cleans the coils that a standard clean cannot fully restore."),
        ("What is the difference between AC maintenance and a chemical wash?",
         "Maintenance is routine care: cleaning filters, clearing the drain, checking gas and airflow. A chemical wash is a deep restoration where the coils are treated with specialised cleaning chemicals to remove built-up dirt, bacteria and mould, restoring cooling and air quality."),
        ("How often should AC filters be cleaned?",
         "AC filters should be cleaned every 2 to 4 weeks in Dubai, especially during summer. Dirty filters restrict airflow, reduce cooling and raise electricity consumption. We clean them at every visit and can show you how between services."),
        ("Why is my AC leaking water?",
         "Water leakage is usually a blocked or dirty drain line, a full drain pan, a frozen coil that has thawed, or poor installation slope. Our technicians clear the drain line, inspect the pan and diagnose the root cause during the visit."),
        ("Why is my AC cooling weak?",
         "Weak cooling is commonly caused by dirty filters and coils, low refrigerant, a failing compressor, or restricted airflow. A cooling performance inspection identifies the cause, and often a clean or chemical wash restores full performance."),
        ("Which areas do you cover for AC service?",
         "Our AC servicing team currently focuses on Downtown Dubai, Business Bay and DIFC. Concentrating on these districts keeps arrival times tight and quality consistent. If you are just outside them, message us on WhatsApp and we will tell you honestly whether we can reach you."),
        ("Do you service apartments and villas?",
         "Yes. We service split, ducted and chilled-water fan-coil systems in both apartments and villas within our current coverage area, and multi-unit properties are quoted per unit so larger homes are priced properly."),
        ("Do you bring your own equipment?",
         "Yes. Our technicians arrive fully equipped with professional tools, cleaning chemicals, gauges and protective sheeting. Nothing is required from you except access to the units."),
        ("Do you provide AC inspections?",
         "Yes. We offer standalone cooling performance and leak inspections, useful before summer, before moving in, or when assessing a property, with a written photo report of findings."),
        ("What AC brands do you service?",
         "We service all major brands including Daikin, Mitsubishi, LG, Samsung, O General, Carrier, Trane, York, Hitachi, Panasonic, Gree and Midea, across split, ducted, central and window units."),
        ("Do you service central and ducted AC systems?",
         "Yes. We maintain central AC, ducted split and chilled-water fan-coil systems in apartments, villas and offices, including duct inspection, coil cleaning and thermostat calibration."),
        ("Can you fix bad smells coming from the AC?",
         "Yes. Musty or sour smells are caused by mould and bacteria on damp coils and in the drain line. A chemical wash plus drain-line cleaning removes the source and restores fresh air, rather than masking it."),
        ("Will servicing my AC lower my electricity bill?",
         "Usually, yes. A clean AC cools faster and runs less to hold temperature. Dirty coils and clogged filters force the system to work harder, so regular servicing typically reduces energy consumption and extends the unit's life."),
        ("Do you offer same-day AC service?",
         "Subject to availability. Message us on WhatsApp with your location and the issue and we will confirm the earliest slot. Any urgency surcharge is shown in your quote upfront."),
        ("Is your AC pricing transparent?",
         "Yes. You get a fixed quote before any work begins, with what is included clearly listed. Parts, if needed, are shown to you before we proceed, so there are no surprises on the invoice."),
        ("Are your AC technicians licensed and insured?",
         "Yes. Nacravo is licensed and insured, and every technician is on our payroll, background-checked and trained to one standard, not dispatched from a marketplace."),
        ("How do I book an AC service?",
         "The fastest way is WhatsApp: tap Book on WhatsApp, tell us your area, property type and the issue, and we will confirm a fixed quote and time. You can also call us or use the quote form on this page."),
        ("Do you clean AC coils and drain lines?",
         "Yes. Coil cleaning and drain-line cleaning are core parts of our service. Clean coils restore heat exchange and cooling, while a clear drain line prevents water leakage and bad smells."),
        ("My AC is noisy, can you help?",
         "Yes. Noise often comes from a loose fan, worn bearings, debris in the blower or vibration from loose panels. Our technicians diagnose the source during the visit and quote any repair before proceeding."),
        ("Do you offer AC maintenance contracts?",
         "Yes. Preventive maintenance plans schedule visits across the year rather than waiting for a breakdown, keep a service record per unit, and give contract properties priority booking. See our annual maintenance page for full contract cover."),
    ],

    "related": [
        ("Annual Maintenance", "/annual-maintenance",
         "Scheduled AMC cover for apartments and villas, with preventive visits and priority callout."),
        ("Handyman Services", "/handyman-services",
         "Plumbing, electrical and fixture work handled on the same visit by the same team."),
        ("Home Cleaning", "/home-cleaning",
         "Regular and one-off cleaning for apartments, townhouses and villas across Dubai."),
        ("Office & Commercial", "/office-commercial-cleaning",
         "Workplace cleaning contracts scheduled around your business hours."),
    ],

    "band2_heading": "Restore your AC performance",
    "band2_body": "Send your details and we will come back with a fixed price and the earliest slot we have.",
}

# Anchors offered in the jump nav under the hero.
PAGE["jump_links"] = [
    ("Servicing", "servicing"),
    ("Chemical wash", "chemical-wash"),
    ("Duct cleaning", "duct-cleaning"),
    ("Repair", "repair"),
    ("Installation", "installation"),
    ("Maintenance plans", "preventive-maintenance"),
]

# Sub-service preselection map for the hero form.
PAGE["subservices"] = {s["anchor"]: s["title"] for s in PAGE["sections"]}
