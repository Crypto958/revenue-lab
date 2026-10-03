#!/usr/bin/env python3
"""
Urbania Hyderabad — IMPROVEMENT PLAN
Derived from the five reference sites in the owner's brief.

Rule for this whole programme: references were used for STRUCTURE, PATTERNS and
INFORMATION ARCHITECTURE only. No copy, logo, image, review or claim was taken
from any reference site. All content here is original.

=============================================================================
WHAT THE REFERENCES ACTUALLY SHOW (evidence, not impression)
=============================================================================

The single most useful finding: almost nobody publishes prices.
  - simplytrip.in ......... zero prices on the homepage; rates only on deep
                            city pages, as a Seater | per km | daily | best-for table
  - saiforceurbaniarentinhyd ... ZERO prices anywhere: no per-km, no package,
                            no inclusions table
  - globalbusrental.com ... zero pricing signals at all
  - osabus.com ............ no price per vehicle
  - urbaniahire.com ....... THE ONLY ONE publishing rate tables:
                            per-km, per-day, driver charge/day, min km/day,
                            GST, toll/state-tax inclusions

Why that matters for us: a generic catalogue (tempo traveller + mini bus + bus
+ car, many cities) cannot quote honestly because the price depends on which
vehicle and partner. A single-model specialist CAN publish honest indicative
rates. Transparent pricing is therefore our clearest differentiator, not a
"nice to have".

Second finding: the winning conversion shape is a TWO-STEP progressive funnel.
  Step 1 — trip intent ONLY, zero personal data:
           From -> To -> Travel date -> Passengers -> [Get a quote]
  Step 2 — contact + refinement, shown WITH a summary and an "Edit" escape:
           Name, Phone/WhatsApp, Pickup time, Trip type, Notes, Consent
Global Bus Rental calls step 1 a "journey bar": one white card floating over the
hero, reading as a single object so the perceived cost of starting is near zero.
Name and phone appear only at step 2, after trip details are already committed.

Third finding: trust belongs INSIDE the hero. Global Bus Rental puts aggregate
scores + review counts directly under the quote form, above the fold — trust at
the exact moment of conversion, not on a separate page.

Weaknesses we can beat (all five references):
  - no or hidden pricing
  - unverifiable trust ("hundreds of happy customers", no counter, no link)
  - seat capacity stated only in prose; no seat map, layout or luggage figure
  - the worst offender captures contact details FIRST and never asks route,
    dates or passenger count at all
  - no WhatsApp option on some, against Indian mobile-first norms
  - generic multi-vehicle positioning that cannot own a niche

=============================================================================
PLAN — ordered by the owner's stated priorities
=============================================================================

P1  CONVERSION
    - Two-step funnel matching the reference shape: trip details first (no PII),
      then contact with a summary + Edit.                 [DONE - planner already
      does mode->details->contact->summary; reorder to summary-before-contact]
    - Hero carries the keyword headline "Force Urbania Rental in Hyderabad",
      with the quote entry above the fold (currently the H1 is poetic and the
      planner sits below the fold).
    - ONE primary CTA label repeated with one accent colour, ending in a
      full-width closing band.                              [partly present]

P2  MOBILE
    - Persistent CALL | WHATSAPP | GET QUOTE bar.           [DONE - 3-up sticky]
    - 16px inputs to stop iOS zoom; safe-area insets.       [DONE]

P3  PREMIUM VISUAL QUALITY
    - The vehicle is the hero. Requires REAL PHOTOGRAPHY — still the top blocker.
      Build the gallery + image-slot architecture so photos drop in by filename.
    - Generous whitespace, modern cards, restrained animation.

P4  TRUST
    - Trust strip with EXPLICIT placeholder fields (Google rating, review count,
      trips completed, years operating, vehicles, drivers, 24/7).
      Nothing renders as a number until the owner supplies it. A placeholder is
      rendered as a visible "To be confirmed", never as a fabricated figure.
    - Reviews section built for genuine Google reviews; empty-state by default.

P5  QUOTE ENQUIRIES
    - Pre-filled WhatsApp fallback on the mobile bar and every failure path.

P6  CLEAR URBANIA CONFIGURATIONS
    - "Find Your Urbania": passenger-count selector (9..17) -> recommends a
      configuration. Rules live in editable data, not in templates.

P7  TRANSPARENT PRICING ARCHITECTURE
    - Rates page using urbaniahire.com's STRUCTURE (their Delhi figures are NOT
      reused): config | per-km | per-day | driver allowance | min km/day |
      toll | parking | state tax/permit | GST | inclusions | exclusions.
    - Every figure is an editable placeholder rendered as a visible to-be-confirmed
      token, never an invented number.

P8  LOCAL HYDERABAD RELEVANCE + P9 SEO ARCHITECTURE
    - Service cards and route/destination pages under /services/, /destinations/,
      /fleet/, /rates/. Built as real content, not thin doorway pages.

P10 ACCESSIBILITY / P11 PERFORMANCE
    - Skip link, landmarks, focus-visible, aria on tabs and live regions. [DONE]
    - Static HTML, no framework, no render-blocking JS. Caching headers. [DONE]

=============================================================================
OPEN DECISION BLOCKING P6/P7 (raised, not silently resolved)
=============================================================================

The brief lists four configurations (17 / 16 / 12-13 premium / 9-10 Maharaja).
The live FACTS_LEDGER and the current site say ONE 17-seat vehicle, and the site
tells customers: "there is a single vehicle — that is why availability is
confirmed per enquiry".

These cannot both be published. Until the owner confirms which vehicles actually
exist, the configuration and rate sections render in a CONFIRMED-FALSE state:
the architecture, layout and guidance are all live and indexable, but the specs
and rates show as to-be-confirmed rather than asserting a fleet that may not
exist. One flag flips it:

    site_data.FLEET_CONFIRMED = True   (after owner confirmation)

That keeps the site honest by construction instead of relying on someone
remembering to remove placeholder text later.
"""
