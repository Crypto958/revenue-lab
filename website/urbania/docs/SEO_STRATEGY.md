# SEO / AEO STRATEGY

Date: 2026-10-03

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
