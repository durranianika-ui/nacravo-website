"""Escape bare '&' characters in element text content.

These are pre-existing minor markup-validity issues (mostly in headings like
"Bookings & Quotes"). Browsers render them fine, but they are invalid HTML and
trivially fixable.

Scope is deliberately narrow: only text BETWEEN tags is touched. Attribute
values and script/style bodies are left alone, so URL query strings (?a=1&b=2)
and JavaScript (a && b) are never modified.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SKIP_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.S | re.I)
BARE_AMP = re.compile(r"&(?!#?\w{1,8};)")


def fix(text):
    """Rebuild the document, escaping bare & only inside text nodes."""
    out = []
    pos = 0
    changes = []

    # Walk the document, skipping over script/style regions entirely.
    protected = [(m.start(), m.end()) for m in SKIP_RE.finditer(text)]

    def in_protected(i):
        return any(a <= i < b for a, b in protected)

    for m in re.finditer(r">([^<>]+)<", text):
        chunk = m.group(1)
        if in_protected(m.start()) or not BARE_AMP.search(chunk):
            continue
        fixed = BARE_AMP.sub("&amp;", chunk)
        out.append((m.start(1), m.end(1), fixed))
        changes.append(chunk.strip()[:60])

    if not out:
        return text, []

    result = []
    for start, end, replacement in out:
        result.append(text[pos:start])
        result.append(replacement)
        pos = end
    result.append(text[pos:])
    return "".join(result), changes


def main():
    total = 0
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        fixed, changes = fix(text)
        if changes:
            path.write_text(fixed, encoding="utf-8", newline="\n")
            total += len(changes)
            print(f"  {path.name}")
            for c in changes:
                print(f"      {c}")
    print(f"\n{total} text-content ampersand(s) escaped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
