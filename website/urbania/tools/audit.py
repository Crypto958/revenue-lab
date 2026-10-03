#!/usr/bin/env python3
"""
Layout audit for the Urbania site.

Turns the visual checks into repeatable assertions: horizontal overflow, the
mobile sticky bar being on-screen and tappable, undersized tap targets, and
elements that overlap the sticky bar.

    ~/.hermes/cache/scratch/pw-venv/bin/python tools/audit.py

Exits non-zero if any hard problem is found.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8140"
SITE = pathlib.Path(__file__).resolve().parent.parent / "app" / "site"

VIEWPORTS = {"desktop": (1440, 1000), "tablet": (834, 1112), "mobile": (390, 844)}
MIN_TAP = 44          # WCAG 2.5.5 target size (CSS px)

PAGES = ["/", "/request-quote/", "/rates/force-urbania-rental-rates-hyderabad/",
         "/fleet/seater-17/", "/destinations/hyderabad-to-srisailam/", "/contact/"]

PROBE = """
() => {
  const de = document.documentElement;
  const vw = window.innerWidth, vh = window.innerHeight;
  const overflowX = de.scrollWidth - de.clientWidth;
  // WCAG: 2.5.8 (AA) requires 24px for pointer targets; 2.5.5 (AAA) wants 44px
  // for touch. A 24px desktop nav link is conformant; on touch it is not.
  const touch = window.matchMedia('(pointer: coarse)').matches || vw <= 900;
  const minTap = touch ? 44 : 24;

  // An element inside a horizontally scrollable ancestor is not a layout bug --
  // that is the intended pattern for wide tables and tab strips.
  const inScroller = el => {
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      const o = getComputedStyle(p).overflowX;
      if ((o === 'auto' || o === 'scroll' || o === 'hidden') && p.scrollWidth > p.clientWidth + 1) return true;
    }
    return false;
  };

  // Intentionally off-screen (screen-reader/bot honeypots) is not a bug.
  const hiddenOffscreen = el => {
    const r = el.getBoundingClientRect();
    if (r.left < -1000 || r.right > vw + 10000) {
      const cs = getComputedStyle(el);
      return cs.position === 'absolute' || cs.position === 'fixed';
    }
    return false;
  };

  const bleeders = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    const cs = getComputedStyle(el);
    if (cs.position === 'fixed' || cs.visibility === 'hidden' || cs.display === 'none') return;
    if (hiddenOffscreen(el)) return;
    if (inScroller(el)) return;
    if (r.right > vw + 1 || r.left < -1) {
      bleeders.push({tag: el.tagName.toLowerCase(), cls: (el.className||'').toString().slice(0,40),
                     left: Math.round(r.left), right: Math.round(r.right)});
    }
  });

  const bar = document.querySelector('.sticky');
  let sticky = null;
  if (bar) {
    const r = bar.getBoundingClientRect();
    const cs = getComputedStyle(bar);
    sticky = {visible: cs.display !== 'none', top: Math.round(r.top), bottom: Math.round(r.bottom),
              height: Math.round(r.height), vh: vh, onScreen: r.bottom <= vh + 1 && r.bottom > 0};
  }

  const small = [];
  document.querySelectorAll('.sticky a, .heroacts a, .jbar button, nav.main a, .uc').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (hiddenOffscreen(el)) return;
    if (r.height < minTap || r.width < minTap) {
      small.push({text: (el.textContent||'').trim().slice(0,24), w: Math.round(r.width), h: Math.round(r.height)});
    }
  });

  return {vw, vh, touch, minTap, overflowX, bleeders: bleeders.slice(0,6), sticky, small: small.slice(0,8)};
}
"""


def main():
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp_name, (w, h) in VIEWPORTS.items():
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            page = ctx.new_page()
            for path in PAGES:
                page.goto(BASE + path, wait_until="load", timeout=30000)
                page.wait_for_timeout(350)
                r = page.evaluate(PROBE)
                label = f"{vp_name:<8} {path}"

                if r["overflowX"] > 1:
                    failures.append(f"{label}: horizontal overflow {r['overflowX']}px")
                    print(f"  FAIL overflow   {label}  {r['overflowX']}px")
                if r["bleeders"]:
                    for b in r["bleeders"]:
                        failures.append(f"{label}: <{b['tag']}> bleeds to {b['right']}px (vw {r['vw']})")
                    print(f"  FAIL bleed      {label}  {r['bleeders']}")
                if r["sticky"] and r["sticky"]["visible"]:
                    s = r["sticky"]
                    if not s["onScreen"]:
                        failures.append(f"{label}: sticky bar off-screen (bottom {s['bottom']} vs vh {s['vh']})")
                        print(f"  FAIL sticky     {label}  {s}")
                    if s["height"] < 44:
                        failures.append(f"{label}: sticky bar only {s['height']}px tall")
                        print(f"  FAIL sticky-height {label} {s['height']}px")
                for t in r["small"]:
                    failures.append(f"{label}: tap target {t['text']!r} is {t['w']}x{t['h']} (<{MIN_TAP})")

                status = "ok" if not (r["overflowX"] > 1 or r["bleeders"]) else "issues"
                print(f"  {status:<8} {label}  overflow={r['overflowX']} "
                      f"sticky={(r['sticky'] or {}).get('height','n/a')}px small={len(r['small'])}")
            ctx.close()
        browser.close()

    print()
    if failures:
        print(f"{len(failures)} layout problem(s):")
        for f in failures[:25]:
            print("  -", f)
        return 1
    print("No layout problems found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
