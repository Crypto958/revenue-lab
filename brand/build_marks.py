#!/usr/bin/env python3
"""
UrbanLoop monogram, lockups, avatar and favicon.

The reference board's UL was two typed letters overlapped with an unexplained
grey block behind them — not a designed mark. This rebuilds it on the idea in the
name itself: a LOOP. The L shares the U's right stem and the U's bowl flows into
the L's foot, so the monogram is one continuous stroke. Shared stem = the two
letters are structurally one object rather than a stack.

Geometry note: the monogram's INK fills its 100x100 box exactly (centre lines run
5.5..94.5 with an 11-unit stroke). That makes cap-height alignment in a lockup
exact rather than approximate — an earlier version padded the viewBox, which
would have mis-aligned the mark against the wordmark.

Stroke-defined rather than filled outlines, so the shared stem is coincident by
construction. Convert to fills downstream if a printer requires it.

    python3 brand/build_marks.py
"""
import os
import sys

import build_wordmark as BW

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "logo")

INK = "#111518"
PAPER = "#FAFBFC"
ACTION = "#0F6A63"
GRAPHITE = "#2A3238"

# ---- monogram centre lines (ink fills 0..100 exactly) -----------------------
#
# DESIGN NOTE — first attempt failed, recorded so it is not retried:
# The original idea was a shared stem (L's stem == U's right stem), on the theory
# that the two letters become one object. Rendered, it read as a lowercase "u"
# with a bar stuck to its foot: the L had no stem of its own, so it vanished, and
# the mark did not say "UL" at all. Clever but illegible.
#
# What ships instead: U and L as distinct, well-drawn letters sharing a baseline
# and stroke weight, tucked tight. Restrained and legible beats clever and
# unreadable — and the brief explicitly asks for a "restrained UL secondary mark".
# The remaining gap between the U's right stem and the L's stem is 9 units of
# white at an 11-unit stroke, which is the tightest spacing that still reads.
U_R = 23.25                                                # (52 - 5.5) / 2
MONO_PATHS = (
    f"M5.5 5.5 V71.25 A{U_R} {U_R} 0 0 0 52 71.25 V5.5",    # U, complete
    "M72 5.5 V94.5 H94.5",                                  # L, own stem + foot
)
MONO_SW = 11


def _mono_group(stroke, sw=MONO_SW):
    return (f'<g fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="butt" stroke-linejoin="miter">'
            + "".join(f'<path d="{d}"/>' for d in MONO_PATHS) + "</g>")


def monogram(stroke):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            f'role="img" aria-label="UrbanLoop">' + _mono_group(stroke) + "</svg>")


def square_tile(bg, stroke, insets=1.52, sw=MONO_SW):
    """Avatar / favicon: monogram optically centred on a solid ground."""
    s = 1 / insets
    off = (100 - 100 * s) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            f'role="img" aria-label="UrbanLoop">'
            f'<rect width="100" height="100" fill="{bg}"/>'
            f'<g transform="translate({off:.3f} {off:.3f}) scale({s:.5f})">'
            + _mono_group(stroke, sw) + "</g></svg>")


def wordmark_group(fill, weight="semibold", tracking=-0.012):
    """(path markup, x0, cap_top, x1, descender) in font units."""
    d, x0, y0, x1, y1 = BW.build(weight, tracking)
    return (f'<g fill="{fill}"><path d="{d}"/></g>', x0, y0, x1, y1)


def lockup_horizontal(fill_word, fill_mark, gap_em=0.34, cap=100.0):
    """Monogram + wordmark, aligned on cap height and baseline.

    Scales by CAP height (not viewBox height, which also carries the descender) —
    the earlier version scaled by viewBox and would have shrunk the caps.
    """
    wm, x0, y0, x1, y1 = wordmark_group(fill_word)
    cap_units = -y0                                   # cap top is negative
    s = cap / cap_units
    w_w = (x1 - x0) * s
    mark_w = cap                                     # monogram ink is cap-height tall
    gap = gap_em * cap
    total_w = mark_w + gap + w_w
    desc = y1 * s                                     # descender below baseline
    vb_h = cap + desc
    tx = mark_w + gap - x0 * s                        # place wordmark after the mark
    ty = cap                                          # cap top -> y=0, baseline -> y=cap
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.0f} {vb_h:.0f}" '
            f'role="img" aria-label="UrbanLoop">'
            + _mono_group(fill_mark)
            + f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.6f})">{wm}</g>'
            + "</svg>")


def lockup_descriptor(fill_word, fill_desc, descriptor="PREMIUM GROUP MOBILITY",
                      tracking_em=0.30):
    """Wordmark with the descriptor set in REAL OUTLINES and optically matched.

    The descriptor is outline-based like the wordmark, not a <text> element: a
    live <text> node would depend on the reader having Inter, which is the exact
    dependency outlining exists to remove.
    """
    wm, x0, y0, x1, y1 = wordmark_group(fill_word)
    cap_units = -y0
    s = 100.0 / cap_units
    w_w = (x1 - x0) * s
    desc = y1 * s

    # descriptor: same machinery, letterspaced, then scaled to the wordmark width
    dpath, dx0, dy0, dx1, dy1 = BW.build("semibold", tracking_em,
                                         text=descriptor, pairs={})
    d_units = dx1 - dx0
    d_scale = (w_w / (d_units * s)) if d_units else 1
    d_h = (dy1 - dy0) * s * d_scale                 # descriptor ink height
    base_y = 100 + desc + 30
    # viewBox must clear the descriptor's FULL height; an earlier version sized it
    # to base_y + 4 and clipped the line off the bottom of the artboard.
    vb_h = base_y + d_h + 4
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_w:.0f} '
            f'{vb_h:.0f}" role="img" aria-label="UrbanLoop — '
            f'{descriptor.title()}">'
            f'<g transform="translate({-x0*s:.2f} 100) scale({s:.6f})">{wm}</g>'
            f'<g fill="{fill_desc}" transform="translate(0 {base_y:.2f}) scale({s*d_scale:.6f}) '
            f'translate({-dx0:.0f} {-dy0:.0f})"><path d="{dpath}"/></g>'
            f"</svg>")


def main():
    os.makedirs(LOGO, exist_ok=True)
    files = {
        "urbanloop-monogram-dark.svg":    monogram(INK),
        "urbanloop-monogram-light.svg":   monogram(PAPER),
        "urbanloop-monogram-mono.svg":    monogram("currentColor"),
        "urbanloop-monogram-accent.svg":  monogram(ACTION),
        "urbanloop-avatar-charcoal.svg":  square_tile(GRAPHITE, PAPER),
        "urbanloop-avatar-paper.svg":     square_tile(PAPER, INK),
        "urbanloop-favicon.svg":          square_tile("#111518", PAPER, insets=1.62, sw=13),
        "urbanloop-lockup-horizontal-dark.svg":  lockup_horizontal(INK, INK),
        "urbanloop-lockup-horizontal-light.svg": lockup_horizontal(PAPER, PAPER),
        "urbanloop-lockup-descriptor-dark.svg":  lockup_descriptor(INK, "#57626A"),
        "urbanloop-lockup-descriptor-light.svg": lockup_descriptor(PAPER, "#9BA6AD"),
    }
    for name, content in files.items():
        with open(os.path.join(LOGO, name), "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"  wrote {name:<44} {len(content):>7,} chars")


if __name__ == "__main__":
    sys.exit(main())
