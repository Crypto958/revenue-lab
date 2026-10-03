# BUSINESS_MODEL.md

**Subject:** How the Hyderabad group-travel business operates commercially — the funnel, the trip-request status model, own-vehicle prioritisation, and the partner-inventory rule.
**Prepared:** 2026-10-03 · **Status:** OPERATING DESIGN (internal).
**Companion documents:** `LEGAL_MODEL_GATE.md` (what we may lawfully do/claim) · `DATA_PRIVACY_CHECKLIST.md` (what we may collect and keep) · `FACTS_LEDGER.md` (what may be published).

> Everything customer-facing in this document is constrained by `LEGAL_MODEL_GATE.md` §4–§5. Where this document says "quote", "confirm" or "partner", read it together with the legal gate: **this is a quote-first, whole-vehicle private-hire model, not a ticketed bus service and not a live marketplace.**

---

## 1. One-line model

A **quote-first, whole-vehicle private group-travel service in Hyderabad**, anchored by one **17-seat Force Urbania**. Demand is qualified by a human, matched to supply, and quoted individually. Availability is **never shown live**. Third-party (partner) capacity, if used at all, is **sourced and verified per trip**, never displayed as inventory.

**What the business is**
- Pre-booked private group transport / vehicle hire **with driver**.
- Whole-vehicle hire for a group that travels together.
- A **quotation enquiry** service — not instant booking.

**What the business is *not***
- Not a bus route, not a stage carriage, not per-seat ticket sales.
- Not a live availability calendar or a multi-vehicle fleet listing.
- Not (currently) a licensed aggregator/marketplace, and not represented as one.

---

## 2. Stakeholders and roles

| Role | Who | Responsibility |
|---|---|---|
| **Owner-operator** | The owner | Owns and runs the Urbania; approves every quote; confirms or declines each trip; final call on partner sourcing. |
| **Enquiry handler** | Owner (initially) / a single trained person | Reads the enquiry, qualifies it, sources supply, prepares the quote, follows up. |
| **Partner operator** | Third-party commercial transport owner (only if/when used) | Provides a permitted, insured, fit vehicle and driver for a specific trip. Verified per trip (see §6). |
| **Customer / trip organiser** | The person who enquires | Supplies trip details; accepts the quote; the trip is completed; may leave a review. |

**Human-in-the-loop principle.** No automated tool may confirm availability, promise a vehicle, or state a price. Only the owner (or a named delegated person) may do so. This matches the site's existing rule that "submitting an enquiry does not confirm a booking."

---

## 3. The funnel

```
VISITOR  →  ENQUIRY  →  QUALIFICATION  →  SUPPLY MATCH  →  QUOTE
      →  BOOKING CONFIRMED  →  COMPLETED  →  REVIEW
```

### 3.1 Visitor
- Arrives from search, WhatsApp, referral, or direct.
- Sees only safe claims (route pages, guides, "request a quotation").
- **No prices, no live availability, no booking button.**

### 3.2 Enquiry
- The visitor submits the quote form (name, contact, trip type, date, group size, pickup/drop, notes) or calls/messages.
- The enquiry is captured with `source_page`, `submitted_at`, and any `utm_*`/`gclid` parameters (see `ANALYTICS_PLAN.md`).
- The system's job ends at capture; a **human** owns the next step.
- **An enquiry is not a booking** and must be labelled as such to the customer.

### 3.3 Qualification
A human answers three questions:
1. **Is this real, dated, and reachable?** (Real trip, real date, contactable organiser.)
2. **Is it a fit for a 17-seat whole-vehicle private hire?** (Group size, trip type, one-way/round-trip, outstation, wedding/event, corporate, sightseeing.)
3. **Is it within what we may lawfully do?** (In-permit geography; no per-seat ticketing; no promise of an unpermitted service — see `LEGAL_MODEL_GATE.md`.)

If it fails any test, it is gently declined or redirected (see status `LOST`).

### 3.4 Supply match
- **First:** can the **own Urbania** genuinely serve this trip? (see §5 — suitability test.)
- **Only if not:** can a **verified partner vehicle** serve it? (see §6 — partner rule.)
- The outcome sets the request status (`OWN_VEHICLE_POSSIBLE` / `PARTNER_SOURCING`).

### 3.5 Quote
- The owner prepares a **written quotation from the itinerary**, using the owner's confirmed commercial rules (rate basis, minimum km, overtime, night allowance, tolls/parking, driver allowance, payment terms, cancellation terms) — **none of which may be invented; they must come from the owner** (see `OWNER_DECISIONS.md`).
- The quote states clearly: it is a quotation, it is subject to confirmation, and submission of the enquiry did not create a booking.
- If a partner is being used, the quote must not misrepresent the vehicle as the own Urbania.

### 3.6 Booking confirmed
- The customer accepts in writing (message/email) **and** the owner confirms the vehicle + driver + date.
- Only now may the trip be called a **confirmed booking**.
- The customer is told what to expect (vehicle, driver contact, pickup time, what is included/excluded).

### 3.7 Completed
- Trip is performed. The customer's trip details are handled per `DATA_PRIVACY_CHECKLIST.md` (including the operator's own statutory trip records — see legal gate §1.3/§1.5).
- Any incident is recorded.

### 3.8 Review
- **Only after a completed trip**, and **only for a real customer**, may a review be requested or published.
- **No fabricated social proof, ever.** (This is an existing hard rule in `README.md`.)
- Published reviews must be genuine and consented to (see privacy doc).

---

## 4. Trip-request status model

Every enquiry becomes exactly one **trip request** with one current status. Statuses are a small, finite set so the owner can see the whole pipeline at a glance.

| Status | Meaning | Who sets it | Typical next status |
|---|---|---|---|
| `NEW` | Enquiry captured; no human has touched it yet. | System (on capture) | `QUALIFYING` or `LOST` |
| `QUALIFYING` | A human is assessing fit / reachability / lawfulness. | Handler | `OWN_VEHICLE_POSSIBLE`, `PARTNER_SOURCING`, `LOST` |
| `OWN_VEHICLE_POSSIBLE` | The own Urbania genuinely fits the trip (see §5). | Handler/Owner | `CUSTOMER_QUOTED`, `FOLLOW_UP`, `LOST` |
| `PARTNER_SOURCING` | Own vehicle not suitable/unavailable; a verified partner is being sourced. | Handler | `QUOTES_RECEIVED`, `LOST` |
| `QUOTES_RECEIVED` | One or more partner quotes are in hand (internal only — never shown to the customer as live inventory). | Handler | `CUSTOMER_QUOTED` |
| `CUSTOMER_QUOTED` | A written quotation has been sent to the customer. | Handler/Owner | `FOLLOW_UP`, `BOOKED`, `LOST` |
| `FOLLOW_UP` | Quoted but not yet decided; a follow-up is scheduled. | Handler | `BOOKED`, `LOST` |
| `BOOKED` | Customer accepted **and** owner confirmed vehicle+driver+date. | Owner | `COMPLETED`, `CANCELLED` |
| `LOST` | Not pursued, declined, out of scope, or went silent. | Handler | — (terminal) |
| `CANCELLED` | A booked trip was cancelled by either side. | Owner | — (terminal) |
| `COMPLETED` | Trip was performed. | Owner | (enables Review) |

**Transition rules**
- Only a **human** may move a request out of `NEW`.
- A request may only reach `BOOKED` after explicit customer acceptance **and** explicit owner confirmation of a specific vehicle and driver.
- `QUOTES_RECEIVED` is an **internal** state; partner quotes are never surfaced to the customer as availability.
- `LOST` and `CANCELLED` are terminal; a returning customer starts a **new** request (history is kept, but not reused).
- No status may imply live availability to a customer except `BOOKED` (and only for that specific trip).

---

## 5. Own-vehicle prioritisation rule

**Principle:** prefer the own Urbania **only when it genuinely suits the trip.** Never force the own vehicle onto a trip it cannot serve well, and never use the own vehicle as a reason to distort the quote.

The own vehicle is prioritised **only if all** of these are true:
1. **Capacity fit** — the group fits with comfortable seating for the stated passenger count, and luggage (measured, not assumed — see `FACTS_LEDGER.md` on luggage).
2. **Date/availability fit** — the own vehicle is not already committed and can do the trip without an unrealistic turnaround.
3. **Geography/permit fit** — the trip is within what the own vehicle is permitted to do (see `LEGAL_MODEL_GATE.md` §1.2/§1.3); no assumption that outstation/interstate is fine.
4. **Trip-type fit** — a whole-vehicle private group hire; not a per-seat/ticketed requirement.
5. **Economics fit** — the trip meets the owner's minimum commercial rules.

If any of these fails, the request moves to `PARTNER_SOURCING` rather than being force-fit to the own vehicle.

> **Anti-distortion rule:** the own vehicle is never described as "the only option", and partner capacity is never hidden merely to steer the booking to the own vehicle. The customer's needs decide.

---

## 6. Partner-inventory rule (never display live)

**Rule:** *Partner inventory is never displayed as live until verified.*

1. **No partner listing on the site.** No partner vehicles, photos, counts, prices, or "available now" indicators appear on the public site. The site shows one vehicle: the owner's Urbania [as a description, not as live stock].
2. **Per-trip sourcing.** A partner is contacted **for a specific request**, on a specific date, and only after the own vehicle has been ruled out.
3. **Verification before use.** Before a partner is offered to a customer, the handler must obtain and record, for that trip and that vehicle:
   - valid **permit**;
   - valid **certificate of fitness**;
   - valid **insurance** covering passenger carriage;
   - valid **PUC**;
   - a **driver** holding the correct transport-class licence (and badge, where required).
   > The *legal* sufficiency of these documents is addressed in `LEGAL_MODEL_GATE.md`; this document only fixes the **operating rule** that they must be seen and recorded, not assumed.
4. **No implied fleet.** The business never describes partner capacity as its own fleet or as a live network.
5. **Disclosure.** When a partner performs a trip, the customer is told, in the quote or confirmation, that the service may be performed by a verified third-party operator.
6. **Expiry control.** Verification documents are re-checked if they were near expiry at the time of the trip; a partner with lapsed documents is not used.
7. **Kill rule.** If a partner cannot evidence the documents above, the request is not served by that partner — it is re-sourced or declined.

**Why this rule exists:** partner inventory is unverified, so showing it "live" would (a) misrepresent capacity, and (b) potentially pull the business into representations the legal gate says it must not make today (`LEGAL_MODEL_GATE.md` §5).

---

## 7. Commercial rules the owner must supply (not to be invented)

These are blocking for quoting. Until the owner supplies them, the business cannot give a real quote — only a "we will confirm" response.

- Pricing basis (per km / per day / fixed), rate, and minimum kilometres.
- Overtime and night-allowance rules.
- Toll / parking / state-permit treatment (included or extra).
- Driver allowance (incl. outstation).
- Payment terms (advance % / on completion).
- Cancellation and refund policy.
- GST status and whether a tax invoice can be issued (see legal gate Q18–Q24).
- Whether any outstation/interstate trip is offered at all, and under what permit (see legal gate Q4, Q36).

*(Mirrors `OWNER_DECISIONS.md` and `DO_NOT_PUBLISH_UNTIL_VERIFIED.md`.)*

---

## 8. What the customer sees at each stage

| Stage | Customer sees | Customer must NOT be led to believe |
|---|---|---|
| Visitor | "Request a quotation." Trip pages and guides. | Availability, prices, or a booking button. |
| Enquiry submitted | "We have your enquiry; this is not a booking." | That a vehicle is held. |
| Qualification | A human reply asking for missing details. | That the trip is confirmed. |
| Quote | A written quotation from the itinerary. | That the quote is a booking, or that a partner vehicle is the owner's own. |
| Booking confirmed | Confirmation of vehicle + driver + date, with inclusions/exclusions. | Anything beyond the confirmed trip. |
| Completed | A genuine request for a review (optional). | Fake or incentivised social proof. |

---

## 9. Metrics (keep the funnel honest)

Primary: **qualified trip enquiries** (not sessions or page views).
Secondary: enquiry → quotation rate; quotation → booking rate; own-vehicle vs partner-vehicle share; completion rate; review rate (real reviews only).
Watched, not optimised: search impressions, guide readership.

No channel is credited without checking the source data (see `ANALYTICS_PLAN.md`).

---

## 10. Hard constraints inherited from the legal gate

1. Quote-first only; **no live availability, no per-seat sales, no instant booking**.
2. **No unverified claims** about permits, insurance, fitness, driver vetting, fleet, partner network, or GST.
3. **No operation on an unpermitted vehicle** and no use of the own permit for a partner's vehicle.
4. Operator statutory records (trip sheets / tourist lists / logbooks) are kept as the applicable rule requires — see `LEGAL_MODEL_GATE.md` §1.3/§1.5 and the questions there.
5. Customer personal data is handled under `DATA_PRIVACY_CHECKLIST.md`.
