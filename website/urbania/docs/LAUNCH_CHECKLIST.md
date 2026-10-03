# LAUNCH CHECKLIST

Current status: **NOT launch ready.** Blockers B1, B2 and B3 in `QA_REPORT.md` are open.

## Identity
- [ ] Final business name confirmed and applied (`BRAND` in `build_ui.py`)
- [ ] Domain registered, `BASE` updated, site rebuilt
- [ ] Canonical URLs resolve to the real domain
- [ ] `Sitemap:` line in `robots.txt` points at the real domain
- [ ] Logo finalized

## Infrastructure
- [ ] HTTPS — confirm the host serves HTTPS and redirects HTTP
- [ ] Single canonical host (www or non-www, not both)
- [ ] Staging environment `noindex`ed, or not publicly reachable
- [ ] 404 page served with a 404 status, not a 200

## Leads
- [ ] `FORM_ENDPOINT` set to a hosted endpoint, or mailto explicitly accepted as the model
- [ ] Test submission sent from a real phone on mobile data
- [ ] Spam protection active
- [ ] Notification reaches the owner, and the message contains trip details, source page, timestamp and UTM
- [ ] Test `tel:` link tapped on a real phone
- [ ] WhatsApp number set, or button confirmed intentionally hidden

## On-page
- [ ] All 11 `[VERIFY BEFORE PUBLISHING]` markers resolved
- [ ] Title and meta description reviewed for every page
- [ ] Open Graph images added (currently none)
- [ ] Structured data re-validated after any content change
- [ ] Internal links reviewed
- [ ] Alt text reviewed once real images replace the diagram

## Technical
- [ ] `robots.txt` reviewed and intentional
- [ ] Host/CDN allows traffic from OpenAI's published search-bot IP ranges
      (`https://openai.com/searchbot.json`) — required for ChatGPT search eligibility and **not**
      settable in robots.txt
- [ ] After any robots.txt change, allow ~24 hours before judging the effect in ChatGPT
- [ ] `sitemap.xml` submitted to Google Search Console and Bing Webmaster Tools
- [ ] Search Console verification
- [ ] Analytics implemented and `/privacy/` updated to match
- [ ] Performance tested at 320 / 375 / 390 / 430 / 768 px and desktop
- [ ] Lighthouse run recorded, with important findings fixed
- [ ] Accessibility basics checked: contrast, labels, keyboard, focus states

## Content and facts
- [ ] Every published statement verified against `FACTS_LEDGER.md`
- [ ] No placeholder, TODO or developer text remains
- [ ] No fabricated review, rating, counter, address or photograph
- [ ] Privacy and terms reviewed by the owner
- [ ] Real vehicle photographs in place

## Day of launch
- [ ] Rebuild and verify every route returns 200
- [ ] Click every link
- [ ] Submit the form once for real and confirm delivery
- [ ] Confirm Google Business Profile consistency with the site (name, phone, URL)
