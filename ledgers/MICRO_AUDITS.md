# MICRO-AUDITS (local business engine)
Batch 1 — Hyderabad high-ticket services (real estate, wedding venues, planners, photographers). Built 2026-10-02 (UTC).
Rule: PUBLIC info only. Every numbered OBSERVED item is from a fetched page/snippet cited in EVIDENCE URLs. INFERENCE is labelled. No fabricated problems or contacts. Prices = ESTIMATE unless cited.
Format per business: BUSINESS / CATEGORY / LOCATION / WEBSITE / GBP+reviews / OBSERVED (n) / INFERRED / UNKNOWN / LIKELY COMMERCIAL EFFECT / WHAT WE'D CHANGE / COMPLEXITY / WHY RELEVANT / PROPOSED PILOT / DECISION MAKER / CONTACT ROUTE / CONTACT CONFIDENCE / INDICATIVE PRICING [ESTIMATE] / EVIDENCE URLs

GBP links below are Google Maps search deep-links (verifiable; not a claimed GBP ID).

---

## 1. Vertex Homes Pvt Ltd — real estate BUILDER
- CATEGORY: Real estate builder (premium apartments/villas; est. 1994; "32 projects" per Housing.com)
- LOCATION: Corporate office — 4th Floor, Plot 8 & 9, Jubilee Enclave, Opp. HITEX, Madhapur, Hyderabad 500081
- WEBSITE: https://vertexhomes.com/
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=Vertex+Homes+Madhapur+Hyderabad ; Justdial 4.0/686 ratings; project-level Google 4.2/118 (Vertex Kingston Park, Wanderlog)
- OBSERVED:
  1. Enquiry is project-gated: a `main1` form posts to `project-redirect.php` (fields: type, location, project) and a second `home` contact form posts to `/include/mail-new.php` using opaque field IDs (`field31228`, `field31229`, `field15714`…) — no semantics, lead routing not visible. [raw HTML]
  2. No `tel:`, `mailto:`, or WhatsApp link in the homepage HTML — no click-to-call; contact only after form/JS. [raw HTML grep]
  3. No online availability/booking calendar; only "Enquire Now"/"Get a Quote". [site + project pages]
  4. Justdial's review synthesis reports buyers flagging the "sales and CRM team" for "lack of respect and hospitality after the initial site visit" and "maintenance issues… delays in addressing them even after several follow-ups". [Justdial]
  5. Prices gated ("Get a Quote"); Vertex 33 West (Nallagandla) listed ₹1.20 Cr–₹1.83 Cr onward. [homznspace]
- INFERRED: Inbound leads likely land in a generic PHP-mail pipeline with no visible CRM/pipeline or acknowledgement; post-site-visit follow-up is a documented weak point; no enquiry→booking visibility → high-value leads can go cold.
- UNKNOWN: CRM in use; response-time SLA; monthly enquiry volume; whether form notifications reliably reach a sales owner.
- LIKELY COMMERCIAL EFFECT: One unit sale ₹1.2–1.8 Cr; ESTIMATE contribution ₹15–40L/unit. A single lost high-intent enquiry (5–15% conversion) ⇒ ₹50k–₹2.5L expected; a lost booking ⇒ ₹15–40L contribution. [ESTIMATE]
- WHAT WE'D CHANGE: Auto-acknowledge + route every enquiry to a named owner with a 3-touch follow-up; instrument a simple pipeline (new→contacted→site visit→quote→booked); post-visit recovery nudge.
- COMPLEXITY: Low–Medium (form webhook + lightweight CRM + follow-up automation).
- WHY RELEVANT: A lost lead = a lost 7-figure sale; post-visit follow-up is a documented complaint.
- PROPOSED PILOT: Free 3-point enquiry audit; wire existing forms into a tracked pipeline with auto-reply + 3-touch follow-up for one launch project.
- DECISION MAKER: Sales/CRM Head or Marketing Head (name not public). [INFERENCE]
- CONTACT ROUTE: Website enquiry form / Madhapur corporate office / LinkedIn company page.
- CONTACT CONFIDENCE: LOW–MEDIUM
- INDICATIVE PRICING [ESTIMATE]: ₹25,000–50,000 setup + ₹15,000–30,000/mo.
- EVIDENCE: https://vertexhomes.com/ ; https://www.justdial.com/Hyderabad/Vertex-Homes-Pvt-Ltd-Near-Akshya-Patra-Opposite-Hitex-Madhapur/040PXX40-XX40-151229064149-T1M6_BZDET ; https://www.homznspace.com/vertex-33-west-nallagandla-hyderabad/ ; https://wanderlog.com/place/details/15064266/vertex-kingston-park

---

## 2. Vishwa Properties — real estate BROKER/consultant
- CATEGORY: Real estate consultant (residential + commercial; buy/sell/invest)
- LOCATION: Plot No. 42, Main Road, Near Alkapoor Township, Manikonda, Hyderabad 500089
- WEBSITE: https://www.vishwaproperties.com/
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=Vishwa+Properties+Manikonda+Hyderabad ; no reliable aggregate review count found (a Justdial "Vishwa Property Wala" 5.0/42 is possibly a different entity)
- OBSERVED:
  1. Homepage contains EIGHT separate enquiry forms (buy / sell / invest split); contact page adds 3 more — fragmented intake, no single capture point. [raw HTML form count]
  2. Fields are unstructured free-text ("e.g. Puppalaguda, Mokila"; "e.g. ₹1.25 Cr or ₹75,000/Sq.Yd") — no dropdowns/validation. [raw HTML]
  3. WhatsApp CTA with prefilled text (`wa.me/917337307056`), phone `tel:7337307056`, email `contact@vishwaproperties.com`. [raw HTML]
  4. `/contact` returns HTTP 404 (nav uses another path). [curl]
  5. No online viewing scheduler; all enquiries route to WhatsApp/phone. [site]
  6. Acts as "Seller" on portals (e.g., Bhashyam Global City, JBM Apartment on Housing.com). [housing.com]
- INFERRED: Leads arrive across WhatsApp + 11 forms with no visible pipeline; follow-up depends on manual WhatsApp/phone discipline; no SLA and no per-listing enquiry visibility.
- UNKNOWN: Monthly enquiry volume; whether WhatsApp Business quick-replies/catalogue are used; CRM existence.
- LIKELY COMMERCIAL EFFECT: Fee on ₹80L–₹2 Cr deal ≈ ₹80k–₹4L (1–2%) [ESTIMATE]. One lost serious buyer ⇒ ₹80k–₹4L; expected value per enquiry ₹8k–₹40k. [ESTIMATE]
- WHAT WE'D CHANGE: One unified intake + auto-assign + WhatsApp-first acknowledgement within minutes + follow-up sequence + dormant-buyer reactivation matched to new listings.
- COMPLEXITY: Low.
- WHY RELEVANT: Broker economics are won/lost on lead response speed and follow-up; a small team cannot manually track 11 forms.
- PROPOSED PILOT: Consolidate forms + WhatsApp into one tracked pipeline; auto-reply + 3-touch follow-up; report lead→viewing→deal.
- DECISION MAKER: Owner/Principal consultant (name not published). [INFERENCE]
- CONTACT ROUTE: Website form / WhatsApp +91 73373 07056 / contact@vishwaproperties.com / Manikonda office.
- CONTACT CONFIDENCE: MEDIUM (published business phone + email).
- INDICATIVE PRICING [ESTIMATE]: ₹15,000–30,000 setup + ₹8,000–15,000/mo.
- EVIDENCE: https://www.vishwaproperties.com/ (raw HTML) ; https://housing.com/in/buy/projects/page/244746-bhashyam-global-city-by-bhashyam-developers-in-shamshabad

---

## 3. The Environ® – Convention — wedding VENUE
- CATEGORY: Wedding/convention venue (11 acres; 200–3,000 guests)
- LOCATION: Survey No. 65, Mansanpalle Village, Maheshwaram Mandal, near Shamshabad, Hyderabad 509325
- WEBSITE: https://www.theenviron.in/
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=The+Environ+Convention+Shamshabad ; Justdial 4.7/64 ratings + 5.0/95 ratings (two listings); Justdial "Booking Price ₹300,000"
- OBSERVED:
  1. Enquiry form (WordPress Contact Form 7) captures Name, Email, Phone, type-of-event, Event Date, expected-number-of-guests — but is repeated 3–4× on the page. [raw HTML]
  2. No online availability calendar / real-time date picker; enquiries are manual callbacks. [site]
  3. Single `tel:6292252525`; NO WhatsApp link on the site (Justdial lists a different number +91 8971833160 + WhatsApp). [raw HTML; Justdial]
  4. SEO-heavy copy ("Best Convention Hall in Hyderabad" repeated) with no booking system or instant quote. [site]
  5. Justdial: "High call pick up rate" (positive) and starting booking price ₹3,00,000. [Justdial]
- INFERRED: ₹3L+ venue enquiries depend on manual callbacks; no automated date-conflict capture; aggregator leads cost commission.
- UNKNOWN: Enquiry volume; callback SLA; whether CF7 notifications are routed and actioned.
- LIKELY COMMERCIAL EFFECT: One lost booking ≈ ₹3,00,000 rental + F&B (plates ₹1,400–1,800 cited) ⇒ ₹3–8L [ESTIMATE]; peak dates amplify.
- WHAT WE'D CHANGE: Instant acknowledgement + date-availability check + structured 3-touch follow-up; auto-send package PDF + site-visit slots; simple pipeline.
- COMPLEXITY: Low–Medium.
- WHY RELEVANT: One booking is worth lakhs and dates are perishable; a slow callback loses.
- PROPOSED PILOT: Add instant auto-reply + 3-touch follow-up + date/lead tracker to the existing CF7 form for one quarter.
- DECISION MAKER: Owner/Sales Head (not published). [INFERENCE]
- CONTACT ROUTE: Site form / 62 92 25 25 25 / Justdial enquiry.
- CONTACT CONFIDENCE: MEDIUM.
- INDICATIVE PRICING [ESTIMATE]: ₹20,000–40,000 setup + ₹12,000–25,000/mo.
- EVIDENCE: https://www.theenviron.in/ ; https://www.justdial.com/Hyderabad/Party-Lawns-in-Janwada/nct-11235621 ; https://www.justdial.com/Rangareddy/The-Environ-Convention-Near-Shamshabad-Shamshabad/040PXX40-XX40-260307122421-I9C3_BZDET

---

## 4. The Vintage Palace — wedding VENUE / banquet
- CATEGORY: Banquet hall / wedding venue (est. 2016; up to ~3,000 guests)
- LOCATION: Pillar No. 102, Golconda Road, Karwan West, Hyderabad 500006
- WEBSITE: NONE (Justdial shows "Website: +Add Website"); discovery via aggregators
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=The+Vintage+Palace+Karwan+Hyderabad ; Google ~4.3–4.4 from ~7,500–7,900 reviews (LBB 4.4; bestmuslimmarriage 4.3/7,913); Justdial 4.0/8,082
- OBSERVED:
  1. No owned website — Justdial literally shows "Website: +Add Website". All online discovery runs through aggregators (Mandap, WeddingWire, Weddingz, Justdial). [Justdial]
  2. Booking is via aggregators: Mandap page says "contact us and book us via the Mandap.com team". [Mandap]
  3. Rigid terms: "70% payment on booking, 30% payment on date, cancellation policy – Non Refund". [Mandap]
  4. Policy: "Outside decorators not allowed"; prices — Hall ₹1,00,000, Lawn ₹2,45,000, Hall 2 ₹85,000. [Mandap]
  5. Recurring review complaints: "Lack of air circulation in some areas" and "Flies in the dining area… unhygienic". [Justdial summary]
- INFERRED: Zero owned lead channel → every enquiry is portal-mediated (commission + no CRM); recurring review themes left unaddressed; no direct booking funnel.
- UNKNOWN: WhatsApp Business use; who answers aggregator leads; response times.
- LIKELY COMMERCIAL EFFECT: One lost booking ≈ ₹85,000–₹2,45,000 rental + catering [ESTIMATE]. With ~8k reviews, recovering even a small share of off-portal enquiries is material.
- WHAT WE'D CHANGE: Minimal direct enquiry channel (single page + WhatsApp + auto-reply) to capture commission-free leads; review-response playbook for the recurring aeration/hygiene complaints.
- COMPLEXITY: Low.
- WHY RELEVANT: An 8k-review venue with no website is leaking direct enquiries; negative themes unanswered.
- PROPOSED PILOT: 1-page direct enquiry + WhatsApp auto-responder (date/guests), plus replies to the top recurring review complaints.
- DECISION MAKER: Owner/Manager (not published). [INFERENCE]
- CONTACT ROUTE: +91 91603 74743 / Justdial / Mandap enquiry.
- CONTACT CONFIDENCE: MEDIUM.
- INDICATIVE PRICING [ESTIMATE]: ₹20,000–35,000 setup + ₹10,000–20,000/mo.
- EVIDENCE: https://www.justdial.com/Hyderabad/The-Vintage-Palace-Pillar-No102-Karwan/040PXX40-XX40-160820110934-W3X7_BZDET ; https://www.mandap.com/hyderabad/the-vintage-palace-in-karwan ; https://lbb.in/hyderabad/best-wedding-venues-banquet-halls/ ; https://www.bestmuslimmarriage.com/blog/top-5-areas-in-hyderabad-known-for-perfect-muslim-matrimony-events-and-gatherings

---

## 5. Weddin Events — wedding PLANNER
- CATEGORY: Wedding & event planner (12+ yrs claimed; 160+ services)
- LOCATION: Bandlaguda Jagir (Shop No 2) + Madhapur (4th Floor, 529-B, Rd No. 11, Kakatiya Hills, Kavuri Hills)
- WEBSITE: https://weddin.in/
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=Weddin+Events+Madhapur+Hyderabad ; site claims "550+ Google reviews"; Justdial 5.0/143; addagio 5.0/59; nimntrn "81+ Google reviews"
- OBSERVED:
  1. Contact page has NO HTML form — it renders "Please enable JavaScript to use our website" and falls back to Call/WhatsApp only. [raw HTML: 0 forms]
  2. Review-count claims conflict: homepage asserts "550+ Verified 5-Star Google Reviews" vs third-party counts of ~59 (addagio), ~81 (nimntrn), 143 (Justdial). [weddin.in; addagio; nimntrn; Justdial]
  3. No online booking/availability system; enquiry is phone/WhatsApp ("free consultation", "call within 2 hours"). [site]
  4. Pricing hidden ("Call for a free consultation"); a Justdial listing shows "Wedding Planning starting at ₹2,50,000". [site; Justdial]
  5. Claims vary across their own properties: weddin.in "500+ events / 12 yrs"; weddin.blog "1,000 events / 1,200+ families". [weddin.in; weddin.blog]
- INFERRED: Lead intake is phone-heavy with no form fallback for out-of-hours or overseas (NRI) enquiries; inflated/inconsistent claims risk trust; no enquiry→consultation→booking tracking.
- UNKNOWN: Whether a form exists behind JS; true review count; enquiry volume.
- LIKELY COMMERCIAL EFFECT: One planning engagement ≈ ₹2.5L+ fee [Justdial] and controls a multi-lakh budget [ESTIMATE ₹2.5–8L+].
- WHAT WE'D CHANGE: Robust no-JS form + instant auto-reply/booking link; unify review claims to a verified figure; simple enquiry→consultation→booking pipeline.
- COMPLEXITY: Low.
- WHY RELEVANT: Full-stack planner; enquiries blocked when JS fails are pure loss; inconsistent social proof undercuts premium pricing.
- PROPOSED PILOT: Working enquiry form + auto-acknowledge + 3-touch follow-up; reconcile review claim to a verified number.
- DECISION MAKER: Founder/Owner (name not published on site). [INFERENCE]
- CONTACT ROUTE: +91 94411 00609 / WhatsApp / Madhapur office.
- CONTACT CONFIDENCE: MEDIUM–HIGH (published phone + WhatsApp + two offices).
- INDICATIVE PRICING [ESTIMATE]: ₹20,000–40,000 setup + ₹12,000–25,000/mo.
- EVIDENCE: https://weddin.in/ ; https://weddin.in/contact ; https://addagio.io/ko/directory/wedding-planners/hyderabad ; https://nimntrn.com/stories/perfect-wedding-hyderabad-2026-vendor-guide ; https://www.justdial.com/Hyderabad/Event-Organisers-For-Navratri/nct-11204426 ; https://weddin.blog/

---

## 6. Yellow Planners — wedding PLANNER
- CATEGORY: Wedding & event planner (est. 2014)
- LOCATION: 4th Floor, 1-64/K/2, opp. Kakatiya Hills Arch, Kavuri Hills Phase 3, Madhapur Rd, Jubilee Hills, Hyderabad 500033
- WEBSITE: https://yellowplanners.com/
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=Yellow+Planners+Jubilee+Hills+Hyderabad ; site claims 4.9 Google; Justdial 4.6/29 (Banjara Hills) & 4.7/119 (Kavuri Hills); wanderlog Google 4.8/22; magicpin 4.9/125; LBB 4.5
- OBSERVED:
  1. Contact page's click-to-call is BROKEN: raw HTML contains `tel:+91` with no number — tapping does nothing. [raw HTML grep]
  2. Contact details inconsistent: site shows phone 8099551438 + email `yellowplannersenquiries@gmail.com` (a Gmail, not a branded domain) + WhatsApp 9700890890; LBB lists 080995 51438; other listings differ. [raw HTML; LBB]
  3. Contact form exists (Elementor: Name, Email, Mobile, Date of Event + more) but there is no auto-reply/booking confirmation and no availability calendar. [raw HTML]
  4. Site's body links out to weddingwire.in; a template footer credits "Toucan solutions". [site]
  5. Claims vary: homepage "650+ weddings / 900+ events / 4.9 Google / 200+ 5-star reviews" vs Justdial 29–119 ratings. [yellowplanners.com; Justdial]
- INFERRED: Broken click-to-call + Gmail inbox + inconsistent numbers = measurable missed enquiries; no pipeline/SLA; review claims outrun verifiable counts.
- UNKNOWN: True review count; who monitors the Gmail inbox; enquiry volume.
- LIKELY COMMERCIAL EFFECT: Full-service planning fees ₹2.5–8L+ [ESTIMATE, anchored to Weddin's ₹2.5L start]; one lost enquiry that books = ₹2.5L+ fee.
- WHAT WE'D CHANGE: Fix click-to-call/WhatsApp routing; move leads off a personal Gmail into a captured inbox + instant auto-reply; add consult scheduling; align social proof to verified counts.
- COMPLEXITY: Low.
- WHY RELEVANT: A long-established, high-volume planner with a visibly broken primary CTA — the clearest "free win" in the set.
- PROPOSED PILOT: Repair CTA + auto-acknowledge every enquiry within minutes + 3-touch follow-up + simple booking/consult tracker.
- DECISION MAKER: Founder Chunduri Phani (public on about page). [FACT]
- CONTACT ROUTE: +91 80995 51438 / WhatsApp 9700890890 / form / Madhapur office.
- CONTACT CONFIDENCE: MEDIUM–HIGH (named founder + published phone).
- INDICATIVE PRICING [ESTIMATE]: ₹20,000–40,000 setup + ₹12,000–25,000/mo.
- EVIDENCE: https://yellowplanners.com/ ; https://yellowplanners.com/contact-us-yellow-planners/ ; https://yellowplanners.com/about-us-event-planner/ ; https://www.justdial.com/Hyderabad/Yellow-Planners-Kavuri-Hills-Sri-Rama-Colony/040PXX40-XX40-180824191427-T7A1_BZDET ; https://lbb.in/hyderabad/top-wedding-planners/ ; https://magicpin.in/Hyderabad/Kavuri-Hills/Entertainment/Yellow-Planners/store/1ccb263/reviews

---

## 7. Photriya Studios — PHOTOGRAPHER
- CATEGORY: Wedding photography & cinematic films (25+ yrs claimed; 4,500+ weddings claimed)
- LOCATION: H.No 1/62/1, Plot 115, 2nd floor, K Square, Madhapur Rd, Kavuri Hills, Jubilee Hills, Hyderabad 500033
- WEBSITE: https://www.photriya.com/
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=Photriya+Studios+Jubilee+Hills+Hyderabad ; Google 4.7/571 (rentechdigital); Justdial 5.0/662; LBB Google 4.7
- OBSERVED:
  1. No enquiry form on the homepage; contact is `tel:+91 9618855959`, a US number `tel:+1 (503) 706-0464`, `wa.me/919849012345`, and email `photriyacs@gmail.com` (a Gmail). [raw HTML]
  2. No online booking/availability calendar; no date-availability check for peak season (Nov–Apr per aggregators). [site]
  3. Third-party entry pricing "₹25,000–₹30,000/Package" (Justdial) sits oddly against the luxury positioning. [Justdial]
  4. Justdial reviews are stale (~7 years old) despite claimed volume. [Justdial]
  5. Second revenue line — Photriya Academy course (₹39,000, 2 months) with its own phone 9618855959. [photriya.com/photriyaacademy]
- INFERRED: High enquiry value + no form + Gmail + no availability system ⇒ manual, leaky intake; a US number implies NRI/destination demand; stale reviews suggest no active review generation.
- UNKNOWN: Enquiry volume; whether WhatsApp is monitored with quick replies; CRM.
- LIKELY COMMERCIAL EFFECT: Candid/premium packages ₹50k–₹2L (WeddingBazaar: average starts ₹50k, up to ₹2–3L) [ESTIMATE]. One lost booking = ₹50k–₹2L.
- WHAT WE'D CHANGE: Enquiry form + instant auto-reply with package/availability + date-hold request; timezone-aware NRI scheduling; post-event review generation.
- COMPLEXITY: Low.
- WHY RELEVANT: Established, high-demand studio leaving NRI/peak-date leads to a US phone + Gmail; dates are perishable.
- PROPOSED PILOT: Add enquiry form + auto-acknowledge + peak-date availability check + post-event review request.
- DECISION MAKER: Venky Mallojjala (Founder, public). [FACT]
- CONTACT ROUTE: +91 96188 55959 / wa.me/919849012345 / photriyacs@gmail.com / office.
- CONTACT CONFIDENCE: MEDIUM–HIGH.
- INDICATIVE PRICING [ESTIMATE]: ₹15,000–30,000 setup + ₹8,000–18,000/mo.
- EVIDENCE: https://www.photriya.com/ ; https://www.photriya.com/photriyaacademy ; https://www.justdial.com/Hyderabad/Photriya-Photography-Near-N-Tv-Office-Masthan-Nagar-Jubilee-Hills/040PXX40-XX40-190814003202-N1X7_BZDET ; https://rentechdigital.com/smartscraper/business-report-details/india/telangana/list-of-photography-studios-in-hyderabad ; https://lbb.in/hyderabad/best-wedding-photographers-hyderabad/

---

## 8. Suguru Weddings — PHOTOGRAPHER
- CATEGORY: Wedding photography & videography
- LOCATION: Banjara Hills / Uday Nagar, Hyderabad
- WEBSITE: https://www.suguruweddings.com/
- GBP/REVIEWS: https://www.google.com/maps/search/?api=1&query=Suguru+Weddings+Banjara+Hills+Hyderabad ; Justdial 4.9/34 ("Suguru Photography")
- OBSERVED:
  1. Site is single-page JS-rendered — raw HTML is only ~2 KB of scripts; content is invisible to crawlers and web-extraction returns empty (CRAWL_EMPTY_CONTENT). [curl 2,188 bytes; extractor error]
  2. Contradictory claims on the same page: "5+ Years Experience / 500+ Happy Couples / 4.9★" AND "9+ Years Experience". [site]
  3. Contact via phone +91-8374962192 and email `info@suguruweddings.com`; "Book Your Event" CTA but no availability calendar/form in raw HTML (JS-only). [site]
  4. Advertises "from ₹50,000"; Justdial shows "Pre Wedding Photography ₹25,000/Event". [site; Justdial]
  5. Runs Google Analytics + Facebook Pixel (gtag G-N7H3W3S5MC, fbevents.js). [raw HTML]
- INFERRED: JS-only site hurts discoverability AND lead capture (no crawlable content, no no-JS fallback form); contradictory claims weaken trust; ad spend (pixel present) leaks the enquiries it generates.
- UNKNOWN: Whether the CTA form functions; true experience/volume; ad spend.
- LIKELY COMMERCIAL EFFECT: One lost booking = ₹50,000–₹1.5L [ESTIMATE, matching advertised ₹50k start]. If ads run (pixel present), every non-converting enquiry is paid-for waste.
- WHAT WE'D CHANGE: Server-rendered/fallback enquiry form + instant auto-reply + availability; reconcile experience claims; capture and follow up every ad-driven enquiry.
- COMPLEXITY: Low–Medium.
- WHY RELEVANT: Paid-traffic signal (pixel) + JS-only intake = paid leads leaking.
- PROPOSED PILOT: Fallback no-JS enquiry form + auto-acknowledge + 3-touch follow-up; align claim numbers.
- DECISION MAKER: Owner (not published). [INFERENCE]
- CONTACT ROUTE: +91 83749 62192 / info@suguruweddings.com.
- CONTACT CONFIDENCE: MEDIUM.
- INDICATIVE PRICING [ESTIMATE]: ₹15,000–30,000 setup + ₹8,000–15,000/mo.
- EVIDENCE: https://www.suguruweddings.com/ (raw HTML ~2 KB) ; https://www.justdial.com/Hyderabad/Photographers/nct-10365365/page-34

---

## NICHE COMPARISON (same engine, 4 categories)
| Niche | One lost enquiry/booking [ESTIMATE] | Observable leak strength | Reachability of buyer | Complexity | Priority |
|-------|--------------------------------------|--------------------------|-----------------------|------------|----------|
| Planner (Yellow Planners) | ₹2.5L+ fee | VERY HIGH (broken CTA, Gmail, no form fallback) | HIGH (named founder) | Low | 1 |
| Venue (Vintage Palace) | ₹85k–₹2.45L rental+F&B | VERY HIGH (no website at all) | MEDIUM | Low | 2 |
| Planner (Weddin) | ₹2.5L+ fee | HIGH (no form, claim mismatch) | MEDIUM-HIGH | Low | 3 |
| Photographer (Suguru) | ₹50k–₹1.5L | HIGH (JS-only, paid pixel, conflicting claims) | MEDIUM | Low-Med | 4 |
| Photographer (Photriya) | ₹50k–₹2L | MEDIUM (no form, Gmail, no availability) | MEDIUM-HIGH (named founder) | Low | 5 |
| Venue (Environ) | ₹3–8L | MEDIUM (form exists, but manual, no calendar) | MEDIUM | Low-Med | 6 |
| Broker (Vishwa) | ₹80k–₹4L | MEDIUM (11 forms, no pipeline) | MEDIUM | Low | 7 |
| Builder (Vertex) | ₹15–40L contribution/booking | MEDIUM (opaque forms, follow-up complaint) | LOW-MED (bigger org) | Low-Med | 8 |

Cross-cutting repeating pains (evidence for standardised product):
1. NO online availability/booking for date-sensitive, high-ticket services (all 8) → a "date-hold + instant availability reply" micro-product.
2. Enquiries land in personal Gmail / WhatsApp / opaque PHP mail with no pipeline or auto-acknowledge (Vertex, Vishwa, Yellow Planners, Photriya, Suguru).
3. Inconsistent contact details and inflated review claims across surfaces (Yellow Planners, Weddin, Suguru) → trust + capture loss.
4. Recurring negative review themes left unanswered/managed (Vintage Palace hygiene/aeration; Vertex post-visit follow-up).

---

# BATCH 2 — Eye / LASIK clinics (Hyderabad). Added 2026-10-03 (UTC) by the Revenue Lab outreach cycle.
New niche (no overlap with Batches prior). Method: raw-HTML lead-capture signal scan of the businesses' PUBLIC pages + web_extract. Same labels/rules: OBSERVED / INFERRED / UNKNOWN; prices ESTIMATE; no fabricated problems or contacts.

## 9. Sree Netralaya Eye Hospital — eye hospital (cataract, LASIK, retina, glaucoma, pediatric)
- WEBSITE: https://www.sreenetralaya.org/
- LOCATION: Hyderabad (multi-specialty eye hospital)
- OBSERVED:
  1. Every booking CTA site-wide is a WhatsApp deep link `wa.me/917799778037` (6 occurrences in the homepage HTML) plus `tel:040-40045670`; NO `<form>` and NO `mailto:` anywhere on the homepage. [raw HTML scan]
  2. Hours published: Mon–Sat 9:00–20:00, Sun 9:00–14:00. [site]
  3. Leadership published: Dr. P. Sreenivasa Rao — Chairman & Managing Director, Phaco/Refractive & LASIK Surgeon. [site]
  4. Resources include Government Schemes + Insurance/TPA pages. [site]
- INFERRED: 100% WhatsApp-dependent intake — if no one answers WhatsApp outside hours, there is no fallback capture and no callback list; no email route published.
- UNKNOWN: WhatsApp response SLA; whether WhatsApp Business quick-replies are used; enquiry volume.
- LIKELY COMMERCIAL EFFECT [ESTIMATE]: cataract/LASIK ₹30k–₹1.5L per eye; missed after-hours chats are lost consultations.
- WHAT WE'D CHANGE: after-hours capture form + WhatsApp auto-responder so a missed chat becomes a logged callback; publish a contact email.
- COMPLEXITY: Low.
- PROPOSED PILOT: WhatsApp auto-reply + after-hours form; measure captured leads for 2 weeks.
- DECISION MAKER: Dr. P. Sreenivasa Rao (public on site). [FACT]
- CONTACT ROUTE: wa.me/917799778037 / 040-40045670.
- CONTACT CONFIDENCE: MED-HIGH (routes published; no email).
- INDICATIVE PRICING [ESTIMATE]: ₹15,000–30,000 setup + ₹8,000–18,000/mo.
- EVIDENCE: https://www.sreenetralaya.org/

## 10. Envision LASIK Centre — LASIK/refractive eye surgery
- WEBSITE: https://envisionlasikcentre.com/
- LOCATION: 3rd Floor, cable bridge road, Road No. 45, Jubilee Hills, Hyderabad 500033
- CLAIMS: "Telangana's largest exclusive LASIK and ICL suite"; WaveLight Plus InnovEyes + SMILE Pro; "30,000+ happy patients". [site]
- OBSERVED:
  1. Capture exists: 3 `<form>` elements + 3 `wa.me/919492820777` links + `tel:9492820777` in raw HTML. [raw HTML scan]
  2. Email is a personal Gmail `envisionlaser@gmail.com` despite premium positioning. [raw HTML]
  3. Hours: Mon–Sat 9:00–20:00, Sun closed. [site]
  4. Founder/lead surgeon named in an on-site quote: Dr. Advaith Sai Alampur. [site]
  5. Confirmation is manual ("Chat Now"/call); no self-serve slot availability observed. [site]
- INFERRED: LASIK is an actively-compared, high-intent purchase; the weak link is confirmation speed + a Gmail inbox, not reach.
- UNKNOWN: enquiry volume; who monitors the Gmail; whether a calendar system exists.
- LIKELY COMMERCIAL EFFECT [ESTIMATE]: LASIK/ICL ₹60k–₹1.5L per case; the centre that confirms availability first usually wins.
- WHAT WE'D CHANGE: instant acknowledgement + slot-availability capture + follow-up for quote-stage enquirers; branded email.
- COMPLEXITY: Low.
- PROPOSED PILOT: auto-ack + availability capture on the existing form.
- DECISION MAKER: Dr. Advaith Sai Alampur (public on site). [FACT]
- CONTACT ROUTE: +91 94928 20777 / wa.me/919492820777 / envisionlaser@gmail.com.
- CONTACT CONFIDENCE: MED-HIGH.
- INDICATIVE PRICING [ESTIMATE]: ₹18,000–35,000 setup + ₹10,000–22,000/mo.
- EVIDENCE: https://envisionlasikcentre.com/

## 11. Pristine Eye Hospitals — eye hospital (cataract, Contoura LASIK/PRK, retina, cornea, pediatric)
- WEBSITE: https://pristineeyehospitals.com/
- LOCATION: Ground & 1st Floor, No.25/Summit, Y-Axis Building, HUDA Techno Enclave, Madhapur, next to Raidurg Metro, Hyderabad 500081
- OBSERVED:
  1. Booking page /book-my-appointment/ instructs visitors to "use the form above" and to "WhatsApp us", but the served HTML contains NO `<form>` and NO `wa.me` link (0 of each in raw HTML); only `tel:919000852020` and a branded email `appointment@pristineeyehospitals.com`. [raw HTML scan]
  2. OPD hours: Mon–Sat 9–19, Sun 9–13 (Sunday strictly by prior appointment; walk-ins not accepted). [site]
  3. Consultants named: Dr C. Jagadesh Reddy (cornea, cataract, refractive surgery) and Dr. Shravya Choudhary Balla. [site]
  4. International-patients page (visa/travel support) present. [site]
- INFERRED: the form may be JS-rendered (functional for a browser user) — but with no HTML/no-JS fallback, any script/embed failure silently removes online booking and leaves only phone/email.
- UNKNOWN: whether the live form actually submits reliably; enquiry volume.
- LIKELY COMMERCIAL EFFECT [ESTIMATE]: cataract/LASIK ₹30k–₹1.5L; a dead "book" path loses high-intent local and international enquiries.
- WHAT WE'D CHANGE: a server-rendered/no-JS fallback form + WhatsApp link so booking survives JS failure; instant auto-ack.
- COMPLEXITY: Low.
- PROPOSED PILOT: verify the live form end-to-end; add fallback capture + auto-ack.
- DECISION MAKER: Dr C. Jagadesh Reddy (named consultant; ownership unconfirmed). [FACT name / INFERENCE role]
- CONTACT ROUTE: +91 90008 52020 / appointment@pristineeyehospitals.com.
- CONTACT CONFIDENCE: MED.
- INDICATIVE PRICING [ESTIMATE]: ₹15,000–30,000 setup + ₹8,000–18,000/mo.
- EVIDENCE: https://pristineeyehospitals.com/book-my-appointment/

### Eye-clinic niche read
Same repeating pain as every prior batch: intake is WhatsApp/phone/manual with no instant acknowledgement and no fallback capture. Differentiator: very high value per case (₹30k–₹1.5L) and strong demand for self-serve booking. Priority order within the new niche: Sree Netralaya (clearest WhatsApp-only gap) > Envision (Gmail + manual confirm) > Pristine (fallback/no-JS risk, verify first).

---

## BATCH 3 — Home-interiors / modular-kitchen + Study-abroad (Hyderabad) · built 2026-10-03
New-niche entry (both niches untouched by Batches 1–2). Value thesis: an interiors project is ₹2–20L and a study-abroad enrolment is ₹25k–₹1.5L+, so one recovered enquiry is economically large. Signals = raw-HTML lead-capture scan (`<form>` / `wa.me` / `tel:` / `mailto:` counts) on each business's own served page, re-checked 2026-10-03.

## 12. Lipsy Interior — modular kitchen / home interiors / false ceiling
- CATEGORY: Modular kitchen + home interiors (est. 2005; "2000+ modular kitchens" per LinkedIn)
- LOCATION: Sriram Nagar Rd, Rajeev Nagar, Yousufguda, Hyderabad 500114
- WEBSITE: https://lipsyinterior.com (as LISTED) — does not resolve from this host
- OBSERVED:
  1. The website URL published on Indian Yellow Pages ("www.lipsyinterior.com"), ExportersIndia and the company's own LinkedIn page does NOT resolve from this host: http://, http://www. and https:// forms all return HTTP 000, and `getent hosts lipsyinterior.com` returns no record. [raw GET + DNS, 2026-10-03]
  2. The business is actively listed and "Verified" on Indian Yellow Pages and ExportersIndia (₹550–750/sqft, "View Mobile"), both driving traffic to that URL. [IYP/ExportersIndia]
  3. Owner & CEO named publicly: **Mohammed Shabuddin** — "Owner & CEO, Lipsy Interior", Hyderabad 500114 (LinkedIn; 20+ yrs; company since 2005). [LinkedIn]
  4. Published phone: +91 80741 54670. [IYP]
- INFERRED: every directory/LinkedIn click currently dead-ends; the only working route is the phone. Cause of the outage UNVERIFIED (transient / DNS / lapsed hosting).
- UNKNOWN: whether the domain is down temporarily or lapsed; whether the owner knows; enquiry volume; GBP existence.
- LIKELY COMMERCIAL EFFECT [ESTIMATE]: interiors ticket ₹2–15L; margin ₹40k–3L/project. A dead web presence on an established operator = direct lost inbound; even 1–2 recovered enquiries/mo ≈ ₹10k–₹1L+.
- WHAT WE'D CHANGE: interim mobile-first one-pager with WhatsApp click-to-chat + call + a short form; re-point the directory/LinkedIn listings to it.
- COMPLEXITY: Low–Medium.
- PROPOSED PILOT: interim capture page + re-point listings; measure enquiries for 2 weeks.
- DECISION MAKER: Mohammed Shabuddin — Owner & CEO. [FACT, LinkedIn]
- CONTACT ROUTE: +91 80741 54670 (published); LinkedIn; Yousufguda office.
- CONTACT CONFIDENCE: MED-HIGH (owner named; phone published; no email).
- INDICATIVE PRICING [ESTIMATE]: ₹12,000–25,000 setup + ₹6,000–12,000/mo.
- EVIDENCE: https://www.indianyellowpages.com/hyderabad/modular-kitchen.htm ; https://www.linkedin.com/in/mohammed-shabuddin-6001a332a ; raw HTTP/DNS check 2026-10-03.

## 13. Fleegl Interiors — modular kitchen / full home interiors
- CATEGORY: Premium modular kitchens, wardrobes, full home interiors (est. 2021; 1–10 employees)
- LOCATION: Sri Durga Sai Hub, 13th Phase Rd, KPHB (near Prajay Megapolis), Hyderabad 500085
- WEBSITE: https://fleegl.in/
- OBSERVED:
  1. Raw-HTML scan of the homepage AND /contact: ZERO `<form>` elements, ZERO `wa.me`, ZERO `whatsapp` references; the only routes are a `tel:+91-7892219412` link and the Gmail written as plain text (`fleeglinteriors@gmail.com`). [raw HTML, 2026-10-03]
  2. The page IS mobile-responsive (`viewport` present) and the business runs an active blog (e.g. "2BHK Interior Design Cost in Hyderabad (2026)", "Gated Community Interior Work Rules") — it invests in inbound content with no capture on the page. [site/blog]
  3. `/contact` and `/contact-us` both returned the homepage HTML (no dedicated contact page served). [curl]
  4. Published: phone +91-7892219412; email fleeglinteriors@gmail.com. [site]
- INFERRED: blog/search visitors not ready to phone have nowhere to leave a number; a plain-text email means opening a mail client (high friction).
- UNKNOWN: enquiry volume; GBP / WhatsApp Business use; forms on other pages.
- LIKELY COMMERCIAL EFFECT [ESTIMATE]: interiors ticket ₹2–15L; one extra captured enquiry/month at 25–35% close ≈ ₹10k–₹1L+.
- WHAT WE'D CHANGE: 3-field form + WhatsApp click-to-chat ("send your floor plan") + auto-acknowledgement, keeping the blog as the feeder.
- COMPLEXITY: Low.
- PROPOSED PILOT: add WhatsApp click-to-chat + short form to the homepage; measure 2 weeks.
- DECISION MAKER: Raghu Charan Raj D Damodhar — Founder & Managing Director. [FACT, LinkedIn]
- CONTACT ROUTE: +91-7892219412 / fleeglinteriors@gmail.com (both on the business's own site); LinkedIn.
- CONTACT CONFIDENCE: HIGH (owner named; phone + email published on own site).
- INDICATIVE PRICING [ESTIMATE]: ₹10,000–20,000 setup + ₹5,000–10,000/mo.
- EVIDENCE: https://fleegl.in/ ; https://fleegl.in/about-fleegl ; raw HTML scan 2026-10-03.

## 14. SSS Interiors — modular kitchen / interiors (AS Rao Nagar / ECIL)
- CATEGORY: Modular kitchen & interior service provider (proprietorship)
- LOCATION: Cellar, Shop No. 08, LIG B-11 & 26, Dr. A S Rao Nagar, ECIL, Hyderabad 500062
- WEBSITE: https://www.sssinteriors.in.net/
- OBSERVED:
  1. Contact page (`/contact-us.html`): 3 `<form>` elements + 4 `tel:` links, but ZERO `wa.me` and ZERO `mailto:`; no email address published on the homepage or contact page. [raw HTML, 2026-10-03]
  2. Price published: Rs 800/sq ft — rare transparency. [site]
  3. Contact person published: Ramesh Garre, Proprietor. [site/IYP]
- INFERRED: form-only capture with no fallback — a failed submission or an email/WhatsApp-preferring visitor leaves no route and gets no acknowledgement.
- UNKNOWN: whether submissions reach a monitored inbox; volume.
- LIKELY COMMERCIAL EFFECT [ESTIMATE]: interiors ticket ₹2–10L; one recovered enquiry/month ≈ ₹10k–₹60k+.
- WHAT WE'D CHANGE: email + WhatsApp click-to-chat fallbacks; auto-acknowledge the form; simple pipeline.
- COMPLEXITY: Low.
- PROPOSED PILOT: add WhatsApp click-to-chat + auto-ack on the existing form; 2-week measure.
- DECISION MAKER: Ramesh Garre — Proprietor. [FACT, published]
- CONTACT ROUTE: website forms / published `tel:` links; AS Rao Nagar office. No email/WhatsApp route published.
- CONTACT CONFIDENCE: MED (person + business known; no email/WhatsApp route).
- INDICATIVE PRICING [ESTIMATE]: ₹8,000–18,000 setup + ₹5,000–10,000/mo.
- EVIDENCE: https://www.sssinteriors.in.net/ ; https://www.sssinteriors.in.net/contact-us.html ; raw HTML scan 2026-10-03.

## 15. Disha Interiors — modular kitchens / wardrobes / interiors (CONTROL / benchmark)
- CATEGORY: Modular kitchens, wardrobes, interiors (est. 1995)
- LOCATION: Plot No: 33, Kavuri Hills, Extn of Road No:36, Jubilee Hills / Madhapur, Hyderabad 500033
- WEBSITE: https://dishahome.com/
- OBSERVED:
  1. Capture present: 1 `<form>`, 5 `tel:` links (incl. `tel:+91 99599 85678`), 4 `mailto:` links (info@dishahome.com); "whatsapp"/"Call Now" referenced 4×/3× though no server-rendered `wa.me` link. [raw HTML, 2026-10-03]
  2. Named in the company's own About/testimonials: "MD Mr. Surya Prakash". [site]
  3. Est. 1995 (About page). [site]
- INFERRED: NONE CLAIMED — included as a benchmark of adequate small-business intake (form + phone + email), to calibrate the leak cases.
- UNKNOWN: WhatsApp float behaviour (JS-injected?); volume.
- LIKELY COMMERCIAL EFFECT: n/a (control).
- WHAT WE'D CHANGE: n/a — possibly server-render the WhatsApp link for no-JS reliability (low priority).
- COMPLEXITY: n/a. PROPOSED PILOT: none.
- DECISION MAKER: Mr. Surya Prakash — MD/Owner. [FACT, per own site]
- CONTACT ROUTE: info@dishahome.com / +91 99599 85678.
- CONTACT CONFIDENCE: HIGH.
- EVIDENCE: https://dishahome.com/ ; https://dishahome.com/pages/about/ ; raw HTML scan 2026-10-03.

## 16. Western Wings Overseas Education & Immigration Services Pvt Ltd — study-abroad consultancy
- CATEGORY: Overseas education & immigration consultancy (Justdial est. 2017; LinkedIn "Managing Director since Feb 2009")
- LOCATION: Flat 201, 2nd Floor, Tulip Chambers, Near Satyam Theatre, Ameerpet, Hyderabad 500016
- WEBSITE: http://www.westernwings.in/
- OBSERVED:
  1. Homepage is a fixed-width, table-based layout (`<table width="1001">`), served as `iso-8859-1` with a Flash-era Dreamweaver script (`Scripts/AC_RunActiveContent.js`); NO `<meta name="viewport">` → not mobile-responsive. [raw HTML, 2026-10-03]
  2. Homepage raw HTML contains ZERO `<form>`, ZERO `wa.me`, ZERO `tel:`, ZERO `mailto:`; phone/email appear only as plain text ("Ph: 7416012233 / 7207314455, Mob: 9393306499, Email: info@westernwings.in"). [raw HTML]
  3. `/contact.html` has 2 `<form>` elements but still no WhatsApp, no click-to-call, no email link; footer reads "© 2016". [raw HTML]
  4. Justdial lists the same firm as "Western Wings Overseas Education & Immigration Services Pvt Ltd" at Tulip Chambers; LinkedIn lists a Managing Director role (Feb 2009–present). [Justdial/LinkedIn]
- INFERRED: the majority of Indian student enquiries begin on a phone; a non-responsive 1001px page with no homepage form/click-to-call converts poorly and captures nothing after hours; "© 2016" suggests years untouched.
- UNKNOWN: enquiry volume/channel mix; whether advisors capture leads offline; the MD's name.
- LIKELY COMMERCIAL EFFECT [ESTIMATE, WIDE]: ₹25k–₹1.5L+ per enrolled student; a mobile-first page with form + WhatsApp CTA plausibly recovers 1–3 enquiries/month. Verify before quoting.
- WHAT WE'D CHANGE: mobile-first landing page + short form + WhatsApp click-to-chat + instant auto-ack + a lead pipeline; keep their existing wording.
- COMPLEXITY: Low–Medium.
- PROPOSED PILOT: rebuild the homepage mobile-first with form + WhatsApp CTA; measure 2–4 weeks vs current.
- DECISION MAKER: Managing Director (name not published on public sources reviewed). [FACT role / UNKNOWN name]
- CONTACT ROUTE: info@westernwings.in / 7416012233 / 7207314455 / 040-64512233 (all published on the site); Ameerpet office.
- CONTACT CONFIDENCE: MED (business + role known; personal name not published).
- INDICATIVE PRICING [ESTIMATE]: ₹15,000–30,000 setup + ₹8,000–15,000/mo.
- EVIDENCE: http://www.westernwings.in/ ; http://www.westernwings.in/contact.html ; https://www.justdial.com/Hyderabad/Western-Wings-Overseas-Education-Immigration-Services-Pvt-Ltd-Near-Satyam-Theatre-Above-Tazaa-Kitchen-Ameerpet/040PXX40-XX40-110520162245-E6U2_BZDET ; https://www.linkedin.com/in/western-wings-overseas-education-116324399

## 17. International Campus Connect — study-abroad platform / consultancy (WATCH)
- CATEGORY: Overseas education portal/consultancy
- LOCATION: 1st Floor, Designer Tower, Plot No.78-A, Silpa Layout, Mind Space Circle→Ramky Tower Rd, Gachibowli, Hyderabad 500032
- WEBSITE: https://icampusconnect.com/ (bare domain serves 200)
- OBSERVED:
  1. `https://www.icampusconnect.com/` returns HTTP 000 from this host, while `https://icampusconnect.com/` returns HTTP 200. [curl, 2026-10-03]
  2. Published routes: +91 80830 34567 / +91 9390628256 (their LinkedIn). [LinkedIn]
- INFERRED: a www/non-www mismatch means any "www"-written link dead-ends. Cause UNVERIFIED (DNS/CDN or transient) — must be browser-confirmed before any claim.
- UNKNOWN: whether the www host serves in-browser/from India; whether the LinkedIn link is actually www-prefixed.
- LIKELY COMMERCIAL EFFECT [ESTIMATE]: n/a until verified; a broken canonical host silently loses dark traffic.
- WHAT WE'D CHANGE: verify in-browser; if confirmed, fix DNS/redirect www→apex.
- COMPLEXITY: Low (if confirmed). PROPOSED PILOT: none until browser-verified.
- DECISION MAKER: unknown. CONTACT ROUTE: phone (published). CONTACT CONFIDENCE: LOW.
- EVIDENCE: https://icampusconnect.com/ ; https://www.linkedin.com/company/i-campus-connect ; curl check 2026-10-03.

### Batch 3 niche read
Home-interiors/modular-kitchen: a genuinely different leak profile from Batches 1–2 — the constraint is not response *speed* but the *absence of a capture surface* (Fleegl, SSS) or a dead web presence entirely (Lipsy). High ticket, low complexity, named owners in 3 of 4 cases. Study-abroad: only one cleanly actionable candidate (Western Wings — a decades-old desktop-only site with no homepage capture), but the highest value per enquiry in the whole local book.
Priority within the new batch: Lipsy (dead site, named CEO) > Fleegl (named founder, own site, exact defect) > Western Wings (highest value) > SSS (no email/WhatsApp route → phone-only approach).
