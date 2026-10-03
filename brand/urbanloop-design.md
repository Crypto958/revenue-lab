---
version: alpha
name: UrbanLoop
description: Premium Group Mobility. Restrained automotive minimalism — a factory-grey Urbania, monochrome chrome, and one functional accent reserved for interaction.
colors:
  primary: "#111518"
  graphite: "#2A3238"
  secondary: "#57626A"
  muted: "#828D95"
  mist: "#D9E0E4"
  fog: "#EEF2F4"
  paper: "#FAFBFC"
  action: "#0F6A63"
  action-ink: "#0A4A45"
  alert: "#9A3412"
typography:
  display:
    fontFamily: Inter
    fontSize: 3.5rem
    fontWeight: 600
    lineHeight: 1.04
    letterSpacing: "-0.028em"
  h1:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.024em"
  h2:
    fontFamily: Inter
    fontSize: 1.75rem
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  h3:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.015em"
  body-lg:
    fontFamily: Inter
    fontSize: 1.1875rem
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "0em"
  body:
    fontFamily: Inter
    fontSize: 1.0625rem
    fontWeight: 400
    lineHeight: 1.62
    letterSpacing: "0em"
  small:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  label:
    fontFamily: Inter
    fontSize: 0.71875rem
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.16em"
  descriptor:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.30em"
rounded:
  sm: 6px
  md: 10px
  lg: 16px
  pill: 100px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 72px
components:
  button-primary:
    backgroundColor: "{colors.action}"
    textColor: "{colors.paper}"
    rounded: "{rounded.md}"
    padding: 15px
  button-primary-hover:
    backgroundColor: "{colors.action-ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.md}"
    padding: 15px
  button-secondary:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 15px
  card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 24px
  card-alt:
    backgroundColor: "{colors.fog}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 24px
  input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 13px
  surface-dark:
    backgroundColor: "{colors.graphite}"
    textColor: "{colors.paper}"
    rounded: "{rounded.lg}"
    padding: 32px
  text-secondary:
    textColor: "{colors.secondary}"
    typography: "{typography.small}"
  text-muted:
    textColor: "{colors.muted}"
    typography: "{typography.label}"
  divider:
    backgroundColor: "{colors.mist}"
    size: 1px
    height: 1px
  error-text:
    textColor: "{colors.alert}"
    typography: "{typography.small}"
---

## Overview

UrbanLoop is a premium group-mobility operator in Hyderabad running Force Urbania
vehicles in factory grey. The brand is deliberately quiet: recognition comes from
typography, proportion, placement and repetition across a fleet — not from
decoration. It must never read as a taxi company, a tour operator, a travel agency,
a bus operator or a limousine cliché.

The system is monochrome chrome with **exactly one functional accent**, and it is
used for interaction only — never on a vehicle.

## Colors

The palette is a single **cool-neutral** ramp plus one accent. This is a correction
of the reference board, which mixed two cool greys (`#6E7378`, `#9AA0A6` at hue
210°) with two warm ones (`#F5F3EE` 43°, `#E4E6E2` 90°). Adjacent swatches visibly
disagreed. Every neutral here sits at hue 200–210° so the ramp reads as one family.

- **primary (#111518):** body text and the deepest surface. 17.7:1 on paper.
- **graphite (#2A3238):** headings and dark panels. 12.6:1 on paper.
- **secondary (#57626A):** secondary text. 6.0:1 on paper — the lightest neutral safe for body copy.
- **muted (#828D95):** icons, inactive states, hairline accents. **3.3:1 — non-text only.** It fails body contrast by design; do not set copy in it.
- **mist (#D9E0E4):** dividers and subtle fills.
- **fog (#EEF2F4):** alternating section background.
- **paper (#FAFBFC):** page background.
- **action (#0F6A63):** THE interactive accent. Primary buttons and links only. 6.2:1 with paper — the highest-chroma value in the system (spread 91, against 12 for the neutrals), which is what makes the primary action findable.
- **action-ink (#0A4A45):** pressed/hover state. 9.8:1 with paper.
- **alert (#9A3412):** form errors only. Deliberately the single warm value in the system; semantic colour is exempt from the cool-neutral rule.

**Contrast floor:** body text 4.5:1, large text and UI boundaries 3:1. `muted` on
`paper` is 3.3:1 and is therefore restricted to non-text use.

## Typography

Inter for everything — it is genuinely well-engineered, has an OFL licence, and
renders reliably across platforms.

- **The wordmark is NOT Inter live text.** It is Inter's glyph outlines, composed
  and optically corrected, emitted as standalone path geometry with no font
  dependency. Never retype the name in a font and call it the logo.
- **Optical spacing is measured, not guessed.** Pair corrections live in
  `brand/build_wordmark.py` and are derived from `brand/measure_spacing.py`.
- **`label`** is the only letterspaced style and is reserved for small uppercase
  eyebrows. **`descriptor`** is used only in the descriptor lockup.
- Negative tracking on headings is intentional and tightens as size increases.
- Inter alone reads as generic "modern SaaS" — that is the single strongest
  AI-template tell. Distinctiveness therefore has to come from the wordmark's
  drawn geometry, not from the body face.

## Layout

8px base. `section` (72px) is the standard vertical rhythm between page bands.
Content measure caps at 1180px; long-form prose caps at 72 characters.

## Elevation & Depth

Depth is minimal and functional: hairline borders (`mist`) and one soft shadow for
raised cards. No glow, no gradient fills, no ambient blurs.

## Shapes

Radii are restrained — 6/10/16px, with `pill` only for filter chips and tags. A
vehicle is not rounded and the interface should not be either.

## Components

Only `button-primary` carries the accent. If two things on a screen are both
`action`, neither reads as primary.

## Logo — clear space, minimum size, backgrounds

**Clear space:** margin equal to the cap height of the wordmark on all sides.
Nothing — type, rule, image edge or vehicle panel — enters that zone.

**Minimum sizes** (below these, use the monogram alone):

| Mark | Minimum |
|---|---|
| Primary wordmark | 96px wide |
| Horizontal lockup | 140px wide |
| Descriptor lockup | 220px wide |
| UL monogram | 18px |
| Favicon / avatar | 16px |

**Backgrounds:**
- Wordmark: `ink` on `paper`/`fog`, or `paper` on `graphite`/`ink`. Nothing else.
- Monogram: `ink`, `paper`, or `action` on a quiet ground. Never on a photograph
  without a solid or scrimmed plate behind it.
- Never place any mark on the factory-grey bodywork in anything but charcoal or white.

## Do's and Don'ts

**Do**
- Keep the vehicle factory grey. Branding is applied, never painted over.
- Use one accent, for interaction only.
- Reproduce the master marks as supplied — never rebuild them from a font.
- Give the mark its clear space and use the monogram below the wordmark minimum.

**Don't**
- No stripes, swooshes, gradients, chrome, gold or decorative graphics.
- No phone number, service list or tagline strip across the vehicle.
- No car-silhouette, steering-wheel or road-icon logos.
- No recolouring the marks outside the values above.
- No stretching, skewing, outlining, shadowing or re-spacing the wordmark.
- Never claim, imply or depict a vehicle, customer or review that is not real.

## Implementation notes

- `slate` and `muted` were chosen to satisfy WCAG at the sizes they are used at;
  changing either requires re-running the contrast check in
  `brand/measure_spacing.py`'s sibling calculations before shipping.
- The `action` accent is absent from the reference board. Its addition is
  deliberate: a pure-grey system gives the primary call-to-action no way to
  distinguish itself, which is a conversion problem, not a taste preference.
- `Vehicle Grey` from the reference board was renamed and split. It conflated an
  OEM paint reference with a UI token; paint and interface colours are now
  governed separately (see `brand/livery/`).
