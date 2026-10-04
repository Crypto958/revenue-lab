#!/usr/bin/env python3
"""
Urbania group transport — design system + layout primitives.
Working name only: the final business name is an OWNER DECISION (see docs/OWNER_DECISIONS.md).

Every fact that is not owner-supplied or independently verified is either omitted from
visible copy or carries an inline  <!-- [VERIFY BEFORE PUBLISHING: ...] -->  marker.
Visible copy positions UrbanLoop as a pan-India, quote-first group-transport aggregator.
"""
import os, json, html, datetime

# ------------------------------------------------------------------ config
BASE = "https://urbanloop.co"                    # canonical production domain
BRAND = "UrbanLoop"                             # LOCKED — never alter, abbreviate or respell
TAGLINE = "Premium Group Mobility"              # the descriptor; used with the mark, not instead of it
BRAND_LINE = "Move Together, Better."           # working brand line — not yet published in the header
PHONE = "+91 91821 26104"                       # owner-supplied customer-care number
# Derived, never typed. Numeric strings are masked as **** in tool output, so a
# hand-copied href silently corrupts the dial link on every page. Digits only.
PHONE_HREF = "tel:+" + "".join(ch for ch in PHONE if ch.isdigit())
PHONE_TXT = "+91&nbsp;91821&nbsp;26104"          # display form: never wraps mid-number on mobile
WHATSAPP = "919182126104"                        # owner-supplied via WhatsApp Business profile
EMAIL = ""                                       # [VERIFY BEFORE PUBLISHING: enquiry email]
CITY = "Hyderabad"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "site")
TODAY = datetime.date.today().isoformat()
YEAR = datetime.date.today().year

# ------------------------------------------------------------- brand assets
# The master marks live in one place — brand/logo/ at the repo root — and are
# inlined at build time, so the built HTML carries no font or file dependency and
# no second copy of the artwork can drift. Colours are rewritten to currentColor
# so one file works on light AND dark surfaces.
BRAND_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "brand", "logo"))


def brand_svg(filename, cls="", label=""):
    """Inline a master mark from brand/logo/.

    Deliberately raises instead of falling back: this is the brand mark in the
    header of every page. A silent placeholder here is how the site ended up
    branded "Urbania Hyderabad" with a "17" tile for months while the real
    identity sat unused in brand/logo/.
    """
    path = os.path.join(BRAND_DIR, filename)
    if not os.path.exists(path):
        raise SystemExit(
            f"\nBRAND ASSET MISSING: {path}\n"
            f"  Every page header depends on it. Rebuild the identity with:\n"
            f"      python3 brand/build_wordmark.py && python3 brand/build_marks.py\n")
    with open(path, encoding="utf-8") as source:
        svg = source.read()
    for c in ("#111518", "#FFFFFF", "#0F6A63", "#FAFBFC"):
        svg = svg.replace(f'fill="{c}"', 'fill="currentColor"')
        svg = svg.replace(f'stroke="{c}"', 'stroke="currentColor"')
    if cls:
        svg = svg.replace("<svg ", f'<svg class="{cls}" ', 1)
    if label:
        svg = svg.replace('aria-label="UrbanLoop"', f'aria-label="{html.escape(label)}"', 1)
    else:
        svg = svg.replace('role="img"', 'role="img" aria-hidden="true"', 1)
    return svg

NAV = [
    ("Home", "/"),
    ("How it works", "/how-it-works/"),
    ("Vehicle options", "/find-a-vehicle/"),
    ("Use cases", "/india/"),
    ("Routes", "/india/"),
    ("Guides", "/guides/"),
]

# ------------------------------------------------------------------ CSS
CSS = """
:root{
--ink:#131A24; --ink-2:#4A5560; --ink-3:#626E7A;
--bg:#FFFFFF; --alt:#F5F7F7; --alt-2:#EAF0F4;
--line:#E2E8E8; --line-2:#C9D3D3;
--accent:#0F6E68; --accent-2:#0A514C; --accent-soft:#E7F1F0;
--warn:#8A5A0B; --warn-bg:#FFF7E6; --warn-line:#F0DFA8;
--sans:system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,monospace;
--r:10px; --r-lg:16px;
--sh:0 1px 2px rgba(14,27,42,.05),0 10px 30px rgba(14,27,42,.07);
--wrap:1180px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.62;
-webkit-font-smoothing:antialiased;text-wrap:pretty;overflow-x:hidden}
img,svg,video{max-width:100%;display:block}
a{color:inherit}
p{margin:0}
h1,h2,h3,h4{margin:0;font-weight:650;letter-spacing:-.022em;line-height:1.14}
h1{font-size:clamp(34px,5vw,58px);line-height:1.06}
h2{font-size:clamp(26px,3.2vw,38px)}
h3{font-size:clamp(18px,1.7vw,21px);line-height:1.25}
h4{font-size:16px}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 24px}
@media(max-width:640px){.wrap{padding:0 18px}}
.eyebrow{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:500}
.lede{font-size:clamp(17px,1.7vw,20px);color:var(--ink-2);max-width:64ch;line-height:1.6}
.small{font-size:14px;color:var(--ink-3)}
.muted{color:var(--ink-3)}
section{padding:clamp(48px,6vw,86px) 0}
section.alt{background:var(--alt);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.shead{max-width:72ch;margin-bottom:38px}
.shead h2{margin-top:12px}
.shead .lede{margin-top:14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;background:var(--accent);color:#fff;
text-decoration:none;padding:15px 26px;border-radius:var(--r);font-size:16px;font-weight:600;border:1px solid transparent;
transition:background .16s,transform .16s,box-shadow .16s;box-shadow:0 6px 18px rgba(17,106,123,.22);cursor:pointer}
.btn:hover{background:var(--accent-2);transform:translateY(-1px)}
.btn.ghost{background:#fff;color:var(--ink);border-color:var(--line-2);box-shadow:none}
.btn.ghost:hover{background:var(--alt);transform:none}
.btn.sm{padding:11px 18px;font-size:15px}
.btn.wide{width:100%}
.txtlink{color:var(--accent);text-decoration:none;font-weight:600;font-size:15.5px;border-bottom:1px solid rgba(17,106,123,.3)}
.txtlink:hover{border-color:var(--accent)}
:focus-visible{outline:3px solid var(--accent-2);outline-offset:3px;border-radius:4px}
.skip-link{position:fixed;left:12px;top:12px;z-index:1000;background:#fff;color:var(--ink);padding:10px 14px;
border:2px solid var(--accent-2);border-radius:6px;transform:translateY(-160%);text-decoration:none;font-weight:700}
.skip-link:focus{transform:none}
/* header */
header{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:18px;height:72px}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.logo{display:flex;align-items:center;text-decoration:none;color:var(--ink)}
.wordmark{font-size:20px;letter-spacing:-.035em;font-weight:700;color:inherit}
@media(max-width:640px){.wordmark{font-size:19px}}
nav.main{display:flex;gap:24px;align-items:center}
nav.main a{font-size:15px;color:var(--ink-2);text-decoration:none;font-weight:500}
nav.main a:hover,nav.main a[aria-current]{color:var(--accent)}
.hact{display:flex;align-items:center;gap:12px}
.calllink{display:inline-flex;align-items:center;gap:7px;font-size:15px;font-weight:600;color:var(--ink);text-decoration:none;white-space:nowrap}
.burger{display:none;background:#fff;border:1px solid var(--line-2);border-radius:8px;padding:9px 11px;cursor:pointer}
.burger span{display:block;width:18px;height:2px;background:var(--ink);margin:4px 0}
#mnav{display:none;background:#fff;border-top:1px solid var(--line)}
#mnav.open{display:block}
#mnav a{display:block;padding:15px 24px;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink-2);font-weight:500}
#mnav .mcta{padding:16px 24px;display:grid;gap:10px}
@media(max-width:1040px){nav.main{display:none}.burger{display:block}}
@media(max-width:640px){.hact .btn{display:none}.calllink{font-size:14px}.bar{height:64px}}
/* hero */
.hero{padding:clamp(40px,5vw,68px) 0 clamp(40px,5vw,64px);background:linear-gradient(180deg,#FAFCFD,#FFFFFF)}
@media(max-width:560px){
  .hero{padding:24px 0 20px}
  .hero h1{font-size:30px;line-height:1.1}
  .hero .lede{margin-top:12px !important;font-size:16.5px !important}
  .heroacts{margin-top:16px}
  .hero .small{font-size:12.5px;margin-top:10px !important}
  section{padding:34px 0}
}
.hgrid{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center}
@media(max-width:940px){.hgrid{grid-template-columns:1fr;gap:32px}}
.hero h1{margin-top:16px}
.hero .lede{margin-top:20px;font-size:clamp(17px,1.8vw,20px)}
.heroacts{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.facts{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:26px}
.fact{display:flex;gap:10px;align-items:flex-start;font-size:14.5px;color:var(--ink-2)}
.fact svg{flex:none;margin-top:3px}
.vwrap{background:var(--alt);border:1px solid var(--line);border-radius:var(--r-lg);padding:14px}
.vcap{font-size:12.5px;color:var(--ink-3);margin-top:10px;text-align:center}
/* ---- hero cloned from the reference: full-bleed image, centred headline,
        floating quote bar overlapping the bottom edge ---- */
.hx{position:relative;background:#101820}
.hx-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 45%;z-index:0}
.hx-scrim{position:absolute;inset:0;z-index:1;pointer-events:none;
background:linear-gradient(180deg,rgba(11,16,21,.58) 0%,rgba(11,16,21,.28) 38%,rgba(11,16,21,.70) 100%)}
/* A radial pool of shade directly behind the copy keeps the headline contrast
   high without darkening the whole photograph — a flat scrim over a dusk shot
   goes muddy. It also has to suppress the vehicle's OWN liveried wordmark, which
   otherwise sits right behind the body copy and competes with the real one. */
.hx-in::before{content:"";position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);
width:min(1360px,100%);height:80%;z-index:-1;pointer-events:none;
background:radial-gradient(closest-side,rgba(8,12,16,.88) 0%,rgba(8,12,16,.66) 36%,
rgba(8,12,16,.24) 68%,rgba(8,12,16,0) 100%)}
/* NOTE: closest-side makes the ellipse reach 0 alpha exactly at the box edge, so no
   rectangular seam shows. Do NOT put overflow:hidden on .hx to contain this — the
   quote bar hangs below the hero with a negative margin and would be clipped. */
.hx-in{position:relative;z-index:2;max-width:1180px;margin:0 auto;
padding:clamp(52px,7vw,104px) 24px 26px;text-align:center;color:#fff}
.hx-in h1{color:#fff;font-size:clamp(31px,5.1vw,63px);letter-spacing:-.032em;line-height:1.03}
.hx-in h1 .l2{display:block;color:#7FCFC6}
.hx-in .lede{color:#D2DAE1;margin:20px auto 0;max-width:54ch}
.hx-mini{margin-top:14px;font-size:13px;color:#A3B2BD}
.hx-mini span+span::before{content:"·";margin:0 8px;color:#6C7C88}
.hx-cap{margin:14px auto 0;max-width:56ch;font-size:11.5px;line-height:1.5;color:#93A2AE}
.hx-cap b{color:#B9C6D0;font-weight:600}
.hx-line{margin-top:14px;font-size:clamp(15px,1.5vw,19px);font-weight:600;letter-spacing:.01em;color:#EFD9B4}
.hx-alt{margin-top:16px;font-size:15px;color:#C3CFD8}
.hx-alt a{color:#fff;font-weight:600;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4);padding-bottom:1px}
.hx-alt a:hover{border-bottom-color:#fff}
.hx-alt span{margin:0 10px;color:#7C8B96}
/* the floating quote bar */
.qwrap{position:relative;z-index:3;max-width:1180px;margin:34px auto -58px;padding:0 24px}
.qwrap .jbar{background:#fff;border:1px solid var(--line);border-radius:14px;
box-shadow:0 18px 44px rgba(12,22,32,.20);padding:14px;margin:0}
.qwrap .jbar-grid{display:grid;grid-template-columns:1.25fr 1.25fr 1fr .85fr auto;gap:0;align-items:stretch}
.qwrap .jf{display:flex;flex-direction:column;gap:4px;padding:8px 16px;border-right:1px solid var(--line);min-width:0}
.qwrap .jf:last-of-type{border-right:0}
.qwrap .jf span{font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-3)}
.qwrap .jf input{border:0;outline:0;background:transparent;font-family:inherit;font-size:15.5px;
color:var(--ink);padding:0;width:100%;min-width:0}
.qwrap .jf input::placeholder{color:#9AA7B0}
.qwrap .jbar button{background:var(--accent);color:#fff;border:0;border-radius:10px;
font-family:inherit;font-size:15.5px;font-weight:650;padding:0 26px;cursor:pointer;
display:inline-flex;align-items:center;gap:9px;white-space:nowrap;min-height:54px;align-self:stretch}
.qwrap .jbar button:hover{background:var(--accent-2)}
.hx-follow{padding-top:88px}
@media(max-width:900px){
  .qwrap .jbar-grid{grid-template-columns:1fr 1fr}
  .qwrap .jf{border-right:0;border-bottom:1px solid var(--line);padding:10px 14px}
  .qwrap .jbar button{grid-column:1/-1;min-height:50px;justify-content:center;margin-top:6px}
}
@media(max-width:640px){
  .hx-in{padding:34px 20px 22px}
  .hx-in h1{font-size:29px}
  .qwrap{margin:24px auto -34px;padding:0 16px}
  .qwrap .jbar-grid{grid-template-columns:1fr}
  .hx-follow{padding-top:60px}
}
/* ---- premium split hero (kept for deep pages) ---- */
.hsplit{display:grid;grid-template-columns:minmax(0,1.04fr) minmax(0,.96fr);background:#0E1316}
.hsplit .hcopy{color:#fff;display:flex;flex-direction:column;justify-content:center;
padding:clamp(40px,5.4vw,78px) clamp(24px,3vw,56px) clamp(40px,5.4vw,78px) max(24px,calc((100vw - 1180px)/2 + 24px))}
.hsplit .hcopy .eyebrow{color:#8FD3CB}
.hsplit .hcopy h1{color:#fff;font-size:clamp(31px,4.1vw,52px);letter-spacing:-.03em;line-height:1.05}
.hsplit .hcopy .lede{color:#B4C0C7;margin-top:18px;max-width:46ch}
.hsplit .hcopy .heroacts{margin-top:26px}
.hsplit .hcopy .btn.ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.32)}
.hsplit .hcopy .btn.ghost:hover{background:rgba(255,255,255,.1)}
.hsplit .hcopy .ucs{margin-top:24px}
.hsplit .hcopy .uc{border-color:rgba(255,255,255,.22);color:#C6D0D6;background:transparent}
.hsplit .hcopy .uc:hover{background:rgba(255,255,255,.1);color:#fff}
.hsplit .hshot{position:relative;min-height:min(76vh,640px);overflow:hidden}
.hsplit .hshot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:64% 50%}
.hsplit .hshot::after{content:"";position:absolute;inset:0;pointer-events:none;
background:linear-gradient(90deg,rgba(14,19,22,.80) 0%,rgba(14,19,22,.28) 22%,rgba(14,19,22,0) 46%)}
@media(max-width:900px){
  .hsplit{grid-template-columns:1fr}
  .hsplit .hshot{min-height:290px;order:-1}
  .hsplit .hshot::after{background:linear-gradient(180deg,rgba(14,19,22,0) 40%,rgba(14,19,22,.85) 100%)}
  .hsplit .hcopy{padding:30px 22px 38px}
  .hsplit .hcopy h1{font-size:29px}
}
/* cards */
.grid{display:grid;gap:18px}
.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr)}
@media(max-width:1000px){.g4{grid-template-columns:repeat(2,1fr)}}@media(max-width:900px){.g3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:720px){.g2,.g3,.g4{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;transition:border-color .16s,box-shadow .16s}
.card:hover{border-color:var(--line-2);box-shadow:var(--sh)}
.card h3{margin-bottom:8px}
.card p{color:var(--ink-2);font-size:15.5px}
.card ul{margin:14px 0 0;padding-left:20px}
.card li{font-size:15px;color:var(--ink-2);margin-bottom:6px}
a.card{text-decoration:none;display:block}
.tag{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
color:var(--accent);background:var(--accent-soft);padding:4px 9px;border-radius:100px;margin-bottom:12px}
/* steps */
.steps{counter-reset:s}
.stepc{display:grid;grid-template-columns:52px 1fr;gap:16px;padding:20px 0;border-top:1px solid var(--line)}
.stepc:last-child{border-bottom:1px solid var(--line)}
.stepc .n{font-family:var(--mono);font-size:13px;color:var(--accent);font-weight:500;padding-top:3px}
.stepc h3{margin-bottom:6px}
.stepc p{color:var(--ink-2);font-size:15.5px}
/* notice */
.notice{background:var(--warn-bg);border:1px solid var(--warn-line);border-radius:var(--r);padding:16px 18px;
font-size:14.5px;color:#5C4A12;display:flex;gap:11px;align-items:flex-start}
.notice b{color:#4A3A0A}
/* faq */
.faq details{border-top:1px solid var(--line);padding:2px 0}
.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;padding:18px 32px 18px 0;font-weight:600;font-size:17px;list-style:none;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:4px;top:16px;color:var(--accent);font-size:20px;font-weight:400}
.faq details[open] summary::after{content:"\\2013"}
.faq p{padding:0 0 20px;color:var(--ink-2);font-size:15.5px;max-width:78ch}
/* form */
.form{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:clamp(22px,3vw,34px)}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:640px){.frow{grid-template-columns:1fr}}
label{display:block;margin-bottom:16px}
label > span{display:block;font-size:14px;font-weight:600;color:var(--ink);margin-bottom:7px}
label .hint{font-weight:400;color:var(--ink-3);font-size:13px}
input,select,textarea{width:100%;background:#fff;border:1px solid var(--line-2);border-radius:var(--r);
padding:13px 14px;font-size:16px;font-family:inherit;color:var(--ink)}
input:focus,select:focus,textarea:focus{outline:0;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
textarea{min-height:96px;resize:vertical}
.fieldset{border:0;padding:0;margin:0 0 8px}
.fieldset legend{font-size:14px;font-weight:600;margin-bottom:8px;padding:0}
.radios{display:flex;flex-wrap:wrap;gap:8px}
.radios label{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line-2);border-radius:100px;
padding:9px 15px;margin:0;font-size:15px;cursor:pointer;color:var(--ink-2);background:#fff}
.radios input{width:auto;margin:0}
.submit-note{background:var(--accent-soft);border:1px solid #BFDCE2;border-radius:var(--r);padding:14px 16px;
font-size:14.5px;color:#0B4351;margin-top:20px}
.err{color:#B42318;font-size:13.5px;margin-top:6px;display:none}
label.bad input,label.bad select,label.bad textarea{border-color:#B42318}
label.bad .err{display:block}
/* footer */
footer{background:#131A24;color:#C7D3DD;padding:52px 0 34px;border-top:1px solid #1D2E3E}
.fgrid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr;gap:30px}
@media(max-width:860px){.fgrid{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.fgrid{grid-template-columns:1fr}}
footer h4{color:#fff;font-size:14px;letter-spacing:.03em;margin-bottom:14px}
.fgrid .fh{color:#fff;font-size:14px;letter-spacing:.03em;margin-bottom:14px;font-weight:650;line-height:1.3}
footer a{display:block;padding:5px 0;color:#C7D3DD;text-decoration:none;font-size:14.5px}
footer a:hover{color:#fff}
.fbot{margin-top:36px;padding-top:20px;border-top:1px solid #1D2E3E;font-size:13px;color:#8FA0AF;
display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
/* sticky mobile */
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:70;display:none;grid-template-columns:repeat(3,1fr);gap:1px;
background:var(--line);border-top:1px solid var(--line-2);padding-bottom:env(safe-area-inset-bottom)}
.sticky a{display:flex;align-items:center;justify-content:center;gap:8px;padding:15px 8px;text-decoration:none;
font-weight:650;font-size:14.5px;background:#fff;color:var(--ink);text-align:center}
.sticky a.q{background:var(--accent);color:#fff}
.sticky a.w{background:#25D366;color:#052E16}
@media(max-width:860px){.sticky{display:grid}.wa{display:none}body{padding-bottom:calc(56px + env(safe-area-inset-bottom))}}
.wa{position:fixed;right:16px;bottom:76px;z-index:70;background:#25D366;color:#052E16;text-decoration:none;
padding:13px 19px;border-radius:100px;font-weight:650;font-size:15px;box-shadow:0 10px 26px rgba(0,0,0,.22)}
@media(min-width:861px){.wa{bottom:20px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;scroll-behavior:auto}}
"""

# ------------------------------------------------------------------ head
def head(title, desc, path, ld=None, noindex=False):
    url = BASE + path
    robots = "noindex, follow" if noindex else "index, follow, max-snippet:-1, max-image-preview:large"
    base_ld = [{
        "@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#org",
        "name": BRAND, "url": BASE + "/",
        "logo": {"@type": "ImageObject", "url": BASE + "/favicon.svg"},
        "description": "UrbanLoop accepts private group transport enquiries across India and confirms a suitable vehicle arrangement and availability per route and date.",
    }, {
        "@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#website",
        "url": BASE + "/", "name": BRAND, "publisher": {"@id": BASE + "/#org"},
    }]
    if ld:
        base_ld.extend(ld if isinstance(ld, list) else [ld])
    ld_html = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in base_ld)
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{html.escape(BRAND)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_IN">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(BRAND)} — private group transport across India">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE}/og.png">
<meta name="theme-color" content="#0F6E68">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/favicon.svg">
<link rel="preload" href="/style.css" as="style">
<link rel="stylesheet" href="/style.css">
{ld_html}
</head>
<body>
<a class="skip-link" href="#main-content">Skip to main content</a>"""

# ------------------------------------------------------------------ chrome
def call_svg():
    return '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L8.1 9.6a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.4c.8.3 1.7.6 2.6.7A2 2 0 0 1 22 16.9Z"/></svg>'

def header(active=""):
    links = "".join(
        f'<a href="{h}"' + (' aria-current="page"' if h == active else "")
        + f'>{html.escape(t)}</a>'
        for t, h in NAV
    )
    mlinks = "".join(f'<a href="{h}">{html.escape(t)}</a>' for t, h in NAV)
    return f"""<header>
  <div class="wrap bar">
    <a class="logo" href="/"><span class="wordmark">{html.escape(BRAND)}</span><span class="sr">{html.escape(TAGLINE)}. Home.</span></a>
    <nav class="main">{links}</nav>
    <div class="hact">
      <a class="calllink" href="{PHONE_HREF}">{call_svg()}<span>{PHONE_TXT}</span></a>
      <a class="btn sm" href="/request-quote/">Request a Trip Quote</a>
      <button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div id="mnav">{mlinks}
    <div class="mcta">
      <a class="btn wide" href="/request-quote/">Request a Trip Quote</a>
      {(f'<a class="btn wide" style="background:#25D366;color:#052E16" href="https://wa.me/{WHATSAPP}">WhatsApp us</a>' if WHATSAPP else '')}
      <a class="btn ghost wide" href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a>
    </div>
  </div>
</header>
<main id="main-content">"""

def footer():
    wa = (f'<a class="wa" href="https://wa.me/{WHATSAPP}" rel="noopener">WhatsApp</a>' if WHATSAPP else "")
    sticky = ('<div class="sticky">'
              '<a class="q" href="/request-quote/">Request Quote</a>'
              + (f'<a class="w" href="https://wa.me/{WHATSAPP}" rel="noopener">WhatsApp</a>' if WHATSAPP else "")
              + f'<a href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a></div>')
    def col(t, items):
        return f'<div><h3 class="fh">{t}</h3>' + "".join(
            f'<a href="{h}">{html.escape(n)}</a>' for n, h in items) + '</div>'
    return f"""</main>
<footer><div class="wrap">
<div class="fgrid">
  <div>
    <div class="logo" style="color:#fff;margin-bottom:12px"><span class="wordmark">{html.escape(BRAND)}</span></div>
    <p style="font-size:14.5px;color:#9FB0BE;max-width:36ch">UrbanLoop helps groups arrange private transport across India. We check the route, vehicle option and date before sending a quotation.</p>
    <p style="margin-top:14px"><a href="{PHONE_HREF}" style="font-weight:600;color:#fff">{call_svg()}&nbsp;Call customer care</a></p>
  </div>
  {col("Trip types", [("Airport group transfers","/services/airport-group-transfers/"),
                 ("Outstation group travel","/services/outstation-group-travel/"),
                 ("Weddings & events","/services/wedding-guest-transport/"),
                 ("Corporate travel","/services/corporate-group-transport/"),
                 ("Pilgrimage travel","/services/pilgrimage-group-travel/"),
                 ("Events and group tours","/services/events-group-transport/")])}
  {col("Company", [("Find a vehicle","/find-a-vehicle/"),
                   ("Published routes","/india/"),
                   ("Force Urbania options","/find-a-vehicle/"),
                   ("How it works","/how-it-works/"),
                   ("What to expect","/what-to-expect/"),("Guides","/guides/"),
                   ("Partner with us","/partner-with-us/"),
                   ("About","/about/"),("Contact","/contact/")])}
  {col("Legal", [("Privacy","/privacy/"),("Terms","/terms/")])}
</div>
<div class="fbot">
  <span>&copy; {YEAR} {html.escape(BRAND)} &middot; India</span>
  <span>Private group transport &middot; Quotation on request</span>
</div>
</div></footer>
{wa}{sticky}
<script>
(function(){{
  var b=document.getElementById('burger'), m=document.getElementById('mnav');
  if(b&&m){{b.addEventListener('click',function(){{var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o);}});}}
}})();
</script>
</body>
</html>"""

def crumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "item": BASE + h}
                                for i, (t, h) in enumerate(items)]}

def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def service_ld(name, desc, area_type="City", area_name=None):
    area_name = area_name or CITY
    return {"@context": "https://schema.org", "@type": "Service", "name": name,
            "serviceType": "Private group transport and vehicle hire",
            "description": desc, "provider": {"@id": BASE + "/#org"},
            "areaServed": {"@type": area_type, "name": area_name},
            "offers": {"@type": "Offer",
                       "priceSpecification": {"@type": "PriceSpecification",
                                              "description": "Quotation provided on request after trip details are submitted. Availability is not guaranteed and is confirmed per enquiry."}}}

# ------------------------------------------------------------------ components
def hero(eyebrow, h1, sub, paras=(), ctas=True, extra=""):
    ps = "".join(f'<p class="lede" style="margin-top:14px">{p}</p>' for p in paras)
    acts = ""
    if ctas:
        acts = ('<div class="heroacts">'
                '<a class="btn" href="/request-quote/">Request a Trip Quote</a>'
                f'<a class="btn ghost" href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a></div>')
    return (f'<section class="hero"><div class="wrap"><div class="hgrid"><div>'
            f'<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1>'
            f'<p class="lede" style="margin-top:18px">{sub}</p>{ps}{acts}</div>'
            f'<div>{extra}</div></div></div></section>')

def section(eyebrow, h2, lede, body, alt=False):
    return (f'<section class="{"alt" if alt else ""}"><div class="wrap">'
            f'<div class="shead"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>'
            f'<p class="lede">{lede}</p></div>{body}</div></section>')

def cta_band(h2="Tell us about your trip and we will send a quotation.",
             lede="Share the date, pickup point, destination, number of passengers and expected duration. We reply with a quotation — this is an enquiry, not a confirmed booking."):
    return (f'<section class="alt"><div class="wrap"><div class="shead"><h2>{h2}</h2>'
            f'<p class="lede">{lede}</p></div>'
            f'<div class="heroacts"><a class="btn" href="/request-quote/">Request a Trip Quote</a>'
             f'<a class="btn ghost" href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a></div>'
            f'</div></section>')

def faq_block(pairs, h2="Questions people ask before enquiring.", eyebrow="FAQ"):
    inner = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)
    return (f'<section><div class="wrap"><div class="shead"><span class="eyebrow">{eyebrow}</span>'
            f'<h2>{h2}</h2></div><div class="faq">{inner}</div></div></section>')

def _hero_photo():
    """The supplied hero photograph, if one is present."""
    for name in ("hero-split.jpg", "hero-split.png", "hero-split.webp",
                 "hero-poster.jpg", "hero-poster.png", "hero-poster.webp"):
        if os.path.exists(os.path.join(OUT, "media", "hero", name)):
            return "/media/hero/" + name
    return None


def vehicle_panel():
    """Vehicle figure for a subpage hero.

    Serves the supplied photograph when one exists, and falls back to a clearly
    labelled diagram — never to stock imagery passed off as the actual vehicle.
    The diagram used to be the only branch, so six subpages shipped a hand-drawn
    box captioned "photographs are being prepared" while a real image sat unused.
    """
    photo = _hero_photo()
    if photo:
        return (
            '<div class="vwrap">'
            f'<img src="{photo}" alt="Force Urbania group transport vehicle" width="747" height="685" loading="lazy" decoding="async">'
            '<p class="vcap"><b>Force Urbania group transport.</b> One of the vehicle options '
            'that may suit your route and group size.</p></div>')
    svg = ('<svg viewBox="0 0 640 300" role="img" aria-label="Illustrative diagram of a 17-seat Force Urbania-style '
           'group travel van, showing passenger seating and a rear luggage area."><rect width="640" height="300" fill="#EAF0F4"/>'
           '<rect x="60" y="70" width="520" height="150" rx="18" fill="#FFFFFF" stroke="#CDD8E0" stroke-width="2"/>'
           '<rect x="60" y="70" width="120" height="150" rx="18" fill="#116A7B" opacity=".12"/>'
           '<path d="M180 70 h300 a18 18 0 0 1 18 18 v40 h-336 v-40 a18 18 0 0 1 18-18 Z" fill="#116A7B" opacity=".22"/>'
           '<circle cx="150" cy="232" r="20" fill="#0E1B2A"/><circle cx="470" cy="232" r="20" fill="#0E1B2A"/>'
           '<g fill="#CDD8E0">'
           '<rect x="200" y="120" width="34" height="30" rx="5"/><rect x="246" y="120" width="34" height="30" rx="5"/>'
           '<rect x="292" y="120" width="34" height="30" rx="5"/><rect x="200" y="160" width="34" height="30" rx="5"/>'
           '<rect x="246" y="160" width="34" height="30" rx="5"/><rect x="292" y="160" width="34" height="30" rx="5"/>'
           '<rect x="338" y="120" width="34" height="30" rx="5"/><rect x="384" y="120" width="34" height="30" rx="5"/>'
           '<rect x="338" y="160" width="34" height="30" rx="5"/><rect x="384" y="160" width="34" height="30" rx="5"/>'
           '</g>'
           '<rect x="450" y="115" width="105" height="75" rx="8" fill="none" stroke="#116A7B" stroke-width="2" stroke-dasharray="6 5"/>'
           '<text x="502" y="160" font-family="Inter,sans-serif" font-size="13" fill="#0C4F5C" text-anchor="middle">Luggage</text>'
           '<text x="120" y="150" font-family="Inter,sans-serif" font-size="13" fill="#0C4F5C" text-anchor="middle">Driver</text>'
           '</svg>')
    return ('<div class="vwrap">' + svg +
            '<p class="vcap"><b>Illustrative diagram &mdash; not a photograph of the actual '
            'vehicle.</b></p></div>')

def write_page(path, doc):
    rel = path.lstrip("/")
    if rel == "" or rel.endswith("/"):
        rel = rel + "index.html"
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("wrote", path)
