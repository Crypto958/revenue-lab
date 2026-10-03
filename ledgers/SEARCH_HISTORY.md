# SEARCH_HISTORY
Check before discovery. Track: SOURCE | METHOD | SIGNAL QUALITY | VALUE.

| Date | Scout | Queries / sources | Outcome | Reuse? |
|------|-------|-------------------|---------|--------|
| 2026-10-02 | CoS | AI-gov/model-risk/IA/SOC2 pricing; India fintech AI; model-risk hiring | D2/D3/D4 evidence | pricing reusable |
| 2026-10-02 | W1 | ISO42001 pricing, Upwork AI-gov, bank validation RFPs, RBI/SR-11-7 | bank tenders (high) | high |
| 2026-10-02 | W2 | EU AI Act omnibus, ISO42001 adoption, IA outsourcing market, audit automation | killed O6; downgraded O1 | medium |
| 2026-10-02 | W3 | GitHub compliance-automation/GRC/doc-extraction/MCP topics | Probo/Docling/LLMWare | medium |
| 2026-10-02 | W4 (Universe B) | Upwork/marketplaces: RFP writers, grants, AI-SDR, CI analysts, Amazon catalog, recruiting, contract abstraction, COI, RegTech, bookkeeping | 10 ranked candidates; 4 STRONG | HIGH |
| 2026-10-02 | W5 (Bank behaviour) | SBI/BoB/JK/Indian Bank RFPs, RBI 2024+2026 drafts, bank codes of conduct, staffing rates | D2 demoted with hard evidence | HIGH |
| 2026-10-02 | W6 (GitHub broad) | livekit/pipecat/gpt-researcher/skyvern/crawl4ai/chatwoot/activepieces/docuseal/twenty/career-ops | licence map + 3 clean picks | HIGH |
| 2026-10-02 | FastMoney-H (this) | answering/AI-receptionist pricing; Upwork job counts (leadgen 2,845 / list-build 1,338 / Amazon listing 844 / reputation 876 / reviews 746); review-ops pricing; Clay/Apollo credit-pain Reddit + Clay community; Recruit Signals + Apify hiring-signal leads; podcast booking + ghostwriting + dubbing pricing; buyer-population counts (Amazon sellers, recruiting agencies, dental practices, agencies) | 6 ADDITIONAL hypotheses (H1–H6) + 5 kills | HIGH |

## Source effectiveness (self-modifying)
- Bank tender/RFP docs: highest budget evidence — but also revealed the FIRM-gate constraint.
- Upwork/marketplace live-job counts: strong demand + pricing proxy (use for pricing, not businesses directly).
- GitHub page HTML + LICENSE + commit atom (API rate-limited): reliable capability/licence verification.
- Vendor pricing pages: pricing only (many SEO/lead-gen) — treat as INFERENCE.

## 2026-10-03 — BATCH 04 (EMAIL-ONLY) discovery + route re-verification
| Date | Scout | Queries / sources | Outcome | Reuse? |
|------|-------|-------------------|---------|--------|
| 2026-10-03 | B04 (email-only) | Web search per email-first segment (boutique hotels, event management, real-estate developers, schools, multispeciality hospitals, recruitment, interiors/architecture) → fetch each business's OWN site with a MOBILE iPhone UA, count raw-HTML `<form>`/`wa.me`/`tel:`/`mailto:`/`viewport`, extract on-page emails | 14 send-ready email-only items (9 Part A re-verified + 5 Part B NEW); 2 WATCH | HIGH |

**Method that worked:**
- **Mobile User-Agent is mandatory.** Legacy Indian SMB sites (Western Wings: table width=1001px, no viewport) behave differently to mobile vs desktop; fetch with an iPhone UA and decode `errors='replace'` (iso-8859-1 pages abort a batch otherwise).
- **Raw-HTML signal counts turn "the site looks weak" into a citable defect.** Counting `<form>`/`wa.me`/`tel:`/`mailto:` in the SERVED HTML produced the strongest openers: Padmaja's FAQ literally says "use the appointment form on this page" while the HTML contains 0 `<form>`; Globus returns HTTP 500 on every non-home URL; Royalton's own "Banquets" nav link 404s.
- **Re-verify before reuse — routes and defects both decayed.** Live re-fetch today: C-012's published mailbox (dwdcmail@gmail.com / nizampet@dwdc.in) is GONE (site now shows `info@dwdc.saastemp.site`, a staging domain); and the claimed defects for C-004/C-006/C-007/C-009/C-017 no longer hold (those sites now serve working forms/prices). Reusing the old drafts unverified would have shipped false claims.
- **Name/DM enrichment:** own-site About pages and public LinkedIn give the decision-maker (Dr. Gautham Naidu — Padmaja MD; Ashok Kumar Pinisetti — ACAS Founder/CEO; Sailesh Kumar Mathur — Hotel Abode Group GM). Where only an info@ mailbox exists, role-address.

**What failed / limits (do not repeat blind):**
- **Directory emails are not own-site emails.** Kalankaar's and KMK's addresses exist only on LinkedIn; KMK's site is a 1,507-byte blank Lovable app-shell and Kalankaar's does not serve at all → route UNVERIFIED, held as WATCH.
- **`getent`/HTTP checks can be flaky mid-session.** westernwings.in returned 200 earlier today then HTTP 000 on repeats (DNS still resolves) — flagged MED, require one successful load before send.
- **A 500 on *every* path incl. garbage means a catch-all error page,** not necessarily a specific broken contact route — phrase accordingly (Globus, B2).
- Segment searches surface many businesses whose capture is actually fine (forms/WhatsApp present) → most were rejected; only the ones with a real observed gap entered the batch. Quality > quantity: cap respected at 14.
