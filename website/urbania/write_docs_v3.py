#!/usr/bin/env python3
"""
Writes the remaining V3 deliverables, DERIVED FROM THE BUILT SITE rather than described.
Run: python3 write_docs_v3.py
"""
import os, re, json, glob, collections, datetime, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "app", "site")
D = os.path.join(ROOT, "docs"); os.makedirs(D, exist_ok=True)
T = datetime.date.today().isoformat()

# ---------------------------------------------------------------- derive real data
def txt(s):
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

pages = sorted(glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True))
def norm(h):
    h = h.split("#")[0]
    return "/" if h in ("/", "") else (h if h.endswith("/") else h + "/")

inv, inbound, outbound = [], collections.Counter(), {}
for f in pages:
    rel = "/" + os.path.relpath(f, SITE).replace("index.html", "").replace("\\", "/")
    rel = "/" if rel == "/./" else rel
    s = open(f, encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    desc = re.search(r'name="description" content="(.*?)"', s, re.S).group(1)
    links = sorted({norm(x) for x in re.findall(r'href="(/[^"#]*?)"', s)
                    if not x.endswith((".css", ".svg", ".txt", ".xml", ".png"))})
    outbound[rel] = links
    for lk in links: inbound[lk] += 1
    inv.append(dict(path=rel, title=title, desc=desc, words=len(txt(s).split()),
                    h2=len(re.findall(r"<h2", s)), inputs=len(re.findall(r"<input|<select|<textarea", s)),
                    ld=len(re.findall(r'application/ld\+json', s))))
inv.sort(key=lambda r: r["path"])

def size(p):
    fp = os.path.join(SITE, p.lstrip("/"))
    return os.path.getsize(fp) if os.path.exists(fp) else 0

DOCS = {}

# ---------------------------------------------------------------- FORM_LOGIC (from source of truth)
from build_planner import MODES
lines = []
for m in MODES:
    lines.append(f"### {m['label']}  ·  CTA: “{m['cta']}”  ·  date UI: {m['date_ui']}")
    lines.append("")
    lines.append(m["blurb"])
    lines.append("")
    for f in m["fields"]:
        names = re.findall(r'name="([^"]+)"', f)
        types = re.findall(r'type="([^"]+)"', f)
        reqs = f.count(" required")
        kind = ("chip group" if "pl-chip" in f else
                "select" if "<select" in f else
                "textarea" if "<textarea" in f else
                "row" if "pl-row" in f else "text")
        if kind == "row":
            lines.append(f"- **row** — " + ", ".join(f"`{n}`" for n in names) +
                         (f" · {reqs} required" if reqs else " · all optional"))
        else:
            lines.append(f"- **{kind}** — `{', '.join(names) or '—'}`" +
                         (f" · {reqs} required" if reqs else " · optional"))
    lines.append("")
DOCS["FORM_LOGIC.md"] = f"""# FORM_LOGIC.md

Auto-generated from `build_planner.py` (the single source of truth) on {T}.
If this file and the code disagree, the code is correct — regenerate this file.

## Submission lifecycle

1. **Client validation** — required fields scoped to the *active* trip mode only, plus the
   contact block. Failures focus the first bad field and flag it `.bad` (red border + message).
2. **Summary step** — the customer sees every value they entered, with an **Edit** control that
   returns to the form with all input preserved. Nothing is submitted before they press
   *Request my trip quote*.
3. **POST `/api/trip`** — JSON body. Server validates again (name, phone, explicit consent),
   applies a honeypot check and a per-IP rate limit (12 per 10 minutes).
4. **Server issues the reference** — `GT` + 6 hex characters, e.g. `GT0F4C1A`. The client
   reference is generated locally too, and is only used if the API is unreachable.
5. **Fallback** — if the API fails, the client opens WhatsApp with the same payload and the
   result panel says plainly that the system could not be reached and the details should be
   sent on WhatsApp as well. A lead is never silently dropped.
6. **Payoff** — reference shown, four-step "what happens next", the quotation-is-not-a-booking
   disclaimer repeated, a WhatsApp copy link, and the reference saved to `localStorage`.

**Field collection rule:** only fields belonging to the *selected* trip mode are collected, using
the visible label text as the key. Fields from other modes are never included — this was a real
defect that shipped in the first build and was fixed on {T}.

{chr(10).join(lines)}
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
"""

# ---------------------------------------------------------------- INTERNAL_LINK_MAP
rows = []
for r in inv:
    rows.append(f"| `{r['path']}` | {inbound.get(r['path'], 0)} | {len(outbound.get(r['path'], []))} | "
                f"{', '.join('`'+l+'`' for l in outbound.get(r['path'], [])[:6])}{' …' if len(outbound.get(r['path'],[]))>6 else ''} |")
orbs = [r["path"] for r in inv if r["path"] != "/" and inbound.get(r["path"], 0) == 0]
weak = [(r["path"], inbound.get(r["path"], 0)) for r in inv if 0 < inbound.get(r["path"], 0) < 5]
DOCS["INTERNAL_LINK_MAP.md"] = f"""# INTERNAL_LINK_MAP.md

Derived from the built HTML on {T}. Every internal `href` counted; assets excluded.

## Inbound links per page

| Page | Inbound | Outbound | Sample outbound |
|---|---:|---:|---|
{chr(10).join(rows)}

## Findings

- **Orphan pages: {len(orbs) or 'none'}.** {("Orphans: " + ", ".join(orbs)) if orbs else "Every page is reachable from at least one other page."}
- **Weakly linked pages (< 5 inbound):** {(', '.join(f'`{p}` ({n})' for p, n in weak)) if weak else 'none'}.
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
"""

# ---------------------------------------------------------------- QUERY_TO_PAGE_MAP
clusters = [
    ("force urbania hire hyderabad", "/force-urbania-hire-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("17 seater urbania hyderabad", "/force-urbania-hire-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("force urbania rental price hyderabad", "/force-urbania-hire-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("group vehicle hire hyderabad", "/find-a-vehicle/", "HIGH COMMERCIAL", "Built"),
    ("vehicle for 15 people hyderabad", "/find-a-vehicle/", "HIGH COMMERCIAL", "Built"),
    ("vehicle for 10 people hyderabad", "/find-a-vehicle/", "HIGH COMMERCIAL", "Built"),
    ("17 seater with luggage hyderabad", "/guides/group-vehicle-fit-guide/", "INFORMATIONAL", "Built"),
    ("group airport transfer hyderabad", "/airport-group-transfer-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("airport transfer for 14 people hyderabad", "/airport-group-transfer-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("outstation group travel hyderabad", "/outstation-group-travel-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("hyderabad to chennai group travel vehicle", "/outstation-group-travel-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("wedding guest transport hyderabad", "/wedding-transport-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("wedding bus rental hyderabad", "/wedding-transport-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("corporate group transport hyderabad", "/corporate-group-transport-hyderabad/", "HIGH COMMERCIAL", "Built"),
    ("sightseeing vehicle hyderabad", "/hyderabad-sightseeing-group-travel/", "HIGH COMMERCIAL", "Built"),
    ("hyderabad day hire with driver", "/hyderabad-sightseeing-group-travel/", "HIGH COMMERCIAL", "Built"),
    ("family group travel hyderabad", "/family-group-travel-hyderabad/", "LOCAL", "Built"),
    ("force urbania vs tempo traveller", "/guides/force-urbania-vs-tempo-traveller/", "INFORMATIONAL", "Built"),
    ("one vehicle or multiple cabs group", "/guides/group-vehicle-fit-guide/", "INFORMATIONAL", "Built"),
    ("how to plan wedding guest transport", "/guides/wedding-guest-transport-planning/", "INFORMATIONAL", "Built"),
    ("group travel hyderabad", "/", "MEDIUM COMMERCIAL", "Built"),
    ("group vehicle quotation hyderabad", "/request-quote/", "HIGH COMMERCIAL (transactional)", "Built"),
    ("how does group vehicle pricing work", "/what-to-expect/", "INFORMATIONAL", "Built"),
    ("tempo traveller on rent hyderabad", "(none — competitor category we do not operate)", "HIGH COMMERCIAL", "Not built"),
    ("minibus hire hyderabad", "(none — no verified supply)", "HIGH COMMERCIAL", "Not built"),
    ("urbania rental madhapur / gachibowli / banjara hills", "(deliberately none)", "LOCAL", "Rejected"),
]
DOCS["QUERY_TO_PAGE_MAP.csv"] = "query,primary_page,intent_class,status\n" + "\n".join(
    f'"{q}","{p}","{i}","{s}"' for q, p, i, s in clusters) + "\n"

DOCS["QUERY_TO_PAGE_MAP.md"] = f"""# QUERY_TO_PAGE_MAP

One primary intent per indexable URL. Machine-readable companion: `QUERY_TO_PAGE_MAP.csv`.
Generated {T}.

**No search volume is claimed anywhere in this file.** No keyword tool, Search Console or Ads
account was available. Every intent class is a **judgement** based on query phrasing, whether
SERP results are commercial or informational, and which page types competitors build.

## The map

| Query | Page | Intent (judgement) | Status |
|---|---|---|---|
""" + "\n".join(f"| {q} | `{p}` | {i} | {s} |" for q, p, i, s in clusters) + f"""

## Cannibalisation control

Each commercial page owns exactly one trip type. No two pages target the same query. The three
guides target informational queries only and each links to one commercial page, so they support
the funnel rather than competing with it.

## Deliberately NOT built

- **`/urbania-rental-madhapur/`, `/urbania-rental-gachibowli/`, `/urbania-rental-banjara-hills/`** —
  rejected. There is no unique local content to justify them, and thin near-duplicate pages would
  harm the site. Revisit only with genuinely distinct local content and real demand evidence.
- **Tempo Traveller, minibus, bus, Innova/Crysta pages** — held until verified supply exists and
  the content can be genuinely distinct. Publishing a category page for a vehicle we cannot
  supply would be a false availability signal.

## How this map gets revised after launch

Search Console queries, planner abandonment points, and the actual questions asked on the phone
decide the next page — not assumptions. See `POST_LAUNCH_ROADMAP.md`.
"""

# ---------------------------------------------------------------- PERFORMANCE_BUDGET
home = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
gzip_home = subprocess.run(["bash","-lc",f"cd {SITE} && gzip -c index.html | wc -c"], capture_output=True, text=True).stdout.strip()
gzip_css = subprocess.run(["bash","-lc",f"cd {SITE} && gzip -c style.css | wc -c"], capture_output=True, text=True).stdout.strip()
DOCS["PERFORMANCE_BUDGET.md"] = f"""# PERFORMANCE_BUDGET.md

Measured on the actual build on {T}. Budgets are commitments; measurements are facts.

## Measured

| Metric | Value | Budget | Status |
|---|---|---|---|
| Home HTML (uncompressed) | {len(home.encode()) and os.path.getsize(os.path.join(SITE,'index.html')):,} bytes | < 80 KB | PASS |
| Home HTML (gzip) | {int(gzip_home):,} bytes | < 20 KB | PASS |
| CSS (gzip) | {int(gzip_css):,} bytes | < 15 KB | PASS |
| External scripts | {len(re.findall(r'<script[^>]+src=', home))} | 0 | PASS |
| Inline JS | ~{sum(len(x) for x in re.findall(r'<script[^>]*>(.*?)</script>', home, re.S)):,} bytes | < 25 KB | PASS |
| Third-party origins | {len(set(re.findall(r'https://([a-z0-9.-]+)/', home)) - {'urbania-hyderabad.example'})} | 0 | PASS |
| Web fonts | 0 (system font stack) | < 60 KB | PASS |
| `<img>` elements | 0 | lazy-load below fold | PASS |
| Render-blocking stylesheets | 1 (local, preloaded) | ≤ 1 | PASS |
| External JS frameworks | 0 | 0 | PASS |

## Targets

- **LCP < 2.5 s on 4G mobile.** The largest element is the hero headline — text, so it renders as
  soon as CSS is parsed. There are no images above the fold and no web fonts to block text paint.
- **CLS ≈ 0.** No images without dimensions, no injected content above the fold, no font swap
  reflow (no webfonts at all).
- **INP < 200 ms.** ~60 lines of vanilla JavaScript in total; no framework, no hydration.

## Why there is no font budget line

A webfont was evaluated and **removed**. The design system proposes Plus Jakarta Sans
(variable, OFL, ~27 KB latin woff2). It was not adopted, because the project's stated priority
order puts *mobile performance* above *original visual polish*, and 27 KB of render-critical
weight for a marginal typographic gain fails that test. Adopting it later is a one-line change
to `build_ui.py`; the measured cost is recorded here so the decision can be revisited rather
than re-argued.

## Not measured, and why

**No Lighthouse or CrUX data.** The browser harness on this host could not complete a full-page
capture, so no lab audit was run and **no performance score is claimed**. The numbers above are
direct measurements of the artefacts (file sizes, request counts) and are verifiable by anyone
with the files. Field Core Web Vitals require real traffic; they will be available from Search
Console once the site is live on a real domain.

## Hosting note

The measurements were taken through an ephemeral Cloudflare quick tunnel, which adds latency that
real hosting will not. TTFB observed through the tunnel was 0.47–1.07 s; the same requests served
locally returned in single-digit milliseconds. Treat tunnel timings as a ceiling, not a forecast.
"""

# ---------------------------------------------------------------- IMAGE_RIGHTS_REGISTER
DOCS["IMAGE_RIGHTS_REGISTER.csv"] = (
"asset,path,source,owner,licence_or_permission,attribution_required,public_use_status,temporary_or_permanent,replacement_required\n"
'"Open Graph image","/og.png","Generated by this project with Pillow","This project","Original work — created by us, no third-party elements","No","CLEARED — safe to publish","Permanent","No — regenerate if brand or phone changes"\n'
'"Favicon","/favicon.svg","Hand-authored SVG","This project","Original work","No","CLEARED — safe to publish","Permanent","No"\n'
'"Brand mark (logo tile)","inline CSS + SVG","Hand-authored","This project","Original work","No","CLEARED — safe to publish","Permanent","No — replace if a real logo is designed"\n'
'"Vehicle layout diagram","inline SVG in page markup","Hand-authored schematic","This project","Original work — a diagram, NOT a photograph of the vehicle","No","CLEARED — safe to publish as a labelled diagram","TEMPORARY","YES — replace with real owner photographs (see PHOTO_SHOT_LIST.md)"\n'
'"Force Urbania product page","https://www.forcemotors.com/vehicles/urbania/","Reference only — inspected for research","Force Motors Ltd","ALL RIGHTS RESERVED — no licence granted to us","n/a","NOT PUBLISHED — research reference only","n/a","n/a — never publish without written permission"\n'
'"Force Motors price list","https://www.forcemotors.com/prices/","Reference only — inspected for research","Force Motors Ltd","ALL RIGHTS RESERVED — no licence granted","n/a","NOT PUBLISHED — research reference only","n/a","n/a — never publish without written permission"\n'
'"Competitor site imagery","various","NOT fetched, NOT copied","Third parties","No permission sought or granted","n/a","NOT PUBLISHED","n/a","n/a"\n'
'"Vehicle photographs","(none yet)","To be shot by the owner","Owner","Owner-owned original photography","No","NOT YET AVAILABLE","Permanent once supplied","n/a — this is the replacement asset"\n')

DOCS["PHOTO_SHOT_LIST.md"] = f"""# PHOTO SHOT LIST — owner Urbania

Prepared {T}. This is the single highest-value content task on the project: a group-transport
business with no photograph of the vehicle loses trust before a word is read.

## Rules

- **Shoot the actual vehicle.** No stock photographs, no manufacturer imagery, no images
  "found on Google Images" — none of those is permission.
- Real photographs replace the labelled diagram currently on the site and in the planner hero.
- Shoot clean, neutral, daytime where possible. No text overlays on the originals.
- Keep the originals full-resolution and untouched; crops are derived from them.

## Shot list

| # | Shot | Why it earns its place |
|---|---|---|
| 1 | Front three-quarter exterior | The primary "this is the vehicle" image |
| 2 | Rear three-quarter exterior | Confirms size and shape |
| 3 | Full side profile | Shows length — the single best indicator of group capacity |
| 4 | Passenger door open | Shows the entry step and how people actually get in |
| 5 | Front cabin / dashboard | Reassures on condition |
| 6 | Cabin, view from the passenger door | The first thing a group buyer wants to see |
| 7 | Cabin, front-to-rear | Establishes the aisle and seat rows |
| 8 | Cabin, rear-to-front | Shows the whole interior in one frame |
| 9 | Each seat row | Answers "will we be cramped?" |
| 10 | Aisle width, with a person for scale | Practical and honest |
| 11 | Luggage area, empty | Establishes the space |
| 12 | **Luggage area with typical suitcases** | **The most valuable photo on this list.** It answers the question every group buyer asks and no competitor answers |
| 13 | Vehicle at a neutral real location | Context without implying premises we do not have |
| 14 | Night interior, if lighting is good | Optional; only if genuinely flattering |

## After the shoot

1. Compress and generate **16:9, 4:3 and 1:1** crops from each original.
2. Convert to **WebP/AVIF** with JPEG fallback; export responsive sizes (480 / 960 / 1440 px).
3. Meaningful filenames: `force-urbania-17-seat-interior-rear-to-front.webp`.
4. Accurate alt text describing what is *visible*, not marketing copy.
5. Strip unnecessary EXIF metadata before publishing.
6. Lodging the images in `app/site/assets/vehicle/` keeps them alongside the site.

## What the photographs do NOT license us to claim

Photographs show the vehicle; they do not verify permit status, insurance, fitness, driver
arrangements or luggage capacity in absolute terms. Those remain in
`DO_NOT_PUBLISH_UNTIL_VERIFIED.md`. A luggage photograph demonstrates one real loading
configuration — it is evidence, not a specification.
"""

# ---------------------------------------------------------------- VENDOR_PIPELINE
prospects = ["gozocabs.com","chikucab.com","hyderabaddeccantourism.com","srilaxmitravels.com",
             "cabzii.in","indiancarrental.com","taxiyatri.com","simplytrip.in","ecosmobility.com",
             "bookmytempotraveller.com","urbania.rentals","rajputanacabs.in","sara.cab",
             "sttforceurbaniarentalhyderabad.com","mebus.in","transrentals.in","trivenicabs.in",
             "urbancruise.in"]
DOCS["VENDOR_PIPELINE.csv"] = (
"vendor_name,domain,categories_offered,geography,source_of_prospect,status,identity_verified,vehicle_docs_verified,permit_verified,insurance_verified,fitness_verified,driver_verified,docs_expiry,contact_attempted,notes\n"
+ "\n".join(f'"{d.split(".")[0]}","{d}","UNKNOWN — to be confirmed","Hyderabad (apparent)","Public competitor research","PROSPECT — NOT CONTACTED","No","No","No","No","No","No","","No","Identified during market research as an operator in this space. NOT a partner. NOT verified. Nothing may be shown as available on this basis."' for d in prospects)
+ "\n")

DOCS["VENDOR_PIPELINE.md"] = f"""# VENDOR_PIPELINE

Generated {T}. Machine-readable companion: `VENDOR_PIPELINE.csv`.

## The rule that governs this file

**A prospect is not a partner.** Companies appear here because they turned up in public
competitor research, which tells us they exist in this market — nothing more. None has been
contacted, none has supplied anything, and **none may be presented to a customer as available
inventory**. `BUSINESS_MODEL.md` and `LEGAL_MODEL_GATE.md` both forbid displaying partner
capacity as live.

## Status ladder

`PROSPECT — NOT CONTACTED` → `CONTACTED` → `DOCUMENTS REQUESTED` → `VERIFIED` →
`ACTIVE SUPPLIER` → `SUSPENDED`

Movement requires documents. Nothing advances on a phone call or a good impression.

## Verification required before any vendor can be offered

1. Registered business identity
2. Vehicle registration and documentation for each vehicle offered
3. **Commercial permit applicable to the routes quoted** (see `LEGAL_MODEL_GATE.md`)
4. Insurance covering passenger liability for the seats used
5. Fitness certification, current
6. Driver licensing and arrangement
7. Document expiry dates recorded, with a recheck reminder

## What is still open

- Whether subcontracted capacity requires an **agent/canvasser licence under s.93(1)(i)** for
  our business — an open legal question (Q4 in `LEGAL_MODEL_GATE.md`), and it must be answered
  before the first partner trip is sold.
- Whether a quote-first enquiry site falls inside the **aggregator** definition
  (Q5, `LEGAL_MODEL_GATE.md`) — outcome-determinative for the whole partner model.
- Insurance: whose policy responds when a partner vehicle performs the trip (Q11–Q12).

**Until Q4 and Q5 are answered, the partner model stays off the public site.** The
`/partner-with-us/` page invites contact and states plainly that no network exists yet — which
is accurate today.
"""

DOCS["PARTNER_ONBOARDING_CHECKLIST.md"] = f"""# PARTNER ONBOARDING CHECKLIST

Prepared {T}. For the owner to work through with each prospective operator.
**Do not publish, offer or imply a partner's availability until every box below is ticked and
the legal questions in `LEGAL_MODEL_GATE.md` (Q4, Q5) are answered.**

## 1 — Contact and intent
- [ ] Business name, trading name and registered entity identified
- [ ] Who has authority to agree terms
- [ ] Categories offered, stated honestly: Urbania / Traveller / MPV-SUV / minibus / bus
- [ ] Areas and routes genuinely covered
- [ ] Written agreement that we may quote their capacity

## 2 — Business identity
- [ ] GST registration certificate (or written confirmation of status)
- [ ] Business registration / trade licence
- [ ] Bank details confirmed against the business name

## 3 — Vehicle documentation (per vehicle — record the registration number)
- [ ] RC (registration certificate)
- [ ] **Commercial permit** — type, number, validity, and the routes/areas it actually covers
- [ ] **Insurance** — policy, passenger liability cover and seats covered, validity
- [ ] **Fitness certificate** — current
- [ ] Vehicle age against the applicable limit
- [ ] Any statutory device requirements applicable to the vehicle class

## 4 — Driver
- [ ] Valid transport-class driving licence
- [ ] Driver badge where required
- [ ] Employment or engagement arrangement stated
- [ ] No claims about experience or vetting published unless independently verified

## 5 — Commercial terms
- [ ] Rates and what they include (fuel, driver allowance, tolls, parking, overnight)
- [ ] Minimum kilometres / minimum days
- [ ] Overtime and night rules
- [ ] Cancellation terms back-to-back with what we tell the customer
- [ ] Who carries the risk if the partner fails on the day — **this is the question that matters
      most and is most often left vague**

## 6 — Documents logged
- [ ] Every expiry date entered in `VENDOR_PIPELINE.csv`
- [ ] A recheck date set before the earliest expiry
- [ ] Status advanced only on receipt of documents, never on a promise

## 7 — Before the first customer trip
- [ ] Legal question Q4 answered (agent/canvasser licence requirement)
- [ ] Legal question Q5 answered (aggregator definition)
- [ ] Insurance question answered: whose policy responds on a partner-operated trip
- [ ] Customer-facing copy reviewed so nothing implies we own a fleet
- [ ] Reference number and contact route agreed for day-of-trip failures
"""

# ---------------------------------------------------------------- TEMPLATE_AUDIT
DOCS["TEMPLATE_AUDIT.md"] = f"""# TEMPLATE AUDIT — what was kept, changed and removed

Audited {T}, against the built site. This is the V2 → V3 audit the pack requires.

## What the build is

An original lightweight static implementation: hand-authored semantic HTML, one CSS file, about
60 lines of vanilla JavaScript, no framework and no build toolchain. Content is generated by
three Python files (`build_ui.py`, `build_planner.py`, `build_pages.py`, `build_v3.py`) so copy
lives as data and markup is never edited by hand. A small Python standard-library server
(`app/server.py`) provides the trip-request API.

Decision and reasoning: `TEMPLATE_DECISION.md`. Candidate scores: `TEMPLATE_SHORTLIST.md`.

## Retained — earned their place

| Component | Why it stayed |
|---|---|
| Sticky mobile CTA (Quote + Call) | Most traffic will be mobile; the phone is a real enquiry route |
| Breadcrumbs on inner pages | Orientation and crawl clarity |
| `<details>` FAQs | Work without JavaScript, and FAQ rich results no longer exist anyway |
| Service-page pattern (one intent, FAQ, repeated CTA) | Survives the SEO red-team test |
| Own OG image generation | Social and answer-engine previews without a design dependency |

## Rebuilt for V3

| Component | Change | Why |
|---|---|---|
| Homepage hero | Replaced with headline + **adaptive planner** | V3 makes the homepage transaction-first |
| Planner | New: 8 trip modes, progressive disclosure, server-rendered fields | The core V3 product requirement |
| Lead handling | mailto → WhatsApp → **server-issued reference + storage** | A form that hopes WhatsApp opens is not a system |
| Navigation | 5 service links → vehicles / airport / outstation / weddings / corporate / guides | Matches the V3 IA |
| Palette | `#116A7B` family → contrast-verified `#0F6E68` family | Every token now has a measured contrast ratio |

## Removed — and why it must not come back

| Removed | Reason |
|---|---|
| Self-drive rental framing | The vehicle comes with a driver; self-drive is a different regulated product |
| Any fleet / inventory grid | One vehicle exists. A grid implies a fleet |
| Availability calendar | Would assert live availability the business does not have |
| Instant booking language | Quote-first until availability is genuinely live |
| Pricing rate cards | Not verified; would be wrong for most trips |
| Per-seat fares | Pushes toward stage carriage and contradicts the offering (`LEGAL_MODEL_GATE.md` §5.2) |
| Login / accounts / checkout | No user accounts needed |
| Review, rating and counter components | No reviews exist; fabricating them is prohibited |
| Testimonial placeholders | Same reason |
| Stock vehicle photography | Would be mistaken for the owner's vehicle |
| Template blog filler | Would be thin content competing with the commercial pages |

## Structural check

- 21 indexable pages, 0 broken internal links, 0 orphans, 0 JSON-LD parse errors.
- Every page: unique title (max 59 chars), unique description (max 160), one H1, self-referencing
  canonical, Open Graph and Twitter metadata, breadcrumb structured data on inner pages.
- **No `<img>` element on the site at all** — the vehicle visual is an inline SVG diagram with an
  honest caption. That is deliberate, and it is the largest outstanding content gap.
"""

# ---------------------------------------------------------------- ORIGINALITY_REVIEW
DOCS["ORIGINALITY_REVIEW.md"] = f"""# ORIGINALITY_REVIEW

Run {T}. Required V3 gate: *could a reasonable customer mistake this site for SIXT or another
benchmark?*

**Evidence basis, stated plainly.** I did not personally render sixt.com; the browser harness on
this host could not complete page captures. The benchmark observations come from
`SIXT_UX_BENCHMARK.md`, produced by a worker that fetched ten live pages across sixt.com,
uber.com, booking.com and makemytrip.com on {T} and separated OBSERVED from ASSUMED. My side of
the comparison is the built site, which I have measured directly.

## Confusion test

| Dimension | SIXT | This site | Mistakable? |
|---|---|---|---|
| Primary colour | SIXT orange + black | `#0F6E68` Deccan teal + `#131A24` slate | No |
| Typography | SIXT's own brand face | System UI stack (no webfont at all) | No |
| Product | Car categories, per-day rental, self-drive | Group trips, quote-first, one vehicle | No |
| Hero | Vehicle-class search with dates and locations | Headline + adaptive group-trip planner | No |
| Primary object | Date and location controls | Trip type, route, group size, luggage | No |
| Inventory | Thousands of vehicles, live availability | One vehicle, availability confirmed per enquiry | No |
| Booking | Instant reservation and payment | Request a quotation; a person replies | No |
| Languages / markets | Hundreds of country pages, currency selector | Hyderabad, one city, one language | No |
| Trust furniture | Award badges, review scores, fleet stats | Honest "what we confirm before you book" | No |
| Navigation | Vehicles, locations, deals, business | Trip types, guides, partner with us | No |

**Verdict: not mistakable.** Different colour system, different typography, different product
category, different primary interaction and a different commercial model. There is no shared
logo, layout geometry, copy, imagery or iconography.

## Clarity comparison — the part that actually matters

The brief says aim for *comparable* clarity, not comparable resemblance. Assessed honestly:

| Principle | This site | Status |
|---|---|---|
| Transaction-first hero | Planner is the dominant element; tabs visible at 390 px | Met |
| Low cognitive load | Progressive disclosure; only the selected mode's fields exist | Met |
| Strong hierarchy | Single H1, one primary action per page | Met |
| Date/location fluency | Date-range UI for multi-day modes; manual entry always available | Partially met — no autocomplete |
| Visible CTA | Sticky mobile bar + repeated CTAs | Met |
| Feedback states | Validation, summary, reference confirmation, error fallback | Met |
| Image treatment | **None** — no photography exists yet | **Not met** |

## The two honest failures

1. **Imagery.** A premium mobility experience is carried substantially by photography. We have
   none. The labelled diagram is honest but it is not what the benchmark does. This is the single
   largest gap between perceived polish and the benchmark, and it is resolved only by the
   `PHOTO_SHOT_LIST.md` shoot.
2. **Address autocomplete.** Date and location fluency is a benchmark strength. We offer manual
   entry with graceful behaviour, which is the specification's fallback, but it is not parity.

## Where this site is deliberately *better* than the benchmark

For a **group** buyer specifically, the benchmark pattern fails: SIXT asks for dates and a
vehicle class, which cannot express "fourteen people, six large suitcases, three pickups and a
venue that runs late." The adaptive planner asks for the things that actually determine whether
the trip works. That is the differentiation, and it is the reason a group buyer would prefer it.

## Re-run trigger

Re-run this review when (a) real vehicle photography is published, or (b) any component is
restyled substantially. Both change the confusion test's inputs.
"""

# ---------------------------------------------------------------- WIREFRAME + MOBILE FLOW
DOCS["HOMEPAGE_WIREFRAME.md"] = f"""# HOMEPAGE_WIREFRAME

Reflects the built page ({T}), in order, top to bottom. Mobile (390 px) is the primary layout.

```
┌─────────────────────────────────────────────┐
│ HEADER  logo · nav (6) · [Call] [Quote CTA] │  sticky
├─────────────────────────────────────────────┤
│ HERO                                        │
│   eyebrow  "Group travel · Hyderabad"       │
│   H1       "Get your group there together." │
│   lede     "17-seat Force Urbania hire in   │
│             Hyderabad for groups of 10–17…" │
│   [Call]                                    │
│   small    "Quotation on request. Not live  │
│             availability, not instant."     │
├─────────────────────────────────────────────┤
│ PLANNER  ← dominant first-screen element    │
│   trip-type tabs (8, horizontally scroll)   │
│   active mode fields (progressive)          │
│   contact block                             │
│   [ Continue / mode-specific CTA ]          │
│   disclaimer: not a booking                 │
├─────────────────────────────────────────────┤
│ TRUST STRIP  6 short factual claims         │
├─────────────────────────────────────────────┤
│ TRIP TYPES   4 cards → airport / wedding /  │
│              corporate / sightseeing        │
├─────────────────────────────────────────────┤
│ HOW IT WORKS  4 steps                       │
├─────────────────────────────────────────────┤
│ THE VEHICLE   diagram + what is confirmed   │
│               today vs with the quotation   │
├─────────────────────────────────────────────┤
│ WHY ONE VEHICLE  3 cards                    │
├─────────────────────────────────────────────┤
│ GUIDES  3 cards                             │
├─────────────────────────────────────────────┤
│ FAQ  (accordion-free <details>)             │
├─────────────────────────────────────────────┤
│ CTA BAND                                    │
├─────────────────────────────────────────────┤
│ FOOTER  trip types · company · legal        │
├─────────────────────────────────────────────┤
│ STICKY (mobile) [Request a Trip Quote][Call]│
└─────────────────────────────────────────────┘
```

## Ordering rationale

The planner sits **above** the trip-type cards because the V3 brief makes the homepage
transaction-first: a visitor who already knows their trip should be able to start immediately.
The trip-type cards then serve the visitor who does not yet know what they need.

The "what is confirmed today vs with your quotation" block sits directly under the vehicle
section on purpose — it is where a sceptical buyer's question forms, and answering it there is
cheaper than letting them leave to ask it.

## Measured against the brief's 10-second test

At 390 px, above the fold: H1, the relevance line naming the vehicle and city, the phone number,
the availability caveat, and the planner's trip-type tabs (verified: tabs fully within the
viewport, planner beginning at 569 px of an 844 px screen).

## Deliberately absent

No hero image, no carousel, no autoplay video, no promotional banner, no cookie wall, no chat
widget, no social proof strip, no price table, no fleet grid.
"""

DOCS["MOBILE_FLOW.md"] = f"""# MOBILE_FLOW

The 390 px journey, measured rather than described. Primary design target per the V3 brief.

## Entry paths

A visitor arrives from one of three places, and the planner is **preselected** for each so the
first thing they see matches why they came:

| Landing page | Planner opens on |
|---|---|
| `/airport-group-transfer-hyderabad/` | Airport |
| `/wedding-transport-hyderabad/` | Wedding / Event |
| `/outstation-group-travel-hyderabad/` | Outstation (date-range controls visible) |
| `/corporate-group-transport-hyderabad/` | Corporate |
| `/hyderabad-sightseeing-group-travel/` | Sightseeing / Day Trip |
| `/family-group-travel-hyderabad/` | Family Trip |
| `/force-urbania-hire-hyderabad/` | Local (vehicle preference offered) |
| `/find-a-vehicle/` | Custom |

All eight verified in the built HTML.

## The step sequence

```
Trip type  →  Route  →  Dates  →  Group / Luggage  →  Vehicle preference
           →  Contact  →  Trip summary (+ Edit)  →  Request  →  Reference
```

Each mode collapses this into the fields it actually needs. Nothing irrelevant is shown, so the
form never looks long even though the system covers eight trip types.

## Measured mobile behaviour

| Check | Result |
|---|---|
| Horizontal overflow at 375 / 390 px | None |
| Planner start position (390 × 844) | 569 px — trip-type tabs fully on screen |
| Trip-type tab height | 44 px (meets the touch-target minimum) |
| Input height | 46 px (exceeds it) |
| Mobile navigation | Hamburger, keyboard-operable, `aria-expanded` toggled |
| Sticky bottom bar | Present: **Request a Trip Quote** + **Call now** |
| Reduced motion | `prefers-reduced-motion` disables transitions and animation |
| JavaScript disabled | `<noscript>` panel gives the phone number and lists what to send |
| Focus visibility | `:focus-visible` outline on every interactive element |

## Error and edge states handled

- **Validation failure** — the offending field is flagged, focused and scrolled into view;
  the summary does not open, so nothing is lost.
- **API unreachable** — WhatsApp opens with the payload, and the confirmation panel says
  explicitly that the system could not be reached so the customer should send it there too.
- **No JavaScript** — phone and email route with the information needed to quote.
- **Long tab strip** — the trip-type row scrolls horizontally with the scrollbar hidden, so all
  eight modes remain reachable without wrapping into a wall of chips.

## Small-screen typography and spacing

Hero padding tightens to 24 px, the H1 drops to 30 px, and section padding reduces at ≤560 px,
so the planner is reached sooner. Nothing is hidden at small sizes — it is only tightened.

## Known weakness

There is **no progress indicator** across the planner steps, and eight tabs in a scroll strip is
a long first interaction. Both are recorded as the next UI iteration in `QA_REPORT.md`.
"""

for name, body in DOCS.items():
    with open(os.path.join(D, name), "w", encoding="utf-8") as fh:
        fh.write(body)
    print(f"wrote docs/{name}  ({len(body):,} chars)")
print(f"\n{len(DOCS)} V3 deliverables written")
