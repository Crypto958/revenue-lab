# DESIGN_SYSTEM.md — Urbania Group Travel

## IMPLEMENTATION NOTES — what was adopted, what diverged (added 2026-10-03)

This document is the specification. This section records where the **built site** follows it and
where it deliberately does not, so the two are not read as contradicting each other.

**Adopted in full — colour.** Every token from §1 is now live in `build_ui.py`, including the
measured contrast ratios (`--ink #131A24` 17.49:1, `--ink-3 #626E7A` 5.21:1, primary `#0F6E68`
6.09:1). Adopting verified values replaced near-miss hand-picked ones; the muted-text token in
particular moved from an estimated ~3.9:1 to a documented 5.21:1, which was a real WCAG AA
failure before.

**Variable-name mapping.** This document uses `--primary` / `--primary-strong` / `--primary-soft`;
the build uses `--accent` / `--accent-2` / `--accent-soft` for the same three values. Names were
kept to avoid churn across inline styles. Values are identical — map by position, not by name.

**Not adopted — `--brass #A9762B`.** The brass accent is specified for decoration and
micro-emphasis only. It was left out of the build because adding a second accent to a
single-accent system introduces more visual noise than it earns on a page whose job is to get a
form completed. Revisit if a real logo or photography arrives that calls for a warmer accent.

**DIVERGED — typography.** §2 proposes **Plus Jakarta Sans** (variable, OFL, ~27 KB latin woff2)
as the single UI and heading family. **The build loads no webfont at all** and uses the system
stack:

```
system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
```

Why the divergence: the project's stated priority order places **mobile performance (4)** above
**original visual polish (5)**. A 27 KB render-critical download for a marginal typographic gain
fails that test, and the site now has **zero third-party origins** as a result. This was a
deliberate, recorded decision — not an oversight.

**Cost to reverse:** one line in `build_ui.py` (restore the `<link>` and change `--sans`), plus
27 KB on first load. The measured cost is in `PERFORMANCE_BUDGET.md` so the trade-off is
re-arguable rather than re-litigated. If photography is added later and the site becomes visually
richer, the font becomes easier to justify.

**Adopted from §9 — accessibility.** Touch targets ≥44 px (the trip-type tabs were 37 px and were
raised), `:focus-visible` outlines, label-on-every-input, `prefers-reduced-motion`, and the
contrast floor all match what is now built.


An **original** design system for the Hyderabad group-travel site (one 17-seat Force Urbania now, a
verified partner network later; **quote-first, not instant booking**).

**Identity statement.** *Warm, grounded, signposted.* The system is built to read as **premium-enough and
trustworthy** — not fake-luxury, not generic taxi-app — and to work across four buyer moods at once:
Gen Z (clean, fast, mobile-first), families (clear, reassuring, large tap targets), weddings (a restrained
warm note in imagery and accents, never cloying), and corporate (sober, precise, invoice-clear).

**Benchmark justification.** We keep SIXT-grade *principles* — proof beside the headline, a planner always
in reach, segment chips, scannable cards, one dominant CTA repeated, a task-first help layer — see
`SIXT_UX_BENCHMARK.md`. We reject SIXT's **orange/black expression** entirely: our primary is a **deep
Deccan teal**, our ink is a **slate near-black (not pure black)**, and we carry a small **brass** accent
used only for decoration and micro-emphasis. Ships with **no framework, no build step, no dependencies** —
copy the tokens block and go.

---

## 1. Colour palette

All hex values are normative. Contrast ratios below were **computed (WCAG 2.1 relative luminance) on
2026-10-03**; "AA" = ≥4.5:1 for normal text, "AA-large" = ≥3:1 for ≥18.66px bold / ≥24px.

| Token | Hex | Role | Key contrast (measured) |
|---|---|---|---|
| `--ink` | `#131A24` | Primary text, dark surfaces, footer bg | 17.49:1 on white |
| `--ink-2` | `#4A5560` | Secondary text, lede copy | 7.61:1 on white |
| `--ink-3` | `#626E7A` | Muted/meta text, captions | 5.21:1 on white · 4.85:1 on `--alt` |
| `--bg` | `#FFFFFF` | Base page surface | — |
| `--alt` | `#F5F7F7` | Section band, cards on white, input wells | — |
| `--line` | `#E2E8E8` | Hairline borders, dividers | decorative |
| `--line-2` | `#C9D3D3` | Input borders, stronger dividers | decorative |
| `--primary` | `#0F6E68` | Brand action, links, focus ring, selected states | 6.09:1 white-on · 6.09:1 on white |
| `--primary-strong` | `#0A514C` | Primary hover/active, dark teal fills | 9.15:1 white-on |
| `--primary-soft` | `#E7F1F0` | Tinted chips, info wells | primary text on it = 5.29:1 |
| `--brass` | `#A9762B` | Decorative accent only (rules, icon fills, ≥24px or non-text) | 3.95:1 on white → **large/decor only** |
| `--brass-text` | `#8A5A12` | Brass used as small text | 5.91:1 on white |
| `--success` | `#17795A` | Success text/icon, confirmation | 5.36:1 on white |
| `--danger` | `#B42318` | Error text/border, destructive | 6.57:1 on white · white-on = 6.57:1 |
| `--warning-fg` | `#8A5A0B` | Warning text | 5.55:1 on `--warning-bg` |
| `--warning-bg` | `#FFF7E6` | Warning well | — |
| `--footer-fg` | `#C7D3DD` | Footer body text on `--ink` | 11.48:1 |

Rules: **brass is never a CTA colour** (that would drift toward SIXT's orange). Only `--primary` /
`--primary-strong` carry actions. Never set body text in `--ink-3` on `--alt` below 16px — 4.85:1 passes,
but keep it for meta, not paragraphs.

CSS:

```css
:root{
  --ink:#131A24; --ink-2:#4A5560; --ink-3:#626E7A;
  --bg:#FFFFFF; --alt:#F5F7F7;
  --line:#E2E8E8; --line-2:#C9D3D3;
  --primary:#0F6E68; --primary-strong:#0A514C; --primary-soft:#E7F1F0;
  --brass:#A9762B; --brass-text:#8A5A12;
  --success:#17795A; --danger:#B42318;
  --warning-fg:#8A5A0B; --warning-bg:#FFF7E6;
  --footer-fg:#C7D3DD;
}
```

---

## 2. Typography

### Typefaces (free, safe to load, with real measured cost)

Measured woff2 sizes below were fetched from Google Fonts on **2026-10-03** (latin subset, GNU/Open Font
Licence or Apache-2.0 — all free for commercial use, self-hostable).

| Family | Licence | Measured latin woff2 | Verdict |
|---|---|---|---|
| **Plus Jakarta Sans** (variable 200–800) | OFL 1.1 | **≈27 KB** (largest subset) | **CHOSEN** — one file covers all UI weights |
| Manrope (variable 200–800) | OFL 1.1 | ≈25 KB | Good runner-up, more geometric |
| Source Sans 3 (variable) | OFL 1.1 | ≈29 KB | Neutral, slightly newsy |
| Inter (variable) | OFL 1.1 | ≈48 KB latin (≈85 KB latin-ext) | Excellent but heaviest; only if max neutrality is required |
| Fraunces (variable, optical) | OFL 1.1 | ≈59–67 KB per subset | **Optional display only** — defer/subset, never site-wide |

**Recommendation:** ship **one** family — **Plus Jakarta Sans** variable — for headings *and* UI, with a
system fallback stack. It is modern, slightly humanist, friendly to Gen Z, sober enough for corporate, and
cheaper than Inter while looking more distinct. Add **Fraunces** *only* as an optional editorial hero
accent later; if you do, self-host one latin subset, `font-display:swap`, and preload it — expected
display ≤8 KB–60 KB depending on subset (measured subset sizes today ranged 19.7 KB–67.3 KB, so treat the
display face as a real budget line).

**Performance cost & mitigation (concrete).**
- One variable family ≈ 27 KB woff2 over the wire versus Inter ≈ 48 KB → **~21 KB saved** by choosing
  Plus Jakarta Sans. A second family *at least doubles* font bytes and adds a second render-blocking
  request.
- Web fonts block text render until loaded; mitigate with `font-display:swap`, **preload** only the face
  used above the fold, `unicode-range` subsetting (Google serves per-subset files automatically; self-host
  the same way), and a matched fallback (`system-ui`) with `size-adjust` to limit layout shift.
- Budget: **fonts ≤ 60 KB total** for v1. If adding Fraunces breaks that, drop it.

Fallback stack: `font-family:'Plus Jakarta Sans', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;`

### Scale (sizes / weights / line-heights)

Fluid via `clamp()`; weights 400/500/600/700; letter-spacing tightens as size grows.

| Style | Size | Weight | Line-height | Tracking |
|---|---|---|---|---|
| Display (hero h1) | `clamp(34px, 5.2vw, 60px)` | 700 | 1.04 | `-0.03em` |
| H2 | `clamp(26px, 3.2vw, 40px)` | 700 | 1.12 | `-0.025em` |
| H3 | `clamp(19px, 1.8vw, 23px)` | 600 | 1.25 | `-0.02em` |
| H4 | 17px | 600 | 1.3 | `-0.01em` |
| Body-lg (lede) | `clamp(17px, 1.8vw, 20px)` | 400 | 1.6 | 0 |
| Body | 17px | 400 | 1.62 | 0 |
| Body-sm | 15px | 400 | 1.55 | 0 |
| Meta/caption | 13.5px | 400/500 | 1.45 | 0 |
| Eyebrow/label | 12px | 600 | 1.4 | `0.14em` UPPERCASE |
| Button | 16px (sm 15px) | 600 | 1 | `0.005em` |

Body copy max width 66ch; lede 62ch. Never set body <16px on mobile.

---

## 3. Spacing scale

Base unit **4px**; a linear-plus set keeps rhythm predictable. Use for margin, padding, gap.

| Token | px |
|---|---|
| `--sp-1` | 4 |
| `--sp-2` | 8 |
| `--sp-3` | 12 |
| `--sp-4` | 16 |
| `--sp-5` | 20 |
| `--sp-6` | 24 |
| `--sp-8` | 32 |
| `--sp-10` | 40 |
| `--sp-12` | 48 |
| `--sp-16` | 64 |
| `--sp-20` | 80 |
| `--sp-24` | 96 |

Rules: section vertical padding `clamp(48px, 6vw, 88px)`; card padding 20–24px; form field vertical gap
16px; grid gap 18px (mobile 14px). Container: `max-width:1180px; margin:0 auto; padding-inline:clamp(18px, 5vw, 24px)`.

---

## 4. Border radii

| Token | px | Use |
|---|---|---|
| `--r-sm` | 6px | inputs, small chips, tags |
| `--r` | 10px | buttons, wells |
| `--r-lg` | 16px | cards, panels, media |
| `--r-xl` | 24px | hero media, feature bands |
| `--r-pill` | 999px | chips/toggles, badges, avatars |

Radii signal "approachable but orderly". Keep one shape language; do not mix 4px and 24px on peers.

---

## 5. Shadow levels

Shadows are **soft and teal-tinted** (not grey/black), signalling lift without heaviness. Borders do the
baseline work; shadows are for elevation only.

```css
--sh-0:none;
--sh-1:0 1px 2px rgba(19,26,36,.05);
--sh-2:0 1px 2px rgba(19,26,36,.05), 0 8px 24px rgba(15,110,104,.08);
--sh-3:0 2px 4px rgba(19,26,36,.06), 0 16px 40px rgba(15,110,104,.12);
--sh-focus:0 0 0 3px rgba(15,110,104,.35);
```

- `sh-1` static cards · `sh-2` card hover / raised planner · `sh-3` modals, sticky bars.
- Never stack two large shadows; never animate shadow size (see Motion).

---

## 6. Buttons — variants & states

Sizes: **md** `padding:14px 24px` · **sm** `10px 16px` · **lg** `16px 28px`. Min height 48px (md/lg),
44px (sm). Radius `--r`.

| Variant | Default | Hover | Active | Disabled | Focus |
|---|---|---|---|---|---|
| **Primary** — *Get a quote* | bg `--primary`, text `#fff` | bg `--primary-strong`, `translateY(-1px)` | `translateY(0)`, bg `--primary-strong` | bg `#9DBAB7`, text `#fff`, `cursor:not-allowed`, no transform | `--sh-focus` |
| **Secondary** — *WhatsApp / Call* | bg `#fff`, text `--ink`, border `--line-2` | bg `--alt` | bg `--primary-soft` | text `--ink-3`, border `--line`, no shadow | `--sh-focus` |
| **Ghost/text link** | text `--primary`, underline 1px 30% | underline 100% | — | text `--ink-3` | `--sh-focus`, `border-radius:4px` |
| **Destructive** | bg `--danger`, text `#fff` | darken to `#961E12` | — | 50% opacity | `--sh-focus` |

Loading state: label replaced by "Sending…", keep button width stable (reserve via `min-width`), add
`aria-busy="true"`, `disabled`. All buttons: `border:1px solid transparent`, `transition:background .16s,
transform .16s, box-shadow .16s`. In a `<button>` use a real `<button>`; for links that navigate use `<a>`
styled as a button.

---

## 7. Form controls

Base: `width:100%; padding:13px 14px; font-size:16px; font-family:inherit; color:--ink; background:#fff;
border:1px solid --line-2; border-radius:--r-sm`. Focus: `outline:0; border-color:--primary;
box-shadow:--sh-focus`. Invalid: `border-color:--danger`. Labels **always visible above the control**
(never placeholder-as-label). Helper text 13px `--ink-3`; error text 13.5px `--danger` with the control
`aria-invalid="true"` and `aria-describedby` pointing at the error id.

- **Text / email / tel** — single line; `inputmode` set (`tel`, `email`). Autocomplete attributes on.
- **Select** — native `<select>` (no custom JS listbox) with `--r-sm`; custom chevron via background SVG
  kept 24px away from the right edge. Native keeps mobile accessibility free.
- **Date range** — two native `type="date"` (or `datetime-local`) fields "Pickup date", "Return date
  (optional)" side by side ≥480px, stacked below. No third-party date library. A small helper line echoes
  the chosen day ("Fri 12 Jun · evening"). Validate order (return ≥ pickup) with an inline message.
- **Radio / chip group** — single-select: pill chips styled as `<label>` wrapping a visually-hidden
  `<input type=radio>`; selected = `--primary-soft` bg, `--primary` border + text, `aria-checked` handled
  by the radio. Multi-select variants use `aria-pressed` toggle buttons. Min target 44px tall.
- **Stepper** — for "Group size (1–17)": `−` / value / `+` buttons ≥44×44px, `role="spinbutton"` or a
  labelled `<input type="number" min=1 max=17>` with hidden spinners + visible −/+; announce changes
  (`aria-live="polite"` on the value). Clamp at 17 with a gentle inline note ("More than 17? We'll quote a
  multi-vehicle plan").
- **File-free by design** — no upload control anywhere (owner decision); attachments happen over
  WhatsApp/email, stated in helper text.

Every control is reachable and operable by keyboard and shows the focus ring. Fieldset + legend for radio
groups. Required fields marked with a visible "*" **and** `required` + an error summary at the top of the
form on submit failure.

---

## 8. Icon system

- **Approach:** a single inline **SVG sprite** (`<symbol>` + `<use>`) authored in-house, or a permissively
  licensed set (e.g. Lucide / Feather / Heroicons — MIT). **Never** SIXT's icons.
- **Grid:** 24×24 with 2px stroke, round caps/joins, `currentColor` so icons inherit text colour.
- **Sizes:** 20px inline-with-text, 24px default, 28–32px feature. Minimum 16px.
- **Accessibility:** decorative icons `aria-hidden="true"` + `focusable="false"`; meaningful icons get a
  `<title>` or adjacent visible label. Never convey meaning by icon alone.
- **Cost:** stroked, single-colour icons are tiny; a curated sprite of ~25 icons is typically well under
  10 KB inline and adds **zero extra requests** when inlined.

---

## 9. Cards

Shared anatomy: media (optional) → eyebrow (optional) → H3 → body → single primary action. Radius
`--r-lg`, border `--line`, bg `#fff`, hover → border `--line-2` + `--sh-2`.

| Variant | Structure | Use |
|---|---|---|
| **Use-case card** | 16:9 photo + occasion + outcome line + "Get a quote" | Home grid (Wedding, Corporate, Airport, Family) |
| **Fleet card** | Photo + seat/luggage facts table + "Request this vehicle" | Urbania spec page |
| **Guide card** | Text-first (no photo) + reading-time meta + link | Blog/guides index |
| **Partner card** | Verification badge as hero element + coverage + "Check availability" | Third-party transport network |
| **Quote/step card** | Numbered steps, no photo | "How it works" |

Rules: exactly one primary action per card; whole-card link only when there is one destination (then
`a.card{display:block}` with the heading as the link text for a11y); no nested interactive elements.

---

## 10. Image treatment & aspect ratios

- **Aspect ratios:** `16:9` hero/wide media · `4:3` card photos · `1:1` avatars & badges · `21:9` optional
  section band. Lock ratio with `aspect-ratio` to prevent shift.
- **Delivery:** `<img>` with `srcset`/`sizes`, `loading="lazy"` and `decoding="async"` below the fold;
  hero image `loading="eager"` + `fetchpriority="high"`. Serve modern formats (AVIF/WebP with fallback).
- **Treatment:** warm, natural, real-Hyderabad photography of groups and moments (loading luggage,
  boarding, arrival). Consistent light grade; **no** heavy filters, duotones or stock-corporate gloss.
  Optional subtle teal-to-transparent scrim behind hero text for legibility.
- **Overlay text:** only over images with a proven contrast scrim; otherwise place text on a solid surface.
- **Attribution/ethics:** photos are ours or licensed; never SIXT's; when a partner vehicle is shown, label
  it as a partner vehicle.

---

## 11. State design (loading / empty / error / success)

- **Loading:** skeleton blocks using `--alt` with a 1.4s shimmer **only** for content regions; for form
  submit use an inline status + button "Sending…" state (no full-screen spinner). Skeletons mirror the
  final layout (same heights) to avoid jump.
- **Empty:** friendly, never blank. Icon + one sentence + a single action. E.g. guides filter with no
  results → "No guides match that yet — browse all guides."
- **Error:** color `--danger` for text/border, `--warning-*` for non-blocking notices. Plain language,
  states the fix, preserves entered data, and points to the field via `aria-describedby`. A form-level
  error summary appears at the top on submit failure.
- **Success (quote enquiry — the important one):** a real `<div role="status">` confirmation containing a
  **reference number**, the honest response-time promise ("We'll reply within X hours"), the WhatsApp/Call
  fallback, and what happens next. This is our most important state because the site captures *briefs*,
  not bookings.

Accessibility: status/error regions use `role="status"` / `role="alert"` and `aria-live` so screen readers
announce state changes. Never rely on colour alone — pair with an icon and text.

---

## 12. Motion

- **Tokens:** `--dur-1:120ms` (hover tint), `--dur-2:180ms` (button/transform), `--dur-3:260ms` (panels,
  drawer), `--ease:cubic-bezier(.2,.7,.3,1)`.
- **Rules:** animate only `transform` and `opacity` (compositor-friendly); never animate `width`, `height`,
  `top`/`left`, or shadow blur. Motion is functional — a 1px lift on hover, a 260ms drawer slide — never
  decorative spectacle. Focus states appear **instantly** (no transition).
- **Reduced motion:** honour the OS setting globally:
  ```css
  @media (prefers-reduced-motion: reduce){
    *,*::before,*::after{animation:none!important;transition:none!important}
    html{scroll-behavior:auto}
  }
  ```
  Under reduced motion the drawer/chips still change state — they just snap instead of sliding.

---

## 13. Accessibility

- **Contrast:** aim WCAG 2.1 **AA** — 4.5:1 body text, 3:1 large text and UI borders/icons. Palette values
  above were measured today; the ones used for text all pass (see §1). `--brass` `#A9762B` = 3.95:1 →
  **only** for ≥24px text or decorative elements; use `--brass-text` `#8A5A12` (5.91:1) for small text.
- **Focus:** visible, never removed. `:focus-visible{outline:3px solid var(--primary); outline-offset:2px;
  border-radius:4px}`, plus `--sh-focus` on inputs/buttons. Contrast of focus indicator ≥3:1 against both
  the component and the page.
- **Touch targets:** minimum **44×44px** (md/lg buttons 48px; chips 44px; icon buttons 44px; stepper ± 44px).
  Spacing between targets ≥8px.
- **Labels:** every control has a persistent visible `<label>` (or `<legend>` for groups); placeholders are
  never the label; icons/buttons have accessible names (`aria-label`); landmarks (`header/nav/main/footer`),
  one `<h1>` per page, logical heading order, skip-to-content link.
- **Forms:** `required`, `aria-invalid`, `aria-describedby` for hints/errors; error summary at top of form;
  `role="status"`/`role="alert"` for async results; time/`autocomplete` hints; group radio/checkbox inputs
  in `<fieldset><legend>`.
- **Media:** meaningful `<img alt>`; decorative images `alt=""`; if video is added, captions/transcript.
- **Language & zoom:** `lang="en-IN"`; layout usable at 200% zoom and 320px width; never disable pinch-zoom.
- **Testing:** keyboard-only pass, screen-reader spot-check (VoiceOver/NVDA/TalkBack), automated axe scan,
  and a manual contrast check of any new colour pairing before shipping.

---

## 14. Implementation notes (no framework, no build)

- Drop the `:root` token blocks (§1, §3–5, §12) into one `style.css`; reference tokens everywhere — never
  hard-code a hex in a component.
- One CSS file, one inline SVG sprite, one preloaded font subset. No JS framework; progressive-enhancement
  only — the quote form posts and validates server-side and works with JS disabled.
- Suggested naming: BEM-lite (`.card`, `.card__media`, `.btn.btn--primary`) or plain utility-free semantic
  classes; keep it consistent with the existing site stylesheet (`style.css` already uses teal + slate ink,
  so this system is a **refinement**, not a rewrite, of the deployed identity).
- Performance budget: HTML+CSS ≤ 60 KB gzipped, fonts ≤ 60 KB, hero image ≤ 150 KB, LCP ≤ 2.5s on 4G.

---

## 15. Do / Don't

**Do:** one primary action per view; proof beside the headline; chips for occasions; honest quote-first
language; tokenised colour/spacing; visible focus everywhere; test at 320px and 200% zoom.

**Don't:** adopt SIXT's orange/black, logo, type, icons, photos or exact geometry; use brass on CTAs; show
a live price we can't honour; use false urgency; animate non-composited properties; ship placeholder-as-
label; exceed the font/asset budget; use pure black `#000` for large surfaces (use `--ink`).
