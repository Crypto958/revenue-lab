# OWNER DECISIONS

Items only the owner can decide. None of these block the build; each blocks publication.
Last updated: 2026-10-03

## Blocking publication

| # | Decision | Current state | Why it matters |
|---|---|---|---|
| 1 | Final business name | Working name `Urbania Hyderabad`. Independent analysis scores four directions: **"Hyderabad Group Travel" 3.90** > GaadiGang 3.85 > GatherSafar 3.80 > `Urbania Hyderabad` 3.35 > **`togALLther` 2.80** | Appears in logo, footer, titles and schema — and determines the domain. `togALLther` is **not recommended** (ambiguous pronunciation, misspelling when dictated, fights mobile autocorrect, reads informal to corporate/wedding buyers). Full scoring: `BRAND_DECISION.md` |
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
