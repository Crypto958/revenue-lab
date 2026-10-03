# SEARCH INTELLIGENCE V3 — Hyderabad group transport (expanded scope)

**Business:** one 17-seat Force Urbania. Market: Hyderabad. Model: pre-booked private group transport /
vehicle hire with driver; **quote-first, not instant booking**; **not a tour operator** (no packages,
tickets, guides or hotels).
**Date of research:** 2026-10-03 (UTC). **Supersedes:** `SEARCH_INTELLIGENCE.md` (V2).
**V3 change:** EXPANDS coverage to **outstation/intercity group travel**, **family group travel**, and
**vehicle-size recommendation** queries ("vehicle for 10 people Hyderabad", "vehicle for 15 people Hyderabad"),
on top of the V2 core (Force Urbania, 17-seater, airport, wedding, corporate, sightseeing, day hire, custom).

---

## 0. HARD RULE — how to read every classification here

> **No search volume or statistic in this document is measured data.** No keyword tool, Search Console,
> Ads account or third-party volume source was accessed. Every intent label — **HIGH COMMERCIAL INTENT /
> MEDIUM COMMERCIAL INTENT / INFORMATIONAL / LOCAL INTENT / BRANDED** — is a **qualitative judgement**
> inferred from (a) the phrasing of the query, (b) which competitors build dedicated pages for it, and
> (c) whether the observed SERP is commercial (quote/booking pages) or informational (guides/blogs).
> **Treat every classification as a directional hypothesis to test, not a fact.**
>
> Competitor observations are limited to domains actually fetched (see `COMPETITOR_NOTES_V3.md` §1 for the
> named list). Anything that could not be loaded is **COULD NOT VERIFY**.

---

## 1. What changed for V3 (expanded scope)

| New scope area | Why it matters | Headline read (judgement) |
|---|---|---|
| **Outstation / intercity group travel** | The van's highest-value, highest-margin use case (multi-day, min-km/day, driver batta, permits). | Commercial and under-served: competitors park outstation numbers behind flat per-km maps or route calculators; almost nobody explains *how the outstation quote is built*. |
| **Family group travel** | The warmest buyer; 12–16 people travelling together is exactly the 17-seat configuration. | Treated as a bullet on every competitor page, never a page of its own. Open content gap. |
| **Vehicle-size recommendation** ("vehicle for 10 / 15 people") | The *pre-purchase* question; the query that decides whether you even get an enquiry. | Answered inconsistently; a capacity-led explainer is a clean, ownable wedge. |

---

## 2. Intent map — CORE scope (carried from V2, still current)

Classifications are **judgement**. Full row-by-row mapping is in `KEYWORD_MAP.csv`.

| Theme | Representative queries | Intent class (judgement) |
|---|---|---|
| Force Urbania rental | force urbania rental / hire / on rent / booking hyderabad | HIGH COMMERCIAL INTENT |
| Force Urbania pricing | force urbania rental price hyderabad; per km rate | HIGH COMMERCIAL INTENT |
| 17 seater hire | 17 seater tempo traveller / van / vehicle hire hyderabad | HIGH COMMERCIAL INTENT |
| Group travel | group travel hyderabad; group tour vehicle hire | MEDIUM COMMERCIAL INTENT |
| Airport group transfer | airport group transfer hyderabad; RGIA group pickup | HIGH COMMERCIAL INTENT |
| Wedding transport | wedding guest transport / wedding bus / baraat vehicle hyderabad | HIGH COMMERCIAL INTENT |
| Corporate transport | corporate transport / corporate tempo traveller hyderabad | HIGH COMMERCIAL INTENT |
| Sightseeing vehicle | hyderabad sightseeing cab / tempo traveller; hyderabad darshan | MEDIUM / LOCAL INTENT |
| Day hire | full day car rental; 8 hour 80 km package | MEDIUM COMMERCIAL INTENT |
| Urbania vs tempo traveller | force urbania vs tempo traveller; tempo traveller alternative | INFORMATIONAL |
| Branded | <business name> hyderabad | BRANDED (placeholder — pending the BRAND_DECISION) |

---

## 3. Intent map — **NEW** scope (outstation / family / vehicle-size)

All labels below are **JUDGEMENT, not measured**.

### 3.1 Outstation / intercity group travel

| Representative queries | Intent class (judgement) | Likely page | Why |
|---|---|---|---|
| hyderabad to tirupati tempo traveller / group vehicle | **HIGH COMMERCIAL INTENT** | /outstation-group-trips-hyderabad | Top pilgrimage route; multiple competitors have route pages |
| hyderabad to srisailam tempo traveller | **HIGH COMMERCIAL INTENT** | /outstation-group-trips-hyderabad | Short high-frequency route; heavily priced in SERPs |
| hyderabad to nagarjuna sagar cab / vehicle | **MEDIUM COMMERCIAL INTENT** | /outstation-group-trips-hyderabad | Short outstation route |
| hyderabad to warangal cab / tempo traveller | **MEDIUM COMMERCIAL INTENT** | /outstation-group-trips-hyderabad | Regional outstation |
| hyderabad to goa / shirdi / vijayawada group trip vehicle | **MEDIUM COMMERCIAL INTENT** | /outstation-group-trips-hyderabad | Long-haul; multi-day, permit-dependent |
| outstation cab from hyderabad group | **MEDIUM COMMERCIAL INTENT** | /outstation-group-trips-hyderabad | Generic outstation + group qualifier |
| tempo traveller minimum km per day | **INFORMATIONAL INTENT** | /outstation-group-trips-hyderabad#pricing | The single most confusing outstation term (250 vs 300 km) |
| driver batta / night charge tempo traveller | **INFORMATIONAL INTENT** | /outstation-group-trips-hyderabad#pricing | Explains the quote; builds trust |
| do tempo travellers run from hyderabad to tirupati | **INFORMATIONAL INTENT** (AI/voice) | /outstation-group-trips-hyderabad | Feasibility question; AI-answer target |

### 3.2 Family group travel

| Representative queries | Intent class (judgement) | Likely page | Why |
|---|---|---|---|
| family group travel hyderabad | **MEDIUM COMMERCIAL INTENT** | /family-group-travel-hyderabad | Warm commercial; group-size-led |
| family trip van hire hyderabad | **MEDIUM COMMERCIAL INTENT** | /family-group-travel-hyderabad | Vehicle-hire framing |
| extended family travel vehicle hyderabad | **MEDIUM COMMERCIAL INTENT** | /family-group-travel-hyderabad | Speaks directly to 12–16 passengers |
| is a 17 seater tempo traveller good for a family trip | **INFORMATIONAL INTENT** (AI/voice) | /family-group-travel-hyderabad | Honest pros/cons; AI-answer target |
| best vehicle for a family pilgrimage from hyderabad | **INFORMATIONAL INTENT** | /family-group-travel-hyderabad | Ties to Tirupati/Srisailam |
| family trip to tirupati / srisailam vehicle hire | **MEDIUM–HIGH COMMERCIAL INTENT** | /family-group-travel-hyderabad + outstation page | Overlaps outstation; the family frame is the emotional layer |

### 3.3 Vehicle-size recommendation

| Representative queries | Intent class (judgement) | Likely page | Why |
|---|---|---|---|
| **vehicle for 10 people hyderabad** | **HIGH COMMERCIAL INTENT** | /group-vehicle-fit-guide | Capacity + city = pre-purchase commercial |
| **vehicle for 15 people hyderabad** | **HIGH COMMERCIAL INTENT** | /group-vehicle-fit-guide | Points straight at a 17-seat Urbania |
| how many people can fit in a tempo traveller | **INFORMATIONAL INTENT** | /group-vehicle-fit-guide | Definitional; AI-answer target |
| which vehicle is best for 10 / 15 / 16 people | **INFORMATIONAL INTENT** (advice-seeking) | /group-vehicle-fit-guide | Sits just above the commercial click |
| 12 seater vs 17 seater vs 20 seater | **INFORMATIONAL INTENT** | /group-vehicle-fit-guide | Comparison; feeds AI answers |
| how much luggage fits in a 17 seater tempo traveller | **INFORMATIONAL INTENT** | /group-vehicle-fit-guide | The most-asked, least-answered group question |
| 17 seater force urbania seating layout | **INFORMATIONAL INTENT** | /group-vehicle-fit-guide | Configuration clarity (16+D vs 17+D confusion) |

**Judgement on this cluster:** the *"vehicle for N people"* phrasing is a **commercial** query wearing an
informational coat — the searcher is about to enquire. The market answers it badly (see
`COMPETITOR_NOTES_V3.md` §4: TaxiYatri's "15 seater" page even lists 24-seat rows). A single, honest,
capacity-led fit guide is the cleanest wedge in the new scope.

---

## 4. Question-form queries (Google, AI answer engines, voice) — V3 additions

Added to the V2 question sets (see `SEARCH_INTELLIGENCE.md` §4):

**Outstation**
- How far is Hyderabad to Tirupati by road, and can a tempo traveller do it in one day?
- What is the minimum kilometres per day for an outstation tempo traveller?
- What is driver batta and night charge on a Hyderabad outstation trip?
- Do I need an interstate permit for a group trip from Hyderabad to Goa?

**Family**
- Which is the best vehicle for a family group of 14 from Hyderabad?
- Is a Force Urbania comfortable for elderly passengers on a long trip?
- How do we fit 15 family members and their luggage in one vehicle?

**Vehicle-size**
- What vehicle should I hire for 10 people in Hyderabad?
- What vehicle should I hire for 15 people in Hyderabad?
- How many passengers fit in a 17-seat Force Urbania, including the driver?
- How much luggage fits in a 16+D Urbania?

AI answer engines **retrieve and cite**, so each answer on the page must be **self-contained, factual and
non-commodity**, and (per V2 §5.2) the site must allow `OAI-SearchBot` so it is citable. Do **not** fabricate
rates or volumes; answer with the *method* and an honest indicative range.

---

## 5. Competitor rate context (as published, NOT verified market rates)

Useful only for *relative framing*; the fetched pages contradict themselves (see `COMPETITOR_NOTES_V3.md` §6).

- **Tempo / Urbania outstation, Hyderabad, as published:** roughly **₹23–₹30/km** for 12–17 seaters on
  chikucab / hyderabaddeccantourism; **₹16–₹36/km** across the 9–30 seater matrix on bookmytempotraveller;
  **₹30/km** for a 17-seat Urbania on hyderabaddeccantourism; **₹38–₹45/km** for a premium Urbania operator
  with a 300 km/day minimum (urbania.rentals, no Hyderabad hub).
- **Minimums observed:** 250 km/day (chikucab, bookmytempotraveller, trivenicabs) to 300 km/day
  (cabzii, urbania.rentals, 24cabservice snippet).
- **Driver allowance observed:** ₹800/day (hyderabaddeccantourism) to ₹1,000/day (urbania.rentals);
  night charge ₹500 (chikucab) – ₹1,000 (urbania.rentals).
- **Route packages:** HYD→Srisailam from ≈₹10,492–₹13,570; HYD→Tirupati ≈₹43,500 (MMT 12-seat, 1,250 km/108 hr).
  *(All competitor-published; treat as indicative only.)*

> These are **published figures on fetched pages**, not survey data and not recommended prices. The operator
> has no verified rate card (`FACTS_LEDGER.md`), so the site must publish *how a quote is built*, not a rate card.

---

## 6. Local + AI-engine notes (carried from V2, unchanged)

- Local intent ("near me", "in Hyderabad") routes through an accurate **Google Business Profile**, a single
  service-area page and the ~2-hour drive-time service-area rule — not spam locality pages. (V2 §5.1(a).)
- Google **no longer shows FAQ rich results** (deprecated May 2026) — but Q&A *content* is still indexed and
  is the extractable format AI answer engines cite. Write Q&A; do not expect an FAQ SERP feature. (V2 §5.1(b).)
- Allow `OAI-SearchBot` so the site is citable in ChatGPT search; `llms.txt` is explicitly **not** a Google
  ranking factor (Google names it something to ignore). (V2 §5.1, §5.2.)
- **Branded** queries depend on the final name — pending `BRAND_DECISION.md`. A coined brand has **no existing
  demand**, so every title must pair **brand + descriptive words** (e.g. "<brand> — 17-seat Force Urbania
  group travel in Hyderabad").

---

## 7. Could not verify (V3)

- **COULD NOT VERIFY** any keyword search volume or trend for any term, in any scope. No volume source was accessed.
- **COULD NOT VERIFY** that the intent classes above match real query volumes — they are judgements from
  phrasing + observed SERPs, not data.
- **COULD NOT VERIFY** the competitor-published rates in §5 as true *market* rates; they are what the pages
  say, and several pages contradict themselves and each other.
- **COULD NOT VERIFY** the specific pages/volumes behind SERP-only domains listed in `COMPETITOR_NOTES_V3.md` §1.
- **COULD NOT VERIFY** whether outstation is actually offered by the operator — this is an open owner decision
  (`OWNER_DECISIONS.md` #17) and gates the whole outstation content set.
- The **BRANDED** class cannot be populated until a final name exists.
