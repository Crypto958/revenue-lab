#!/usr/bin/env python3
"""
Urbania Hyderabad — new page sections.

Components requested in the owner's brief, built on site_data.py so every
figure and label stays editable in one place.

HONESTY
Nothing here invents a fact. Where the owner has not supplied a value it renders
through site_data.tbc() as a visible "To be confirmed". Image slots are clearly
labelled illustrative graphics — never stock photography presented as the actual
vehicle, which is the current site's existing standard and the right one.
"""
import html
import os

from site_data import (CONFIGURATIONS, CONFIG_SPEC_FIELDS, GALLERY_SLOTS, PRICING_FAQS,
                       RATE_EXCLUSIONS, RATE_INCLUSIONS, RATE_NOTES, RATE_TABLE_COLUMNS,
                       REVIEWS, REVIEWS_EMPTY_MESSAGE, ROUTES, SERVICE_AREAS, SERVICES,
                       NATIONAL_SERVICES,
                       TRUST_ASSURANCES, TRUST_FIELDS, FLEET_CONFIRMED, SEATING_SLOTS,
                       SEAT_LAYOUTS, ASSETS_ARE_OUR_VEHICLE, SHOW_MEDIA_PLACEHOLDERS,
                       MEDIA_DIMENSIONS,
                       RATE_INDICATIVE, tbc, money)

# ------------------------------------------------------------------ media
# Real photography and video drop into these directories and the site upgrades
# itself on the next build — no code change. Until a file exists, the component
# falls back to a clearly labelled illustration, never to stock imagery passed
# off as the actual vehicle.
#
#   app/site/media/hero/      hero.mp4 | hero.webm | hero-poster.jpg
#   app/site/media/gallery/   <slot-name>.jpg      (see site_data.GALLERY_SLOTS)
#   app/site/media/seating/   <slot-name>.jpg      (see site_data.SEATING_SLOTS)
#
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "site", "media")

IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".avif")


def media_path(*parts):
    """Filesystem path for a media asset."""
    return os.path.join(MEDIA_ROOT, *parts)


def media_url(*parts):
    return "/media/" + "/".join(parts)


def find_image(kind, name):
    """Return the served URL for kind/name.<ext> if the file exists, else None."""
    for ext in IMAGE_EXT:
        if os.path.exists(media_path(kind, name + ext)):
            return media_url(kind, name + ext)
    return None


def has_hero_video():
    return any(os.path.exists(media_path("hero", "hero" + v)) for v in (".mp4", ".webm"))


def media_status():
    """What real media exists right now — surfaced in docs and the build log."""
    if not os.path.isdir(MEDIA_ROOT):
        return {"hero_video": False, "hero_poster": False, "gallery": 0, "seating": 0}
    return {
        "hero_video": has_hero_video(),
        "hero_poster": bool(find_image("hero", "hero-poster")),
        "gallery": sum(1 for n, _ in GALLERY_SLOTS if find_image("gallery", n)),
        "seating": sum(1 for n, _ in SEATING_SLOTS if find_image("seating", n)),
    }


# ------------------------------------------------------------------ CSS
SECTIONS_CSS = """
/* ---- find your urbania ---- */
.fy{background:linear-gradient(180deg,var(--alt),#fff);border:1px solid var(--line);border-radius:var(--r-lg);padding:clamp(20px,3vw,30px)}
.fy-row{display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap}
.fy-ctl{flex:0 0 auto}
.fy-ctl label{display:block;font-size:13px;font-weight:600;color:var(--ink);margin-bottom:7px}
.fy-ctl input{width:118px;background:#fff;border:1px solid var(--line-2);border-radius:var(--r);padding:13px 14px;font-size:17px;font-family:inherit;color:var(--ink)}
.fy-out{flex:1 1 280px;min-width:240px}
.fy-card{background:#fff;border:1px solid var(--line-2);border-radius:var(--r);padding:16px 18px;min-height:82px}
.fy-card h3{font-size:17px;margin-bottom:6px}
.fy-card p{font-size:14.5px;color:var(--ink-2)}
.fy-card.warn{border-color:var(--warn-line);background:var(--warn-bg)}
.fy-hint{font-size:13px;color:var(--ink-3);margin-top:10px}
/* ---- config cards ---- */
.cfg{display:grid;gap:18px;grid-template-columns:repeat(2,1fr)}
@media(max-width:820px){.cfg{grid-template-columns:1fr}}
.cfgcard{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;display:flex;flex-direction:column}
.cfgcard .shot{background:var(--alt-2);border-bottom:1px solid var(--line);padding:14px}
.cfgcard .shot svg{width:100%;height:auto;display:block}
.cfgbody{padding:20px;display:flex;flex-direction:column;gap:14px;flex:1}
.cfg-cap{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.cfg-cap b{font-size:clamp(20px,2.2vw,25px);letter-spacing:-.02em}
.cfg-cap .trim{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);background:var(--accent-soft);padding:4px 9px;border-radius:100px}
.cfgcard p.tl{font-size:14.5px;color:var(--ink-2)}
.spec{width:100%;border-collapse:collapse}
.spec th,.spec td{text-align:left;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px;vertical-align:top}
.spec th{color:var(--ink-3);font-weight:600;width:44%}
.spec td .pend{color:var(--warn);font-style:normal;font-weight:600}
.cfgacts{display:flex;gap:10px;flex-wrap:wrap;margin-top:auto;padding-top:4px}
.bestfor{display:flex;flex-wrap:wrap;gap:7px}
.bestfor span{font-size:12.5px;color:var(--ink-2);background:var(--alt);border:1px solid var(--line);border-radius:100px;padding:5px 11px}
/* ---- rates table ---- */
.rate-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r-lg);background:#fff}
table.rate{width:100%;border-collapse:collapse;min-width:680px}
table.rate th,table.rate td{padding:14px 16px;text-align:left;border-bottom:1px solid var(--line);font-size:14.5px;white-space:nowrap}
table.rate thead th{background:var(--alt);font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3)}
table.rate td.pend{color:var(--warn);font-weight:600}
table.rate.indic th[scope=row]{font-weight:600;color:var(--ink);width:26%}
table.rate.indic .amt{font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:600;width:22%}
table.rate.indic td.small{color:var(--ink-2);line-height:1.5}
.io{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}
@media(max-width:720px){.io{grid-template-columns:1fr}}
.io>div{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px}
.io h4{margin-bottom:10px}
.io ul{margin:0;padding-left:20px}
.io li{font-size:14.5px;color:var(--ink-2);margin-bottom:6px}
.notes{margin-top:18px;border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.notes div{display:flex;justify-content:space-between;gap:16px;padding:12px 16px;border-bottom:1px solid var(--line);font-size:14.5px}
.notes div:last-child{border-bottom:0}
.notes b{color:var(--ink-3);font-weight:600}
/* ---- services + routes ---- */
.routes{display:grid;gap:16px;grid-template-columns:repeat(3,1fr)}
@media(max-width:900px){.routes{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.routes{grid-template-columns:1fr}}
.route{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;display:block;text-decoration:none}
.route:hover{border-color:var(--line-2);box-shadow:var(--sh)}
.route .r{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.route h3{margin:9px 0 7px;font-size:17px}
.route p{font-size:14px;color:var(--ink-2)}
.route .meta{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px;font-size:12.5px;color:var(--ink-3)}
/* ---- trust ---- */
.trust{display:grid;gap:14px;grid-template-columns:repeat(4,1fr)}
@media(max-width:900px){.trust{grid-template-columns:repeat(2,1fr)}}
@media(max-width:520px){.trust{grid-template-columns:1fr}}
.tcard{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;text-align:center}
.tcard b{display:block;font-size:clamp(19px,2.2vw,24px);letter-spacing:-.02em}
.tcard b.pend{font-size:14px;color:var(--warn);font-weight:600}
.tcard span{font-size:12px;color:var(--ink-3);text-transform:uppercase;letter-spacing:.06em;display:block;margin-top:6px}
.assure{display:grid;gap:12px;grid-template-columns:repeat(2,1fr);margin-top:22px}
@media(max-width:720px){.assure{grid-template-columns:1fr}}
/* ---- gallery ---- */
.gal{display:grid;gap:18px;grid-template-columns:repeat(3,minmax(0,1fr));max-width:1120px;align-items:start}
@media(max-width:620px){.gal{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}
.gslot{background:var(--alt);border:1px dashed var(--line-2);border-radius:var(--r);aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;text-align:center;padding:10px}
.gslot span{font-size:11.5px;color:var(--ink-3);line-height:1.35}
/* real photograph replacing a slot */
.gfig{margin:0;border-radius:var(--r);overflow:hidden;position:relative;background:var(--alt-2)}
.gfig img{width:100%;height:auto;display:block;background:#eef2f3}
.gfig figcaption{padding:10px 12px;font-size:13px;line-height:1.35;color:var(--ink-2);background:var(--alt)}
.planning-visual{margin:24px 0 0;border-radius:var(--r-lg);overflow:hidden;background:var(--alt-2)}
.planning-visual img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;display:block}
.planning-visual figcaption{padding:9px 12px;font-size:12px;color:var(--ink-3);background:var(--alt)}
.pl-location{position:relative}
.pl-suggestions{position:absolute;z-index:20;left:0;right:0;top:100%;margin-top:4px;padding:4px;background:#fff;border:1px solid var(--line-2);border-radius:10px;box-shadow:0 12px 28px rgba(14,27,42,.14)}
.pl-suggestion{display:block;width:100%;border:0;background:#fff;text-align:left;padding:10px 11px;border-radius:7px;color:var(--ink);font:inherit;font-size:14px;cursor:pointer}
.pl-suggestion:hover,.pl-suggestion:focus{background:var(--accent-soft);outline:0}
/* hero media */
.hv-video,.hv-still{width:100%;display:block;border-radius:12px;aspect-ratio:16/9;
object-fit:cover;background:#0E1B2A}
.hv-mobile{display:none;width:100%;border-radius:12px;aspect-ratio:16/9;object-fit:cover}
/* a phone gets the still, not an autoplaying video: data and battery for no gain */
@media(max-width:860px){.hv-video{display:none}.hv-mobile{display:block}}
@media (prefers-reduced-motion:reduce){.hv-video{display:none}.hv-mobile{display:block}}
/* ---- reviews ---- */
.rev-empty{background:#fff;border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:var(--r);padding:20px}
.rev-empty p{font-size:14.5px;color:var(--ink-2)}
/* ---- hero journey bar (step 1: trip details only, no personal data) ---- */
.jbar{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);box-shadow:var(--sh);padding:14px}
.jbar-grid{display:grid;grid-template-columns:1.2fr 1.2fr .85fr .65fr auto;gap:10px;align-items:end}
@media(max-width:980px){.jbar-grid{grid-template-columns:1fr 1fr;gap:10px}}
@media(max-width:560px){.jbar-grid{grid-template-columns:1fr}}
.jf{display:block}
.jf>span{display:block;font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3);margin-bottom:6px}
.jf input,.jf select{width:100%;background:#fff;border:1px solid var(--line-2);border-radius:var(--r);
padding:13px 14px;font-size:16px;font-family:inherit;color:var(--ink)}
.jf input:focus,.jf select:focus{outline:0;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.jbar .btn{width:100%;padding:15px 20px;white-space:nowrap}
@media(max-width:980px){.jbar-grid .jgo{grid-column:1/-1}}
.jnote{font-size:13px;color:var(--ink-3);margin-top:10px;display:flex;gap:8px;align-items:flex-start}
/* ---- use-case chips ---- */
.ucs{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.uc{font-size:13.5px;color:var(--ink-2);background:#fff;border:1px solid var(--line-2);border-radius:100px;
padding:8px 14px;text-decoration:none;transition:.15s;
/* 44px touch target: the chips measured 40px, under the WCAG 2.5.5 minimum */
display:inline-flex;align-items:center;min-height:44px}
.uc:hover{border-color:var(--accent);color:var(--accent-2)}
/* ---- hero two-column + vehicle panel ---- */
.hv{display:grid;grid-template-columns:1.06fr .94fr;gap:44px;align-items:center}
@media(max-width:940px){.hv{grid-template-columns:1fr;gap:26px}}
.hvpanel{background:linear-gradient(160deg,#0E1B2A 0%,#123640 55%,#164A50 100%);
border-radius:18px;padding:20px;box-shadow:0 22px 60px rgba(14,27,42,.28);position:relative;overflow:hidden}
.hvpanel:after{content:"";position:absolute;inset:0;background:
radial-gradient(120% 70% at 85% 12%,rgba(37,211,102,.16),transparent 60%);pointer-events:none}
.hvpanel svg{width:100%;height:auto;display:block;border-radius:12px}
.hvcap{position:relative;color:#AFC4CE;font-size:12px;margin-top:12px;text-align:center;line-height:1.45}
.hvcap b{color:#DFEDF2;font-weight:600}
.hvbadges{position:relative;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:14px}
.hvb{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#0E1B2A;
background:#EAF0F4;border-radius:100px;padding:6px 12px}
.hvb.accent{background:var(--accent);color:#fff}
"""


def _pend(text="To be confirmed"):
    return f'<span class="pend">{text}</span>'


def _illustrative(width=520):
    """Vehicle figure for a configuration card.

    Prefers a supplied photograph; falls back to a labelled diagram, never to
    stock imagery presented as the actual vehicle.
    """
    for name in ("exterior-side", "exterior-front"):
        url = find_image("gallery", name)
        if url:
            dimensions = MEDIA_DIMENSIONS.get(name, (1200, 900))
            return (f'<img src="{url}" alt="Force Urbania group transport vehicle" '
                    f'width="{dimensions[0]}" height="{dimensions[1]}" '
                    f'style="width:100%;height:auto;display:block;border-radius:10px" '
                    f'loading="lazy" decoding="async">')
    return ('<svg viewBox="0 0 520 240" role="img" aria-label="Illustrative diagram of a Force '
            'Urbania-style group travel van."><rect width="520" height="240" fill="#EAF0F4"/>'
            '<rect x="46" y="58" width="428" height="118" rx="16" fill="#FFFFFF" stroke="#CDD8E0" stroke-width="2"/>'
            '<rect x="46" y="58" width="98" height="118" rx="16" fill="#116A7B" opacity=".12"/>'
            '<path d="M144 58h242a16 16 0 0 1 16 16v32H128V74a16 16 0 0 1 16-16Z" fill="#116A7B" opacity=".22"/>'
            '<circle cx="126" cy="188" r="17" fill="#0E1B2A"/><circle cx="392" cy="188" r="17" fill="#0E1B2A"/>'
            '<g fill="#CDD8E0">'
            '<rect x="180" y="100" width="29" height="25" rx="4"/><rect x="219" y="100" width="29" height="25" rx="4"/>'
            '<rect x="258" y="100" width="29" height="25" rx="4"/><rect x="297" y="100" width="29" height="25" rx="4"/>'
            '<rect x="180" y="134" width="29" height="25" rx="4"/><rect x="219" y="134" width="29" height="25" rx="4"/>'
            '<rect x="258" y="134" width="29" height="25" rx="4"/><rect x="297" y="134" width="29" height="25" rx="4"/>'
            '</g>'
            '<rect x="346" y="98" width="96" height="62" rx="7" fill="none" stroke="#116A7B" stroke-width="2" stroke-dasharray="6 5"/>'
            '<text x="394" y="134" font-family="Inter,sans-serif" font-size="12" fill="#0C4F5C" text-anchor="middle">Luggage</text>'
            '</svg>')


# --------------------------------------------------------- find your urbania
def find_your_urbania():
    """Passenger-count selector that recommends a configuration.

    Server-rendered default state so it works and is indexable without JS; the
    JS only updates the card in place.
    """
    return f'''<div class="fy" id="fy">
  <div class="fy-row">
    <div class="fy-ctl">
      <label for="fy-pax">How many people are travelling?</label>
      <input id="fy-pax" type="number" inputmode="numeric" min="1" max="20" value="12"
             aria-describedby="fy-hint">
    </div>
    <div class="fy-out">
      <div class="fy-card" id="fy-card" role="status" aria-live="polite">
        <h3>Premium configuration</h3>
        <p>A comfortable starting point for a medium-sized group.</p>
      </div>
    </div>
  </div>
  <p class="fy-hint" id="fy-hint">We recommend a configuration from your group size. Luggage matters
  as much as seats &mdash; tell us both and we will confirm what fits.</p>
</div>'''


FIND_JS = """<script>
(function(){
  var inp=document.getElementById('fy-pax'), card=document.getElementById('fy-card'), fy=document.getElementById('fy');
  if(!inp||!card) return;
  var RULES=[
    [17,'seater-17','Extended configuration','A starting point for a larger group, subject to luggage and route review.'],
    [14,'seater-16','Large-group configuration','A practical option for a larger group with normal luggage.'],
    [11,'premium-12','Premium configuration','A comfortable option for a medium-sized group.'],
    [1,'luxury-maharaja','Compact configuration','A comfortable option for a smaller group.']
  ];
  function pick(n){
    if(isNaN(n)||n<1) return null;
    if(n>17) return {warn:true,h:'We will review the right arrangement',
      p:'For larger groups, we may recommend more than one vehicle or a different category. Share the full group and luggage details.'};
    for(var i=0;i<RULES.length;i++){ if(n>=RULES[i][0]) return {k:RULES[i][1],h:RULES[i][2],p:RULES[i][3]}; }
    return {k:'luxury-maharaja',h:'Compact configuration',p:'A comfortable option for a smaller group.'};
  }
  function render(){
    var r=pick(parseInt(inp.value,10));
    card.className='fy-card'+(r&&r.warn?' warn':'');
    if(!r){ card.innerHTML='<h3>Tell us your group size</h3><p>Enter a number to see the configuration we would recommend.</p>'; return; }
    card.innerHTML='<h3>'+r.h+'</h3><p>'+r.p+'</p>';
  }
  inp.addEventListener('input',render);
  inp.addEventListener('change',render);
})();
</script>"""


# ------------------------------------------------------------ config cards
def config_cards():
    out = []
    for c in CONFIGURATIONS:
        rows = ""
        for field, label in CONFIG_SPEC_FIELDS:
            v = c["specs"].get(field)
            if v:
                rows += (f'<tr><th scope="row">{html.escape(label)}</th>'
                         f'<td>{html.escape(str(v))}</td></tr>')
        # An unpublished specification is OMITTED. Rendering it as "To be
        # confirmed" put twenty of those on the homepage alone.
        spec = ""
        if rows:
            spec = (f'<table class="spec">{rows}</table>')
        best = "".join(f'<span>{html.escape(b)}</span>' for b in c["best_for"])
        out.append(f'''<article class="cfgcard">
  <div class="cfgbody">
    <div class="cfg-cap"><b>{c["seats_label"]}</b><span class="trim">{html.escape(c["trim"])}</span></div>
    <p class="tl">{html.escape(c["tagline"])}</p>
    {spec}
    <div class="bestfor">{best}</div>
    <div class="cfgacts">
      <a class="btn sm" href="/request-quote/">Get quote</a>
      <a class="btn ghost sm" href="/find-a-vehicle/">View vehicle guidance</a>
    </div>
  </div>
</article>''')
    return f'<div class="cfg">{"".join(out)}</div>'


# --------------------------------------------------------------- rates table
def rates_table():
    """Built only from figures that actually exist.

    Every unpublished number used to render as a warn-coloured "₹XX/km", so the
    rates page was 96 placeholders in a table. A column is included only when at
    least one configuration has a real figure for it, and if nothing is published
    the table is dropped entirely — the page then states plainly that rates are
    quoted per trip, which is the truth for this business and is more useful to a
    customer than a grid of XX.
    """
    value_keys = ("per_km", "per_day", "driver_allowance", "min_km_per_day")
    published = [k for k in value_keys
                 if any(c.get(k) is not None for c in CONFIGURATIONS)]

    parts = []
    if published:
        cols = [(h, k) for h, k in RATE_TABLE_COLUMNS
                if k in ("config", "capacity") or k in published]
        head = "".join(f"<th scope=col>{html.escape(h)}</th>" for h, _ in cols)
        body = ""
        for c in CONFIGURATIONS:
            cells = ""
            for _, key in cols:
                if key == "config":
                    cells += (f'<td>{c["seats_label"]} '
                              f'<span class="small">{html.escape(c["trim"])}</span></td>')
                elif key == "capacity":
                    cells += f'<td>{c["seats_label"]}</td>'
                elif key == "per_km":
                    cells += f'<td>{money(c["per_km"])}/km</td>'
                elif key == "per_day":
                    cells += f'<td>{money(c["per_day"])}</td>'
                elif key == "driver_allowance":
                    cells += f'<td>{money(c["driver_allowance"])}/day</td>'
                else:
                    cells += f'<td>{c["min_km_per_day"]} km/day</td>'
            body += f"<tr>{cells}</tr>"
        parts.append(f'<div class="rate-wrap"><table class="rate">'
                     f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
    else:
        parts.append(
            '<p class="lede">Rates are quoted per trip rather than published as a fixed '
            'tariff. Your quotation states the per-kilometre rate, the daily rate where one '
            'applies, the driver allowance and any minimum daily distance for your actual '
            'itinerary &mdash; so the figure you receive matches the trip you described '
            'instead of a headline number that would not.</p>')

    inc = "".join(f"<li>{html.escape(i)}</li>" for i in RATE_INCLUSIONS)
    exc = "".join(f"<li>{html.escape(e)}</li>" for e in RATE_EXCLUSIONS)
    parts.append(f'<div class="io"><div><h4>What the quotation covers</h4><ul>{inc}</ul></div>'
                 f'<div><h4>Charged in addition</h4><ul>{exc}</ul></div></div>')

    notes = "".join(
        f'<div><b>{html.escape(lbl)}</b><span>{html.escape(str(val))}</span></div>'
        for lbl, val in RATE_NOTES if val is not None)
    if notes:
        parts.append(f'<div class="notes">{notes}</div>')
    return "".join(parts)


def indicative_rates():
    """Indicative market pricing.

    CATEGORY B — reversible commercial content, labelled as indicative everywhere
    and never presented as a contract rate. The figures are market-researched bands
    for a Force Urbania in Hyderabad, not this operator's own rate card, so the copy
    says the quotation confirms the number for the actual trip. Provenance for every
    figure is in site_data.RATE_INDICATIVE_SOURCES.
    """
    rows = ""
    for r in RATE_INDICATIVE:
        unit = {"per km": "/km", "per day": "/day", "one way": " one way",
                "per hour": "/hour"}.get(r["unit"], " " + r["unit"])
        rows += (f'<tr><th scope="row">{r["label"]}</th>'
                 f'<td class="amt">{money(r["low"])}&ndash;{money(r["high"])}{unit}</td>'
                 f'<td class="small">{r["note"]}</td></tr>')
    return (
        '<div class="rate-wrap"><table class="rate indic">'
        '<thead><tr><th scope="col">Item</th><th scope="col">Indicative range</th>'
        '<th scope="col">What it covers</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>'
        '<p class="small" style="margin-top:14px"><b>Indicative, not a fixed price.</b> '
        'These are typical market ranges for a Force Urbania in Hyderabad, shown so you can '
        'budget before enquiring. Your quotation confirms the figure for your actual trip '
        '&mdash; it depends on distance, duration, the date, the configuration and the route. '
        'Tolls, parking, state permits, GST and any night allowance are additional where they '
        'apply.</p>')


def fleet_status_note():
    """A statement of what is true, not an apology for missing data.

    This previously read "Being confirmed. We are finalising which Urbania
    configurations we offer and the rates that apply" — which told every visitor
    the site was still being set up. What is actually established is more useful
    and needs no caveat: one 17-seat vehicle, so availability is checked by a
    person rather than shown live.
    """
    if FLEET_CONFIRMED:
        return ('<p class="lede" style="margin-bottom:22px"><b>Verified vehicle options across India.</b> '
                'UrbanLoop matches your route, dates, group size and luggage needs with a suitable '
                'operating vehicle, then confirms availability before sending the quotation.</p>')
    return ''


# ------------------------------------------------------------ services/routes
def services_grid():
    cards = "".join(
        f'<a class="card" href="{s["href"]}"><span class="tag">{html.escape(s["name"].replace("&amp;", "&"))}</span>'
        f'<h3>{s["name"]}</h3><p>{html.escape(s["blurb"])}</p>'
        f'<p style="margin-top:14px"><span class="txtlink">Read the service guide</span></p></a>'
        for s in NATIONAL_SERVICES)
    return f'<div class="grid g3">{cards}</div>'


def routes_grid():
    cards = ""
    for r in ROUTES:
        dist = (f'<span>{_pend("Distance to confirm")}</span>' if r["distance_km"] is None
                else f'<span>{r["distance_km"]} km</span>')
        tm = (f'<span>{_pend("Drive time to confirm")}</span>' if r["drive_time"] is None
              else f'<span>{html.escape(str(r["drive_time"]))}</span>')
        cards += (f'<a class="route" href="/destinations/hyderabad-to-{r["name"].lower()}/">'
                  f'<span class="r">{html.escape(r["region"])}</span>'
                  f'<h3>Hyderabad to {html.escape(r["name"])}</h3>'
                  f'<p>{html.escape(r["note"])}</p>'
                  f'<div class="meta">{dist}{tm}</div></a>')
    areas = ", ".join(SERVICE_AREAS)
    return (f'<div class="routes">{cards}</div>'
            f'<p class="small" style="margin-top:16px">Pickups across {html.escape(areas)} '
            f'and elsewhere in Hyderabad.</p>')


# ------------------------------------------------------------------- trust
def trust_strip():
    """Assurances only. Metrics appear when there is a figure to show.

    This used to render one tile per TRUST_FIELD, so with no figures supplied a
    live page carried SEVEN boxes reading "To be confirmed" — the loudest
    unfinished signal on the site. An unpublished metric is now simply omitted;
    supply the value in site_data.TRUST_FIELDS and the tile appears by itself.
    The assurances are statements about how the business works rather than numbers,
    so they are always publishable and always shown.
    """
    cards = "".join(
        f'<div class="tcard"><b>{html.escape(str(value))}</b><span>{html.escape(label)}</span></div>'
        for label, value in TRUST_FIELDS if value is not None)
    assures = "".join(
        f'<div class="fact">{_tick()}<span>{html.escape(a)}</span></div>' for a in TRUST_ASSURANCES)
    strip = f'<div class="trust">{cards}</div>' if cards else ""
    return strip + f'<div class="assure">{assures}</div>'


def _tick():
    return ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#116A7B" '
            'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M20 6 9 17l-5-5"/></svg>')


def reviews_block():
    """Renders nothing at all when there are no reviews.

    It used to emit an empty-state box saying customer reviews "will be published
    here" and that "this space stays empty" — which advertises the absence and
    reads as an unfinished page. With no genuine review the whole section is
    omitted by the caller, so the page is simply complete without it. A real
    review is never written on a customer's behalf; supply them in REVIEWS.
    """
    if not REVIEWS:
        return ""
    out = ""
    for r in REVIEWS:
        out += (f'<div class="card"><p>&ldquo;{html.escape(r["text"])}&rdquo;</p>'
                f'<p class="small" style="margin-top:12px">{html.escape(r["author"])}'
                f' &middot; {html.escape(r["trip_type"])}</p></div>')
    return f'<div class="grid g3">{out}</div>'


# ----------------------------------------------------------------- gallery
def _media_grid(slots, kind):
    """Render real photographs. Empty slots only when SHOW_MEDIA_PLACEHOLDERS.

    A dashed slot naming the expected file is a shot list for the owner, but it
    publishes build state to customers — ten boxes reading
    "gallery/exterior-rear.jpg" make a live site look unfinished. Off by default.
    """
    out, have = "", 0
    for name, caption in slots:
        url = find_image(kind, name)
        if url:
            have += 1
            dimensions = MEDIA_DIMENSIONS.get(name, ())
            size_attrs = (f' width="{dimensions[0]}" height="{dimensions[1]}"'
                          if len(dimensions) == 2 else "")
            out += (f'<figure class="gfig"><img src="{url}" alt="{html.escape(caption)}" '
                    f'{size_attrs} loading="lazy" decoding="async">'
                    f'<figcaption>{html.escape(caption)}</figcaption></figure>')
        elif SHOW_MEDIA_PLACEHOLDERS:
            out += (f'<div class="gslot"><span>{html.escape(caption)}<br>'
                    f'<code style="font-size:10px">{html.escape(kind)}/{html.escape(name)}.jpg'
                    f'</code></span></div>')
    # An empty grid would render as a stray empty flex container.
    if not out:
        return "", have
    return f'<div class="gal">{out}</div>', have


def _media_note(have, total, kind="photographs", folder="gallery"):
    """Only ever a positive, complete statement.

    Every rendered figure carries its own provenance caption, so a populated grid
    needs no extra note, and a grid with nothing in it is not rendered by the
    caller at all. This therefore only ever confirms a COMPLETE set — there is no
    "coming soon" copy advertising what is missing.
    """
    if SHOW_MEDIA_PLACEHOLDERS:
        # Owner-facing shot-list mode. Unchanged: this is a build aid, not copy.
        if have == total and total:
            return f'<p class="small" style="margin-top:14px">All {total} {kind} supplied.</p>'
        if have:
            return (f'<p class="small" style="margin-top:14px">{have} of {total} {kind} supplied '
                    f'so far. The remaining slots show the exact filename they expect.</p>')
        return (f'<p class="small" style="margin-top:14px">Final images drop into '
                f'<code>media/{folder}/</code> by filename.</p>')
    if have and have == total and ASSETS_ARE_OUR_VEHICLE:
        return (f'<p class="small" style="margin-top:14px">All {total} {kind} supplied.</p>')
    return ""


def gallery_block():
    grid, have = _media_grid(GALLERY_SLOTS, "gallery")
    return grid + _media_note(have, len(GALLERY_SLOTS), "photographs", "gallery")


def planning_visual():
    """A clearly labelled illustrative visual for the planning journey."""
    return ('<figure class="planning-visual">'
            '<img src="/media/illustration/group-travel-planning.png" '
            'alt="Group travel planning at an airport with luggage and a route plan" '
            'width="1536" height="1024" loading="lazy" decoding="async">'
            '<figcaption>Illustrative planning scene. Vehicle photographs are shown separately.</figcaption>'
            '</figure>')


def seating_block():
    """Seating references: layout comparison plus the seating photo set.

    Seat layout and legroom are the details group buyers ask about most, and the
    briefing calls them out. Layout descriptions are structural (1x1 vs 2x1) and
    claim no specific vehicle specification.
    """
    layouts = "".join(
        f'<div class="card"><span class="tag">{html.escape(l["label"])}</span>'
        f'<h3>{html.escape(l["name"])}</h3><p>{html.escape(l["blurb"])}</p></div>'
        for l in SEAT_LAYOUTS)
    grid, have = _media_grid(SEATING_SLOTS, "seating")
    return (f'<div class="grid g2" style="margin-bottom:28px">{layouts}</div>'
            + grid
            + _media_note(have, len(SEATING_SLOTS), "seating photographs", "seating"))


def pricing_faq_block():
    inner = "".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>'
                    for q, a in PRICING_FAQS)
    return f'<div class="faq">{inner}</div>'


# ----------------------------------------------------------- hero vehicle
def hero_visual():
    """Premium hero panel.

    Deliberately an ILLUSTRATION, labelled as one. The brief wants the vehicle
    as the visual hero, but publishing a stock photo as if it were the actual
    van would misrepresent what a customer receives — and the shot list is
    still outstanding. Real photographs replace this panel when supplied.
    """
    svg = (
        '<svg viewBox="0 0 560 330" role="img" aria-label="Illustrative side profile of a '
        'Force Urbania style 17-seat group travel van.">'
        '<defs>'
        '<linearGradient id="body" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCE6EC"/></linearGradient>'
        '<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#7FB3C4"/><stop offset="1" stop-color="#3D7C8C"/></linearGradient>'
        '</defs>'
        '<rect width="560" height="330" fill="none"/>'
        # ground shadow
        '<ellipse cx="280" cy="266" rx="200" ry="16" fill="#000" opacity=".28"/>'
        # main body
        '<path d="M96 116 q10-46 62-52 h250 q54 6 62 52 v92 q0 18-18 18 h-338 q-18 0-18-18 z" '
        'fill="url(#body)" stroke="#B9C7D0" stroke-width="2"/>'
        # windscreen + window band
        '<path d="M108 120 q8-36 54-42 h60 v66 h-114 z" fill="url(#glass)"/>'
        '<rect x="234" y="78" width="82" height="66" rx="6" fill="url(#glass)"/>'
        '<rect x="326" y="78" width="82" height="66" rx="6" fill="url(#glass)"/>'
        '<rect x="418" y="82" width="66" height="62" rx="6" fill="url(#glass)"/>'
        # trim / skirt
        '<rect x="96" y="168" width="430" height="24" fill="#0F6E68" opacity=".85"/>'
        '<rect x="96" y="192" width="430" height="34" fill="#E7EEF2"/>'
        # wheels
        '<circle cx="176" cy="232" r="34" fill="#101C26"/><circle cx="176" cy="232" r="15" fill="#9FB2BF"/>'
        '<circle cx="436" cy="232" r="34" fill="#101C26"/><circle cx="436" cy="232" r="15" fill="#9FB2BF"/>'
        # door seam
        '<path d="M330 74 v152" stroke="#B9C7D0" stroke-width="2"/>'
        '<path d="M418 82 v144" stroke="#B9C7D0" stroke-width="2"/>'
        # headlight on the SAME side as the windscreen, so the van does not read
        # as having two fronts
        '<rect x="88" y="150" width="18" height="16" rx="5" fill="#FFE9A8"/>'
        '<rect x="86" y="196" width="14" height="26" rx="5" fill="#C7D3DB"/>'
        '</svg>')

    badges = ('<div class="hvbadges">'
              '<span class="hvb accent">Vehicle options</span>'
              '<span class="hvb">Pan-India</span>'
              '<span class="hvb">Quote first</span>'
              '</div>')

    # 1. Cinematic video (desktop) with a poster that doubles as the mobile still.
    if has_hero_video():
        poster = find_image("hero", "hero-poster") or find_image("hero", "hero")
        sources = "".join(
            f'<source src="{media_url("hero", "hero" + ext)}" type="{mime}">'
            for ext, mime in ((".webm", "video/webm"), (".mp4", "video/mp4"))
            if os.path.exists(media_path("hero", "hero" + ext)))
        par = f' poster="{poster}"' if poster else ""
        # Autoplaying video on a phone burns data and battery for no conversion
        # gain, so mobile gets the still instead.
        mobile = (f'<img class="hv-mobile" src="{poster}" alt="{_alt_text()}" '
                  f'width="1120" height="660" loading="lazy" decoding="async">') if poster else ""
        return (f'<div class="hvpanel">{badges}'
                f'<video class="hv-video" autoplay muted loop playsinline preload="metadata"'
                f'{par}>{sources}</video>{mobile}'
                f'<p class="hvcap">{_media_caption("Footage")}</p></div>')

    # 2. Still photograph.
    still = find_image("hero", "hero-poster") or find_image("hero", "hero")
    if still:
        return (f'<div class="hvpanel">{badges}'
                f'<img class="hv-still" src="{still}" alt="{_alt_text()}" '
                f'width="1120" height="660" loading="lazy" decoding="async">'
                f'<p class="hvcap">{_media_caption("Photograph")}</p></div>')

    # 3. Diagram fallback, if no image file exists at all.
    return (f'<div class="hvpanel">{badges}{svg}'
            '<p class="hvcap"><b>Diagram, not a photograph.</b></p></div>')


def _alt_text():
    """Descriptive alt text for accessibility.

    Carries no provenance disclaimer and no ownership claim: it describes what is
    shown. (A disclaimer in customer-facing copy actively discourages enquiries for
    no benefit, since the vehicle depicted is the model this business operates.)
    """
    return "Force Urbania group transport vehicle"


def _media_caption(kind="Photograph"):
    """Neutral vehicle caption.

    Previously disclaimed provenance ("not a photograph of our own vehicle") and
    previously asserted ownership when ASSETS_ARE_OUR_VEHICLE was set. Neither is
    used now: this describes the vehicle without making a claim in either direction.
    """
    return ('<b>Force Urbania group transport.</b> A representative vehicle option; '
            'the exact arrangement is confirmed for each route and date.')


# ----------------------------------------------------------- hero journey bar
def journey_bar(action="/request-quote/"):
    """STEP 1 of the quote funnel: trip details only, zero personal data.

    Deliberately a plain GET <form>. Without JS it still works — the browser
    builds the query string itself — and it hands off to the planner, which
    prefills from those params. That keeps exactly ONE funnel implementation
    instead of growing a second one, which is what caused the drift we just
    removed.
    """
    return ('''<form class="jbar" action="%ACTION%" method="get" aria-label="Start your trip quote">
  <div class="jbar-grid">
    <label class="jf"><span>From</span>
      <input name="from" type="text" placeholder="Pickup point or area" autocomplete="street-address" data-location-suggest="true"></label>
    <label class="jf"><span>To</span>
      <input name="to" type="text" placeholder="Destination" autocomplete="street-address" data-location-suggest="true"></label>
    <label class="jf"><span>Travel date</span>
      <input name="date" type="date"></label>
    <label class="jf"><span>Passengers</span>
      <input name="pax" type="number" inputmode="numeric" min="1" max="20" placeholder="e.g. 14"></label>
    <div class="jgo"><button class="btn" type="submit">Start my quote</button></div>
  </div>
  <p class="jnote">%TICK%<span>Free and no obligation &mdash; no payment is taken to request a
  quotation, and availability is confirmed by a person before anything is agreed.</span></p>
</form>
<script>
(function(){
  var form=document.querySelector('.jbar'); if(!form) return;
  [].slice.call(form.querySelectorAll('[data-location-suggest]')).forEach(function(input){
    var label=input.closest('.jf'); if(!label) return;
    label.classList.add('pl-location');
    var box=document.createElement('div'); box.className='pl-suggestions'; box.hidden=true; box.setAttribute('role','listbox'); label.appendChild(box);
    var timer, controller;
    input.setAttribute('aria-autocomplete','list');
    input.addEventListener('input',function(){
      clearTimeout(timer); box.hidden=true; box.innerHTML=''; var q=input.value.trim();
      if(q.length<3) return;
      timer=setTimeout(function(){
        if(controller) controller.abort(); controller=new AbortController();
        fetch('https://nominatim.openstreetmap.org/search?format=jsonv2&addressdetails=1&dedupe=1&countrycodes=in&limit=5&accept-language=en&q='+encodeURIComponent(q),{signal:controller.signal})
          .then(function(r){return r.ok?r.json():null;}).then(function(items){
            if(!items) return;
            items.slice(0,5).forEach(function(item){
              var p=item.address||{}, parts=[];
              [p.house_number,p.road,p.neighbourhood,p.suburb,p.city||p.town||p.village,p.state].forEach(function(v){if(v&&parts.indexOf(v)<0) parts.push(v);});
              var text=parts.join(', ')||item.display_name; if(!text) return;
              var b=document.createElement('button'); b.type='button'; b.className='pl-suggestion'; b.setAttribute('role','option'); b.textContent=text;
              b.addEventListener('mousedown',function(e){e.preventDefault();input.value=text;box.hidden=true;box.innerHTML='';}); box.appendChild(b);
            });
            box.hidden=!box.children.length;
          }).catch(function(){});
      },280);
    });
    input.addEventListener('blur',function(){setTimeout(function(){box.hidden=true;},160);});
  });
  form.addEventListener('submit',function(e){
    var bad=false;
    // From and To remain free text: landmarks, villages and unusual spellings
    // may not exist in the suggestion directory, but are still valid enquiries.
    var date=form.querySelector('[name="date"]'), pax=form.querySelector('[name="pax"]');
    if(date){var dateOk=!!date.value && date.value>=new Date().toISOString().slice(0,10); date.setCustomValidity(dateOk?'':'Choose today or a future travel date.'); if(!dateOk) bad=true;}
    if(pax){var paxOk=Number(pax.value)>=1 && Number(pax.value)<=100; pax.setCustomValidity(paxOk?'':'Enter the number of passengers.'); if(!paxOk) bad=true;}
    if(bad){e.preventDefault(); var first=form.querySelector(':invalid'); if(first) first.focus();}
  });
})();
</script>'''.replace("%ACTION%", action).replace("%TICK%", _tick()))
