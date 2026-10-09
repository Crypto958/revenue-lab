# FORM_LOGIC.md

Form lifecycle notes for the planner generated from `build_planner.py`.

## Submission lifecycle

1. **Client validation** — required fields scoped to the *active* trip mode only, plus the
   contact block. Failures focus the first bad field and flag it `.bad` (red border + message).
2. **Review step** — the customer sees trip details and can edit them. Reviewing does not send
   or store trip details.
3. **Consent and contact** — only after name, phone, and explicit privacy consent are supplied
   does the browser POST the complete request to `/api/trip`.
4. **Save and notify** — the function validates contact and consent, then stores the full
   request in Netlify Blobs. Once saved, it attempts a ZeptoMail owner alert containing only
   name, phone, trip type, route, date, group size, and reference. Mail failure does not undo
   the saved request.
5. **Confirmation or recovery** — a successful save shows the server reference and says the
   request is an enquiry, not a booking. A failed save shows no false confirmation and keeps
   the form available to retry, with a WhatsApp fallback.

**Field collection rule:** only fields belonging to the *selected* trip mode are collected, using
the visible label text as the key. Fields from other modes are never included — this was a real
defect that shipped in the first build and was fixed on 2026-10-03.

### Owner alert setup

Create a Zoho ZeptoMail Agent, authenticate the UrbanLoop sending domain, and verify the sender
address. Then add `ZEPTOMAIL_SEND_MAIL_TOKEN` and `ZEPTOMAIL_FROM_ADDRESS` as server-side
environment variables in Netlify. Do not put the token in site files or browser-visible settings.
Until both values are set, requests still save normally and email alerts remain off.

### City / Local  ·  CTA: “Find local options”  ·  date UI: single

Point-to-point travel inside Hyderabad, with optional stops.

- **row** — `pickup`, `destination` · 2 required
- **text** — `stops` · optional
- **row** — `date`, `start_time` · 1 required
- **select** — `duty, end_time` · 1 required
- **select** — `passengers, luggage` · 1 required

### Airport  ·  CTA: “Request airport options”  ·  date UI: single

Group arrivals and departures at Rajiv Gandhi International Airport.

- **chip group** — `airport_direction, airport_direction, airport_direction` · 3 required
- **row** — `airport`, `address` · all optional
- **text** — `flight_no` · optional
- **row** — `date`, `flight_time` · 1 required
- **select** — `passengers, cabin_bags` · 1 required
- **select** — `large_bags, return_leg` · 1 required

### Outstation  ·  CTA: “Check outstation options”  ·  date UI: range

Intercity and multi-day travel. Outstation trips depend on the permissions and arrangements that apply at the time — we confirm before quoting.

- **chip group** — `trip_shape, trip_shape, trip_shape` · 3 required
- **row** — `pickup`, `destinations` · 2 required
- **text** — `add_stop` · optional
- **select** — `return_date, overnight` · optional
- **select** — `passengers, luggage` · 1 required
- **text** — `est_km` · optional

### Wedding / Event  ·  CTA: “Plan my event transport”  ·  date UI: range

Guest movement across a wedding or event schedule.

- **select** — `guests, movement_pattern` · 2 required
- **chip group** — `event_needs, event_needs, event_needs, event_needs, event_needs, event_needs` · optional
- **row** — `main_pickup`, `venue` · all optional
- **text** — `extra_pickups` · optional
- **select** — `vehicles_known, date_from` · optional
- **text** — `schedule_notes` · optional

### Corporate  ·  CTA: “Request corporate transport”  ·  date UI: range

Teams, delegations and scheduled movement across a visit.

- **row** — `company`, `team_size` · 1 required
- **row** — `duty_window`, `date_from` · all optional
- **text** — `return_date` · optional
- **row** — `pickup`, `destination` · all optional
- **text** — `stops` · optional
- **chip group** — `corporate_needs, corporate_needs, corporate_needs, corporate_needs, corporate_needs` · optional
- **select** — `invoice_requirement` · optional

### Sightseeing / Day Trip  ·  CTA: “Request day trip quote”  ·  date UI: range

Multi-stop city travel on your own itinerary. Transport only — no guides or tickets.

- **row** — `pickup`, `start_time` · 1 required
- **text** — `itinerary` · optional
- **select** — `duration, passengers` · 2 required
- **chip group** — `route_help, route_help` · optional

### Family Trip  ·  CTA: “Plan family trip”  ·  date UI: range

Family groups travelling together, including children and luggage.

- **row** — `pickup`, `destination` · 2 required
- **text** — `stops` · optional
- **row** — `adults`, `children` · all optional
- **row** — `date_from`, `return_date` · all optional
- **select** — `luggage` · optional

### Custom  ·  CTA: “Tell us your plan”  ·  date UI: range

Anything that does not fit the other modes. Describe it and we will work out what is needed.

- **text** — `plan` · optional
- **row** — `pickup`, `date_from` · 1 required
- **row** — `return_date`, `passengers` · 1 required
- **text** — `stages` · optional

## Vehicle preference

One chip group, added to every mode: **Force Urbania (17 seats)** or **Recommend one for my group**.
Preference is a request. It is never presented as availability, and the Urbania page states this
explicitly where the preference is offered.

## Attribution carried through the form

`source_page`, `submitted_at` (ISO 8601), and `utm_source`, `utm_medium`, `utm_campaign`,
`utm_term`, `utm_content`, `gclid` when present. Stored server-side on the trip record so a lead
can be traced to its channel even before analytics exists.

## Not collected, deliberately

No address book access, no location permission, no payment details, no ID documents, no
date of birth. Nothing beyond what is needed to quote the trip.
