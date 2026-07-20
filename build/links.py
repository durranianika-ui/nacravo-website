"""Contextual internal links and local-SEO area coverage.

Two things live here:

1. CONTEXTUAL — one natural in-body sentence per landing page that links to two
   or three genuinely-related siblings. Navigation, footer and the related-
   services grid already link everything to everything; these are the links that
   sit inside prose, where they carry real relevance signal and actually get
   clicked.

2. COMMUNITIES — the Dubai communities named on general-service pages.
   DELIBERATELY NOT APPLIED TO THE AC PAGE: AC servicing is scoped to Downtown
   Dubai, Business Bay and DIFC, and listing Marina or Arabian Ranches there
   would contradict the rest of that page. General cleaning and maintenance are
   available across Dubai, so naming communities within Dubai is consistent with
   what those pages already say.
"""

# Communities named on general-service pages only.
COMMUNITIES = [
    "Downtown Dubai", "Business Bay", "DIFC", "Dubai Marina", "JLT",
    "Palm Jumeirah", "JVC", "Dubai Hills", "Arabian Ranches", "Mirdif",
]

LOCAL_INTRO = ("We work across Dubai, subject to availability. Communities we are booked in "
               "most often include:")

LOCAL_NOTE = ("Not listed? Message us with your building or community and we will tell you "
              "honestly whether we can reach you.")

# slug -> in-body sentence with inline links.
CONTEXTUAL = {
    "home-cleaning":
        'Booking a regular clean is the easiest way to keep on top of a home. If the property '
        'has been left a while, or you are handing it back to a landlord, start with a '
        '<a href="/deep-cleaning">deep clean</a> or an '
        '<a href="/move-in-out-cleaning">end-of-tenancy clean</a> instead, and add '
        '<a href="/specialized-cleaning#sofa-cleaning">sofa and carpet cleaning</a> if the '
        'upholstery needs attention.',

    "deep-cleaning":
        'A deep clean is a reset, not a routine. Most customers follow it with '
        '<a href="/home-cleaning">regular home cleaning</a> to hold the standard, and book '
        '<a href="/specialized-cleaning">specialist upholstery or carpet work</a> at the same '
        'visit. If you are moving out, the '
        '<a href="/move-in-out-cleaning">move-out clean</a> is the version built around '
        'handover inspections.',

    "move-in-out-cleaning":
        'Handover cleaning is usually booked alongside other work on an empty property. We can '
        'run <a href="/deep-cleaning">deep cleaning</a> on the kitchen and bathrooms, '
        '<a href="/handyman-services">handyman repairs</a> for the snags a landlord will flag, '
        'and <a href="/pest-control">pest control</a> before new tenants move in.',

    "holiday-home-cleaning":
        'Short-let turnovers work best with the rest of the property covered too. Owners often '
        'add <a href="/deep-cleaning">periodic deep cleans</a> between busy seasons, '
        '<a href="/specialized-cleaning">upholstery and mattress cleaning</a> for guest-facing '
        'furniture, and an <a href="/annual-maintenance">annual maintenance contract</a> so '
        'faults are fixed before a guest reports them.',

    "office-commercial-cleaning":
        'Workplace contracts rarely stop at cleaning. We also handle '
        '<a href="/ac-service-dubai">AC servicing</a> for offices in Downtown, Business Bay and '
        'DIFC, <a href="/handyman-services">handyman and electrical work</a> out of hours, and '
        '<a href="/specialized-cleaning#carpet-cleaning">office carpet cleaning</a> as a '
        'scheduled extra.',

    "specialized-cleaning":
        'Specialist cleaning is often the finishing step. It pairs naturally with a '
        '<a href="/deep-cleaning">full deep clean</a>, with '
        '<a href="/move-in-out-cleaning">move-out cleaning</a> when a landlord is inspecting '
        'upholstery, and with <a href="/home-cleaning">regular home cleaning</a> once the heavy '
        'work is done.',

    "pest-control":
        'Treatment works better on a clean property. We frequently run pest control alongside a '
        '<a href="/deep-cleaning">deep clean</a> of kitchens and bathrooms, and before tenants '
        'arrive as part of a <a href="/move-in-out-cleaning">move-in clean</a>. For restaurants '
        'and shops, it sits with <a href="/office-commercial-cleaning">commercial cleaning</a> '
        'on the same schedule.',

    "handyman-services":
        'Most handyman calls come with something else that needs doing. We cover '
        '<a href="/ac-service-dubai">AC servicing and repair</a> in Downtown, Business Bay and '
        'DIFC, put recurring jobs on an '
        '<a href="/annual-maintenance">annual maintenance contract</a>, and handle the repairs '
        'that come up during a <a href="/move-in-out-cleaning">move-out inspection</a>.',

    "annual-maintenance":
        'A contract is the sensible option once you are calling someone every few months. It '
        'covers the same <a href="/handyman-services">handyman, plumbing and electrical work</a> '
        'we do on single jobs, includes <a href="/ac-service-dubai">AC servicing</a> where we '
        'operate, and suits owners already using our '
        '<a href="/holiday-home-cleaning">holiday home turnovers</a>.',

    "ac-service-dubai":
        'AC work often overlaps with the rest of a property. Recurring servicing is usually '
        'better handled on an <a href="/annual-maintenance">annual maintenance contract</a>, '
        'electrical and fixture jobs sit with '
        '<a href="/handyman-services">handyman services</a>, and offices in our coverage area '
        'combine it with <a href="/office-commercial-cleaning">commercial cleaning</a>.',
}
