#!/usr/bin/env python3
"""Westbridge — page builders. Run: python3 build_pages.py"""
import os, json, html
from build_ui import (BASE, BRAND, TAGLINE, EMAIL, WHATSAPP, CITY, OUT, TODAY, CSS, NAV,
                      head, header, footer, crumb_ld, faq_ld, service_ld, hero, shead,
                      card, faq_block, band, workflow, write_page)
from build_data import JOURNEY, DIAGNOSIS, SOLUTIONS, PACKAGES, STEPS, PROJECTS, INDUSTRIES

def page(path, title, desc, body, ld=None, active="", keywords=None, noindex=False):
    doc = "\n".join([head(title, desc, path, ld, keywords, noindex), header(active), body, footer()])
    write_page(path, doc)

# ---------------------------------------------------------------- shared sections
def diag_section():
    cards = "".join(
        f'<button class="dcard" data-d="{d["key"]}" aria-expanded="false">'
        f'<h3>{d["title"]}</h3><p>{d["short"]}</p></button>' for d in DIAGNOSIS)
    panels = ""
    for d in DIAGNOSIS:
        p = d["panel"]
        rows = "".join(f'<div class="row"><b>{k}</b><span>{v}</span></div>' for k, v in p["rows"])
        panels += (f'<div class="dpanel" data-p="{d["key"]}"><div class="dbox">'
                   f'<p class="lede" style="max-width:70ch">{p["finding"]}</p>'
                   f'<div style="margin-top:20px">{rows}</div>'
                   f'<div class="card accent" style="margin-top:22px">'
                   f'<span class="k">Recommended system</span><h3>{p["system"]}</h3>'
                   f'<a class="txtlink" href="{p["link"]}">{p["label"]}</a></div>'
                   f'</div></div>')
    js = """<script>
(function(){
  var cards=document.querySelectorAll('.dcard'), panels=document.querySelectorAll('.dpanel');
  cards.forEach(function(c){ c.addEventListener('click',function(){
    var k=c.getAttribute('data-d'), open=c.classList.contains('on');
    cards.forEach(function(x){x.classList.remove('on');x.setAttribute('aria-expanded','false');});
    panels.forEach(function(p){p.classList.remove('on');});
    if(!open){ c.classList.add('on'); c.setAttribute('aria-expanded','true');
      var t=document.querySelector('.dpanel[data-p="'+k+'"]'); if(t) t.classList.add('on'); }
  });});
})();
</script>"""
    return (f'<section id="diagnose"><div class="wrap">'
            f'{shead("Start here", "Where is your business losing customers?", "Pick the sentence that sounds most like your business. You will get a straight answer on what is usually behind it, and what we would look at first.")}'
            f'<div class="diag">{cards}</div>{panels}</div></section>{js}')

def journey_section():
    stages = "".join(
        f'<div class="stage{" on" if i in (1,2,4) else ""}"><span class="n">{i+1:02d}</span>'
        f'<h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(JOURNEY))
    return (f'<section id="journey"><div class="wrap">'
            f'{shead("The framework", "The seven stages every customer moves through.", "Businesses rarely lose customers everywhere. They lose them at one or two specific stages — and those are the only stages worth fixing first.")}'
            f'<div class="journey">{stages}</div>'
            f'<p class="small" style="margin-top:26px;max-width:70ch">Highlighted stages are the ones we find broken most often in local businesses: capture, response and recovery.</p>'
            f'<div style="margin-top:24px"><a class="txtlink" href="/how-it-works/">See how we work through them</a></div>'
            f'</div></section>')

def projects_grid(items, show_filters=True):
    f = ('<div class="filters"><button class="on" data-f="all">All systems</button>'
         '<button data-f="get-leads">Get leads</button><button data-f="convert-leads">Convert leads</button>'
         '<button data-f="voice">Voice AI</button><button data-f="whatsapp">WhatsApp</button>'
         '<button data-f="websites">Websites</button><button data-f="automation">Automation</button>'
         '<button data-f="retain">Retention</button></div>') if show_filters else ""
    cards = ""
    for p in items:
        caps = "".join(f'<span>{x}</span>' for x in p["tags"])
        cards += (f'<article class="proj" data-cat="{" ".join(p["cats"])}">'
                  f'<div class="pvis"><div class="mock"><div class="l a"></div><div class="l b"></div>'
                  f'<div class="l c"></div><div class="l b"></div></div>'
                  f'<div class="tags">{"".join(f"<span>{t}</span>" for t in p["tags"][:3])}</div></div>'
                  f'<div class="pbody">'
                  f'<span class="badge {"concept" if p["type"]=="Concept Build" else "client"}">{p["type"]}</span>'
                  f'<h3>{p["title"]}</h3>'
                  f'<p class="prob">{p["summary"]}</p>'
                  f'<div class="cap">{caps}</div>'
                  f'<p class="sys"><b>Built to fix:</b> {p["problem"][:96].rstrip()}…</p>'
                  f'<a class="txtlink" href="/work/{p["slug"]}/">See how it works</a>'
                  f'</div></article>')
    return f'{f}<div class="grid g3">{cards}</div>'

def solutions_section():
    out = ""
    for s in SOLUTIONS:
        feats = "".join(f'<li>{x}</li>' for x in s["features"])
        out += (f'<div class="card" id="{s["anchor"]}"><span class="k">{s["kicker"]}</span>'
                f'<h3>{s["title"]}</h3><p>{s["problem"]}</p>'
                f'<ul>{feats}</ul><p class="out"><b>Outcome:</b> {s["outcome"]}</p></div>')
    return (f'<section id="solutions"><div class="wrap">'
            f'{shead("Solutions", "Four things we fix, in plain language.", "Not a catalogue of technology. Each group addresses one commercial problem — and each can be bought on its own.")}'
            f'<div class="grid g2">{out}</div></div></section>')

def packages_section():
    out = ""
    for p in PACKAGES:
        items = "".join(f'<li>{x}</li>' for x in p["items"])
        price = f'<span class="price">{p["price"]}</span>' if p["price"] else ""
        pop = '<span class="pop">Most common starting point</span>' if p["feat"] else ""
        out += (f'<div class="pack{" feat" if p["feat"] else ""}">{pop}'
                f'<h3>{p["name"]}</h3><p class="small">{p["for_who"]}</p>{price}'
                f'<ul>{items}</ul><p class="out"><b>Outcome:</b> {p["outcome"]}</p></div>')
    return (f'<section id="packages"><div class="wrap">'
            f'{shead("Packages", "Ways to buy it.", "Pricing depends on what the audit finds and how much of the system you need. We would rather quote accurately than publish a number we have to walk back.")}'
            f'<div class="grid g4">{out}</div>'
            f'<p class="small" style="margin-top:26px;max-width:70ch">You do not have to buy everything. Most businesses start with the one stage that is leaking worst, prove it in their own numbers, then extend. '
            f'<a class="txtlink" href="/growth-audit/" style="margin-left:6px">Find out which one</a></p></div></section>')

def steps_section():
    out = "".join(f'<div class="stepc"><span class="n">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in STEPS)
    return f'<section id="process"><div class="wrap">{shead("How it works", "Diagnose. Design. Build. Launch. Improve.")}<div class="steps">{out}</div></div></section>'

def beforeafter_section():
    before = ["Customer calls", "No answer", "Customer calls a competitor"]
    after = ["Customer calls", "AI answers immediately", "Lead captured", "Appointment booked",
             "WhatsApp confirmation sent", "Staff receives a qualified lead"]
    b = "".join(f'<div class="steprow"><i></i>{x}</div>' for x in before)
    a = "".join(f'<div class="steprow"><i></i>{x}</div>' for x in after)
    return (f'<section id="before-after"><div class="wrap">'
            f'{shead("The difference", "What changes when nobody has to pick up.", "The same call, handled two ways. This is the whole idea, and it is why response speed is the first thing we fix.")}'
            f'<div class="ba">'
            f'<div class="bacard before"><h3>Without Westbridge</h3>{b}'
            f'<p class="small" style="margin-top:18px">Nothing was broken. The call simply rang out, and the customer moved on.</p></div>'
            f'<div class="bacard after"><h3>With Westbridge</h3>{a}'
            f'<p class="small" style="margin-top:18px">One more booking, recorded and confirmed — without anyone stopping what they were doing.</p></div>'
            f'</div></div></section>')

def demo_section():
    return ('<section id="demo"><div class="wrap">'
            + shead("Demonstration", "Watch how an enquiry is lost — and recovered.",
                    "A 52-second walkthrough of the flow we install: a 9pm enquiry that goes unanswered, and a booking confirmed the next morning. This is our own explainer, labelled as ours — not a client recording.")
            + '<div style="margin-top:34px">'
              '<video controls preload="metadata" playsinline poster="/assets/westbridge-logo.jpg" '
              'style="width:100%;max-width:940px;border:1px solid var(--line-2);border-radius:16px;background:#000">'
              '<source src="/video/westbridge_explainer.mp4" type="video/mp4">Your browser does not support video.</video>'
              '<p class="small" style="margin-top:12px">Westbridge — Enquiry Response System · 52 seconds</p>'
              '</div></div></section>')

def industries_section():
    out = "".join(
        f'<a class="card" href="/industries/{i["slug"]}/" style="text-decoration:none;display:block">'
        f'<h3>{i["name"]}</h3><p>{i["intro"][:132].rstrip()}\u2026</p>'
        f'<span class="txtlink" style="margin-top:16px">See the workflow</span></a>'
        for i in INDUSTRIES)
    return (f'<section id="industries"><div class="wrap">'
            f'{shead("Industries", "Designed around your actual customer journey.", "These are not generic pages with the word \u201cbusiness\u201d swapped out. Each maps the real workflow of that trade, end to end.")}'
            f'<div class="grid g3">{out}</div></div></section>')

HOME_FAQ = [
 ("What exactly does Westbridge do?",
  "We find where a business is losing customers — usually at the point of enquiry, response or follow-up — and then build the systems that fix it: a conversion-led website, AI response on calls and WhatsApp, booking, CRM records, automated follow-up, review requests and customer reactivation."),
 ("Do I need to understand AI to work with you?",
  "No. You need to understand your customers. We choose the technology; you get the outcome. Much of what we sell is really a guarantee that nothing goes unanswered."),
 ("Will this replace my staff?",
  "No. It removes the repetitive part — repeated questions, reminders, chasing quotes — so your people spend their time on work that genuinely needs a person."),
 ("Can it use my existing WhatsApp number?",
  "Yes. We work with your existing number so customers keep messaging the same place they always have. Nothing changes for them."),
 ("Can it work with my current website?",
  "Often, yes — response, booking and follow-up can be layered onto what you already have. If the website itself is the leak, we will say so and quote a replacement separately."),
 ("Can the AI transfer to a human?",
  "Always, and immediately on request. Every system we build has human handover built in rather than added afterwards."),
 ("What happens when the AI does not know an answer?",
  "It says so and hands the conversation to a person with the context already collected. It does not guess, and it only answers from content the business has approved."),
 ("Can Westbridge work with my existing CRM?",
  "Usually. If you already run a CRM we integrate with it. If you do not, we set up something appropriate rather than selling you an enterprise platform you will not use."),
 ("How long does implementation take?",
  "Simple response and follow-up systems can be live within days. Anything involving voice, telephony or multiple locations takes longer, because it is tested against real calls before going live."),
 ("What kinds of businesses is this suitable for?",
  "Businesses where one customer is worth a meaningful amount and enquiries arrive by phone or WhatsApp — clinics, salons and spas, real estate, hotels and venues, home and auto services, coaching centres and professional practices."),
 ("Do I have to buy everything?",
  "No. Most businesses start with the single stage that is leaking worst, prove it works in their own numbers, then extend. You can stop after the first fix."),
 ("How is customer data handled?",
  "Only what is needed for the enquiry, used only to respond to it, never sold or rented. Consent is captured explicitly, opt-outs stop contact immediately, and you can ask us to delete your data at any time."),
 ("Is this an AI company?",
  "No. We are a customer-response and revenue-recovery practice that uses AI where it helps. If a human process fixes the problem better, we will say that instead."),
]

# ---------------------------------------------------------------- HOME
def build_home():
    trust = ["Diagnose first — we audit before we quote",
             "Built and managed by us, not a DIY subscription",
             "Concept builds clearly labelled as concept builds",
             "Human handover in every system"]
    strap = "Websites <s>·</s> WhatsApp <s>·</s> AI Calls <s>·</s> Lead Follow-Up <s>·</s> CRM <s>·</s> Automation"
    featured = [p for p in PROJECTS if p.get("featured")] + [p for p in PROJECTS if not p.get("featured")][:1]
    body = (hero("Revenue-leak diagnosis · " + CITY,
                 "We find where your business is losing customers — and build the systems that fix it.",
                 "Most local businesses do not have a marketing problem. They have a leak: a call that rings out, a message read hours later, a quote nobody chased. We find that leak, fix it, and prove it in your numbers.",
                 ctas=True, strap=strap, trust=trust)
            + diag_section()
            + journey_section()
            + '<section id="featured"><div class="wrap">'
              + shead("Proof of work", "Systems we have built and can show you.",
                      "Working builds, labelled honestly as concept builds — designed and demonstrated by Westbridge, not deployed at a named client. When real client work arrives it will be labelled as client work.")
              + projects_grid(featured, show_filters=False)
              + '<div style="margin-top:30px"><a class="txtlink" href="/work/">See all systems</a></div></div></section>'
            + solutions_section()
            + demo_section()
            + industries_section()
            + steps_section()
            + beforeafter_section()
            + '<section id="audit-cta"><div class="wrap">'
              + shead("Growth audit", "Find out where your business is losing customers.",
                      "A short diagnostic — what you sell, how customers reach you, and what you think is broken. You get a recommended setup immediately, and a written finding from us.")
              + '<div class="grid g3" style="margin-top:8px">'
              + card("01", "Answer a few questions", "About two minutes. No jargon, and nothing you would have to look up.")
              + card("02", "See your recommended setup", "The specific system we would install first, based on the problem you picked.")
              + card("03", "Get a written finding", "We read your public customer journey and send a specific finding — not a brochure.")
              + '</div><div style="margin-top:30px"><a class="btn" href="/growth-audit/">Find my revenue leaks</a></div>'
              + '</div></section>'
            + faq_block(HOME_FAQ, "Questions people actually ask.", "FAQ")
            + band("Would this increase trust if we emailed you tomorrow?",
                   "We are early and we say so. What we can offer now is a specific diagnosis of your customer journey, a working demonstration of the system, and honest labelling of everything that is a concept build rather than client work."))
    page("/", "Westbridge — We find where your business is losing customers",
         "Westbridge diagnoses where local businesses lose customers — missed calls, slow replies, unchased quotes — and builds the websites, AI response and follow-up systems that fix it. Hyderabad, India.",
         body,
         ld=[service_ld("Revenue-leak diagnosis and customer-response systems",
                        "Diagnosis of where a business loses customers, followed by implementation of enquiry response, booking, CRM, follow-up and reactivation systems.",
                        "Local and service businesses in India"),
             {"@context": "https://schema.org", "@type": "VideoObject",
              "name": "Westbridge — Enquiry Response System",
              "description": "How a local business loses an enquiry at 9pm and recovers it: acknowledgement, qualification, booking and reminder.",
              "thumbnailUrl": BASE + "/assets/westbridge-logo.jpg",
              "contentUrl": BASE + "/video/westbridge_explainer.mp4",
              "uploadDate": TODAY, "duration": "PT52S"},
             faq_ld(HOME_FAQ)],
         active="/")

# ---------------------------------------------------------------- SOLUTIONS
def build_solutions():
    body = (hero("Solutions", "Four problems. Four systems.",
                 "We do not sell a catalogue of technology. We fix the stage of your customer journey that is leaking — and it is entirely reasonable to start with just one of these.",
                 strap="Get found <s>·</s> Convert more <s>·</s> Never miss a customer <s>·</s> Automate the busywork")
            + solutions_section()
            + packages_section()
            + steps_section()
            + faq_block([
                ("Do I have to buy all four?",
                 "No. Most businesses start with one. The audit tells you which one is leaking worst, and that is the one worth fixing first."),
                ("How do I know which one I need?",
                 "If you are short of enquiries it is Get found. If enquiries arrive and go cold it is Convert more. If they arrive when nobody can answer it is Never miss a customer. If your team is drowning in repeat admin it is Automate the busywork."),
                ("Can you do just the website?",
                 "Yes — though a website without a response system is only half the job, because the enquiries it generates still need answering."),
                ("What if I already have some of this?",
                 "Then we build around it. Nothing is replaced for the sake of it."),
                ("How is pricing decided?",
                 "By what the audit finds and how much of the system you need. We quote after the diagnosis rather than before, so the number reflects your actual situation."),
              ], "Choosing between them.", "FAQ")
            + band("Not sure which one is your problem?",
                   "The diagnostic takes two minutes and gives you a straight answer on what we would fix first."))
    page("/solutions/", "Solutions — Websites, AI Response, Follow-Up and Automation | Westbridge",
         "Four solution groups for local businesses: get found, convert more enquiries, never miss a customer, and automate repetitive admin. Hyderabad, India.",
         body,
         ld=[service_ld("Customer acquisition, response and retention systems",
                        "Conversion websites, AI reception, WhatsApp automation, CRM, follow-up, booking, reviews and reactivation for local businesses."),
             crumb_ld([("Home", "/"), ("Solutions", "/solutions/")])],
         active="/solutions/",
         keywords="AI receptionist India, WhatsApp automation local business, lead follow up automation, appointment booking automation, local business website lead generation")

# ---------------------------------------------------------------- WORK
def build_work():
    body = (hero("Proof of work", "Systems built, demonstrated and labelled honestly.",
                 "Every build is shown with its problem, its system and its workflow. Where something is a concept build it says so on the card. Where it is client work it will say that instead.",
                 strap="Concept builds <s>·</s> Client work <s>·</s> Demonstrated workflows")
            + '<section><div class="wrap">'
            + shead("Portfolio", "All systems.",
                    "Filter by what you need. Each system page explains the commercial problem, the build, the workflow, and what happens when something goes wrong.")
            + projects_grid(PROJECTS)
            + '<p class="small" style="margin-top:30px;max-width:74ch">Every project on this page is currently a <b>concept build</b> — designed and built by Westbridge to demonstrate the system. None is presented as deployed client work. Client projects will be added, labelled as client work, as they go live.</p>'
            + '</div></section>'
            + band("Want this for your business?",
                   "Tell us how customers currently find and contact you. We will tell you which of these systems would pay for itself first."))
    page("/work/", "Work — AI Receptionist, WhatsApp and Automation Systems | Westbridge",
         "Westbridge concept builds: AI receptionist, WhatsApp sales assistant, lead recovery, no-show recovery, growth websites, review generation and customer reactivation.",
         body, ld=[crumb_ld([("Home", "/"), ("Work", "/work/")])], active="/work/",
         keywords="AI receptionist demo, WhatsApp automation demo, lead recovery system, automation concept builds India")

def build_project(p):
    feats = "".join(f'<li>{x}</li>' for x in p["features"])
    improve = "".join(f'<li>{x}</li>' for x in p["improves"])
    rel = "".join(f'<div class="row"><b>{k}</b><span>{v}</span></div>' for k, v in p["reliability"])
    demo = "".join(f'<li>{x}</li>' for x in p["demo"])
    techspans = "".join(f'<span style="font-size:13px;color:var(--ink-2);border:1px solid var(--line);padding:6px 11px;border-radius:8px">{t}</span>' for t in p["technology"])
    body = (f'<section class="hero"><div class="wrap">'
            f'<span class="eyebrow">{p["type"]} &nbsp;·&nbsp; {" &nbsp;·&nbsp; ".join(p["tags"])} &nbsp;·&nbsp; {p["industry"]}</span>'
            f'<h1 style="margin-top:16px">{p["title"]}</h1>'
            f'<p class="lede" style="margin-top:22px;font-size:clamp(18px,1.9vw,22px)">{p["summary"]}</p>'
            f'<div class="hero-cta"><a class="btn" href="/growth-audit/">Find my revenue leaks</a>'
            f'<a class="btn ghost" href="/work/">All systems</a></div></div></section>'
            + '<section><div class="wrap"><div class="grid g2" style="align-items:start">'
              f'<div>{shead("The problem", "Why this costs money.")}<p class="lede">{p["problem"]}</p></div>'
              f'<div>{shead("What we built", "The complete system.")}<p class="lede">{p["solution"]}</p></div>'
              '</div></div></section>'
            + '<section><div class="wrap"><div class="grid g2" style="align-items:start">'
              f'<div>{shead("See it in action", "The workflow, step by step.")}'
              + workflow(p["workflow"], hi={0, len(p["workflow"]) - 1})
              + f'<p class="small" style="margin-top:20px">{p["demo_note"]} Demonstrations are labelled as examples and never presented as real customer conversations.</p></div>'
              f'<div>{shead("What we would show you", "Available in a walkthrough.")}<div class="card"><ul>{demo}</ul></div>'
              f'<div class="card" style="margin-top:20px"><span class="k">Capabilities in this build</span><ul>{feats}</ul></div></div>'
              '</div></div></section>'
            + '<section><div class="wrap">'
              + shead("Designed to improve", "What this system is built to change.",
                      "These are the intended outcomes. We have not measured them at a paying client yet, so they are stated as designed objectives — not results, and with no invented percentages.")
              + f'<div class="card"><ul>{improve}</ul></div></div></section>'
            + f'<section><div class="wrap">{shead("Reliability &amp; human handover", "What happens when the AI should not be the one answering.")}'
              f'<div class="dbox">{rel}</div></div></section>'
            + f'<section><div class="wrap">{shead("Technology", "How it is put together.", "The commercial outcome comes first; this is the implementation behind it.")}'
              f'<div class="card" style="display:flex;gap:8px;flex-wrap:wrap">{techspans}</div></div></section>'
            + band("Where is your business losing customers?",
                   "Tell us how your customers currently find and contact you. We will identify the biggest opportunities and explain what we would improve first."))
    page(f'/work/{p["slug"]}/', f'{p["title"]} — {p["type"]} | Westbridge',
         p["summary"][:158], body,
         ld=[service_ld(p["title"], p["summary"], p["industry"]),
             crumb_ld([("Home", "/"), ("Work", "/work/"), (p["title"], f'/work/{p["slug"]}/')])],
         active="/work/", keywords=f'{p["title"]}, {", ".join(p["tags"])}')

# ---------------------------------------------------------------- INDUSTRIES
def build_industries():
    body = (hero("Industries", "Built around your actual customer journey.",
                 "Generic pages describe your trade. These map the workflow: how the enquiry arrives, who answers it, where it becomes a booking, and where it is usually lost.",
                 strap="Clinics <s>·</s> Salons &amp; spas <s>·</s> Real estate <s>·</s> Hotels &amp; venues <s>·</s> Coaching <s>·</s> Services")
            + industries_section()
            + band("Your industry not listed?",
                   "The workflow is usually similar even when the trade differs. Tell us how customers reach you and we will map it."))
    page("/industries/", "Industries — Clinics, Salons, Real Estate, Hotels, Coaching | Westbridge",
         "Industry-specific customer workflows for clinics, salons and spas, real estate, hotels and venues, coaching centres and local services in India.",
         body, ld=[crumb_ld([("Home", "/"), ("Industries", "/industries/")])], active="/industries/",
         keywords="AI receptionist for dentists, WhatsApp automation for clinics India, appointment booking salons, real estate lead follow up")

def build_industry(i):
    pains = "".join(f'<li>{x}</li>' for x in i["pains"])
    systems = "".join(f'<span style="font-size:13px;color:var(--ink-2);border:1px solid var(--line);padding:6px 11px;border-radius:8px">{s}</span>' for s in i["systems"])
    body = (f'<section class="hero"><div class="wrap"><span class="eyebrow">Industry &nbsp;·&nbsp; {i["name"]}</span>'
            f'<h1 style="margin-top:16px">{i["headline"]}</h1>'
            f'<p class="lede" style="margin-top:22px;font-size:clamp(18px,1.9vw,22px)">{i["intro"]}</p>'
            f'<div class="hero-cta"><a class="btn" href="/growth-audit/">Find my revenue leaks</a>'
            f'<a class="btn ghost" href="/industries/">Other industries</a></div></div></section>'
            + '<section><div class="wrap"><div class="grid g2" style="align-items:start">'
              f'<div>{shead("Where it leaks", "The predictable losses in this trade.")}<div class="card"><ul>{pains}</ul></div></div>'
              f'<div>{shead("The workflow we would build", "Enquiry to repeat customer.")}'
              + workflow(i["workflow"], hi={0, len(i["workflow"]) - 1}) + '</div>'
              '</div></div></section>'
            + f'<section><div class="wrap">{shead("Systems involved", "What this usually includes.")}'
              f'<div class="card" style="display:flex;gap:8px;flex-wrap:wrap">{systems}</div></div></section>'
            + '<section><div class="wrap">' + shead("What changes", "Designed to improve.")
              + '<div class="grid g3">'
              + card("", "Faster first response", "Every enquiry acknowledged in minutes, including after hours and at peak.")
              + card("", "More from what you already have", "Interest you already generate converts at a higher rate because nothing is left sitting.")
              + card("", "Less admin for staff", "Reminders, repeat questions and chasing stop being manual work.")
              + '</div></div></section>'
            + band(f"Would this work for your business?",
                   "Tell us how enquiries reach you today. We will map your own workflow and tell you where it is leaking."))
    page(f'/industries/{i["slug"]}/', f'{i["headline"]} | Westbridge',
         i["intro"][:158], body,
         ld=[service_ld(f'Westbridge for {i["name"]}', i["intro"], i["name"]),
             crumb_ld([("Home", "/"), ("Industries", "/industries/"), (i["name"], f'/industries/{i["slug"]}/')])],
         active="/industries/",
         keywords=f'AI for {i["name"].lower()}, {i["name"].lower()} lead response, missed call recovery {i["name"].lower()}')

# ---------------------------------------------------------------- HOW IT WORKS / ABOUT
def build_how():
    body = (hero("How it works", "Diagnose first. Then build only what is leaking.",
                 "We do not start with a product. We start by reading your customer journey — where enquiries arrive, who answers them, and where they stop turning into customers.",
                 strap="01 Diagnose <s>·</s> 02 Design <s>·</s> 03 Build <s>·</s> 04 Launch <s>·</s> 05 Improve")
            + steps_section()
            + '<section><div class="wrap">'
              + shead("Diagnosis", "What the diagnosis actually looks at.",
                      "We use what a customer sees. No access to your internal systems is needed for this stage, and it takes nothing from your staff.")
              + '<div class="grid g3">'
              + card("", "Where you are found", "Search, Google Business Profile, your website, social — and whether each gives a visitor something to do.")
              + card("", "How enquiries arrive", "Calls, WhatsApp, forms, Instagram, walk-ins — and which of them land somewhere owned.")
              + card("", "How fast you reply", "Including after hours. This is usually the single largest leak we find.")
              + card("", "What happens after the quote", "Whether anything is chased, and how long interest survives unattended.")
              + card("", "Where staff time goes", "Which repetitive tasks consume hours that should belong to customers in front of you.")
              + card("", "What you can already measure", "Which channel produces bookings — or why nobody can currently tell.")
              + '</div></div></section>'
            + '<section><div class="wrap">' + shead("Design &amp; build", "Then we fix one thing properly.")
              + '<div class="grid g2">'
              + card("Design", "The highest-impact fix first", "We recommend the single change with the best return, not the biggest project. You can stop after it.")
              + card("Build", "Tested before it goes live", "Anything handling real calls or messages is tested against real scenarios before your customers meet it.")
              + '</div></div></section>'
            + faq_block([
                ("What does the diagnosis cost?", "Nothing. We read your public customer journey and send a written finding. If it is not worth acting on, we will say so."),
                ("How long before anything goes live?", "A response and follow-up system can be live within days. Voice, telephony and multi-location work takes longer because it is tested against real calls first."),
                ("What do you need from me?", "One line about the business, and access to the channels we are connecting. No access to internal systems is needed for the diagnosis."),
                ("How do you measure whether it worked?", "Response time, enquiries acknowledged, bookings produced, quotes recovered and reviews received. If it does not move one of those, it is not working."),
              ], "Practical questions.", "FAQ")
            + band("Start with the diagnosis.",
                   "Two minutes of questions, a recommended setup immediately, and a written finding from us afterwards."))
    page("/how-it-works/", "How It Works — Diagnose, Design, Build, Launch, Improve | Westbridge",
         "Westbridge's method: diagnose where customers are lost, design the highest-impact fix, build and test it, launch it, then keep improving it.",
         body, ld=[crumb_ld([("Home", "/"), ("How it works", "/how-it-works/")])], active="/how-it-works/",
         keywords="AI automation process, local business growth audit, customer journey diagnosis India")

def build_about():
    body = (hero("About", "An audit habit, applied to customers.",
                 "Westbridge exists because the same failure turns up in business after business: an enquiry arrives, nobody owns it, nothing escalates, and no one notices until the customer is gone.",
                 ctas=True)
            + '<section><div class="wrap">' + shead("Who", "About the practice.")
              + '<div class="dbox">'
              + '<div class="row"><b>Operated by</b><span>Abhishek Singh, FCCA, MCSI — around twelve years in internal audit, model risk, controls and compliance in financial services.</span></div>'
              + '<div class="row"><b>Why that matters</b><span>The failure is almost never technical. It is a process with no owner and no escalation, and auditing is the discipline of finding exactly that — and of proving whether a fix worked.</span></div>'
              + '<div class="row"><b>How we work</b><span>Evidence before contact. We read the public customer journey and name a specific defect before proposing any project.</span></div>'
              + f'<div class="row"><b>Where we work</b><span>{CITY} first, where businesses are researchable and owners reachable. Delivery is remote, so other Indian cities are served too.</span></div>'
              + '<div class="row"><b>What we will not do</b><span>Sell you AI you do not need, publish a statistic we cannot source, or present a concept build as client work.</span></div>'
              + '<div class="row"><b>Size</b><span>Small on purpose. The person who diagnoses your business is the person who builds and answers your email.</span></div>'
              + '</div></div></section>'
            + '<section><div class="wrap">' + shead("How we talk about our work", "Honest labelling, by rule.")
              + '<div class="grid g3">'
              + card("Concept build", "Built and demonstrated by us", "Designed to show the system working. Never described as deployed at a client.")
              + card("Client work", "Deployed for a paying business", "Only claimed once it is genuinely live, and only with permission.")
              + card("Designed to improve", "An objective, not a result", "Until numbers are measured at a real client, outcomes are stated as intent. No invented percentages.")
              + '</div></div></section>'
            + faq_block([
                ("How big is Westbridge?", "Small on purpose. The diagnosis and the build are done by the same person who answers your email — there is no account manager between you and the work."),
                ("Do you outsource the building?", "No. We build and manage what we sell, which is why we are careful about what we take on."),
                ("Is Westbridge an agency?", "We describe it as a practice. We diagnose, build and manage a customer-response system — closer to how an audit is delivered than how a campaign agency runs."),
                ("What are your credentials?", "FCCA and MCSI, with around twelve years in internal audit, risk, controls and compliance. No conventional undergraduate degree, which we state plainly rather than obscure."),
              ], "About the practice.", "FAQ")
            + band("Want the same read of your business?",
                   "The growth audit is free and takes two minutes to start."))
    page("/about/", "About — Westbridge Customer Response Systems, Hyderabad",
         "Westbridge is an independent practice in Hyderabad that diagnoses where businesses lose customers, applying an audit discipline to customer journeys.",
         body, ld=[crumb_ld([("Home", "/"), ("About", "/about/")])], active="/about/",
         keywords="Westbridge Hyderabad, customer response consultancy India, revenue leak audit")

# ---------------------------------------------------------------- GROWTH AUDIT
AUDIT_JS = """<script>
(function(){
  var form=document.getElementById('audit'); if(!form) return;
  var steps=[].slice.call(form.querySelectorAll('.fstep'));
  var bars=[].slice.call(document.querySelectorAll('.fprog i'));
  var i=0, nxt=document.getElementById('anext'), bak=document.getElementById('aback'),
      cnt=document.getElementById('acount'), res=document.getElementById('result');
  var REC={
    "Need more enquiries":{sys:"Conversion Website + Local Visibility + Lead Capture",
      areas:["Lead generation","Google and local visibility","Website conversion"],
      note:"Being found, and being easy to act on, is your first fix. Response systems matter less until enquiries exist."},
    "Missed calls":{sys:"AI Receptionist + Missed-Call Recovery + Booking",
      areas:["Lead response","Missed-call recovery","After-hours availability"],
      note:"A call that rings out is the most expensive leak there is, because the customer is already trying to buy."},
    "Slow responses":{sys:"Instant Response + WhatsApp Automation + CRM",
      areas:["Lead response","Instant acknowledgement","Lead routing"],
      note:"You are losing customers to whoever replies first. This is usually the fastest fix with the clearest return."},
    "Leads don't follow up":{sys:"CRM + Automated Follow-Up + Quote Recovery",
      areas:["Follow-up sequencing","Quote recovery","Pipeline visibility"],
      note:"You already earn this revenue and lose it to silence. Chasing it is the highest-return work available."},
    "Poor website":{sys:"Conversion Website + WhatsApp CTA + Analytics",
      areas:["Website conversion","Enquiry capture","Channel measurement"],
      note:"The site is describing the business rather than giving a visitor one obvious thing to do."},
    "Too many repetitive tasks":{sys:"Reminders + FAQ Handling + Review Automation",
      areas:["Staff workload","Reminder automation","Review generation"],
      note:"Your people are doing work that follows the same pattern every time. That is the definition of automatable."},
    "Appointment no-shows":{sys:"Booking + Reminders + No-Show Recovery",
      areas:["No-show reduction","Booking confirmation","Slot recovery"],
      note:"Booked appointments that do not convert are pure lost revenue, and the reminder is usually the missing piece."},
    "Not enough Google reviews":{sys:"Review Generation + Feedback Routing",
      areas:["Review volume","Reputation","Unhappy-customer recovery"],
      note:"Happy customers rarely volunteer. Being asked at the right moment is most of the difference."},
    "Old customers don't return":{sys:"Reactivation + Rebooking + Retention Reporting",
      areas:["Repeat revenue","Customer reactivation","Lifetime value"],
      note:"Your existing customer list is the cheapest revenue available, and it is currently sitting still."},
    "Unsure":{sys:"Diagnose first — then a staged build",
      areas:["Full journey diagnosis","Prioritised fix list","Measurement setup"],
      note:"That is a perfectly good answer. We will diagnose the journey and tell you which stage is leaking worst."}
  };
  function render(){
    steps.forEach(function(s,n){s.classList.toggle('on',n===i);});
    bars.forEach(function(b,n){b.classList.toggle('on',n<=i);});
    bak.style.visibility=i===0?'hidden':'visible';
    nxt.textContent=(i===steps.length-1)?'Show my recommended setup':'Continue';
    if(cnt) cnt.textContent='Step '+(i+1)+' of '+steps.length;
  }
  function invalid(){
    var cur=steps[i], f=[].slice.call(cur.querySelectorAll('[required]')), bad=false;
    for(var k=0;k<f.length;k++){
      var x=f[k];
      if(x.type==='radio'||x.type==='checkbox'){
        var g=[].slice.call(cur.querySelectorAll('input[name="'+x.name+'"]'));
        if(!g.some(function(y){return y.checked;})){bad=true;break;}
      } else if(!x.value.trim()){ x.focus(); bad=true; break; }
    }
    if(bad){ alert('Please answer this step to continue.'); return true; }
    return false;
  }
  function collect(){
    var d={};
    new FormData(form).forEach(function(v,k){ if(k==='_honey') return; d[k]=d[k]?d[k]+', '+v:v; });
    return d;
  }
  function showResult(){
    var d=collect(), key=d['Biggest problem']||'Unsure', r=REC[key]||REC['Unsure'];
    document.getElementById('rsys').textContent=r.sys;
    document.getElementById('rnote').textContent=r.note;
    document.getElementById('rproblem').textContent=key;
    var list=document.getElementById('rareas'); list.innerHTML='';
    r.areas.concat(['Follow-up automation','Measurement and reporting']).slice(0,5).forEach(function(a,n){
      var el=document.createElement('div'); el.className='ritem';
      el.innerHTML='<span class="num">0'+(n+1)+'</span><div><b>'+a+'</b><p>'+
        (n===0?'The highest-impact place to start, based on what you told us.':'Included in the recommended setup for this problem.')+
        '</p></div>';
      list.appendChild(el);
    });
    form.style.display='none';
    document.querySelector('.fprog').style.display='none';
    res.classList.add('on');
    res.scrollIntoView({behavior:'smooth',block:'start'});
  }
  function submit(){
    var d=collect(); showResult();
    fetch('https://formsubmit.co/ajax/'+encodeURIComponent(document.getElementById('femail').value.trim()),
      {method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
       body:JSON.stringify(d)}).then(function(){ 
         var s=document.getElementById('rsent'); if(s) s.textContent='Your answers have been sent to Westbridge.';
       }).catch(function(){
         var s=document.getElementById('rsent');
         if(s) s.textContent='We could not send automatically — please email us the same details so nothing is missed.';
       });
  }
  nxt.addEventListener('click',function(){
    if(invalid()) return;
    if(i===steps.length-1){ submit(); return; }
    i=Math.min(i+1,steps.length-1); render();
  });
  bak.addEventListener('click',function(){ i=Math.max(i-1,0); render(); });
  form.addEventListener('keydown',function(e){
    if(e.key==='Enter'&&e.target.tagName!=='TEXTAREA'){ e.preventDefault(); nxt.click(); }
  });
  render();
})();
</script>"""

def build_audit():
    def opts(name, values, req=True):
        t = "radio" if req else "checkbox"
        return "".join(
            f'<label class="fopt"><input type="{t}" name="{name}" value="{v}"{" required" if req else ""}>{v}</label>'
            for v in values)
    steps_html = (
        '<div class="fstep on"><h3>What type of business do you run?</h3><span>This decides which workflow we map.</span>'
        + opts("Business type", ["Dental clinic", "Medical / specialty clinic", "Salon or spa", "Real estate",
                                 "Hotel / venue / banquet", "Home or auto services", "Coaching / academy",
                                 "Professional services", "Something else"]) + '</div>'
        '<div class="fstep"><h3>Business name and website</h3><span>So we can read your public customer journey.</span>'
        '<div class="frow"><div><span>Business name *</span><input type="text" name="Business" required autocomplete="organization"></div>'
        '<div><span>Website, if you have one</span><input type="text" name="Website" placeholder="Optional — or your Google listing"></div></div></div>'
        '<div class="fstep"><h3>How do customers usually find you?</h3><span>Tick everything that applies.</span>'
        + opts("Found via", ["Google", "Website", "Instagram / Facebook", "Referrals", "Advertising", "Walk-ins", "Other"], req=False) + '</div>'
        '<div class="fstep"><h3>How do they usually contact you?</h3><span>Tick everything that applies.</span>'
        + opts("Contact via", ["Phone", "WhatsApp", "Website form", "Instagram / Facebook", "Email", "Walk-in", "Other"], req=False) + '</div>'
        '<div class="fstep"><h3>What is currently your biggest problem?</h3><span>Pick the one that costs you most.</span>'
        + opts("Biggest problem", ["Need more enquiries", "Missed calls", "Slow responses", "Leads don't follow up",
                                   "Poor website", "Too many repetitive tasks", "Appointment no-shows",
                                   "Not enough Google reviews", "Old customers don't return", "Unsure"]) + '</div>'
        '<div class="fstep"><h3>Roughly how much is a customer worth?</h3><span>Approximate is fine — this tells us what a leak costs you.</span>'
        + opts("Monthly enquiries", ["Under 30 enquiries a month", "30 to 100", "100 to 300", "Over 300", "Not sure"])
        + '<div class="frow"><div><span>Approximate value of a new customer</span>'
          '<input type="text" name="Customer value" placeholder="e.g. 15000 — optional"></div>'
          '<div><span>City</span><input type="text" name="City" placeholder="Hyderabad"></div></div></div>'
        '<div class="fstep"><h3>Where should we send your finding?</h3><span>We reply within one working day.</span>'
        '<div class="frow"><div><span>Your name *</span><input type="text" name="Name" required autocomplete="name"></div>'
        '<div><span>Email *</span><input type="email" name="Email" id="femail" required autocomplete="email"></div>'
        '<div><span>WhatsApp / phone *</span><input type="tel" name="Phone" required autocomplete="tel"></div>'
        '<div><span>Anything else we should know</span><input type="text" name="Notes" placeholder="Optional"></div></div>'
        '<label class="consent"><input type="checkbox" name="Consent" value="Yes" required>'
        '<span>I agree that Westbridge may use these details to contact me about this request, as described in the '
        '<a href="/privacy/" style="color:var(--ink-2)">privacy notice</a>. No marketing lists, no third parties.</span></label></div>'
    )
    result_html = (
        '<div class="result" id="result">'
        '<div class="rhead"><span class="eyebrow">Your result</span>'
        '<h3>Your recommended Westbridge setup</h3>'
        '<p class="lede" style="margin-top:14px">Based on the problem you picked — <b id="rproblem"></b> — and how your customers reach you.</p>'
        '<p class="lede" id="rnote" style="margin-top:14px"></p></div>'
        '<div style="margin-top:26px"><span class="eyebrow">Recommended system</span>'
        '<div class="big" style="margin-top:12px;font-size:clamp(22px,2.6vw,30px)" id="rsys"></div></div>'
        '<div class="rlist" id="rareas"></div>'
        '<p class="small" style="margin-top:22px;max-width:70ch">This recommendation is rule-based and generated from your answers. It is a starting point for a conversation, not a guaranteed outcome.</p>'
        '<p class="small" id="rsent" style="margin-top:10px"></p>'
        '<div style="margin-top:26px;display:flex;gap:14px;flex-wrap:wrap">'
        '<a class="btn" href="/contact/">Book my free growth review</a>'
        '<a class="btn ghost" href="/work/">See the systems</a></div></div>'
    )
    calc = ('<section id="calculator"><div class="wrap">'
            + shead("The cost of the leak", "What unanswered enquiries may be costing you.",
                    "An illustrative estimate only. Move the sliders to see how the numbers behave — this is a way of thinking about the problem, not a forecast.")
            + '<div class="calc"><div>'
              '<label><span>Enquiries a month <span class="val" id="v1">120</span></span>'
              '<input type="range" id="i1" min="10" max="1000" step="10" value="120"></label>'
              '<label><span>Percentage missed or not followed up <span class="val" id="v2">25%</span></span>'
              '<input type="range" id="i2" min="0" max="80" step="5" value="25"></label>'
              '<label><span>Average value of a customer <span class="val" id="v3">15,000</span></span>'
              '<input type="range" id="i3" min="500" max="200000" step="500" value="15000"></label>'
              '<label><span>Share of those you could realistically recover <span class="val" id="v4">40%</span></span>'
              '<input type="range" id="i4" min="5" max="90" step="5" value="40"></label>'
              '</div>'
              '<div class="cout"><span class="eyebrow">Illustrative opportunity</span>'
              '<div class="big" style="margin-top:14px" id="cout">0</div>'
              '<p class="small" style="margin-top:10px">per month, if that share of the missed enquiries were recovered</p>'
              '<div style="margin-top:20px;padding-top:18px;border-top:1px solid var(--line)">'
              '<p class="small" id="cdetail"></p></div>'
              '<p class="small" style="margin-top:18px">This is an illustrative estimate, not a guaranteed result. It does not account for seasonality, capacity or your actual conversion rates.</p>'
              '</div></div></div></section>'
            '<script>(function(){var f=function(id){return document.getElementById(id);};'
            'function up(){var n=+f("i1").value,m=+f("i2").value,v=+f("i3").value,r=+f("i4").value;'
            'f("v1").textContent=n;f("v2").textContent=m+"%";'
            'f("v3").textContent=v.toLocaleString("en-IN");f("v4").textContent=r+"%";'
            'var missed=n*m/100,rec=missed*r/100,val=rec*v;'
            'f("cout").textContent="\\u20B9"+val.toLocaleString("en-IN",{maximumFractionDigits:0});'
            'f("cdetail").textContent="About "+Math.round(missed)+" enquiries a month are being missed or not followed up, worth roughly \\u20B9"+(missed*v).toLocaleString("en-IN",{maximumFractionDigits:0})+" in customer value.";'
            '}["i1","i2","i3","i4"].forEach(function(id){f(id).addEventListener("input",up);});up();})();</script>')

    body = (hero("Growth audit", "Find out where your business is losing customers.",
                 "Seven short steps — what you sell, how customers reach you, and what you think is broken. You get a recommended setup immediately, and a written finding from us after we read your customer journey.",
                 ctas=False, strap="About 2 minutes <s>·</s> No jargon <s>·</s> Written finding, not a brochure")
            + calc
            + '<section id="audit-form"><div class="wrap">'
            + shead("Diagnostic", "Where is your business losing customers?")
            + '<div class="audit"><div class="fprog"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>'
            + '<form id="audit" novalidate>' + steps_html
            + '<div class="fnav"><button class="btn" id="anext" type="button">Continue</button>'
              '<button class="btn ghost" id="aback" type="button">Back</button>'
              '<span class="small" id="acount">Step 1 of 7</span></div></form>'
            + result_html
            + '<noscript><p class="small">This diagnostic needs JavaScript. Email '
            + f'<a href="mailto:{EMAIL}" style="color:var(--ink-2)">{EMAIL}</a> with one line about your business instead.</p></noscript>'
            + '</div></div></section>'
            + faq_block([
                ("Is the audit really free?", "Yes. The diagnostic is instant, and the written finding that follows costs nothing and carries no obligation."),
                ("What do you do with my answers?", "We use them to prepare your finding and to reply to you. We do not sell them, rent them or add you to a marketing list."),
                ("Will you try to sell me everything?", "No. We recommend the single highest-impact fix first. It is entirely normal to start with one system and stop there."),
                ("How is the recommendation calculated?", "It is rule-based: the problem you pick maps to a recommended system. It is deliberately transparent — no black box, and we will explain any recommendation on a call."),
              ], "About the audit.", "FAQ"))
    doc = "\n".join([head("Free Growth Audit — Find Where Your Business Loses Customers | Westbridge",
                          "A free two-minute diagnostic for local businesses. Find where enquiries are lost and get a recommended customer-response system immediately.",
                          "/growth-audit/",
                          [service_ld("Free growth audit", "A diagnostic of where a business loses customers, returning a recommended system and a written finding."),
                           crumb_ld([("Home", "/"), ("Growth audit", "/growth-audit/")])],
                          "free growth audit, business revenue leak audit, lead loss diagnostic India"),
                    header(""), body, footer(), AUDIT_JS])
    write_page("/growth-audit/", doc)

# ---------------------------------------------------------------- CONTACT / PRIVACY / THANKYOU
def build_contact():
    body = (hero("Contact", "Tell us how customers find and contact you.",
                 "One line is enough to start. We will read your public customer journey and reply with a specific finding — not a brochure.",
                 ctas=False)
            + '<section><div class="wrap"><div class="grid g3">'
            + '<div class="card"><span class="k">Fastest</span><h3>Run the diagnostic</h3>'
              '<p>Seven questions, an instant recommended setup, and a written finding after we read your journey.</p>'
              '<a class="txtlink" href="/growth-audit/">Find my revenue leaks</a></div>'
            + f'<div class="card"><span class="k">Email</span><h3>Write to us directly</h3>'
              f'<p>One line about the business and, if you have one, your website. That is enough for us to begin.</p>'
              f'<a class="txtlink" href="mailto:{EMAIL}">{EMAIL}</a></div>'
            + f'<div class="card"><span class="k">Talk</span><h3>Prefer a conversation?</h3>'
              f'<p>We will arrange a short call — and come to it having already read your customer journey.</p>'
              f'<a class="txtlink" href="mailto:{EMAIL}?subject=Call%20request%20%E2%80%94%20Westbridge">Request a call</a></div>'
            + '</div>'
            + f'<p class="small" style="margin-top:30px">Westbridge · {CITY}, Telangana, India. We reply within one working day.</p>'
            + '</div></section>'
            + faq_block([
                ("What should I send?", "The business name, what it does, and the website or Google listing if there is one. Nothing else is required to begin."),
                ("What happens next?", "We read the public customer journey and reply with a specific finding: what we observed and what it is likely costing. No proposal unless you ask for one."),
                ("Am I committing to anything?", "No. The finding is free, with no obligation and no contract."),
              ], "Before you write.", "FAQ"))
    page("/contact/", "Contact Westbridge — Free Growth Audit and Customer Journey Review",
         "Contact Westbridge to request a free growth audit. Tell us how customers find and contact your business and we will reply with a specific finding.",
         body, ld=[crumb_ld([("Home", "/"), ("Contact", "/contact/")])], active="",
         keywords="contact Westbridge, free growth audit India, customer journey review Hyderabad")

def build_privacy():
    rows = [("What we collect", "Your name, business name, phone number, email address, and optionally your website, city, business type, how customers find and contact you, your biggest problem and an approximate customer value. We collect nothing automatically beyond ordinary web-server request logs."),
            ("Why we use it", "To prepare and send the finding you asked for, and to reply if you write back. We do not sell, rent or share it with third parties, and we do not add you to any marketing list."),
            ("Who sees it", "Us, and the form provider. Diagnostic submissions are delivered by email through FormSubmit, a form-to-email service, so your details pass through that provider on the way to us. Email is held in Google Workspace."),
            ("How long we keep it", "While the conversation is live, and up to twelve months afterwards for our own records. Ask us at any time and we will remove them sooner."),
            ("Your choices", f"Email {EMAIL} to see what we hold, correct it, delete it, or withdraw consent. We action requests within thirty days. If you are unhappy with our response you may complain to the Data Protection Board of India."),
            ("Cookies", "This site sets no analytics or advertising cookies. If analytics is added later, this notice and a consent prompt will be updated first."),
            ("AI systems", "Where we deploy AI assistants for clients, they answer only from content the business has approved, escalate to a human on request or uncertainty, and never invent an answer.")]
    inner = "".join(f'<div class="row"><b>{a}</b><span>{b}</span></div>' for a, b in rows)
    body = (hero("Privacy", "Privacy notice.", "Short, because it should be readable.",
                 ["This notice explains what happens to the details you submit through the diagnostic or send by email. It is written to be understood in one reading, in line with India's Digital Personal Data Protection Act, 2023."],
                 ctas=False)
            + f'<section><div class="wrap"><div class="dbox">{inner}</div>'
              f'<p class="small" style="margin-top:30px">Last updated {TODAY} · {BRAND}, {CITY}, India · '
              f'<a href="mailto:{EMAIL}" style="color:var(--ink-2)">{EMAIL}</a></p></div></section>')
    page("/privacy/", "Privacy Notice — How Westbridge Handles Your Data",
         "How Westbridge collects, uses and stores the details you submit through the growth audit, and how to have them removed.",
         body, ld=[crumb_ld([("Home", "/"), ("Privacy", "/privacy/")])], active="",
         keywords="Westbridge privacy notice, DPDP Act India, data protection")

def build_thanks():
    body = (hero("Received", "Thank you — your audit request is on its way.",
                 "We will read your public customer journey and reply within one working day with a specific finding: what we observed, and what it is likely costing.",
                 ctas=False)
            + faq_block([
                ("How long does it take?", "One working day to reply, usually a day or two to complete the read of your customer journey."),
                ("What will you send?", "A short written finding: the specific defects we observed and what they are likely costing. No proposal unless you ask for one."),
                ("Does it commit me to anything?", "No. The audit is free, with no obligation and no contract."),
              ], "What happens next.", "While you wait")
            + band("Want to look at the systems meanwhile?",
                   "Each one is shown with its problem, its workflow, and what happens when something goes wrong.",
                   primary=("See the systems", "/work/"), secondary=("How we work", "/how-it-works/")))
    page("/thank-you/", "Thank you — your audit request has been sent | Westbridge",
         "Your growth audit request has been received. Westbridge replies within one working day.",
         body, ld=[crumb_ld([("Home", "/"), ("Thank you", "/thank-you/")])], noindex=True, keywords="thank you")

# ---------------------------------------------------------------- static + sitemap
SITEMAP_PATHS = ["/", "/solutions/", "/work/", "/industries/", "/how-it-works/", "/about/",
                 "/growth-audit/", "/contact/", "/privacy/"]

def build_sitemap():
    paths = list(SITEMAP_PATHS) + [f'/work/{p["slug"]}/' for p in PROJECTS] + [f'/industries/{i["slug"]}/' for i in INDUSTRIES]
    urls = "".join(
        f'  <url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod>'
        f'<changefreq>{"weekly" if p == "/" else "monthly"}</changefreq>'
        f'<priority>{"1.0" if p == "/" else "0.8"}</priority></url>\n' for p in paths)
    write_page("/sitemap.xml",
               '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + urls + "</urlset>\n")
    return paths

def build_static():
    write_page("/style.css", CSS)
    write_page("/favicon.svg",
               '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0B1220"/>'
               '<rect x="15" y="15" width="15" height="15" rx="4" fill="#2563EB"/>'
               '<path d="M17 40h30M17 49h19" stroke="#F7F8FA" stroke-width="4" stroke-linecap="round"/></svg>')
    write_page("/robots.txt",
               "# Westbridge - robots.txt\n# All crawlers welcome, including AI answer engines.\n\n"
               "User-agent: *\nAllow: /\n\n"
               + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in
                         ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User",
                          "ClaudeBot", "Claude-Web", "Claude-SearchBot", "Google-Extended",
                          "Applebot-Extended", "CCBot", "Bingbot", "Amazonbot", "meta-externalagent"])
               + f"Sitemap: {BASE}/sitemap.xml\n")
    lines = [f"# {BRAND}", "",
             f"> {BRAND} finds where local and service businesses lose customers — missed calls, slow replies, "
             "unchased quotes, unrequested reviews — and builds the websites, AI response, booking, CRM and "
             f"follow-up systems that fix it. Based in {CITY}, India.", "",
             "## Key facts", f"- Contact: {EMAIL}", f"- Location: {CITY}, Telangana, India",
             "- Positioning: revenue-leak diagnosis, not an AI agency",
             "- Method: diagnose, design, build, launch, improve",
             "- Core offer: enquiry response, AI receptionist, WhatsApp automation, booking, CRM, follow-up, reviews, reactivation",
             "- Operator: Abhishek Singh, FCCA, MCSI — around twelve years in internal audit, risk and controls",
             "- Labelling rule: concept builds are labelled 'Concept Build' and never presented as client work. "
             "Outcomes are stated as 'Designed to improve', never as measured results.", "",
             "## What it fixes",
             "Local businesses lose enquiries because nothing acknowledges them immediately: booking buttons with no "
             "form behind them, enquiries answered only in business hours, manual confirmations with no reminder, and "
             "quotations never followed up. Westbridge installs one response layer across the channels the business "
             "already uses.", "", "## Systems"]
    lines += [f"- [{p['title']}]({BASE}/work/{p['slug']}/): {p['summary'][:110]}" for p in PROJECTS]
    lines += ["", "## Industries"]
    lines += [f"- [{i['name']}]({BASE}/industries/{i['slug']}/): {i['intro'][:100]}" for i in INDUSTRIES]
    lines += ["", "## Pages"]
    lines += [f"- [{t}]({BASE}{h})" for t, h in
              [("Home", "/"), ("Solutions", "/solutions/"), ("Work", "/work/"), ("Industries", "/industries/"),
               ("How it works", "/how-it-works/"), ("Growth audit", "/growth-audit/"),
               ("About", "/about/"), ("Contact", "/contact/"), ("Privacy", "/privacy/")]]
    lines += ["", "## Preferred citation",
              f'"{BRAND} finds where a local business is losing customers — typically a missed call, a slow reply or '
              'an unchased quotation — and builds the websites, AI response, booking and follow-up systems that fix it. '
              f'Based in {CITY}, India."']
    write_page("/llms.txt", "\n".join(lines) + "\n")

def main():
    build_home(); build_solutions(); build_work()
    for p in PROJECTS:
        build_project(p)
    build_industries()
    for i in INDUSTRIES:
        build_industry(i)
    build_how(); build_about(); build_audit(); build_contact(); build_privacy(); build_thanks()
    build_static()
    paths = build_sitemap()
    print(f"DONE - {len(paths)} sitemap URLs, last update {TODAY}")

if __name__ == "__main__":
    main()
