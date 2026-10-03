# GitHub Commercialization Ledger — Audit/Compliance/AI Solo Founder
Verified by opening repo pages (web_extract) + GitHub API, 2026-10-02. Stars/commits are live figures.

**The arbitrage pattern found:** open-source platform (MIT/Apache) × India-cost implementation × audit-domain credibility = a *managed compliance / document-AI service* sold at Indian consulting rates (₹2–5L/mo) while Western incumbents charge $10–30k/yr SaaS. The software is free; the buyer pays for the outcome, the mapping work, and someone accountable who speaks auditor.

---

## 1. Probo — https://github.com/getprobo/probo
- **STARS / MOMENTUM / LAST COMMIT:** 1,416★ · 222 forks · created 2025-01-07 · 6,860 commits · pushed **2026-10-02** (daily cadence)
- **LICENSE:** **MIT** (GitHub API + repo page). Most permissive of the GRC trio — rebrand/close the derivative is allowed.
- **PROCESS COLLAPSED:** the manual spreadsheet grind of building and *maintaining* a SOC 2 / ISO 27001 / GDPR program — policy drafting, control mapping, evidence collection, task chasing.
- **WHO DOES IT TODAY:** Big 4 / mid-tier Indian ISO consultants and internal compliance staff; the founder's own former job class.
- **WHO PAYS + PRICE:** Startup/scale-up CEO-CTO (security & compliance budget). Comparables: Vanta ~$10–30k/yr, Drata ~$7.5–15k/yr, Comp AI $3–5k/yr; India ISO 27001 implementation ₹15–40L one-time, managed ISMS ₹2–5L/month; Big 4 ₹27–84L per engagement.
- **MANAGED SERVICE / VERTICAL LAYER:** Yes — "compliance-as-a-service" white-label; sell the platform + operator. Best vertical: Indian SaaS/IT-services companies selling to US/EU buyers who must show SOC 2/ISO.
- **FOUNDER MUST BE A DEVELOPER?** No. Self-host (Docker), configure frameworks, run the program. Light dev for branding/integrations; hire for the rest.
- **LEGAL CONSTRAINT:** MIT — clean. Watch trademark only.
- **DIFFICULTY:** MED (self-host + productise).
- **WORKING DEMO?** Yes — clone, docker-compose, load SOC 2 template, show a control with auto-collected evidence.
- **VERDICT:** **BUILD — top pick.** Permissive license + founder's exact domain + a real recurring retainer. Fastest believable path to first ₹.

## 2. CISO Assistant — https://github.com/intuitem/ciso-assistant-community
- **STARS / MOMENTUM / LAST COMMIT:** 4,466★ · 845 forks · created 2023-09-20 · 7,876 commits · active (repo lists Pro/Enterprise editions alongside)
- **LICENSE:** **AGPL-3.0** (community edition) + separate commercial license for Pro/Enterprise in same monorepo.
- **PROCESS COLLAPSED:** control-framework mapping and risk register work — 200+ frameworks (ISO 27001, NIS2, DORA, GDPR, CMMC, SOC 2, PCI DSS) with automatic cross-mapping.
- **WHO DOES IT TODAY:** GRC consultants; in-house security leads; spreadsheet-based risk registers.
- **WHO PAYS + PRICE:** Mid/large enterprises and regulated SMEs; EU clients facing **NIS2/DORA deadlines**, Indian firms on **DPDPA**. India: compliance gap analysis from ₹8L, continuous compliance ₹2.5–8L/month, DPO-as-a-service ₹15–25L/yr.
- **MANAGED SERVICE / VERTICAL LAYER:** Yes — the licensing *forces* the model: you can host and charge, but you can't close your fork, so the moat is service + mapping content + accountability, not code. Strong play: "NIS2/DORA readiness" and "DPDPA compliance" packaged engagements.
- **FOUNDER MUST BE A DEVELOPER?** No — this is implementation/consulting (framework mapping, evidence, audit support), the founder's core skill.
- **LEGAL CONSTRAINT:** AGPL-3.0 — you MUST offer source (incl. your modifications) to network users. Fine for hosting/services; forbids a closed proprietary SaaS fork. Enterprise features are separately licensed.
- **DIFFICULTY:** MED.
- **WORKING DEMO?** Yes — run it, show a NIS2 or DPDPA framework mapped to controls with a gap report.
- **VERDICT:** **BUILD (service-led).** Broadest framework library = sellable consulting surface; AGPL caps the software exit but not the services revenue.

## 3. Comp AI — https://github.com/trycompai/comp
- **STARS / MOMENTUM / LAST COMMIT:** 2,005★ · 422 forks · created 2025-01-15 · 8,232 commits · very active
- **LICENSE:** **AGPL-3.0 + "/ee" Enterprise Edition** dirs under a commercial license (open-core).
- **PROCESS COLLAPSED:** same GRC grind as #1/#2, but AI-native ("Vanta & Drata alternative") — AI policy editor, automated cloud (AWS/GCP) evidence scanning.
- **WHO DOES IT TODAY:** Vanta/Drata + Indian compliance consultants.
- **WHO PAYS + PRICE:** Same buyer; positioned at $3–5k/yr vs Vanta $10–30k/yr — a pricing wedge, but see license.
- **MANAGED SERVICE / VERTICAL LAYER:** Yes, but AGPL + /ee means the best features are vendor-gated — you inherit a competitor's roadmap.
- **FOUNDER MUST BE A DEVELOPER?** No.
- **LEGAL CONSTRAINT:** AGPL-3.0 imposes source-disclosure on your hosted service; /ee restricted.
- **DIFFICULTY:** MED.
- **WORKING DEMO?** Yes (Bun/Temporal stack — heavier setup than #1).
- **VERDICT:** **WATCH, don't build on it.** Fastest-growing and best marketing, but it's a venture-funded company using OSS as a funnel — weakest structural fit for a solo operator. Useful as competitive intel only.

## 4. LLMWare — https://github.com/llmware-ai/llmware
- **STARS / MOMENTUM / LAST COMMIT:** 14,848★ · 2,937 forks · created 2023-09-29 · 2,386 commits · pushed 2026-10-01
- **LICENSE:** **Apache-2.0**
- **PROCESS COLLAPSED:** RAG/document intelligence over finance, legal and compliance document sets using **small, runnable-locally models** (SLIM) — not a cloud LLM call.
- **WHO DOES IT TODAY:** Associates manually reading contracts/filings; offshore doc-review teams; expensive enterprise search tools.
- **WHO PAYS + PRICE:** BFSI/legal/compliance teams with confidentiality constraints. The wedge: **data never leaves the client's premises** — sellable to Indian banks, NBFCs, insurers and audit firms who cannot send client documents to OpenAI.
- **MANAGED SERVICE / VERTICAL LAYER:** Yes — on-prem/private "document intelligence desk": ingest a client's contract/loan/policy corpus, expose Q&A, extraction and clause flags. Charge per engagement or per-seat.
- **FOUNDER MUST BE A DEVELOPER?** Partly — MED build. Founder sets the domain schema and acceptance tests; a contractor wires the pipeline. This is exactly the "domain layer over engineering" split.
- **LEGAL CONSTRAINT:** Apache-2.0 — clean. Model licenses may differ per-model; check the specific SLIM model cards.
- **DIFFICULTY:** MED.
- **WORKING DEMO?** Yes — index a folder of sample contracts, ask a question, show a cited answer with page/block provenance.
- **VERDICT:** **BUILD.** Best founder-fit repo in the set (finance + legal + compliance + privacy), permissive license, and provenance/citation is exactly the audit-grade output buyers pay for.

## 5. Docling — https://github.com/docling-project/docling
- **STARS / MOMENTUM / LAST COMMIT:** 68.3k★ · 5.0k forks · created 2024-07-09 · 1,541 commits · latest commit **2026-10-02 (1 hr ago)**
- **LICENSE:** **MIT** (codebase); individual model licenses vary. Now under **LF AI & Data** (was IBM Research Zurich) — governance risk low.
- **PROCESS COLLAPSED:** getting messy real-world documents (PDF, scanned, DOCX, XLSX, PPTX) into structured, machine-readable form — table/layout/reading-order recovery.
- **WHO DOES IT TODAY:** offshore data-entry/BPO teams; manual copy-paste into Excel/ERP.
- **WHO PAYS + PRICE:** AP/finance teams, banks, insurers, accounting firms. Comparables: Azure Document Intelligence ~$1.50/1,000 pages OCR, ~$10/1,000 prebuilt invoice (~$0.01/invoice) but you fund the build; **Rossum from $18,000/yr** (~$1.50/doc).
- **MANAGED SERVICE / VERTICAL LAYER:** Yes — a vertical "documents → structured data" service (e.g., bank statements / GSTR invoices / loan files → reconciled JSON) billed per document or per month. The layer above Docling (schemas, validation, reconciliation, human review) is the sellable product; Docling is the free engine.
- **FOUNDER MUST BE A DEVELOPER?** Partly — MED. Pipeline glue + schema design can be delegated; the founder owns the extraction accuracy spec and client sign-off.
- **LEGAL CONSTRAINT:** MIT — clean. Verify any bundled model (RapidOCR etc.) licenses separately.
- **DIFFICULTY:** MED.
- **WORKING DEMO?** Yes — convert a real GST invoice PDF to structured JSON in minutes.
- **VERDICT:** **BUILD (as a component).** No moat in the parser alone; the moat is the validated schema + domain rules + accountability layer you put on top.

## 6. Unstract — https://github.com/Zipstack/unstract
- **STARS / MOMENTUM / LAST COMMIT:** 7.3k★ · 720 forks · created 2024-02-21 · 1,747 commits · 593 releases · last commit 2026-09-30
- **LICENSE:** **AGPL-3.0** (OSS build); cloud/enterprise plugins proprietary.
- **PROCESS COLLAPSED:** building and operating LLM document-extraction **pipelines** (prompt-studio + API/ETL deployment) without hand-coding each document type.
- **WHO DOES IT TODAY:** data-engineering teams, IDP contractors, in-house RPA squads.
- **WHO PAYS + PRICE:** enterprises needing document→database at volume; comparables same as Docling (Rossum $18k/yr; Azure per-page) — Unstract replaces their build cost, not their OCR cost.
- **MANAGED SERVICE / VERTICAL LAYER:** Yes — "extraction pipeline as a service": you own the prompt/schema library per client (invoices, KYC, statements) and run it for them.
- **FOUNDER MUST BE A DEVELOPER?** Partly — LOW-MED to operate the UI; the OSS build is a product, not a library.
- **LEGAL CONSTRAINT:** AGPL-3.0 — you may sell hosting, but must offer source (incl. modifications) to users; the cloud plugin path is vendor-controlled.
- **DIFFICULTY:** MED.
- **WORKING DEMO?** Yes — the no-code builder is demo-friendly; connect a sample PDF, ship an API.
- **VERDICT:** **BUILD (fastest demo).** AGPL caps the software play; if you only ever ship services, it's the quickest path to a live document-extraction demo.

## 7. Browser-use — https://github.com/browser-use/browser-use
- **STARS / MOMENTUM / LAST COMMIT:** 117.0k★ · 12.9k forks · created 2024-10-31 · 10,319 commits · latest commit **2026-10-02**
- **LICENSE:** **MIT**
- **PROCESS COLLAPSED:** repetitive work trapped in web UIs where no API exists — downloading statements, portal filings, GSTR/ROC/Bank/EPFO portals, scraping data into spreadsheets.
- **WHO DOES IT TODAY:** junior staff and BPO/RPA teams clicking through portals; UiPath bots at enterprise cost.
- **WHO PAYS + PRICE:** audit/accounting firms, back-office ops, KPOs. Comparables: UiPath ₹15–50L+/yr in India (~$8–10k/unattended bot/yr; median contract $45k/yr); Indian BPO per-task rates.
- **MANAGED SERVICE / VERTICAL LAYER:** Yes — "agentic back-office as a service": per-workflow or per-seat automations (e.g., monthly bank-statement collection for 200 client accounts). High-value because it's the exact manual labour audit firms bill for.
- **FOUNDER MUST BE A DEVELOPER?** Partly — MED-HIGH implementation, but MIT + browser-use's own hosted Cloud make it usable without deep engineering. Partner with one developer.
- **LEGAL CONSTRAINT:** MIT — clean. **Real risk is ToS, not license:** automating bank/tax portals may breach site terms and, in a client context, data-protection obligations. Disclose and get written client authorisation.
- **DIFFICULTY:** MED-HIGH (reliability + credentials + auditability).
- **WORKING DEMO?** Yes — script a portal login + statement download and show the extracted output.
- **VERDICT:** **BUILD if paired with a developer; otherwise park.** Biggest labour-cost collapse in the set, but the least founder-native and the highest operational risk. Pair with #8 for the audit-grade wrapper.

## 8. OpenAdapt — https://github.com/OpenAdaptAI/OpenAdapt
- **STARS / MOMENTUM / LAST COMMIT:** 1,757★ · 261 forks · created 2023-04-12 · pushed 2026-09-26 (multi-repo project: openadapt-flow, -capture, -privacy)
- **LICENSE:** **MIT**
- **PROCESS COLLAPSED:** turning a *human demonstration* of a GUI task into a deterministic program that runs with **0 model calls** and only reports `VERIFIED` when an independent check of the system-of-record agrees — i.e. verified last-mile execution with a tamper-evident run receipt.
- **WHO DOES IT TODAY:** nobody in this audit-grade form — adjacent to RPA (which verifies the click, not the business effect) and to manual controls testing.
- **WHO PAYS + PRICE:** regulated back-office and internal-audit/controls functions that must evidence a control ran correctly (SOX-style, BFSI ops). Comparable anchor: RPA + SOX controls-testing budgets; UiPath-class spend.
- **MANAGED SERVICE / VERTICAL LAYER:** Yes — and it's the most *defensible* packaging here because it sells **evidence**, not automation: "the control executed and here is the independent proof." That is precisely a model-risk/audit professional's product.
- **FOUNDER MUST BE A DEVELOPER?** No for the *domain* (qualification contracts, effect verifiers, control mapping); yes for early deployment — needs a technical partner.
- **LEGAL CONSTRAINT:** MIT — clean.
- **DIFFICULTY:** HIGH (early product, multi-repo, needs qualification contracts per workflow).
- **WORKING DEMO?** Yes — the built-in `openadapt flow tutorial` runs the MockMed synthetic demo end-to-end and prints a VERIFIED receipt.
- **VERDICT:** **STRONG PILOT, not tomorrow's launch.** Highest strategic fit with the founder's model-risk/internal-audit edge and the only repo that sells assurance rather than labour — but immature for a same-week sellable asset. Demo it, then package consulting around it.

---

## Flagged / rejected (evidence-based)

**Abandoned (do not build on):**
- `ICLRandD/Blackstone` — legal NLP, last push **2024-07-16** (~26 months stale), 700★, Apache-2.0. Dead.
- `opendatalab/PDF-Extract-Kit` — last push **2025-01-03** (~21 months stale), 10,036★, AGPL-3.0. Superseded by MinerU.

**License traps (commercial resale restricted — check before hosting/reselling):**
- `n8n-io/n8n` (206k★) — Sustainable Use License (NOASSERTION), **not OSI**; restricts offering it as a hosted service.
- `FlowiseAI/Flowise`, `windmill-labs/windmill`, `dify`, `twentyhq/twenty`, `activepieces` — all report `NOASSERTION`: custom/source-available or AGPL-style terms. Read the LICENSE before any SaaS play.
- **AGPL-3.0 family** (CISO Assistant, Comp AI, Unstract, Skyvern 23.1k★, listmonk, Firefly III): selling a *hosted service* is allowed, but you **must offer the source (including your modifications) to users** — no closed proprietary fork.

**Rejected — interesting, no process to collapse:**
- `microsoft/markitdown` (188.0k★, MIT, created 2024-11-13) and `getzep/graphiti` (31.4k★, Apache-2.0) and `modelcontextprotocol/servers` (91.0k★): great plumbing, but as standalone assets they collapse no billable business step. Use as components (markitdown/MinerU under #5; graphiti under #4).

## Strong alternates (verified, kept in reserve)
- `opendatalab/MinerU` — 80,998★, created 2024-02-29, pushed 2026-09-30, **Apache-2.0 + thresholds** (commercial use allowed; separate license only above 100M MAU or $20M/mo revenue; **must credit MinerU** in any third-party online service). Handles OFD and Office formats — useful for India GST docs.
- `Skyvern-AI/skyvern` — 23.1k★, AGPL-3.0, created 2024-02-28, active 2026-10-02. Product-shaped browser-workflow automation (form-filling, invoicing). Same AGPL/services logic as #6.
- `Stirling-Tools/Stirling-PDF` — 93,445★, **open-core** (MIT core; `engine/`, `saas/`, `proprietary/` dirs under separate licenses — not a clean MIT). Only viable as an internal utility, not a resold product.
- `unclecode/crawl4ai` — 84,641★, Apache-2.0, created 2024-05-09; already has its own commercial Cloud (Crawl4AI Cloud), so the lead-gen/scraping arbitrage is taken by upstream.

## Bottom line for the Chief of Staff
- **Ship tomorrow:** #1 Probo (MIT) + #5 Docling (MIT) + #4 LLMWare (Apache) — all permissive, all demoable in a day, all inside the founder's audit/finance/document domain, all sellable as a ₹2–5L/month managed service against $10–30k/yr incumbents.
- **Fastest demo, weaker licence:** #6 Unstract.
- **Highest ceiling, needs a developer/technical partner:** #7 browser-use, #8 OpenAdapt.
- **Do not build on:** anything AGPL if the goal is a closed sellable software asset, and anything flagged abandoned or non-OSI (n8n).
