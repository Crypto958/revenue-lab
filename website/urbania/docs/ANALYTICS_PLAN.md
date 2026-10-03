# ANALYTICS PLAN

Date: 2026-10-03

## Status

**Not implemented.** No analytics is loaded, because doing so requires the owner's account and would set
cookies. The privacy page states accurately that the site sets no analytics or advertising cookies —
that statement must be updated *before* any analytics is enabled, not after.

## Recommended stack (free tiers)

1. **Google Analytics 4** or a privacy-friendly alternative (Plausible, Umami). A lighter option keeps
   the site fast, which matters more than report richness at one-vehicle scale.
2. **Google Search Console** — required. This is the single most valuable data source for this business:
   it shows the real queries arriving, including the long-tail group-size and luggage questions.
3. **Bing Webmaster Tools** — cheap to add, covers Bing and Copilot surfaces.

## Events to track

| Event | Fires when | Why |
|---|---|---|
| `quote_form_view` | `/request-quote/` loads | Size of the top-of-funnel |
| `quote_form_start` | First field interaction | Where drop-off begins |
| `quote_form_submit` | Validation passes and submit fires | The primary conversion |
| `quote_form_error` | Validation fails | Finds confusing fields |
| `phone_click` | Any `tel:` link tapped | Many enquiries will be calls, not forms |
| `email_click` | `mailto:` tapped | Secondary path |
| `whatsapp_click` | WhatsApp button tapped | Only once the number is enabled |
| `service_page_view` | Any of the four service pages loads | Which trip type attracts demand |
| `guide_read` | Guide pages with high scroll depth | Which questions deserve a real page |

The form already captures `source_page`, `submitted_at`, and any `utm_*` / `gclid` parameters into the
submitted payload — so attribution survives the enquiry even before analytics exists.

## Measurement model

```
TRAFFIC SOURCE (utm / referrer / GBP)
    -> LANDING PAGE
        -> SERVICE PAGE VIEW
            -> QUOTE START
                -> QUOTE SUBMISSION
                    -> QUALIFIED LEAD        (owner judgement)
                        -> QUOTED
                            -> BOOKED
```

## KPIs

- **Primary: qualified trip enquiries.** Not sessions, not page views.
- Secondary: enquiry → quotation rate; quotation → booking rate.
- Watched but not optimised for: average position, impressions, guide readership.

## Privacy

If analytics is enabled: add a consent mechanism where required, update `/privacy/`, keep IP handling
privacy-conscious, and avoid adding more than one analytics script to protect page speed.

## Attribution discipline

No lead is counted as "from Google" without checking Search Console. No claim about which channel works
is made until at least a month of real enquiry data exists.
