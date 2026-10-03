#!/usr/bin/env python3
"""Debug the descriptor lockup geometry — the line keeps clipping."""
import build_wordmark as BW

wm, x0, y0, x1, y1 = BW.build("semibold")
cap_units = -y0
s = 100.0 / cap_units
w_w = (x1 - x0) * s
desc = y1 * s

print(f"wordmark: x0={x0} y0={y0} x1={x1} y1={y1}")
print(f"  cap_units={cap_units}  s={s:.6f}")
print(f"  w_w={w_w:.1f}  descender-below-baseline={desc:.1f}")
print(f"  wordmark ink y: 0 .. {100 + desc:.1f}")

dpath, dx0, dy0, dx1, dy1 = BW.build("semibold", 0.30, text="PREMIUM GROUP MOBILITY", pairs={})
print(f"\ndescriptor raw: dx0={dx0} dy0={dy0} dx1={dx1} dy1={dy1}")
print(f"  width units={dx1-dx0}  ink height units={dy1-dy0}")

d_scale = w_w / ((dx1 - dx0) * s)
print(f"  d_scale={d_scale:.6f}")
d_h = (dy1 - dy0) * s * d_scale
print(f"  scaled descriptor height d_h={d_h:.1f}")

base_y = 100 + desc + 30
vb_h = base_y + d_h + 4
print(f"\n  descriptor places at y {base_y:.1f} .. {base_y + d_h:.1f}")
print(f"  viewBox height calculated = {vb_h:.1f}")
print(f"  fits inside viewBox? {base_y + d_h <= vb_h}")

print("\n--- actual SVG emitted ---")
import build_marks as BM
out = BM.lockup_descriptor("#111518", "#57626A")
import re
print("  viewBox:", re.search(r'viewBox="([^"]+)"', out).group(1))
for m in re.finditer(r'transform="([^"]+)"', out):
    print("  transform:", m.group(1))
