# LOCAL OUTREACH QUEUE — BATCH 05 (STUDY ABROAD · EMAIL-ONLY · zero personal exposure)

**Status: DRAFT / QUEUED — NOT SENT.** Draft-and-queue only, pending Abhishek's approval.
**Why this batch exists:** the 2026-10-03 assessment flagged that the highest-value local vertical in the book had been under-mined ("the highest-value local lead in the entire 26-business book is a study-abroad consultancy, not a clinic or salon"). An overseas enrolment is worth **₹25,000–₹1,50,000+**, the highest value-per-enquiry of any niche audited so far, and consultancies publish email — so this vertical is also **email-first** (no personal WhatsApp/DM/phone needed to send).
**Sender:** Abhishek Singh, FCCA, MCSI (fca.abhi007@gmail.com) · linkedin.com/in/abhishek-singh-fcca-mcsi-897b3684
**Offer:** Westbridge — "We Bring Clients": enquiry-response / lead-recovery for local businesses. Free audit → ₹10,000 setup + ₹5,000/mo. No client, testimonial or result is claimed anywhere in these drafts.

**Method (reproducible, not "the site looks weak"):** each business's OWN page was fetched with a **mobile User-Agent** on 2026-10-03 and the raw-HTML lead-capture signals counted (`<form>` / `wa.me` / `tel:` / `mailto:` / viewport meta). Any claim that depends on JavaScript was then **re-checked in a real browser** before being written down. Where a signal could not be reproduced in the live DOM, it was dropped — see "Rejected claims" at the bottom.

---

### S1· Varshini Consultants — Ameerpet, Hyderabad

- **Decision-maker:** **A N Murthy — Director** (public LinkedIn, "Director at Varshini Consultants", Dec 2012–present)
- **PUBLISHED EMAIL:** `enquiry@varshiniconsultants.com` — source: http://www.varshiniconsultants.com/Contact-us.html (present in the served page bytes, verified 2026-10-03)
- **Alternate routes on the same page:** +91 40 40101192 / +91 9533126677 (plain text)
- **OBSERVED defects (evidence, mobile-UA fetch 2026-10-03):**
  1. **No viewport meta on the homepage or on Contact-us.html** → on a phone the site renders as a shrunken desktop page.
  2. **Zero `tel:` links, zero `mailto:` links, zero `wa.me` links** on both pages: the phone numbers and the email address are plain text, so on a phone they have to be copied by hand.
  3. The contact form posts to `contactmail.php` and its only confirmation is a JavaScript `alert('Thanku For Submitting your Detail....')` — no acknowledgement, no record for the student.
  4. Footer reads "© Copyright 2014".
- **FOUR-QUESTION:** why them = named Director + defects fully visible in their own bytes; why now = NZ/Canada intake season runs on mobile enquiries; why care = a student on a phone cannot tap to call or write; ask = 15 minutes.
- **SUBJECT:** varshiniconsultants.com on a phone
- **BODY (105 words):**

```text
Hi Mr Murthy,
I opened varshiniconsultants.com on my phone. The pages carry no mobile viewport setting, so they render as a shrunken desktop page, and there is no tap-to-call, WhatsApp or email link on either the homepage or the contact page — your numbers and enquiry@varshiniconsultants.com sit as plain text, so a student has to copy them by hand. The contact form's only reply is a JavaScript alert, and the footer still reads 2014.
New Zealand and Canada enquiries usually go to whoever replies first, so I can fix the mobile layout and add a working call and WhatsApp button with a proper auto-reply. Worth 15 minutes?
Abhishek | linkedin.com/in/abhishek-singh-fcca-mcsi-897b3684
```

- **ONE-TAP MAILTO:** <mailto:enquiry@varshiniconsultants.com?subject=varshiniconsultants.com%20on%20a%20phone&body=Hi%20Mr%20Murthy%2C%0AI%20opened%20varshiniconsultants.com%20on%20my%20phone.%20The%20pages%20carry%20no%20mobile%20viewport%20setting%2C%20so%20they%20render%20as%20a%20shrunken%20desktop%20page%2C%20and%20there%20is%20no%20tap-to-call%2C%20WhatsApp%20or%20email%20link%20on%20either%20the%20homepage%20or%20the%20contact%20page%20%E2%80%94%20your%20numbers%20and%20enquiry%40varshiniconsultants.com%20sit%20as%20plain%20text%2C%20so%20a%20student%20has%20to%20copy%20them%20by%20hand.%20The%20contact%20form%27s%20only%20reply%20is%20a%20JavaScript%20alert%2C%20and%20the%20footer%20still%20reads%202014.%0ANew%20Zealand%20and%20Canada%20enquiries%20usually%20go%20to%20whoever%20replies%20first%2C%20so%20I%20can%20fix%20the%20mobile%20layout%20and%20add%20a%20working%20call%20and%20WhatsApp%20button%20with%20a%20proper%20auto-reply.%20Worth%2015%20minutes%3F%0AAbhishek%20%7C%20linkedin.com%2Fin%2Fabhishek-singh-fcca-mcsi-897b3684>
- **CONFIDENCE:** HIGH (business + named Director + own published email all verified)

---

### S2· EV Overseas — Himayat Nagar, Hyderabad

- **Decision-maker:** name not published publicly (LinkedIn company page is "Self-Owned · Founded 2025 · Myself Only employees") → role-addressed ("Hi,")
- **PUBLISHED EMAIL:** `info@evoverseas.com` — source: https://www.evoverseas.com/contact.html (present in served bytes, verified 2026-10-03)
- **Alternate routes on the same page:** WhatsApp https://wa.me/919666963756 (working); phone published as text +91-9666963756
- **OBSERVED defect (evidence — confirmed by mobile-UA fetch AND in a real browser after JavaScript, 2026-10-03):**
  The tap-to-call link on **both the homepage and the contact page** is literally `tel:+919****3756` — the middle digits are replaced by asterisks, so tapping "call" dials an invalid number while every written mention of the number is correct. The homepage also serves **0 `<form>` elements**, leaving WhatsApp as the only working route for a student who would rather call or write.
- **FOUR-QUESTION:** why them = a defect any phone would expose in one tap, and they cannot see it; why now = a 2025-founded practice still building its funnel; why care = a wasted tap is a lost enquiry at ₹25k–₹1.5L; ask = 10 minutes.
- **SUBJECT:** Your "call" button on evoverseas.com doesn't dial
- **BODY (95 words):**

```text
Hi,
I opened evoverseas.com on my phone and tapped the call button. It doesn't dial your number — the link in the page code is tel:+919****3756, with the middle digits replaced by asterisks. The same broken link is on the contact page, and the homepage has no enquiry form at all, so WhatsApp is currently the only route that works.
I can fix the call button and add a short enquiry form with an instant auto-reply, so a student who would rather talk or write than message isn't lost.
Worth 10 minutes?
Abhishek | linkedin.com/in/abhishek-singh-fcca-mcsi-897b3684
```

- **ONE-TAP MAILTO:** <mailto:info@evoverseas.com?subject=Your%20%22call%22%20button%20on%20evoverseas.com%20doesn%27t%20dial&body=Hi%2C%0AI%20opened%20evoverseas.com%20on%20my%20phone%20and%20tapped%20the%20call%20button.%20It%20doesn%27t%20dial%20your%20number%20%E2%80%94%20the%20link%20in%20the%20page%20code%20is%20tel%3A%2B919%2A%2A%2A%2A3756%2C%20with%20the%20middle%20digits%20replaced%20by%20asterisks.%20The%20same%20broken%20link%20is%20on%20the%20contact%20page%2C%20and%20the%20homepage%20has%20no%20enquiry%20form%20at%20all%2C%20so%20WhatsApp%20is%20currently%20the%20only%20route%20that%20works.%0AI%20can%20fix%20the%20call%20button%20and%20add%20a%20short%20enquiry%20form%20with%20an%20instant%20auto-reply%2C%20so%20a%20student%20who%20would%20rather%20talk%20or%20write%20than%20message%20isn%27t%20lost.%0AWorth%2010%20minutes%3F%0AAbhishek%20%7C%20linkedin.com%2Fin%2Fabhishek-singh-fcca-mcsi-897b3684>
- **CONFIDENCE:** HIGH (defect reproduced twice, independently: curl + live DOM)

---

### S3· Global Study Connect — Dilsukhnagar, Hyderabad (est. 2008)

- **Decision-maker:** name not published on the site or in public listings → role-addressed ("Hi,")
- **PUBLISHED EMAIL:** `info@globalstudyconnect.in` and `globalstudyconnect.dsnr@gmail.com` — source: https://globalstudyconnect.in/contact-us/ (both present in served bytes, verified 2026-10-03)
- **Alternate routes on the same page:** +91 88971 87048 (contact page) / +91 97011 23377, +91 95733 88866, +91 8977754811 (homepage); Instagram
- **OBSERVED defects (evidence, mobile-UA fetch + live-DOM check, 2026-10-03):**
  1. **Four different phone numbers across two pages** — three on the homepage, a different one on the contact page.
  2. The live DOM on **both** pages contains **zero `tel:` and zero `mailto:` links** — every number and email address is plain text, so a phone visitor must copy by hand.
  (Their WhatsApp click-to-chat widget **does work** — this draft does **not** claim WhatsApp is missing. See "Rejected claims".)
- **FOUR-QUESTION:** why them = an 2008-established consultancy running a 2024 site, so a defect there is a maintenance gap not a budget problem; why now = mobile-first student behaviour; why care = an ambiguous number plus copy-paste friction loses calls; ask = 15 minutes.
- **SUBJECT:** Four different phone numbers on globalstudyconnect.in
- **BODY (100 words):**

```text
Hi,
I looked at globalstudyconnect.in on a phone. Your homepage lists three numbers (97011 23377, 95733 88866, 8977754811) while the contact page lists a different one (88971 87048), so a student can't tell which to call. None of them is tappable, and the email addresses are plain text too — on a phone everything has to be copied by hand. Your WhatsApp widget does work.
I can settle on one number across the site, make the number and email tap-to-call and tap-to-write, and add an instant auto-reply so an enquiry isn't lost to a copy-paste.
Worth 15 minutes?
Abhishek | linkedin.com/in/abhishek-singh-fcca-mcsi-897b3684
```

- **ONE-TAP MAILTO:** <mailto:info@globalstudyconnect.in?subject=Four%20different%20phone%20numbers%20on%20globalstudyconnect.in&body=Hi%2C%0AI%20looked%20at%20globalstudyconnect.in%20on%20a%20phone.%20Your%20homepage%20lists%20three%20numbers%20%2897011%2023377%2C%2095733%2088866%2C%208977754811%29%20while%20the%20contact%20page%20lists%20a%20different%20one%20%2888971%2087048%29%2C%20so%20a%20student%20can%27t%20tell%20which%20to%20call.%20None%20of%20them%20is%20tappable%2C%20and%20the%20email%20addresses%20are%20plain%20text%20too%20%E2%80%94%20on%20a%20phone%20everything%20has%20to%20be%20copied%20by%20hand.%20Your%20WhatsApp%20widget%20does%20work.%0AI%20can%20settle%20on%20one%20number%20across%20the%20site%2C%20make%20the%20number%20and%20email%20tap-to-call%20and%20tap-to-write%2C%20and%20add%20an%20instant%20auto-reply%20so%20an%20enquiry%20isn%27t%20lost%20to%20a%20copy-paste.%0AWorth%2015%20minutes%3F%0AAbhishek%20%7C%20linkedin.com%2Fin%2Fabhishek-singh-fcca-mcsi-897b3684>
- **CONFIDENCE:** MED-HIGH (defect verified in live DOM; person unnamed)

---

### S4· The Study Connect — KPHB Colony, Hyderabad (founded 2022) — OPTIONAL / MED

- **Decision-maker:** name not published on the site → role-addressed ("Hi,")
- **PUBLISHED EMAIL:** `ho@thestudyconnect.com` and `support@studyconnect.co.in` — source: https://thestudyconnect.com/ (present in served bytes, verified 2026-10-03). Branch mailboxes also published: eluru@, gajuwaka@, nellore@, vijayawada@
- **OBSERVED defect (evidence, mobile-UA fetch + live DOM, 2026-10-03):** the homepage carries **no `tel:` and no `mailto:` links** — numbers and branch emails are plain text. The enquiry form and one `wa.me` link **do** work.
- **Why it is optional:** this is the weakest defect in the batch (their capture is functional); include it only if the email batch is being sent anyway.
- **SUBJECT:** Tap-to-call on thestudyconnect.com
- **BODY (88 words):**

```text
Hi,
I checked thestudyconnect.com on a phone. Your site lists four branch offices — Eluru, Gajuwaka, Nellore and Vijayawada — but the homepage has no tappable phone number or email address, so a student has to copy them by hand. The enquiry form and WhatsApp do work, so this is the last gap between a visitor and a call.
I can make the numbers and branch emails tap-to-call and tap-to-write, and route each enquiry to the right branch with an instant acknowledgement.
Worth 15 minutes?
Abhishek | linkedin.com/in/abhishek-singh-fcca-mcsi-897b3684
```

- **ONE-TAP MAILTO:** <mailto:ho@thestudyconnect.com?subject=Tap-to-call%20on%20thestudyconnect.com&body=Hi%2C%0AI%20checked%20thestudyconnect.com%20on%20a%20phone.%20Your%20site%20lists%20four%20branch%20offices%20%E2%80%94%20Eluru%2C%20Gajuwaka%2C%20Nellore%20and%20Vijayawada%20%E2%80%94%20but%20the%20homepage%20has%20no%20tappable%20phone%20number%20or%20email%20address%2C%20so%20a%20student%20has%20to%20copy%20them%20by%20hand.%20The%20enquiry%20form%20and%20WhatsApp%20do%20work%2C%20so%20this%20is%20the%20last%20gap%20between%20a%20visitor%20and%20a%20call.%0AI%20can%20make%20the%20numbers%20and%20branch%20emails%20tap-to-call%20and%20tap-to-write%2C%20and%20route%20each%20enquiry%20to%20the%20right%20branch%20with%20an%20instant%20acknowledgement.%0AWorth%2015%20minutes%3F%0AAbhishek%20%7C%20linkedin.com%2Fin%2Fabhishek-singh-fcca-mcsi-897b3684>
- **CONFIDENCE:** MED (defect small; person unnamed)

---

## CONTROLS / BENCHMARKS added this cycle (no leak claimed)

- **i20fever / Yathapu Consulting** (KPHB; Founder **Naveen Yathapu**; 8 offices, 150+ staff, est. 2006) — homepage intake healthy: 2 `<form>`, 1 `wa.me`, 4 `tel:`, 2 `mailto:`, viewport present, `info@i20fever.com` published. CONTROL. (Note: this domain serves **gzip unconditionally** — see Rejected claims.)
- **Videsh Consultz** — 2 `<form>`, 5 `tel:`, 3 `mailto:` → CONTROL (healthy intake).
- **HOC Overseas Consultants** (Punjagutta; `info@hocedu.com`) — 2 `<form>`, 2 `wa.me`, 5 `tel:`, 3 `mailto:` → CONTROL.
- **TcollegeDayz Pvt Ltd** (Madhapur; `info.tcollegedayz@gmail.com`) — 2 `<form>`, 7 `wa.me`, 3 `tel:`, 1 `mailto:` → CONTROL.
- **PupilAbroad** (Himayat Nagar, est. 2003) — 3 `<form>`, 1 `wa.me`, 6 `tel:`, 2 `mailto:` → CONTROL.

## WATCH (not sendable yet — do not claim)

- **Western Wings Overseas Education** (Ameerpet) — already drafted as O-020 / B04 A8; still the only legacy-desktop copy in the vertical.
- **SimplyTakeOff** — `simplytakeoff.com` (www and apex) both serve a **GoDaddy website-builder placeholder**, not a business site. Cause unverified (their real site may be elsewhere) → not a claim.
- **Study Square Telangana** — `studysquaretelangana.com` resolves to a **private/internal address** (extract service blocks it; this host gets no A record). Misconfigured DNS or a mispublished domain — UNVERIFIED, not a claim.
- **Pathway International Studies** — serves a 1,624-byte JavaScript app shell; raw-HTML signals meaningless.
- **Santamonica Study Abroad (Hyderabad)** — franchise location page returns 0 of every signal with viewport present; template/JS-rendered. Not a micro-business (Kerala-headquartered brand) → not pursued.

## REJECTED CLAIMS (recorded so they are not re-invented)

1. **"Global Study Connect has no WhatsApp"** — FALSE. The homepage returned 0 `wa.me` in raw HTML and 0 `a[href*=whatsapp]` in the DOM, but the page loads the WordPress **Click-to-Chat (`ht_ctc_chat_var`)** plugin, which renders the widget via JS. The draft above therefore claims only what is true: no `tel:` / no `mailto:` / four inconsistent numbers.
2. **"i20fever has no mobile site / no capture"** — FALSE. The domain serves gzip **unconditionally** (bytes begin `1f 8b`), so a plain `curl` returns binary and every count reads 0. With `--compressed`: 2 `<form>`, 4 `tel:`, viewport present. **Always re-fetch with `--compressed` (or check for the gzip magic bytes) before recording a zero.**
3. **"EV Overseas' number is missing"** — overstated. The number is published correctly in text and in the WhatsApp link; only the `tel:` anchor is masked. The draft says exactly that.
4. **"/contact-us/ returns 404 on evoverseas.com, hocedu.com, pupilabroad.com"** — NOT defects. Those paths are not the links the businesses publish (EV links `contact.html`; HOC links `contact.php`; PupilAbroad links `./contact`, which returns 200). Only cite a URL the business itself links to.

## WHAT IS NOT IN THIS BATCH

- No WhatsApp/DM/phone item: every item above is email-only and needs no personal handle.
- No national brands (IDP, upGrad, Jamboree, Edwise, Fateh, Global Tree, KC Overseas) — no owner-reachable decision surface for a micro-pilot.
- Nothing is sent. Sending awaits Abhishek's approval.
