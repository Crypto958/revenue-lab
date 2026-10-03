# QA REPORT — independent red-team pass

Date: 2026-10-03 · Method: automated source scanning + build validation + live HTTP checks + browser DOM testing.

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
