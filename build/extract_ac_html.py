"""Lift the AC page's unique content sections out verbatim.

These blocks (comparison table, problems grid, before/after slider, chemical-wash
comparison, six-step process, property types, brands) are good content that
already ranks. They are preserved character-for-character and re-composed by
build_ac.py into the regenerated page, rather than being rewritten.

Writes build/ac_blocks.py.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "ac-service-dubai.html"

# id -> variable name. Order here is not the render order; build_ac.py decides that.
WANTED = {
    "why": "COMPARISON",
    "problems": "PROBLEMS",
    "before-after": "BEFORE_AFTER",
    "chemical": "CHEMICAL",
    "process": "PROCESS",
    "residential": "PROPERTY_TYPES",
    "brands": "BRANDS",
}


def extract_section(text, section_id):
    """Return the full <section ...id="X"...> ... </section> block.

    Sections do not nest in this document, so matching to the next </section>
    is safe; we assert that no inner <section appears in the captured block.
    """
    start = re.search(r'<section[^>]*id="%s"[^>]*>' % re.escape(section_id), text)
    if not start:
        raise SystemExit(f"FAILED: section id='{section_id}' not found")
    end = text.index("</section>", start.start()) + len("</section>")
    block = text[start.start():end]
    if "<section" in block[1:]:
        raise SystemExit(f"FAILED: nested <section> inside id='{section_id}'")
    return block


def main():
    text = SRC.read_text(encoding="utf-8")

    if (ROOT / "build" / "ac_blocks.py").exists() and "--force" not in sys.argv:
        print(
            "Nothing to do: build/ac_blocks.py already exists.\n"
            "This is a ONE-SHOT migration script and ac_blocks.py is now the\n"
            "source of truth for these sections. Re-run with --force only if you\n"
            "intend to re-extract from the current ac-service-dubai.html."
        )
        return 0

    parts = ["'''AC page content blocks, extracted verbatim from the previous\n"
             "ac-service-dubai.html by build/extract_ac_html.py. Do not hand-edit.\n'''\n"]

    for section_id, var in WANTED.items():
        block = extract_section(text, section_id)
        # sanity: none of the preserved blocks may carry a testimonial
        for banned in ("rev-card", "blockquote", "rev-stars"):
            if banned in block:
                raise SystemExit(f"FAILED: '{banned}' found in preserved section '{section_id}'")
        parts.append(f'{var} = """{block}"""\n')
        print(f"  {len(block):6d} chars  #{section_id} -> {var}")

    (ROOT / "build" / "ac_blocks.py").write_text("\n".join(parts), encoding="utf-8", newline="\n")
    print("\nbuild/ac_blocks.py written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
