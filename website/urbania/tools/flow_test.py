#!/usr/bin/env python3
"""
End-to-end quote-flow test in a real browser.

Covers the two-step funnel the brief specifies:
  step 1  home hero journey bar (trip details only)  ->  hand off
  step 2  /request-quote/ planner (prefilled)        ->  contact + submit

    ~/.hermes/cache/scratch/pw-venv/bin/python tools/flow_test.py

Exits non-zero on failure. Takes screenshots of each step into .sshots/.
"""
import argparse
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8140"
OUT = pathlib.Path(__file__).resolve().parent.parent / ".sshots"

TRIP = {"from": "Banjara Hills", "to": "Ramoji Film City",
        "date": "2026-11-14", "pax": "14"}


def fail(msg):
    print(f"  FAIL  {msg}")
    return False


def main():
    global BASE
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=BASE, help="site root (default local preview)")
    ap.add_argument("--prefix", default="", help="screenshot filename prefix")
    args = ap.parse_args()
    BASE = args.base.rstrip("/")
    print(f"base: {BASE}\n")

    OUT.mkdir(exist_ok=True)
    ok = True

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 1000})
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))

        # ---- STEP 1: hero journey bar, trip details only -------------------
        print("STEP 1  hero journey bar")
        page.goto(BASE + "/", wait_until="load")
        page.wait_for_timeout(400)
        bar = page.locator("form.jbar")
        for name, value in TRIP.items():
            bar.locator(f'input[name="{name}"]').fill(value)
        page.screenshot(path=str(OUT / "flow-1-hero-filled.png"))

        bar.locator('button[type="submit"]').click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(600)
        print(f"  -> navigated to {page.url}")

        if "/request-quote/" not in page.url:
            ok = fail(f"journey bar did not hand off (url={page.url})")
        for name, value in TRIP.items():
            if f"{name}=" not in page.url:
                ok = fail(f"handoff dropped '{name}' from the query string")

        # ---- STEP 2: planner, prefilled ------------------------------------
        print("STEP 2  planner prefill + submit")
        page.screenshot(path=str(OUT / "flow-2-planner.png"))

        prefill = page.evaluate("""() => {
            const on = document.querySelector('.pl-mode.on') || document;
            const q = new URLSearchParams(location.search);
            const names = {from:['pickup','main_pickup','address'],
                           to:['destination','destinations','venue','itinerary'],
                           date:['date','date_from','return_date'],
                           pax:['passengers','guests','team_size']};
            const out = {};
            for (const k in names) {
              out[k] = null;
              for (const n of names[k]) {
                const el = on.querySelector('[name="'+n+'"]');
                if (el) { out[k] = el.value; break; }
              }
            }
            return {expected: Object.fromEntries(q), got: out};
        }""")
        print(f"  prefill: {prefill}")
        if not prefill["got"].get("from"):
            ok = fail("pickup was not prefilled from the journey bar handoff")
        if prefill["got"].get("pax") != TRIP["pax"]:
            ok = fail(f"passengers not prefilled (got {prefill['got'].get('pax')!r})")

        # fill anything still empty inside the active mode
        filled = page.evaluate("""() => {
            const on = document.querySelector('.pl-mode.on');
            let n = 0;
            on.querySelectorAll('input,select,textarea').forEach(el => {
              if (el.type === 'radio' || el.type === 'checkbox') {
                if (!el.checked) { el.checked = true; n++; }
                return;
              }
              if (!el.value) {
                el.value = el.type === 'date' ? '2026-11-14'
                        : el.type === 'number' ? '4'
                        : el.tagName === 'SELECT' ? (el.options[1] ? el.options[1].value : '')
                        : 'Banjara Hills';
                n++;
              }
            });
            return n;
        }""")
        print(f"  auto-filled {filled} remaining mode field(s)")

        # Contact details sit after the trip fields and before the review step,
        # so they must be filled before Continue (validate() covers them).
        page.locator('.pl-contact input[name="contact_name"]').fill("Flow Test")
        page.locator('.pl-contact input[name="contact_phone"]').fill("9812345678")
        page.locator('.pl-contact input[name="contact_email"]').fill("flow@example.com")
        page.locator('.pl-contact input[name="consent"]').check()

        # honeypot must stay empty for a human submission
        hp = page.locator('input[name="_hp"]')
        if hp.count() and hp.first.input_value():
            ok = fail("honeypot unexpectedly populated")

        # advance to the summary
        page.locator("#pl-next").click()
        page.wait_for_timeout(500)
        summary_visible = page.locator("#pl-summary.on").count() > 0
        print(f"  summary shown: {summary_visible}")
        if not summary_visible:
            ok = fail("Continue did not reveal the summary step")
        page.screenshot(path=str(OUT / "flow-3-summary.png"))

        page.locator("#pl-send").click()
        page.wait_for_timeout(2500)
        # scrollIntoView on the result uses behaviour:'smooth'; wait for it to
        # settle and pin the viewport so the screenshot shows the confirmation.
        page.evaluate("() => { const r = document.querySelector('#pl-result');"
                      " if (r) r.scrollIntoView({block:'center', behavior:'auto'}); }")
        page.wait_for_timeout(600)
        page.screenshot(path=str(OUT / "flow-4-result.png"))

        result = page.locator("#pl-result").inner_text()
        m = re.search(r"(GT[0-9A-F]{6})", result)
        print(f"  result text: {result.strip()[:120]!r}")

        # VISIBILITY, not just presence. inner_text() happily returns the text of
        # a hidden element, which is why an earlier version of this test passed
        # while the customer saw the form vanish with no confirmation at all.
        vis = page.evaluate("""() => {
            const r = document.getElementById('pl-result');
            const cs = getComputedStyle(r);
            const b = r.getBoundingClientRect();
            return {visible: cs.display!=='none' && cs.visibility!=='hidden' && b.height>0,
                    height: Math.round(b.height),
                    insideHiddenForm: (() => { const f=document.getElementById('plform');
                        return !!f && f.contains(r) && getComputedStyle(f).display==='none'; })()};
        }""")
        print(f"  confirmation visible to customer: {vis}")
        if not vis["visible"]:
            ok = fail("the confirmation is not visible — the customer sees no acknowledgement")
        if vis["insideHiddenForm"]:
            ok = fail("the confirmation sits inside the form that gets hidden on success")

        if not m:
            ok = fail(f"no reference issued; result={result.strip()[:200]!r}")
        elif m.group(1) == "GT000000":
            ok = fail("honeypot path taken on a genuine submission")
        else:
            print(f"  OK    real reference issued: {m.group(1)}")

        if errors:
            ok = fail(f"console errors: {errors[:3]}")
        else:
            print("  OK    no console errors")

        ctx.close()
        browser.close()

    print()
    print("QUOTE FLOW PASSED" if ok else "QUOTE FLOW FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
