# HOMEPAGE_WIREFRAME

Reflects the built page (2026-10-03), in order, top to bottom. Mobile (390 px) is the primary layout.

```
┌─────────────────────────────────────────────┐
│ HEADER  logo · nav (6) · [Call] [Quote CTA] │  sticky
├─────────────────────────────────────────────┤
│ HERO                                        │
│   eyebrow  "Group travel · Hyderabad"       │
│   H1       "Get your group there together." │
│   lede     "17-seat Force Urbania hire in   │
│             Hyderabad for groups of 10–17…" │
│   [Call]                                    │
│   small    "Quotation on request. Not live  │
│             availability, not instant."     │
├─────────────────────────────────────────────┤
│ PLANNER  ← dominant first-screen element    │
│   trip-type tabs (8, horizontally scroll)   │
│   active mode fields (progressive)          │
│   contact block                             │
│   [ Continue / mode-specific CTA ]          │
│   disclaimer: not a booking                 │
├─────────────────────────────────────────────┤
│ TRUST STRIP  6 short factual claims         │
├─────────────────────────────────────────────┤
│ TRIP TYPES   4 cards → airport / wedding /  │
│              corporate / sightseeing        │
├─────────────────────────────────────────────┤
│ HOW IT WORKS  4 steps                       │
├─────────────────────────────────────────────┤
│ THE VEHICLE   diagram + what is confirmed   │
│               today vs with the quotation   │
├─────────────────────────────────────────────┤
│ WHY ONE VEHICLE  3 cards                    │
├─────────────────────────────────────────────┤
│ GUIDES  3 cards                             │
├─────────────────────────────────────────────┤
│ FAQ  (accordion-free <details>)             │
├─────────────────────────────────────────────┤
│ CTA BAND                                    │
├─────────────────────────────────────────────┤
│ FOOTER  trip types · company · legal        │
├─────────────────────────────────────────────┤
│ STICKY (mobile) [Request a Trip Quote][Call]│
└─────────────────────────────────────────────┘
```

## Ordering rationale

The planner sits **above** the trip-type cards because the V3 brief makes the homepage
transaction-first: a visitor who already knows their trip should be able to start immediately.
The trip-type cards then serve the visitor who does not yet know what they need.

The "what is confirmed today vs with your quotation" block sits directly under the vehicle
section on purpose — it is where a sceptical buyer's question forms, and answering it there is
cheaper than letting them leave to ask it.

## Measured against the brief's 10-second test

At 390 px, above the fold: H1, the relevance line naming the vehicle and city, the phone number,
the availability caveat, and the planner's trip-type tabs (verified: tabs fully within the
viewport, planner beginning at 569 px of an 844 px screen).

## Deliberately absent

No hero image, no carousel, no autoplay video, no promotional banner, no cookie wall, no chat
widget, no social proof strip, no price table, no fleet grid.
