# SCOUT — High-ticket local services, Hyderabad
Date: 2026-10-02 (UTC) · Scout: subagent · Status: COMPLETE (8 real businesses, 4 categories)
Full evidence-dense audits: ~/revenue-lab/ledgers/MICRO_AUDITS.md (Batch 1)
Method: public page fetches (curl raw HTML + web_extract + search snippets). Browser backend was down (Chromium libatk missing) — used HTTP fallback. Labels: OBSERVED / INFERRED / UNKNOWN. Prices = ESTIMATE unless cited.

## Businesses (2 per category)
(a) Real estate: 1. Vertex Homes (builder) · 2. Vishwa Properties (broker)
(b) Venues: 3. The Environ® – Convention · 4. The Vintage Palace
(c) Planners: 5. Weddin Events · 6. Yellow Planners
(d) Photographers: 7. Photriya Studios · 8. Suguru Weddings

## Headline findings (all OBSERVED, cited in ledger)
- The Vintage Palace: NO owned website (Justdial "Add Website"); ~7,900 Google reviews; booking only via aggregators; rigid 70%/30% non-refundable terms. [Justdial, Mandap]
- Yellow Planners: contact page click-to-call is BROKEN (`tel:+91` with no number); leads land in a personal Gmail + WhatsApp; review claims (200+ 5-star) vs 29–119 Justdial ratings. Founder Chunduri Phani public. [raw HTML, LBB, Justdial]
- Weddin Events: contact page has NO form (JS-only, "Please enable JavaScript"); homepage claims "550+ Google reviews" vs ~59/81/143 elsewhere. [raw HTML, addagio, nimntrn, Justdial]
- Suguru Weddings: JS-only site (~2 KB raw HTML, invisible to crawlers); contradictory "5+ years" vs "9+ years"; runs a Facebook Pixel (paid traffic) yet no working capture. [raw HTML, Justdial]
- Photriya Studios: no enquiry form; contact via a US phone + Gmail; stale (~7-yr-old) reviews; peak-season availability not bookable online. Founder Venky Mallojjala public. [raw HTML, Justdial, LBB]
- The Environ: good CF7 intake (date + guests) but manual callbacks, no availability calendar, no WhatsApp on site, a 2nd number elsewhere. [raw HTML, Justdial]
- Vishwa Properties: 8 forms on homepage + 3 more (/contact 404) = fragmented; WhatsApp + phone + email present; no pipeline. [raw HTML, housing.com]
- Vertex Homes: opaque PHP-mail forms (field31228…), no click-to-call, no booking calendar; Justdial review synthesis flags post-site-visit sales/CRM follow-up failures. [raw HTML, Justdial]

## Value of one lost enquiry/booking [ESTIMATE]
Builder (Vertex) ₹15–40L contribution per booking · Venue (Environ) ₹3–8L · Venue (Vintage Palace) ₹85k–₹2.45L · Planner (Weddin/Yellow) ₹2.5L+ fee · Broker (Vishwa) ₹80k–₹4L commission · Photographer ₹50k–₹2L.

## Repeating pains (standardisable product signal)
1. No online availability/date-hold for date-sensitive high-ticket services (8/8).
2. Enquiries in personal Gmail / WhatsApp / opaque mail with no auto-acknowledge or pipeline.
3. Inconsistent contact details + inflated review claims across surfaces (trust + capture loss).
4. Recurring negative reviews left unanswered.

## Priority for outreach (reachability x leak strength)
1) Yellow Planners (broken CTA + named founder) · 2) Vintage Palace (no website) · 3) Weddin Events · 4) Suguru · 5) Photriya · 6) Environ · 7) Vishwa · 8) Vertex.

## Caveats / gaps
- Browser automation failed this run; Google Business Profiles could not be opened directly — GBP links are Maps search deep-links, review counts come from Justdial/Wanderlog/aggregators (cross-checked where possible).
- No emails or contacts were invented. Contact confidences: MEDIUM–HIGH for Weddin, Yellow Planners, Photriya; MEDIUM for Environ, Vintage Palace, Suguru, Vishwa; LOW–MEDIUM for Vertex.
- Prices are ESTIMATE from public rate cards/portals (Justdial, Mandap, homznspace, WeddingBazaar); per-company spend NOT verified.
