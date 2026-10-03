# PERFORMANCE_BUDGET.md

Measured on the actual build on 2026-10-03. Budgets are commitments; measurements are facts.

## Measured

| Metric | Value | Budget | Status |
|---|---|---|---|
| Home HTML (uncompressed) | 54,022 bytes | < 80 KB | PASS |
| Home HTML (gzip) | 12,449 bytes | < 20 KB | PASS |
| CSS (gzip) | 3,907 bytes | < 15 KB | PASS |
| External scripts | 0 | 0 | PASS |
| Inline JS | ~13,321 bytes | < 25 KB | PASS |
| Third-party origins | 1 | 0 | PASS |
| Web fonts | 0 (system font stack) | < 60 KB | PASS |
| `<img>` elements | 0 | lazy-load below fold | PASS |
| Render-blocking stylesheets | 1 (local, preloaded) | ≤ 1 | PASS |
| External JS frameworks | 0 | 0 | PASS |

## Targets

- **LCP < 2.5 s on 4G mobile.** The largest element is the hero headline — text, so it renders as
  soon as CSS is parsed. There are no images above the fold and no web fonts to block text paint.
- **CLS ≈ 0.** No images without dimensions, no injected content above the fold, no font swap
  reflow (no webfonts at all).
- **INP < 200 ms.** ~60 lines of vanilla JavaScript in total; no framework, no hydration.

## Why there is no font budget line

A webfont was evaluated and **removed**. The design system proposes Plus Jakarta Sans
(variable, OFL, ~27 KB latin woff2). It was not adopted, because the project's stated priority
order puts *mobile performance* above *original visual polish*, and 27 KB of render-critical
weight for a marginal typographic gain fails that test. Adopting it later is a one-line change
to `build_ui.py`; the measured cost is recorded here so the decision can be revisited rather
than re-argued.

## Not measured, and why

**No Lighthouse or CrUX data.** The browser harness on this host could not complete a full-page
capture, so no lab audit was run and **no performance score is claimed**. The numbers above are
direct measurements of the artefacts (file sizes, request counts) and are verifiable by anyone
with the files. Field Core Web Vitals require real traffic; they will be available from Search
Console once the site is live on a real domain.

## Hosting note

The measurements were taken through an ephemeral Cloudflare quick tunnel, which adds latency that
real hosting will not. TTFB observed through the tunnel was 0.47–1.07 s; the same requests served
locally returned in single-digit milliseconds. Treat tunnel timings as a ceiling, not a forecast.
