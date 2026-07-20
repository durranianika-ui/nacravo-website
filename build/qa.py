"""Whole-site QA for the Nacravo static site.

There is no framework build/lint/typecheck to run here, so this stands in for
one. It validates every .html file in the repo root:

  * structure      — doctype, lang, single <h1>, title/description present
  * metadata       — title/description/canonical unique across pages
  * schema         — every application/ld+json block parses, required @type set
  * links          — every internal href resolves to a real route or anchor
  * anchors        — every #fragment target exists on the target page
  * ids            — no duplicate id on a page
  * accessibility  — inputs labelled, images have alt, buttons have names
  * contact        — no stale phone number or privacy@ address survives
  * tracking       — exactly one GTM container + one tracking layer per page

Usage: ./.venv/Scripts/python.exe build/qa.py
"""

import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_FILES = {"thank-you.html"}          # noindex utility page, not linked
STALE = ["971556365807", "+971 55 636 5807", "privacy@nacravo.com"]

errors = []
warnings = []


class Doc(HTMLParser):
    """Minimal parser collecting only what the checks below need."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []          # href values
        self.h1 = 0
        self.title = None
        self._in_title = False
        self.images = []         # (src, alt-or-None)
        self.inputs = []         # (tag, id, type, aria_label, aria_labelledby)
        self.labels_for = set()
        self.lang = None
        self.jsonld = []
        self._in_ld = False
        self._ld_buf = []
        self.buttons = []        # (has_text_placeholder, aria_label)
        self._btn_stack = []
        self.scripts_src = []
        self.gtm_ids = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "stylesheet" and "href" in a:
            self.links.append(a["href"])
        if tag == "img":
            self.images.append((a.get("src", ""), a.get("alt")))
        if tag in ("input", "select", "textarea"):
            if a.get("type") not in ("hidden", "submit", "button"):
                self.inputs.append((tag, a.get("id"), a.get("type"),
                                    a.get("aria-label"), a.get("aria-labelledby")))
        if tag == "label" and "for" in a:
            self.labels_for.add(a["for"])
        if tag == "script":
            if "src" in a:
                self.scripts_src.append(a["src"])
            if a.get("type") == "application/ld+json":
                self._in_ld = True
                self._ld_buf = []
        if tag == "button":
            self._btn_stack.append({"aria": a.get("aria-label"), "text": ""})

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self.jsonld.append("".join(self._ld_buf))
            self._in_ld = False
        if tag == "button" and self._btn_stack:
            b = self._btn_stack.pop()
            self.buttons.append((b["text"].strip(), b["aria"]))

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_ld:
            self._ld_buf.append(data)
        if self._btn_stack:
            self._btn_stack[-1]["text"] += data


def route_to_file(route):
    """Map a site route to the file that serves it (Vercel cleanUrls)."""
    route = route.split("?", 1)[0]
    if route == "/":
        return ROOT / "index.html"
    name = route.lstrip("/")
    if name.endswith(".html"):
        return ROOT / name
    direct = ROOT / name
    if direct.is_file():          # e.g. /sitemap.xml, /favicon.ico, /assets/x.css
        return direct
    return ROOT / (name + ".html")


def main():
    pages = sorted(p for p in ROOT.glob("*.html") if p.name not in SKIP_FILES)
    parsed = {}

    redirects = set()
    vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    for r in vercel.get("redirects", []):
        redirects.add(r["source"])

    # ---------- parse every page ----------
    for path in pages:
        text = path.read_text(encoding="utf-8")
        doc = Doc()
        doc.feed(text)
        doc.raw = text
        parsed[path.name] = doc

        name = path.name

        if not text.lstrip().lower().startswith("<!doctype html>"):
            errors.append(f"{name}: missing <!DOCTYPE html>")
        if doc.lang != "en":
            errors.append(f"{name}: <html lang> is {doc.lang!r}, expected 'en'")
        if doc.h1 != 1:
            errors.append(f"{name}: found {doc.h1} <h1> elements, expected exactly 1")
        if not doc.title or not doc.title.strip():
            errors.append(f"{name}: empty <title>")

        if 'name="description"' not in text:
            errors.append(f"{name}: no meta description")
        if 'rel="canonical"' not in text:
            errors.append(f"{name}: no canonical link")

        # ---------- stale contact details ----------
        for s in STALE:
            if s in text:
                errors.append(f"{name}: stale contact detail present -> {s}")

        # ---------- heading hierarchy ----------
        # No skipped levels (h2 -> h4), and nothing above h1 in document order.
        levels = [int(m) for m in re.findall(r"<h([1-6])\b", text)]
        prev = 0
        for lv in levels:
            if prev and lv > prev + 1:
                errors.append(f"{name}: heading level skips h{prev} -> h{lv}")
                break
            prev = lv
        if levels and levels[0] != 1:
            errors.append(f"{name}: first heading is h{levels[0]}, expected h1")

        # ---------- escaping ----------
        # &amp;amp; means a pre-escaped string was escaped a second time.
        if "&amp;amp;" in text:
            errors.append(f"{name}: double-escaped entity (&amp;amp;) — a value was escaped twice")
        # A bare & in element TEXT content should be an entity. Scoped to text
        # rather than the whole document on purpose: script/style bodies contain
        # `&&`, and query strings like ...&family=Inter are ubiquitous in URLs
        # and parse correctly in every browser, so flagging those is noise.
        stripped = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", text, flags=re.S | re.I)
        for chunk in re.findall(r">([^<>]+)<", stripped):
            m = re.search(r"&(?!#?\w{1,8};)", chunk)
            if m:
                errors.append(f"{name}: unescaped '&' in text content -> {chunk.strip()[:80]!r}")
                break  # one report per page is enough

        # ---------- duplicate ids ----------
        dupes = {i for i in doc.ids if doc.ids.count(i) > 1}
        if dupes:
            errors.append(f"{name}: duplicate id(s) {sorted(dupes)}")

        # ---------- schema ----------
        for i, block in enumerate(doc.jsonld):
            try:
                data = json.loads(block)
            except json.JSONDecodeError as e:
                errors.append(f"{name}: JSON-LD block {i + 1} does not parse ({e})")
                continue
            if "@context" not in data or "@type" not in data:
                errors.append(f"{name}: JSON-LD block {i + 1} missing @context/@type")
            if data.get("@type") == "FAQPage":
                for q in data.get("mainEntity", []):
                    if not q.get("acceptedAnswer", {}).get("text", "").strip():
                        errors.append(f"{name}: FAQ schema entry with empty answer")

        # ---------- tracking: exactly one layer ----------
        gtm = len(re.findall(r"googletagmanager\.com/gtm\.js", text))
        if gtm != 1:
            errors.append(f"{name}: {gtm} GTM loader(s), expected exactly 1")
        inline_tracker = "window.nacravoTrack = {" in text
        shared_tracker = any("nacravo.js" in s for s in doc.scripts_src)
        if inline_tracker and shared_tracker:
            errors.append(f"{name}: BOTH inline tracker and shared nacravo.js — events would double-fire")
        if not inline_tracker and not shared_tracker:
            warnings.append(f"{name}: no tracking layer found")

        # ---------- accessibility ----------
        for src, alt in doc.images:
            if alt is None:
                errors.append(f"{name}: <img src='{src[:50]}'> has no alt attribute")
        for tag, el_id, el_type, aria, arialabelledby in doc.inputs:
            labelled = (el_id and el_id in doc.labels_for) or aria or arialabelledby
            if not labelled:
                errors.append(f"{name}: <{tag} id={el_id!r}> has no label")
        for text_content, aria in doc.buttons:
            if not text_content and not aria:
                errors.append(f"{name}: <button> with no accessible name")

    # ---------- metadata uniqueness ----------
    for field, pattern in [("title", None),
                           ("description", r'<meta name="description" content="([^"]+)"'),
                           ("canonical", r'<link rel="canonical" href="([^"]+)"')]:
        seen = {}
        for name, doc in parsed.items():
            if field == "title":
                value = (doc.title or "").strip()
            else:
                m = re.search(pattern, doc.raw)
                value = m.group(1).strip() if m else ""
            if not value:
                continue
            key = value.lower()
            if key in seen:
                errors.append(f"duplicate {field}: {name} and {seen[key]} share \"{value[:70]}\"")
            seen[key] = name

    # ---------- internal links + anchors ----------
    for name, doc in parsed.items():
        for href in doc.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
                continue
            if not href or href == "#":
                continue

            if href.startswith("#"):
                target = href[1:]
                if target and target not in doc.ids:
                    errors.append(f"{name}: in-page anchor '#{target}' has no matching element")
                continue

            route, _, fragment = href.partition("#")
            if route in redirects:
                continue

            target_file = route_to_file(route)
            if not target_file.is_file():
                errors.append(f"{name}: link '{href}' -> missing file {target_file.name}")
                continue

            if fragment and target_file.name.endswith(".html"):
                other = parsed.get(target_file.name)
                if other is None:
                    other = Doc()
                    other.feed(target_file.read_text(encoding="utf-8"))
                if fragment not in other.ids:
                    errors.append(f"{name}: link '{href}' -> '#{fragment}' not found in {target_file.name}")

    # ---------- sitemap agrees with reality ----------
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>https://www\.nacravo\.com(/[^<]*)</loc>", sitemap)
    for loc in locs:
        f = route_to_file(loc)
        if not f.is_file():
            errors.append(f"sitemap.xml: {loc} has no file")
    landing = ["home-cleaning", "deep-cleaning", "move-in-out-cleaning", "holiday-home-cleaning",
               "office-commercial-cleaning", "specialized-cleaning", "pest-control",
               "ac-service-dubai", "handyman-services", "annual-maintenance", "services"]
    for slug in landing:
        if f"/{slug}" not in locs:
            errors.append(f"sitemap.xml: /{slug} is missing")
    if "/ac-services" in locs:
        errors.append("sitemap.xml: /ac-services must not be listed (it is a 301 to /ac-service-dubai)")

    # ---------- documented media gaps ----------
    # Surfaced as warnings so a missing gallery stays visible rather than
    # quietly looking like a finished page.
    for name, doc in parsed.items():
        if "GALLERY PLACEHOLDER" in doc.raw:
            warnings.append(f"{name}: gallery intentionally absent — no honest photography available "
                            f"(see build/media.py GALLERY_GAPS)")

    # ---------- report ----------
    print(f"QA — {len(pages)} pages checked\n")
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
    print("PASS — structure, metadata, schema, links, anchors, a11y and sitemap all clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
