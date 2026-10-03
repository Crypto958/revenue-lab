#!/usr/bin/env python3
"""
Measure optical inter-letter gaps in the UrbanLoop wordmark.

The eye judges a letter pair by its TIGHTEST point, not by one sampled band. An
earlier version of this sampled only the x-height, which ignored the L's arm at
the baseline and produced a misleading number. This samples the full height where
both glyphs have ink and reports the minimum gap.

    python3 brand/measure_spacing.py
"""
import sys

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

FONT = "brand/fonts/inter-extract/extras/ttf/Inter-SemiBold.ttf"
WORD = "UrbanLoop"

# Current pair corrections under test (em). Inter applies 0 kerning to all of
# these, so anything here is a deliberate wordmark override.
PAIRS = {
    ("L", "o"): -0.030, ("U", "r"): -0.008, ("n", "L"): 0.006,
    ("b", "a"): -0.004, ("a", "n"): 0.002, ("o", "o"): -0.006, ("o", "p"): -0.004,
}


class FlattenPen(BasePen):
    def __init__(self, glyphSet, steps=40):
        super().__init__(glyphSet)
        self.segs, self.steps, self._pt = [], steps, None

    def _moveTo(self, pt):
        self._pt = pt

    def _lineTo(self, pt):
        if self._pt is not None:
            self.segs.append((self._pt, pt))
        self._pt = pt

    def _curveToOne(self, p1, p2, p3):
        p0, n = self._pt, self.steps
        for i in range(1, n + 1):
            t = i / n
            mt = 1 - t
            self._lineTo(((mt**3 * p0[0] + 3*mt**2*t * p1[0] + 3*mt*t**2 * p2[0] + t**3 * p3[0]),
                          (mt**3 * p0[1] + 3*mt**2*t * p1[1] + 3*mt*t**2 * p2[1] + t**3 * p3[1])))

    def _closePath(self):
        self._pt = None

    def _endPath(self):
        self._pt = None


def ink_span(segs, y):
    xs = []
    for (x0, y0), (x1, y1) in segs:
        if (y0 <= y < y1) or (y1 <= y < y0):
            t = (y - y0) / (y1 - y0)
            xs.append(x0 + t * (x1 - x0))
    if len(xs) < 2:
        return None
    xs.sort()
    spans = [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]
    return (min(s[0] for s in spans), max(s[1] for s in spans)) if spans else None


def yextent(segs):
    ys = [p[1] for s in segs for p in s]
    return min(ys), max(ys)


def min_gap(segs_a, xa, segs_b, xb, samples=160):
    """Tightest horizontal white gap between two placed glyphs."""
    lo_a, hi_a = yextent(segs_a)
    lo_b, hi_b = yextent(segs_b)
    lo, hi = max(lo_a, lo_b), min(hi_a, hi_b)      # only where BOTH have ink
    if hi <= lo:
        lo, hi = min(lo_a, lo_b), max(hi_a, hi_b)
    best = None
    for i in range(samples + 1):
        y = lo + (hi - lo) * i / samples
        sa, sb = ink_span(segs_a, y), ink_span(segs_b, y)
        if not sa or not sb:
            continue
        g = (sb[0] + xb) - (sa[1] + xa)
        if best is None or g < best:
            best = g
    return best


def main():
    font = TTFont(FONT)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm

    flat, widths = {}, {}
    for c in WORD:
        name = cmap[ord(c)]
        pen = FlattenPen(gs)
        gs[name].draw(pen)
        flat[c], widths[c] = pen.segs, gs[name].width

    pos, x, prev = [], 0.0, None
    for c in WORD:
        if prev is not None:
            x += PAIRS.get((prev, c), 0.0) * upm
        pos.append((c, x))
        x += widths[c]
        prev = c

    print("=== minimum optical gap per pair (the tightest point the eye reads) ===")
    print(f"{'pair':<7}{'gap(em)':>9}")
    rows = []
    for (a, xa), (b, xb) in zip(pos, pos[1:]):
        g = min_gap(flat[a], xa, flat[b], xb)
        if g is not None:
            rows.append((a, b, g / upm))
    mean = sum(r[2] for r in rows) / len(rows)
    for a, b, g in rows:
        flag = ""
        if g < mean - 0.020: flag = "  <-- too tight"
        elif g > mean + 0.020: flag = "  <-- too loose"
        print(f"{a}+{b:<5}{g:>9.4f}{flag}")
    print(f"{'MEAN':<7}{mean:>9.4f}")

    print("\n=== proposed corrections (equalise toward the mean) ===")
    for a, b, g in rows:
        cur = PAIRS.get((a, b), 0.0)
        new = cur + (mean - g)
        print(f"  {a}+{b}: {cur:+.4f} -> {new:+.4f}   (gap {g:+.4f} -> ~{mean:.4f})")

    print("\nPYTHON_DICT:")
    print("PAIRS = {")
    for a, b, g in rows:
        cur = PAIRS.get((a, b), 0.0)
        print(f'    ("{a}", "{b}"): {cur + (mean - g):+.4f},')
    print("}")


if __name__ == "__main__":
    sys.exit(main())
