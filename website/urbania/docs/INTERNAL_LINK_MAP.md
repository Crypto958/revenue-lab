# INTERNAL_LINK_MAP.md

Derived from the built HTML on 2026-10-03. Every internal `href` counted; assets excluded.

## Inbound links per page

| Page | Inbound | Outbound | Sample outbound |
|---|---:|---:|---|
| `/` | 21 | 21 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/about/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/airport-group-transfer-hyderabad/` | 21 | 19 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/contact/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/corporate-group-transport-hyderabad/` | 21 | 19 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/family-group-travel-hyderabad/` | 21 | 19 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/find-a-vehicle/` | 21 | 20 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/force-urbania-hire-hyderabad/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/guides/` | 21 | 21 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/guides/force-urbania-vs-tempo-traveller/` | 6 | 20 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/guides/group-vehicle-fit-guide/` | 10 | 20 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/guides/wedding-guest-transport-planning/` | 4 | 20 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/how-it-works/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/hyderabad-sightseeing-group-travel/` | 21 | 19 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/outstation-group-travel-hyderabad/` | 21 | 19 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/partner-with-us/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/privacy/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/request-quote/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/terms/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/wedding-transport-hyderabad/` | 21 | 19 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |
| `/what-to-expect/` | 21 | 18 | `/`, `/about/`, `/airport-group-transfer-hyderabad/`, `/contact/`, `/corporate-group-transport-hyderabad/`, `/family-group-travel-hyderabad/` … |

## Findings

- **Orphan pages: none.** Every page is reachable from at least one other page.
- **Weakly linked pages (< 5 inbound):** `/guides/wedding-guest-transport-planning/` (4).
  Guide pages sit lowest by design — they are discovered from their hub, the footer and the
  service pages that reference them, not from the main navigation.
- **Navigation** carries the six highest-commercial-intent pages. Everything else is reachable
  from the footer, which appears on all pages.

## Anchor-text rule applied

Anchors are descriptive and vary naturally (`Outstation group travel`, `Force Urbania hire in
Hyderabad`, `What vehicle fits a group of 10–17?`). No "click here", no bare URLs, and no
repeated identical anchor text pointing at different pages.

## Hub-and-spoke shape

- **Hub:** `/` (links out to every commercial page and the planner).
- **Spokes:** the eight trip-type pages, each linking to one relevant guide and back to the planner.
- **Guides:** informational ring, each linking to two related pages, keeping the informational
  cluster from competing with the commercial pages for the same queries.
