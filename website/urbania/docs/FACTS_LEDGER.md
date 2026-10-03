# FACTS LEDGER — Urbania group transport (Hyderabad)

Single source of truth. **Every agent and every page must use this ledger.**
Last updated: 2026-10-03

Rule: if a fact is not VERIFIED here, it does not appear as a settled statement on the website.

---

## VERIFIED — owner-supplied, safe to publish

| Fact | Value | Source |
|---|---|---|
| Vehicle | Force Urbania, 17 seats | Owner, project brief |
| Number of vehicles | One | Owner, project brief |
| Telephone (published for calls) | +91 62020 66104 | Owner, project brief |
| WhatsApp Business number | +91 91821 26104 | Owner, WhatsApp Business profile screenshot |
| Lead delivery channel | WhatsApp (one-tap from the quote form) | Owner direction |
| City | Hyderabad | Owner, project brief |
| Business model | Pre-booked private group transport / vehicle hire with driver | Owner, project brief |
| Conversion model | Quotation enquiry only — not instant booking | Owner, project brief |
| Positioning | "Private Group Travel & 17-Seater Force Urbania Hire in Hyderabad" | Owner, project brief |
| Not a tour operator | No packaged tours, guides, tickets, hotels | Owner, project brief |

## SAFE PUBLIC CLAIM — written so it cannot be wrong

| Claim as published | Why it is safe |
|---|---|
| "17-seat Force Urbania" | Directly supplied by the owner |
| "Availability is confirmed personally for each enquiry" | Describes the process, not a guarantee |
| "Submitting an enquiry does not confirm a booking" | True by design of the system built |
| "Quotation prepared from your itinerary" | Describes the model |
| "Transport service, not a packaged tour" | Directly supplied constraint |
| "Luggage capacity depends on passenger numbers — share both and suitability will be confirmed" | Avoids any unverified capacity claim |
| "Outstation travel depends on the permissions and operating arrangements that apply at the time" | Instructs enquirer to verify; states nothing unverified |

## SOURCED THIRD-PARTY DATA — published, with the source recorded

Distances and drive times are the ONLY figures on this site that come from outside
the business rather than from the owner. They were researched 2026-10-03 and
cross-checked across several independent distance sources. They are approximate by
nature — routed distance varies with the route taken and the time of day — and every
destination page says so explicitly.

Each figure carries its source in `ROUTE_DISTANCE_SOURCES` in `site_data.py`, and the
test suite **refuses to publish a distance with no entry there**. That is the
enforceable version of the original rule ("publish no unsourced number").

| Destination | km | Drive time | Sources | Confidence |
|---|---|---|---|---|
| Srisailam | 214 | 4h 45m | Yatra; Rajadrop Taxi (213–215 km) | High |
| Tirupati | 565 | 10h | Savaari; Uber Intercity (560–574 km) | Medium |
| Vijayawada | 273 | 4h 50m | Yatra; Savaari (272–275 km) | High |
| Warangal | 147 | 3h | Savaari; Uber Intercity (146–149 km) | High |
| Bangalore | 573 | 10h | Uber Intercity 571; Savaari 575 | Medium |
| Hampi | 377 | 8h | Hampi.in; Tusk Travel (375–380 km) | High |
| Goa (to Panaji) | 644 | 11h | Uber Intercity 629 → CoveringIndia 659; Savaari 644 | Medium |
| Ooty | 845 | 14h | Yatra 839; Holidify 847; Savaari 850 | Medium |

**Excluded as outliers** (recorded so they are not reintroduced): Tirupati 625 km · 
Vijayawada 305 km · Bangalore 610 km · Goa 721 km · Ooty 885 km.

**Goa caveat:** the figure is to Panaji. North and South Goa endpoints differ by well
over an hour, so the page states which one it means.

Do not tighten these into false precision. If a route is re-verified and the figure
changes, update both `ROUTES` and `ROUTE_DISTANCE_SOURCES` together.

## INDICATIVE PRICING — market-researched, labelled as indicative (Category B)

Publishing decision: launch with indicative market ranges rather than "request a quote"
alone, so a customer can budget before enquiring. This is authorised as Category B
(reversible commercial content) and is NOT presented as a contract rate anywhere.

**These are not UrbanLoop's own rates.** They are typical market ranges gathered
2026-10-03 from live Hyderabad-facing operator rate cards, with Delhi-priced cards
(urbaniahire.com, urbaniatemporental.com, urbaniavannonrent.com, tempotravller.com,
renttraveller.com) deliberately excluded. Every surface that shows them says they are
indicative and that the quotation confirms the figure for the actual trip.

| Item | Indicative range | Basis |
|---|---|---|
| Local / city | ₹30–40 /km | chikucabs 30-35; chikucab 38-40; 24cabservice 37-39; actempotravellerhire 34-40 |
| Outstation | ₹30–45 /km | rajputanacabs 32-40; actempotravellerhire 34-45; 24cabservice 35-39; chikucab 38-40 |
| Full day 8hr/80km | ₹6,800–10,000 | hyderabadwheels 6,825 incl. taxes; actempotravellerhire 8,000 → 10,000 by seating |
| Driver allowance | ₹500–800 /day | chikucab/chikucabs 500; rinocab 500; actempotravellerhire 600-700; mebus 800 |
| Airport transfer, one way | ₹4,000–4,500 | actempotravellerhire only — see caveat below |
| GST | 5% | standard contract-carriage rate |
| Minimum km/day, outstation | 250–300 km | genuine market split; both stated |
| Night allowance | ₹250–800 | varies by operator; stated as a range |

**Excluded as unreliable:** bhavanicabs.com local Urbania at ₹2,000–3,000/day — far
below every other source. **Outliers excluded** from the per-km bands: rinocab ₹25,
sara.cab ₹45.

**Weakest figure — airport transfer.** Only ONE Hyderabad van operator publishes a flat
rate (₹4,000–4,500). Every other operator quotes airport runs per km or as a package.
Route-specific van fares (RGIA→HITEC City vs Gachibowli vs Secunderabad) were not
published anywhere; only sedan/SUV figures exist (₹850–1,400). Treat as indicative and
verify with the owner before it is presented as a firm airport tariff.

**Owner action:** replace `RATE_INDICATIVE` in `site_data.py` with UrbanLoop's own rate
card. The rendering, the disclaimer and the test guard all follow the data — no code
change is needed.

The test suite enforces that a rupee figure may appear on a page **only** if it traces
to `RATE_INDICATIVE` or `CONFIGURATIONS`. An invented number still cannot reach a page.


## UNVERIFIED — must not be published as fact

Operating base address · permanent driver arrangement · driver vetting or experience · permit status ·
commercial insurance status · vehicle fitness/compliance · vehicle year and variant · final service area ·
minimum kilometres · overtime rate · night allowance · toll treatment ·
parking treatment · cancellation policy · payment terms · availability pattern · operating history in
Hyderabad · customer reviews · customer counts · exact luggage capacity · GST/invoicing status · photographs
of the vehicle · any special safety feature.

**Removed from this list:** pricing, rate per kilometre and driver allowance are no longer
unverified — they are published as INDICATIVE market ranges under Category B above, clearly
labelled and with their sources recorded. The distinction that matters is that they are
indicative, not that they are secret.

All of the above are handled by writing copy that **does not depend on them** (see SAFE PUBLIC CLAIM),
leaving an inline `<!-- [VERIFY BEFORE PUBLISHING: ...] -->` marker in the source where a decision is needed.

## OWNER DECISION REQUIRED — blocking publication

1. **Final business name.** RESOLVED — the site now uses the locked brand name `UrbanLoop`
   throughout (wordmark, header, footer, titles, schema). See `brand/urbanloop-design.md`.
2. **Domain name.** `BASE` in `build_ui.py` is a placeholder: `https://urbania-hyderabad.example`.
   This also means the `Sitemap:` line in robots.txt and every canonical URL currently point at a
   non-existent domain.
3. **Lead delivery address.** `LEAD_EMAIL` in `build_pages.py`, and whether to use a hosted form
   endpoint (`FORM_ENDPOINT`) instead of the current mailto fallback.
4. **WhatsApp availability.** `WHATSAPP` in `build_ui.py` is empty, so the WhatsApp button is
   suppressed rather than shipping a dead link.

## DO NOT PUBLISH YET — see DO_NOT_PUBLISH_UNTIL_VERIFIED.md

Everything listed in that checklist. It is the gate between "built" and "launch ready".

## OPEN CONFLICTS — raised, not silently resolved

**C1 — Two different phone numbers are in play.** The brief gives **+91 62020 66104** as the number to
publish. The WhatsApp Business profile screenshot shows **+91 91821 26104** under Contact information.
Both are now wired in their respective roles (call link vs WhatsApp link), but this may be the wrong
split and it needs one answer: **which number should customers call, and which should they message?**

**C2 — The WhatsApp Business profile location reads "Supaul, Bihar", not Hyderabad.** This website
targets Hyderabad. For customer trust this matters: a Hyderabad customer opening a WhatsApp chat with a
profile that says Supaul, Bihar may reasonably hesitate. It also matters for Google Business Profile,
where the service-area configuration must reflect where the business genuinely operates. **Resolve
before GBP setup.**

**C3 — The WhatsApp Business profile has no business email and no website set.** Both should be filled in
once the domain is chosen, so the profile and the site corroborate each other.
