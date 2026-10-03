# Revenue Lab — Hyderabad Dental & Specialty Clinic Scout
Date: 2026-10-02 · Method: public websites (raw HTML inspection), Justdial/aggregator listings, search snippets, Google Maps listing check. No private data. Every claim tagged OBSERVED / INFERRED / UNKNOWN.

Legend: OBSERVED = seen directly in page source, listing, or review text retrieved. INFERRED = reasoned conclusion. UNKNOWN = not verifiable publicly.

Pricing for OUR services is [ESTIMATE] — solo India operator, async, side business.

---

## 1. Dr White Dental Care
- CATEGORY: Dental (implants, Invisalign, cosmetic)
- LOCATION: Madinaguda (Hafeezpet) + Nizampet, Hyderabad
- WEBSITE: https://drwhitedentalcare.com/
- REVIEWS: Justdial 5.0 (303 ratings) https://www.justdial.com/Hyderabad/Dr-White-Dental-Care-Madinaguda-Madinaguda/040PXX40-XX40-241009211345-C4E1_BZDET/reviews ; site claims 4.9★ / "340+ verified reviews"
- OBSERVED:
  1. 3 Elementor contact forms on homepage, all named generically "New Form" (`<form class="elementor-form" ... name="New Form">`).
  2. WhatsApp deep links present for BOTH branches: `api.whatsapp.com/send?phone=919000016118` and `...919848085789`, with prefilled text "Hello".
  3. Published emails: `dwdcmail@gmail.com` and `nizampet@dwdc.in` (branch-branded domain = above-average digital maturity).
  4. Instagram `instagram.com/drwhitedentalcare` + Facebook `facebook.com/drwhitedentalcare` linked.
  5. No slot/calendar booking (no Calendly/Practo/embedded scheduler found in HTML).
  6. No treatment price list on homepage for implants/Invisalign (transparent-pricing claimed in copy, but no figures published).
- INFERRED: Two disjoint branch numbers + generic forms = enquiries land in a shared Gmail/inbox with no branch routing or response SLA; leads arriving after hours sit until someone checks a phone.
- UNKNOWN: Actual enquiry response time; whether forms are answered same-day; whether Google reviews are replied to.
- LIKELY COMMERCIAL EFFECT: An implant/Invisalign case is ₹30k–₹1.5L+. One unanswered online enquiry ≈ one lost high-value case; a single recovered case can exceed a full year of retainer.
- WHAT WE'D CHANGE: Replace generic form with a short qualifying form (treatment + preferred slot + phone) → auto-reply + WhatsApp handoff; single booking link for both branches; review-request automation.
- IMPLEMENTATION COMPLEXITY: Low–Med
- WHY RELEVANT: They already invest in WhatsApp + forms + socials, so they understand the channel — the gap is *routing and speed*, an easy, high-credibility fix.
- PROPOSED PILOT: Add an instant auto-reply + slot-preference capture on the existing form (no new site), measure response time for 2 weeks.
- DECISION MAKER: Dr. Sri Lakshmi — Founder, Dental Surgeon & Implantologist (publicly listed on site)
- CONTACT ROUTE: +91 900 001 6118 (Madinaguda) / +91 984 808 5789 (Nizampet); dwdcmail@gmail.com; nizampet@dwdc.in; Instagram DM
- CONTACT CONFIDENCE: HIGH
- INDICATIVE PRICING [ESTIMATE]: Setup ₹4,000–8,000 one-time; ₹3,000–5,000/month, or ₹150–400/qualified booking.
- EVIDENCE: https://drwhitedentalcare.com/ · https://drwhitedentalcare.com/about-us/ · Justdial reviews link above

---

## 2. Krishna's Dant Ayush
- CATEGORY: Dental (family + implants + aligners)
- LOCATION: Parvatha Nagar Temple Rd, Tulasi Nagar, Madhapur, Hyderabad
- WEBSITE: https://krishnasdantayush.com/
- REVIEWS: Google Maps shows 5.0★ (review count not displayed on card); https://www.google.com/maps/search/Krishna's+Dant+Ayush+Madhapur+Hyderabad/
- OBSERVED:
  1. Booking form is a JS shim that opens WhatsApp prefilled: `<form class="booking-form" id="bookingForm" onsubmit="return sendToWhatsApp(event)">` → `wa.me/917013338012?text=Hi, I'd like to book...`.
  2. Site copy: "Send us your details on WhatsApp — we'll confirm within minutes. No calls, no waiting."
  3. NO Instagram and NO Facebook link anywhere in the HTML (grep returned none).
  4. NO published email address at all — only phone/WhatsApp +91 70133 38012.
  5. Only one price appears in the page source (₹350); no treatment price list.
  6. Hours Mon–Sat 10:30–8:30, **closed Sunday**; also has a Netlify feedback form.
- INFERRED: 100% of booking depends on a human replying on WhatsApp; if none answers, the lead evaporates with no callback list. Sunday closure + Madhapur's young-professional catchment = weekend enquiries lost to competitors open 7 days.
- UNKNOWN: WhatsApp response time; whether missed chats are followed up; review count.
- LIKELY COMMERCIAL EFFECT: In a market where Partha Dental/Toothsi are open 7 days and advertise online booking, a WhatsApp-only, Sunday-closed clinic bleeds weekend and after-hours demand — each missed chat is a ₹3k–₹60k case depending on treatment.
- WHAT WE'D CHANGE: Add a fallback form + auto-reply (so a missed chat still becomes a captured lead with a callback task); open an Instagram presence; add Google review capture.
- IMPLEMENTATION COMPLEXITY: Low
- WHY RELEVANT: The clinic already sells on WhatsApp speed ("confirm within minutes") — the risk is exactly the promise it makes; fixing capture is directly aligned with its own positioning.
- PROPOSED PILOT: WhatsApp auto-responder + after-hours capture form; weekly missed-chat report.
- DECISION MAKER: Dr. Monika Bajaj (BDS, MDS – Periodontist) and Dr. Guru Charan (BDS, MDS – Oral & Maxillofacial Surgeon), both listed as the clinical leads
- CONTACT ROUTE: +91 70133 38012 (call/WhatsApp); Instagram — none found (UNKNOWN if one exists)
- CONTACT CONFIDENCE: HIGH (phone/WhatsApp published); LOW for email (none published)
- INDICATIVE PRICING [ESTIMATE]: Setup ₹3,000–6,000; ₹2,500–4,000/month.
- EVIDENCE: https://krishnasdantayush.com/

---

## 3. Dr Madhavi's Advanced Skin Hair & Laser Clinic
- CATEGORY: Dermatology (skin, hair, laser, aesthetics)
- LOCATION: 1st Floor, 7-1-220/46, Sravya D Estates, opp. Nature Cure Hospital, Balkampet (S R Nagar), Hyderabad 500016
- WEBSITE: https://madhavisskinclinic.in/
- REVIEWS: Justdial 4.4 / ~2,100–2,183 ratings — https://www.justdial.com/Hyderabad/Dr-Madhavis-Advanced-Skin-Hair-Laser-Clinic-Opposite-to-Nature-Cure-Hospital-Balkampet/040PXX40-XX40-130624144957-Q5S7_BZDET/reviews
- OBSERVED:
  1. Every CTA is phone-first: "Call Our Clinic : +(91)- 9642659757, 040-40136113" repeated site-wide; "BOOK AN APPOINTMENT" routes to phone.
  2. Contact form is generic WP Contact Form 7; no appointment slots.
  3. NO WhatsApp deep link (only the word "WhatsApp" appears — no `wa.me`/`api.whatsapp.com` href in HTML).
  4. Instagram `instagram.com/drmadhaviskinclinic` + Facebook present. Email `madhavisskinclinic@gmail.com`.
  5. Visible negative reviews retrieved on Justdial: "Pathetic treatment DR MADHAVI RUINED MY FACE"; "Unsanitised · No follow-up care"; "Unprofessional and unethical doctor..."; and a Justdial summary flagging "long waiting times... 60 to 90 minutes" and "money-oriented management".
  6. Recent rating trend on Justdial includes 1.0 and 2.0 entries.
  7. Clinic runs ~10:00–13:00 and 18:00–20:30 (per threebestrated listing) — narrow windows.
- INFERRED: Negative reviews appear to be left standing without visible owner responses in the excerpts retrieved (full set not exhaustively checked) → reputation damage compounds in the same search results new patients read.
- UNKNOWN: Whether the clinic replies to Google/Justdial reviews; actual reply times.
- LIKELY COMMERCIAL EFFECT: Aesthetics/derm is review-driven; a "ruined my face" 1★ on the listing new patients land on directly suppresses conversion. 60–90 min waits kill word-of-mouth referrals. Recoverable revenue without spending a rupee on ads.
- WHAT WE'D CHANGE: A review-response playbook (respond + move complaining patients to a private channel), wait-time reduction via appointment slotting, and a WhatsApp click-to-chat with auto-ack.
- IMPLEMENTATION COMPLEXITY: Med (reputation management needs consistency)
- WHY RELEVANT: This is the clearest, most concrete pain in the set — public negative reviews + wait complaints + phone-only booking. High urgency, high storytelling value.
- PROPOSED PILOT: Draft & schedule responses to the specific negative reviews; install WhatsApp click-to-chat + auto-ack. 2-week trial.
- DECISION MAKER: Dr. Madhavi Pudi, MBBS, DNB — Founder/Dermatologist (publicly listed)
- CONTACT ROUTE: +91 96426 59757 / 040-4013 6113; madhavisskinclinic@gmail.com; Instagram DM
- CONTACT CONFIDENCE: HIGH
- INDICATIVE PRICING [ESTIMATE]: Setup ₹4,000–7,000; ₹3,000–6,000/month (reputation + booking).
- EVIDENCE: https://madhavisskinclinic.in/ · https://madhavisskinclinic.in/contact-us/ · https://threebestrated.in/dermatologist-doctors-in-hyderabad-ts · Justdial reviews link above

---

## 4. Dr Praneeth Skin. Hair. Laser Clinic
- CATEGORY: Dermatology (clinical + cosmetic, laser)
- LOCATION: #16-31-481/101, JB Shashi Arcade, 2nd Floor, JNTU Rd, above Bandhan Bank, KPHB Colony, Kukatpally, Hyderabad 500085
- WEBSITE: https://www.drpraneethclinic.com/
- REVIEWS: Justdial 4.7 / 451 ratings — https://www.justdial.com/Hyderabad/Dr-Praneeth-Skin-Hair-Laser-Clinic-Above-Bandhan-Bank-KPHB-Colony/040PXX40-XX40-180531134020-V8C7_BZDET/reviews
- OBSERVED:
  1. "Make An Appointment" links to https://www.drpraneethclinic.com/appointment/ — fetched page contains **no form** (curl found no `<form>` tag; only phone numbers + `drpraneethclinic@gmail.com`).
  2. Site FAQ says you can "book Dr. Praneeth's appointment through the website" — but the website booking page has no input fields (dead-end CTA).
  3. NO WhatsApp deep link in HTML (only the word "WhatsApp").
  4. Instagram `instagram.com/drpraneethclinic` + Facebook linked. Email is a Gmail address.
  5. Hours Mon–Sat 10:00–13:00 and 17:00–20:00 (split, ~6 hrs/day); single doctor.
  6. Justdial "What users liked" shows no negatives listed, but the site's public FAQ "how can I take appointments" answer is phone-only in practice.
- INFERRED: Every "book online" intent funnels into a phone call during narrow hours; the appointment page is a conversion dead end. After-hours and lunch-hour enquiries are lost with no capture.
- UNKNOWN: How many of the /appointment/ visits bounce; whether phone is answered reliably.
- LIKELY COMMERCIAL EFFECT: Cosmetic derm (laser packages ₹5k–₹40k) attracts a digital-native, Instagram-discovered audience that expects a form at 11 pm — a phone-only path silently drops them.
- WHAT WE'D CHANGE: Turn the dead /appointment/ page into a real short form (name, phone, concern, preferred time) with auto-reply + WhatsApp fallback; publish starting prices for 2–3 hero treatments.
- IMPLEMENTATION COMPLEXITY: Low (single page fix)
- WHY RELEVANT: The clinic already *promises* website booking (FAQ) — we're not inventing a need, just making the promised path actually work. Very easy first "win".
- PROPOSED PILOT: Ship the appointment form on /appointment/ + auto-reply in 48 hrs; measure enquiries in 2 weeks.
- DECISION MAKER: Dr. P. Praneeth Kumar Reddy — Founder, Dermatologist/Venereologist (publicly listed)
- CONTACT ROUTE: 040-4855 3939 / +91 9704 946 534; drpraneethclinic@gmail.com; Instagram DM
- CONTACT CONFIDENCE: HIGH
- INDICATIVE PRICING [ESTIMATE]: Setup ₹3,000–5,000; ₹2,000–4,000/month.
- EVIDENCE: https://www.drpraneethclinic.com/ · https://www.drpraneethclinic.com/appointment/ (no form) · https://www.drpraneethclinic.com/contact-us/ · Justdial reviews link above

---

## 5. Vem Speciality Clinics
- CATEGORY: Orthopaedics & Spine (+ Dermatology/trichology at same clinic)
- LOCATION: Plot no. 1213, 1st Floor, Swamy Ayyappa Society, Mega Hills, Madhapur, Hyderabad 500081
- WEBSITE: https://vemspecialtyclinics.com/
- REVIEWS: Justdial 3.9 / 117 ratings (clinic) — https://www.justdial.com/Hyderabad/VEM-SPECIALITY-CLINIC-Near-Hanuman-Temple-Madhapur/040PXX40-XX40-180512113606-W8M6_BZDET ; Dr. Krishna Bhargava Vem 4.7 / 119 ratings
- OBSERVED:
  1. Site advertises "Book an Appointment" and "ONLINE CONSULTATION" — but no booking form exists on the site (curl found only a site-search `<form>`), so both CTAs are non-functional as booking paths.
  2. WhatsApp deep link `wa.me/918374345767` present on homepage and contact page.
  3. Contact page lists +91 40-42203987 and +91 837 434 5767; the only email in source is `prakapagoti27@gmail.com` (appears to be a developer/webmaster address, not a clinic inbox).
  4. Justdial "What can be improved": "High charges for services", "Money-oriented management", "Delayed consultations and appointments".
  5. Clinic rating (3.9) is materially below the lead doctor's personal rating (4.7) → the *facility* experience is the weak link, not the surgeon.
  6. Practo profile exists (fee ₹400–500, Madhapur) and Pristyn lists a bookable slot.
- INFERRED: Patients research the surgeon (4.7), arrive, and are disappointed by facility/pricing/delays (3.9). The two dead booking CTAs push people to aggregators (Practo/Pristyn) where the clinic doesn't control the narrative or the fee.
- UNKNOWN: Whether WhatsApp enquiries are answered; who owns the site inbox.
- LIKELY COMMERCIAL EFFECT: Spine/ortho cases are ₹80k–₹3L+. A 3.9 clinic rating depresses inbound; every enquiry deflected to an aggregator risks losing the case or paying a commission.
- WHAT WE'D CHANGE: Make "Book Appointment"/"Online Consultation" a real form with a clinic-owned email; publish transparent consultation fees; systematic review-request after successful surgeries to lift the 3.9.
- IMPLEMENTATION COMPLEXITY: Med
- WHY RELEVANT: Two prominent CTAs that literally do nothing is an unusually clean, demonstrable defect — and the surgeon-vs-clinic rating gap is a persuasive story.
- PROPOSED PILOT: Convert the two CTAs into a working appointment form + clinic email; add post-visit review request. 30-day measurement.
- DECISION MAKER: Dr. Krishna Bhargava Reddy — Consultant Orthopaedic & Spine Surgeon, MBBS, MS(Ortho), FISS (publicly listed)
- CONTACT ROUTE: +91 40-42203987 / +91 837 434 5767; WhatsApp wa.me/918374345767; Practo profile
- CONTACT CONFIDENCE: MEDIUM (phone + WhatsApp verified; email is an unverified developer address)
- INDICATIVE PRICING [ESTIMATE]: Setup ₹5,000–9,000; ₹3,000–6,000/month.
- EVIDENCE: https://vemspecialtyclinics.com/ · https://vemspecialtyclinics.com/contact-us/ · https://www.practo.com/hyderabad/clinics/spine-surgery-clinics/hitech-city · Justdial reviews link above

---

## 6. DakshinRehab (Physiotherapy & Neuro Rehabilitation Centre) — CONTROL / best-in-class
- CATEGORY: Physiotherapy & Neuro-rehabilitation (inpatient + OPD)
- LOCATION: 3rd Floor, ARD Magnum, Green Hills Rd, Moosapet, Kukatpally, Hyderabad 500018
- WEBSITE: https://www.dakshinrehab.ai/
- REVIEWS: Site claims 4.8 (100+ Google reviews); HexaHealth lists 4.4/5 (87 ratings) — https://www.hexahealth.com/hyderabad/doctor/dr-sujith-omkaram-paediatric-orthopaedician
- OBSERVED:
  1. Full online booking flow present ("Book Free Assessment"); free assessment explicitly gated: "Your initial assessment is free only when you book an appointment online and attend your confirmed time slot."
  2. WhatsApp `wa.me/918019299888`, phone +91 80192 99888, domain email `info@dakshinrehab.ai`.
  3. Condition-specific landing pages (stroke, sports injury, pediatric, inpatient neuro-rehab) — real SEO/content engine.
  4. OPD 9:00–20:00 all days incl. Sunday; inpatient visiting hours stated.
  5. No published price for physio sessions / treatment packages.
- INFERRED: This clinic already has the capture + booking + content stack most peers lack → it is a benchmark, and a poor *first* cold-outreach target (little obvious pain). Better used as a "what good looks like" reference in the niche table.
- UNKNOWN: Booking-to-show rate; whether "free assessment" gating causes friction complaints.
- LIKELY COMMERCIAL EFFECT: Low immediate upside from a booking fix; upside is marginal (pricing transparency, review volume) rather than structural.
- WHAT WE'D CHANGE (if engaged): Publish package pricing; simplify the very content-dense enquiry path to a single 2-field form.
- IMPLEMENTATION COMPLEXITY: Low (but low need)
- WHY RELEVANT: Serves as the control showing which fixes are standard practice — sharpens the pitch to clinics (3,4,5) that are missing them.
- PROPOSED PILOT: Not recommended as a first pilot; keep on a "later / benchmark" list.
- DECISION MAKER: Named clinical lead not publicly stated (site is brand-led) — UNKNOWN
- CONTACT ROUTE: +91 80192 99888; WhatsApp wa.me/918019299888; info@dakshinrehab.ai
- CONTACT CONFIDENCE: HIGH (contact routes); LOW for decision-maker name
- INDICATIVE PRICING [ESTIMATE]: n/a (benchmark only)
- EVIDENCE: https://www.dakshinrehab.ai/ · https://www.dakshinrehab.ai/contact

---

## 7. Aanvi Fertility & Women's Centre
- CATEGORY: IVF / Fertility + women's care
- LOCATION: Shop No 1075/15/1–5, Tilaknagar X Roads, Shivam Rd, Nallakunta, Hyderabad 500044
- WEBSITE: https://www.aanviivf.com/ (second brand site: https://www.drswarna.com/)
- REVIEWS: Justdial 4.8 / 231 ratings — https://www.justdial.com/Hyderabad/Aanvi-Fertility-and-Womens-Centre-Nallakunta-Nallakunta/040PXX40-XX40-220423231014-A9J8_BZDET ; GarbhSaathi shows only ~5 Google reviews
- OBSERVED:
  1. Booking form on homepage (`id="bookingForm"`) + Elementor popup form.
  2. WhatsApp `api.whatsapp.com/send?phone=7386183535`; email `aanviivf@gmail.com`; Instagram `instagram.com/aanvi_fertility_centre` + Facebook.
  3. Two live websites for the same doctor/practice (aanviivf.com and drswarna.com) — fragmented presence.
  4. Justdial "can be improved": "confusion in remembering patients", "lack of clarity in providing estimated delivery dates"; one negative review about an argument with the doctor.
  5. Google review volume is thin (~5) versus ~231 on Justdial.
  6. No published IVF package pricing on the site.
- INFERRED: The practice has accumulated trust on Justdial but has not converted it to Google — the channel where most new patients now search. Duplicate sites split SEO authority.
- UNKNOWN: Enquiry response time; consultation-to-treatment conversion.
- LIKELY COMMERCIAL EFFECT: IVF cycles run ₹1.5L–₹2L+. Being under-visible on Google while strong on a declining aggregator = systematically losing first-time discovery, the top of a very high-value funnel.
- WHAT WE'D CHANGE: Consolidate to one site; systematic Google review capture (target 100+); add an enquiry auto-reply with a "what to expect" response to reduce "lack of clarity" complaints.
- IMPLEMENTATION COMPLEXITY: Med
- WHY RELEVANT: High ticket value + a concrete, fixable visibility gap (Justdial strong, Google thin) + duplicate-site confusion.
- PROPOSED PILOT: Google review-request flow (post-consultation SMS/WhatsApp) + auto-ack on the existing booking form.
- DECISION MAKER: Dr. Swarna — Founder, MBBS, DGO, DRM, Gynecologist & IVF Specialist (publicly listed)
- CONTACT ROUTE: +91 95153 73535 (listing) / WhatsApp 7386183535; aanviivf@gmail.com; Instagram DM
- CONTACT CONFIDENCE: MEDIUM-HIGH
- INDICATIVE PRICING [ESTIMATE]: Setup ₹5,000–9,000; ₹4,000–7,000/month.
- EVIDENCE: https://www.aanviivf.com/ · https://www.drswarna.com/ · https://www.garbhsaathi.in/clinics/hyderabad · Justdial link above

---

## 8. Fertilica IVF & Women Care
- CATEGORY: IVF / Fertility
- LOCATION: 8-2-681/7, 3rd Floor, Rd No. 12, Banjara Hills (HQ) + Karmanghat/Saroor Nagar, Hyderabad
- WEBSITE: https://www.fertilicaivf.com/
- REVIEWS: Miro Fertility lists 4.9 / 239 reviews (IVF cost est. ₹1.1–1.9L) — https://www.mirofertility.com/clinics/hyderabad/area/banjara-hills ; LinkedIn https://www.linkedin.com/company/fertilicaivf
- OBSERVED:
  1. NO enquiry/booking form on the homepage (curl found no `<form>`); lead capture is WhatsApp/phone only.
  2. WhatsApp deep link in source: `api.whatsapp.com/send?phone=+919...1115` (number resolves to 99499 91115 in page text).
  3. Instagram `instagram.com/fertilicaivf` + Facebook + active LinkedIn company page.
  4. Email is a Gmail address (`fertilicaivf@gmail.com`) despite premium positioning and ₹1.1–1.9L treatment cost.
  5. Site is a small custom static site (a few pages); no blog/content engine, despite fertility being a high-intent search category.
  6. Site markets "affordable, ethical, and transparent fertility care" but publishes no figures.
- INFERRED: With no form and a Gmail inbox, after-hours enquiry volume from a high-intent, emotionally-urgent audience is lost; there is no content to capture organic "IVF cost / success rate Hyderabad" searches.
- UNKNOWN: WhatsApp/phone response SLA; whether an enquiry-tracking system exists.
- LIKELY COMMERCIAL EFFECT: Fertility is the highest-value category here; a single recovered enquiry is worth more than a year of any retainer. Every night-time enquiry with no capture is direct lost revenue.
- WHAT WE'D CHANGE: Add a discreet enquiry form + auto-reply (fertility enquirers prefer asynchronous first contact); move to a clinic-branded email; build 3–5 decision-stage content pages (cost, success rates, process).
- IMPLEMENTATION COMPLEXITY: Med
- WHY RELEVANT: Highest ticket value in the set + a clean, verifiable defect (no form) + a Gmail credibility mismatch on a premium service.
- PROPOSED PILOT: Enquiry form + WhatsApp auto-ack on the existing site; 2-week lead-count baseline.
- DECISION MAKER: Dr. Sumina Reddy — Founder (publicly listed on site/LinkedIn)
- CONTACT ROUTE: WhatsApp +91 99499 91115; fertilicaivf@gmail.com; Instagram DM; LinkedIn company page
- CONTACT CONFIDENCE: MEDIUM-HIGH
- INDICATIVE PRICING [ESTIMATE]: Setup ₹5,000–10,000; ₹4,000–8,000/month.
- EVIDENCE: https://www.fertilicaivf.com/ · https://www.mirofertility.com/clinics/hyderabad/area/banjara-hills · https://www.linkedin.com/company/fertilicaivf

---

# Niche comparison table

| # | Business | Category | Area | Online booking form? | WhatsApp? | Instagram/FB? | Own-domain email? | Rating (source) | Clearest observable gap | Priority |
|---|----------|----------|------|----------------------|-----------|----------------|--------------------|-----------------|-------------------------|----------|
| 1 | Dr White Dental Care | Dental | Madinaguda/Nizampet | Yes (generic) | Yes (both branches) | Yes | Yes (dwdc.in) | 5.0 Justdial / 4.9 site | No slot booking; two disjoint numbers | Med |
| 2 | Krishna's Dant Ayush | Dental | Madhapur | WhatsApp-only | Yes | **No** | **No** | 5.0 Google (count n/a) | 100% WhatsApp-dependent, Sunday closed | Med |
| 3 | Dr Madhavi's Skin Clinic | Dermatology | Balkampet (SR Nagar) | No (phone CTA) | **No link** | Yes | No (Gmail) | 4.4 Justdial | Public 1★ "ruined my face" + 60–90m waits | **High** |
| 4 | Dr Praneeth Skin.Hair.Laser | Dermatology | KPHB | **No** (dead page) | **No link** | Yes | No (Gmail) | 4.7 Justdial | /appointment/ page has no form | **High** |
| 5 | Vem Speciality Clinics | Ortho/Spine | Madhapur | **No** (dead CTAs) | Yes | No link found | No (webmaster Gmail) | 3.9 clinic / 4.7 doctor | Two dead CTAs; 3.9 clinic rating | **High** |
| 6 | DakshinRehab | Physio/Neuro | Moosepet | **Yes (real)** | Yes | — | Yes (.ai) | 4.8 Google | (benchmark — few gaps) | Low |
| 7 | Aanvi Fertility | IVF | Tilaknagar | Yes | Yes | Yes | No (Gmail) | 4.8 Justdial / ~5 Google | Justdial strong, Google thin; 2 sites | **High** |
| 8 | Fertilica IVF | IVF | Banjara Hills | **No** | Yes | Yes + LinkedIn | No (Gmail) | 4.9 / 239 reviews | No form; Gmail on premium brand | Med-High |

## Cross-cutting patterns (the niche thesis)
- **Booking forms are frequently decorative.** 4 of 8 (Madhavi's, Praneeth, Vem, Fertilica) either have no form, a dead-end "appointment" page, or CTAs that link nowhere. This is the single most repeatable, demonstrable defect.
- **WhatsApp is used as a crutch, not a system.** Where present (Krishna's, Dr White, Vem, DakshinRehab, Aanvi, Fertilica) it has no auto-ack/fallback, so coverage depends on a human at the phone.
- **Gmail dominates.** 6 of 8 use a Gmail address even at premium price points — a cheap credibility fix.
- **Aggregator-vs-Google mismatch is common** (Aanvi: 231 Justdial vs ~5 Google; Madhavi's: 2.1k Justdial ratings but visible 1★ left standing).
- **Highest-value, most-defective targets:** Madhavi's (reputation + wait), Praneeth (dead booking page), Vem (dead CTAs + 3.9 rating), Aanvi (Google visibility), Fertilica (no form).

## Suggested first-contact order
1. Dr Praneeth (dead page — easiest, most concrete "we fixed your booking page" demo)
2. Dr Madhavi's (reputation + waits — high pain, clear storytelling)
3. Vem Speciality (two CTAs that do nothing + rating gap)
4. Fertilica IVF (highest ticket, no form)
5. Aanvi Fertility (Google visibility gap)
6. Krishna's Dant Ayush / Dr White (channel maturity, subtler)
7. DakshinRehab (benchmark, defer)
