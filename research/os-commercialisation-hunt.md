# GitHub / Open-Source Commercialisation Hunt (broad mandate, beyond audit/finance)

**Verified:** 2026-10-02. Stars + last-commit read live from github.com (HTML star counter + `/commits/HEAD.atom`); licences read from each repo's raw `LICENSE`/`license.txt` — not guessed. Prices cited to vendor pricing pages.
**Lens:** can a solo India-based, bank-employed, non-heavy-dev founder turn this into an async, productised, AI-operated income stream? First question = can someone make money; second = can Abhishek own it.
**₹1 lakh = ₹100,000 ≈ US$1,150.** "Founder hrs / ₹1L" = founder hours to book ₹1,00,000 of revenue in that line (setup + oversight, after the AI does execution).

---

## 1. LiveKit Agents — voice AI agents / telephony
**URL:** https://github.com/livekit/agents | **14,449★** | last commit **2026-10-01T22:37:54Z** | **Apache-2.0** (raw LICENSE verified)
- **Expensive capability now cheap:** production real-time voice agents with telephony (SIP), turn detection, STT→LLM→TTS pipelines. Building this stack in 2023 cost a funded team; now it's a `pip install`.
- **Who pays today:** AI receptionist / answering services — Smith.ai human $300/mo per 30 calls ($10/call) and AI $150–500/mo (https://smith.ai/pricing/receptionists , https://smith.ai/pricing/ai-receptionist); NextPhone flat from $199/mo (https://www.getnextphone.com/blog/best-ai-receptionist); Vapi $0.05/min hosting + component layers (https://vapi.ai/pricing); Retell $0.07–0.31/min (https://www.retellai.com/pricing); Synthflow $29/mo 50 min → $99/mo 200 min (https://synthflow.ai/ai-answering-service). India: telecaller ₹12–20K/mo (https://www.glassdoor.co.in/Salaries/telecaller-salary-SRCH_KO0,10.htm); AI outbound call ₹6–12/min vs human agent $0.50–1.75/min (https://www.callmissed.com/en/blog/the-cost-economics-of-a-voice-minute-in-2026-what-every-business-needs-to-know).
- **Paid outcome:** setup + monthly retainer for an AI receptionist that answers missed calls, books appointments, and speaks Hindi/regional languages (Sarvam STT ₹30/hr, TTS ₹3/1000 chars — https://www.sarvam.ai/api-pricing).
- **Founder hrs / ₹1L:** ~50 hrs early (per-client telephony + prompt setup + monitoring), falling to ~20 hrs at scale.
- **Non-heavy-dev founder:** borderline — needs a pair for telephony/SIP + webhooks. Not solo-able day one.
- **Async / no confidential data:** NO — live calls, recordings, caller PII in scope. Real-time support burden.
- **Licence trap:** none. Apache-2.0. (LiveKit Cloud is the paid arm, but the code is clean.)
- **Productised service / micro-SaaS:** yes — managed "AI receptionist for clinics/real-estate/coaching" is the cleanest form.
- **₹10L/month mechanism:** 100 SMBs × ₹10K/mo, or 40 clinics × ₹25K/mo.
- **Verdict:** biggest market and revenue ceiling, but it is the *least* async and most ops-heavy — it violates the "not a second job" rule unless paired. **Tier-1 only if a technical co-pilot exists.**

## 2. Pipecat — voice/multimodal agents (permissive twin of #1)
**URL:** https://github.com/pipecat-ai/pipecat | **16,146★** | last commit **2026-10-02T15:30:08Z** | **BSD-2-Clause** (raw LICENSE verified)
- Same collapsed capability as #1, **more permissive licence** (BSD-2 beats LiveKit's Apache only marginally — both fine), maintained by Daily + community, ships a CLI that scaffolds a bot in under a minute and first-class Sarvam (Indian STT/LLM/TTS) integrations.
- **Who pays today:** identical buyer set to #1 (Smith.ai, NextPhone $199/mo, Synthflow).
- **Paid outcome / hrs / trap:** same as #1. ~50 hrs/₹1L early. **No licence trap.**
- **₹10L/month mechanism:** as #1.
- **Verdict:** pick Pipecat *or* LiveKit, not both — Pipecat if you want the simplest scaffold + Indian-language provider list. Same async/ops caveat as #1.

## 3. GPT-Researcher — autonomous deep research
**URL:** https://github.com/assafelovic/gpt-researcher | **29,876★** | last commit **2026-09-26T16:56:07Z** | **Apache-2.0** (README)
- **Expensive capability now cheap:** a cited, 20+ source, multi-page research report that used to take an analyst a week. Perplexity/Gartner sell this; the engine is now free.
- **Who pays today:** Gartner/Forrester/IDC syndicated subscriptions $25K–60K/yr (1–5 users), $100K–500K+ enterprise, ~$130K starter (https://dupple.com/blog/market-research-top-companies , https://www.g2.com/products/gartner/reviews); Klue/Crayon competitive-intel $20K–40K/yr (https://dupple.com/learn/best-ai-competitive-intelligence-tools); Perplexity Pro $20/mo (https://www.perplexity.ai/hub/pricing).
- **Paid outcome:** productised research reports / ongoing competitive-intel digests sold to agencies, D2C brands, VC/PE analysts, and content teams — ₹8–15K per bespoke report, or ₹25–50K/mo monitoring retainers.
- **Founder hrs / ₹1L:** ~8–12 hrs (10–15 reports; ~30–45 min of AI run + human review each). **Best hours-to-rupee ratio on this list.**
- **Non-heavy-dev founder:** YES — pip install + API key; runs headless.
- **Async / no confidential data:** YES — fully async, works off public web. No PII.
- **Licence trap:** none. Apache-2.0.
- **Productised service / micro-SaaS:** both viable; service first, micro-SaaS (topic-monitoring subscriptions) second.
- **₹10L/month mechanism:** 100 reports/mo × ₹10K, or 20 retainers × ₹50K.
- **Verdict:** **Tier-1. Cleanest fit to the brief** — async, no confidential data, low dev, public-data only, obvious buyers. Distribution (finding who pays for reports) is the only real work.

## 4. Skyvern — AI browser automation / RPA
**URL:** https://github.com/Skyvern-AI/skyvern | **23,126★** | last commit **2026-10-02T18:31:48Z** | **AGPL-3.0** (README; anti-bot logic withheld to their cloud)
- **Expensive capability now cheap:** UiPath-style unattended RPA. UiPath Pro = $1,380/mo for 1 attended + 1 unattended bot (https://aimultiple.com/rpa-pricing); market rates $5–15K/bot/yr.
- **Who pays today:** enterprises buying UiPath/Automation Anywhere; SMBs paying offshore VAs/BPO for repetitive portal work.
- **Paid outcome:** "we automate your repetitive portal task" (invoice entry, form filing, data pulls) sold as a fixed monthly per-workflow retainer.
- **Founder hrs / ₹1L:** ~30–60 hrs (each workflow needs build + selector QA). Ongoing low.
- **Non-heavy-dev founder:** NO — needs a dev (Python, Docker, LLM keys, CAPTCHA handling).
- **Async / no confidential data:** async batch, BUT workflows run inside client systems with credentials → confidential-data exposure.
- **Licence trap:** **YES — AGPL-3.0.** Offering it to clients over a network triggers §13 (must offer source to users); modifying + hosting = must publish. Only avoidable with a commercial licence or by using it purely internally. Real friction.
- **Productised service / micro-SaaS:** service yes; SaaS is legally messy under AGPL.
- **₹10L/month mechanism:** 20 clients × ₹50K/mo.
- **Verdict:** strong "process to collapse" but **AGPL + dev-heavy + credential-handling** = fails the "async, low-conflict, not-a-second-job" test. Reject for Abhishek.

## 5. Crawl4AI — LLM-ready web scraping / data extraction
**URL:** https://github.com/unclecode/crawl4ai | **84,644★** | last commit **2026-09-25T06:35:50Z** | **Apache-2.0** (repo page)
- **Expensive capability now cheap:** large-scale structured web extraction into clean Markdown/JSON, with deep-crawl, JS rendering, anti-bot handling.
- **Who pays today:** Clay — paid plans from $149/mo, Pro $800/mo, new Launch $185/mo, Growth $495/mo (https://www.clay.com/pricing , https://www.clay.com/faq); Apify $39/$199/$999 tiers (https://www.kdnuggets.com/2025/07/oxylabs/best-web-scraping-companies-in-2025); Apollo.
- **Paid outcome:** lead lists / market-data extractions / price-monitoring feeds sold per-order (₹5–15K) or as growth retainers.
- **Founder hrs / ₹1L:** ~10–15 hrs (10–20 orders; ~30–60 min per extraction). Excellent ratio.
- **Non-heavy-dev founder:** yes with light Python; the Docker API server makes it a callable service.
- **Async / no confidential data:** YES — batch, public data only.
- **Licence trap:** none. Apache-2.0. (Firecrawl, the flashier rival — 187,880★, last commit 2026-10-02 — is **AGPL-3.0**; prefer Crawl4AI for lawful resale.)
- **Productised service / micro-SaaS:** yes — "India lead-gen data" and compliance/price monitoring are natural micro-SaaS.
- **₹10L/month mechanism:** 200 lead-list orders × ₹5K, or 20 growth retainers × ₹50K.
- **Verdict:** **Tier-1.** Same virtues as GPT-Researcher (async, public data, low dev, Apache) with an even more immediate buyer (every sales team). Watch ToS/robots compliance — that is the real risk, not the licence.

## 6. Chatwoot — omni-channel customer support desk (+ AI Captain)
**URL:** https://github.com/chatwoot/chatwoot | **37,436★** | last commit **2026-10-02T01:19:23Z** | **MIT core** + `ee/` commercial (raw LICENSE: "MIT Expat")
- **Expensive capability now cheap:** Intercom/Zendesk-class inbox across web, email, WhatsApp, Instagram, etc., plus an AI agent.
- **Who pays today:** Zendesk $55–169/agent/mo, monthly $69–219 (https://www.zendesk.com/pricing/ , https://hiverhq.com/blog/zendesk-pricing); Intercom $29–132/seat/mo + $0.99/Fin outcome (https://www.intercom.com/pricing); Salesforce Service Cloud.
- **Paid outcome:** managed AI-first support desk for Indian SMBs — setup + WhatsApp/email channel wiring + AI agent training, monthly per-business fee.
- **Founder hrs / ₹1L:** ~40 hrs (deployment, channel setup, AI tuning, per-client babysitting).
- **Non-heavy-dev founder:** medium — self-host is a Rails app; Docker deploy is doable but the WhatsApp/omnichannel plumbing needs a pair.
- **Async / no confidential data:** async-ish, BUT holds customer PII and support threads → confidential-data exposure.
- **Licence trap:** none for the MIT core. **Avoid the `ee/` directory** (commercial licence) — do not enable enterprise features.
- **Productised service / micro-SaaS:** yes.
- **₹10L/month mechanism:** 100 SMBs × ₹10K/mo.
- **Verdict:** solid recurring revenue, but PII custody + deploy complexity push it to Tier-2 for a solo bank-employed operator.

## 7. Activepieces — workflow automation / Zapier replacement (MIT core)
**URL:** https://github.com/activepieces/activepieces | **24,853★** | last commit **2026-10-01T22:47:29Z** | **MIT core** + `packages/ee/` commercial (raw LICENSE verified)
- **Expensive capability now cheap:** Zapier/Make-style automation with an AI-first, no-code builder and 280+ MCP tools. **Critically, the core is MIT, not n8n's Sustainable Use Licence** — so you *can* host and resell.
- **Who pays today:** Zapier (task-based, free 100 tasks) https://zapier.com/pricing; Make from $9/mo https://www.make.com/en/pricing; n8n.
- **Paid outcome:** automation-agency retainers — connect a client's CRM/WhatsApp/Sheets and ship + maintain flows.
- **Founder hrs / ₹1L:** ~40–60 hrs (each flow is bespoke); recurring once built.
- **Non-heavy-dev founder:** medium-high — no-code builder, but integrations/self-hosting need care.
- **Async / no confidential data:** async, BUT flows touch client credentials and data → confidential-data exposure.
- **Licence trap:** none for core (MIT). **Avoid `packages/ee/`.** (Explicitly contrast: **n8n = Sustainable Use Licence — forbids hosting/reselling for clients** https://docs.n8n.io/n8n-community-license ; **NocoDB = Sustainable Use Licence too** — verified in its LICENSE.md, despite many blogs claiming AGPL.)
- **Productised service / micro-SaaS:** yes — the classic automation agency.
- **₹10L/month mechanism:** 50 clients × ₹20K/mo retainer.
- **Verdict:** **Tier-2 strong.** The permissive licence is the whole advantage over n8n; the agency model is proven. Client-data custody is the caveat.

## 8. DocuSeal — e-signature (DocuSign alternative)
**URL:** https://github.com/docusealco/docuseal | **18,648★** | last commit **2026-09-28T11:39:31Z** | **AGPL-3.0 + Section 7(b) additional terms** (repo page + LICENSE)
- **Expensive capability now cheap:** document fill + legally-usable e-signature on any device. DocuSign Standard = **$540/yr per user** for 100 envelopes/user/yr with overage fees (https://ecom.docusign.com/plans-and-pricing/esignature , https://support.docusign.com/s/articles/FAQ-Docusign-overage-charges).
- **Who pays today:** DocuSign, PandaDoc, Adobe Sign; Indian real-estate, lending, staffing, and education paperwork.
- **Paid outcome:** e-sign workflow hosted for SMBs / HR / lending — per-document or monthly seat.
- **Founder hrs / ₹1L:** ~15–25 hrs if self-serve micro-SaaS; more if concierge.
- **Non-heavy-dev founder:** medium — Ruby/Docker deploy, template building.
- **Async / no confidential data:** async, BUT signed contracts = high-value confidential documents. Custody risk.
- **Licence trap:** **YES — AGPL-3.0 plus extra §7(b) terms** (branding/attribution). Hosted SaaS forces source disclosure; the additional terms complicate white-labelling.
- **Productised service / micro-SaaS:** yes, but AGPL taxes the SaaS route.
- **₹10L/month mechanism:** 200 businesses × ₹5K/mo, or 2,000 seats × ₹500/mo.
- **Verdict:** real market, but **AGPL + confidential documents** = reject for a solo operator. (Documenso, 15,299★, 2026-10-01, is also **AGPL-3.0**; OpenSign 7,051★, last commit 2026-08-21, also **AGPL-3.0** — same trap across the category.)

## 9. Twenty — modern CRM (Salesforce alternative)
**URL:** https://github.com/twentyhq/twenty | **57,826★** | last commit **2026-10-02T17:07:36Z** | **AGPL-3.0** ("mostly AGPLv3", raw LICENSE verified)
- **Expensive capability now cheap:** a Salesforce-class CRM data model + UI, "designed for AI".
- **Who pays today:** Salesforce from $25/user/mo (https://www.salesforce.com/sales/pricing/); HubSpot Starter $7–20/seat/mo (https://www.hubspot.com/pricing); Zoho CRM India ₹800/user/mo (https://www.zoho.com/en-us/crm/).
- **Paid outcome:** CRM implementation + AI-enrichment for Indian SMBs (pipeline hygiene, WhatsApp sync, lead scoring).
- **Founder hrs / ₹1L:** ~50–70 hrs — this is consulting-shaped, not product-shaped.
- **Non-heavy-dev founder:** NO — TypeScript/NestJS + Postgres, migrations, self-hosting.
- **Async / no confidential data:** holds full customer PII → confidential-data exposure.
- **Licence trap:** **YES — AGPL-3.0.**
- **Productised service / micro-SaaS:** service yes; SaaS legally taxed.
- **₹10L/month mechanism:** 20 implementations × ₹50K + ₹10K/mo maintenance.
- **Verdict:** reject — dev-heavy, PII-heavy, AGPL, and it consumes founder hours rather than AI-compressing them.

## 10. Career-Ops — AI job-search / recruiting agent
**URL:** https://github.com/career-ops-hq/career-ops | **73,232★** (created 2026-04-04, **#1 GitHub Trending**, Trendshift) | last commit **2026-10-02T17:29:47Z** | **MIT** (raw LICENSE verified; repo ships TRADEMARK.md)
- **Expensive capability now cheap:** scan job boards → score each role 1–5 vs a CV → tailor an ATS-friendly CV + cover letter → track applications. Runs locally in an AI coding CLI (Claude Code/Codex/etc.). This is a résumé-agency + recruiter's front office, collapsed to an agent.
- **Who pays today:** LinkedIn Recruiter Lite ~$170/seat/mo (https://www.linkedhelper.com/blog/reduce-linkedin-recruiter-cost); resume-writing/outplacement services; ATS-hardened CV shops.
- **Paid outcome:** (a) B2C: done-with-you job-search package per candidate (₹5–20K); (b) **B2B, the better play:** bulk CV tailoring / candidate screening for Indian staffing & outplacement firms (₹2L/mo contracts).
- **Founder hrs / ₹1L:** ~15–25 hrs (batch AI + light human review). Very good ratio.
- **Non-heavy-dev founder:** yes — it runs inside an AI coding CLI; no infra.
- **Async / no confidential data:** async, BUT CVs are PII — handle under a DPA.
- **Licence trap:** none (MIT); **name/trademark cannot be reused** (TRADEMARK.md).
- **Productised service / micro-SaaS:** both; B2B staffing servicing is the durable one.
- **₹10L/month mechanism:** 100 candidates × ₹10K, or 5 staffing firms × ₹2L/mo.
- **Verdict:** the highest-momentum repo found and MIT-clean. B2C willingness-to-pay is weak; **B2B staffing-outsourcing is the monetisable edge.** Tier-2, with upside.

---

## Honourable mentions / deliberate rejects
| Repo | Stars / last commit | Licence | Note |
|---|---|---|---|
| Firecrawl | 187,880★ / 2026-10-02 | AGPL-3.0 | Vendor already monetising it; AGPL blocks resale |
| Appsmith | 40,993★ / 2026-10-02 | Apache-2.0 | Strong Retool alternative ($0→$45/user/mo, https://retool.com/pricing) — internal-tools agency. Real Tier-2 candidate |
| ERPNext | 39,743★ / 2026-10-02 | GPL-3.0 | SMB ERP vs Odoo $24.90/mo (https://www.odoo.com/) — services-heavy, India-strong, but GPL + consulting-shaped |
| Stirling-PDF | 93,446★ / 2026-10-02 | MIT | Clean licence, but low-ARPU commodity |
| OpenHands | 89,805★ / 2026-10-02 | MIT | Coding agents; MIT-clean but crowded + consumes heavy dev |
| paperless-ngx | 46,235★ / 2026-10-02 | GPL-3.0 | Document DMS; prior wave covered doc processing |
| Postiz | 36,627★ / 2026-10-02 | AGPL-3.0 | Social scheduling is crowded + low-ARPU |
| opengtm | 46★ / **2026-04-09** | — | **Abandoned** (Clay-alternative; no momentum) — reject |
| NocoDB | 65,160★ / 2026-10-02 | **Sustainable Use Licence** | Cannot host/resell — hard trap (blogs mislabel it AGPL) |
| n8n | — | **Sustainable Use Licence** | Cannot host client workflows — hard trap |
| fish-speech | 32,920★ / 2026-09-16 | **Fish Audio Research Licence** | **Non-commercial** (commercial needs a paid licence) — trap |
| Open WebUI | 153,806★ / 2026-09-21 | Custom (branding clause) | Cannot white-label → weak for resale |

---

## Recommendation to the Chief of Staff (ranked)
1. **GPT-Researcher** — the single best fit: async, public-data-only, low-dev, Apache-2.0, proven expensive buyer set (Gartner $25–60K/yr, Klue/Crayon $20–40K/yr) collapsing to ~10 hrs/₹1L.
2. **Crawl4AI** — same profile, more immediate buyer (every sales team; Clay $149–800/mo), only real risk is scraping ToS compliance. **Use Crawl4AI, not Firecrawl (AGPL).**
3. **LiveKit Agents / Pipecat** — biggest revenue ceiling (voice receptionist for India's 7.3 crore registered MSMEs, https://www.pib.gov.in/PressReleaseDetail.aspx?PRID=2209712), but the only candidate that is *not* async and needs a technical co-pilot. Include **only if** the "pair with a dev" budget exists.
- **Avoid as the primary engine:** Skyvern, DocuSeal, Twenty (AGPL + confidential data), and any Sustainable Use / non-commercial licence (n8n, NocoDB, fish-speech).
- **Common thread of the winners:** permissive licence (MIT/Apache/BSD), public (not confidential) data, and a process the AI runs end-to-end so founder hours ≈ 10–25 per ₹1L, not 50–70.
