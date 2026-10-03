#!/usr/bin/env python3
"""
Screenshot the local Urbania preview at desktop / tablet / mobile.

Run with the playwright venv:
    ~/.hermes/cache/scratch/pw-venv/bin/python tools/shoot.py [--full]

Writes PNGs to .sshots/ (gitignored) and prints their paths.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8140"
OUT = pathlib.Path(__file__).resolve().parent.parent / ".sshots"

VIEWPORTS = {
    "desktop": dict(width=1440, height=1000),
    "tablet":  dict(width=834,  height=1112),
    "mobile":  dict(width=390,  height=844),
}

PAGES = {
    "home":          "/",
    "quote":         "/request-quote/",
    "rates":         "/rates/force-urbania-rental-rates-hyderabad/",
    "fleet":         "/fleet/seater-17/",
    "destination":   "/destinations/hyderabad-to-srisailam/",
    "contact":       "/contact/",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="full-page instead of viewport")
    ap.add_argument("--pages", default="home,quote", help="comma-separated page keys")
    ap.add_argument("--viewports", default="desktop,tablet,mobile")
    ap.add_argument("--prefix", default="")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    keys = [k.strip() for k in args.pages.split(",") if k.strip()]
    vps = [v.strip() for v in args.viewports.split(",") if v.strip()]

    written = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp_name in vps:
            vp = VIEWPORTS[vp_name]
            ctx = browser.new_context(viewport=vp, device_scale_factor=1)
            page = ctx.new_page()
            for key in keys:
                path = PAGES[key]
                page.goto(BASE + path, wait_until="load", timeout=30000)
                page.wait_for_timeout(700)          # let fonts/layout settle
                name = f"{args.prefix}{key}-{vp_name}.png"
                dest = OUT / name
                page.screenshot(path=str(dest), full_page=args.full)
                written.append(dest)
                print(f"{vp_name:<8} {key:<12} -> {dest}  ({dest.stat().st_size:,}B)")
            ctx.close()
        browser.close()

    print(f"\n{len(written)} screenshot(s) in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
