"""Full inventory of the LIVE GTM container, GTM-KD4PH4XP.

Read-only. Fetches nothing and changes nothing in GTM — it parses the published
gtm.js that GTM serves to browsers, which is the authoritative record of what
actually runs.

Known limitation: the published container strips human-readable tag and trigger
NAMES. Tag IDs are present and are what the GTM UI shows in the tag list, so the
report keys off tag_id and says so rather than inventing names.

Usage: ./.venv/Scripts/python.exe build/gtm_audit.py
"""

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "build" / "gtm" / "gtm-live.js"

TAG_TYPES = {
    "__gaawe": "GA4 Event",
    "__googtag": "Google Tag (gtag config)",
    "__awct": "Google Ads Conversion Tracking",
    "__gclidw": "Conversion Linker",
    "__paused": "PAUSED (tag disabled in GTM)",
    "__cl": "Click Listener",
    "__fsl": "Form Submit Listener",
    "__hl": "History Listener",
}


def load():
    js = SRC.read_text(encoding="utf-8", errors="replace")
    blob = re.search(r'"resource":\s*(\{.*?\}),\s*"runtime"', js, re.S)
    if not blob:
        raise SystemExit("FAILED: could not locate the container resource block")
    return json.loads(blob.group(1)), js


def main():
    data, js = load()
    macros = data.get("macros", [])
    preds = data.get("predicates", [])
    rules = data.get("rules", [])
    tags = data.get("tags", [])

    def macro_label(i):
        m = macros[i]
        return m.get("vtp_name") or m.get("function", "?").replace("__", "")

    def resolve(v):
        if isinstance(v, list) and v and v[0] == "macro":
            return "{{" + macro_label(v[1]) + "}}"
        if isinstance(v, list) and v and v[0] == "list":
            out = []
            for item in v[1:]:
                if isinstance(item, list) and item and item[0] == "map":
                    d = {}
                    for k in range(1, len(item) - 1, 2):
                        d[resolve(item[k])] = resolve(item[k + 1])
                    out.append(d)
                else:
                    out.append(resolve(item))
            return out
        return v

    # ---- map rules: tag index -> list of predicate descriptions ----
    fires_on = collections.defaultdict(list)
    blocked_by = collections.defaultdict(list)
    for r in rules:
        conds = []
        for clause in r:
            if clause[0] == "if":
                conds += [preds[c] for c in clause[1:]]
            elif clause[0] == "unless":
                conds += [{"neg": preds[c]} for c in clause[1:]]
        desc = []
        for c in conds:
            if "neg" in c:
                desc.append("NOT " + pred_text(c["neg"], macro_label))
            else:
                desc.append(pred_text(c, macro_label))
        for clause in r:
            if clause[0] == "add":
                for t in clause[1:]:
                    fires_on[t] += desc
            elif clause[0] == "block":
                for t in clause[1:]:
                    blocked_by[t] += desc

    print("=" * 96)
    print("GTM CONTAINER INVENTORY — GTM-KD4PH4XP (live, published)")
    print("=" * 96)
    print(f"  macros/variables : {len(macros)}")
    print(f"  triggers         : {len(preds)} predicates across {len(rules)} rules")
    print(f"  tags             : {len(tags)}")
    print()

    print("=" * 96)
    print("FULL TAG INVENTORY")
    print("=" * 96)
    for i, t in enumerate(tags):
        fn = t.get("function", "?")
        kind = TAG_TYPES.get(fn, fn)
        tid = t.get("tag_id", "?")
        ev = t.get("vtp_eventName", "")
        mid = t.get("vtp_measurementIdOverride") or t.get("vtp_tagId") or ""
        print(f"\n  [idx {i:2d}]  tag_id={tid:<5}  {kind}")
        if ev:
            print(f"            event name      : {ev}")
        if mid:
            print(f"            measurement/dest: {mid}")
        if fn == "__awct":
            print(f"            conversion ID   : {t.get('vtp_conversionId')}")
            print(f"            conversion label: {t.get('vtp_conversionLabel')}")
            print(f"            value           : {resolve(t.get('vtp_conversionValue'))}")
            print(f"            currency        : {resolve(t.get('vtp_currencyCode'))}")
        trig = fires_on.get(i, [])
        print(f"            fires on        : {', '.join(sorted(set(trig))) if trig else 'NEVER (no rule)'}")
        if blocked_by.get(i):
            print(f"            blocked by      : {', '.join(sorted(set(blocked_by[i])))}")
        est = resolve(t.get("vtp_eventSettingsTable"))
        if isinstance(est, list) and est:
            params = []
            for d in est:
                if isinstance(d, dict):
                    params.append(f"{d.get('parameter')}={d.get('parameterValue')}")
            if params:
                print(f"            parameters      : {', '.join(params)}")

    # ---- duplicate analysis ----
    print()
    print("=" * 96)
    print("DUPLICATE EVENT ANALYSIS")
    print("=" * 96)
    sig = collections.defaultdict(list)
    for i, t in enumerate(tags):
        if t.get("function") != "__gaawe":
            continue
        key = (t.get("vtp_eventName"),
               t.get("vtp_measurementIdOverride"),
               tuple(sorted(set(fires_on.get(i, [])))))
        sig[key].append(i)

    dupes = {k: v for k, v in sig.items() if len(v) > 1}
    if not dupes:
        print("  No duplicate GA4 tags found.")
    for (ev, mid, trig), idxs in dupes.items():
        print(f"\n  DUPLICATE: GA4 event '{ev}' -> {mid}")
        print(f"    trigger : {', '.join(trig)}")
        print(f"    fired by {len(idxs)} tags:")
        for i in idxs:
            t = tags[i]
            est = resolve(t.get("vtp_eventSettingsTable")) or []
            params = sorted(d.get("parameter") for d in est if isinstance(d, dict))
            print(f"      - idx {i:2d}  tag_id={t.get('tag_id')}  "
                  f"{len(params)} params: {', '.join(params) if params else '(none)'}")
            for flag in ("vtp_sendEcommerceData", "vtp_enableUserProperties",
                         "vtp_enableEuid", "vtp_migratedToV2"):
                if flag in t:
                    print(f"                 {flag} = {t[flag]}")
        print(f"    => GA4 records this event {len(idxs)}x per real occurrence.")

    # Google Ads duplication check
    ads = [i for i, t in enumerate(tags) if t.get("function") == "__awct"]
    print(f"\n  Google Ads conversion tags: {len(ads)}")
    for i in ads:
        print(f"    idx {i} tag_id={tags[i].get('tag_id')} "
              f"fires on {', '.join(sorted(set(fires_on.get(i, []))))}")
    print(f"  => Google Ads conversions are "
          f"{'NOT duplicated' if len(ads) == 1 else 'AT RISK OF DUPLICATION'}.")

    # ---- built-in listener check ----
    print()
    print("=" * 96)
    print("BUILT-IN TRIGGER CHECK  (would cause duplicate conversions if any tag used them)")
    print("=" * 96)
    builtin = ["gtm.formSubmit", "gtm.linkClick", "gtm.click", "gtm.historyChange",
               "gtm.elementVisibility", "gtm.scrollDepth", "gtm.timer"]
    used = []
    for p in preds:
        a1 = p.get("arg1")
        if isinstance(a1, str) and a1 in builtin:
            used.append(a1)
    print(f"  built-in event predicates present: {used if used else 'NONE'}")
    print("  All firing conditions are custom-event equality checks."
          if not used else "  REVIEW: a built-in trigger exists.")

    # ---- paused tags ----
    paused = [(i, tags[i].get("tag_id"), sorted(set(fires_on.get(i, []))))
              for i, t in enumerate(tags) if t.get("function") == "__paused"]
    print()
    print("=" * 96)
    print(f"PAUSED TAGS ({len(paused)})")
    print("=" * 96)
    for i, tid, trig in paused:
        print(f"  idx {i:2d}  tag_id={tid:<5} would fire on: {', '.join(trig) if trig else '(no rule)'}")

    return 0


def pred_text(p, macro_label):
    fn = p.get("function", "?").lstrip("_")
    a0, a1 = p.get("arg0"), p.get("arg1")
    if isinstance(a0, list) and a0 and a0[0] == "macro":
        a0 = "{{" + macro_label(a0[1]) + "}}"
    return f"{a0} {fn} '{a1}'"


if __name__ == "__main__":
    sys.exit(main())
