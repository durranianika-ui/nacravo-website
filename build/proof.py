"""Verified-evidence registry for the paid landing pages.

Everything the CRO audit asks to show above the fold — a Google rating, a review
count, real customer quotes, a workmanship warranty, a diagnostic fee, a
response-time SLA — is evidence about the real world. None of it may be written
here from inference, from a competitor's page, or from what would convert best.
A value belongs in this file only once someone at Nacravo has confirmed it and
can point at the source.

Empty entries are not an oversight. The template renders a component only when
its entry is populated, so an unverified claim is structurally impossible to
publish: there is no placeholder to forget to replace.

TO POPULATE
  REVIEWS   needs the Google Business Profile rating and review count as shown
            publicly on the profile today, plus the profile URL, plus two or
            three short verbatim quotes with the reviewer's display name and
            date. Do not paraphrase, do not select only five-star reviews, and
            re-check the count before each publish — a stale count is a false
            claim. Review schema must NOT be added until the rating is visible
            on the page and Google's review-snippet eligibility rules are met.
  WARRANTY  needs the written workmanship/remedy policy: what is covered, for
            how long, what voids it, and who signs it off. "Satisfaction
            guaranteed" is not a policy.
  PRICING   needs prices operations will actually honour, with what is included
            and excluded, and a review date. The pages already explain the
            pricing BASIS honestly (see render_pricing in template.py); this is
            only for confirmed numbers. A "from AED X" anchor invented to lift
            conversion is out of the question.
  RESPONSE  needs measured first-response and same-day-fulfilment rates by
            service and daypart, from the WhatsApp inbox and dispatch records.
            Until then the pages say only what is verifiably true: the opening
            hours, and that same-day depends on availability.
"""

# Google Business Profile evidence.
#   {"rating": 4.8, "count": 137, "url": "https://...", "quotes": [
#       {"name": "...", "date": "2026-07-14", "text": "..."}]}
REVIEWS = {}

# Written service-recovery / workmanship policy.
#   {"heading": "...", "body": "...", "scope": "...", "duration": "..."}
WARRANTY = {}

# Confirmed prices, per service slug.
#   {"home-cleaning": {"from": 000, "unit": "hour", "includes": [...], "excludes": [...]}}
PRICING = {}

# Measured response performance.
#   {"first_response_median_minutes": 0, "same_day_rate": 0.0, "measured_from": "...", "measured_to": "..."}
RESPONSE = {}


def has(section):
    """True when a section carries verified content and may be rendered."""
    return bool(section)


def gaps():
    """What is still unverified, for the QA report and the handover."""
    out = []
    if not REVIEWS:
        out.append("REVIEWS: no verified Google rating, review count or quotes — "
                   "the rating strip and review section are not rendered.")
    if not WARRANTY:
        out.append("WARRANTY: no documented workmanship or service-recovery policy — "
                   "no guarantee is claimed anywhere.")
    if not PRICING:
        out.append("PRICING: no operations-confirmed prices — pages explain the pricing "
                   "basis only, with no numbers.")
    if not RESPONSE:
        out.append("RESPONSE: no measured response times — pages state opening hours and "
                   "'same-day subject to availability' only, with no SLA.")
    return out


if __name__ == "__main__":
    g = gaps()
    print("Verified-evidence gaps ({}):".format(len(g)))
    for line in g:
        print("  - " + line)
    if not g:
        print("  none — every proof component has verified content.")
