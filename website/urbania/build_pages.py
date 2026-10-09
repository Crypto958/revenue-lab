#!/usr/bin/env python3
"""Urbania group transport — pages. Run: python3 build_pages.py"""
import os, json, html, urllib.parse
from build_ui import (BASE, BRAND, PHONE, PHONE_HREF, PHONE_TXT, WHATSAPP, CITY, OUT, TODAY, YEAR, CSS,
                      NAV, head, header, footer, crumb_ld, faq_ld, service_ld,
                      hero, section, cta_band, faq_block, vehicle_panel, write_page, call_svg, brand_svg)
from build_planner import planner, PLANNER_CSS, PLANNER_JS, MODES
import build_sections as SEC
import site_data as DATA
from verified_seo_cohort import CITY_COHORT, ROUTE_COHORT

# Lead delivery. OWNER DECISION REQUIRED — see docs/OWNER_DECISIONS.md.
# Empty endpoint => the form composes a pre-filled email instead, so no lead is lost.
FORM_ENDPOINT = "/api/trip"   # same-origin Netlify Function. Falls back to WhatsApp if unreachable.
LEAD_EMAIL = "fca.abhi007@gmail.com"   # owner-supplied professional address; confirm/replace

def planner_blocks(preset=""):
    """Adaptive planner markup + its JS, with the delivery endpoint resolved."""
    mk = planner(preset).replace("%PHONE_HREF%", PHONE_HREF)
    return mk + PLANNER_JS.replace("%WA%", WHATSAPP).replace("%ENDPOINT%", FORM_ENDPOINT)

AVAIL_NOTE = ("We check the route, vehicle fit and availability for your dates, then include the "
              "confirmation with your quotation.")

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
 ("Can UrbanLoop arrange group transport anywhere in India?",
  "We accept enquiries from across India. Share the origin, destination, dates, group size and trip type; we check the route and suitable operating vehicle options before sending a quotation."),
 ("What information should I provide to get a quotation?",
  "Travel date, pickup point, main destination or drop point, number of passengers, whether you need a few hours, a full day or multiple days, and an estimate of the distance or number of stops. If you are unsure about distance, select \u201cNot sure\u201d — we can work it out from your itinerary."),
 ("Can we provide our own itinerary?",
  "Yes. All the trips we quote are based on the customer's own plan. You choose the stops and the running order; we tell you what is practical for a single day and how the timing works."),
 ("Can we request multiple stops?",
  "Yes — multi-stop trips are a normal part of group travel. List the stops in the enquiry so the route and duration can be quoted accurately."),
 ("Does submitting the form confirm the booking?",
  "No. Submitting the form is a quotation enquiry. It does not confirm vehicle availability or create a booking. We reply with a quotation and confirm availability before anything is agreed."),
 ("How many passengers can travel?",
  "Vehicle suitability depends on the group size, luggage, route and the operating option available for your dates. Share the exact number of adults and children so we can recommend and confirm the right arrangement."),
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
        "Verified vehicle options across India",
        "Quotation prepared for your actual itinerary",
        "Availability checked before anything is agreed",
        "Airport groups, weddings, corporate travel and outstation trips",
        "Your itinerary, not a fixed package",
        "Travelling as one group instead of coordinating several cabs",
    ]
    tick = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#116A7B" stroke-width="2.6" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
    facthtml = "".join(f'<div class="fact">{tick}<span>{f}</span></div>' for f in facts)
    usecases = ["Airport", "Outstation", "Corporate", "Weddings", "Family trips",
                "Pilgrimage", "Events"]
    chips = "".join(f'<a class="uc" href="#find-your-urbania-vehicles">{u}</a>' for u in usecases)
    hero_img = SEC.find_image("hero", "hero-split")
    if hero_img:
        # Template cloned from the primary reference: full-bleed photograph, dark
        # scrim, centred two-line headline with the second line in the accent, and
        # the quote bar floating over the hero's bottom edge as the single CTA.
        hero = (
            '<section class="hx">'
            f'<img class="hx-bg" src="{hero_img}" alt="" aria-hidden="true" '
            f'width="747" height="685" fetchpriority="high" decoding="async">'
            '<div class="hx-scrim"></div>'
            '<div class="hx-in">'
            '<span class="eyebrow" style="color:#8FD3CB">UrbanLoop &middot; Premium Group Mobility</span>'
            '<h1 style="margin-top:16px">Group transport'
            '<span class="l2">across India</span></h1>'
            '<p class="hx-line">Move Together, Better.</p>'
            '<p class="lede">Premium group transportation for airport transfers, family journeys, '
            'corporate travel, weddings, events and outstation trips. Tell us where you are travelling, '
            'how many people are going and what vehicle category you need; we coordinate suitable options '
            'across India.</p>'
            + (f'<p class="hx-alt"><a href="https://wa.me/{WHATSAPP}" rel="noopener">WhatsApp us</a>'
               f'<span>&middot;</span><a href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a></p>'
               if WHATSAPP else '')
            + '<p class="hx-cap"><b>Vehicle options matched to your trip.</b> Availability is checked for your route and dates before we quote.</p>'
            f'<div class="qwrap">{SEC.journey_bar()}</div>'
            '</div></section>'
            # The bar hangs below the hero, so this section starts clear of it.
            f'<section class="hx-follow" id="find-your-urbania"><div class="wrap">'
            + SEC.fleet_status_note()
            + f'<div class="ucs" style="margin-top:22px">{chips}</div>'
            + '</div></section>'
        )
    else:
        # No wide crop supplied yet — keep the two-column layout with the visual panel.
        intro = (
            '<span class="eyebrow">UrbanLoop &middot; India-wide group transport</span>'
            '<h1>Group transport across India</h1>'
            '<p class="lede">Private group travel for airport transfers, weddings, corporate days, '
            'outstation travel and sightseeing. Share the route and dates so suitable vehicle '
            'options can be checked before a quotation.</p>'
            '<div class="heroacts">'
            '<a class="btn" href="/request-quote/">Get a quote</a>'
            f'<a class="btn ghost" href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a>'
            '</div>'
            f'<div class="ucs">{chips}</div>'
        )
        hero = ('<section class="hero"><div class="wrap"><div class="hv"><div>' + intro
                + '</div><div>' + SEC.hero_visual() + '</div>'
                '</div></div></section>'
                + '<section style="padding-top:0"><div class="wrap">'
                  + SEC.fleet_status_note() + SEC.journey_bar() + '</div></section>')
    body = (
        hero
        + f'<section class="alt"><div class="wrap"><div class="facts">{facthtml}</div></div></section>'
        + '<section id="find-your-urbania-vehicles"><div class="wrap"><div class="shead">'
          '<span class="eyebrow">Vehicle matching</span><h2>Find a suitable vehicle option</h2>'
          '<p class="lede">Tell us how many people are travelling. We use group size, luggage, route and dates to recommend a suitable arrangement.</p></div>'
          + SEC.find_your_urbania() + '</div></section>'
        + section("Vehicle options", "Choose the right starting point.",
                  "These are the operational categories we can consider. The exact vehicle and configuration are confirmed for your route, date and group details.",
                  SEC.config_cards(), alt=True)
        + '<section style="padding-top:0"><div class="wrap">'
          '<div class="shead" style="margin-bottom:18px"><h2 style="font-size:clamp(19px,2.1vw,25px)">'
          'Plan your group trip</h2></div>'
          + planner_blocks("") + '</div></section>'
        + section("Trip types", "What groups use the vehicle for.",
                  "Every trip is quoted from your own plan. These are the four situations that come up most often.",
                  '<div class="grid g2">'
                  '<a class="card" href="/india/"><span class="tag">Airport</span>'
                  '<h3>Group airport transfers</h3><p>Arrivals, departures or both, with the group and their luggage planned together. Provide flight timing and passenger count.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Airport group transfers</span></p></a>'
                  '<a class="card" href="/india/"><span class="tag">Weddings &amp; events</span>'
                  '<h3>Wedding and event transport</h3><p>Guest movement between hotels, venues and the airport across one day or several. Send the schedule and guest numbers.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Wedding &amp; event transport</span></p></a>'
                  '<a class="card" href="/india/"><span class="tag">Corporate</span>'
                  '<h3>Corporate group travel</h3><p>Visiting teams, delegations and off-site groups moving between airport, hotel, office and venue on a schedule.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Corporate group transport</span></p></a>'
                  '<a class="card" href="/india/"><span class="tag">Sightseeing &amp; day hire</span>'
                  '<h3>Sightseeing and day hire</h3><p>Full-day or multi-stop city travel using your own itinerary — you choose the stops and the running order.</p>'
                  '<p style="margin-top:14px"><span class="txtlink">Sightseeing &amp; custom trips</span></p></a>'
                  '</div>', alt=True)
        + section("Services", "What we are booked for.",
                  "Every trip is quoted from your own plan. These are the situations that come up most often.",
                  SEC.services_grid())
        + section("Routes", "Find your route.",
                  "Share any origin and destination in India. Published route pages provide planning context; the quotation confirms the practical details for your dates.",
                  '<p><a class="btn" href="/india/">Explore India-wide routes and destinations</a></p>', alt=True)
        + section("Pricing", "A clear quotation for your trip.",
                  "We do not publish a one-size-fits-all price. Route, dates, duration, vehicle category and group requirements all affect the quotation.",
                  '<p><a class="btn" href="/request-quote/">Request a trip quotation</a></p>')
        + section("Trust", "What you can rely on.",
                  "We publish figures we can stand behind. Where we do not have one yet, we say so.",
                  SEC.trust_strip(), alt=True)
        # Bands with nothing real to show are OMITTED, not rendered empty with
        # "coming soon" copy. An empty box advertises the absence and is the
        # clearest "unfinished" signal a page can carry; each rendered photograph
        # already carries its own provenance caption.
        + (section("Reviews", "What customers say.",
                   "Reviews appear here only when they are genuine.",
                   SEC.reviews_block()) if SEC.REVIEWS else "")
        + (section("Gallery", "The vehicle, photographed.",
                   "Images of the Force Urbania model.",
                   SEC.gallery_block(), alt=True) if SEC.media_status()["gallery"] else "")
        + section("Seating", "Seating references.",
                  "Seat layout and legroom decide whether a long trip is comfortable. These are the "
                  "details group buyers ask about most.",
                  SEC.seating_block())
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
        + section("Vehicle information", "The right arrangement for your group.",
                  "UrbanLoop coordinates suitable vehicle options for the route and date you provide. We confirm the exact arrangement, luggage fit and availability before you accept a quotation.",
                  '<div class="grid g3">'
                  '<div class="card"><h3>Group size</h3><p>Tell us the number of adults, children and any special seating needs so we can recommend a suitable configuration.</p></div>'
                  '<div class="card"><h3>Luggage</h3><p>Luggage capacity depends on passenger numbers and bag sizes. Share your passenger count and approximate luggage in the enquiry so suitability is confirmed for your trip rather than assumed.</p></div>'
                  '<div class="card"><h3>Driver and vehicle details</h3><p>Driver arrangements, permit, insurance and vehicle documentation are provided with your quotation so you know exactly what you are booking before you confirm.</p></div>'
                  '</div>'
                  '<!-- [VERIFY BEFORE PUBLISHING: seating layout, luggage capacity in practice, driver arrangement, '
                  'permit status, insurance status, vehicle fitness/compliance, vehicle year and model variant] -->',
                  alt=True)
        + section("Why UrbanLoop", "One contact point for group transport.",
                  "We make the vehicle search and quotation process easier without asking you to contact multiple operators yourself.",
                  '<div class="grid g3">'
                  '<div class="card"><h3>Route review</h3><p>We review the pickup points, destination, stops and timing before recommending an arrangement.</p></div>'
                  '<div class="card"><h3>Verified options</h3><p>We use operating vehicle information rather than presenting an unverified listing as available.</p></div>'
                  '<div class="card"><h3>Clear next step</h3><p>You receive a quotation with the vehicle arrangement and availability confirmation before deciding.</p></div>'
                  '</div>')
        + section("Guides", "Before you enquire.",
                  "Short, practical pages answering the questions that come up most often.",
                  '<div class="grid g3">'
                  '<a class="card" href="/guides/force-urbania-vs-tempo-traveller/"><h3>Force Urbania vs Tempo Traveller</h3>'
                  '<p>How the two group vehicles compare, and how to decide which suits your group and route.</p></a>'
                  '<a class="card" href="/guides/group-vehicle-fit-guide/"><h3>Choosing a vehicle for your group</h3>'
                  '<p>Working out what vehicle a group actually needs, including luggage and seating.</p></a>'
                  '<a class="card" href="/guides/wedding-guest-transport-planning/"><h3>Wedding guest transport</h3>'
                  '<p>Planning guest movement between hotels, venues and the airport without chaos.</p></a>'
                  '</div>', alt=True)
        + section("Pricing questions", "What it costs, and how it is worked out.",
                  "Commercial questions answered plainly, including what sits outside the quotation.",
                  '<p>Route, dates, duration, vehicle category and group requirements all affect the quotation. <a href="/request-quote/">Send your trip details</a> for a clear price.</p>')
        + faq_block(CORE_FAQ)
        + cta_band()
        + SEC.FIND_JS
    )
    page("/", "Group Transport Across India | UrbanLoop",
         "Arrange private group transport across India. Share your route, dates and group size; UrbanLoop checks suitable vehicle options and availability before quoting.",
         body,
         ld=[service_ld("Private group transport across India",
                        "UrbanLoop checks suitable vehicle options and availability for airport transfers, weddings, corporate travel, family trips, events and custom routes across India. Quotation provided on request.",
                        area_type="Country", area_name="India"),
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
                   "Short, practical pages about planning group travel across India — from vehicle fit and luggage to wedding schedules.",
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
    page("/guides/", "Group Transport Guides Across India | UrbanLoop",
         "Practical guides to planning group transport across India — vehicle comparison, passenger and luggage fit, and wedding guest transport.",
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
               "Force Urbania vs Tempo Traveller | Group Travel India",
               "How the Force Urbania and Tempo Traveller compare for group travel across India, and the questions that decide which suits your group and route.",
               "Force Urbania vs Tempo Traveller for group travel",
               "An honest comparison, and how to decide for your own group.",
               ["Both vehicles are widely used for group travel in India. The choice usually comes down to group size, luggage and how long you are on the road — not to the badge on the front."],
               secs, faqs,
               [("Home", "/"), ("Guides", "/guides/"),
                ("Urbania vs Tempo Traveller", "/guides/force-urbania-vs-tempo-traveller/")],
               related=[("What vehicle fits a group of 10\u201317?",
                         "/guides/group-vehicle-fit-guide/",
                         "Work out seating and luggage before you start comparing vehicles."),
                        ("Plan an India-wide group trip",
                         "/india/",
                         "Start with your route, dates, passengers and luggage.")])

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
     ("What vehicle do I need for 15 people?",
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
               "What Vehicle Fits a Group of 10\u201317 People? | UrbanLoop",
               "How to work out what vehicle a group of 10 to 17 people needs, including the luggage question that most group travel plans get wrong.",
               "Travelling with 10\u201317 people: what vehicle do you need?",
               "Group size is the easy part. Luggage and duration decide whether a plan actually works.",
               ["This page is meant to help you work out the requirement before you start asking for prices."],
               secs, faqs,
               [("Home", "/"), ("Guides", "/guides/"), ("Vehicle fit guide", "/guides/group-vehicle-fit-guide/")],
               related=[("Force Urbania vs Tempo Traveller",
                         "/guides/force-urbania-vs-tempo-traveller/",
                         "How the two group vehicles compare, and how to choose between them."),
                        ("Group airport transfers",
                         "/services/airport-group-transfers/",
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
               "How to Arrange Transport for Wedding Guests | UrbanLoop",
               "A practical approach to planning wedding guest transport across India — building the movement list, grouping guests and avoiding common failures.",
               "How to arrange transport for wedding guests",
               "Build the movement list first. Vehicles are the easy part.",
               ["Wedding transport is a scheduling problem, not a vehicle problem. Get the schedule right and the vehicle follows."],
               secs, faqs,
               [("Home", "/"), ("Guides", "/guides/"),
                ("Wedding guest transport", "/guides/wedding-guest-transport-planning/")],
               related=[("Wedding &amp; event transport",
                        "/services/wedding-guest-transport/",
                         "How we quote guest movement across a wedding schedule."),
                        ("What vehicle fits a group of 10\u201317?",
                         "/guides/group-vehicle-fit-guide/",
                         "Seating and luggage, checked before the day rather than on it.")])


def build_quote():
    body = (breadcrumb([("Home", "/"), ("Request a trip quote", "/request-quote/")])
            + hero("Request a trip quote",
                   "Request a trip quote",
                   "Share your date, pickup point, destination, passenger count and how long you need the vehicle. We reply with a quotation for the trip you described.",
                   paras=[AVAIL_NOTE], ctas=False)
            + section("Trip details", "Tell us about the trip.",
                      "Fields marked * are needed to quote accurately. Everything else helps us get it right first time.",
                      planner_blocks(""))
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
                 "We aim to respond promptly, but we do not publish a guaranteed response time because it depends on enquiry volume. If your trip is time-critical, call customer care."),
                ("Can I request a quotation for several dates?",
                 "Yes. Note the alternative dates in the notes field and we will quote for each."),
                ("Do you store my details?",
                 "Your trip details are used to prepare your quotation and reply to you. See the privacy page for how information is handled."),
              ], "About the enquiry.")
            + cta_band("Prefer to speak to someone?",
                       "Call and describe the trip. If you already have the details to hand, the form takes about two minutes."))
    # The planner renders its own JS via planner_blocks(); there is a single
    # quote funnel now, so no separate page-level script is injected here.
    doc = "\n".join([head("Request a Trip Quote Across India | UrbanLoop",
                          "Request private group transport across India. Send your date, route, group size and duration. This is an enquiry, not a booking.",
                          "/request-quote/",
                          [service_ld("Trip quotation request",
                                      "Quotation request for private group transport across India with a suitable vehicle arrangement checked per enquiry.",
                                      area_type="Country", area_name="India"),
                           crumb_ld([("Home", "/"), ("Request a trip quote", "/request-quote/")])]),
                    (header("/request-quote/") + body + footer()).replace(PHONE, PHONE_TXT)])
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
                      "WhatsApp, phone, or the quotation form. The form records your trip details, "
                      "and the confirmation screen gives you a one-tap option to send the same "
                      "summary to us on WhatsApp.",
                      '<div class="grid g3">'
                      f'<div class="card"><span class="tag">WhatsApp</span><h3>Message us</h3>'
                      f'<p>The fastest route. Send the date, route, passenger count and duration and we will reply with a quotation.</p>'
                      f'<p style="margin-top:16px"><a class="txtlink" href="https://wa.me/{WHATSAPP}">WhatsApp +91 91821 26104</a></p>'
                      f'<!-- [VERIFY BEFORE PUBLISHING: the WhatsApp Business number (+91 91821 26104) differs from the '
                      f'call number published in the brief (+91 62020 66104). Confirm which is which, and note the '
                      f'WhatsApp Business profile shows Supaul, Bihar rather than Hyderabad.] --></div>'
                      f'<div class="card"><span class="tag">Phone</span><h3>Call</h3>'
                      f'<p>Describe the trip and we will tell you what we need to quote.</p>'
                      f'<p style="margin-top:16px"><a class="txtlink" href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a></p></div>'
                      '<div class="card"><span class="tag">Form</span><h3>Request a trip quote</h3>'
                      '<p>The fastest way to give us the full picture: date, route, passengers and duration.</p>'
                      '<p style="margin-top:16px"><a class="txtlink" href="/request-quote/">Request a trip quote</a></p></div>'
                      f'<div class="card"><span class="tag">Email</span><h3>Email</h3>'
                      f'<p>Include your trip details so we can quote without a round of questions.</p>'
                      f'<p style="margin-top:16px"><a class="txtlink" href="mailto:{LEAD_EMAIL}">{LEAD_EMAIL}</a></p>'
                      f'<!-- [VERIFY BEFORE PUBLISHING: confirm the public enquiry email address. A business address on '
                      f'the domain is preferable to a personal address.] --></div>'
                      '</div>')
            + section("Getting in touch", "How to reach us.",
                      "Pre-booked private group transport with a 17-seat Force Urbania.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>By telephone</h3><ul>'
                      f'<li><a href="{PHONE_HREF}">{call_svg()}&nbsp;Call customer care</a></li>'
                      '<li>Quickest for checking whether a date is free</li>'
                      '<li>Based in Hyderabad</li></ul></div>'
                      '<div class="card"><h3>By quotation request</h3><ul>'
                      '<li>Send the date, pickup point, destination and passenger count</li>'
                      '<li>You receive a written quotation in reply</li>'
                      '<li>Nothing is charged to ask, and an enquiry does not book the vehicle</li>'
                      '</ul></div></div>', alt=True)
            + cta_band())
    page("/contact/", "Contact UrbanLoop | Group Transport India",
         "Contact UrbanLoop about private group transport across India or request a trip quote online.",
         body, ld=[crumb_ld([("Home", "/"), ("Contact", "/contact/")])], active="/contact/")

def build_privacy():
    rows = [
        ("What we collect", "For a trip enquiry, we collect the trip and contact details you choose to submit. For a supplier enquiry, we may collect business and contact details, operating base and service areas, fleet size, vehicle configuration and registration details, driver arrangements and the checks you carry out, indicative rates and commercial terms, and optional rate cards, business documents, vehicle registration certificates, permits, insurance, fitness documents and vehicle photos."),
        ("Why we use it", "Trip details are used to prepare and respond to your quotation request. Supplier details and documents are used to review the operator, vehicle, service area, compliance information, driver-check process and commercial fit, and to contact you about the enquiry. A supplier enquiry is not an approval or promise of work. We do not add these details to a marketing list."),
        ("Who processes the forms", "Website forms are submitted to UrbanLoop through Netlify's form handling service. Submission records are available to authorized site account administrators for enquiry handling and supplier review. Supplier rates and documents are not published or presented to customers as live availability."),
        ("AI chat", "When the AI chat is available, the messages you send and recent chat context are sent to OpenAI's API to generate a reply. Do not share payment details or sensitive personal information in chat. UrbanLoop does not add chat transcripts to its trip enquiry records; use the trip form or WhatsApp if you want us to follow up about a journey."),
        ("How long we keep it", "We keep an enquiry while it is being handled and remove it when it is no longer needed for that purpose, unless a legal record-keeping requirement applies. You may ask us to correct or delete a submission."),
        ("Your choices and requests", f"You may ask to access, correct or delete your details, or withdraw consent for an enquiry, by calling {PHONE} or using the contact page. We will use reasonable steps to locate the relevant submission."),
        ("Cookies and analytics", "This site currently sets no analytics or advertising cookies. If measurement is added later, this page will be updated before it is enabled."),
    ]
    inner = "".join(f'<div class="card" style="margin-bottom:14px"><h3>{a}</h3><p>{b}</p></div>' for a, b in rows)
    body = (breadcrumb([("Home", "/"), ("Privacy", "/privacy/")])
            + hero("Privacy", "Privacy notice.", "A clear note about the information you share with UrbanLoop.", ctas=False)
            + section("Privacy", "How your information is handled.",
                      "We use the details you submit only for the enquiry purpose described here.",
                      inner, alt=False)
            + f'<section><div class="wrap"><p class="small">Last updated {TODAY}.</p>'
              f'<!-- [VERIFY BEFORE PUBLISHING: legal entity name and contact for data requests; '
              f'confirm DPDP Act compliance wording with the owner] --></div></section>')
    page("/privacy/", "Privacy Notice | UrbanLoop",
         "How UrbanLoop handles trip enquiries and supplier interest form details.",
         body, ld=[crumb_ld([("Home", "/"), ("Privacy", "/privacy/")])], noindex=True)

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
         body, ld=[crumb_ld([("Home", "/"), ("Terms", "/terms/")])], noindex=True)

def build_404():
    body = (hero("404", "That page is not here.",
                 "The link may be out of date, or the page may have moved.",
                 ctas=False)
            + section("Where to go", "Try one of these.",
                      "Or call and we will point you to the right place.",
                      '<div class="grid g3">'
                      '<a class="card" href="/"><h3>Home</h3><p>Overview of the vehicle and the trip types.</p></a>'
                      '<a class="card" href="/request-quote/"><h3>Request a trip quote</h3><p>Send your trip details and get a quotation.</p></a>'
                      f'<a class="card" href="{PHONE_HREF}"><h3>Call customer care</h3><p>Speak to us about the trip.</p></a>'
                      '</div>'))
    page("/404.html", "Page not found | " + BRAND,
         "The page you requested could not be found.", body, noindex=True)

# ------------------------------------------------------------------ static
SITEMAP = ["/", "/india/", "/find-a-vehicle/", "/force-urbania-hire-hyderabad/",
           "/airport-group-transfer-hyderabad/", "/outstation-group-travel-hyderabad/",
           "/wedding-transport-hyderabad/", "/corporate-group-transport-hyderabad/",
           "/hyderabad-sightseeing-group-travel/", "/family-group-travel-hyderabad/",
           "/how-it-works/", "/what-to-expect/", "/request-quote/", "/partner-with-us/",
           "/guides/", "/guides/force-urbania-vs-tempo-traveller/",
           "/guides/group-vehicle-fit-guide/", "/guides/wedding-guest-transport-planning/",
           "/about/", "/contact/", "/destinations/"]

# Derived from site_data so a new configuration, route or service cannot be
# added without appearing in sitemap.xml. A page that exists but is not listed
# is invisible to search, which defeats the point of the architecture.
SITEMAP += ["/rates/force-urbania-rental-rates-hyderabad/"]
if DATA.FLEET_CONFIRMED:
    SITEMAP += [f'/fleet/{c["key"]}/' for c in DATA.CONFIGURATIONS]
SITEMAP += [f'/destinations/hyderabad-to-{r["name"].lower()}/' for r in DATA.ROUTES]
# These older URLs remain reachable for existing visitors, but their intent is
# covered by the stronger national service pages below. Keep them out of the
# index and sitemap to avoid competing canonical topics.
LEGACY_SERVICE_ALIASES = {"/services/events/", "/services/pilgrimage-tours/"}
SITEMAP += [s["href"] for s in DATA.SERVICES
            if s["href"].startswith("/services/") and s["href"] not in LEGACY_SERVICE_ALIASES]
SITEMAP += [s["href"] for s in DATA.NATIONAL_SERVICES]
SITEMAP += [f'/city/{slug}/' for _, slug, _, _ in CITY_COHORT]
SITEMAP += [f'/route/{origin_slug}-to-{destination.lower().replace(" ", "-")}/'
            for _, origin_slug, _, destination in ROUTE_COHORT]

# ------------------------------------------------------------------ SEO PAGES
# Architecture the brief asks for. These are real, substantive pages, not thin
# doorway pages. Every figure comes from site_data as a placeholder; nothing is
# invented, and unconfirmed specs render as "To be confirmed".
def _seo_page(path, title, desc, active, eyebrow, h1, sub, paras,
              body_sections, faqs, crumb, ldname, lddesc, noindex=False):
    body = (breadcrumb(crumb)
            + hero(eyebrow, h1, sub, paras=list(paras) + [AVAIL_NOTE], ctas=True)
            + body_sections
            + faq_block(faqs) + cta_band())
    page(path, title, desc, body,
         ld=[service_ld(ldname, lddesc), faq_ld(faqs), crumb_ld(crumb)],
         active=active, noindex=noindex)


def build_destinations_hub():
    cards = "".join(
        f'<a class="card" href="/destinations/hyderabad-to-{r["name"].lower()}/">'
        f'<h3>Hyderabad to {html.escape(r["name"])}</h3>'
        f'<p>{html.escape(r["note"])}</p>'
        '<span class="txtlink" style="margin-top:14px">Read the route guide</span></a>'
        for r in DATA.ROUTES
    )
    body = (
        breadcrumb([("Home", "/"), ("Destinations", "/destinations/")])
        + hero("Destinations · Hyderabad", "Group travel from Hyderabad.",
               "Route guides for trips quoted from your own itinerary, with practical planning points before you enquire.",
               paras=[AVAIL_NOTE])
        + section("Routes", "Choose a destination.",
                  "Each route page explains what to include in an enquiry and what depends on your dates, stops and group.",
                  f'<div class="grid g3">{cards}</div>')
        + cta_band("Planning a route not listed here?",
                   "Tell us the pickup point, destination, dates and group size and we will check whether we can quote it.")
    )
    page("/destinations/", "Group Travel Destinations from Hyderabad | UrbanLoop",
         "Route planning information for group travel from Hyderabad, including outstation destinations and custom itineraries.",
         body,
         ld=[service_ld("Group travel destinations from Hyderabad",
                        "Route planning information for group transport from Hyderabad, with quotations prepared for each itinerary."),
             crumb_ld([("Home", "/"), ("Destinations", "/destinations/")])],
         active="/destinations/")


def build_india_hub():
    city_cards = "".join(
        f'<a class="card" href="/city/{slug}/"><h3>{html.escape(city)}</h3>'
        f'<p>{html.escape(state)} · Verified service-area guide</p>'
        '<span class="txtlink" style="margin-top:14px">View city transport</span></a>'
        for city, slug, state, _ in CITY_COHORT)
    body = (
        breadcrumb([("Home", "/"), ("India", "/india/")])
        + hero("India-wide group transport", "Group transport across India.",
               "Tell us the origin, destination, dates and group size. UrbanLoop checks the route and a suitable vehicle arrangement before sending a quotation.",
               paras=["This is a managed quotation service, not a live availability directory. Vehicle, driver and route details are confirmed for the specific enquiry before a booking is agreed."])
        + section("Use cases", "Plan the journey your group actually needs.",
                  "Airport transfers, weddings, corporate movement, family travel, pilgrimage and multi-stop outstation trips can all be assessed from one enquiry.",
                  '<div class="grid g3">'
                  '<a class="card" href="/services/airport-group-transfers/"><h3>Airport transfers</h3><p>Share flight timing, pickup points, passengers and luggage.</p></a>'
                  '<a class="card" href="/services/wedding-guest-transport/"><h3>Wedding transport</h3><p>Send the guest movements, hotels, venues and dates.</p></a>'
                  '<a class="card" href="/services/corporate-group-transport/"><h3>Corporate travel</h3><p>Describe the team, schedule, stops and invoice needs.</p></a>'
                  '<a class="card" href="/services/outstation-group-travel/"><h3>Outstation trips</h3><p>Give us the route, stop order, dates and passenger count.</p></a>'
                  '<a class="card" href="/services/pilgrimage-group-travel/"><h3>Pilgrimage travel</h3><p>Plan early starts, temple stops and multi-day movement.</p></a>'
                  '<a class="card" href="/services/events-group-transport/"><h3>Events and group tours</h3><p>Share the schedule, venues and group requirements.</p></a>'
                  '<a class="card" href="/request-quote/"><h3>Custom itinerary</h3><p>Start with your own route if it does not fit a listed use case.</p></a>'
                  '</div>')
        + section("How it works", "One enquiry, checked before quotation.",
                  "Share the facts we need and we will reply with what can actually be arranged for those dates.",
                  '<div class="steps">'
                  '<div class="stepc"><span class="n">01</span><div><h3>Tell us the trip</h3><p>Origin, destination, dates, passengers, luggage and stops.</p></div></div>'
                  '<div class="stepc"><span class="n">02</span><div><h3>We check the practical fit</h3><p>We review the route and suitable vehicle arrangement for the enquiry.</p></div></div>'
                  '<div class="stepc"><span class="n">03</span><div><h3>We send a quotation</h3><p>The quotation sets out the inclusions, terms and availability position.</p></div></div>'
                  '</div>', alt=True)
        + section("Published information", "Cities and routes with verified data.",
                  "Browse the published city and route cohort for planning context. A page is added only when its underlying location or route data has been verified.",
                  '<p><a class="btn ghost" href="/destinations/">Browse published routes</a></p>')
        + section("Verified service areas", "Choose a city.",
                  "These cities are the first nationwide cohort. Each page explains what to send in an enquiry without exposing internal operator details.",
                  f'<div class="grid g3">{city_cards}</div>', alt=True)
        + cta_band("Have a route in mind?", "Send the city, route, dates and group size and request a quotation.")
    )
    page("/india/", "India-Wide Group Transport Routes | UrbanLoop",
         "Request private group transport across India. Share your route, dates and group size; UrbanLoop checks vehicle suitability and availability before quoting.",
         body,
         ld=[{"@context": "https://schema.org", "@type": "Service",
             "name": "Private group transport across India",
             "serviceType": "Private group transport quotation service",
             "description": "UrbanLoop accepts group transport enquiries across India and confirms a suitable vehicle arrangement and availability per route and date.",
             "provider": {"@id": BASE + "/#org"},
             "areaServed": {"@type": "Country", "name": "India"}},
             crumb_ld([("Home", "/"), ("India", "/india/")])],
         active="/india/")


def build_verified_city_pages():
    """Build the first verified city cohort without exposing operator data."""
    for city, slug, state, destinations in CITY_COHORT:
        city_routes = [r for r in ROUTE_COHORT if r[1] == slug]
        route_cards = "".join(
            f'<a class="card" href="/route/{slug}-to-{destination.lower().replace(" ", "-")}/">'
            f'<h3>{html.escape(city)} to {html.escape(destination)}</h3>'
            '<p>Route planning, group-size and luggage details to include in the enquiry.</p>'
            '<span class="txtlink" style="margin-top:14px">Read the route guide</span></a>'
            for _, _, _, destination in city_routes)
        body_sections = (
            section("Planning", f"Group transport from {html.escape(city)}.",
                    "Airport, local, wedding, corporate, family, pilgrimage and outstation enquiries are assessed from the actual itinerary.",
                    '<div class="grid g3">'
                    '<div class="card"><h3>Tell us the trip</h3><p>Share the pickup point, destination, dates, passengers and luggage.</p></div>'
                    '<div class="card"><h3>We check the fit</h3><p>Vehicle variants and route arrangements are checked before a quotation is sent.</p></div>'
                    '<div class="card"><h3>You receive a quotation</h3><p>The quotation explains the available arrangement, inclusions and terms.</p></div>'
                    '</div>', alt=True)
            + section("Nearby routes", f"Popular routes from {html.escape(city)}.",
                      "These are verified route guides linked to this base city. Distances and journey times are not published unless separately verified.",
                      f'<div class="grid g3">{route_cards}</div>' if route_cards else
                      '<p>Tell us the destination and dates for a custom route check.</p>')
            + section("Vehicle fit", "Choose the right configuration for the group.",
                      "Operators in this verified city record have access to Force Urbania variants. Exact passenger capacity depends on the selected configuration and luggage, so it is confirmed at quotation stage.",
                      '<p><a class="btn ghost" href="/find-a-vehicle/">See vehicle guidance</a></p>')
        )
        faqs = [
            (f"Can I request group transport from {city}?",
             f"Yes. {city} is a verified base city in the current UrbanLoop service-area dataset. Send the route, dates and group size and we will confirm the practical arrangement before quoting."),
            (f"What trips can be requested from {city}?",
             "Airport, local city, outstation, wedding, corporate, family/group and pilgrimage transport can be assessed. Availability and vehicle fit are confirmed per enquiry."),
            ("Is a specific vehicle guaranteed when I submit an enquiry?",
             "No. An enquiry starts a manual check. The selected vehicle configuration and availability are confirmed in the quotation before a booking is agreed."),
        ]
        path = f"/city/{slug}/"
        _seo_page(path, f"Group Transport in {city} | Force Urbania | UrbanLoop",
                  f"Request Force Urbania group transport from {city}, {state}. Airport, wedding, corporate, family and outstation trips are checked per route and date.",
                  path, f"Verified service area · {city}", f"Group transport in {city}.",
                  f"Force Urbania enquiries from {city}, with route and vehicle fit confirmed before quotation.",
                  [f"{city} is a verified base city in the current UrbanLoop service-area dataset. The verified nearby catchment is approximately 250 km from the base city; exact route suitability is checked per enquiry."],
                  body_sections, faqs,
                  [("Home", "/"), ("India", "/india/"), (city, path)],
                  f"Group transport in {city}",
                  f"Force Urbania group transport enquiries from {city}, with availability confirmed per route and date.")


def build_verified_route_pages():
    """Build 30 route pages from the first 10 verified base cities."""
    for city, origin_slug, state, destination in ROUTE_COHORT:
        destination_slug = destination.lower().replace(" ", "-")
        path = f"/route/{origin_slug}-to-{destination_slug}/"
        origin_path = f"/city/{origin_slug}/"
        body_sections = (
            section("Route planning", f"{city} to {destination} by group vehicle.",
                    "The route is quoted from your itinerary rather than a fixed package. Share the dates, passenger count, luggage and any stops so the arrangement can be checked.",
                    '<div class="grid g3">'
                    '<div class="card"><h3>Origin</h3><p>Pickup points and any additional collection points in or around the verified base city.</p></div>'
                    '<div class="card"><h3>Destination</h3><p>Tell us the final destination, venue or accommodation and any planned stops.</p></div>'
                    '<div class="card"><h3>Dates</h3><p>Travel dates and duration determine the practical vehicle and driver arrangement.</p></div>'
                    '</div>', alt=True)
            + section("What to include", "Help us quote the route accurately.",
                      "Exact distance and journey time are not published here because they vary with the route, stops and timing.",
                      '<div class="grid g2"><div class="card"><h3>Send</h3><ul><li>Pickup area and destination</li><li>Travel and return dates</li><li>Passenger and luggage count</li><li>Stops or overnight plans</li></ul></div>'
                      '<div class="card"><h3>We confirm</h3><ul><li>Suitable Urbania configuration</li><li>Route and operating arrangement</li><li>Availability for the dates</li><li>Quotation terms and inclusions</li></ul></div></div>')
            + section("Related planning", "Start with the city or the full India guide.",
                      "Use the city page for nearby route context, or send a custom itinerary if your destination is different.",
                      f'<p><a class="btn ghost" href="{origin_path}">View {html.escape(city)} transport</a> '
                      '<a class="btn ghost" href="/india/">India-wide group transport</a></p>')
        )
        faqs = [
            (f"Can I request group transport from {city} to {destination}?",
             f"Yes. This is a verified route entry in the current UrbanLoop cohort. Send your dates, group size and itinerary so the practical arrangement can be checked."),
            ("What vehicle will be used on this route?",
             "A suitable Force Urbania configuration is checked against the passenger and luggage requirements. The exact configuration and availability are confirmed in the quotation."),
            ("Are distance and travel time guaranteed?",
             "No. They depend on the selected route, stops, traffic and date. We confirm the practical details from your itinerary rather than publish a fixed promise."),
        ]
        _seo_page(path, f"{city} to {destination} Group Transport | Force Urbania",
                  f"Request Force Urbania group transport from {city} to {destination}. Share dates, passengers, luggage and stops for a checked quotation.",
                  path, f"Verified route · {city} to {destination}", f"{city} to {destination} group transport.",
                  "A route-specific quotation checked from your itinerary, group size and dates.",
                  [f"This named route is part of the verified {city} service-area cohort. Vehicle fit and availability are confirmed before a booking is agreed."],
                  body_sections, faqs,
                  [("Home", "/"), ("India", "/india/"), (city, origin_path), (destination, path)],
                  f"{city} to {destination} group transport",
                  f"Force Urbania group transport from {city} to {destination}, quoted per itinerary.")


def build_rates_page():
    how = (
        '<div class="grid g3">'
        '<div class="card"><h3>Distance</h3><p>Outstation trips are billed per kilometre, measured '
        'garage to garage, so the journey to reach you is counted the same way a customer would expect.</p></div>'
        '<div class="card"><h3>Time</h3><p>Local use is billed as a package &mdash; a set number of hours and '
        'kilometres for the day &mdash; with extra hours and extra kilometres charged beyond that.</p></div>'
        '<div class="card"><h3>The driver</h3><p>Outstation and overnight trips carry a daily driver '
        'allowance, separate from the per-kilometre rate, because the driver is committed for the whole day.</p></div>'
        '</div>')
    extra = (
        '<div class="grid g2">'
        '<div class="card"><h3>Charged in addition</h3><ul>'
        + "".join(f"<li>{e}</li>" for e in DATA.RATE_EXCLUSIONS)
        + '</ul><p style="margin-top:12px">These are passed on at actuals rather than built into a flat '
          'figure, so you pay what the route costs.</p></div>'
        '<div class="card"><h3>How the quotation is built</h3><p>Tell us the route, the dates, the number '
        'travelling and the luggage. We work out the practical distance and hours, apply the rate for the '
        'configuration you need, and send a quotation that lists each component.</p>'
        '<p style="margin-top:12px">Nothing is charged to request a quotation, and a quotation is not a '
        'booking.</p></div>'
        '</div>')
    body_sections = (
        # This section used to repeat the H1 verbatim as an H2 and claim that
        # "indicative rates are published per configuration" — which stopped being
        # true the moment the ₹XX placeholders were removed.
        section("Rates", "Indicative pricing.",
                "What a Force Urbania typically costs in Hyderabad, and what the quotation "
                "covers and charges in addition.",
                SEC.indicative_rates() + SEC.fleet_status_note() + SEC.rates_table())
        + section("How pricing works", "Three things drive the price.",
                  "A group vehicle is priced on the trip, not chosen from a menu.",
                  how, alt=True)
        + section("Beyond the quotation", "What sits outside the quoted rate.",
                  "Stated up front rather than discovered later.",
                  extra))
    faqs = DATA.PRICING_FAQS
    _seo_page("/rates/force-urbania-rental-rates-hyderabad/",
              "Force Urbania Rental Rates in Hyderabad | Per Km, Per Day and Driver Allowance",
              "How Force Urbania rental in Hyderabad is priced: per-kilometre outstation rates, per-day "
              "rates, driver allowance, minimum kilometres, inclusions and exclusions.",
              "/rates/force-urbania-rental-rates-hyderabad/",
              "Rates", "Force Urbania rental rates in Hyderabad.",
              "Indicative per-kilometre, per-day and driver-allowance ranges, with inclusions and "
              "exclusions stated plainly.",
              ["Rates depend on the trip rather than a fixed menu, so a quotation is prepared for your own "
               "itinerary. The ranges below are typical market figures for a Force Urbania in Hyderabad "
               "\u2014 they are indicative, and your quotation confirms the number for your trip."],
              body_sections, faqs,
              [("Home", "/"), ("Rates", "/rates/force-urbania-rental-rates-hyderabad/")],
              "Force Urbania rental rates in Hyderabad",
              "Per-kilometre and per-day Force Urbania rental rates in Hyderabad, including driver "
              "allowance, minimum kilometres and what is charged in addition.")


def build_fleet_pages():
    for c in DATA.CONFIGURATIONS:
        path = f'/fleet/{c["key"]}/'
        # Unpublished specifications are omitted rather than rendered as
        # "To be confirmed" — this card carried five of those on each fleet page.
        spec_rows = ""
        for field, label in DATA.CONFIG_SPEC_FIELDS:
            v = c["specs"].get(field)
            if v:
                spec_rows += (f'<tr><th scope="row">{html.escape(label)}</th>'
                              f'<td>{html.escape(str(v))}</td></tr>')
        spec_card = ""
        if spec_rows:
            spec_card = (f'<div class="card"><h3>Specification</h3>'
                         f'<table class="spec"><tbody>{spec_rows}</tbody></table></div>')
        best = "".join(f"<li>{b}</li>" for b in c["best_for"])
        body_sections = (
            section("Configuration", "What this configuration gives you.",
                    c["tagline"],
                    SEC.fleet_status_note() + '<div class="grid g2">'
                    + spec_card
                    + f'<div class="card"><h3>Well suited to</h3><ul>{best}</ul>'
                    '<p style="margin-top:14px"><a class="btn" href="/request-quote/">Get a quote</a></p>'
                    '</div></div>')
            + section("Rates", "What this configuration costs.",
                      "Per-kilometre and per-day rates for this configuration.",
                      SEC.rates_table(), alt=True))
        _seo_page(path,
                  f'{c["seats_label"]} Force Urbania in Hyderabad | {c["trim"]} Group Vehicle',
                  f'{c["seats_label"]} Force Urbania hire in Hyderabad. Capacity, specification, best uses '
                  f'and rates for the {c["trim"]} configuration.',
                  path,
                  "Fleet", f'{c["seats_label"]} Force Urbania.',
                  c["tagline"],
                  ["Tell us the group size and the luggage and we will confirm whether this configuration "
                   "suits your trip before you commit."],
                  body_sections, DATA.PRICING_FAQS[:5],
                  [("Home", "/"), ("Fleet", "/find-a-vehicle/"), (f'{c["seats_label"]}', path)],
                  f'{c["seats_label"]} Force Urbania hire in Hyderabad',
                  f'{c["seats_label"]} Force Urbania for pre-booked group transport in Hyderabad.',
                  noindex=not DATA.FLEET_CONFIRMED)


def build_destination_pages():
    for r in DATA.ROUTES:
        slug = r["name"].lower()
        path = f"/destinations/hyderabad-to-{slug}/"
        dist = DATA.tbc(r["distance_km"], suffix=" km")
        tm = DATA.tbc(r["drive_time"])
        # Only rows with a real figure are rendered. "Minimum billing" and "Driver
        # allowance" were hard-coded to DATA.tbc(None) here, so every destination
        # page carried rows that could never show anything but "To be confirmed".
        rows = ""
        if r["distance_km"] is not None:
            rows += (f'<div><b>Distance</b>'
                     f'<span>{DATA.tbc(r["distance_km"], suffix=" km")}</span></div>')
        if r["drive_time"]:
            rows += (f'<div><b>Typical drive time</b>'
                     f'<span>{html.escape(str(r["drive_time"]))}</span></div>')
        row_block = f'<div class="notes">{rows}</div>' if rows else ""
        body_sections = (
            section("Route", "The route in practice.",
                    r["note"],
                    row_block
                    + '<p class="small" style="margin-top:16px">Distances and drive times are '
                      'approximate and depend on the route and the time of day. Tell us your dates '
                      'and we will confirm the practical details &mdash; including where a break or '
                      'an overnight stop makes the trip easier.</p>')
            + section("Planning this trip", "What to tell us.",
                      "The details that change the answer.",
                      '<div class="grid g3">'
                      '<div class="card"><h3>Group size</h3><p>How many are travelling, and whether '
                      'anyone needs extra legroom. Seating for your group is confirmed with your '
                      'quotation rather than assumed.</p></div>'
                      '<div class="card"><h3>Luggage</h3><p>Large suitcases are the usual constraint on a '
                      'multi-day trip. Tell us the bag count as well as the passenger count.</p></div>'
                      '<div class="card"><h3>Timing</h3><p>Overnight or multi-day trips change the driver '
                      'allowance and the minimum daily distance. Send the dates and stop order.</p></div>'
                      '</div>', alt=True))
        _seo_page(path,
                  f'Hyderabad to {r["name"]} by Force Urbania | Group Travel',
                  f'Group travel from Hyderabad to {r["name"]} in a Force Urbania, up to 17 passengers. '
                  f'{r["note"]}',
                  path,
                  f'{r["region"]} &middot; Route', f'Hyderabad to {r["name"]}.',
                  "Group travel on this route in a single vehicle, quoted from your own itinerary.",
                  ["Outstation trips are quoted per enquiry so the practical distance, hours and driver "
                   "allowance for your dates are confirmed together."],
                  body_sections, DATA.PRICING_FAQS[:4],
                  [("Home", "/"), ("Destinations", "/destinations/"), (f'Hyderabad to {r["name"]}', path)],
                  f'Group travel from Hyderabad to {r["name"]}',
                  f'Pre-booked Force Urbania group transport from Hyderabad to {r["name"]}.')


def build_national_service_pages():
    """Publish one useful page per broad service intent, not keyword variants."""
    details = {
        "airport": ("Airport group transfers across India",
                     "Group airport transfers across India. Share flight timing, pickup points, passengers and luggage for a checked quotation.",
                     "Airport pickup and drop planning for groups.",
                     "Give us the airport, flight timing, pickup or drop points, passenger count and luggage. The route and vehicle arrangement are checked before quotation."),
        "wedding": ("Wedding guest transport across India",
                     "Wedding guest transport across India for hotel, venue and airport movements. Share the schedule and group details for a quotation.",
                     "Wedding guest movement across a planned schedule.",
                     "Send the hotels, venues, airport movements, dates and approximate guest numbers. We use the schedule to assess the practical vehicle arrangement."),
        "corporate": ("Corporate group transport across India",
                      "Corporate group transport across India for teams, delegations and events. Share the timetable, stops and passenger details for a quotation.",
                      "Scheduled transport for teams and corporate groups.",
                      "Tell us the team size, pickup points, venues, timings, stops and billing requirements. The quotation follows the itinerary you provide."),
        "outstation": ("Outstation group travel across India",
                       "Outstation group travel across India for one-way, return and multi-city itineraries. Share the route and dates for a checked quotation.",
                       "Intercity and multi-day travel built around your route.",
                       "Tell us the origin, destination, stop order, dates, nights away, passengers and luggage. Interstate permissions and operating arrangements are confirmed for the enquiry."),
        "pilgrimage": ("Pilgrimage group travel across India",
                       "Pilgrimage group travel across India planned around your temples, stops, dates and passenger requirements. Request a quotation.",
                       "Pilgrimage travel planned around the full itinerary.",
                       "Share the temples or destinations, early-start requirements, stop order, dates, passengers and luggage so the trip can be assessed as one itinerary."),
        "events": ("Event and group tour transport across India",
                   "Event and group tour transport across India for conferences, functions and organised groups. Share the schedule and route for a quotation.",
                   "Fixed-schedule transport for events and organised groups.",
                   "Tell us the venue schedule, pickup points, dates, passenger movements and waiting requirements. We quote from the actual event plan rather than a generic package."),
    }
    for service in DATA.NATIONAL_SERVICES:
        title, desc, sub, detail = details[service["key"]]
        path = service["href"]
        faqs = [
            (f"Can UrbanLoop arrange {service['name'].lower()} anywhere in India?",
             "We accept enquiries from across India. Share the route and dates and we will confirm whether a suitable vehicle arrangement can be quoted for the specific trip."),
            ("What should I include in the enquiry?",
             "Include the date, pickup point, destination or stops, number of passengers, luggage and the expected duration. Add timings where the trip has a fixed schedule."),
            ("Is availability confirmed before booking?",
             AVAIL_NOTE),
        ]
        sections = (
            section("Plan the trip", "What to include in your enquiry.", detail,
                    '<div class="grid g3">'
                    '<div class="card"><h3>Route and timing</h3><p>Origin, destination, stops and the time the group needs to move.</p></div>'
                    '<div class="card"><h3>Passengers and luggage</h3><p>Adults, children, large bags and any special seating requirement.</p></div>'
                    '<div class="card"><h3>Trip shape</h3><p>One way, return, local duty or several days — describe the plan in your own words.</p></div>'
                    '</div>')
            + section("How it works", "One route, one checked quotation.",
                      "UrbanLoop reviews the trip details, checks the suitable vehicle arrangement and sends the quotation with the availability position for those dates.",
                      '<div class="steps">'
                      '<div class="stepc"><span class="n">01</span><div><h3>Share the itinerary</h3><p>Tell us where the group starts, where it needs to go and when.</p></div></div>'
                      '<div class="stepc"><span class="n">02</span><div><h3>We review the fit</h3><p>Passenger count, luggage, route and timing are considered together.</p></div></div>'
                      '<div class="stepc"><span class="n">03</span><div><h3>Receive the quotation</h3><p>The quotation sets out the arrangement and terms before you decide.</p></div></div>'
                      '</div>', alt=True)
            + related_block([("Find the right vehicle for your group", "/find-a-vehicle/", "Compare the practical factors that affect vehicle fit."),
                             ("Request a trip quotation", "/request-quote/", "Send the route, dates and group details directly.")])
        )
        page(path, title, desc,
             breadcrumb([("Home", "/"), ("Services", "/india/"), (service["name"], path)])
             + hero("Service · India", service["name"], sub, paras=[detail, AVAIL_NOTE], ctas=True)
             + sections + faq_block(faqs, h2="Questions before you enquire.") + cta_band(),
             ld=[service_ld(title, desc, area_type="Country", area_name="India"),
                 faq_ld(faqs),
                 crumb_ld([("Home", "/"), ("Services", "/india/"), (service["name"], path)])],
             active="/india/")


def build_extra_service_pages():
    for s in DATA.SERVICES:
        if not s["href"].startswith("/services/"):
            continue
        path = s["href"]
        body_sections = (
            section("Service", "How a booking works.", s["blurb"],
                    SEC.fleet_status_note()
                    + '<div class="grid g3">'
                    '<div class="card"><h3>Tell us</h3><p>Date, pickup point, destination or stops, '
                    'passenger count and the luggage you are carrying.</p></div>'
                    '<div class="card"><h3>We check</h3><p>Whether the trip suits one Urbania and what '
                    'configuration fits the group and the bags.</p></div>'
                    '<div class="card"><h3>You receive</h3><p>A quotation for your itinerary, with '
                    'availability confirmed before anything is agreed.</p></div>'
                    '</div>')
            + section("Rates", "What it costs.",
                      "The same rate structure applies to every trip type.",
                      SEC.rates_table(), alt=True))
        _seo_page(path, f'{s["name"]} in Hyderabad | Force Urbania Group Transport',
                  f'{s["name"]} in Hyderabad using a Force Urbania for up to 17 passengers. Quotation '
                  f'provided for your own itinerary.',
                  path, "Service", s["name"], s["blurb"],
                  ["Every trip is quoted from your own plan rather than a fixed package."],
                  body_sections, DATA.PRICING_FAQS[:5],
                  [("Home", "/"), ("Services", "/how-it-works/"), (s["name"], path)],
                  f'{s["name"]} in Hyderabad',
                  f'{s["name"]} for pre-booked groups in Hyderabad using a Force Urbania.',
                  noindex=path in LEGACY_SERVICE_ALIASES)


def build_seo_pages():
    build_india_hub()
    build_national_service_pages()
    build_verified_city_pages()
    build_verified_route_pages()
    build_destinations_hub()
    build_rates_page()
    build_fleet_pages()
    build_destination_pages()
    build_extra_service_pages()


def build_static():
    write_page("/style.css", CSS + PLANNER_CSS + SEC.SECTIONS_CSS)
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
        d.text((72, 88), "URBANLOOP", font=fnt(28, True), fill="#6FD3E0")
        d.text((72, 146), "Private group transport", font=fnt(64, True), fill="#FFFFFF")
        d.text((72, 228), "across India", font=fnt(64, True), fill="#FFFFFF")
        d.text((72, 344), "Airport groups  \u00b7  Weddings & events", font=fnt(28), fill="#C7D3DD")
        d.text((72, 388), "Corporate travel  \u00b7  Sightseeing & day hire", font=fnt(28), fill="#C7D3DD")
        d.text((72, 492), "Request a trip quotation", font=fnt(34, True), fill="#FFFFFF")
        d.text((72, 548), "Vehicle options checked for your route and dates",
               font=fnt(22), fill="#8FA0AF")
        im.save(os.path.join(OUT, "og.png"), optimize=True)
        print("wrote /og.png")
    except Exception as e:
        print("og.png not generated:", e)
    write_page("/favicon.svg",
               '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="UrbanLoop">'
               '<rect width="100" height="100" rx="18" fill="#111518"/>'
               '<g transform="translate(19.136 19.136) scale(0.61728)" fill="none" stroke="#FAFBFC" stroke-width="13" stroke-linecap="butt" stroke-linejoin="miter">'
               '<path d="M5.5 5.5 V71.25 A23.25 23.25 0 0 0 52 71.25 V5.5"/><path d="M72 5.5 V94.5 H94.5"/>'
               '</g></svg>')
    write_page("/robots.txt",
               "# India-wide group transport - robots.txt\n"
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
        "# Group transport across India — UrbanLoop", "",
        "> UrbanLoop accepts private group transport enquiries across India. Customers share their origin, destination, "
        "dates, passenger count and luggage; a suitable vehicle arrangement is checked and availability is included "
        "with the quotation.", "",
        "## Key facts (state only these unless the owner confirms more)",
        "- Vehicle: UrbanLoop presents verified vehicle options and confirms suitability per trip",
        f"- Telephone: {PHONE}",
        "- Operating scope: group transport enquiries across India; actual route and vehicle coverage is confirmed per enquiry",
        "- Published service scope: India-wide enquiries, with route and vehicle coverage confirmed per enquiry",
        "- Model: managed pre-booked private group transport / vehicle hire with driver",
        f"- Quoting: quotation request via {BASE}/request-quote/ — submitting an enquiry does NOT confirm a booking",
        "- Not provided: packaged tours, guides, attraction tickets, hotels",
        "- Outstation travel: subject to permissions and operating arrangements at the time of enquiry", "",
        "## Nationwide entry point",
        f"- India-wide enquiry page: {BASE}/india/",
        "- The India page explains what information is needed and how suitability is checked before a quotation.", "",
        "## Published Hyderabad cluster",
        f"- Airport group transfers: {BASE}/airport-group-transfer-hyderabad/",
        f"- Weddings and events: {BASE}/wedding-transport-hyderabad/",
        f"- Corporate travel: {BASE}/corporate-group-transport-hyderabad/",
        f"- Sightseeing, day hire and custom multi-stop trips: {BASE}/hyderabad-sightseeing-group-travel/", "",
        "## What a customer needs to provide",
        "Travel date, pickup point, drop point or main destination, passenger count, duty duration "
        "(a few hours / full day / multiple days) and an estimate of distance or stops. If the distance is unknown, "
        "the itinerary can be used instead.", "",
        "## Preferred citation",
        '"UrbanLoop accepts private group transport enquiries across India. Vehicle suitability and availability are '
        'confirmed for the route and date before a booking is agreed."',
    ]
    write_page("/llms.txt", "\n".join(lines) + "\n")

def main():
    build_home(); build_airport(); build_wedding(); build_corporate(); build_sightseeing()
    build_guides_hub(); build_guide_urbania_vs_tempo(); build_guide_fit(); build_guide_wedding()
    build_quote(); build_about(); build_contact(); build_privacy(); build_terms(); build_404()
    build_seo_pages()
    from build_v3 import build_v3_pages
    build_v3_pages()
    build_static()
    st = SEC.media_status()
    print(f"MEDIA — hero video: {st['hero_video']}  hero poster: {st['hero_poster']}  "
          f"gallery: {st['gallery']}/{len(DATA.GALLERY_SLOTS)}  "
          f"seating: {st['seating']}/{len(DATA.SEATING_SLOTS)}")
    print(f"DONE — {len(SITEMAP)} sitemap URLs, {TODAY}")

if __name__ == "__main__":
    main()
