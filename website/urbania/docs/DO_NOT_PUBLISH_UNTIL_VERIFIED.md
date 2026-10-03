# DO NOT PUBLISH UNTIL VERIFIED

Owner checklist. This page is the gate between "built" and "launch ready".
Last updated: 2026-10-03

Tick each item only when the fact is genuinely confirmed. Nothing below is currently confirmed.

## Legal / regulatory
- [ ] PERMIT — permit type and validity, and whether it covers every trip type quoted
- [ ] INSURANCE — commercial passenger insurance, cover level, and what it does and does not cover
- [ ] FITNESS / COMMERCIAL COMPLIANCE — fitness certificate and any other statutory document current
- [ ] INTERSTATE / OUTSTATION permission — whether outstation trips may legally be offered at all
- [ ] GST — registration status and whether tax invoices can be issued

## Operations
- [ ] DRIVER ARRANGEMENT — employed, contracted, or per-trip
- [ ] DRIVER CLAIMS — any statement about experience or vetting (nothing may be claimed until verified)
- [ ] ACTUAL OPERATING BASE — where the vehicle is kept
- [ ] SERVICE AREA — the areas genuinely served
- [ ] AVAILABILITY — realistic pattern; do not imply 24/7
- [ ] LUGGAGE CAPABILITY — measured, with representative luggage

## Commercial
- [ ] PRICING MODEL — per km, per day, or fixed
- [ ] RATE PER KILOMETRE
- [ ] MINIMUM KILOMETRES
- [ ] OVERTIME RULES
- [ ] NIGHT ALLOWANCE
- [ ] TOLL RULES — included or additional
- [ ] PARKING RULES
- [ ] PAYMENT TERMS
- [ ] CANCELLATION TERMS

## Identity and assets
- [ ] BUSINESS NAME — final name confirmed and applied everywhere
- [ ] DOMAIN — registered, and `BASE` in `build_ui.py` updated
- [ ] ENQUIRY EMAIL — a monitored address (a business address is preferable to a personal one)
- [ ] WHATSAPP — number confirmed, or the button left hidden
- [ ] VEHICLE PHOTOGRAPHS — the shot list below completed and substituted for the illustrative diagram
- [ ] LOGO — if a real logo exists, replace the placeholder mark

## Vehicle photograph shot list
- [ ] Front three-quarter exterior
- [ ] Rear three-quarter exterior
- [ ] Side profile
- [ ] Passenger door open
- [ ] Front cabin
- [ ] Passenger cabin, front view
- [ ] Passenger cabin, rear view
- [ ] Seat rows
- [ ] Aisle
- [ ] Luggage area (empty)
- [ ] Luggage area with representative luggage (this answers the most common customer question)
- [ ] Dashboard / interior detail
- [ ] Vehicle at a neutral, real location
- [ ] Night interior (optional)

When real images arrive: compress, generate responsive sizes, convert to WebP/AVIF, use meaningful
filenames, write accurate alt text, and strip unnecessary metadata.

## Gates before announcing the site
- [ ] Every `[VERIFY BEFORE PUBLISHING]` marker in the source resolved or deliberately accepted
      (currently **11** markers in the built HTML)
- [ ] `robots.txt` `Sitemap:` line points at the real domain
- [ ] Canonical URLs resolve to the real domain
- [ ] Form delivery tested end to end from a real phone
- [ ] Phone number tested by tapping the link on a real phone
