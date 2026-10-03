# DATA_PRIVACY_CHECKLIST.md

**Subject:** India's Digital Personal Data Protection Act, 2023 ("DPDP Act") and the Digital Personal Data Protection Rules, 2025 ("DPDP Rules"), applied to a Hyderabad group-travel website that collects **names, phone numbers, trip details and locations**.
**Prepared:** 2026-10-03 · **Status:** RESEARCH + OPERATING CHECKLIST. Not legal advice.
**Markers:** **FINDING** (from cited primary text) · **OPEN QUESTION** (needs a professional) · **COULD NOT VERIFY**.
**Sources** in §10, referenced inline as `[P1] … [P7]`. All accessed **2026-10-03**.

> **Not legal advice.** This maps the statutory obligations onto a small quote-first site. Confirm the content of the published privacy notice and the consent wording with a lawyer before publishing.

---

## 1. Does the DPDP Act apply to this site?

- **FINDING** — DPDP Act s.3(a): the Act applies to processing of digital personal data within India where the data is collected **in digital form or in non-digital form and digitised subsequently**. A website enquiry form, a WhatsApp message, or trip details typed into a CRM are all in scope. [P1]
- **FINDING** — s.3(b): it also applies to processing outside India if connected with offering goods or services to Data Principals in India. [P1]
- **FINDING** — s.3(c): it does **not** apply to (i) personal data processed by an individual for any personal or domestic purpose, and (ii) personal data made publicly available by the Data Principal (or by someone legally obliged to publish it). [P1]
- **FINDING** — Operative dates: the DPDP Rules, 2025 (G.S.R. 846(E), **dated 13 November 2025**) bring rules into force in phases — **Rules 1, 2 and 17–21 on 13 November 2025**; **Rule 4 (Consent Manager) one year later**; and **Rules 3, 5–16, 22 and 23 eighteen months after publication (≈ 13 May 2027)**. [P2]
  - **Practical read:** the substantive duties below — notice (Rule 3), security safeguards (Rule 6), breach intimation (Rule 7), erasure periods (Rule 8), contact info (Rule 9), children (Rules 10–12), rights (Rule 14) — bite from **≈ 13 May 2027**. Government has said it will allow a **transition of up to 18 months**. [P2][P3]
- **OPEN QUESTION** — whether a lawyer considers the site's current practice already compliant with the Act (which is in force) even before the Rules' substantive provisions commence. Treat compliance as required, not "when the Rules start".

### 1.1 Who is who
- **FINDING** — The business is the **Data Fiduciary** — it determines the purpose and means of processing (DPDP Act definitions; obligations in Chapter II). [P1]
- **FINDING** — Third parties who process data **on the business's behalf** (form-handling service, web host, WhatsApp/Business messaging, email provider, CRM, analytics provider) are **Data Processors**; the Fiduciary may engage them "only under a valid contract" (s.8(2)) and is responsible for their processing (s.8(1)). [P1]
- **OPEN QUESTION** — which of the current tools (e.g. a hosted form endpoint, the host, WhatsApp) are **Processors** vs independent **Fiduciaries**, and what contract clauses each needs. (Q1, Q2)

---

## 2. Data map — what this site actually collects

| Data | Where it is collected | Why (purpose) | Notes |
|---|---|---|---|
| Name | Quote form / WhatsApp | To respond and identify the trip organiser | Personal data |
| Phone number | Quote form / WhatsApp | To respond, confirm, coordinate the trip | Personal data |
| Trip details (type, date, group size, pickup/drop, notes) | Quote form | To qualify, price and arrange the trip | May include other people's data |
| Locations (pickup/drop/route) | Quote form | To plan the trip | Location data |
| Source/attribution (`utm_*`, `gclid`, `source_page`, `submitted_at`) | Auto-captured | To know where enquiries come from | Often personal data if it can be linked |
| Communications (messages/emails/calls) | WhatsApp/email/phone | To manage the enquiry and booking | Personal data |

- **FINDING** — Where the site collects **group members' or passengers'** details (e.g. a passenger list for a trip), those individuals are also Data Principals; the organiser is providing their data. Collect only what a trip genuinely requires. [P1]
- **OPEN QUESTION** — whether a **statutory trip list / passenger list** (AITP r.10, CMVR r.85) counts as processing under the Act and how long it must be kept versus the DPDP erasure rule. The transport rule and the data rule must be read together by a lawyer. (Q3)

---

## 3. Consent notice — what it must contain

- **FINDING** — s.5(1): every request for consent must be **accompanied or preceded by a notice** informing the Data Principal of: (i) the personal data and the purpose for which it is proposed to be processed; (ii) the manner in which she may exercise her rights (s.6(4) withdrawal and s.13 grievance); and (iii) the manner in which she may complain to the Board. [P1]
- **FINDING** — s.5(3): the Data Fiduciary must give the option to access the notice **in English or any language in the Eighth Schedule** to the Constitution. [P1]
- **FINDING** — DPDP Rules, **Rule 3**, requires the notice to —
  - (a) be **presented and understandable independently** of any other information;
  - (b) give, **in clear and plain language**, a fair account enabling specific and informed consent, including **at minimum**: (i) an **itemised description** of the personal data, and (ii) the **specified purpose(s)** and a **specific description of the goods/services or uses** enabled by the processing; and
  - (c) give the **communication link** for the website/app and describe the means by which the Data Principal may **(i) withdraw consent** (with ease comparable to giving it), **(ii) exercise her rights**, and **(iii) complain to the Board**. [P2]
- **FINDING** — s.6(1): consent must be **free, specific, informed, unconditional and unambiguous, with a clear affirmative action**, and limited to data **necessary** for the specified purpose. [P1]
- **FINDING** — s.6(3): every request for consent must be in **clear and plain language**, with the option of English or an Eighth Schedule language, and must provide contact details of a **Data Protection Officer** where applicable, or another authorised person to respond on rights. [P1]
- **FINDING** — s.6(4): the Data Principal may **withdraw consent at any time**, with ease comparable to giving it; s.6(6): on withdrawal the Fiduciary must cease processing (and cause processors to cease) within a reasonable time, unless required/authorised by law. [P1]
- **FINDING** — s.6(10): where consent is the basis, the **Fiduciary bears the burden** of proving that a notice was given and consent was obtained. **Keep an auditable record of the notice version shown and the consent captured.** [P1]
- **OPEN QUESTION** — whether, and how, to run a **cookie/consent banner**, and what the lawful basis is for any non-essential cookie. (Q4)

---

## 4. Purpose limitation

- **FINDING** — s.4(1): personal data may be processed **only** in accordance with the Act and **for a lawful purpose** — either (a) the Data Principal's **consent**, or (b) **certain legitimate uses** (s.7). [P1]
- **FINDING** — s.7 lists limited legitimate uses without consent (e.g. voluntary provision of data for a specified purpose the person hasn't objected to; state functions; legal obligations; medical emergency; employment-related). Marketing to a new audience, or re-using trip data for unrelated advertising, is **not** a listed legitimate use and needs consent. [P1]
- **Rule:** collect data **for the trip and nothing more**; do not repurpose enquiry data for marketing or partner-sharing without a specific, separate basis.
- **OPEN QUESTION** — whether sharing an enquiry with a **partner operator** (to source a trip) requires the Data Principal's specific consent (likely yes, and it should be disclosed in the notice). (Q5)

---

## 5. Retention and erasure

- **FINDING** — s.8(7): a Fiduciary shall, **unless retention is necessary for compliance with any law**, (a) **erase** personal data upon withdrawal of consent or as soon as it is reasonable to assume the specified purpose is no longer served, whichever is earlier; and (b) cause its processors to erase data made available for processing. [P1]
- **FINDING** — s.8(8) + **Rule 8(1)–(2)**: the "purpose no longer served" period applies to classes of Fiduciaries listed in the **Third Schedule** (large e-commerce entities ≥2 crore users; online gaming intermediaries ≥50 lakh users; social media intermediaries ≥2 crore users) at **three years**. **A small transport business is not in the Third Schedule**, so the fixed three-year rule does not apply — but the general erasure duty in s.8(7) still does. [P2]
- **FINDING** — **Rule 8(3)**: every Fiduciary must retain personal data, associated traffic data and processing logs for a **minimum of one year** from the date of processing (for the Seventh Schedule purposes), then **erase**, unless further retention is required by other law. [P2]
- **FINDING** — practical implication: a **default retention of at least one year, then deletion**, with any longer retention justified by another law (e.g. tax/company records, or the transport trip-record rules). [P1][P2]
- **OPEN QUESTION** — the exact retention period to adopt, balancing (i) the one-year minimum + erasure rule, (ii) the operator's transport trip-record duties under CMVR/AITP/Telangana rules, and (iii) tax/accounting record-keeping. This needs a lawyer/CA. (Q6)

---

## 6. Data-Principal rights

| Right | Provision | What it means operationally |
|---|---|---|
| **Access** | s.11(1) | On request, give a summary of the personal data being processed, the processing activities, and the identities of other Fiduciaries/Processors with whom it has been shared, plus a description of the data shared. [P1] |
| **Correction / completion / updating / erasure** | s.12 | On request, correct inaccurate/misleading data, complete incomplete data, update it; and erase on request unless retention is necessary for the specified purpose or law. [P1] |
| **Grievance redressal** | s.13 | Provide readily available means to complain; respond within the prescribed period; the Data Principal must exhaust this before going to the Board. [P1] |
| **Nomination** | s.14 | Allow a Data Principal to nominate someone to exercise rights on death/incapacity. [P1] |
| **Withdrawal of consent** | s.6(4) | Easy to withdraw, as easily as given. [P1] |

- **FINDING** — **Rule 14(1)**: publish prominently on the website/app the **means** to make a rights request and any particulars required to identify the Data Principal. [P2]
- **FINDING** — **Rule 14(3)**: every Fiduciary must have a grievance-redressal system and respond **within a period not exceeding ninety days**. [P2]
- **FINDING** — **Rule 9**: publish prominently the business contact information of a person who can answer questions about processing. [P2]

---

## 7. Security, breach and other duties

- **FINDING** — s.8(5) + **Rule 6(1)**: take **reasonable security safeguards** to prevent a personal data breach, including at minimum: encryption/obfuscation/masking or virtual tokens; access controls; logging/monitoring/review to detect unauthorised access; backup/continuity measures; **retain logs and personal data for at least one year**; appropriate contract provisions with Processors; technical/organisational measures. [P1][P2]
- **FINDING** — s.8(6) + **Rule 7**: on becoming aware of a breach, intimate **each affected Data Principal** without delay (concise, clear, plain: description, consequences, mitigation, safety measures, contact), and intimate the **Board** without delay, with detailed information **within 72 hours**. [P1][P2]
- **FINDING** — s.9 + **Rules 10–12**: before processing a **child's** personal data, obtain **verifiable consent of a parent/lawful guardian**; do not undertake tracking/behavioural monitoring of children or targeted advertising at children. (Note: a group trip may include minors; see Q7.) [P1][P2]
- **FINDING** — s.8(3): where data may be used to make a decision affecting the Data Principal or disclosed to another Fiduciary, ensure its **completeness, accuracy and consistency**. [P1]
- **FINDING** — s.10 + **Rule 12**: **Significant Data Fiduciaries** (notified by Government) have extra duties (DPO in India, independent audits, DPIA). A single-vehicle business is not expected to be one, but the Government may notify classes. **COULD NOT VERIFY** whether any transport class has been notified [P1][P2].
- **FINDING** — **Rule 15**: personal data may be transferred outside India subject to any Government restrictions on making it available to a foreign State/entity. If analytics or a CRM stores data abroad, this is the relevant provision. [P2]

---

## 8. What the published privacy notice must contain (drafting checklist)

A lawyer should sign this off, but it should at minimum cover:

- [ ] **Identity and contact** of the business, and the contact of the person who answers data questions (Rule 9) and the grievance channel (Rule 14). [P2]
- [ ] **Itemised list of the personal data collected** (name, phone, trip details, locations, attribution data). [P2 Rule 3(b)(i)]
- [ ] **Specified purpose(s)** for each item, with a plain description of the service enabled (e.g. "to prepare and send you a quotation", "to arrange the trip"). [P2 Rule 3(b)(ii)]
- [ ] **Lawful basis** (consent) and an explicit statement that consent is the basis. [P1 s.4]
- [ ] **Who data may be shared with** (e.g. a partner operator, messaging/hosting providers) and why. [P1 s.11; Q5]
- [ ] **Retention period** and what happens at the end. [P1 s.8(7)]
- [ ] **How to withdraw consent**, and that it can be done as easily as consent was given. [P1 s.6(4); P2 Rule 3(c)(i)]
- [ ] **How to exercise rights** (access, correction, erasure, grievance, nomination) and what identification is needed. [P1 s.11–14; P2 Rule 14]
- [ ] **How to complain to the Data Protection Board**, with the link. [P1 s.5(1)(iii); P2 Rule 3(c)(iii)]
- [ ] **Language option** — English or an Eighth Schedule language. [P1 s.5(3)]
- [ ] **Security** summary and **breach-notification** commitment. [P1 s.8(5)–(6)]
- [ ] **Children** — a statement on how minors' data is handled, if at all. [P1 s.9]
- [ ] **Cookies/analytics** — what is set, and the consent basis (see §9).
- [ ] **Version/date** of the notice, kept as an auditable record. [P1 s.6(10)]

---

## 9. What must be true BEFORE adding analytics or any third-party script

**Current state:** the site loads **no analytics and no third-party scripts**, and sets no cookies; the privacy page says so. **That statement must be updated *before* anything is enabled, not after.** (Matches `ANALYTICS_PLAN.md`.)

Before adding **any** analytics, pixel, tag manager, chat widget, embedded map, or third-party script, all of the following must be true:

- [ ] **Decide the provider and its role.** Confirm whether the provider is a **Data Processor** (acts only on your instructions) or an independent **Data Fiduciary**; use a processor where possible. [P1 s.8(2)]
- [ ] **Update the privacy notice first** to itemise the new data (e.g. IP address, device, pages, approximate location), the purpose (auditing/site improvement), and the provider. [P2 Rule 3]
- [ ] **Establish a lawful basis.** If the processing is not a listed legitimate use under s.7, obtain **consent** — a real, specific, affirmative consent, not a buried line. [P1 s.4/s.7]
- [ ] **Consent banner if required.** If the script sets non-essential cookies/identifiers, block it until consent is given (no pre-ticked or implied consent). [P1 s.6(1)]
- [ ] **Minimise.** Prefer a privacy-friendly, cookieless analytics setup; disable IP-based personalisation; do not send trip details or phone numbers into analytics as event parameters. [P1 s.6(1) necessity]
- [ ] **Contract with the provider** covering processing, security and deletion, and check where data is stored/transferred (Rule 15). [P1 s.8(2); P2 Rule 15]
- [ ] **Security review** of the tag: what it can access, whether it is necessary, and how it is kept updated. [P1 s.8(5)]
- [ ] **Consent record.** Keep evidence of the notice version shown and the consent captured. [P1 s.6(10)]
- [ ] **Retention** for analytics logs set to the minimum needed (and at least the Rule 8(3) one-year floor for the covered data/logs). [P2 Rule 8(3)]
- [ ] **Kill-switch** — a documented way to remove the script and delete the data.
- [ ] **No third-party script that reaches into the enquiry form data** without a processor contract and a lawful basis.

**Rule of thumb:** *notice and consent come before the tag, not after.*

---

## 10. Sources

All URLs accessed **2026-10-03**.

- **[P1]** The Digital Personal Data Protection Act, 2023 (No. 22 of 2023), as published in the Gazette of India, Extraordinary, Part II, Section 1, CG-DL-E-12082023-248045 — PDF: https://egazette.gov.in/WriteReadData/2023/248045.pdf ; India Code handle: https://www.indiacode.nic.in/indiacode/handle/123456789/22037
- **[P2]** The Digital Personal Data Protection Rules, 2025, G.S.R. 846(E), dated **13 November 2025** — Gazette PDF: https://egazette.gov.in/WriteReadData/2025/267650.pdf ; MeitY copy: https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
- **[P3]** Press Information Bureau, "Government notifies DPDP Rules to empower citizens and protect personal data" — https://www.pib.gov.in/PressReleaseDetail.aspx?PRID=2190014
- **[P4]** MeitY — Explanatory note to the DPDP Rules, 2025 — https://www.meity.gov.in/content/explanatory-note-digital-personal-data-protection-rules-2025
- **[P5]** MeitY — DPDP Rules, 2025 document page — https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
- **[P6]** (SECONDARY, used only to locate the primary gazette) PwC India — "MeitY notifies Digital Personal Data Protection Rules, 2025" (notes notification G.S.R. 846(E) dated 13 November 2025 and the 18-month compliance window) — https://www.pwc.in/research-insights/news_alert/regulatory-insights/meity-notifies-digital-personal-data-protection-rules-2025.html
- **[P7]** (SECONDARY, used only to cross-check Rule 3 wording) DPDP Rules 2025 Rule 3 explainer — https://dpdprules.org/rules/3

---

## 11. Open questions for a lawyer

1. Which current tools (host, hosted form endpoint, WhatsApp Business, email) are **Data Processors** vs independent **Fiduciaries**, and what contract/DPA clauses does each need [P1 s.8]?
2. What exactly must the **enquiry form** say at the point of collection so that consent is "specific and informed" (Rule 3)?
3. How do the **statutory trip/passenger-list** duties (AITP r.10, CMVR r.85, Telangana MV Rules) interact with the DPDP **erasure** duty and the one-year minimum retention [P1 s.8(7); P2 Rule 8]?
4. Do we need a **cookie/consent banner**, and for what (especially before any analytics is added)?
5. Does sharing an enquiry with a **partner operator** need specific, separate consent, and how must it be disclosed?
6. What **retention schedule** should we adopt across enquiries, bookings, and trip records?
7. How do we handle **minors** on group trips (verifiable parental consent, no tracking) [P1 s.9]?
8. Are there any **foreign data transfers** in our toolchain that trigger Rule 15 constraints [P2 Rule 15]?
9. What **breach-response procedure** (who notifies the Board, within 72 hours) should we document [P1 s.8(6); P2 Rule 7]?
10. Confirm the business is **not** (and is unlikely to be) a **Significant Data Fiduciary**, and that no transport class has been notified [P1 s.10].

---

## 12. One-page operational checklist (do these in order)

- [ ] Write and publish a DPDP-compliant **privacy notice** (§8) — signed off by a lawyer.
- [ ] Put a **short consent line + link** at the point of collection on the form, and record the consent.
- [ ] Inventory every tool that touches enquiry data; classify each as Processor/Fiduciary; sign appropriate contracts.
- [ ] Fix a **retention schedule** (default: ≥1 year, then delete; longer only where another law requires).
- [ ] Stand up a **rights + grievance channel** with a **≤90-day** response commitment and a published contact.
- [ ] Document a **security baseline** (encryption, access control, logs, backups) and keep logs ≥1 year.
- [ ] Document a **breach procedure** (affected individuals without delay; Board within 72 hours).
- [ ] Do **not** add analytics or third-party scripts until §9 is fully satisfied and the privacy notice is updated first.
- [ ] Re-check the whole checklist as the DPDP Rules' substantive provisions commence (≈ 13 May 2027).
