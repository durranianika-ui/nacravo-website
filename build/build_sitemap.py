"""Generate sitemap.xml from the site's actual routes.

Every entry is checked against a real .html file on disk, so a sitemap URL can
never point at a page that does not exist. /thank-you is intentionally excluded
because robots.txt disallows it.

Usage: ./.venv/Scripts/python.exe build/build_sitemap.py [YYYY-MM-DD]
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.nacravo.com"

# Pages whose content changed in this release get today's lastmod; the untouched
# legal pages keep their previous date so we do not falsely signal a change.
LEGAL_LASTMOD = "2026-07-11"

# (path, file, changefreq, priority, lastmod)
def routes(today):
    landing = [
        "home-cleaning", "deep-cleaning", "move-in-out-cleaning",
        "holiday-home-cleaning", "office-commercial-cleaning",
        "specialized-cleaning", "pest-control",
        "ac-service-dubai", "handyman-services", "annual-maintenance",
    ]

    items = [("/", "index.html", "weekly", "1.0", today),
             ("/services", "services.html", "weekly", "0.9", today)]

    for slug in landing:
        items.append((f"/{slug}", f"{slug}.html", "weekly", "0.9", today))

    items += [
        ("/legal", "legal.html", "monthly", "0.6", LEGAL_LASTMOD),
        ("/privacy-policy", "privacy-policy.html", "yearly", "0.5", today),
        ("/terms-of-service", "terms-of-service.html", "yearly", "0.5", today),
        ("/cookie-policy", "cookie-policy.html", "yearly", "0.4", today),
        ("/refund-policy", "refund-policy.html", "yearly", "0.4", today),
        ("/data-deletion", "data-deletion.html", "yearly", "0.4", today),
        ("/accessibility", "accessibility.html", "yearly", "0.4", today),
        ("/security", "security.html", "yearly", "0.4", today),
        ("/acceptable-use", "acceptable-use.html", "yearly", "0.4", today),
        ("/application", "application.html", "yearly", "0.4", LEGAL_LASTMOD),
        ("/sitemap", "sitemap.html", "monthly", "0.3", today),
    ]
    return items


def main():
    today = sys.argv[1] if len(sys.argv) > 1 else "2026-07-20"

    entries = []
    missing = []
    for path, filename, freq, priority, lastmod in routes(today):
        if not (ROOT / filename).is_file():
            missing.append(filename)
            continue
        entries.append(
            "  <url>\n"
            f"    <loc>{SITE}{path}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )

    if missing:
        print(f"FAILED: sitemap references missing files: {missing}")
        return 1

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(entries)
           + "\n</urlset>\n")

    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")
    print(f"sitemap.xml written — {len(entries)} URLs, all verified to exist on disk")
    return 0


if __name__ == "__main__":
    sys.exit(main())
