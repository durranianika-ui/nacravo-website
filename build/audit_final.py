"""Production-readiness audit: the checks the earlier scripts did NOT cover.

Deliberately assumes nothing previously passed. Covers:
  * WCAG AA contrast, computed properly (previously reported as unverified)
  * redirect chains and loops
  * trailing-slash / clean-URL consistency
  * every referenced image exists; every image in /images is referenced
  * duplicate imagery across pages
  * DOM size and render-blocking resources
  * mailto/tel/WhatsApp link hygiene
"""

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- contrast
def srgb_to_lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    lo, hi = sorted((a, b))
    return (hi + 0.05) / (lo + 0.05)


PALETTE = {
    "pearl": "#F5F2EC", "sage": "#7E8F70", "moss": "#3B4636", "euca": "#C9D2BF",
    "sand": "#E8E0D0", "stone": "#8C8880", "clay": "#B9876B", "line": "#E2DCCF",
    "moss-deep": "#2E372B", "white": "#FFFFFF", "wa-green": "#25D366",
}

# (label, foreground, background, is_large_text, where)
CONTRAST_CHECKS = [
    ("Body text",                 "#3B4636", "#F5F2EC", False, "body on pearl"),
    ("Body text on white",        "#3B4636", "#FFFFFF", False, "cards"),
    ("Secondary text #54594C",    "#54594C", "#F5F2EC", False, "lead / section copy"),
    ("Secondary text on white",   "#54594C", "#FFFFFF", False, "anchor-card p"),
    ("Card body #44483D",         "#44483D", "#FFFFFF", False, "list items"),
    ("Eyebrow (sage-text/pearl)", "#5E6C4F", "#F5F2EC", False, "eyebrow kicker"),
    ("Eyebrow (sage-text/white)", "#5E6C4F", "#FFFFFF", False, "drop-col heading"),
    ("Stone meta #6F6B63",        "#6F6B63", "#F5F2EC", False, "fine print / captions"),
    ("Stone on white",            "#6F6B63", "#FFFFFF", False, "lp-fineprint"),
    ("Nav link #5A5F52",          "#5A5F52", "#F5F2EC", False, "nav-links a"),
    ("Primary btn label",         "#F5F2EC", "#7E8F70", False, "btn-primary [BRAND DECISION]"),
    ("WhatsApp btn label",        "#FFFFFF", "#25D366", False, "btn-wa [BRAND DECISION]"),
    ("Ghost btn label",           "#3B4636", "#F5F2EC", False, "btn-ghost"),
    ("Footer text #BBC4B0",       "#BBC4B0", "#2E372B", False, "footer a"),
    ("Footer muted #9AA391",      "#9AA391", "#2E372B", False, "foot-legal"),
    ("Footer tag #9AA391",        "#9AA391", "#2E372B", False, "foot-bottom"),
    ("Footer heading pearl",      "#F5F2EC", "#2E372B", False, "footer h2.fh"),
    ("Pillar body #BBC4B0",       "#BBC4B0", "#2E372B", False, "pillar p (moss-deep)"),
    ("Pillar body on moss",       "#BBC4B0", "#3B4636", False, "pillar p"),
    ("CTA band body #C9D2BF",     "#C9D2BF", "#3B4636", False, "cta-band p"),
    ("Trust pill #54594C",        "#54594C", "#ECE6D8", False, "trust span"),
    ("Area chip #44483D",         "#44483D", "#FFFFFF", False, "area-chips span"),
    ("Error text #B04A3E",        "#B04A3E", "#FDF4F2", False, "err-msg"),
    ("Link sage-text underline",  "#5E6C4F", "#FFFFFF", False, "ctx-note a"),
    ("H1 / large heading",        "#3B4636", "#F5F2EC", True,  "h1, h2"),
    ("Gallery tag on overlay",    "#F5F2EC", "#2E372B", False, "gal-tag (85% moss)"),
    ("Sage icon/border (non-text)","#7E8F70", "#F5F2EC", True,  "checkmarks, icons - 3:1 UI threshold"),
]


def audit_contrast():
    print("=" * 78)
    print("WCAG CONTRAST — computed, not assumed  (AA: 4.5:1 normal, 3:1 large)")
    print("=" * 78)
    fails, warns = [], []
    for label, fg, bg, large, where in CONTRAST_CHECKS:
        r = ratio(fg, bg)
        need = 3.0 if large else 4.5
        need_aaa = 4.5 if large else 7.0
        if r < need:
            status, bucket = "FAIL AA", fails
        elif r < need_aaa:
            status, bucket = "PASS AA", warns
        else:
            status, bucket = "PASS AAA", None
        if bucket is not None and status == "FAIL AA":
            bucket.append((label, fg, bg, r, need, where))
        print(f"  {r:5.2f}:1  {status:8s}  {label:26s} {fg} on {bg}  ({where})")
    print()
    if fails:
        print(f"  {len(fails)} COMBINATION(S) FAIL WCAG AA:")
        for label, fg, bg, r, need, where in fails:
            print(f"    x {label}: {r:.2f}:1, needs {need}:1 — {fg} on {bg} ({where})")
    else:
        print("  All checked combinations meet WCAG AA.")
    return fails


# ---------------------------------------------------------------- redirects
def audit_redirects():
    print()
    print("=" * 78)
    print("REDIRECTS — chains, loops, and destination validity")
    print("=" * 78)
    cfg = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    redirects = {r["source"]: r["destination"] for r in cfg.get("redirects", [])}
    problems = []

    for src, dest in sorted(redirects.items()):
        target = dest.split("#")[0]
        # chain: destination is itself a redirect source
        if target in redirects:
            problems.append(f"CHAIN: {src} -> {dest} -> {redirects[target]}")
        # loop
        seen, cur = {src}, target
        while cur in redirects:
            cur = redirects[cur].split("#")[0]
            if cur in seen:
                problems.append(f"LOOP: {src} eventually returns to {cur}")
                break
            seen.add(cur)
        # destination must resolve to a real file
        name = target.strip("/")
        f = ROOT / (name + ".html") if name else ROOT / "index.html"
        if not f.is_file():
            problems.append(f"DEAD: {src} -> {dest} (no {f.name})")
        # source must NOT also exist as a real page (would shadow the redirect)
        src_file = ROOT / (src.strip("/") + ".html")
        if src_file.is_file():
            problems.append(f"SHADOWED: {src} redirects but {src_file.name} also exists")

    print(f"  {len(redirects)} redirects declared")
    if problems:
        for p in problems:
            print("    x " + p)
    else:
        print("  No chains, no loops, all destinations resolve, no shadowed sources.")
    return problems


# ---------------------------------------------------------------- urls
def audit_urls():
    print()
    print("=" * 78)
    print("URL CONSISTENCY — trailing slash / clean URLs / absolute paths")
    print("=" * 78)
    problems = []
    for p in sorted(ROOT.glob("*.html")):
        html = p.read_text(encoding="utf-8")
        for href in set(re.findall(r'href="(/[^"#?]*)"', html)):
            if href != "/" and href.endswith("/"):
                problems.append(f"{p.name}: trailing slash on {href}")
            if href.endswith(".html"):
                problems.append(f"{p.name}: .html extension in {href} (cleanUrls is on)")
        # canonical must be absolute, no trailing slash except root
        m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        if m:
            c = m.group(1)
            if not c.startswith("https://www.nacravo.com"):
                problems.append(f"{p.name}: canonical not absolute www — {c}")
            path = c.replace("https://www.nacravo.com", "")
            if path != "/" and path.endswith("/"):
                problems.append(f"{p.name}: canonical has trailing slash — {c}")
            if path.endswith(".html"):
                problems.append(f"{p.name}: canonical uses .html — {c}")
    if problems:
        for x in problems[:20]:
            print("    x " + x)
    else:
        print("  All internal links extensionless and slash-free; canonicals absolute.")
    return problems


# ---------------------------------------------------------------- images
def audit_images():
    print()
    print("=" * 78)
    print("IMAGES — existence, orphans, duplication across pages, dimensions")
    print("=" * 78)
    problems = []
    referenced = collections.defaultdict(set)   # file -> pages

    for p in sorted(ROOT.glob("*.html")):
        html = p.read_text(encoding="utf-8")
        for src in re.findall(r'(?:src|srcset)="([^"]+)"', html):
            for candidate in re.split(r",", src):
                m = re.match(r"\s*(images/[^\s]+)", candidate)
                if m:
                    referenced[m.group(1)].add(p.name)
        for og in re.findall(r'content="https://www\.nacravo\.com/(images/[^"]+)"', html):
            referenced[og].add(p.name + " (og)")

    for f, pages in sorted(referenced.items()):
        if not (ROOT / f).is_file():
            problems.append(f"MISSING FILE: {f} referenced by {sorted(pages)[:3]}")

    on_disk = {f"images/{p.name}" for p in (ROOT / "images").glob("*.jpg")}
    orphans = sorted(on_disk - set(referenced))
    print(f"  {len(referenced)} image paths referenced, {len(on_disk)} jpg files on disk")
    if orphans:
        print(f"  {len(orphans)} unreferenced (orphan) asset(s):")
        for o in orphans:
            print(f"    - {o}")

    # heavy re-use of the same image across many pages
    print("\n  Re-use across pages (hero/gallery duplication):")
    for f, pages in sorted(referenced.items(), key=lambda kv: -len(kv[1])):
        real = {x for x in pages if "(og)" not in x}
        if len(real) >= 3:
            print(f"    {f:34s} used on {len(real)} pages")

    if problems:
        for x in problems:
            print("    x " + x)
    return problems, orphans


# ---------------------------------------------------------------- weight
def audit_weight():
    print()
    print("=" * 78)
    print("PAGE WEIGHT / DOM SIZE / RENDER BLOCKING")
    print("=" * 78)
    css = (ROOT / "assets" / "nacravo.css").stat().st_size
    ac_css = (ROOT / "assets" / "nacravo-ac.css").stat().st_size
    js = (ROOT / "assets" / "nacravo.js").stat().st_size
    print(f"  shared css {css/1024:6.1f} KB   ac css {ac_css/1024:5.1f} KB   shared js {js/1024:5.1f} KB")
    print()
    for p in sorted(ROOT.glob("*.html")):
        html = p.read_text(encoding="utf-8")
        elements = len(re.findall(r"<[a-zA-Z][^>]*>", html))
        inline_css = sum(len(m) for m in re.findall(r"<style>(.*?)</style>", html, re.S))
        inline_js = sum(len(m) for m in re.findall(r"<script(?![^>]*src)[^>]*>(.*?)</script>", html, re.S))
        blocking = len(re.findall(r'<link[^>]+rel="stylesheet"', html))
        flag = "  <-- LARGE DOM" if elements > 1500 else ""
        print(f"  {p.name:30s} {p.stat().st_size/1024:6.1f} KB  {elements:5d} el  "
              f"inline css {inline_css/1024:5.1f} KB  inline js {inline_js/1024:5.1f} KB  "
              f"{blocking} blocking css{flag}")


# ---------------------------------------------------------------- links
def audit_link_hygiene():
    print()
    print("=" * 78)
    print("LINK HYGIENE — tel / mailto / WhatsApp / rel attributes")
    print("=" * 78)
    problems = []
    tel_set, mail_set, wa_set = set(), set(), set()
    for p in sorted(ROOT.glob("*.html")):
        html = p.read_text(encoding="utf-8")
        tel_set |= set(re.findall(r'href="tel:([^"]+)"', html))
        # strip ?subject= / ?body= prefills — same address, not an inconsistency
        mail_set |= {m.split("?", 1)[0] for m in re.findall(r'href="mailto:([^"]+)"', html)}
        wa_set |= set(re.findall(r'href="https://wa\.me/(\d+)', html))
        for a in re.findall(r"<a\b[^>]*>", html):
            if 'target="_blank"' in a and "noopener" not in a:
                problems.append(f"{p.name}: target=_blank without rel=noopener")
                break
    print(f"  tel: values      {sorted(tel_set)}")
    print(f"  mailto: values   {sorted(mail_set)}")
    print(f"  wa.me numbers    {sorted(wa_set)}")
    if len(tel_set) > 1 or len(mail_set) > 1 or len(wa_set) > 1:
        problems.append("Inconsistent contact values across the site")
    if problems:
        for x in problems:
            print("    x " + x)
    else:
        print("  Single consistent value for each; all _blank links carry rel=noopener.")
    return problems


def main():
    fails = audit_contrast()
    r = audit_redirects()
    u = audit_urls()
    i, orphans = audit_images()
    audit_weight()
    l = audit_link_hygiene()

    print()
    print("=" * 78)
    total = len(fails) + len(r) + len(u) + len(i) + len(l)
    print(f"BLOCKING ISSUES: {total}   |   orphan assets: {len(orphans)}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
