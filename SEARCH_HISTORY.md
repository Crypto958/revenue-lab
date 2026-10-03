# SEARCH_HISTORY
Before discovery, check here. Avoid repeating low-value exploration unless new information justifies it.
Track: SOURCE | SEARCH METHOD | SIGNAL QUALITY | OPPORTUNITIES GENERATED | EVENTUAL COMMERCIAL VALUE.

| Date | Scout | Queries / sources used | Outcome | Reuse? |
|------|-------|------------------------|---------|--------|
| 2026-10-02 | CoS sweep | AI-governance / model-risk / IA / SOC2 pricing; India fintech AI; model-risk hiring | Evidence for D2/D3/D4 | pricing evidence reusable |
| 2026-10-02 | W1 | ISO 42001 pricing, Upwork AI-gov, bank validation RFPs, RBI/SR-11-7 | Bank tenders found (high value) | high |
| 2026-10-02 | W2 | EU AI Act omnibus, ISO 42001 adoption, internal-audit outsourcing market, audit-automation incumbents | Killed O6; downgraded O1 | medium |
| 2026-10-02 | W3 | GitHub: compliance-automation, GRC, doc extraction, MCP, lead-gen topics | Probo/Docling/LLMWare identified | medium |
| 2026-10-02 | Scout A (global remote roles) | Remotive / jobgether / Himalayas / dailyremote + employer ATS APIs (Greenhouse, Ashby, Workday, Lever, Amazon.jobs) for internal-audit/risk/GRC/model-risk/AI-governance roles performable from India | 12 India-eligible/global-remote roles + GitLab(closed)/Kraken/Stripe/Canonical ineligible | high — output: research/scout_a_global_remote_roles.md |
| 2026-10-02 | B (Track A) | Transferable high-comp remote roles: trust & safety, risk ops, compliance ops, internal audit at scale-ups, AI/enterprise risk, SOX/ICFR, third-party risk, GRC/SaaS assurance, RevOps. Sources: Greenhouse/company ATS + remote.com + web3.career + Deel/Remofirst/Revolut/Airwallex careers | 12 India-eligible roles verified (see research/scout_b_transferable_remote_roles.md) | high |
| 2026-10-02 | W-Local | Hyderabad local services scout (home/auto/hotel-banquet/recruitment). Sources: web_search + web_extract + raw curl; Justdial/TripAdvisor/Google Maps for review evidence | 8 real businesses audited + 7-point journey problems each (see research/scout_operational_local_services_hyderabad.md) | high — feeds Local Business Engine outreach |

## Source effectiveness (self-modifying search strategy)
- Bank tender portals / RFP documents: HIGHEST signal quality (real budgets). Prioritise.
- GitHub topics + repo API: good for capability discovery; weak for demand.
- Vendor pricing pages: useful for pricing; many are SEO/lead-gen — treat as INFERENCE.
- Raw-HTML signal scan (count `<form>` / `wa.me` / `tel:` / `mailto:` in the served page) is the cheapest, hardest-to-argue lead-capture evidence. Use it FIRST for any local-business audit.
- Browser backend WORKS on this host as of 2026-10-03 (the 2026-10-02 "Chromium libatk missing" blocker is cleared).

## Cycle log
- 2026-10-03 · Outreach cycle · (1) Reconciliation scan: the local engine had 32 deep audits but an EMPTY CONTACTS/OUTREACH/OPPORTUNITIES ledger — the real bottleneck was converting research into queued outreach, not more research. (2) New niche discovery: Hyderabad eye/LASIK clinics (Sree Netralaya, Envision, Pristine) via web_search + raw-HTML lead-capture scan. Output: 3 new audits (MICRO_AUDITS Batch 2) + a 16-item local outreach queue (outreach/LOCAL_QUEUE_BATCH_02.md) + filled ledgers. Signal quality: HIGH.
- 2026-10-03 · Outreach cycle 2 (execution layer) · Diagnosis: the pipeline is full (36 drafts, 3 batches) and the binding constraint has MOVED to approval→send; more drafting creates no opportunity while sends are blocked. Action: built the LOCAL EXECUTION KIT (one-tap wa.me/mailto links, paste-ready tracking sheet, D+3/D+7/D+14 cadence, 3 show-before-ask 3-point-fix artefacts) and re-verified contact routes live. Output: outreach/LOCAL_EXECUTION_KIT_2026-10-03.md (16 items). Method note: route re-verification via web fetch found real decay (Yellow Planners' published phone now stale), confirming routes must be re-checked immediately before any send. Signal quality: n/a (execution, not discovery); commercial value: TBD on first send.
- Reddit/community threads: good for disconfirming evidence + real pain language.
- 2026-10-03 · Outreach cycle 3 (new niches + decision-collapse) · Method: web_search for candidates → mobile-UA curl raw-HTML lead-capture scan (`<form>`/`wa.me`/`tel:`/`mailto:`) + DNS check on each business's own served page → named-owner lookup on LinkedIn/own-site. Sources queried: Justdial/IYP/ExportersIndia directories, LinkedIn, city business sites. Output: 6 audits in 2 NEW niches (home-interiors/modular-kitchen ×4, study-abroad ×2) appended to MICRO_AUDITS (Batch 3), 4 tailored drafts (outreach/LOCAL_QUEUE_BATCH_03.md), and the consolidated founder decision brief (DECISION_NEEDED.md). Two leak archetypes newly documented: no capture surface (Fleegl, SSS) and DEAD listed website (Lipsy Interior — lipsyinterior.com does not resolve). Signal quality: HIGH for interiors, MED for study-abroad (only 1 of 2 cleanly actionable). Commercial value: TBD on approval.
