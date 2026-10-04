#!/usr/bin/env python3
"""
V3 information architecture — the pages added by the V3 prompt pack.

Each page owns ONE primary intent (no cannibalisation), carries a preset planner where the
spec requires preselection, and states only verified facts.
"""
from build_pages import (page, breadcrumb, section, hero, cta_band, faq_block, related_block,
                         vehicle_panel, planner_blocks, AVAIL_NOTE)
from build_ui import (BASE, BRAND, PHONE, PHONE_HREF, WHATSAPP, CITY, TODAY,
                      crumb_ld, faq_ld, service_ld, call_svg)

def planner_hero(eyebrow, h1, sub, preset, extra_paras=()):
    ps = "".join(f'<p class="lede" style="margin-top:14px">{p}</p>' for p in extra_paras)
    return ('<section><div class="wrap">'
            f'<span class="eyebrow">{eyebrow}</span><h1 style="margin-top:14px">{h1}</h1>'
            f'<p class="lede" style="margin-top:16px;font-size:clamp(17px,1.8vw,20px)">{sub}</p>{ps}'
            '</div></section>'
            '<section style="padding-top:0"><div class="wrap">'
            + planner_blocks(preset) + '</div></section>')

# ------------------------------------------------------------------ /find-a-vehicle/
def build_find_a_vehicle():
    faqs = [
        ("How do I know which vehicle my group needs?",
         "Start with the number of passengers including children, then the luggage. Luggage, not seat count, is what usually decides it: a vehicle that seats a group comfortably may not also carry everyone's large suitcases. Send both numbers and we will tell you what fits."),
        ("What vehicle do I need for my group?",
         "Vehicle fit depends on passengers, luggage, route and dates. Tell us the full requirement and we will recommend a suitable arrangement rather than assume from passenger count alone."),
        ("Can I request a specific vehicle?",
         "You can state a preference and we will take it into account. Preference is a request, not a guarantee — availability and suitability are confirmed before anything is agreed."),
        ("Do you have different vehicle options?",
         "Yes. UrbanLoop is positioned around suitable vehicle options rather than one fixed vehicle. The exact category and availability are checked for each route and date before a quotation is sent."),
    ]
    body = (breadcrumb([("Home", "/"), ("Find a vehicle", "/find-a-vehicle/")])
            + planner_hero(
                "Vehicle recommendation · India",
                "Find the right vehicle for your group size.",
                "Tell us how many are travelling and how much luggage there is. We will recommend what suits your trip — and say so honestly if one vehicle will not cover it.",
                "custom",
                ["Luggage is what most group plans get wrong. A vehicle that seats everyone may not also take everyone's large suitcases, so we ask for both numbers before recommending."])
            + section("Sizing", "How to work out what your group needs.",
                      "Group size is the easy part. These are the ranges people usually land in.",
                      '<div class="grid g3">'
                      '<div class="card"><h3>Smaller groups</h3><p>A compact configuration may be the most practical choice, especially for city transfers or lighter luggage.</p></div>'
                      '<div class="card"><h3>Medium-sized groups</h3><p>A premium configuration can provide a comfortable balance of passenger space and luggage room.</p></div>'
                      '<div class="card"><h3>Larger groups</h3><p>A large-group or extended configuration may be appropriate, subject to luggage and route review.</p></div>'
                      '<div class="card"><h3>Very large groups</h3><p>We may recommend more than one vehicle or a different category. Tell us the total requirement and we will explain the practical options.</p></div>'
                      '<div class="card"><h3>Heavy luggage</h3><p>Airport runs, wedding groups and multi-day trips carry far more baggage. Mention it at the enquiry stage, not on the day.</p></div>'
                      '<div class="card"><h3>Children and infants</h3><p>Count children in the passenger total. Mention infants separately, since they affect seating.</p></div>'
                      '</div>', alt=True)
            + section("Preference", "Vehicle preference is a request, not a booking.",
                      "You can tell us what you would prefer. What we can promise is that we will tell you honestly what is available for your dates.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>What we arrange</h3><ul><li>Verified vehicle categories matched to the enquiry</li>'
                      '<li>Pre-booked group transport across India</li><li>Exact arrangement confirmed before acceptance</li></ul></div>'
                      '<div class="card"><h3>What we may source</h3><ul>'
                      '<li>Other vehicle categories through third-party operators, as that network is built and verified</li>'
                      '<li>Never shown as available until verified and confirmed for your dates</li>'
                      '<li>Never presented as our own fleet</li></ul></div>'
                      '</div>')
            + related_block([("What vehicle fits 10\u201317 people?",
                              "/guides/group-vehicle-fit-guide/",
                              "The longer version, including how luggage changes the answer."),
                             ("Force Urbania vs Tempo Traveller",
                              "/guides/force-urbania-vs-tempo-traveller/",
                              "How the two group vehicles compare, and how to choose.")])
            + faq_block(faqs, h2="Vehicle size questions.")
            + cta_band("Not sure what you need?",
                       "Describe the trip and the group, and we will recommend rather than guess."))
    page("/find-a-vehicle/", "Find the Right Group Vehicle Across India | UrbanLoop",
         "Work out which vehicle arrangement suits your group size, luggage, route and dates across India.",
         body,
         ld=[service_ld("Group vehicle recommendation across India",
                        "Guidance on which vehicle arrangement suits a group of a given size and luggage requirement across India.",
                        area_type="Country", area_name="India"),
             faq_ld(faqs), crumb_ld([("Home", "/"), ("Find a vehicle", "/find-a-vehicle/")])],
         active="/find-a-vehicle/")

# ------------------------------------------------------------------ /force-urbania-hire-hyderabad/
def build_urbania_page():
    faqs = [
        ("Can I hire a Force Urbania in Hyderabad for one day?",
         "Yes — day hire is one of the trip types we quote for. Send the date, pickup point, the stops you want and the expected duration, and we will reply with a quotation. Availability is confirmed with the quotation."),
        ("How many people can travel in a Force Urbania?",
         "The suitable configuration depends on the exact vehicle, passenger count, luggage and route. Share the number of adults and children so seating can be confirmed for your group."),
        ("Can 17 people travel with luggage?",
         "Not necessarily with a full set of large suitcases as well. Luggage space depends on passenger numbers and bag sizes, so share both and suitability will be confirmed for your trip rather than assumed."),
        ("How does UrbanLoop arrange the vehicle?",
         "UrbanLoop checks verified operating vehicle options for the route and date. The exact vehicle arrangement and availability are confirmed before a quotation is accepted."),
        ("Can I see the vehicle before booking?",
         "Ask us. We will describe the vehicle, its seating and its current condition in writing with your quotation, and answer anything you want to check before you confirm."),
        ("What is not included?",
         "We provide the vehicle and the driver for the journeys described in your quotation. Attraction tickets, guides, hotels and packaged tours are not part of the service."),
    ]
    body = (breadcrumb([("Home", "/"), ("Force Urbania hire", "/force-urbania-hire-hyderabad/")])
            + planner_hero(
                "Force Urbania · India",
                "Force Urbania group transport across India.",
                "Force Urbania group transport for airport runs, weddings, corporate days, outstation travel and sightseeing, subject to route and date confirmation.",
                "custom",
                ["You can note Force Urbania as your preference in the planner. Preference is a request rather than a guarantee: availability is confirmed for your dates before anything is agreed."])
            + section("The vehicle", "What we are offering.",
                      "Stated plainly, without claims we cannot yet support with photographs or documentation.",
                      '<div class="grid g2"><div>' + vehicle_panel() + '</div>'
                      '<div class="card"><h3>Confirmed today</h3><ul>'
                      '<li>Make and model: Force Urbania</li>'
                      '<li>Seats: 17</li>'
                      '<li>Number of vehicles: one</li>'
                      f'<li>Telephone: {PHONE}</li>'
                      '<li>Service: pre-booked private group transport with a driver</li></ul>'
                      '<h3 style="margin-top:20px">Confirmed with your quotation</h3><ul>'
                      '<li>Vehicle documentation and permit status</li>'
                      '<li>Insurance cover applicable to your trip</li>'
                      '<li>Driver arrangement</li>'
                      '<li>Luggage capacity for your specific group</li>'
                      '<li>Terms, inclusions and exclusions</li></ul>'
                      '<p class="small" style="margin-top:14px">Written this way deliberately: anything that depends '
                      'on your specific trip is confirmed rather than assumed.</p></div></div>', alt=True)
            + section("Use cases", "Trips it suits.",
                      "The Urbania works best where a group wants to stay together for a planned journey.",
                      '<div class="grid g3">'
                      '<a class="card" href="/services/airport-group-transfers/"><h3>Airport group transfers</h3><p>Arrivals, departures and multiple pickups with luggage.</p></a>'
                      '<a class="card" href="/services/wedding-guest-transport/"><h3>Weddings and events</h3><p>Guest movement across a schedule, not a single trip.</p></a>'
                      '<a class="card" href="/services/corporate-group-transport/"><h3>Corporate travel</h3><p>Teams and delegations moving together on a timetable.</p></a>'
                      '<a class="card" href="/services/outstation-group-travel/"><h3>Outstation trips</h3><p>Intercity and multi-day travel, subject to permissions and arrangements.</p></a>'
                      '<a class="card" href="/india/"><h3>Sightseeing and day hire</h3><p>Multi-stop city travel on your own itinerary.</p></a>'
                      '<a class="card" href="/india/"><h3>Family trips</h3><p>Family groups travelling together with children and luggage.</p></a>'
                      '</div>')
            + faq_block(faqs, h2="Force Urbania questions.")
            + cta_band())
    page("/force-urbania-hire-hyderabad/", "Force Urbania Group Transport Across India | UrbanLoop",
         "Request Force Urbania group transport across India. Share your route, dates, group size and luggage for a checked quotation.",
         body,
         ld=[service_ld("Force Urbania group transport across India",
                        "Force Urbania group transport with a driver for pre-booked private group trips across India. Quotation on request.", area_type="Country", area_name="India"),
             faq_ld(faqs), crumb_ld([("Home", "/"), ("Force Urbania hire", "/force-urbania-hire-hyderabad/")])],
         active="/find-a-vehicle/")

# ------------------------------------------------------------------ /outstation-group-travel-hyderabad/
def build_outstation():
    faqs = [
     ("Can you do outstation trips from Hyderabad?",
      "Outstation travel depends on the permissions and the operating arrangements that apply at the time of your enquiry. Tell us the route and the dates and we will confirm whether we can quote for it rather than assuming."),
     ("How is an outstation trip priced?",
      "A quotation is prepared for each enquiry based on the route, the number of days, the distance and the date. Terms covering tolls, parking, driver allowance and overnight arrangements are set out in the quotation."),
     ("How many days can we book?",
      "Multi-day trips are quoted for the whole period. Tell us the depart date, the return date and what the vehicle needs to do on each day."),
     ("Can we stop on the way?",
      "Yes. List the stops and we will plan the route and the timing around them. Anything that changes the duration or the distance is reflected in your quotation."),
     ("What about overnight stays?",
      "Tell us how many nights and where the vehicle should be. Overnight arrangements and any associated charges are set out in your quotation."),
     ("Is the vehicle available for a one-way drop?",
      "One-way, round trip and multi-city shapes are all quoted. Tell us which you need in the planner."),
     ("Do you operate outside Telangana?",
      "Interstate travel depends on the permits and arrangements that apply for the specific route and dates. Ask us and we will confirm for your trip."),
    ]
    body = (breadcrumb([("Home", "/"), ("Outstation group travel", "/outstation-group-travel-hyderabad/")])
            + planner_hero(
                "Outstation · group travel · " + CITY,
                "Outstation group travel from Hyderabad.",
                "Intercity and multi-day trips for groups, quoted on the route and the number of days rather than a fixed rate card.",
                "outstation",
                ["Outstation travel depends on the permissions and operating arrangements that apply at the time, so we confirm before quoting rather than afterwards."])
            + section("Planning", "What an outstation enquiry needs.",
                      "The route and the dates matter more than anything else here.",
                      '<div class="grid g3">'
                      '<div class="card"><h3>Trip shape</h3><p>One way, round trip or multi-city. Multi-city changes the route and the day count.</p></div>'
                      '<div class="card"><h3>Date range</h3><p>Departure and return date, with the trip length shown in days and nights.</p></div>'
                      '<div class="card"><h3>Stops</h3><p>Places you want to break the journey at, in the order you would like.</p></div>'
                      '<div class="card"><h3>Nights away</h3><p>How many nights and where the vehicle should be overnight.</p></div>'
                      '<div class="card"><h3>Group and luggage</h3><p>Passenger count and baggage — multi-day trips carry more than day trips.</p></div>'
                      '<div class="card"><h3>Distance</h3><p>If you know it, tell us. If not, the route is enough for us to work it out.</p></div>'
                      '</div>', alt=True)
            + section("Terms", "What the quotation sets out.",
                      "Outstation pricing has more variables than a city trip, so the terms are stated in the quotation rather than assumed.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>The quotation covers</h3><ul>'
                      '<li>The vehicle and driver for the route and days described</li>'
                      '<li>How tolls and parking are handled</li>'
                      '<li>Driver allowance and overnight arrangements</li>'
                      '<li>Any interstate or permit-related charges that apply</li></ul></div>'
                      '<div class="card"><h3>Before you confirm</h3><ul>'
                      '<li>Availability for your dates</li>'
                      '<li>Whether the route is one we can operate</li>'
                      '<li>What is included and what is additional</li>'
                      '<li>Payment and cancellation terms</li></ul></div>'
                      '</div>')
            + related_block([("Force Urbania hire in Hyderabad",
                              "/force-urbania-hire-hyderabad/",
                              "The vehicle, and what suits a long-distance group trip."),
                             ("What vehicle fits a group of 10\u201317?",
                              "/guides/group-vehicle-fit-guide/",
                              "Multi-day trips carry more luggage — check the fit before you commit.")])
            + faq_block(faqs, h2="Outstation questions.")
            + cta_band("Planning an outstation trip?",
                       "Give us the route and dates and we will confirm whether we can operate it before quoting."))
    page("/outstation-group-travel-hyderabad/", "Outstation Group Travel from Hyderabad | 17-Seater Hire",
         "Outstation and multi-day group travel from Hyderabad with a 17-seat Force Urbania. One-way, round trip and multi-city. Request a quotation with your route and dates.",
         body,
         ld=[service_ld("Outstation group travel from Hyderabad",
                        "Intercity and multi-day group transport from Hyderabad using a 17-seat Force Urbania, subject to permissions and arrangements applicable at the time of enquiry."),
             faq_ld(faqs), crumb_ld([("Home", "/"), ("Outstation group travel", "/outstation-group-travel-hyderabad/")])],
         active="/outstation-group-travel-hyderabad/")

# ------------------------------------------------------------------ /family-group-travel-hyderabad/
def build_family():
    faqs = [
     ("What is the best way to move a family group in Hyderabad?",
      "If the family is larger than a car can take and everyone wants to arrive together, a single group vehicle is usually the simplest answer. If the group is small and the trips are short, two cars can also work. Tell us the numbers and we will say which makes more sense."),
     ("Can you carry children and infants?",
      "Yes, and we ask you to count them in the passenger total and mention infants separately so seating can be confirmed. Any child-seat requirement should be raised at the enquiry stage so it can be confirmed rather than assumed."),
     ("Where does the luggage go?",
      "Luggage space depends on how many passengers are travelling and the size of the bags. Family trips often include prams or bulky items, so tell us and suitability will be confirmed for your trip."),
     ("Can we make several stops?",
      "Yes. Family trips often involve collecting people from more than one address before heading out. List the pickups and we will plan a sensible order."),
     ("Can we book for a full day or a weekend?",
      "Yes. Day hire and multi-day family trips are both quoted, based on the itinerary and the duration."),
     ("Is there anything for the children to do during the trip?",
      "We provide the vehicle and the driver for the journey. We do not provide entertainment, guides or activity bookings."),
    ]
    body = (breadcrumb([("Home", "/"), ("Family group travel", "/family-group-travel-hyderabad/")])
            + planner_hero(
                "Family trips · " + CITY,
                "Family group travel in Hyderabad.",
                "One vehicle so the family arrives together — with room planned for luggage, prams and children rather than discovered on the day.",
                "family",
                ["Tell us the adults, the children and the luggage. Family trips are the ones where baggage most often changes the answer."])
            + section("Planning", "What family trips usually involve.",
                      "Practical points, in the order they cause problems.",
                      '<div class="grid g3">'
                      '<div class="card"><h3>Everyone together</h3><p>One vehicle means the family arrives at the same time and no one is following a cab driver across the city.</p></div>'
                      '<div class="card"><h3>Luggage and prams</h3><p>Bulky items are the usual surprise. Mention them at the enquiry stage.</p></div>'
                      '<div class="card"><h3>Multiple pickups</h3><p>Collecting relatives from two or three addresses before setting off.</p></div>'
                      '<div class="card"><h3>Children and seating</h3><p>Count children in the total, and mention infants and any child-seat requirement.</p></div>'
                      '<div class="card"><h3>Day trips and weekends</h3><p>Full-day outings and multi-day family travel are quoted the same way as any other trip.</p></div>'
                      '<div class="card"><h3>Return planning</h3><p>Tell us whether you need the return leg as well, so both are quoted once.</p></div>'
                      '</div>', alt=True)
            + related_block([("What vehicle fits a group of 10\u201317?",
                              "/guides/group-vehicle-fit-guide/",
                              "The luggage question, explained — and why it decides most family trips."),
                             ("Sightseeing &amp; day trips",
                              "/hyderabad-sightseeing-group-travel/",
                              "Planning a family day out with several stops.")])
            + faq_block(faqs, h2="Family trip questions.")
            + cta_band("Travelling with the family?",
                       "Send the numbers and the luggage and we will tell you honestly what fits."))
    page("/family-group-travel-hyderabad/", "Family Group Travel Hyderabad | 17-Seater for Families",
         "Family group travel in Hyderabad with a 17-seat Force Urbania. Plan for children, luggage and prams, with multiple pickups. Request a trip quotation.",
         body,
         ld=[service_ld("Family group travel in Hyderabad",
                        "Pre-booked group transport for family groups travelling together in and around Hyderabad, using a 17-seat Force Urbania. Quotation on request."),
             faq_ld(faqs), crumb_ld([("Home", "/"), ("Family group travel", "/family-group-travel-hyderabad/")])],
         active="/family-group-travel-hyderabad/")

# ------------------------------------------------------------------ /how-it-works/
def build_how():
    faqs = [
     ("How long does it take to get a quotation?",
      "We aim to respond promptly, but we do not publish a guaranteed response time because it depends on enquiry volume. If your trip is time-critical, call " + PHONE + "."),
     ("What information do you need from me?",
      "Your trip type, the route, the dates, the number of passengers and the luggage position. The planner asks for exactly that and nothing more than your trip needs."),
     ("Why can you not show availability straight away?",
      "Because we operate one vehicle and confirm suitability per trip. A live availability display would imply a fleet we do not have."),
     ("What happens if the Urbania does not suit my trip?",
      "We will tell you. Where we can source a suitable option through another operator we will say so; where we cannot, we will say that too rather than leave you waiting."),
     ("When is a booking actually confirmed?",
      "Only after you accept the quotation and the payment terms are met. Sending an enquiry does not reserve the vehicle."),
     ("How is the price decided?",
      "By the trip type, the route, the duration or the number of days, and the date. A quotation is prepared for your actual itinerary rather than a published rate card."),
    ]
    steps = ("""<div class="pl-veh">
<div class="pl-vcard"><b>1. Tell us the trip</b><p class="small" style="margin-top:8px">Trip type, route, dates, passengers and luggage. The planner takes about two minutes.</p></div>
<div class="pl-vcard"><b>2. We check fit and availability</b><p class="small" style="margin-top:8px">We look at whether your trip suits the 17-seat Urbania, and whether it is free on your dates. If it is not suitable, we say so.</p></div>
<div class="pl-vcard"><b>3. You receive a quotation</b><p class="small" style="margin-top:8px">A price for the trip you described, with the inclusions, exclusions and terms stated.</p></div>
<div class="pl-vcard feat"><b>4. Confirm</b><p class="small" style="margin-top:8px">A booking exists only once you accept the quotation. Until then nothing is reserved.</p></div>
</div>""")
    body = (breadcrumb([("Home", "/"), ("How it works", "/how-it-works/")])
            + hero("How it works",
                   "Four steps from enquiry to confirmed trip.",
                   "No instant booking, because there is one vehicle and availability has to be checked. What that means in practice is that a person looks at your trip rather than an algorithm.",
                   ctas=False)
            + section("The process", "What happens after you send your details.",
                      "Every trip request follows the same four steps.",
                      steps)
            + section("Why it works this way", "An honest process rather than a booking engine.",
                      "These are deliberate choices, not missing features.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>Why no instant booking</h3><p>A live calendar would imply a fleet. We have one vehicle, so availability is a real question each time and is answered by a person.</p></div>'
                      '<div class="card"><h3>Why we ask so much</h3><p>Route, dates, passengers and luggage all change the answer. Asking once is faster than quoting twice.</p></div>'
                      '<div class="card"><h3>Why we say no</h3><p>If a group is too large, the luggage will not fit, or the route carries requirements we cannot meet, we would rather say so than take a trip we cannot deliver.</p></div>'
                      '<div class="card"><h3>Your details</h3><p>Used to prepare your quotation and reply to you. Nothing else — see the privacy notice.</p></div>'
                      '</div>', alt=True)
            + faq_block(faqs, h2="Process questions.")
            + cta_band("Ready to send your trip details?",
                       "The planner asks only for what your trip type needs."))
    page("/how-it-works/", "How It Works | Group Travel Enquiry to Quotation",
         "How a group travel enquiry works here: tell us the trip, we check fit and availability, you receive a quotation, and a booking is confirmed only after you accept it.",
         body,
         ld=[faq_ld(faqs), crumb_ld([("Home", "/"), ("How it works", "/how-it-works/")])],
         active="/how-it-works/")

# ------------------------------------------------------------------ /partner-with-us/
def build_partner():
    faqs = [
     ("What kind of operators are you looking for?",
      "Commercial operators in and around Hyderabad with vehicles suitable for group travel — Traveller, MPV/SUV, minibus and bus categories, as well as additional Urbania capacity."),
     ("Do you have partners already?",
      "No. This page is an open invitation, not a claim that a network exists. Nothing is presented as a partnership until an operator has been verified and supplied under agreed terms."),
     ("What information will you ask for?",
      "Business identity, vehicle documentation, permit, insurance and fitness, driver arrangements, service history and the categories you can genuinely cover."),
     ("Will my vehicles appear on the website?",
      "Not as live inventory. Categories may be referred to as options we can request. Individual vehicles are not advertised as available, because we are not displaying a live fleet."),
     ("How would work be allocated?",
      "On suitability and reliability for the specific trip, not on the lowest price alone. Fit, compliance and dependability come first."),
     ("How do I get in touch?",
      f"Call {PHONE} or email with your business name, the vehicle categories you operate and the areas you cover."),
    ]
    body = (breadcrumb([("Home", "/"), ("Partner with us", "/partner-with-us/")])
            + hero("Operators &amp; suppliers",
                   "Partner with us.",
                   "We operate one 17-seat Force Urbania. As demand grows beyond what a single vehicle can cover, we want to work with verified local operators rather than turn enquiries away.",
                   paras=["This is an invitation, not an announcement. We have no partner network to advertise yet, and we will not describe one until operators are verified and supplying."],
                   ctas=False)
            + section("Who we are looking for", "Categories we expect to need.",
                      "Stated as categories we may request, never as available inventory.",
                      '<div class="grid g3">'
                      '<div class="card"><h3>Force Urbania</h3><p>Additional 17-seat capacity for periods when our own vehicle is committed.</p></div>'
                      '<div class="card"><h3>Tempo Traveller</h3><p>Group travel across a range of seating configurations.</p></div>'
                      '<div class="card"><h3>MPV / SUV</h3><p>Smaller groups, airport runs and executive movement.</p></div>'
                      '<div class="card"><h3>Minibus</h3><p>Groups larger than a single group vehicle can carry.</p></div>'
                      '<div class="card"><h3>Bus</h3><p>Large groups, events and corporate movement.</p></div>'
                      '<div class="card"><h3>Wedding and event fleets</h3><p>Operators used to multi-vehicle guest movement across a schedule.</p></div>'
                      '</div>', alt=True)
            + section("Verification", "What we check before sending work.",
                      "We would rather have a small verified list than a long unverified one — and the same standard applies to what we tell customers about our own vehicle.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>Business and vehicles</h3><ul>'
                      '<li>Registered business identity</li>'
                      '<li>Vehicle registration and documentation</li>'
                      '<li>Commercial permit applicable to the routes</li>'
                      '<li>Insurance and fitness certification</li>'
                      '<li>Driver licensing and arrangements</li></ul></div>'
                      '<div class="card"><h3>Working together</h3><ul>'
                      '<li>Reliability and response, tracked over time</li>'
                      '<li>Service fit for group and event travel</li>'
                      '<li>Agreed terms, inclusions and exclusions</li>'
                      '<li>Documented validity dates, rechecked on expiry</li></ul></div>'
                      '</div>')
            + faq_block(faqs, h2="Partner questions.")
            + cta_band("Operate group vehicles in Hyderabad?",
                       "Tell us what you run and where, and we will start with verification rather than promises. "
                       f"Call {PHONE} or use the contact page."))
    page("/partner-with-us/", "Partner With Us | Group Transport Operators, Hyderabad",
         "Invitation for verified Hyderabad transport operators — Urbania, Traveller, MPV/SUV, minibus and bus categories. Verification requirements and how work is allocated.",
         body,
         ld=[faq_ld(faqs), crumb_ld([("Home", "/"), ("Partner with us", "/partner-with-us/")])],
         active="")

def build_expect():
    """Genuine trust content that does not depend on owner-supplied facts."""
    faqs = [
     ("How is the price worked out?",
      "A quotation is built from the trip type, the route and distance, how long the vehicle is needed or how many days, and the date. Anything with a fixed cost — tolls, parking, a driver allowance for an overnight stay — is stated separately in the quotation so you can see what you are paying for rather than a single unexplained figure."),
     ("Why can I not see prices on the site?",
      "Because a group trip has too many variables for an honest headline rate. A two-hour city run, an airport transfer with sixteen people and heavy luggage, and a three-day outstation trip to Chennai are not the same product. A published rate card would either be padded for the worst case or wrong for most enquiries."),
     ("What do you confirm before I pay anything?",
      "Whether your trip is suitable for the 17-seat Urbania, whether the vehicle is free on your dates, the full price with inclusions and exclusions, and the terms that apply if plans change."),
     ("What happens if the vehicle breaks down?",
      "It is dealt with as a breakdown, and the honest answer is that the remedy depends on where and when it happens. Ask us to set out in the quotation what happens in that event, and do not accept a verbal assurance — it should be written down before you confirm."),
     ("What if I need to cancel or change the date?",
      "Cancellation and change terms depend on the trip and the date, so they are stated in your quotation rather than in a blanket policy. Ask for them in writing before you pay."),
     ("What if we are running late on the day?",
      "Extensions beyond the agreed duty are handled as set out in your quotation. The cleanest way to avoid a surprise is to tell us the realistic timing up front, including buffer for a wedding or an event that rarely runs to schedule."),
     ("What is not included?",
      "Attraction tickets, guides, hotels, meals and packaged tour services. We provide the vehicle and the driver for the journeys described — nothing else is implied."),
     ("Who do I deal with if something goes wrong?",
      "The same person who quotes your trip. There is no call centre and no account manager in between."),
    ]
    body = (breadcrumb([("Home", "/"), ("What to expect", "/what-to-expect/")])
            + hero("Straight answers",
                   "What to expect, and what we will not pretend to know.",
                   "Most transport websites answer these questions with silence or a generic policy. Here is what we can tell you, and what must be confirmed in writing for your specific trip.",
                   paras=["This page exists because a quotation you cannot interrogate is not worth much. Everything below is either how we work, or something you should insist on seeing in writing before you pay."],
                   ctas=False)
            + section("Pricing", "How a price is actually built.",
                      "Four things drive the number, and none of them can be guessed from a website.",
                      '<div class="grid g4">'
                      '<div class="card"><h3>Route and distance</h3><p>Where you are going, and how far the vehicle has to travel to get you there and back.</p></div>'
                      '<div class="card"><h3>Duration</h3><p>Hours for a city trip, days for outstation travel. The vehicle is committed for the whole period.</p></div>'
                      '<div class="card"><h3>Fixed costs</h3><p>Tolls, parking and overnight driver arrangements, which we itemise rather than bury.</p></div>'
                      '<div class="card"><h3>The date</h3><p>Peak wedding and festival dates affect availability and price, the same as they do for anything else in short supply.</p></div>'
                      '</div>')
            + section("Before you pay", "What should be in writing before you confirm.",
                      "Ask for all of this. If any of it is missing, ask again.",
                      '<div class="grid g2">'
                      '<div class="card"><h3>In the quotation</h3><ul>'
                      '<li>The full price, with what is included and what is extra</li>'
                      '<li>How tolls and parking are treated</li>'
                      '<li>The permitted duty window and what overtime costs</li>'
                      '<li>Cancellation and date-change terms</li>'
                      '<li>Payment terms and timing</li></ul></div>'
                      '<div class="card"><h3>About the vehicle and driver</h3><ul>'
                      '<li>Vehicle documentation and permit status for the trip</li>'
                      '<li>Insurance cover that applies</li>'
                      '<li>The driver arrangement</li>'
                      '<li>Luggage capacity confirmed for your group, in writing</li></ul></div>'
                      '</div>', alt=True)
            + section("When things go wrong", "Plans change. Here is the honest position.",
                      "We would rather set expectations now than explain afterwards.",
                      '<div class="grid g3">'
                      '<div class="card"><h3>Running late</h3><p>Tell us the realistic timing up front. Weddings and events rarely run to schedule, and a buffer agreed in advance costs less than an argument on the night.</p></div>'
                      '<div class="card"><h3>Breakdown or delay</h3><p>The remedy depends on where and when it happens. Ask for it to be set out in writing, and do not accept a verbal assurance.</p></div>'
                      '<div class="card"><h3>Changes on the day</h3><p>Small changes are usually workable. Anything that extends the duty or changes the route is reflected in the terms you agreed.</p></div>'
                      '<div class="card"><h3>A trip we cannot do</h3><p>If the group is too large, the luggage will not fit, or the route carries requirements we cannot meet, we will say so before you commit rather than after.</p></div>'
                      '<div class="card"><h3>If we cannot source a vehicle</h3><p>Where the Urbania does not suit your trip, we will tell you. If we can find a suitable option through a verified operator we will say so; if we cannot, we will say that too.</p></div>'
                      '<div class="card"><h3>Your data</h3><p>Used to prepare your quotation and reply to you. Not sold, not rented, not added to a marketing list. See the privacy notice.</p></div>'
                      '</div>')
            + faq_block(faqs, h2="The questions most sites avoid.")
            + cta_band("Still unsure about something?",
                       "Ask before you enquire. A straight answer costs nothing and saves both of us time."))
    page("/what-to-expect/", "What to Expect | Group Trip Pricing, Terms and Changes",
         "How group trip pricing is built, what must be confirmed in writing before you pay, and what happens if plans change. Straight answers for Hyderabad group travel.",
         body,
         ld=[faq_ld(faqs), crumb_ld([("Home", "/"), ("What to expect", "/what-to-expect/")])],
         active="")

def build_v3_pages():
    build_find_a_vehicle(); build_urbania_page(); build_outstation()
    build_family(); build_how(); build_partner(); build_expect()
    print("V3 pages built")
