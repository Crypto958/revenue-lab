# MOBILE_FLOW

The 390 px journey, measured rather than described. Primary design target per the V3 brief.

## Entry paths

A visitor arrives from one of three places, and the planner is **preselected** for each so the
first thing they see matches why they came:

| Landing page | Planner opens on |
|---|---|
| `/airport-group-transfer-hyderabad/` | Airport |
| `/wedding-transport-hyderabad/` | Wedding / Event |
| `/outstation-group-travel-hyderabad/` | Outstation (date-range controls visible) |
| `/corporate-group-transport-hyderabad/` | Corporate |
| `/hyderabad-sightseeing-group-travel/` | Sightseeing / Day Trip |
| `/family-group-travel-hyderabad/` | Family Trip |
| `/force-urbania-hire-hyderabad/` | Local (vehicle preference offered) |
| `/find-a-vehicle/` | Custom |

All eight verified in the built HTML.

## The step sequence

```
Trip type  →  Route  →  Dates  →  Group / Luggage  →  Vehicle preference
           →  Contact  →  Trip summary (+ Edit)  →  Request  →  Reference
```

Each mode collapses this into the fields it actually needs. Nothing irrelevant is shown, so the
form never looks long even though the system covers eight trip types.

## Measured mobile behaviour

| Check | Result |
|---|---|
| Horizontal overflow at 375 / 390 px | None |
| Planner start position (390 × 844) | 569 px — trip-type tabs fully on screen |
| Trip-type tab height | 44 px (meets the touch-target minimum) |
| Input height | 46 px (exceeds it) |
| Mobile navigation | Hamburger, keyboard-operable, `aria-expanded` toggled |
| Sticky bottom bar | Present: **Request a Trip Quote** + **Call now** |
| Reduced motion | `prefers-reduced-motion` disables transitions and animation |
| JavaScript disabled | `<noscript>` panel gives the phone number and lists what to send |
| Focus visibility | `:focus-visible` outline on every interactive element |

## Error and edge states handled

- **Validation failure** — the offending field is flagged, focused and scrolled into view;
  the summary does not open, so nothing is lost.
- **API unreachable** — WhatsApp opens with the payload, and the confirmation panel says
  explicitly that the system could not be reached so the customer should send it there too.
- **No JavaScript** — phone and email route with the information needed to quote.
- **Long tab strip** — the trip-type row scrolls horizontally with the scrollbar hidden, so all
  eight modes remain reachable without wrapping into a wall of chips.

## Small-screen typography and spacing

Hero padding tightens to 24 px, the H1 drops to 30 px, and section padding reduces at ≤560 px,
so the planner is reached sooner. Nothing is hidden at small sizes — it is only tightened.

## Known weakness

There is **no progress indicator** across the planner steps, and eight tabs in a scroll strip is
a long first interaction. Both are recorded as the next UI iteration in `QA_REPORT.md`.
