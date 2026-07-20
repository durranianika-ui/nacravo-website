"""Bring text and state colours up to WCAG AA.

Measured failures (build/audit_final.py) and what is done about each:

  FIXED — text and state colours, no brand surface changed:
    sage #7E8F70 used as TEXT      3.11:1 -> --sage-text #5E6C4F   5.03:1
    stone #8C8880 fine print       3.16:1 -> #6F6B63               4.75:1
    error text #C0574B             4.12:1 -> #B04A3E               4.98:1
    footer muted #8A9380           3.87:1 -> #9AA391               4.73:1

  NOT FIXED — requires a branding decision, reported instead:
    primary button pearl-on-sage   3.11:1
    WhatsApp button white-on-green 1.98:1
  Sage is a mid-tone: it fails with light labels AND with dark labels until the
  label is nearly black. Fixing these means changing the button colour itself,
  which the brief forbids. Options and ratios are in the SEO report.

Sage remains unchanged wherever it is decorative (icons, checkmarks, borders,
focus rings). Those are non-text UI components and pass the 3:1 threshold of
WCAG 1.4.11 at 3.11:1.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SAGE_TEXT = "#5E6C4F"
STONE_NEW = "#6F6B63"
ERROR_NEW = "#B04A3E"
FOOT_MUTED_NEW = "#9AA391"

# Selectors where sage is used as TEXT and must meet 4.5:1.
SAGE_TEXT_RULES = [
    (".eyebrow{font-size:13px;letter-spacing:0.14em;text-transform:uppercase;color:var(--sage)",
     ".eyebrow{font-size:13px;letter-spacing:0.14em;text-transform:uppercase;color:var(--sage-text)"),
    (".cc-banner a{color:var(--sage);text-decoration:underline}",
     ".cc-banner a{color:var(--sage-text);text-decoration:underline}"),
    (".drop-col .drop-h{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--sage)",
     ".drop-col .drop-h{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--sage-text)"),
    (".drop-col a:hover{color:var(--sage)}", ".drop-col a:hover{color:var(--sage-text)}"),
    (".mm-sub{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--sage)",
     ".mm-sub{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--sage-text)"),
    (".crumb a{color:var(--sage)}", ".crumb a{color:var(--sage-text)}"),
    (".lp-form summary.lp-more{font-size:13.5px;color:var(--sage)",
     ".lp-form summary.lp-more{font-size:13.5px;color:var(--sage-text)"),
    (".lp-form .lp-fineprint a{color:var(--sage);text-decoration:underline}",
     ".lp-form .lp-fineprint a{color:var(--sage-text);text-decoration:underline}"),
    (".rel-card .rel-go{font-size:13px;color:var(--sage)",
     ".rel-card .rel-go{font-size:13px;color:var(--sage-text)"),
    (".ctx-note a{color:var(--sage);text-decoration:underline;text-underline-offset:2px}",
     ".ctx-note a{color:var(--sage-text);text-decoration:underline;text-underline-offset:2px}"),
    (".prose a{color:var(--sage);text-decoration:underline;text-underline-offset:2px}",
     ".prose a{color:var(--sage-text);text-decoration:underline;text-underline-offset:2px}"),
    (".company-card a{color:var(--sage);text-decoration:underline}",
     ".company-card a{color:var(--sage-text);text-decoration:underline}"),
    (".toc a:hover{color:var(--moss)}", ".toc a:hover{color:var(--moss)}"),  # no-op guard
]

GLOBAL = [
    # add the new token next to the palette
    ("--stone:#8C8880;", f"--stone:{STONE_NEW};--sage-text:{SAGE_TEXT};"),
    ("--stone:#8C8880", f"--stone:{STONE_NEW}"),
    # state + footer colours
    ("color:#C0574B", f"color:{ERROR_NEW}"),
    ("color:#8A9380", f"color:{FOOT_MUTED_NEW}"),
]


def patch(path):
    text = path.read_text(encoding="utf-8")
    original = text
    n = 0

    for old, new in GLOBAL:
        if old in text and old != new:
            n += text.count(old)
            text = text.replace(old, new)

    for old, new in SAGE_TEXT_RULES:
        if old in text and old != new:
            n += text.count(old)
            text = text.replace(old, new)

    # ensure --sage-text exists wherever --sage does
    if "--sage:" in text and "--sage-text:" not in text:
        text = re.sub(r"(--sage:#7E8F70;)", r"\1--sage-text:" + SAGE_TEXT + ";", text, count=1)
        n += 1

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return n
    return 0


def main():
    targets = sorted(ROOT.glob("*.html")) + [ROOT / "build" / "extract_assets.py"]
    total = 0
    for p in targets:
        c = patch(p)
        if c:
            print(f"  {c:3d}  {p.relative_to(ROOT).as_posix()}")
            total += c
    print(f"\n{total} colour replacements")

    # verify the token landed everywhere sage is used
    missing = [p.name for p in ROOT.glob("*.html")
               if "--sage:" in p.read_text(encoding="utf-8")
               and "--sage-text:" not in p.read_text(encoding="utf-8")]
    if missing:
        print(f"FAILED: --sage-text missing in {missing}")
        return 1
    print("Verified: --sage-text defined wherever --sage is.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
