#!/usr/bin/env python3
"""
Build the UrbanLoop wordmark as real vector outlines.

Why this exists: the reference board's wordmark was *typed text* rendered by an
image generator, which is why it has no optical corrections and cannot be
reproduced at scale. This composes actual glyph outlines from Inter (OFL-1.1),
applies measured optical spacing, and emits a single SVG path per weight.

Not a font-subset: the output is standalone path geometry with no font
dependency, so it renders identically anywhere with no webfont load.

    python3 brand/build_wordmark.py
"""
import os
import sys

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts", "inter-extract", "extras", "ttf")
OUT = os.path.join(HERE, "logo")

WORD = "UrbanLoop"

# Optical pair corrections in em units (negative = tighten).
#
# Inter applies ZERO kerning to all eight of these pairs, so its own sidebearings
# are already well tuned. Measured minimum optical gaps (brand/measure_spacing.py)
# across the shared ink band were:
#   U+r .132  r+b .087  b+a .086  a+n .137  n+L .147  L+o .095  o+o .081  o+p .107
#   mean .109
# Corrections below pull the outliers toward the mean but deliberately do not
# equalise it exactly: round pairs (o+o) are meant to sit tighter than flat-sided
# ones, which is the whole point of optical sidebearings. Over-equalising is what
# produced the over-tight L+o in the first pass.
PAIRS = {
    ("U", "r"): -0.018,
    ("r", "b"): +0.008,
    ("b", "a"): +0.006,
    ("a", "n"): -0.014,
    ("n", "L"): -0.018,
    ("L", "o"): -0.016,
    ("o", "o"): -0.002,
    ("o", "p"): -0.002,
}

WEIGHTS = {
    "semibold": "Inter-SemiBold.ttf",   # primary wordmark
    "medium":   "Inter-Medium.ttf",     # airy variant for large display
    "bold":     "Inter-Bold.ttf",       # very small sizes / favicon
}


def _layout(font, tracking_em, text=None, pairs=None):
    """Yield (glyph_name, x_units) for each character, in em-accurate units."""
    text = text if text is not None else WORD
    pairs = PAIRS if pairs is None else pairs
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    x, prev = 0.0, None
    for ch in text:
        if prev is not None:
            x += (tracking_em + pairs.get((prev, ch), 0.0)) * upm
        name = cmap[ord(ch)]
        yield name, x
        x += gs[name].width
        prev = ch


def build(weight_key, tracking_em=-0.012, text=None, pairs=None):
    """Return (combined_path_d, x0, y0, x1, y1) in font units."""
    font = TTFont(os.path.join(FONTS, WEIGHTS[weight_key]))
    gs = font.getGlyphSet()

    d_parts, xs, ys = [], [], []
    for name, x in _layout(font, tracking_em, text, pairs):
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
        gs[name].draw(TransformPen(pen, Transform().translate(x, 0).scale(1, -1)))
        d_parts.append(pen.getCommands())

        bp = ControlBoundsPen(gs)
        gs[name].draw(TransformPen(bp, Transform().translate(x, 0).scale(1, -1)))
        if bp.bounds:
            xs += [bp.bounds[0], bp.bounds[2]]
            ys += [bp.bounds[1], bp.bounds[3]]

    return " ".join(p for p in d_parts if p), min(xs), min(ys), max(xs), max(ys)


def cap_height(weight_key="semibold"):
    """Cap height in font units — used to align a mark against the wordmark."""
    font = TTFont(os.path.join(FONTS, WEIGHTS[weight_key]))
    return font["OS/2"].sCapHeight


def svg(weight_key, fill, tracking_em=-0.012, pad_em=0.02):
    d, x0, y0, x1, y1 = build(weight_key, tracking_em)
    upm = TTFont(os.path.join(FONTS, WEIGHTS[weight_key]))["head"].unitsPerEm
    pad = upm * pad_em
    vb = (x0 - pad, y0 - pad, (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]:.0f} {vb[1]:.0f} '
            f'{vb[2]:.0f} {vb[3]:.0f}" role="img" aria-label="UrbanLoop">'
            f'<path d="{d}" fill="{fill}"/></svg>')


VARIANTS = [
    ("urbanloop-wordmark-dark.svg",        "semibold", "#111518",      -0.012),
    ("urbanloop-wordmark-light.svg",       "semibold", "#FAFBFC",      -0.012),
    ("urbanloop-wordmark-mono.svg",        "semibold", "currentColor", -0.012),
    ("urbanloop-wordmark-medium-dark.svg", "medium",   "#111518",      -0.010),
    ("urbanloop-wordmark-small-dark.svg",  "bold",     "#111518",      -0.004),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, w, fill, tr in VARIANTS:
        content = svg(w, fill, tr)
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"  wrote {name:<40} {len(content):>7,} chars")

    print("\nbaseline metrics (font units, Inter upm=2048):")
    d, x0, y0, x1, y1 = build("semibold")
    print(f"  inked width  {x1 - x0:.0f}   height {y1 - y0:.0f}")
    print(f"  cap top {y0:.0f}   baseline 0   descender {y1:.0f}")

    print("\noptical pair corrections applied (em):")
    for (a, b), v in sorted(PAIRS.items()):
        print(f"  {a}+{b}: {v:+.3f}")


if __name__ == "__main__":
    sys.exit(main())
