"""One-off sitewide replacement of Nacravo's public contact details.

Runs on raw bytes so file encodings and CRLF/LF line endings survive untouched.
Ordering matters: the longest, most specific patterns are replaced first so a
shorter pattern can never eat part of a longer one.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (old, new) applied in order — longest / most specific first.
REPLACEMENTS = [
    (b"+971 55 636 5807", b"+971 55 540 3038"),   # display format
    (b"+971556365807",    b"+971555403038"),      # tel: links, JSON-LD
    (b"971556365807",     b"971555403038"),       # wa.me links (bare)
    (b"privacy@nacravo.com", b"info@nacravo.com"),
]

SUFFIXES = {".html", ".xml", ".json", ".txt", ".webmanifest", ".md"}
SKIP_DIRS = {".git", ".venv", "node_modules", "build"}


def targets():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        yield path


def main():
    total = 0
    touched = []

    for path in targets():
        original = path.read_bytes()
        data = original
        per_file = 0

        for old, new in REPLACEMENTS:
            count = data.count(old)
            if count:
                data = data.replace(old, new)
                per_file += count

        if data != original:
            path.write_bytes(data)
            total += per_file
            touched.append((path.relative_to(ROOT).as_posix(), per_file))

    for name, count in sorted(touched):
        print(f"  {count:4d}  {name}")
    print(f"\n{total} replacements across {len(touched)} files")

    # Verify nothing survived.
    leftovers = []
    for path in targets():
        data = path.read_bytes()
        for old, _ in REPLACEMENTS:
            if old in data:
                leftovers.append(f"{path.relative_to(ROOT).as_posix()}: {old.decode()}")

    if leftovers:
        print("\nFAILED — leftovers found:")
        for item in leftovers:
            print("  " + item)
        return 1

    print("Verified: no old phone number or privacy@ address remains.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
