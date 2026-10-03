# ONE Force Urbania - Website Template / Base Shortlist

**Business:** ONE Force Urbania (17-seat), Hyderabad, India - pre-booked private group transport (airport groups, weddings/events, corporate teams, sightseeing/day hire, custom multi-stop trips).  
**Model:** Quote-first. One vehicle only - no fleet, no inventory, no availability calendar, no accounts, no instant booking, no marketplace, no self-drive, no ecommerce/Stripe, no database.  
**Deliverable:** evaluate >=8 credible bases across 15 criteria (1-10 each, max 150) and recommend one.  
**Prepared:** 2026-10-03. **Candidates verified:** 14.

## Method & verification

- Licences were read from the repositories' actual licence files (raw GitHub `LICENSE`/`LICENSE.md`) and cross-checked against the GitHub API `license.spdx_id` field where available; a few were read from the project's official licence page (Flowbite, HTML5 UP, Preline). Where a licence could not be cleanly verified it is stated explicitly and penalised.
- Every demo URL listed below was fetched and returned **HTTP 200** at the time of writing.
- Live pages of the top candidates were probed for `tel:` links and sticky/fixed elements (SBS v1/v2 and SBS v2 returned 5 `tel:` links + 1 sticky element; AstroWind and ScrewFast returned 0 `tel:` links).
- Scores are judged *for this specific one-vehicle, quote-first, India-local group-transport use case*, not in the abstract. 15 criteria, 1-10 each; total out of 150.

## Scoring rubric (15 criteria, 1-10)

1. **Mobile-first quality** - responsive layout, touch targets, mobile nav.  
2. **Visual credibility** - does it look trustworthy to a wedding/corporate buyer.  
3. **Local-service conversion fit** - call/WhatsApp/quote patterns toward a local buyer.  
4. **Page-speed potential** - achievable Core Web Vitals / static output.  
5. **SEO architecture** - semantic HTML, meta/schema, sitemap, clean URLs, content pages.  
6. **Accessibility** - contrast, semantics, keyboard, ARIA.  
7. **Code quality** - structure, maintainability, conventions.  
8. **Ease of modification** - how fast a non-author can re-skin/re-content.  
9. **Dependency weight** - 10 = lightest (no framework/runtime bloat).  
10. **Licence suitability** - clarity + freedom for a commercial site (10 = clean MIT/public-domain-like).  
11. **ONE-vehicle suitability** - 10 = no fleet/inventory/booking baggage to rip out.  
12. **Quote-first conversion fit** - supports a quote/contact flow, not an instant-book flow.  
13. **Articles later** - built-in blog/MDX engine for SEO content.  
14. **Image/gallery handling** - optimised images, gallery/lightbox for vehicle/interiors.  
15. **Sticky mobile CTA capability** - can it carry a persistent Call/WhatsApp/Quote bar.  

## Licence verification summary

| Candidate | Licence (as verified) | Verified at |
|---|---|---|
| Small Business Starter (free) | MIT | repo LICENSE.md + GitHub API |
| Small Business Starter v2 | MIT | repo LICENSE + GitHub API |
| AstroWind | MIT | repo LICENSE.md + GitHub API |
| Astro Paper | MIT | repo LICENSE + GitHub API |
| ScrewFast | MIT (dependency: Preline UI = MIT + Fair-Use) | repo LICENSE + GitHub API |
| Astro Nano | MIT | repo LICENSE + GitHub API |
| HyperUI | MIT | repo LICENSE + GitHub API |
| Flowbite (community) | MIT (Pro = separate EULA) | flowbite.com/docs/getting-started/license + API |
| Start Bootstrap - Agency | MIT | repo LICENSE + GitHub API |
| Preline UI | Dual: MIT + 'Preline UI Fair Use License' | repo LICENSE |
| HTML5 UP | Creative Commons Attribution 3.0 (CC BY 3.0) | html5up.net/license |
| JAKS.dev Vault | MIT | repo LICENSE + GitHub API |
| Tailwind Toolbox Landing Page | MIT | repo LICENSE |
| Cruip Open (React) | GPL-3.0 | repo README (GitHub API: no SPDX file detected) |

## Candidate evaluations

### 1. Small Business Starter (free)

- **Source URL:** https://github.com/alancuenca/small-business-starter
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE.md` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://free-sbs.netlify.app/ (HTTP 200)
- **Advantages:** Purpose-built for trade/service businesses; 5 `tel:` links; sticky header; brand swapped in two files; JSON-LD + sitemap + robots.txt; blog included; Astro image optimisation; near-100 Lighthouse claims.
- **Disadvantages:** Demo is electrician-themed; no WhatsApp link by default; single-author project (41 stars); the contact form uses Netlify Forms (assumes Netlify hosting).
- **Modifications required:** Swap copy/brand tokens; add a full-width 17-seat Urbania hero; add Hyderabad service-area pages; wire a quote form (email/WhatsApp); swap favicon/OG.
- **Performance concerns:** None material - static Astro output, Tailwind v4, minimal JS (drawer only).

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 9 |
| 2 | Visual credibility | 8 |
| 3 | Local-service conversion fit | 10 |
| 4 | Page-speed potential | 9 |
| 5 | SEO architecture | 9 |
| 6 | Accessibility | 8 |
| 7 | Code quality | 9 |
| 8 | Ease of modification | 10 |
| 9 | Dependency weight (10=lightest) | 9 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 10 |
| 12 | Quote-first conversion fit | 10 |
| 13 | Articles later | 8 |
| 14 | Image/gallery handling | 9 |
| 15 | Sticky mobile CTA capability | 9 |
| | **TOTAL** | **137 / 150** |

### 2. Small Business Starter v2

- **Source URL:** https://github.com/alancuenca/small-business-starter-v2
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://small-business-starter-v2.netlify.app/ (HTTP 200)
- **Advantages:** Minimal, blazing-fast Astro 7 + Tailwind v4; same mobile-first DNA and `tel:` patterns; cleanest dependency profile of the set.
- **Disadvantages:** Newest candidate (0 stars, released 2026); fewer pre-built sections than v1; still trade-oriented, not vehicle/event oriented.
- **Modifications required:** Same as v1, plus re-adding a hero/gallery if v2 trims them.
- **Performance concerns:** None material - intentionally minimal output.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 9 |
| 2 | Visual credibility | 8 |
| 3 | Local-service conversion fit | 9 |
| 4 | Page-speed potential | 10 |
| 5 | SEO architecture | 8 |
| 6 | Accessibility | 8 |
| 7 | Code quality | 9 |
| 8 | Ease of modification | 9 |
| 9 | Dependency weight (10=lightest) | 10 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 10 |
| 12 | Quote-first conversion fit | 9 |
| 13 | Articles later | 7 |
| 14 | Image/gallery handling | 8 |
| 15 | Sticky mobile CTA capability | 9 |
| | **TOTAL** | **133 / 150** |

### 3. AstroWind

- **Source URL:** https://github.com/arthelokyo/astrowind
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE.md` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://astrowind.vercel.app/ (HTTP 200)
- **Advantages:** Most-starred Astro theme (6k+); excellent Lighthouse; 30+ typed composable sections; strong SEO/blog/RSS/MDX; Unpic image CDN.
- **Disadvantages:** Generic SaaS/startup template - no local-service or call-first patterns (0 `tel:` links); the large widget library is more to delete than to add.
- **Modifications required:** Remove half the widgets; build a transport hero, route/use-case cards, gallery; add `tel:` + quote form; retune palette to the Urbania brand.
- **Performance concerns:** Strong baseline; strip optional analytics/embeds to keep it lean.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 8 |
| 2 | Visual credibility | 9 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 9 |
| 5 | SEO architecture | 9 |
| 6 | Accessibility | 8 |
| 7 | Code quality | 9 |
| 8 | Ease of modification | 7 |
| 9 | Dependency weight (10=lightest) | 8 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 9 |
| 12 | Quote-first conversion fit | 6 |
| 13 | Articles later | 9 |
| 14 | Image/gallery handling | 8 |
| 15 | Sticky mobile CTA capability | 6 |
| | **TOTAL** | **121 / 150** |

### 4. Astro Paper

- **Source URL:** https://github.com/satnaing/astro-paper
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://astro-paper.pages.dev/ (HTTP 200)
- **Advantages:** Best-in-class blog/SEO foundation (5k+ stars); minimal, fast, accessible; excellent MDX/code-block handling.
- **Disadvantages:** A blog theme, not a business site - no services, gallery, or conversion sections; the whole marketing layer must be added.
- **Modifications required:** Build every commercial page from scratch on top of the blog engine.
- **Performance concerns:** Excellent - essentially static HTML with tiny JS.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 8 |
| 2 | Visual credibility | 7 |
| 3 | Local-service conversion fit | 4 |
| 4 | Page-speed potential | 10 |
| 5 | SEO architecture | 8 |
| 6 | Accessibility | 8 |
| 7 | Code quality | 9 |
| 8 | Ease of modification | 8 |
| 9 | Dependency weight (10=lightest) | 9 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 9 |
| 12 | Quote-first conversion fit | 4 |
| 13 | Articles later | 10 |
| 14 | Image/gallery handling | 5 |
| 15 | Sticky mobile CTA capability | 5 |
| | **TOTAL** | **114 / 150** |

### 5. ScrewFast

- **Source URL:** https://github.com/mearashadowfax/ScrewFast
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT + GitHub API = MIT; BUT depends on Preline UI (dual MIT + Fair-Use licence)
- **Demo:** https://screwfast.uk/ (HTTP 200)
- **Advantages:** Sleek, modern marketing look; blog + docs built in; Astro + Tailwind; 1.4k stars; actively maintained.
- **Disadvantages:** SaaS/startup framing with 0 `tel:` patterns; ships GSAP + Lenis + Preline JS (heavier); Preline dependency adds licence ambiguity.
- **Modifications required:** Strip GSAP/Lenis animations; rebuild hero/services/CTA for transport; add `tel:` + quote CTA; verify/remove the Preline dependency.
- **Performance concerns:** GSAP, Lenis smooth-scroll and Preline JS inflate the JS payload vs plain Astro themes.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 8 |
| 2 | Visual credibility | 9 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 7 |
| 5 | SEO architecture | 8 |
| 6 | Accessibility | 7 |
| 7 | Code quality | 8 |
| 8 | Ease of modification | 7 |
| 9 | Dependency weight (10=lightest) | 5 |
| 10 | Licence suitability | 8 |
| 11 | ONE-vehicle suitability | 9 |
| 12 | Quote-first conversion fit | 7 |
| 13 | Articles later | 8 |
| 14 | Image/gallery handling | 7 |
| 15 | Sticky mobile CTA capability | 7 |
| | **TOTAL** | **111 / 150** |

### 6. Astro Nano

- **Source URL:** https://github.com/markhorn-dev/astro-nano
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://astro-nano-demo.vercel.app/ (HTTP 200)
- **Advantages:** Ruthlessly minimal, zero-framework, extremely fast; easy to reason about; a clean skeleton.
- **Disadvantages:** Portfolio/blog framing; no commercial sections, gallery, or CTA; sparse styling out of the box.
- **Modifications required:** Effectively build the whole business site yourself; Nano only supplies layout + blog plumbing.
- **Performance concerns:** Near-optimal - almost no JS.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 8 |
| 2 | Visual credibility | 6 |
| 3 | Local-service conversion fit | 3 |
| 4 | Page-speed potential | 10 |
| 5 | SEO architecture | 7 |
| 6 | Accessibility | 8 |
| 7 | Code quality | 8 |
| 8 | Ease of modification | 9 |
| 9 | Dependency weight (10=lightest) | 10 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 10 |
| 12 | Quote-first conversion fit | 3 |
| 13 | Articles later | 9 |
| 14 | Image/gallery handling | 4 |
| 15 | Sticky mobile CTA capability | 4 |
| | **TOTAL** | **109 / 150** |

### 7. HyperUI

- **Source URL:** https://github.com/markmead/hyperui
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://hyperui.dev/ (HTTP 200)
- **Advantages:** Largest free copy-paste Tailwind component collection (12k+ stars); no build tools needed; Alpine optional; easy to cherry-pick sections incl. CTA/sticky nav.
- **Disadvantages:** Component collection only (no pages); minimal SEO/gallery; some sections are ecommerce-oriented; all architecture is left to you.
- **Modifications required:** Assemble pages from components; add an Astro/static shell, SEO, gallery, `tel:`/quote CTA.
- **Performance concerns:** Near-zero if you skip JS components; CSS cost depends on your Tailwind build.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 9 |
| 2 | Visual credibility | 8 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 9 |
| 5 | SEO architecture | 4 |
| 6 | Accessibility | 7 |
| 7 | Code quality | 8 |
| 8 | Ease of modification | 8 |
| 9 | Dependency weight (10=lightest) | 9 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 8 |
| 12 | Quote-first conversion fit | 6 |
| 13 | Articles later | 2 |
| 14 | Image/gallery handling | 6 |
| 15 | Sticky mobile CTA capability | 8 |
| | **TOTAL** | **108 / 150** |

### 8. Flowbite (community edition)

- **Source URL:** https://github.com/themesberg/flowbite
- **Licence:** MIT (SPDX: MIT) for the community release - verified at https://flowbite.com/docs/getting-started/license/ + GitHub API = MIT (Flowbite Pro is a separate paid EULA)
- **Demo:** https://flowbite.com/blocks/ (HTTP 200)
- **Advantages:** 400+ Tailwind sections/blocks (heroes, CTA banners, sticky navbars, testimonials, footers); polished; huge ecosystem.
- **Disadvantages:** A component library, not a website - you assemble it; interactive components pull Flowbite JS/Alpine; much of the showcase is the paid Pro edition.
- **Modifications required:** Assemble a home + services + contact site from blocks; add a static/Astro shell; wire `tel:`/quote; add SEO.
- **Performance concerns:** Flowbite JS + Alpine only if interactive components are used; otherwise pure Tailwind.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 9 |
| 2 | Visual credibility | 9 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 7 |
| 5 | SEO architecture | 5 |
| 6 | Accessibility | 7 |
| 7 | Code quality | 8 |
| 8 | Ease of modification | 7 |
| 9 | Dependency weight (10=lightest) | 6 |
| 10 | Licence suitability | 9 |
| 11 | ONE-vehicle suitability | 8 |
| 12 | Quote-first conversion fit | 6 |
| 13 | Articles later | 3 |
| 14 | Image/gallery handling | 6 |
| 15 | Sticky mobile CTA capability | 8 |
| | **TOTAL** | **104 / 150** |

### 9. Start Bootstrap - Agency

- **Source URL:** https://github.com/StartBootstrap/startbootstrap-agency
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://startbootstrap.github.io/startbootstrap-agency/ (HTTP 200)
- **Advantages:** Battle-tested (2k+ stars), MIT, mobile-first, portfolio/gallery grid, professional-services vibe; well documented.
- **Disadvantages:** Bootstrap 5 (heavier CSS + JS bundle than Tailwind); agency-portfolio framing; no blog; dated look.
- **Modifications required:** Re-theme to transport; add services/quote/contact; add a `tel:` sticky bar; add SEO/schema; trim unused Bootstrap.
- **Performance concerns:** Bootstrap CSS/JS larger than a Tailwind output; still ships a meaningful JS bundle.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 8 |
| 2 | Visual credibility | 7 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 7 |
| 5 | SEO architecture | 6 |
| 6 | Accessibility | 7 |
| 7 | Code quality | 7 |
| 8 | Ease of modification | 8 |
| 9 | Dependency weight (10=lightest) | 6 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 9 |
| 12 | Quote-first conversion fit | 6 |
| 13 | Articles later | 3 |
| 14 | Image/gallery handling | 6 |
| 15 | Sticky mobile CTA capability | 7 |
| | **TOTAL** | **103 / 150** |

### 10. Preline UI

- **Source URL:** https://github.com/htmlstreamofficial/preline
- **Licence:** Dual licence: MIT AND 'Preline UI Fair Use License' - verified at repo `LICENSE`; the dual/Fair-Use clause is not a clean MIT grant
- **Demo:** https://preline.co/examples.html (HTTP 200)
- **Advantages:** Professional Tailwind component/template library; strong accessible patterns; sticky navbars and CTA blocks.
- **Disadvantages:** Dual/Fair-Use licence adds legal ambiguity (not clean MIT); interactive components require the Preline JS plugin layer; library, not a site.
- **Modifications required:** Assemble pages; resolve licence clarity; add a static shell, SEO, gallery, `tel:`/quote.
- **Performance concerns:** Preline JS plugin layer adds weight vs pure markup.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 9 |
| 2 | Visual credibility | 9 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 7 |
| 5 | SEO architecture | 4 |
| 6 | Accessibility | 8 |
| 7 | Code quality | 8 |
| 8 | Ease of modification | 7 |
| 9 | Dependency weight (10=lightest) | 6 |
| 10 | Licence suitability | 7 |
| 11 | ONE-vehicle suitability | 8 |
| 12 | Quote-first conversion fit | 6 |
| 13 | Articles later | 3 |
| 14 | Image/gallery handling | 6 |
| 15 | Sticky mobile CTA capability | 8 |
| | **TOTAL** | **102 / 150** |

### 11. HTML5 UP - Landed / Story

- **Source URL:** https://html5up.net/ (e.g. https://html5up.net/landed)
- **Licence:** Creative Commons Attribution 3.0 (CC BY 3.0) - verified at https://html5up.net/license (attribution obligation)
- **Demo:** https://html5up.net/landed (HTTP 200) / https://html5up.net/story (HTTP 200)
- **Advantages:** Hand-crafted, stylish, fully responsive; light static HTML/CSS; distinctive modular layouts.
- **Disadvantages:** CC BY requires visible attribution (a licence obligation); jQuery + skel/scrollex JS; no blog; no conversion patterns.
- **Modifications required:** Strip jQuery/skel; add services/gallery/quote; add `tel:` CTA; keep or replace attribution; build SEO/meta/schema.
- **Performance concerns:** jQuery + scroll plugins add JS; otherwise lean static assets.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 8 |
| 2 | Visual credibility | 8 |
| 3 | Local-service conversion fit | 5 |
| 4 | Page-speed potential | 8 |
| 5 | SEO architecture | 6 |
| 6 | Accessibility | 6 |
| 7 | Code quality | 7 |
| 8 | Ease of modification | 7 |
| 9 | Dependency weight (10=lightest) | 7 |
| 10 | Licence suitability | 7 |
| 11 | ONE-vehicle suitability | 9 |
| 12 | Quote-first conversion fit | 5 |
| 13 | Articles later | 4 |
| 14 | Image/gallery handling | 7 |
| 15 | Sticky mobile CTA capability | 5 |
| | **TOTAL** | **99 / 150** |

### 12. JAKS.dev Vault - business templates

- **Source URL:** https://github.com/jakscoduxdev-netizen/JakDEvTemplates
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT + GitHub API `license.spdx_id = MIT`
- **Demo:** https://templates.jack-codes.com/ (HTTP 200)
- **Advantages:** 26 single-file HTML templates incl. business/corporate; no build step; MIT with no attribution demand; instantly shippable.
- **Disadvantages:** Tailwind v3 via CDN (runtime, not production-optimised); inline JS; very low stars (3); thin SEO; not transport-specific.
- **Modifications required:** Pick `business-corporate-pro`; swap content; move to compiled Tailwind; build inner pages, gallery, `tel:`/quote CTA, JSON-LD.
- **Performance concerns:** CDN Tailwind runtime cost; no image-optimisation pipeline.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 7 |
| 2 | Visual credibility | 7 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 5 |
| 5 | SEO architecture | 5 |
| 6 | Accessibility | 6 |
| 7 | Code quality | 6 |
| 8 | Ease of modification | 9 |
| 9 | Dependency weight (10=lightest) | 6 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 9 |
| 12 | Quote-first conversion fit | 7 |
| 13 | Articles later | 3 |
| 14 | Image/gallery handling | 5 |
| 15 | Sticky mobile CTA capability | 6 |
| | **TOTAL** | **97 / 150** |

### 13. Tailwind Toolbox Landing Page

- **Source URL:** https://github.com/tailwindtoolbox/Landing-Page
- **Licence:** MIT (SPDX: MIT) - verified: repo `LICENSE` = MIT
- **Demo:** https://tailwindtoolbox.github.io/Landing-Page/ (HTTP 200)
- **Advantages:** Single `index.html`, no build step; instantly editable; fixed nav with CTA; tiny file count.
- **Disadvantages:** Loads Tailwind via the Play CDN (not production-grade - runtime compile, large); one generic page; no blog, gallery, or forms; dated 2018-2022 design.
- **Modifications required:** Rebuild styling to compiled Tailwind; add services/about/gallery/contact; add `tel:` + quote CTA; add SEO/meta/JSON-LD.
- **Performance concerns:** CDN Tailwind JIT is a real Core Web Vitals penalty vs a compiled stylesheet.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 7 |
| 2 | Visual credibility | 6 |
| 3 | Local-service conversion fit | 6 |
| 4 | Page-speed potential | 5 |
| 5 | SEO architecture | 5 |
| 6 | Accessibility | 6 |
| 7 | Code quality | 6 |
| 8 | Ease of modification | 8 |
| 9 | Dependency weight (10=lightest) | 7 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 9 |
| 12 | Quote-first conversion fit | 7 |
| 13 | Articles later | 2 |
| 14 | Image/gallery handling | 4 |
| 15 | Sticky mobile CTA capability | 6 |
| | **TOTAL** | **94 / 150** |

### 14. Cruip Open (React / Next.js)

- **Source URL:** https://github.com/cruip/open-react-template
- **Licence:** GPL-3.0 - stated in repo README (https://www.gnu.org/licenses/gpl-3.0.html); GitHub API reports no SPDX-detected licence file
- **Demo:** https://open.cruip.com/ (HTTP 200)
- **Advantages:** Beautiful, animated, professionally designed; Next.js + Tailwind; free GPL landing template.
- **Disadvantages:** GPL-3.0 copyleft (viral licence, awkward for a commercial client site); React/Next hydration cost; SaaS framing; no local-service patterns.
- **Modifications required:** Re-frame copy/sections; add services/gallery/quote; add `tel:` CTA; add SEO/schema; remove unused demo sections.
- **Performance concerns:** React/Next runtime hydration exceeds static-Astro options; still fast with SSG.

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 8 |
| 2 | Visual credibility | 9 |
| 3 | Local-service conversion fit | 5 |
| 4 | Page-speed potential | 6 |
| 5 | SEO architecture | 7 |
| 6 | Accessibility | 7 |
| 7 | Code quality | 8 |
| 8 | Ease of modification | 6 |
| 9 | Dependency weight (10=lightest) | 5 |
| 10 | Licence suitability | 6 |
| 11 | ONE-vehicle suitability | 8 |
| 12 | Quote-first conversion fit | 6 |
| 13 | Articles later | 3 |
| 14 | Image/gallery handling | 6 |
| 15 | Sticky mobile CTA capability | 6 |
| | **TOTAL** | **96 / 150** |

## Ranked results

| Rank | Candidate | Total / 150 |
|---|---|---|
| 1 | 1. Small Business Starter (free) | **137** |
| 2 | 2. Small Business Starter v2 | **133** |
| 3 | 3. AstroWind | **121** |
| 4 | 4. Astro Paper | **114** |
| 5 | 5. ScrewFast | **111** |
| 6 | 6. Astro Nano | **109** |
| 7 | 7. HyperUI | **108** |
| 8 | 8. Flowbite (community edition) | **104** |
| 9 | 9. Start Bootstrap - Agency | **103** |
| 10 | 10. Preline UI | **102** |
| 11 | 11. HTML5 UP - Landed / Story | **99** |
| 12 | 12. JAKS.dev Vault - business templates | **97** |
| 13 | 14. Cruip Open (React / Next.js) | **96** |
| 14 | 13. Tailwind Toolbox Landing Page | **94** |

## Original lightweight static implementation - does it score higher?

Two honest scenarios for a hand-written **semantic HTML + CSS + minimal vanilla JS, no framework** build (original work, zero dependencies):

**Scenario A - realistic solo build** (no dedicated designer; blog/gallery/SEO built by hand):

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 9 |
| 2 | Visual credibility | 8 |
| 3 | Local-service conversion fit | 10 |
| 4 | Page-speed potential | 10 |
| 5 | SEO architecture | 9 |
| 6 | Accessibility | 9 |
| 7 | Code quality | 9 |
| 8 | Ease of modification | 10 |
| 9 | Dependency weight (10=lightest) | 10 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 10 |
| 12 | Quote-first conversion fit | 10 |
| 13 | Articles later | 5 |
| 14 | Image/gallery handling | 8 |
| 15 | Sticky mobile CTA capability | 10 |
| | **TOTAL** | **137 / 150** |

**Scenario B - best-case design-led build** (skilled designer/dev; everything purpose-built):

| # | Criterion | Score |
|---|---|---|
| 1 | Mobile-first quality | 10 |
| 2 | Visual credibility | 9 |
| 3 | Local-service conversion fit | 10 |
| 4 | Page-speed potential | 10 |
| 5 | SEO architecture | 10 |
| 6 | Accessibility | 9 |
| 7 | Code quality | 10 |
| 8 | Ease of modification | 10 |
| 9 | Dependency weight (10=lightest) | 10 |
| 10 | Licence suitability | 10 |
| 11 | ONE-vehicle suitability | 10 |
| 12 | Quote-first conversion fit | 10 |
| 13 | Articles later | 6 |
| 14 | Image/gallery handling | 9 |
| 15 | Sticky mobile CTA capability | 10 |
| | **TOTAL** | **143 / 150** |

### Verdict on the original implementation

**No - an original build is NOT automatically higher-scoring than the best template, for a solo operator.**

- The realistic original build scores **137/150**, i.e. it *ties* the best template (Small Business Starter (free), 137/150) rather than beating it.
- Only the best-case, design-led original build (143/150) clears the best template, and only by ~6 points - earned entirely on *Dependency weight* (10 vs 9), *Licence* (10 vs 10 - both already max), *Code quality*/*Ease of modification* and exact-fit conversion.
- A from-scratch build **starts at 0** on the criteria the template hands over ready-made: *Visual credibility*, *Image/gallery handling*, *SEO architecture* and especially *Articles later* (an original must build the whole blog/MDX layer - scored 5-6 vs the template's 8). Those few points are exactly why a plain hand-written build cannot out-score a purpose-built local-service Astro template without real design effort.
- The strongest criterion for going original is *Dependency weight* and *ONE-vehicle fit* - but the winning template (Small Business Starter) already scores 9-10 on both while giving up nothing material. So the rationale for an original build is *control and zero dependencies*, not a higher score.

## Recommendation

**Single best base: `1. Small Business Starter (free)` (137/150)**  
Repo: https://github.com/alancuenca/small-business-starter - Licence: **MIT** (verified) - Demo: https://free-sbs.netlify.app/

**Why it wins:** it is the only candidate *designed* for a local trade/service business (mobile-first, 5 `tel:` links, sticky header, contact/quote flow, trust bar, reviews, gallery), it is **Astro 6 + Tailwind v4** (static output, minimal JS, near-100 Lighthouse), it ships **JSON-LD + sitemap + robots + OG + canonical** and a **blog** for later SEO articles, its whole brand/content lives in **two files** (fast to re-skin for Urbania), and it is **clean MIT** with **no fleet/booking/ecommerce baggage** to strip. It scored top on the three criteria that matter most here: local-service conversion fit (10), ONE-vehicle suitability (10) and quote-first conversion fit (10).

**Runner-up:** Small Business Starter v2 (MIT, Astro 7) - marginally lighter/faster (133/150); pick it if you prefer the newest Astro and a more minimal starting point.

**Third:** AstroWind (MIT, 121/150) - the most polished and best-maintained generic Astro base, but it is SaaS-framed with zero call/quote patterns, so more re-work is needed.

**Use plan for V1:** fork `small-business-starter`, swap brand tokens + copy in the two content files, add a 17-seat Urbania hero, add an `tel:` + WhatsApp sticky mobile bar, wire a simple quote form (email/WhatsApp - no database), add Hyderabad service-area pages and a gallery, keep the blog for later articles. Avoid: JAKS/Tailwind-Toolbox (CDN-Tailwind runtime cost), Preline (licence ambiguity), Cruip (GPL-3.0), and anything Bootstrap-heavier (Start Bootstrap) unless already familiar.

## Sources (all fetched 2026-10-03)

- https://github.com/alancuenca/small-business-starter
- https://github.com/alancuenca/small-business-starter-v2
- https://github.com/arthelokyo/astrowind
- https://github.com/satnaing/astro-paper
- https://github.com/mearashadowfax/ScrewFast
- https://github.com/markhorn-dev/astro-nano
- https://github.com/markmead/hyperui
- https://github.com/themesberg/flowbite
- https://flowbite.com/docs/getting-started/license/
- https://github.com/StartBootstrap/startbootstrap-agency
- https://github.com/htmlstreamofficial/preline
- https://html5up.net/license
- https://html5up.net/landed
- https://github.com/jakscoduxdev-netizen/JakDEvTemplates
- https://github.com/tailwindtoolbox/Landing-Page
- https://github.com/cruip/open-react-template
- https://astro.build/themes/details/free-small-business-starter/
