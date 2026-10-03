#!/usr/bin/env python3
"""Urbania group transport — pages. Run: python3 build_pages.py"""
import os, json, html, urllib.parse
from build_ui import (BASE, BRAND, PHONE, PHONE_HREF, PHONE_TXT, WHATSAPP, CITY, OUT, TODAY, YEAR, CSS,
                      NAV, head, header, footer, crumb_ld, faq_ld, service_ld,
                      hero, section, cta_band, faq_block, vehicle_panel, write_page, call_svg)
from build_planner import planner, PLANNER_CSS, PLANNER_JS, MODES

# Lead delivery. OWNER DECISION REQUIRED — see docs/OWNER_DECISIONS.md.
# Empty endpoint => the form composes a pre-filled email instead, so no lead is lost.
FORM_ENDPOINT = "/api/trip"   # same-origin backend endpoint (app/server.py). Falls back to WhatsApp if unreachable.
LEAD_EMAIL = "fca.abhi007@gmail.com"   # owner-supplied professional address; confirm/replace

def planner_blocks(preset=""):
    """Adaptive planner markup + its JS, with the delivery endpoint resolved."""
    mk = planner(preset).replace("%PHONE_HREF%", PHONE_HREF).replace("%PHONE%", PHONE)
    return mk + PLANNER_JS.replace("%WA%", WHATSAPP).replace("%ENDPOINT%", FORM_ENDPOINT)

AVAIL_NOTE = ("Availability is confirmed personally for each enquiry — this site does not show "
              "live availability or take instant bookings.")

def page(path, title, desc, body, ld=None, active="", noindex=False):
    # Telephone numbers must not wrap mid-number on narrow screens: display form uses &nbsp;.
    # Applied to the HTML body only — head() carries the JSON-LD, which must keep plain spaces.
    html_body = (header(active) + body + footer()).replace(PHONE, PHONE_TXT)
    doc = "\n".join([head(title, desc, path, ld, noindex), html_body])
    write_page(path, doc)

def breadcrumb(items):
    return ('<div class="wrap"><p class="small" style="padding-top:16px">'
            + " / ".join(f'<a href="{h}" style="color:var(--ink-3);text-decoration:none">{html.escape(t)}</a>'
                         for t, h in items) + '</p></div>')

def related_block(items, h2="Read next."):
    cards = "".join(
        f'<a class="card" href="{h}"><h3>{t}</h3><p>{d}</p>'
        f'<span class="txtlink" style="margin-top:14px">Read this</span></a>' for t, h, d in items)
    return (f'<section class="alt"><div class="wrap"><div class="shead"><h2>{h2}</h2></div>'
            f'<div class="grid g2">{cards}</div></div></section>')

# ------------------------------------------------------------------ shared FAQ pool
CORE_FAQ = [
 ("Can I hire a 17-seat Force Urbania for one day in Hyderabad?",
  "Yes — day hire is one of the trip types we quote for. Send the date, pickup point, the stops you want to make and the expected duration, and we will reply with a quotation. Availability is confirmed with the quotation."),
 ("What information should I provide to get a quotation?",
  "Travel date, pickup point, main destination or drop point, number of passengers, whether you need a few hours, a full day or multiple days, and an estimate of the distance or number of stops. If you are unsure about distance, select \u201cNot sure\u201d — we can work it out from your itinerary."),
 ("Can we provide our own itinerary?",
  "Yes. All the trips we quote are based on the customer's own plan. You choose the stops and the running order; we tell you what is practical for a single day and how the timing works."),
 ("Can we request multiple stops?",
  "Yes — multi-stop trips are a normal part of group travel. List the stops in the enquiry so the route and duration can be quoted accurately."),
 ("Does submitting the form confirm the booking?",
  "No. Submitting the form is a quotation enquiry. It does not confirm vehicle availability or create a booking. We reply with a quotation and confirm availability before anything is agreed."),
 ("How many passengers can travel?",
  "The vehicle is a 17-seat Force Urbania. Share your exact passenger count in the enquiry, particularly if the group includes children, so seating can be confirmed."),
 ("How much luggage can we carry?",
  "Luggage space depends on how many passengers are travelling and the size of the bags. Please share the number of passengers and an approximate luggage requirement (for example, number of large suitcases and cabin bags) so suitability can be confirmed for your trip rather than assumed."),
 ("How is the trip price calculated?",
  "A quotation is prepared for each enquiry based on the trip type, duration, distance or route, and the date. The rate depends on these details, so we quote rather than publish a single figure."),
 ("Is this suitable for airport groups?",
  "Yes. Group airport transfers are one of the main trip types we handle — for arrivals, departures or both. Provide flight timing and the number of passengers with luggage so the pickup can be planned."),
 ("Can the vehicle be used for wedding guest transfers?",
  "Yes. Wedding and event guest movement is a frequent use — hotel to venue, airport to hotel, or several pickups across a day. Send the schedule and the number of guests travelling together."),
 ("Do you provide packaged tours, guides or attraction tickets?",
  "No. We provide the vehicle and the driver for the journey you plan. Attraction tickets, guides, hotels and packaged tours are not part of the service."),
 ("Is availability guaranteed?",
  "No. " + AVAIL_NOTE),
 ("Can you handle outstation trips?",
  "Outstation trips depend on the permissions and operating arrangements that apply at the time of your enquiry. Tell us the route and dates and we will confirm whether we can quote for it."),
]

# ------------------------------------------------------------------ HOME
def build_home():
    facts = [
        "One 17-seat Force Urbania — a single vehicle, not a marketplace",
        "Quotation prepared for your actual itinerary",
        "Availability confirmed personally before anything is agreed",
        "Airport groups, weddings, corporate travel and day hire",
        "Your itinerary, not a fixed package",
        "Travelling as one group instead of coordinating several cabs",
    ]
    tick = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#116A7B" stroke-width="2.6" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
    facthtml = "".join(f'<div class="fact">{tick}<span>{f}</span></div>' for f in facts)
    body = (
        '<section class="hero"><div class="wrap">'
        '<span class="eyebrow">Group travel · ' + CITY + '</span>'
        '<h1>Get your group there together.</h1>'
        '<p class="lede" style="margin-top:16px;font-size:clamp(18px,1.9vw,21px)">17-seat Force Urbania hire in '
        'Hyderabad for groups of 10\u201317. Tell us the trip — airport run, wedding, outstation, day out or '
        'something custom — and we check what suits your group before sending a quotation.</p>'
        f'<div class="heroacts"><a class="btn ghost" href="{PHONE_HREF}">{call_svg()}&nbsp;Call {PHONE_TXT}</a></div>'
        '<p class="small" style="margin-top:14px">Quotation on request. Availability is confirmed personally — '
        'this site does not show live availability and does not take instant bookings.</p>'
        '</div></section>'
        + '<section style="padding-top:0"><div class="wrap">'
          '<div class="shead" style="margin-bottom:18px"><h2 style="font-size:clamp(19px,2.1vw,25px)">'
          'Plan your group trip</h2></div>'
          + planner_blocks("") + '</div></section>'
        + f'<section class="alt"><div class="wrap"><div class="facts">{facthtml}</div></div></section>'
        + section("Trip types", "What groups use the vehicle for.",
                  "Every trip is quoted from your own plan. These are the four situations that come up most often.",
                  '<div class="grid g2">'
                  '<a class="card" href="/airport-group-transfer-hyderabad/"><span class="tag">Airport</span>'
                  '<h3>Group airport transfers</h3><p>Arrivals, departures or both, with the group and their luggage in one vehicle instead of several taxis. Provide flight timing and passenger count.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Airport group transfers</span></p></a>'
                  '<a class="card" href="/wedding-transport-hyderabad/"><span class="tag">Weddings &amp; events</span>'
                  '<h3>Wedding and event transport</h3><p>Guest movement between hotels, venues and the airport across one day or several. Send the schedule and guest numbers.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Wedding &amp; event transport</span></p></a>'
                  '<a class="card" href="/corporate-group-transport-hyderabad/"><span class="tag">Corporate</span>'
                  '<h3>Corporate group travel</h3><p>Visiting teams, delegations and off-site groups moving between airport, hotel, office and venue on a schedule.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Corporate group transport</span></p></a>'
                  '<a class="card" href="/hyderabad-sightseeing-group-travel/"><span class="tag">Sightseeing &amp; day hire</span>'
                  '<h3>Sightseeing and day hire</h3><p>Full-day or multi-stop city travel using your own itinerary — you choose the stops and the running order.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Sightseeing &amp; custom trips</span></p></a>'
                  '</div>', alt=True)
        + section("How it works", "From enquiry to quotation, in four steps.",
                  "There is no booking engine here. A person reads your trip details and replies with a quotation.",
                  '<div class="steps">'
                  '<div class="stepc"><span class="n">01</span><div><h3>Send your trip details</h3>'
                  '<p>Date, pickup point, destination, passenger count and how long you need the vehicle. Use the form or call.</p></div></div>'
                  '<div class="stepc"><span class="n">02</span><div><h3>We review the itinerary</h3>'
                  '<p>If anything is unclear — distance, stop order, timing — we ask rather than assume it.</p></div></div>'
                  '<div class="stepc"><span class="n">03</span><div><h3>You receive a quotation</h3>'
                  '<p>A price for the trip you described, plus confirmation of whether the vehicle is free on that date.</p></div></div>'
                  '<div class="stepc"><span class="n">04</span><div><h3>Availability is confirmed</h3>'
                  '<p>Nothing is reserved until availability is confirmed with you. The enquiry itself does not hold the vehicle.</p></div></div>'
                  '</div>')
        + section("The vehicle", "A 17-seat Force Urbania.",
                  "One vehicle, used for pre-booked group trips. Knowing exactly which vehicle will arrive is the practical advantage of booking a single dedicated vehicle rather than a marketplace listing.",
                  '<div class="grid g3">'
                  '<div class="card"><h3>Seating</h3><p>17 seats in a single vehicle, so the whole group travels together and arrives together.</p></div>'
                  '<div class="card"><h3>Luggage</h3><p>Luggage capacity depends on passenger numbers and bag sizes. Share your passenger count and approximate luggage in the enquiry so suitability is confirmed for your trip rather than assumed.</p></div>'
                  '<div class="card"><h3>Driver and vehicle details</h3><p>Driver arrangements, permit, insurance and vehicle documentation are provided with your quotation so you know exactly what you are booking before you confirm.</p></div>'
                  '</div>'
                  '<!-- [VERIFY BEFORE PUBLISHING: seating layout, luggage capacity in practice, driver arrangement, '
                  'permit status, insurance status, vehicle fitness/compliance, vehicle year and model variant] -->',
                  alt=True)
        + section("Why one vehicle", "Why groups book a single vehicle rather than several cabs.",
                  "Beyond price, the practical difference is coordination.",
                  '<div class="grid g3">'
                  '<div class="card"><h3>One group, one vehicle</h3><p>Everyone travels together and arrives at the same time, which matters when a group is heading to one venue or one flight.</p></div>'
                  '<div class="card"><h3>One point of coordination</h3><p>A single itinerary and a single driver to deal with, instead of directing three or four vehicles to the same place.</p></div>'
                  '<div class="card"><h3>Multi-stop trips are workable</h3><p>Several pickups or stops in one day are practical when one vehicle is holding the whole plan.</p></div>'
                  '</div>')
        + section("Guides", "Before you enquire.",
                  "Short, practical pages answering the questions that come up most often.",
                  '<div class="grid g3">'
                  '<a class="card" href="/guides/force-urbania-vs-tempo-traveller/"><h3>Force Urbania vs Tempo Traveller</h3>'
                  '<p>How the two group vehicles compare, and how to decide which suits your group and route.</p></a>'
                  '<a class="card" href="/guides/group-vehicle-fit-guide/"><h3>Travelling with 10\u201317 people</h3>'
                  '<p>Working out what vehicle a group actually needs, including luggage and seating.</p></a>'
                  '<a class="card" href="/guides/wedding-guest-transport-planning/"><h3>Wedding guest transport</h3>'
                  '<p>Planning guest movement between hotels, venues and the airport without chaos.</p></a>'
                  '</div>', alt=True)
        + faq_block(CORE_FAQ)
        + cta_band()
    )
    page("/", "17-Seater Force Urbania Hire in Hyderabad | Group Travel",
         "Pre-booked private group transport in Hyderabad with a 17-seat Force Urbania — airport group transfers, weddings, corporate travel and custom day trips.",
         body,
         ld=[service_ld("17-seat Force Urbania hire and private group transport in Hyderabad",
                        "Pre-booked private group transport in Hyderabad using a 17-seat Force Urbania, for airport transfers, weddings and events, corporate travel, sightseeing and custom multi-stop trips. Quotation provided on request."),
             faq_ld(CORE_FAQ)],
         active="/")

# ------------------------------------------------------------------ SERVICE PAGES
def service_page(path, active, title, desc, ldname, lddesc, eyebrow, h1, sub, paras,
                 body_sections, faqs, crumb, related=None, preset=""):
    planner_html = ""
    if preset:
        planner_html = ('<section style="padding-top:0"><div class="wrap">'
                        '<div class="shead" style="margin-bottom:18px">'
                        '<h2 style="font-size:clamp(19px,2.1vw,25px)">Plan this trip</h2></div>'
                        + planner_blocks(preset) + '</div></section>')
    body = (breadcrumb(crumb)
            + hero(eyebrow, h1, sub, paras=list(paras) + [AVAIL_NOTE], ctas=True, extra=vehicle_panel())
            + planner_html
            + body_sections
            + (related_block(related) if related else "")
            + faq_block(faqs) + cta_band())
    page(path, title, desc, body,
         ld=[service_ld(ldname, lddesc), faq_ld(faqs), crumb_ld(crumb)],
         active=active)

def build_airport():
    faqs = [
     ("How should we plan a group airport transfer?",
      "Send the flight timing, the number of passengers, the pickup point and the drop point. If the group is arriving on one flight and leaving on another, tell us both and whether you need the vehicle to wait or return later."),
     ("Can you handle several pickups before the airport?",
      "Yes. Groups often gather from two or three addresses before a single run to the airport. List each pickup point and the number of passengers at each so the timing and route can be planned properly."),
     ("What luggage information do you need?",
      "The number of passengers and an approximate luggage requirement — for example how many large suitcases and how many cabin bags. Share this so suitability can be confirmed for your specific trip rather than assumed."),
     ("Do you track flights?",
      "Tell us your flight number and scheduled time. How disruptions are handled will be confirmed with your quotation, since it depends on the timing and arrangements for that day."),
     ("Can we book a one-way transfer only?",
      "Yes. One-way and return transfers are both quoted. Tell us which you need."),
     ("Can the vehicle wait for a delayed arrival?",
      "Waiting arrangements and any charges that apply are set out in your quotation so there are no unexpected additions on the day."),
     ("Is a group airport transfer suitable for an early-morning flight?",
      "Tell us the pickup time you need and we will confirm whether we can cover it for your date. Availability is confirmed per enquiry — do not assume it is available."),
    ]
    body_sections = (
        section("Planning", "What a group airport transfer involves.",
                "The vehicle is booked for your group and your timings. This is pre-booked private transport, not a shared shuttle and not an on-demand cab.",
                '<div class="grid g3">'
                '<div class="card"><h3>Arrivals</h3><p>The group is met and moved together — useful when several people arrive on the same flight with luggage.</p></div>'
                '<div class="card"><h3>Departures</h3><p>One pickup with enough capacity for everyone, planned around a single check-in deadline rather than several.</p></div>'
                '<div class="card"><h3>Both directions</h3><p>Arrival and departure can be quoted together, including multi-day trips where the vehicle is used in between.</p></div>'
                '<div class="card"><h3>Multiple pickups</h3><p>Gathering the group from more than one address before a single run to the airport.</p></div>'
                '<div class="card"><h3>Hotel and venue transfers</h3><p>Airport to hotel, hotel to venue, or between hotels for a multi-day group stay.</p></div>'
                '<div class="card"><h3>Return trip enquiries</h3><p>Tell us both legs at the time of enquiry so the whole plan is quoted once.</p></div>'
                '</div>', alt=True)
        + section("Information", "What to include in your enquiry.",
                  "The more precise the details, the more accurate the quotation.",
                  '<div class="grid g2"><div class="card"><h3>Give us</h3><ul>'
                  '<li>Travel date and required pickup time</li>'
                  '<li>Flight timing, and flight number if you have it</li>'
                  '<li>Pickup point (and any additional pickups)</li>'
                  '<li>Drop point — airport, hotel or venue</li>'
                  '<li>Number of passengers</li>'
                  '<li>Approximate luggage requirement</li>'
                  '<li>One-way or return</li></ul></div>'
                  '<div class="card"><h3>What happens next</h3><ul>'
                  '<li>We review the timings and the group size</li>'
                  '<li>We ask about anything unclear rather than assuming</li>'
                  '<li>You receive a quotation for the trip</li>'
                  '<li>Availability is confirmed with the quotation</li>'
                  '<li>Nothing is reserved until that confirmation</li></ul></div></div>')
        + '<section class="alt"><div class="wrap"><div class="notice">'
          '<span>&#9432;</span><div><b>This is a quotation enquiry.</b> Submitting your details does not confirm '
          'vehicle availability or create a booking. Airport pickup is not guaranteed until availability is '
          'confirmed with you.</div></div></div></section>'
    )
    service_page(
        "/airport-group-transfer-hyderabad/", "/airport-group-transfer-hyderabad/",
        "Group Airport Transfer Hyderabad | 17-Seater Force Urbania",
        "Group airport transfers in Hyderabad with a 17-seat Force Urbania. Send flight timing, pickup point, passenger count and luggage details to request a quotation.",
        "Group airport transfers in Hyderabad",
        "Pre-booked group airport transfers in Hyderabad using a 17-seat Force Urbania, for arrivals, departures and multiple pickups. Quotation on request.",
        "Airport group transfers · Hyderabad",
        "Group airport transfers in Hyderabad",
        "One vehicle for the whole group and their luggage, planned around your flight times.",
        ["Useful for groups arriving or departing together, for wedding parties flying in, and for corporate teams landing on the same flight. Send the timing and we will quote for the actual plan."],
        body_sections, faqs,
        [("Home", "/"), ("Airport group transfers", "/airport-group-transfer-hyderabad/")],
        related=[("Travelling with 10\u201317 people",
                  "/guides/group-vehicle-fit-guide/",
                  "The luggage question that breaks most airport runs, and how to check your group fits one vehicle.")],
        preset="airport")

def build_wedding():
    faqs = [
     ("How do we plan transport for wedding guests?",
      "Start with the schedule: which guests need to move, from where to where, on which day, and at what time. Send that list and the number of guests travelling together, and we will quote for the vehicle across those movements."),
     ("Can the vehicle do several trips in one day?",
      "Yes. Wedding days usually involve multiple movements — hotel to venue, venue to hotel, airport runs in between. These are planned as one duty so the vehicle is available across the day."),
     ("Can you do multiple pickups from different hotels?",
      "Yes. List each pickup point and how many guests are at each, and we can plan a sensible order."),
     ("Can you handle airport arrivals for guests?",
      "Yes, though guests arriving on different flights at different times may need separate arrangements. Send the flight details and we will tell you what is workable."),
     ("Is the vehicle available for multi-day wedding events?",
      "Multi-day enquiries are quoted for the whole period. Tell us each day's requirements so the quotation reflects the actual duty rather than a single trip."),
     ("Can we decorate the vehicle?",
      "Any decoration must not affect safety or the vehicle's condition, and arrangements are confirmed with your quotation."),
     ("What if our timings change on the day?",
      "Changes are handled as they arise, and any difference in duty duration or distance is reflected in the final billing terms set out in your quotation."),
    ]
    body_sections = (
        section("Planning", "The movements a wedding day usually needs.",
                "Weddings rarely need one trip. They need the same vehicle available across a schedule, which is what makes a single group vehicle practical.",
                '<div class="grid g3">'
                '<div class="card"><h3>Hotel to venue</h3><p>Moving a block of guests from their accommodation to the ceremony or reception.</p></div>'
                '<div class="card"><h3>Airport to hotel</h3><p>Collecting arriving guests, including several pickups across a day.</p></div>'
                '<div class="card"><h3>Family movements</h3><p>Moving immediate family between venues, homes and the venue on the day.</p></div>'
                '<div class="card"><h3>Multiple pickup points</h3><p>Guests spread across more than one hotel gathered in a planned order.</p></div>'
                '<div class="card"><h3>Multi-event schedules</h3><p>Mehendi, ceremony and reception on different days, each with its own movement plan.</p></div>'
                '<div class="card"><h3>Return transport</h3><p>Getting guests safely back at the end of the event, planned in advance rather than at midnight.</p></div>'
                '</div>', alt=True)
        + section("Information", "What to send us.",
                  "A simple list is enough — send it as it is and we will work out the sequencing.",
                  '<div class="grid g2"><div class="card"><h3>For each movement</h3><ul>'
                  '<li>Day and date</li><li>Pickup point and time</li><li>Drop point</li>'
                  '<li>Number of guests travelling together</li>'
                  '<li>Whether the vehicle should wait or return</li></ul></div>'
                  '<div class="card"><h3>What happens next</h3><ul>'
                  '<li>We map the movements into a practical schedule</li>'
                  '<li>We flag anything that will not work in one vehicle</li>'
                  '<li>You receive a quotation for the duty</li>'
                  '<li>Availability is confirmed with the quotation</li></ul></div></div>')
        + '<section class="alt"><div class="wrap"><div class="notice"><span>&#9432;</span><div>'
          '<b>What is not included.</b> We provide the vehicle and driver for the journeys you plan. '
          'Decoration packages, event coordination, guest management, guides, tickets and hotel arrangements '
          'are not part of this service.</div></div></div></section>'
    )
    service_page(
        "/wedding-transport-hyderabad/", "/wedding-transport-hyderabad/",
        "Wedding & Event Transport Hyderabad | 17-Seater Urbania",
        "Wedding and event guest transport in Hyderabad with a 17-seat Force Urbania — hotel-to-venue runs, airport pickups and multi-day schedules.",
        "Wedding and event guest transport in Hyderabad",
        "Pre-booked wedding and event guest transport in Hyderabad using a 17-seat Force Urbania, covering multiple movements, pickups and multi-day schedules. Quotation on request.",
        "Weddings &amp; events · Hyderabad",
        "Wedding and event guest transport in Hyderabad",
        "One vehicle, one schedule, for the movements a wedding day actually needs.",
        ["Send the guest movement list — days, pickup points, drop points and guest numbers — and we will quote for the vehicle across that schedule."],
        body_sections, faqs,
        [("Home", "/"), ("Wedding & event transport", "/wedding-transport-hyderabad/")],
        related=[("Planning wedding guest transport",
                  "/guides/wedding-guest-transport-planning/",
                  "How to build the movement list before you look for vehicles \u2014 and the failures to avoid.")],
        preset="wedding")

def build_corporate():
    faqs = [
     ("What corporate group movements do you handle?",
      "Visiting teams and delegations moving between the airport, hotel, office and event venues, conference transfers, off-site and team travel, and scheduled multi-stop days where several addresses are visited in one plan."),
     ("Can you handle a scheduled day with several stops?",
      "Yes. Send the running order and the timings and we will quote for the duty. If the schedule is unrealistic for one vehicle in one day, we will say so rather than accept it and under-deliver."),
     ("Do you provide GST invoices?",
      "Invoicing and any applicable tax treatment are confirmed in your quotation. Please tell us at the enquiry stage what your finance team requires."),
     ("Can we set up a repeat arrangement for visiting teams?",
      "Tell us the pattern — how often teams visit, the usual route and timings — and we can quote for recurring requirements."),
     ("Can the vehicle be used for an off-site or team outing?",
      "Yes. Day trips and off-site travel are quoted the same way as any other group trip, based on your itinerary and duration."),
     ("What about waiting time between meetings?",
      "If the vehicle needs to wait during the day, say so in the enquiry. Waiting arrangements and any charges are set out in the quotation."),
     ("Can we get a single quotation for a multi-day visit?",
      "Yes. Multi-day and multi-leg requirements are quoted together so the whole visit is covered in one document."),
    ]
    body_sections = (
        section("Requirements", "What corporate groups usually need.",
                "Corporate travel is the most schedule-driven use of the vehicle. The plan matters as much as the vehicle.",
                '<div class="grid g3">'
                '<div class="card"><h3>Visiting teams</h3><p>A team arriving together and moving as one group between the hotel, office and airport.</p></div>'
                '<div class="card"><h3>Delegations</h3><p>Formal visits where the group needs to arrive together and on time.</p></div>'
                '<div class="card"><h3>Airport, hotel and office</h3><p>Multi-leg movement across a day, planned as a single duty.</p></div>'
                '<div class="card"><h3>Conference movement</h3><p>Moving attendees between a hotel and a conference venue, including return trips.</p></div>'
                '<div class="card"><h3>Off-site and team travel</h3><p>Day outings and off-site sessions on your own itinerary.</p></div>'
                '<div class="card"><h3>Repeat requirements</h3><p>Regular visits that follow the same pattern and can be quoted as a standing arrangement.</p></div>'
                '</div>', alt=True)
        + section("Information", "What to send for a corporate enquiry.",
                  "Accuracy here saves time later, particularly for scheduled days.",
                  '<div class="grid g2"><div class="card"><h3>Include</h3><ul>'
                  '<li>Dates and, where relevant, the running order of the day</li>'
                  '<li>Each leg: pickup point, drop point and required time</li>'
                  '<li>Number of passengers (and whether it may change)</li>'
                  '<li>Whether the vehicle should wait between legs</li>'
                  '<li>Any invoicing or documentation your finance team requires</li></ul></div>'
                  '<div class="card"><h3>What happens next</h3><ul>'
                  '<li>We review the schedule for practicality in one vehicle</li>'
                  '<li>We raise anything that needs adjusting</li>'
                  '<li>You receive a quotation covering the legs described</li>'
                  '<li>Availability is confirmed with the quotation</li></ul></div></div>')
        + '<section class="alt"><div class="wrap"><div class="notice"><span>&#9432;</span><div>'
          '<b>Quotation enquiry only.</b> Submitting the form does not reserve the vehicle. '
          'Availability is confirmed with your quotation before anything is agreed.</div>'
          '<!-- [VERIFY BEFORE PUBLISHING: GST registration and whether tax invoices can be issued; '
          'permit status for the routes quoted; insurance cover details] -->'
          '</div></div></section>'
    )
    service_page(
        "/corporate-group-transport-hyderabad/", "/corporate-group-transport-hyderabad/",
        "Corporate Group Transport Hyderabad | 17-Seater Urbania",
        "Corporate group transport in Hyderabad with a 17-seat Force Urbania — visiting teams, delegations and scheduled multi-stop days.",
        "Corporate group transport in Hyderabad",
        "Pre-booked corporate group transport in Hyderabad using a 17-seat Force Urbania for visiting teams, delegations, conference movement and scheduled multi-stop days. Quotation on request.",
        "Corporate travel · Hyderabad",
        "Corporate group transport in Hyderabad",
        "For visiting teams and delegations that need to move together, on schedule.",
        ["Send the legs of the day — pickup points, drop points and times — and we will quote for the duty. If a schedule will not work in one vehicle, we will tell you before you commit."],
        body_sections, faqs,
        [("Home", "/"), ("Corporate group transport", "/corporate-group-transport-hyderabad/")],
        related=[("What vehicle fits a group of 10\u201317?",
                  "/guides/group-vehicle-fit-guide/",
                  "Confirm whether the delegation and their luggage fit one vehicle before you commit to a schedule.")],
        preset="corporate")

def build_sightseeing():
    faqs = [
     ("Can we design our own sightseeing route?",
      "Yes. You choose the places and the order. We look at the plan and tell you what is realistic in the time available, and how the day would run."),
     ("How does day hire work?",
      "You hire the vehicle for an agreed period rather than a fixed point-to-point trip. Tell us the date, the pickup point, the stops you want and roughly how many hours you need, and we will quote for the duty."),
     ("Do you provide a guide or tickets?",
      "No. We provide the vehicle and the driver for the journey. Guides, entry tickets and attraction bookings are not part of the service and must be arranged separately."),
     ("How many stops can we fit into a day?",
      "That depends on distance between stops and how long you want at each. Send your list and we will tell you honestly what fits and what would need a second day."),
     ("Can we change the plan during the day?",
      "Small changes are usually possible, but a materially different route or a longer duty affects the arrangement. Anything that changes the duty is reflected in the billing terms in your quotation."),
     ("Can the vehicle be booked for multiple days of sightseeing?",
      "Yes. Multi-day sightseeing is quoted for the whole period based on your itinerary."),
     ("Is outstation sightseeing possible?",
      "Outstation travel depends on the permissions and operating arrangements that apply at the time of the enquiry. Tell us the destination and dates and we will confirm whether we can quote."),
    ]
    body_sections = (
        section("Clarification", "Transport service, not a packaged tour.",
                "This distinction matters, so it is stated plainly.",
                '<div class="grid g2">'
                '<div class="card"><h3>What this is</h3><ul>'
                '<li>Vehicle hire with a driver for the period you book</li>'
                '<li>Your itinerary, sequenced practically</li>'
                '<li>Multi-stop travel within the day</li>'
                '<li>Transport between the places you choose</li></ul></div>'
                '<div class="card"><h3>What this is not</h3><ul>'
                '<li>Not a packaged tour or a fixed itinerary sold to you</li>'
                '<li>No guides</li>'
                '<li>No attraction entry tickets</li>'
                '<li>No hotel, meal or activity bookings</li>'
                '<li>No travel-agent services</li></ul></div></div>', alt=True)
        + section("Planning", "What to include in a day-hire enquiry.",
                  "A simple list of stops is enough to start.",
                  '<div class="grid g2"><div class="card"><h3>Include</h3><ul>'
                  '<li>Date of travel</li>'
                  '<li>Where the group is starting from</li>'
                  '<li>Where they need to be at the end</li>'
                  '<li>The stops you want, in the order you would like</li>'
                  '<li>Roughly how long you want at each stop</li>'
                  '<li>Number of passengers</li>'
                  '<li>How many hours or days you need the vehicle</li></ul></div>'
                  '<div class="card"><h3>How we respond</h3><ul>'
                  '<li>We check the route is practical for the time available</li>'
                  '<li>We flag stops that will not fit in one day</li>'
                  '<li>We suggest a running order if it helps</li>'
                  '<li>You receive a quotation for the duty</li>'
                  '<li>Availability is confirmed with the quotation</li></ul></div></div>')
    )
    service_page(
        "/hyderabad-sightseeing-group-travel/", "/hyderabad-sightseeing-group-travel/",
        "Hyderabad Sightseeing & Day Hire | 17-Seater Urbania",
        "Sightseeing and day hire in Hyderabad with a 17-seat Force Urbania. Bring your own itinerary — transport only, no guides or tickets.",
        "Sightseeing, day hire and custom multi-stop group travel in Hyderabad",
        "Pre-booked sightseeing and day hire in Hyderabad using a 17-seat Force Urbania, based on the customer's own itinerary. Transport service only. Quotation on request.",
        "Sightseeing &amp; day hire · Hyderabad",
        "Sightseeing, day hire and custom multi-stop group travel",
        "You choose the places and the order. We quote for the vehicle and tell you honestly what fits in a day.",
        ["This is a transport service, not a packaged tour. We quote for the vehicle and the driver; you plan the itinerary."],
        body_sections, faqs,
        [("Home", "/"), ("Sightseeing & day hire", "/hyderabad-sightseeing-group-travel/")],
        related=[("Force Urbania vs Tempo Traveller",
                  "/guides/force-urbania-vs-tempo-traveller/",
                  "How the two group vehicles compare, and the four questions that decide which suits your route.")],
        preset="sightseeing")

# ------------------------------------------------------------------ GUIDES
def build_guides_hub():
    body = (breadcrumb([("Home", "/"), ("Guides", "/guides/")])
            + hero("Guides", "Practical answers before you enquire.",
                   "Short pages about planning group travel in Hyderabad — written to help you work out whether a 17-seat vehicle suits your trip.",
                   ctas=False)
            + section("Guides", "Start here.",
                      "These answer the questions that come up most often in enquiries.",
                      '<div class="grid g3">'
                      '<a class="card" href="/guides/force-urbania-vs-tempo-traveller/"><h3>Force Urbania vs Tempo Traveller</h3>'
                      '<p>How the two group vehicles differ, and how to decide which one suits your group and route.</p></a>'
                      '<a class="card" href="/guides/group-vehicle-fit-guide/"><h3>Travelling with 10\u201317 people</h3>'
                      '<p>How to work out what vehicle a group needs, including seating and luggage.</p></a>'
                      '<a class="card" href="/guides/wedding-guest-transport-planning/"><h3>Wedding guest transport</h3>'
                      '<p>Planning guest movements between hotels, venues and the airport.</p></a>'
                      '</div>')
            + cta_band())
    page("/guides/", "Group Travel Guides | Hyderabad 17-Seater Urbania",
         "Practical guides to planning group travel in Hyderabad — Urbania vs Tempo Traveller, choosing a vehicle for 10-17 people, and wedding guest transport.",
         body, ld=[crumb_ld([("Home", "/"), ("Guides", "/guides/")])], active="/guides/")

def guide_page(path, title, desc, h1, sub, intro_paras, sections_html, faqs, crumb,
               related=None):
    body = (breadcrumb(crumb)
            + hero("Guide", h1, sub, paras=intro_paras, ctas=False)
            + sections_html
            + (related_block(related, "Related reading and next steps.") if related else "")
            + faq_block(faqs, h2="Related questions.") + cta_band())
    page(path, title, desc, body, ld=[faq_ld(faqs), crumb_ld(crumb)], active="/guides/")

def build_guide_urbania_vs_tempo():
    secs = (
        section("Comparison", "How the two vehicles are usually compared.",
                "Both are used for group travel in India. The right choice depends on your group size, luggage and how long you are travelling.",
                '<div class="grid g2">'
        '<div class="card"><h3>Force Urbania</h3><ul>'
        '<li>A 17-seat group vehicle with a monocoque body and a more car-like ride</li>'
        '<li>Useful where the group is large and comfort over a longer day matters</li>'
        '<li>Suited to airport groups, wedding movements and full-day itineraries</li>'
        '<li>Luggage capacity depends on passenger numbers — always confirm for your trip</li>'
        '</ul><p style="margin-top:14px" class="small">The vehicle offered here is a 17-seat Force Urbania.</p></div>'
        '<div class="card"><h3>Tempo Traveller</h3><ul>'
        '<li>The long-established group vehicle in India, available in several seating layouts</li>'
        '<li>Often easier to find at short notice because the market is larger</li>'
        '<li>Comfort and specification vary significantly between individual vehicles</li>'
        '<li>Suitable for similar trip types — airports, weddings, day trips</li>'
        '</ul><p style="margin-top:14px" class="small">We do not operate a Tempo Traveller, so this is general context rather than a sales comparison.</p></div>'
        '</div>')
        + section("Deciding", "How to decide which one you need.",
                  "Four questions settle it in most cases.",
                  '<div class="steps">'
                  '<div class="stepc"><span class="n">01</span><div><h3>How many are travelling?</h3>'
                  '<p>Count adults and children. If the group is 14\u201317, a 17-seat vehicle fits with little margin; if it is under about 12 you have more choice.</p></div></div>'
                  '<div class="stepc"><span class="n">02</span><div><h3>How much luggage is there?</h3>'
                  '<p>Luggage, not passenger count, is usually what breaks a group plan. Airport runs with large suitcases are the common failure case: a full vehicle of people and a full set of large bags may not both fit.</p></div></div>'
                  '<div class="stepc"><span class="n">03</span><div><h3>How long is the journey?</h3>'
                  '<p>A short transfer tolerates a basic vehicle. A full day of multi-stop travel makes ride quality and seating space matter more.</p></div></div>'
                  '<div class="stepc"><span class="n">04</span><div><h3>Do you want one vehicle or several?</h3>'
                  '<p>One vehicle keeps the group together and gives you a single itinerary to manage. Several vehicles are more flexible on pickup points but harder to coordinate.</p></div></div>'
                  '</div>', alt=True)
    )
    faqs = [
     ("Is a Force Urbania bigger than a Tempo Traveller?",
      "Both are group vehicles and both are commonly configured with similar seating counts. The practical differences are in body construction, ride quality and the specification of the individual vehicle, rather than the category itself. Confirm the exact seating layout of any vehicle you are quoted."),
     ("How many people can travel in a 17-seat Urbania?",
      "The vehicle offered here has 17 seats. Share your exact passenger count, including children, so seating can be confirmed for your group."),
     ("Can a group of 17 travel with luggage?",
      "Not necessarily with a full set of large suitcases as well. Luggage capacity depends on the number of passengers and the size of the bags, so share both in your enquiry and suitability will be confirmed for your trip rather than assumed."),
     ("Which is more comfortable for a long day trip?",
      "That depends on the individual vehicle rather than the category. Ask what specifically is being offered for your date, including the vehicle's age and condition."),
     ("Which is cheaper?",
      "Price depends on the trip, the duration, the distance and the date rather than on the vehicle category alone. A quotation for your actual itinerary is the only meaningful comparison."),
    ]
    guide_page("/guides/force-urbania-vs-tempo-traveller/",
               "Force Urbania vs Tempo Traveller | Group Travel Hyderabad",
               "How the Force Urbania and Tempo Traveller compare for group travel in Hyderabad, and the four questions that decide which suits your group and route.",
               "Force Urbania vs Tempo Traveller for group travel",
               "An honest comparison, and how to decide for your own group.",
               ["Both vehicles are widely used for group travel in India. The choice usually comes down to group size, luggage and how long you are on the road — not to the badge on the front."],
               secs, faqs,
               [("Home", "/"), ("Guides", "/guides/"),
                ("Urbania vs Tempo Traveller", "/guides/force-urbania-vs-tempo-traveller/")],
               related=[("What vehicle fits a group of 10\u201317?",
                         "/guides/group-vehicle-fit-guide/",
                         "Work out seating and luggage before you start comparing vehicles."),
                        ("Sightseeing and day hire",
                         "/hyderabad-sightseeing-group-travel/",
                         "Full-day and multi-stop trips on your own itinerary.")])

def build_guide_fit():
    secs = (
        section("Working it out", "Start with people, then luggage, then time.",
                "Group size is the easy part. Luggage and duration are what actually decide whether a plan works.",
                '<div class="grid g3">'
        '<div class="card"><h3>Under 10 people</h3><p>A large SUV or two cabs may be more economical. A 17-seat vehicle is not usually necessary unless luggage is heavy or you want everyone together.</p></div>'
        '<div class="card"><h3>10\u201313 people</h3><p>A group vehicle works comfortably and leaves room for luggage. This is often the most straightforward range.</p></div>'
        '<div class="card"><h3>14\u201317 people</h3><p>The vehicle is close to full. Luggage becomes the deciding factor, particularly for airport runs with large suitcases.</p></div>'
        '</div>')
        + section("The luggage trap", "Why luggage, not seats, breaks group plans.",
                  "A vehicle that seats 17 people does not automatically carry 17 people and their holiday luggage at the same time. This is the most common misunderstanding in group transport, and the one most likely to cause a problem on the day.",
                  '<div class="grid g2">'
                  '<div class="card"><h3>What to tell us</h3><ul>'
                  '<li>Number of passengers, including children</li>'
                  '<li>How many large suitcases</li>'
                  '<li>How many cabin or hand bags</li>'
                  '<li>Any bulky items such as a pram or wheelchair</li></ul></div>'
                  '<div class="card"><h3>Why it matters</h3><ul>'
                  '<li>Airport runs with full-size luggage are the hardest case</li>'
                  '<li>Wedding groups often travel with extra bags and garments</li>'
                  '<li>Multi-day trips carry more luggage than day trips</li>'
                  '<li>Getting it wrong means a decision on the day, under time pressure</li></ul></div></div>', alt=True)
        + section("Time", "How long the vehicle is needed.",
                  "Duration changes the shape of the quotation, so it is worth being clear about it.",
                  '<div class="grid g3">'
                  '<div class="card"><h3>A few hours</h3><p>A transfer or a short errand run. Quoted for the duty rather than the day.</p></div>'
                  '<div class="card"><h3>A full day</h3><p>Day hire for sightseeing or a wedding schedule with multiple movements.</p></div>'
                  '<div class="card"><h3>Multiple days</h3><p>Quoted for the whole period, with each day\u2019s requirements stated.</p></div>'
                  '</div>')
    )
    faqs = [
     ("What vehicle do I need for 15 people in Hyderabad?",
      "A 17-seat group vehicle is the usual answer, but confirm the luggage position as well as the passenger count. Fifteen passengers with a full set of large suitcases is a different requirement from fifteen passengers with hand baggage."),
     ("Can 15 people with luggage fit in an Urbania?",
      "It depends entirely on the luggage. Share the number of passengers and how many large and cabin bags there are, and suitability will be confirmed for your specific trip rather than assumed."),
     ("Should a group use one 17-seater or multiple cabs?",
      "One vehicle keeps the group together and gives you a single itinerary and a single driver to deal with. Multiple cabs can be more flexible for pickups spread across the city. If the group is larger than the vehicle capacity, or luggage is heavy, multiple vehicles may be the only workable option."),
     ("How many people can travel in a 17-seat vehicle?",
      "Seventeen seats, subject to the exact seating layout and configuration. Confirm your passenger count in the enquiry."),
     ("What if we are more than 17 people?",
      "Then a single 17-seat vehicle will not carry the whole group. Tell us the total number and we will be honest about whether it can be covered at all."),
    ]
    guide_page("/guides/group-vehicle-fit-guide/",
               "What Vehicle for 10\u201317 People? | Hyderabad Group Travel",
               "How to work out what vehicle a group of 10 to 17 people needs in Hyderabad, including the luggage question that most group travel plans get wrong.",
               "Travelling with 10\u201317 people: what vehicle do you need?",
               "Group size is the easy part. Luggage and duration decide whether a plan actually works.",
               ["If you are moving a group in Hyderabad, this page is meant to help you work out the requirement before you start asking for prices."],
               secs, faqs,
               [("Home", "/"), ("Guides", "/guides/"), ("Vehicle fit guide", "/guides/group-vehicle-fit-guide/")],
               related=[("Force Urbania vs Tempo Traveller",
                         "/guides/force-urbania-vs-tempo-traveller/",
                         "How the two group vehicles compare, and how to choose between them."),
                        ("Group airport transfers",
                         "/airport-group-transfer-hyderabad/",
                         "Planning an airport run for a group travelling with luggage.")])

def build_guide_wedding():
    secs = (
        section("Planning", "Build the movement list before you look for vehicles.",
                "Wedding transport goes wrong when it is planned as a single trip rather than a schedule.",
                '<div class="steps">'
        '<div class="stepc"><span class="n">01</span><div><h3>List every movement</h3>'
        '<p>Who is moving, from where, to where, on which day and at what time. A simple table is enough.</p></div></div>'
        '<div class="stepc"><span class="n">02</span><div><h3>Group guests by movement, not by relationship</h3>'
        '<p>Guests staying at the same hotel and attending the same event can travel together. Grouping guests by where they are rather than by family makes the plan far simpler.</p></div></div>'
        '<div class="stepc"><span class="n">03</span><div><h3>Decide what needs the vehicle to wait</h3>'
        '<p>Some movements need the vehicle to stay; others need it to return later. Both change the duty and therefore the quotation.</p></div></div>'
        '<div class="stepc"><span class="n">04</span><div><h3>Plan the returns in advance</h3>'
        '<p>The end of an event is the hardest time to improvise transport. Agree the return plan before the day, not during it.</p></div></div>'
        '</div>')
        + section("Common problems", "Where wedding transport usually breaks down.",
                  "These are the recurring issues, and most are avoidable with a clearer list at the enquiry stage.",
                  '<div class="grid g3">'
                  '<div class="card"><h3>Airport arrivals spread across flights</h3><p>Guests on different flights at different times may not be coverable in one vehicle movement. Send the flight details early.</p></div>'
                  '<div class="card"><h3>Guest numbers changing late</h3><p>Numbers often move. Tell us the expected range so the plan does not need rebuilding a day before.</p></div>'
                  '<div class="card"><h3>Luggage and garments</h3><p>Wedding groups travel with more than usual. Mention it, since it affects fit.</p></div>'
                  '</div>', alt=True)
        + section("Scope", "What a transport provider does and does not do.",
                  "Being clear about this avoids disappointment on the day.",
                  '<div class="grid g2"><div class="card"><h3>Provided</h3><ul>'
                  '<li>The vehicle and the driver for the journeys you plan</li>'
                  '<li>Multiple movements across a day, planned together</li>'
                  '<li>Multi-day arrangements quoted as one duty</li></ul></div>'
                  '<div class="card"><h3>Not provided</h3><ul>'
                  '<li>Guest list management or coordination</li>'
                  '<li>Event planning or on-site coordination</li>'
                  '<li>Decoration, catering or venue arrangements</li>'
                  '<li>Guides or tickets</li></ul></div></div>')
    )
    faqs = [
     ("How far in advance should wedding transport be arranged?",
      "As early as the movement list is known, particularly for dates in peak season. Availability is confirmed per enquiry, so it is worth asking before the plan is fixed."),
     ("Can one vehicle cover all the guest movements?",
      "Only if the movements do not overlap. If two groups need to move at the same time, one vehicle cannot be in two places. Tell us the full list and we will say honestly what a single vehicle can cover."),
     ("What if guests arrive on different flights?",
      "That usually requires separate movements rather than one. Send the flight details and we will tell you what is workable."),
     ("Can the vehicle stay at the venue all day?",
      "A vehicle can be hired for the duty, but it cannot be in two places. Waiting arrangements and any charges are set out in your quotation."),
    ]
    guide_page("/guides/wedding-guest-transport-planning/",
               "How to Arrange Transport for Wedding Guests in Hyderabad",
               "A practical approach to planning wedding guest transport in Hyderabad — building the movement list, grouping guests and avoiding the common failures.",
               "How to arrange transport for wedding guests in Hyderabad",
               "Build the movement list first. Vehicles are the easy part.",
               ["Wedding transport is a scheduling problem, not a vehicle problem. Get the schedule right and the vehicle follows."],
               secs, faqs,
               [("Home", "/"), ("Guides", "/guides/"),
                ("Wedding guest transport", "/guides/wedding-guest-transport-planning/")],
               related=[("Wedding &amp; event transport",
                         "/wedding-transport-hyderabad/",
                         "How we quote guest movement across a wedding schedule."),
                        ("What vehicle fits a group of 10\u201317?",
                         "/guides/group-vehicle-fit-guide/",
                         "Seating and luggage, checked before the day rather than on it.")])

# ------------------------------------------------------------------ QUOTE FORM
TRIP_TYPES = ["Airport Transfer", "Wedding / Event", "Corporate", "Sightseeing / Day Hire",
              "Custom Group Trip", "Other"]
DUTY = ["A few hours", "Full day", "Multiple days", "Not sure"]

def quote_form():
    rt = "".join(f'<label><input type="radio" name="trip_type" value="{t}"{" required" if i==0 else ""}>{t}</label>'
                 for i, t in enumerate(TRIP_TYPES))
    dt = "".join(f'<label><input type="radio" name="duty" value="{t}"{" required" if i==0 else ""}>{t}</label>'
                 for i, t in enumerate(DUTY))
    return f'''<form class="form" id="quoteform" novalidate>
  <fieldset class="fieldset">
    <legend>Trip type *</legend>
    <div class="radios" role="radiogroup" aria-label="Trip type">{rt}</div>
    <p class="err" id="err-trip_type">Please choose a trip type.</p>
  </fieldset>

  <div class="frow" style="margin-top:20px">
    <label>Travel date *<input type="date" name="date" required></label>
    <label>Passenger count *<input type="number" name="passengers" min="1" max="17" inputmode="numeric" required
      placeholder="Number of people travelling"><span class="hint">The vehicle has 17 seats.</span></label>
  </div>
  <div class="frow">
    <label>Pickup point *<input type="text" name="pickup" required placeholder="Area, hotel or address"></label>
    <label>Drop point / main destination *<input type="text" name="drop" required placeholder="Where the group is going"></label>
  </div>

  <fieldset class="fieldset" style="margin-top:8px">
    <legend>Duty duration *</legend>
    <div class="radios" role="radiogroup" aria-label="Duty duration">{dt}</div>
    <p class="err" id="err-duty">Please choose a duration.</p>
  </fieldset>

  <div class="frow" style="margin-top:20px">
    <label>Approximate hours or number of days<input type="text" name="duration" placeholder="e.g. 8 hours, or 3 days"></label>
    <label>Estimated kilometres
      <select name="km">
        <option value="Not sure">Not sure</option>
        <option value="Under 50 km">Under 50 km</option>
        <option value="50-100 km">50\u2013100 km</option>
        <option value="100-250 km">100\u2013250 km</option>
        <option value="250-500 km">250\u2013500 km</option>
        <option value="Over 500 km">Over 500 km</option>
      </select><span class="hint">Choose \u201cNot sure\u201d if you would rather we work it out.</span></label>
  </div>

  <label>Number of stops or a short note about the route
    <textarea name="notes" placeholder="Optional. List any extra stops, flight timing, luggage requirement, or anything that affects the plan."></textarea></label>

  <div class="frow">
    <label>Your name *<input type="text" name="name" required autocomplete="name"></label>
    <label>Phone number *<input type="tel" name="phone" required autocomplete="tel" placeholder="We reply by phone or WhatsApp"></label>
  </div>
  <label>Email <span class="hint">(optional — include it if you would prefer a written quotation)</span>
    <input type="email" name="email" autocomplete="email"></label>

  <input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true"
         style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">

  <div class="submit-note">
    <b>This is a quotation enquiry.</b> Submitting this form does not confirm vehicle availability and does not
    create a booking. We reply with a quotation and confirm availability before anything is agreed.
  </div>

  <div style="margin-top:20px">
    <button class="btn wide" type="submit" id="qsubmit">REQUEST MY TRIP QUOTE</button>
    <p class="small" style="margin-top:12px;text-align:center">Prefer to talk? Call
      <a href="{PHONE_HREF}" style="color:var(--accent);font-weight:600">{PHONE}</a></p>
  </div>
</form>
<div id="qresult" tabindex="-1" aria-live="polite"></div>'''

QUOTE_JS = """<script>
(function(){
  var f=document.getElementById('quoteform'); if(!f) return;
  var out=document.getElementById('qresult');
  function groupInvalid(name){
    var g=f.querySelectorAll('input[name="'+name+'"]');
    return !Array.prototype.some.call(g,function(x){return x.checked;});
  }
  function mark(el,bad){
    var l=el.closest('label'); if(l) l.classList.toggle('bad',bad);
    el.setAttribute('aria-invalid',bad?'true':'false');
  }
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=false;
    if(groupInvalid('trip_type')){ document.getElementById('err-trip_type').style.display='block'; bad=true; }
    else { document.getElementById('err-trip_type').style.display='none'; }
    if(groupInvalid('duty')){ document.getElementById('err-duty').style.display='block'; bad=true; }
    else { document.getElementById('err-duty').style.display='none'; }
    Array.prototype.forEach.call(f.querySelectorAll('input[required],select[required],textarea[required]'),function(el){
      var empty=!el.value || !el.value.trim();
      mark(el,empty); if(empty) bad=true;
    });
    var em=f.querySelector('input[name=email]');
    if(em.value.trim() && !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(em.value.trim())){ mark(em,true); bad=true; }
    else if(em.value.trim()){ mark(em,false); }
    if(bad){
      var first=f.querySelector('label.bad input, label.bad select, label.bad textarea');
      if(first){ first.focus(); first.scrollIntoView({block:'center',behavior:'smooth'}); }
      return;
    }
    var hp=f.querySelector('input[name=_hp]');
    if(hp && hp.value){ return; }
    var fd=new FormData(f), o={};
    fd.forEach(function(v,k){ if(k!=='_hp') o[k]=o[k]?o[k]+', '+v:v; });
    o.source_page=location.pathname;
    o.submitted_at=new Date().toISOString();
    var q=new URLSearchParams(location.search);
    ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'].forEach(function(k){
      if(q.get(k)) o[k]=q.get(k);
    });
    var lines=Object.keys(o).map(function(k){return k.replace(/_/g,' ')+': '+o[k];}).join('\\n');
    var ep="%ENDPOINT%", WA="%WA%";
    var waLink = WA ? ('https://wa.me/'+WA+'?text='+encodeURIComponent(lines)) : '';
    function done(sent){
      f.style.display='none';
      out.innerHTML='<div class="form" style="margin-top:24px"><h3>'
        +(sent?'Your trip details have been sent.':'Almost done — one tap to send.')
        +'</h3>'
        +'<p class="lede" style="margin-top:12px">This is a quotation enquiry and does not confirm vehicle '
        +'availability or a booking. We review the details and reply with a quotation.</p>'
        +'<p class="lede" style="margin-top:12px">'
        +(WA?('If WhatsApp did not open, <a href="'+waLink+'" target="_blank" rel="noopener" '
              +'style="color:var(--accent);font-weight:600">tap here to send your details</a>, or call ')
            :'Call ')
        +'<a href="%PHONE_HREF%" style="color:var(--accent);font-weight:600">%PHONE%</a>.</p>'
        +'<p class="small" style="margin-top:16px">A copy of the details being sent:</p>'
        +'<pre style="white-space:pre-wrap;background:var(--alt);border:1px solid var(--line);border-radius:10px;'
        +'padding:16px;font-size:13.5px" id="qsummary"></pre></div>';
      document.getElementById('qsummary').textContent=lines;
      out.focus(); out.scrollIntoView({block:'start',behavior:'smooth'});
    }
    if(ep){
      fetch(ep,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
        body:JSON.stringify(o)}).then(function(){ done(true); })
        .catch(function(){ if(waLink){ window.open(waLink,'_blank'); } done(false); });
    } else if(WA){
      window.open(waLink,'_blank');
      done(true);
    } else {
      var subject='Trip quote request — '+o['trip_type']+' — '+(o['date']||'');
      window.location.href='mailto:%EMAIL%?subject='+encodeURIComponent(subject)+
        '&body='+encodeURIComponent(lines);
      done(true);
    }
  });
})();
</script>"""

def build_quote():
    body = (breadcrumb([("Home", "/"), ("Request a trip quote", "/request-quote/")])
            + hero("Request a trip quote",
                   "Request a trip quote",
                   "Share your date, pickup point, destination, passenger count and how long you need the vehicle. We reply with a quotation for the trip you described.",
                   paras=[AVAIL_NOTE], ctas=False)
            + section("Trip details", "Tell us about the trip.",
                      "Fields marked * are needed to quote accurately. Everything else helps us get it right first time.",
                      quote_form())
            + section("What happens next", "Four steps after you submit.",
                      "No automated booking. A person reviews the details and comes back to you.",
                      '<div class="steps">'
                      '<div class="stepc"><span class="n">01</span><div><h3>We review your trip details</h3>'
                      '<p>Route, timing, group size and duration — and we check the plan is realistic in one vehicle.</p></div></div>'
                      '<div class="stepc"><span class="n">02</span><div><h3>We ask if anything is unclear</h3>'
                      '<p>Distance, stop order or timing. We would rather ask than quote on a guess.</p></div></div>'
                      '<div class="stepc"><span class="n">03</span><div><h3>You receive a quotation</h3>'
                      '<p>A price for the trip described, with the terms that apply.</p></div></div>'
                      '<div class="stepc"><span class="n">04</span><div><h3>Availability is confirmed</h3>'
                      '<p>Nothing is held or reserved until availability is confirmed with you.</p></div></div>'
                      '</div>', alt=True)
            + faq_block([
                ("Does submitting the form book the vehicle?",
                 "No. It is a quotation enquiry. It does not confirm availability and does not create a booking. We reply with a quotation and confirm availability before anything is agreed."),
                ("What if I do not know the distance?",
                 "Select \u201cNot sure\u201d and describe the stops instead. We can work out the practical distance from your itinerary."),
                ("How quickly will I hear back?",
                 "We aim to respond promptly, but we do not publish a guaranteed response time because it depends on enquiry volume. If your trip is time-critical, call " + PHONE + "."),
                ("Can I request a quotation for several dates?",
                 "Yes. Note the alternative dates in the notes field and we will quote for each."),
                ("Do you store my details?",
                 "Your trip details are used to prepare your quotation and reply to you. See the privacy page for how information is handled."),
              ], "About the enquiry.")
            + cta_band("Prefer to speak to someone?",
                       "Call and describe the trip. If you already have the details to hand, the form takes about two minutes."))
    js = (QUOTE_JS.replace("%ENDPOINT%", FORM_ENDPOINT).replace("%EMAIL%", LEAD_EMAIL)
          .replace("%PHONE_HREF%", PHONE_HREF).replace("%PHONE%", PHONE)
          .replace("%WA%", WHATSAPP))
    doc = "\n".join([head("Request a Trip Quote | 17-Seater Group Transport Hyderabad",
                          "Request a quotation for a 17-seat Force Urbania in Hyderabad. Send your date, pickup, destination, passenger count and duration. An enquiry, not a booking.",
                          "/request-quote/",
                          [service_ld("Trip quotation request",
                                      "Quotation request for pre-booked private group transport in Hyderabad using a 17-seat Force Urbania."),
                           crumb_ld([("Home", "/"), ("Request a trip quote", "/request-quote/")])]),
                    (header("/request-quote/") + body + footer()).replace(PHONE, PHONE_TXT), js])
    write_page("/request-quote/", doc)

# ------------------------------------------------------------------ UTILITY
def build_about():
    body = (breadcrumb([("Home", "/"), ("About", "/about/")])
            + hero("About", "Pre-booked private group transport in Hyderabad.",
                   "A single 17-seat Force Urbania, offered for group trips that are planned in advance.",
                   paras=["This is not a marketplace, an aggregator or an on-demand cab service. One vehicle is offered, "
                          "and every trip is quoted individually from the customer's own itinerary."], ctas=True)
            + section("How we work", "Straightforward, and stated plainly.",
                      "Because there is one vehicle, the honest position is simple.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>What you can expect</h3><ul>'
                      '<li>Your trip details read by a person, not an algorithm</li>'
                      '<li>A quotation based on your actual itinerary</li>'
                      '<li>Availability confirmed before anything is agreed</li>'
                      '<li>An honest answer if one vehicle cannot cover your plan</li></ul></div>'
                      '<div class="card"><h3>What we do not do</h3><ul>'
                      '<li>Instant booking or live availability display</li>'
                      '<li>Packaged tours, guides or attraction tickets</li>'
                      '<li>Multiple vehicle types or a fleet to choose from</li>'
                      '<li>Claims we cannot support</li></ul></div></div>')
            + section("Vehicle", "The vehicle.",
                      "One 17-seat Force Urbania, used for pre-booked group trips.",
                      '<div class="grid g2"><div>' + vehicle_panel() + '</div>'
                      '<div class="card"><h3>Details available on request</h3>'
                      '<p>Vehicle documentation and the practical details of the arrangement — driver, luggage capacity for '
                      'your group, and the terms that apply — are provided with your quotation so you know exactly what '
                      'you are booking.</p>'
                      '<p style="margin-top:14px" class="small">Written this way deliberately: details that depend on '
                      'your specific trip are confirmed rather than assumed.</p></div></div>', alt=True)
            + faq_block([
                ("Is this a vehicle rental company?",
                 "This is pre-booked private group transport — the vehicle is provided with a driver for the journeys agreed in your quotation. It is not self-drive hire and not a marketplace."),
                ("How many vehicles are available?",
                 "One. Because there is a single vehicle, availability is confirmed per enquiry rather than guaranteed."),
                ("Do you operate outside Hyderabad?",
                 "Outstation travel depends on the permissions and operating arrangements that apply at the time. Tell us the route and dates and we will confirm whether we can quote."),
              ], "About the service.")
            + cta_band())
    page("/about/", "About | 17-Seater Force Urbania Group Transport Hyderabad",
         "This pre-booked private group transport service in Hyderabad offers one 17-seat Force Urbania, quoted per itinerary, with availability confirmed first.",
         body, ld=[crumb_ld([("Home", "/"), ("About", "/about/")])], active="/about/")

def build_contact():
    body = (breadcrumb([("Home", "/"), ("Contact", "/contact/")])
            + hero("Contact", "Get in touch about your trip.",
                   "Call to discuss the trip, or send the details through the quotation form.",
                   ctas=False)
            + section("Contact", "How to reach us.",
                      "WhatsApp, phone, or the quotation form. The form sends your trip details straight to WhatsApp in one tap.",
                      '<div class="grid g3">'
                      f'<div class="card"><span class="tag">WhatsApp</span><h3>Message us</h3>'
                      f'<p>The fastest route. Send the date, route, passenger count and duration and we will reply with a quotation.</p>'
                      f'<p style="margin-top:16px"><a class="txtlink" href="https://wa.me/{WHATSAPP}">WhatsApp +91 91821 26104</a></p>'
                      f'<!-- [VERIFY BEFORE PUBLISHING: the WhatsApp Business number (+91 91821 26104) differs from the '
                      f'call number published in the brief (+91 62020 66104). Confirm which is which, and note the '
                      f'WhatsApp Business profile shows Supaul, Bihar rather than Hyderabad.] --></div>'
                      f'<div class="card"><span class="tag">Phone</span><h3>Call</h3>'
                      f'<p>Describe the trip and we will tell you what we need to quote.</p>'
                      f'<p style="margin-top:16px"><a class="txtlink" href="{PHONE_HREF}">{PHONE_TXT}</a></p></div>'
                      '<div class="card"><span class="tag">Form</span><h3>Request a trip quote</h3>'
                      '<p>The fastest way to give us the full picture: date, route, passengers and duration.</p>'
                      '<p style="margin-top:16px"><a class="txtlink" href="/request-quote/">Request a trip quote</a></p></div>'
                      f'<div class="card"><span class="tag">Email</span><h3>Email</h3>'
                      f'<p>Include your trip details so we can quote without a round of questions.</p>'
                      f'<p style="margin-top:16px"><a class="txtlink" href="mailto:{LEAD_EMAIL}">{LEAD_EMAIL}</a></p>'
                      f'<!-- [VERIFY BEFORE PUBLISHING: confirm the public enquiry email address. A business address on '
                      f'the domain is preferable to a personal address.] --></div>'
                      '</div>')
            + section("Business details", "Details published only once confirmed.",
                      "Rather than filling this page with claims, here is exactly what is still being confirmed.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>Available now</h3><ul>'
                      f'<li>Telephone: {PHONE}</li>'
                      '<li>Vehicle: 17-seat Force Urbania</li>'
                      '<li>Service: pre-booked private group transport, quotation on request</li>'
                      '<li>City: Hyderabad</li></ul></div>'
                      '<div class="card"><h3>Being confirmed before publication</h3><ul>'
                      '<li>Registered business name and address</li>'
                      '<li>Operating base and confirmed service area</li>'
                      '<li>Permit, insurance and fitness documentation</li>'
                      '<li>Driver arrangements</li>'
                      '<li>GST and invoicing status</li>'
                      '<li>Photographs of the vehicle</li></ul>'
                      '<p style="margin-top:14px" class="small">We would rather publish nothing here than publish '
                      'something unverified.</p></div></div>', alt=True)
            + cta_band())
    page("/contact/", "Contact | Group Transport Hyderabad " + PHONE,
         f"Contact for pre-booked private group transport in Hyderabad with a 17-seat Force Urbania. Call {PHONE} or request a trip quote online.",
         body, ld=[crumb_ld([("Home", "/"), ("Contact", "/contact/")])], active="/contact/")

def build_privacy():
    rows = [
        ("What we collect", "The trip details you submit — trip type, travel date, pickup and drop points, passenger count, duty duration, estimated distance, and your name, phone number and email if you provide one."),
        ("Why we use it", "Only to prepare your quotation and reply to your enquiry. We do not sell, rent or share your details with third parties, and we do not add you to a marketing list."),
        ("Sending the form", "When you submit the form, your details are used to compose the quotation request that reaches us. Please be aware that the enquiry travels over ordinary email unless a different delivery method is confirmed."),
        ("How long we keep it", "While your enquiry is active, and for a reasonable period afterwards for our records. Ask us and we will delete it sooner."),
        ("Your choices", f"Call or email us to see what we hold, correct it, or ask us to delete it. See the contact page for how to reach us."),
        ("Cookies and analytics", "This site currently sets no analytics or advertising cookies. If measurement is added later, this page will be updated before it is enabled."),
    ]
    inner = "".join(f'<div class="card" style="margin-bottom:14px"><h3>{a}</h3><p>{b}</p></div>' for a, b in rows)
    body = (breadcrumb([("Home", "/"), ("Privacy", "/privacy/")])
            + hero("Privacy", "Privacy notice.", "Short, because it should be readable.", ctas=False)
            + section("Privacy", "How your information is handled.",
                      "Your trip details are used to prepare your quotation and reply to you, and for nothing else.",
                      inner, alt=False)
            + f'<section><div class="wrap"><p class="small">Last updated {TODAY}.</p>'
              f'<!-- [VERIFY BEFORE PUBLISHING: legal entity name and contact for data requests; '
              f'confirm DPDP Act compliance wording with the owner] --></div></section>')
    page("/privacy/", "Privacy Notice | Group Transport Hyderabad",
         "How trip enquiry details are handled for this Hyderabad group transport service.",
         body, ld=[crumb_ld([("Home", "/"), ("Privacy", "/privacy/")])])

def build_terms():
    items = [
        ("Quotation enquiries only", "Submitting the enquiry form does not confirm vehicle availability, does not reserve the vehicle and does not create a booking. A trip is agreed only once availability is confirmed and the terms are accepted."),
        ("Pricing", "A quotation is prepared for each enquiry based on trip type, duration, distance or route, and date. The quotation is valid for the period stated in it."),
        ("Inclusions", "The quotation covers the vehicle and driver for the journeys described. Tolls, parking, permits, interstate taxes, driver allowance and any other statutory charges are included or excluded as stated in the quotation."),
        ("Waiting and overtime", "Waiting time and any extension beyond the agreed duty are treated as set out in the quotation."),
        ("Changes and cancellation", "Changes to the itinerary may change the price. Cancellation terms are those stated in your quotation, since they depend on the trip and the date."),
        ("Passenger and luggage limits", "The vehicle must not be loaded beyond its permitted seating and weight capacity. Share accurate passenger and luggage information at the enquiry stage so suitability can be confirmed."),
        ("Customer responsibilities", "Provide accurate trip details, be ready at the agreed pickup time, and ensure the group complies with the driver's reasonable instructions and with applicable law."),
        ("Vehicle and driver", "The vehicle and driver details for your trip are provided as part of your quotation."),
        ("Liability", "Nothing in these terms excludes liability that cannot be excluded under applicable law."),
    ]
    inner = "".join(f'<div class="card" style="margin-bottom:14px"><h3>{a}</h3><p>{b}</p></div>' for a, b in items)
    body = (breadcrumb([("Home", "/"), ("Terms", "/terms/")])
            + hero("Terms", "Terms of service.", "The basis on which trips are quoted and provided.", ctas=False)
            + section("Terms", "How trips are quoted and provided.",
                      "The specific terms for your trip are those stated in your quotation. This page sets out the general basis.",
                      inner)
            + f'<section class="alt"><div class="wrap"><div class="notice"><span>&#9432;</span><div>'
              'These terms are a general statement of how quotations work. The specific terms for your trip are those '
              'stated in your quotation.</div></div>'
              f'<p class="small" style="margin-top:20px">Last updated {TODAY}.'
              '<!-- [VERIFY BEFORE PUBLISHING: legal review of these terms; cancellation and payment policy; '
              'toll, parking, overtime and driver-allowance rules] --></p></div></section>')
    page("/terms/", "Terms of Service | Group Transport Hyderabad",
         "Terms covering quotation enquiries, pricing, inclusions and changes for pre-booked group transport in Hyderabad.",
         body, ld=[crumb_ld([("Home", "/"), ("Terms", "/terms/")])])

def build_404():
    body = (hero("404", "That page is not here.",
                 "The link may be out of date, or the page may have moved.",
                 ctas=False)
            + section("Where to go", "Try one of these.",
                      "Or call and we will point you to the right place.",
                      '<div class="grid g3">'
                      '<a class="card" href="/"><h3>Home</h3><p>Overview of the vehicle and the trip types.</p></a>'
                      '<a class="card" href="/request-quote/"><h3>Request a trip quote</h3><p>Send your trip details and get a quotation.</p></a>'
                      f'<a class="card" href="{PHONE_HREF}"><h3>Call {PHONE}</h3><p>Speak to us about the trip.</p></a>'
                      '</div>'))
    page("/404.html", "Page not found | " + BRAND,
         "The page you requested could not be found.", body, noindex=True)

# ------------------------------------------------------------------ static
SITEMAP = ["/", "/find-a-vehicle/", "/force-urbania-hire-hyderabad/",
           "/airport-group-transfer-hyderabad/", "/outstation-group-travel-hyderabad/",
           "/wedding-transport-hyderabad/", "/corporate-group-transport-hyderabad/",
           "/hyderabad-sightseeing-group-travel/", "/family-group-travel-hyderabad/",
           "/how-it-works/", "/what-to-expect/", "/request-quote/", "/partner-with-us/",
           "/guides/", "/guides/force-urbania-vs-tempo-traveller/",
           "/guides/group-vehicle-fit-guide/", "/guides/wedding-guest-transport-planning/",
           "/about/", "/contact/", "/privacy/", "/terms/"]

def build_static():
    write_page("/style.css", CSS + PLANNER_CSS)
    # Open Graph image — generated graphic, NOT a photograph of the actual vehicle.
    try:
        from PIL import Image, ImageDraw, ImageFont
        im = Image.new("RGB", (1200, 630), "#131A24")
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 1200, 10], fill="#0F6E68")
        def fnt(sz, bold=False):
            for path in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold
                         else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]):
                try: return ImageFont.truetype(path, sz)
                except Exception: pass
            return ImageFont.load_default()
        d.text((72, 88), "17-SEAT FORCE URBANIA", font=fnt(28, True), fill="#6FD3E0")
        d.text((72, 146), "Private group transport", font=fnt(64, True), fill="#FFFFFF")
        d.text((72, 228), "in Hyderabad", font=fnt(64, True), fill="#FFFFFF")
        d.text((72, 344), "Airport groups  \u00b7  Weddings & events", font=fnt(28), fill="#C7D3DD")
        d.text((72, 388), "Corporate travel  \u00b7  Sightseeing & day hire", font=fnt(28), fill="#C7D3DD")
        d.text((72, 492), "+91 62020 66104", font=fnt(34, True), fill="#FFFFFF")
        d.text((72, 548), "Quotation on request \u2014 availability confirmed before booking",
               font=fnt(22), fill="#8FA0AF")
        im.save(os.path.join(OUT, "og.png"), optimize=True)
        print("wrote /og.png")
    except Exception as e:
        print("og.png not generated:", e)
    write_page("/favicon.svg",
               '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0F6E68"/>'
               '<text x="32" y="43" font-family="Inter,Arial,sans-serif" font-size="30" font-weight="700" '
               'fill="#fff" text-anchor="middle">17</text></svg>')
    write_page("/robots.txt",
               "# Group transport Hyderabad - robots.txt\n"
               "# Public commercial pages: crawlable by search engines and AI answer engines.\n\n"
               "User-agent: *\nAllow: /\nDisallow: /thank-you/\n\n"
               "# Answer engines and search assistants: allowed to surface public content.\n"
               "User-agent: OAI-SearchBot\nAllow: /\n\n"
               "User-agent: ChatGPT-User\nAllow: /\n\n"
               "User-agent: PerplexityBot\nAllow: /\n\n"
               "User-agent: Google-Extended\nAllow: /\n\n"
               "User-agent: Googlebot\nAllow: /\n\n"
               "User-agent: Bingbot\nAllow: /\n\n"
               "# Training-only crawlers: access not required to be cited as an answer source.\n"
               "# Remove the Disallow lines below if the owner chooses to allow model training.\n"
               "User-agent: GPTBot\nDisallow: /\n\n"
               "User-agent: CCBot\nDisallow: /\n\n"
               "User-agent: ClaudeBot\nDisallow: /\n\n"
               f"Sitemap: {BASE}/sitemap.xml\n")
    urls = "".join(f'  <url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod>'
                   f'<changefreq>{"weekly" if p in ("/", "/request-quote/") else "monthly"}</changefreq>'
                   f'<priority>{"1.0" if p == "/" else ("0.9" if p == "/request-quote/" else "0.8")}</priority></url>\n'
                   for p in SITEMAP)
    write_page("/sitemap.xml",
               '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + urls + "</urlset>\n")
    lines = [
        "# Group transport — Hyderabad (working name)", "",
        "> Pre-booked private group transport in Hyderabad using a 17-seat Force Urbania. Airport group transfers, "
        "weddings and events, corporate travel, and sightseeing or custom multi-stop day hire. Quotation on request. "
        "Availability is confirmed personally per enquiry; the website does not take instant bookings.", "",
        "## Key facts (state only these unless the owner confirms more)",
        "- Vehicle: one 17-seat Force Urbania (a single vehicle, not a fleet)",
        f"- Telephone: {PHONE}",
        "- City: Hyderabad, India",
        "- Model: pre-booked private group transport / vehicle hire with driver",
        f"- Quoting: quotation request via {BASE}/request-quote/ — submitting an enquiry does NOT confirm a booking",
        "- Not provided: packaged tours, guides, attraction tickets, hotels",
        "- Outstation travel: subject to permissions and operating arrangements at the time of enquiry", "",
        "## Trip types",
        f"- Airport group transfers: {BASE}/airport-group-transfer-hyderabad/",
        f"- Weddings and events: {BASE}/wedding-event-transport-hyderabad/",
        f"- Corporate travel: {BASE}/corporate-group-transport-hyderabad/",
        f"- Sightseeing, day hire and custom multi-stop trips: {BASE}/hyderabad-sightseeing-group-travel/", "",
        "## What a customer needs to provide",
        "Travel date, pickup point, drop point or main destination, passenger count, duty duration "
        "(a few hours / full day / multiple days) and an estimate of distance or stops. If the distance is unknown, "
        "the itinerary can be used instead.", "",
        "## Preferred citation",
        '"A 17-seat Force Urbania is offered for pre-booked private group transport in Hyderabad, covering airport '
        'group transfers, weddings, corporate travel and custom sightseeing itineraries. Trips are quoted per enquiry '
        'and availability is confirmed before a booking is agreed."',
    ]
    write_page("/llms.txt", "\n".join(lines) + "\n")

def main():
    build_home(); build_airport(); build_wedding(); build_corporate(); build_sightseeing()
    build_guides_hub(); build_guide_urbania_vs_tempo(); build_guide_fit(); build_guide_wedding()
    build_quote(); build_about(); build_contact(); build_privacy(); build_terms(); build_404()
    from build_v3 import build_v3_pages
    build_v3_pages()
    build_static()
    print(f"DONE — {len(SITEMAP)} sitemap URLs, {TODAY}")

if __name__ == "__main__":
    main()
