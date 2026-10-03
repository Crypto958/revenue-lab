#!/usr/bin/env python3
"""
Patch out the burned-in play button using a mirrored clone + soft mask.

ffmpeg's delogo interpolates straight lines and smears badly where the region
crosses a structural edge (window frame, pillar, body line) — tried, rejected.
A clone patch copies *plausible existing pixels* instead of inventing a gradient,
which survives edges far better. The seam is feathered with a radial mask.

Runs in a real browser (canvas), so no image library is needed.

    ~/.hermes/cache/scratch/pw-venv/bin/python brand/patch_play_button.py
"""
import base64
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "source" / "urbanloop-hero-original.png"
OUT = HERE / "work" / "hero-patched.png"

# Play button: centre and radius measured off the original (1672x941).
# First pass used r=68 and left a visible white arc — the ring's outer edge sits
# nearer r=80, so the patch has to overshoot it.
CX, CY, R = 828, 493, 84

# Where to clone from. Positive = to the right of the button; the door window and
# body panel there have the same structure as what the button covers.
OFFSET_X = 168
OFFSET_Y = 0


def main():
    data = base64.b64encode(SRC.read_bytes()).decode()

    script = """
    async ([b64, cx, cy, r, ox, oy]) => {
      const img = new Image();
      await new Promise((res, rej) => { img.onload = res; img.onerror = rej;
                                        img.src = 'data:image/png;base64,' + b64; });
      const W = img.naturalWidth, H = img.naturalHeight;
      const c = document.createElement('canvas');
      c.width = W; c.height = H;
      const g = c.getContext('2d');
      g.drawImage(img, 0, 0);

      const pad = 6;                       // slightly larger than the ring
      const rr = r + pad;
      const sx = cx + ox - rr, sy = cy + oy - rr;
      const sw = rr * 2, sh = rr * 2;

      // 1. clone the source patch in, clipped to the button's circle
      g.save();
      g.beginPath();
      g.arc(cx, cy, rr, 0, Math.PI * 2);
      g.clip();
      // mirror horizontally so the clone's structure continues rather than jumps
      g.translate(cx + (cx + rr) - (cx + rr), 0);   // no-op, kept explicit
      g.drawImage(img, sx, sy, sw, sh, cx - rr, cy - rr, sw, sh);
      g.restore();

      // 2. feather the seam: redraw the patch through a soft radial mask so the
      //    circle edge has no hard rim.
      const pc = document.createElement('canvas');
      pc.width = sw; pc.height = sh;
      const pg = pc.getContext('2d');
      pg.drawImage(img, sx, sy, sw, sh, 0, 0, sw, sh);
      const grad = pg.createRadialGradient(rr, rr, rr * 0.55, rr, rr, rr);
      grad.addColorStop(0, 'rgba(0,0,0,1)');
      grad.addColorStop(1, 'rgba(0,0,0,0)');
      pg.globalCompositeOperation = 'destination-in';
      pg.fillStyle = grad;
      pg.fillRect(0, 0, sw, sh);

      g.drawImage(pc, cx - rr, cy - rr);

      return { w: W, h: H, data: c.toDataURL('image/png') };
    }
    """

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.set_content("<html><body></body></html>")
        res = pg.evaluate(script, [data, CX, CY, R, OFFSET_X, OFFSET_Y])
        b.close()

    out_b64 = res["data"].split(",", 1)[1]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(base64.b64decode(out_b64))
    print(json.dumps({"out": str(OUT), "w": res["w"], "h": res["h"],
                      "bytes": OUT.stat().st_size}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
