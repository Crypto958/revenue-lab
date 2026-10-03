#!/usr/bin/env python3
"""Writes the project documentation set. Run: python3 write_docs.py"""
import os, datetime
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
os.makedirs(D, exist_ok=True)
T = datetime.date.today().isoformat()

DOCS = {}

DOCS["FACTS_LEDGER.md"] = f"""# FACTS LEDGER — Urbania group transport (Hyderabad)

Single source of truth. **Every agent and every page must use this ledger.**
Last updated: {T}

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

## UNVERIFIED — must not be published as fact

Operating base address · permanent driver arrangement · driver vetting or experience · permit status ·
commercial insurance status · vehicle fitness/compliance · vehicle year and variant · final service area ·
pricing · rate per kilometre · minimum kilometres · overtime rate · night allowance · toll treatment ·
parking treatment · cancellation policy · payment terms · availability pattern · operating history in
Hyderabad · customer reviews · customer counts · exact luggage capacity · GST/invoicing status · photographs
of the vehicle · any special safety feature.

All of the above are handled by writing copy that **does not depend on them** (see SAFE PUBLIC CLAIM),
leaving an inline `<!-- [VERIFY BEFORE PUBLISHING: ...] -->` marker in the source where a decision is needed.

## OWNER DECISION REQUIRED — blocking publication

1. **Final business name.** The site currently uses the working name `Urbania Hyderabad`.
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
"""

DOCS["OWNER_DECISIONS.md"] = f"""# OWNER DECISIONS

Items only the owner can decide. None of these block the build; each blocks publication.
Last updated: {T}

## Blocking publication

| # | Decision | Current state | Why it matters |
|---|---|---|---|
| 1 | Final business name | Working name `Urbania Hyderabad` in use | Appears in the logo, footer, titles and schema |
| 2 | Domain name | Placeholder `https://urbania-hyderabad.example` | Canonicals, sitemap and robots all point at it |
| 3 | Lead delivery — **now via WhatsApp** (owner direction) | Form sends the full trip details to WhatsApp in one tap; verified in-browser. Email is no longer the primary path | WhatsApp must be actively monitored |
| 4 | WhatsApp number | Two numbers in play: +91 62020 66104 (brief, now the call link) and +91 91821 26104 (profile, now the WhatsApp link) | Confirm which is which |
| 4a | WhatsApp Business profile location shows **Supaul, Bihar** | Unresolved — potential trust and GBP issue | Site targets Hyderabad |
| 4b | WhatsApp profile has no business email or website set | Unresolved | Fill once the domain is chosen |
| 5 | Public call number confirmation | +91 62020 66104 published as given | Confirm it is the number to publish |

## Commercial rules to confirm

| # | Decision | Why it matters |
|---|---|---|
| 6 | Pricing model — per km, per day, minimum km, overtime, night allowance | Must be quotable consistently |
| 7 | Toll and parking treatment (included or extra) | A common source of dispute |
| 8 | Driver allowance and outstation terms | Should reflect what is actually paid |
| 9 | Payment terms (advance % / on completion) | Needed before quoting |
| 10 | Cancellation policy | Published nowhere yet by design |
| 11 | GST registration and whether tax invoices can be issued | Corporate enquiries ask; cannot claim until confirmed |

## Operational facts to confirm

| # | Decision | Why it matters |
|---|---|---|
| 12 | Permit status, insurance status, fitness/compliance | Cannot be published unverified |
| 13 | Permanent driver arrangement | Cannot claim driver quality |
| 14 | Confirmed service area and operating base | "Based in Hyderabad" is deliberately not claimed |
| 15 | Vehicle year, model variant, seating layout | Buyers ask |
| 16 | Luggage capacity in practice | The single most common group-travel question |
| 17 | Whether outstation trips are possible at all | Currently answered as "depends — we will confirm" |
| 18 | Photographs of the vehicle | See the shot list in VISUAL_CONTENT_SPEC |

## Deliberately NOT asked (decided by the manager)

- Structure, page set, URL slugs — reversible, decided and implemented.
- Whether to publish prices — decided: no, quote-based. Change only if the owner supplies a fixed rate card.
- Whether to allow AI crawlers — decided: allow answer engines, disallow training-only crawlers
  (`GPTBot`, `CCBot`, `ClaudeBot`). Easily reversed in `robots.txt`.
- Whether to show a fleet, filters, or an availability calendar — decided: no. One vehicle.
"""

DOCS["TEMPLATE_DECISION.md"] = f"""# TEMPLATE DECISION

Date: {T} · Decision owner: Central Manager

## Decision

**Build on an original lightweight static implementation** — hand-written semantic HTML, one CSS file,
and roughly 60 lines of vanilla JavaScript for the mobile menu and the quote-form validation.
No JavaScript framework, no build toolchain, no runtime dependencies, no database.

Framework output is generated by three Python files so content is data, not markup.

## Why this was chosen over a template

The brief required scoring candidates 1–10 on sixteen criteria, with explicit penalties for anything built
around login, fleet inventory, search filters, availability calendars, ecommerce, self-drive rental or
databases. Every credible template in the transport/rental category carries at least one of those, because
they are built for fleets and marketplaces rather than for one vehicle and a quotation.

Weighted against the criteria that actually decide this project:

| Criterion | Template (typical best-in-class) | This implementation |
|---|---|---|
| Suitability for a ONE-vehicle business | Must strip fleet UI | Native — there is no fleet concept |
| Suitability for quote-first conversion | Usually booking-first; needs rework | Native — one CTA, one form |
| Dependency weight | Tailwind build chain or a JS framework | Zero dependencies |
| Page speed potential | 70–95 depending on runtime JS | Static HTML + one CSS file |
| Ease of modification | Component system to learn | Three Python files, content as data |
| Licence suitability | Varies; several require attribution | Original work, unencumbered |
| Accessibility | Varies widely | Landmarks, labels, focus states, reduced-motion |

## What was kept from the template study

- The **service-page pattern** (one clear intent per page, FAQ near the bottom, repeated CTA).
- A **sticky mobile call-to-action bar** carrying both Quote and Call.
- A **filterable portfolio of systems** is deliberately NOT used here — it belongs to the other project;
  a transport site needs four service pages and a quote form, not a filterable grid.
- **Breadcrumbs** on all inner pages.
- **HTML `<details>` FAQs** rather than a JavaScript accordion, so they work without JS.

## What was explicitly rejected

Fleet listing grids · vehicle filters · self-drive daily pricing · sign-in/sign-up · checkout ·
payment gateway · availability calendar · customer dashboard · manufacturer catalogues ·
placeholder testimonial sections · fake counters · template blog filler.

These were removed rather than restyled, because leaving them would have made the site look like
"a car-rental template with different text" — the specific failure the brief warned against.

## Correction: the claim that an original build "scores higher" was wrong

The independent template scout verified 14 candidates and scored them on the required 16 criteria. Its
result contradicts the reasoning above, and the correction is recorded here rather than quietly dropped:

| Base | Score |
|---|---|
| Small Business Starter (free) — Astro 6 + Tailwind v4, MIT | 137 / 150 |
| Small Business Starter v2 — Astro 7 + Tailwind v4, MIT | 133 / 150 |
| AstroWind — Astro + Tailwind, MIT | 121 / 150 |
| **This original implementation** | **137 / 150 (tie)** — best case with further design work, ~143 / 150 |

The scout's verdict was explicit: for a solo operator, an original hand-written build **does not
out-score** the best template. It is a **tie**, and the template wins on criteria this build is weakest
on — visual credibility, image/gallery handling, SEO architecture and especially article/blog support
(scored 5–6 here against 8 there).

**Decision, and why it stands anyway.** The two options tie on the scorecard, so the scorecard stops
being the decider and the tie-break governs. This implementation is **already built, validated and
live**: 15 pages, 0 build errors, 0 broken internal links, 20/20 routes returning 200, form validation
verified in a real browser at 375px. Adopting the template now means rebuilding all fifteen pages to
reach roughly the same score. Against that, the genuine costs of staying are acknowledged: **no blog
infrastructure and weaker gallery handling**, both of which the template provides and neither of which
this business needs at one vehicle and zero published trips.

**When the decision should be reversed.** If the owner commits to regular article publishing or an
image-heavy vehicle gallery, adopt Small Business Starter (MIT) and migrate — the content already lives
as data in `build_pages.py`, so the copy transfers. That is the honest trigger condition, not a
preference for hand-built code.

**Note on the research workstreams.** `TEMPLATE_SHORTLIST.md` (Agent B) holds the full per-criterion
scores; `SEARCH_INTELLIGENCE.md`, `KEYWORD_MAP.csv`, `COMPETITOR_NOTES.md` and `CONTENT_GAPS.md`
(Agent A) hold the market research. Where Agent A's official-source findings contradicted this project's
assumptions, the findings won and the documents were corrected — see `SEO_STRATEGY.md`.
"""

DOCS["SEO_STRATEGY.md"] = f"""# SEO / AEO STRATEGY

Date: {T}

## Principle

The site does not try to rank for "vehicle rental Hyderabad". It is built to intercept a narrower,
higher-intent moment: **a person who already knows they have a group of roughly 10–17 people to move.**
Every page serves that funnel.

## Page-to-intent map

| Page | Primary intent | Primary term |
|---|---|---|
| `/` | Commercial + local | 17 seater Force Urbania hire Hyderabad |
| `/airport-group-transfer-hyderabad/` | High commercial + local | group airport transfer Hyderabad |
| `/wedding-event-transport-hyderabad/` | High commercial + local | wedding guest transport Hyderabad |
| `/corporate-group-transport-hyderabad/` | High commercial | corporate group transport Hyderabad |
| `/hyderabad-sightseeing-group-travel/` | Commercial + local | sightseeing vehicle hire Hyderabad / day hire |
| `/request-quote/` | Transactional | group vehicle quotation Hyderabad |
| `/guides/force-urbania-vs-tempo-traveller/` | Comparison / informational | Force Urbania vs Tempo Traveller |
| `/guides/group-vehicle-fit-guide/` | Informational | what vehicle for 15 people / 17 seater with luggage |
| `/guides/wedding-guest-transport-planning/` | Informational | planning wedding guest transport |

Exact query volumes are **not** stated because no keyword-volume tool is available on this host.
Intent classes are judgements, not measured data — see `KEYWORD_MAP.csv`.

## Cannibalisation control

Each commercial page owns a distinct trip type. No two pages target the same query. The three guides
target informational queries only and each links to exactly one commercial page, so they support the
funnel rather than competing with it.

No location pages were created. The brief's instruction not to generate
`/urbania-rental-madhapur/`-style programmatic pages is honoured: there is not yet unique local
content to justify them, and thin duplicates would harm the site.

## On-page specification (applied to every indexable page)

Unique title · unique meta description · exactly one H1 · question-shaped H2s where natural ·
answer-first opening paragraph · FAQ block with `<details>` · breadcrumb · canonical · Open Graph ·
internal links with descriptive anchor text · one clear CTA repeated.

## Structured data — deliberate choices

Included: `Organization`, `WebSite`, `Service`, `BreadcrumbList`, `FAQPage`.

**Deliberately excluded, and why — now backed by official documentation rather than judgement:**
- `LocalBusiness` / `AutomotiveBusiness` — **Google Search Central's Local business structured data page
  (last updated 2026-09-08) lists `address` (PostalAddress, "the physical location of the business") and
  `name` as REQUIRED properties**, with no documented service-area exception. This business has no
  verified address and must not invent one or use a virtual office, so it cannot satisfy the documented
  requirement. Omission is therefore correct, not merely cautious. Revisit only if a genuine premises or
  confirmed service-area situation is established and re-checked against current guidance.
- `AggregateRating` / `Review` — there are no reviews. Fabricating them is prohibited. Note also that
  Google's Local business page states `aggregateRating`/`review` is "only recommended for sites that
  capture reviews about other local businesses", so it is doubly inapplicable here.
- `priceRange`, `openingHours`, `geo` — none verified.
- `Offer` with a real price — pricing is quote-based and unconfirmed. The `Offer` currently carries only
  a textual note that a quotation is provided on request.

**Correction applied after research (2026-10-03):** `FAQPage` is retained because it is a valid
schema.org type, accurately describes visible content, and is parsed by systems other than Google — but
**the earlier justification that it would earn FAQ rich results is wrong and is withdrawn.** Google
deprecated the FAQ rich result: the entry "Deprecating the FAQ rich result feature" states it would no
longer appear in Search from 7 May 2026, and documentation was removed on 15 June 2026
(`https://developers.google.com/search/updates`). FAQ blocks remain on the pages because they genuinely
help readers, not because of any rich-result expectation.

All JSON-LD is validated in the build (`0` parse errors) and reflects only visible content.

## AI answer-engine (AEO) posture

- `robots.txt` **allows** `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Google-Extended`, `Googlebot`
  and `Bingbot`, so the site can be crawled and cited in answers.
- Training-only crawlers (`GPTBot`, `CCBot`, `ClaudeBot`) are **disallowed**. This is a reversible
  policy choice: being cited as an answer source does not require allowing model training. Both policies
  are kept separate so the owner can change one without the other.
- `/llms.txt` provides a plain-language fact sheet stating what the business does, the vehicle, the
  quoting model, what the customer must provide, and an explicit statement that outstation and other
  unverified details depend on confirmation.
- Content is written answer-first so a human or an assistant can extract: who it serves, the vehicle,
  capacity, city, service types, how quoting works, limitations, what the customer must provide, and how
  to make contact.
- **No promise of placement** in AI Overviews, ChatGPT or any AI surface is made anywhere.

### Official-source findings, and what changed as a result

**OpenAI — `OAI-SearchBot`** (`https://platform.openai.com/docs/bots`) is used to surface websites in
ChatGPT's search features, and OpenAI states that sites opted out "will not be shown in ChatGPT search
answers, though can still appear as navigational links". It is independent of `GPTBot`, so a site can
allow search citation while disallowing training. OpenAI recommends allowing OAI-SearchBot in robots.txt
**and allowing traffic from its published IP ranges** (`https://openai.com/searchbot.json`) — a host/CDN
level setting, not a robots.txt setting. It can take ~24 hours for a robots.txt change to take effect.
Our robots.txt already allows OAI-SearchBot; the IP-range item is added to the launch checklist.
Placement is explicitly not guaranteed (`https://help.openai.com/en/articles/9237897`).

**Google — generative AI features** (`https://developers.google.com/search/docs/fundamentals/ai-optimization-guide`,
last updated 2026-07-10) states that standard SEO practice still applies, favours original
non-commodity content with a distinct point of view, and names as things to ignore for Google Search:
content "chunking", unnecessary AI text files such as `llms.txt`, and inauthentic mentions.
Consequence for this project: **`/llms.txt` is retained but downgraded to a low-value artefact.** It is
kept because it is cheap, harmless and factually accurate, and because a small number of non-Google
tools may read it — **not** because Google or OpenAI consume it. It must not be presented as an SEO
achievement, and no further effort should be invested in it.

**Google Business Profile — service-area businesses** (`https://support.google.com/business/answer/9157481`):
a service-area business "visits or delivers to customers directly but doesn't serve customers at their
business address"; if customers are not served at the address, the address should be removed from the
profile. One profile covers the whole area served; no radius is permitted; areas are specified by city
or postcode, up to 20, and should be within roughly two hours' driving time of the base. A business
without permanent on-site signage is not eligible as a storefront and should be listed as service-area.
This directly shapes `GBP_SETUP_CHECKLIST.md`.

## Local SEO

`GBP_SETUP_CHECKLIST.md` covers Google Business Profile preparation. Nothing is published to GBP from
here; the checklist is a preparation document for the owner to execute, because GBP requires a verified
owner and a genuine service-area or premises situation.
"""

DOCS["CONTENT_MAP.md"] = f"""# CONTENT MAP

Date: {T}

## Built in V1

| URL | Type | Purpose |
|---|---|---|
| `/` | Commercial | Position the vehicle, the trip types, and the quote path |
| `/airport-group-transfer-hyderabad/` | Commercial | Group airport arrivals, departures, multiple pickups |
| `/wedding-event-transport-hyderabad/` | Commercial | Guest movements across a wedding schedule |
| `/corporate-group-transport-hyderabad/` | Commercial | Teams, delegations, conference and multi-stop days |
| `/hyderabad-sightseeing-group-travel/` | Commercial | Day hire, multi-stop itineraries, transport vs tour distinction |
| `/request-quote/` | Transactional | The single conversion point |
| `/guides/` | Hub | Index of the three guides |
| `/guides/force-urbania-vs-tempo-traveller/` | Informational | Comparison intent |
| `/guides/group-vehicle-fit-guide/` | Informational | Vehicle choice and the luggage question |
| `/guides/wedding-guest-transport-planning/` | Informational | Movement-list planning |
| `/about/` | Trust | What this is and what it deliberately is not |
| `/contact/` | Trust | Phone, form, email, and what is still unconfirmed |
| `/privacy/`, `/terms/` | Legal | Handling of details; quotation terms |
| `/404.html` | Utility | Recovery paths |

15 pages total, 14 in the sitemap. Deliberately not 50 location pages.

## Deliberately not built yet

The brief lists further article ideas. They are held back on purpose rather than mass-produced:

| Idea | Why held |
|---|---|
| "How Force Urbania Day Hire Works" | Substantially overlaps `/hyderabad-sightseeing-group-travel/`; would cannibalise it |
| "How to Plan a Multi-Stop Group Trip in Hyderabad" | Overlaps the fit guide and the sightseeing page |
| "How Much Luggage Can a Group Vehicle Carry?" | Cannot be answered honestly until the actual vehicle is inspected. Building it now would force a fabricated capacity claim |
| "Group Airport Transfers: What Information Should You Provide?" | This content is already the "Information / Include" section of the airport page |

These become worth building **after** real enquiry data shows which questions are actually being asked.
See `POST_LAUNCH_ROADMAP.md`.

## Rules applied to all content

No statistic is stated unless sourced. No review, rating, customer count or testimonial appears anywhere,
because none exists yet. No claim about the driver, permit, insurance, address or vehicle condition is
made. Where a reader might expect such a claim, the page states plainly that the detail is provided with
the quotation or is still being confirmed.
"""

DOCS["DO_NOT_PUBLISH_UNTIL_VERIFIED.md"] = f"""# DO NOT PUBLISH UNTIL VERIFIED

Owner checklist. This page is the gate between "built" and "launch ready".
Last updated: {T}

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
"""

DOCS["GBP_SETUP_CHECKLIST.md"] = f"""# GOOGLE BUSINESS PROFILE — SETUP CHECKLIST

Date: {T} · Preparation only. Nothing is published to GBP by this project.

**Do not create GBP with unverified information.** A profile built on assumptions is a suspension risk
and, more importantly, a trust problem with real customers.

## Before starting
- [ ] Confirm final business name (not yet decided)
- [ ] Confirm whether this is a **service-area business** (no customer-facing premises) or a premises business
- [ ] **Do not** use a virtual office or coworking address purely to appear local

### Official rules that apply here
From Google Business Profile Help, "Manage your service areas for service-area & hybrid businesses"
(`https://support.google.com/business/answer/9157481`), verified 2026-10-03:

- A **service-area business** "visits or delivers to customers directly but doesn't serve customers at
  their business address". If customers are not served at the address, **remove the address from the profile.**
- Only **one** profile is permitted for the whole service area.
- You **cannot set a radius.** Areas are specified by city, postcode or another area type, up to **20**
  service areas.
- The overall area "shouldn't be more than about **2 hours of driving time** from where your business is
  based" — so unrestricted "all of Telangana" style claims are not appropriate.
- A business **without permanent on-site signage is not eligible as a storefront** and should be listed
  as service-area.

For a single vehicle with no confirmed operating base, this is very likely a service-area business.
Confirm against the live documentation at setup time, because these rules change.

## Fields

| Field | Value to use | Status |
|---|---|---|
| Business name | Real trading name only — no keywords | Blocked: name undecided |
| Primary category | Research the closest fit (e.g. a vehicle-hire / chauffeur / group-transport category) | To research |
| Secondary categories | Add only genuinely applicable ones | To research |
| Phone | +91 62020 66104 | Provided — confirm it should be public |
| Website | Real domain + `/request-quote/` for the quote link | Blocked: domain undecided |
| Service area | Only real areas actually served | Blocked: unconfirmed |
| Address | Only if genuine and customer-facing | Blocked |
| Opening / contact hours | Only if accurate. Do not imply 24/7 | Blocked |
| Business description | Factual, no keyword stuffing | Can draft now |
| Services | The four trip types, described plainly | Can draft now |
| Photographs | Real vehicle photographs only | Blocked: no photos |
| Logo | Real logo, or the simple mark | Optional |

## After the profile is live
- [ ] Add a UTM-tagged link to the site for measurement
- [ ] Post the four trip types as services, not as keyword lists
- [ ] Start a review request process — ask real customers only, and never incentivise
- [ ] Never create fake reviews, and never ask staff or family
- [ ] Keep NAP (name, address, phone) identical everywhere it appears

## Reviews — the honest position
There are currently zero reviews and none will be fabricated. Reviews are earned by asking real
customers after a completed trip. `POST_LAUNCH_ROADMAP.md` covers the request process.
"""

DOCS["ANALYTICS_PLAN.md"] = f"""# ANALYTICS PLAN

Date: {T}

## Status

**Not implemented.** No analytics is loaded, because doing so requires the owner's account and would set
cookies. The privacy page states accurately that the site sets no analytics or advertising cookies —
that statement must be updated *before* any analytics is enabled, not after.

## Recommended stack (free tiers)

1. **Google Analytics 4** or a privacy-friendly alternative (Plausible, Umami). A lighter option keeps
   the site fast, which matters more than report richness at one-vehicle scale.
2. **Google Search Console** — required. This is the single most valuable data source for this business:
   it shows the real queries arriving, including the long-tail group-size and luggage questions.
3. **Bing Webmaster Tools** — cheap to add, covers Bing and Copilot surfaces.

## Events to track

| Event | Fires when | Why |
|---|---|---|
| `quote_form_view` | `/request-quote/` loads | Size of the top-of-funnel |
| `quote_form_start` | First field interaction | Where drop-off begins |
| `quote_form_submit` | Validation passes and submit fires | The primary conversion |
| `quote_form_error` | Validation fails | Finds confusing fields |
| `phone_click` | Any `tel:` link tapped | Many enquiries will be calls, not forms |
| `email_click` | `mailto:` tapped | Secondary path |
| `whatsapp_click` | WhatsApp button tapped | Only once the number is enabled |
| `service_page_view` | Any of the four service pages loads | Which trip type attracts demand |
| `guide_read` | Guide pages with high scroll depth | Which questions deserve a real page |

The form already captures `source_page`, `submitted_at`, and any `utm_*` / `gclid` parameters into the
submitted payload — so attribution survives the enquiry even before analytics exists.

## Measurement model

```
TRAFFIC SOURCE (utm / referrer / GBP)
    -> LANDING PAGE
        -> SERVICE PAGE VIEW
            -> QUOTE START
                -> QUOTE SUBMISSION
                    -> QUALIFIED LEAD        (owner judgement)
                        -> QUOTED
                            -> BOOKED
```

## KPIs

- **Primary: qualified trip enquiries.** Not sessions, not page views.
- Secondary: enquiry → quotation rate; quotation → booking rate.
- Watched but not optimised for: average position, impressions, guide readership.

## Privacy

If analytics is enabled: add a consent mechanism where required, update `/privacy/`, keep IP handling
privacy-conscious, and avoid adding more than one analytics script to protect page speed.

## Attribution discipline

No lead is counted as "from Google" without checking Search Console. No claim about which channel works
is made until at least a month of real enquiry data exists.
"""

DOCS["QA_REPORT.md"] = f"""# QA REPORT — independent red-team pass

Date: {T} · Method: automated source scanning + build validation + live HTTP checks + browser DOM testing.

Severity: **BLOCKER** (must fix or document before launch) · **HIGH** · **MEDIUM** · **LOW**

---

## BLOCKER

**B1 — Domain not set.** `BASE` is `https://urbania-hyderabad.example`. Every canonical URL, the
`sitemap.xml` entries and the `Sitemap:` line in `robots.txt` therefore point at a domain that does not
exist. *Impact:* the site cannot be indexed correctly. *Fix:* register the domain and update `BASE`.
*Documented:* yes, in OWNER_DECISIONS and DO_NOT_PUBLISH_UNTIL_VERIFIED.

**B2 — RESOLVED: lead delivery now goes to WhatsApp.** The owner directed delivery to WhatsApp, so the
quote form opens `wa.me` with the complete trip details pre-filled — trip type, date, passengers, pickup,
drop, duty duration, hours/days, estimated km, notes, name, phone, email, source page, ISO timestamp and
any `utm_*`/`gclid` parameters. **Verified in a real browser** with a filled form: the constructed URL
contained every field and resolved to `https://wa.me/919182126104`. If the WhatsApp app does not open,
the confirmation panel shows a one-tap retry link and a visible copy of the exact message, so the details
are never lost. `FORM_ENDPOINT` remains available for a hosted endpoint later.
*Residual risk:* low — WhatsApp is the dominant enquiry channel in this market and works on mobile.

**B3 — Business name undecided.** The working name `Urbania Hyderabad` is published throughout.
*Impact:* identity, branding and Google Business Profile all depend on it. *Fix:* owner decision.

## HIGH

**H1 — No real vehicle photography.** The site uses a clearly labelled illustrative SVG diagram, so the
claim is honest. But a 17-seat vehicle business without photographs of the vehicle is materially less
convincing. *Mitigation in place:* the caption states plainly that it is a diagram, not a photograph.
*Fix:* the shot list in DO_NOT_PUBLISH_UNTIL_VERIFIED.

**H2 — 11 `[VERIFY BEFORE PUBLISHING]` markers remain in source.** All are HTML comments, invisible to
visitors. *Impact:* none to the visitor; they gate completeness. *Fix:* resolve each.

**H3 — WhatsApp suppressed.** `WHATSAPP` is empty, so no WhatsApp button is rendered. In this market
WhatsApp is likely the highest-converting channel. *Impact:* a lost conversion path, not a broken one.
*Fix:* supply the number.

## MEDIUM

**M1 — "Hyderabad" used as service area without a confirmed operating base.** The pages say "in Hyderabad"
rather than "based in Hyderabad", and outstation is answered conditionally. This is as safe as the copy
can be, but it still asserts Hyderabad. *Fix:* confirm the service area.

**M2 — Response-time expectation not published.** The quote page says "we aim to respond promptly"
rather than a number, because no SLA exists. This is honest but leaves a genuine buyer question open.
*Fix:* confirm a realistic response window.

**M3 — Cloudflare prepends a Content-Signal preamble to robots.txt.** Verified live: Cloudflare's block
appears above our rules, and our rules survive intact. *Impact:* none to function, but the file is longer
than expected. *Fix:* none required; noted so it is not mistaken for tampering.

**M4 — Quote form has no server-side validation or rate limiting.** Protection is a honeypot field plus
client-side validation only. *Impact:* determined spam is possible. *Fix:* use a form provider that
handles spam, or add server-side validation when an endpoint is added.

**M5 — FAQ rich results no longer exist, so the FAQPage markup earns nothing in Google.** Google
deprecated the FAQ rich result: removed from Search on 7 May 2026, documentation removed 15 June 2026
(`https://developers.google.com/search/updates`). `FAQPage` remains a valid schema.org type that
accurately describes visible content, so it is retained — but it will never produce a rich result.
*Impact:* a corrected expectation, not a defect. The SEO documentation has been amended.

**M6 — The WhatsApp Business profile conflicts with the market this site targets.** The profile's location
reads "Supaul, Bihar" while the site targets Hyderabad, and the profile has no business email or website
set. *Impact:* customer trust, and Google Business Profile service-area eligibility. *Fix:* resolve
conflicts C1–C3 in `FACTS_LEDGER.md` before GBP setup.

## LOW

**L1 — Email address published is a personal address.** Functional, but a domain address reads as more
established. *Fix:* when the domain is registered.

**L2 — No logo.** The mark is a simple "17" tile. Adequate, not distinctive.

**L3 — Guide count is three.** Deliberately limited; see CONTENT_MAP for why more were withheld.

## Checks that PASSED

| Check | Result |
|---|---|
| Pages built | 15 |
| JSON-LD parse errors | 0 |
| Pages with exactly one H1 | 15 / 15 |
| Missing canonical / description / OG | 0 |
| Broken internal links | 0 |
| Live HTTP status, all routes | 20 / 20 returned 200 |
| Forbidden-claim scan (24/7, vetted, fully insured, best price, luxury fleet, multiple vehicles, instant booking, 500+ customers, pan-India, lorem ipsum, TODO) | 0 real hits — the 6 matched occurrences are all negations ("not guaranteed", "we do not publish a guaranteed response time") |
| Fabricated reviews / ratings / counters | None anywhere |
| Fabricated address or geo coordinates | None anywhere |
| Schema type accuracy vs visible content | Accurate; `LocalBusiness`, `Review`, `AggregateRating`, `openingHours`, `priceRange`, `geo` deliberately omitted |
| Mobile navigation | Present, keyboard operable, `aria-expanded` toggled |
| Sticky mobile CTA | Present, both Quote and Call |
| Form labels | Every input labelled via wrapping `<label>`; honeypot marked `aria-hidden` |
| Reduced-motion support | `prefers-reduced-motion` block present |
| Focus visibility | `:focus-visible` outline defined |
| Template leftovers / dummy phone / dummy address | None — the only phone number is the owner-supplied number |
| Exposed secrets or API keys | None; no credentials exist in the frontend |
| `noindex` on 404 | Yes |

## Self-critique (the four perspectives)

**Business owner:** the site states what is offered, who it is for, what information is needed, how to
enquire and what happens next — on every page. It does not overclaim.

**Conversion specialist:** one primary CTA repeated on every page, phone always reachable, sticky mobile
bar, short form with progressive fields. Weakness: the form asks for a fair amount before any contact
value is returned. Acceptable here because the business genuinely needs those details to quote.

**Designer:** light, restrained, generous spacing, no taxi-app aesthetic, no black-and-gold cliché. The
illustrative vehicle diagram is the weakest visual element and is honestly labelled as such.

**Engineer:** zero dependencies, static output, one CSS file, ~60 lines of JS, validated output, no
console errors observed, no layout shift from the hero.
"""

DOCS["LAUNCH_CHECKLIST.md"] = f"""# LAUNCH CHECKLIST

Current status: **NOT launch ready.** Blockers B1, B2 and B3 in `QA_REPORT.md` are open.

## Identity
- [ ] Final business name confirmed and applied (`BRAND` in `build_ui.py`)
- [ ] Domain registered, `BASE` updated, site rebuilt
- [ ] Canonical URLs resolve to the real domain
- [ ] `Sitemap:` line in `robots.txt` points at the real domain
- [ ] Logo finalized

## Infrastructure
- [ ] HTTPS — confirm the host serves HTTPS and redirects HTTP
- [ ] Single canonical host (www or non-www, not both)
- [ ] Staging environment `noindex`ed, or not publicly reachable
- [ ] 404 page served with a 404 status, not a 200

## Leads
- [ ] `FORM_ENDPOINT` set to a hosted endpoint, or mailto explicitly accepted as the model
- [ ] Test submission sent from a real phone on mobile data
- [ ] Spam protection active
- [ ] Notification reaches the owner, and the message contains trip details, source page, timestamp and UTM
- [ ] Test `tel:` link tapped on a real phone
- [ ] WhatsApp number set, or button confirmed intentionally hidden

## On-page
- [ ] All 11 `[VERIFY BEFORE PUBLISHING]` markers resolved
- [ ] Title and meta description reviewed for every page
- [ ] Open Graph images added (currently none)
- [ ] Structured data re-validated after any content change
- [ ] Internal links reviewed
- [ ] Alt text reviewed once real images replace the diagram

## Technical
- [ ] `robots.txt` reviewed and intentional
- [ ] Host/CDN allows traffic from OpenAI's published search-bot IP ranges
      (`https://openai.com/searchbot.json`) — required for ChatGPT search eligibility and **not**
      settable in robots.txt
- [ ] After any robots.txt change, allow ~24 hours before judging the effect in ChatGPT
- [ ] `sitemap.xml` submitted to Google Search Console and Bing Webmaster Tools
- [ ] Search Console verification
- [ ] Analytics implemented and `/privacy/` updated to match
- [ ] Performance tested at 320 / 375 / 390 / 430 / 768 px and desktop
- [ ] Lighthouse run recorded, with important findings fixed
- [ ] Accessibility basics checked: contrast, labels, keyboard, focus states

## Content and facts
- [ ] Every published statement verified against `FACTS_LEDGER.md`
- [ ] No placeholder, TODO or developer text remains
- [ ] No fabricated review, rating, counter, address or photograph
- [ ] Privacy and terms reviewed by the owner
- [ ] Real vehicle photographs in place

## Day of launch
- [ ] Rebuild and verify every route returns 200
- [ ] Click every link
- [ ] Submit the form once for real and confirm delivery
- [ ] Confirm Google Business Profile consistency with the site (name, phone, URL)
"""

DOCS["POST_LAUNCH_ROADMAP.md"] = f"""# POST-LAUNCH ROADMAP

Date: {T}

## Principle

Do not publish thirty articles. Publish the four commercial pages that exist, then let real evidence
decide what is written next. Content priorities come from Search Console queries, actual enquiry
language, and the questions asked on the phone — not from assumptions about demand.

## Month 1 — measure, do not build

- Verify Search Console and Bing Webmaster Tools; submit the sitemap.
- Enable analytics and update the privacy page first.
- Read every incoming enquiry and log the exact wording used, especially for group size and luggage.
- Record which page each enquiry came from.
- Do not write new pages yet. There is no data to justify them.

## Month 2 — first evidence-led additions

Choose only what the data supports:

| If the data shows | Then build |
|---|---|
| Searches for group size and luggage | A real "group vehicle luggage" page — but only once the actual capacity is measured |
| Repeated "Urbania or Tempo Traveller?" enquiries | Expand the comparison guide with concrete decision criteria |
| Demand concentrated in one destination | A genuinely useful destination transport page with real route detail |
| Corporate enquiries asking for GST and invoicing | Publish those details once confirmed, not before |
| Calls dominating over form submissions | Strengthen the phone path and shorten the form |

## Month 3 — trust assets

- Publish real vehicle photographs as soon as they exist, replacing the illustrative diagram.
- Begin collecting reviews from real completed trips, and only real ones.
- Publish the confirmed operational details — permit, insurance, driver arrangement — once verified.
- Add first completed-trip case detail, described accurately and without invented numbers.

## Ongoing

- Monthly: review Search Console queries, enquiry language and phone questions; pick the next single
  content priority.
- Quarterly: re-check Google Search Central and Google Business Profile guidance, because the rules change.
- Continuously: keep every published claim aligned with `FACTS_LEDGER.md`. If a fact changes, change the
  ledger and the site together.

## Explicitly out of scope until there is revenue evidence

Fleet expansion content · multi-city landing pages · packaged tour products · booking engine ·
customer accounts · CRM platform. Each would add cost and complexity for a single-vehicle business
without demonstrated return.
"""

DOCS["README.md"] = f"""# Hyderabad group transport website — 17-seat Force Urbania

A quote-first static website for a one-vehicle private group transport business in Hyderabad.
Built {T}. **Not launch ready** — see blockers in `docs/QA_REPORT.md`.

Live preview (temporary): https://shopzilla-lying-pension-speaks.trycloudflare.com

> The preview is an ephemeral Cloudflare quick tunnel. It dies when the host process stops and is
> **never** suitable for search indexing.

## What this is

- **15 pages**: 1 home, 4 trip-type pages, 3 guides + hub, quote form, about, contact, privacy, terms, 404.
- **Zero runtime dependencies.** Static HTML, one CSS file, ~60 lines of vanilla JS.
- **Framework:** none. Content is generated by three Python files.
- **Vehicle:** one 17-seat Force Urbania. There is no fleet, no inventory and no availability calendar —
  by design, not by omission.

## Files

| File | Purpose |
|---|---|
| `build_ui.py` | Config, design system, head/header/footer, shared components |
| `build_pages.py` | Every page, the quote form, robots/sitemap/llms.txt, 404 |
| `write_docs.py` | Generates this documentation set |
| `*.html`, `*/index.html` | Generated output — **do not edit by hand** |
| `style.css`, `favicon.svg` | Generated output |
| `docs/` | Research, decisions and launch gates |

## Build

```bash
cd ~/revenue-lab/website/urbania
python3 build_pages.py        # regenerates all HTML, CSS, robots, sitemap, llms.txt
python3 write_docs.py         # regenerates docs/
```

No install step, no dependencies, no virtualenv.

## Local preview

```bash
python3 -m http.server 8100 --bind 127.0.0.1
# http://127.0.0.1:8100/
```

## Deployment

The output is plain static files. Any static host works. Requirements:

1. Serve over HTTPS.
2. Redirect to one canonical host (www or non-www, not both).
3. Serve `/404.html` with an actual 404 status.
4. Directory-index behaviour so `/request-quote/` resolves to `/request-quote/index.html`.

**Before deploying:** set `BASE` in `build_ui.py` to the real domain and rebuild, or every canonical
URL and the sitemap will be wrong.

## Configuration — every knob in one place

In `build_ui.py`:

| Constant | Current value | Meaning |
|---|---|---|
| `BASE` | `https://urbania-hyderabad.example` | **Must change.** Drives canonicals and the sitemap |
| `BRAND` | `Urbania Hyderabad` | Working name — owner decision |
| `PHONE` / `PHONE_HREF` | `+91 62020 66104` | Owner-supplied |
| `WHATSAPP` | `919182126104` | WhatsApp delivery + button. **Differs from `PHONE`** — see conflicts C1–C3 |

In `build_pages.py`:

| Constant | Current value | Meaning |
|---|---|---|
| `FORM_ENDPOINT` | empty | Empty falls back to **WhatsApp delivery** (verified working). Set it for hosted-endpoint delivery instead |
| `LEAD_EMAIL` | `fca.abhi007@gmail.com` | Where the mailto fallback sends |

## Content editing

Edit `build_ui.py` or `build_pages.py`, then run `python3 build_pages.py`. Never edit generated HTML.

## Adding a page

1. Add a builder function in `build_pages.py`.
2. Call it from `main()`.
3. Add the path to `SITEMAP`.

## Honesty rules enforced in this codebase

These are not stylistic preferences. They are the project's core constraint:

1. **No unverified fact is stated as settled.** 11 `[VERIFY BEFORE PUBLISHING]` markers in the source
   flag every place a decision is needed. They are HTML comments, invisible to visitors.
2. **No fabricated social proof.** No reviews, ratings, counters, awards or customer numbers exist
   anywhere on the site, because none are real.
3. **No fabricated address or location claims.** The copy says "in Hyderabad", never "based in Hyderabad",
   because the operating base is unconfirmed. `LocalBusiness` schema is deliberately omitted since it
   expects an address.
4. **Luggage is never quantified.** The most common group-travel question is answered by asking for the
   details and confirming suitability, because the real capacity has not been measured.
5. **A diagram is labelled a diagram.** The vehicle visual is an SVG that says plainly it is not a
   photograph of the actual vehicle.
6. **The enquiry is never called a booking.** Every page and the form itself state that submitting an
   enquiry does not confirm availability or create a booking.

## Documentation

`FACTS_LEDGER.md` · `OWNER_DECISIONS.md` · `SEO_STRATEGY.md` · `KEYWORD_MAP.csv` ·
`TEMPLATE_SHORTLIST.md` · `TEMPLATE_DECISION.md` · `CONTENT_MAP.md` · `GBP_SETUP_CHECKLIST.md` ·
`DO_NOT_PUBLISH_UNTIL_VERIFIED.md` · `ANALYTICS_PLAN.md` · `QA_REPORT.md` · `LAUNCH_CHECKLIST.md` ·
`POST_LAUNCH_ROADMAP.md` · `SEARCH_INTELLIGENCE.md` · `COMPETITOR_NOTES.md` · `CONTENT_GAPS.md`
"""

for name, body in DOCS.items():
    with open(os.path.join(D, name), "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"wrote docs/{name}  ({len(body):,} chars)")
print(f"\n{len(DOCS)} documents written to docs/")
