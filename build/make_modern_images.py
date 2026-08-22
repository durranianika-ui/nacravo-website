"""Generate AVIF and WebP alongside every JPEG in images/.

The JPEGs stay: they are the <img> fallback inside the <picture> the template
emits, so a browser that supports neither format is unaffected. Re-running is
cheap and idempotent — a derivative is only rebuilt when it is missing or older
than its source.

Usage:  python build/make_modern_images.py [--force]

Requires ImageMagick 7 on PATH (`magick`).
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES = ROOT / "images"

# Quality chosen by eye against the originals: these are soft-focus interior
# photographs, where the formats do well. Raise, do not lower, if banding shows
# in a gradient.
WEBP_Q = "80"
AVIF_Q = "55"

FORCE = "--force" in sys.argv


def newer(src, dst):
    return not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime


def encode(src, dst, args):
    cmd = ["magick", str(src)] + args + [str(dst)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  FAILED " + dst.name + ": " + r.stderr.strip()[:200])
        return 0
    return dst.stat().st_size


def main():
    jpegs = sorted(IMAGES.glob("*.jpg"))
    if not jpegs:
        print("no JPEGs found in " + str(IMAGES))
        return 1

    j_total = w_total = a_total = 0
    built = 0
    for src in jpegs:
        j = src.stat().st_size
        j_total += j
        webp = src.with_suffix(".webp")
        avif = src.with_suffix(".avif")

        if FORCE or newer(src, webp):
            encode(src, webp, ["-quality", WEBP_Q, "-define", "webp:method=6"])
            built += 1
        if FORCE or newer(src, avif):
            encode(src, avif, ["-quality", AVIF_Q])
            built += 1

        w = webp.stat().st_size if webp.exists() else 0
        a = avif.stat().st_size if avif.exists() else 0
        w_total += w
        a_total += a
        print("  {0:<28} jpg {1:6.1f}  webp {2:6.1f}  avif {3:6.1f} KB".format(
            src.name, j / 1024, w / 1024, a / 1024))

    print("\n{0} files, {1} derivatives (re)built".format(len(jpegs), built))
    print("total  jpg {0:.0f} KB   webp {1:.0f} KB ({2:.0f}%)   avif {3:.0f} KB ({4:.0f}%)".format(
        j_total / 1024, w_total / 1024, 100 * w_total / j_total,
        a_total / 1024, 100 * a_total / j_total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
