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
