"""Read-only SEO / structure audit across the site.

Reports facts; changes nothing. Used to drive the Phase 1 audit: heading
hierarchy, metadata lengths, image alt coverage, word counts, internal link
in-degree (orphan detection), keyword overlap between landing pages, and
Open Graph completeness.
"""

import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

LANDING = ["home-cleaning", "deep-cleaning", "move-in-out-cleaning",
           "holiday-home-cleaning", "office-commercial-cleaning",
           "specialized-cleaning", "pest-control", "ac-service-dubai",
           "handyman-services", "annual-maintenance"]
ALL_PAGES = LANDING + ["index", "services"]

STOP = set("""a an the and or of for in on at to with your our we you it is are be этой from that this by as
than then them they their there here what when which who how why do does not no yes if all any can
will just more most some such only own same so too very s t don now dubai nacravo service services""".split())


def text_of(html):
    """Visible text, with script/style/head stripped."""
    body = re.sub(r"<head\b.*?</head>", " ", html, flags=re.S | re.I)
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"&[a-z]+;", " ", body)
    return re.sub(r"\s+", " ", body).strip()


def main():
    docs = {}
    for slug in ALL_PAGES:
        p = ROOT / f"{slug}.html"
        if p.is_file():
            docs[slug] = p.read_text(encoding="utf-8")

    print("=" * 78)
    print("HEADING HIERARCHY  (h1 -> h2 -> h3, flags any skipped level)")
    print("=" * 78)
    for slug, html in docs.items():
        levels = [int(m) for m in re.findall(r"<h([1-4])\b", html)]
        counts = collections.Counter(levels)
        skips = []
        prev = 0
        for lv in levels:
            if prev and lv > prev + 1:
                skips.append(f"h{prev}->h{lv}")
            prev = lv
        flag = f"  SKIPS: {skips[:3]}" if skips else ""
        print(f"  {slug:30s} h1={counts[1]} h2={counts[2]:2d} h3={counts[3]:2d} h4={counts[4]:2d}{flag}")

    print()
    print("=" * 78)
    print("METADATA LENGTHS  (title target 50-60, description 140-160)")
    print("=" * 78)
    for slug, html in docs.items():
        t = re.search(r"<title>(.*?)</title>", html, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', html)
        tl = len(t.group(1)) if t else 0
        dl = len(d.group(1)) if d else 0
        tw = "" if 50 <= tl <= 60 else "  <-- title"
        dw = "" if 140 <= dl <= 160 else "  <-- desc"
        print(f"  {slug:30s} title={tl:3d}  desc={dl:3d}{tw}{dw}")

    print()
    print("=" * 78)
    print("CONTENT DEPTH + IMAGES")
    print("=" * 78)
    for slug, html in docs.items():
        words = len(text_of(html).split())
        imgs = re.findall(r"<img\b[^>]*>", html)
        no_alt = [i for i in imgs if 'alt="' not in i]
        lazy = [i for i in imgs if 'loading="lazy"' in i]
        dims = [i for i in imgs if 'width="' in i and 'height="' in i]
        thin = "  <-- THIN" if words < 600 else ""
        print(f"  {slug:30s} {words:5d} words  {len(imgs)} img "
              f"(alt {len(imgs)-len(no_alt)}/{len(imgs)}, lazy {len(lazy)}, dims {len(dims)}){thin}")

    print()
    print("=" * 78)
    print("OPEN GRAPH / SOCIAL")
    print("=" * 78)
    for slug, html in docs.items():
        og = re.search(r'<meta property="og:image" content="([^"]*)"', html)
        img = og.group(1).rsplit("/", 1)[-1] if og else "MISSING"
        exists = (ROOT / "images" / img).is_file() if og else False
        tw = "twitter:image" in html
        print(f"  {slug:30s} og:image={img:28s} exists={exists}  twitter={tw}")

    print()
    print("=" * 78)
    print("INTERNAL LINK IN-DEGREE  (how many pages link TO each landing page)")
    print("=" * 78)
    indeg = collections.Counter()
    sources = collections.defaultdict(set)
    for slug, html in docs.items():
        for href in set(re.findall(r'href="(/[^"#?]*)', html)):
            target = href.strip("/")
            if target in LANDING or target == "services":
                if target != slug:
                    indeg[target] += 1
                    sources[target].add(slug)
    for slug in LANDING + ["services"]:
        n = indeg[slug]
        flag = "  <-- ORPHAN" if n == 0 else ("  <-- WEAK" if n < 3 else "")
        print(f"  {slug:30s} in-links from {n:2d} pages{flag}")

    print()
    print("=" * 78)
    print("KEYWORD CLUSTER OVERLAP  (top title/h1/h2 terms shared between pages)")
    print("=" * 78)
    terms = {}
    for slug in LANDING:
        html = docs[slug]
        head = " ".join(re.findall(r"<h[12]\b[^>]*>(.*?)</h[12]>", html, re.S))
        head += " " + (re.search(r"<title>(.*?)</title>", html, re.S) or re.match("", "")).group(1)
        words = [w for w in re.findall(r"[a-z]+", head.lower()) if w not in STOP and len(w) > 3]
        terms[slug] = collections.Counter(words)

    pairs = []
    for i, a in enumerate(LANDING):
        for b in LANDING[i + 1:]:
            shared = set(w for w, c in terms[a].items() if c >= 2) & set(w for w, c in terms[b].items() if c >= 2)
            if shared:
                pairs.append((len(shared), a, b, sorted(shared)[:6]))
    pairs.sort(reverse=True)
    if not pairs:
        print("  no significant overlap")
    for n, a, b, shared in pairs[:10]:
        flag = "  <-- REVIEW" if n >= 3 else ""
        print(f"  {n} shared: {a} / {b}  {shared}{flag}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
