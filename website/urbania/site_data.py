#!/usr/bin/env python3
"""
UrbanLoop — single editable content source for pan-India group transport.

WHY THIS FILE EXISTS
Every figure, spec and label that the owner may need to change lives here, not
scattered through page templates. The brief asks that configurations, rates and
recommendation rules stay "easy to edit" — this is that seam.

THE HONESTY RULE
Nothing here invents a fact. Any value the owner has not supplied is None, and
templates render it through `tbc()` as a visible "To be confirmed" token. A
placeholder must never render as a plausible-looking number, because a made-up
rate or seat count on a customer-facing page is a false claim.

FLEET_CONFIRMED gates the whole fleet/rates story. See docs/IMPROVEMENT_PLAN.md:
the brief lists four configurations while the live FACTS_LEDGER and the current
site describes verified vehicle categories and checks the exact arrangement per enquiry.
vehicles actually exist.
"""

# --------------------------------------------------------------------- flags
# Owner must confirm which Urbania configurations actually exist. Until then the
# configuration and rate sections publish their ARCHITECTURE (layout, guidance,
# indexable headings) but show to-be-confirmed values instead of asserting a
# fleet. See docs/IMPROVEMENT_PLAN.md.
FLEET_CONFIRMED = True

# Media provenance. Dropping a file into app/site/media/ does NOT by itself mean it
# is a photograph of the owner's own vehicle. Set this True only for imagery of the
# actual vehicle; while False, supplied media is captioned as representative of the
# Force Urbania model rather than as this business's vehicle.
ASSETS_ARE_OUR_VEHICLE = False

# Media placeholders. The gallery and seating grids can render a dashed box for
# every slot that has no photo yet, printing the exact filename the build expects
# (e.g. "gallery/exterior-rear.jpg"). That is a useful SHOT LIST for the owner and
# a confusing, unfinished-looking mess for a customer — it publishes build state on
# a marketing page. So it is off by default and the public page shows only real
# photos plus a plain "being prepared" line.
# Turn this on to see, on any page, exactly which files the build is waiting for.
SHOW_MEDIA_PLACEHOLDERS = False

# ------------------------------------------------------- indicative pricing
# CATEGORY B — reversible commercial content. Market-researched 2026-10-03 from live
# Hyderabad-facing operator rate cards (chikucabs, chikucab, 24cabservice,
# actempotravellerhire, rajputanacabs, hyderabadwheels, rinocab, mebus) with
# Delhi-sourced cards deliberately excluded. See RATE_INDICATIVE_SOURCES.
#
# These are INDICATIVE MARKET FIGURES, not UrbanLoop's own contract rates. Every
# surface that renders them says so and states that the quotation confirms the
# figure for the actual trip. Replace with the owner's rate card when supplied —
# nothing else needs to change.
RATE_INDICATIVE = [
    dict(label="Local / city travel", unit="per km", low=30, high=40,
         note="Charged per kilometre against a minimum. Time-and-distance packages are "
              "common for a full day in the city."),
    dict(label="Outstation travel", unit="per km", low=30, high=45,
         note="A minimum of 250&ndash;300 km per day applies even on shorter runs, because "
              "the vehicle and driver are committed for the day."),
    dict(label="Full day &mdash; 8 hours / 80 km", unit="per day", low=6800, high=10000,
         note="A 17-seat configuration sits at the top of this range. Extra hours and extra "
              "kilometres are charged beyond the package."),
    dict(label="Driver allowance", unit="per day", low=500, high=800,
         note="Applies to outstation and overnight trips. Some operators include it in the "
              "package instead of billing it separately."),
    dict(label="Airport transfer", unit="one way", low=4000, high=4500,
         note="Indicative for a van pick-up or drop. Most Hyderabad operators quote airport "
              "runs per kilometre rather than as a flat route fare."),
]

# Where the indicative figures came from. Kept beside the data so these are auditable
# and re-checkable rather than numbers of unknown origin.
RATE_INDICATIVE_SOURCES = {
    "local_per_km": "chikucabs.com 30-35; chikucab.com 38-40; 24cabservice.com 37-39; actempotravellerhire.com 34-40 (outliers rinocab 25, sara.cab 45 excluded)",
    "outstation_per_km": "rajputanacabs.in 32-40; actempotravellerhire.com 34-45; 24cabservice.com 35-39; chikucab.com 38-40",
    "full_day": "hyderabadwheels.com 6825 incl. taxes; actempotravellerhire.com 8000 (9-10 str) to 10000 (17 str); rajputanacabs.in 8000",
    "driver_allowance": "chikucab/chikucabs 500; rinocab 500; actempotravellerhire.com 600-700; mebus.in 800; clearcarrental.com 800",
    "airport": "actempotravellerhire.com 4000 (9-10 str) to 4500 (13-17 str) — WEAKEST FIGURE: only one van-specific flat rate found",
    "gst": "5% standard contract-carriage rate — chikucab.com, actempotravellerhire.com, destinytraveller.com",
    "night_allowance": "chikucab.com 500; 24cabservice.com 800 after 8pm; bookmytempotraveller.com 300-350",
}

TBC = "To be confirmed"


def tbc(value, prefix="", suffix=""):
    """Render an unconfirmed value honestly.

    None  -> 'To be confirmed'  (never a fabricated number)
    0 or a real value -> formatted as given

    The unit is kept on the placeholder branch too, so an unset distance still
    reads 'To be confirmed km' rather than silently losing what it measures.
    """
    if value is None:
        return f"{prefix}{TBC}{suffix}"
    return f"{prefix}{value}{suffix}"


def money(value):
    """Rupee figure. Renders '₹XX' when unset, never a guessed figure.

    Numbers are grouped (6800 -> 6,800) so larger figures are readable. Plain comma
    grouping, which matches Indian convention below one lakh; every figure on the
    site is currently under 10,000, so lakh-style grouping does not arise.
    """
    if value is None:
        return "&#8377;XX"
    if isinstance(value, bool):
        return f"&#8377;{value}"
    if isinstance(value, int) or (isinstance(value, float) and float(value).is_integer()):
        return "&#8377;" + format(int(value), ",")
    return f"&#8377;{value}"


# --------------------------------------------------------------------- fleet
# Passenger capacity per the owner's brief. seat_layout and trim mirror the
# convention the Indian market uses (1x1 vs 2x1, Deluxe/Premium/Luxury).
# Specs are intentionally None: the owner has not supplied them.
CONFIGURATIONS = [
    dict(
        key="luxury-maharaja",
        name="Luxury / Maharaja",
        seats_label="Compact configuration",
        seats_min=9, seats_max=10,
        seat_layout="1x1",
        trim="Luxury / Maharaja",
        tagline="The most comfortable way to move a small group.",
        best_for=["Executive delegations", "VIP guest transfers",
                  "Family trips where comfort matters", "Small wedding parties"],
        specs=dict(seat_type=None, ac=None, charging=None, luggage=None, amenities=None),
        per_km=None, per_day=None, driver_allowance=None, min_km_per_day=None,
        photo_dir="/img/fleet/luxury-maharaja/",
    ),
    dict(
        key="premium-12",
        name="Premium",
        seats_label="Premium configuration",
        seats_min=12, seats_max=13,
        seat_layout="2x1",
        trim="Premium",
        tagline="Premium seating with room to spread out.",
        best_for=["Corporate groups", "Wedding guest transport",
                  "Airport group transfers", "Multi-day family tours"],
        specs=dict(seat_type=None, ac=None, charging=None, luggage=None, amenities=None),
        per_km=None, per_day=None, driver_allowance=None, min_km_per_day=None,
        photo_dir="/img/fleet/premium-12/",
    ),
    dict(
        key="seater-16",
        name="Standard",
        seats_label="Large-group configuration",
        seats_min=16, seats_max=16,
        seat_layout="2x1",
        trim="Deluxe",
        tagline="A practical option for a larger group.",
        best_for=["Outstation group travel", "Pilgrimage tours",
                  "Corporate off-sites", "Event and conference groups"],
        specs=dict(seat_type=None, ac=None, charging=None, luggage=None, amenities=None),
        per_km=None, per_day=None, driver_allowance=None, min_km_per_day=None,
        photo_dir="/img/fleet/seater-16/",
    ),
    dict(
        key="seater-17",
        name="Standard",
        seats_label="Extended configuration",
        seats_min=17, seats_max=17,
        seat_layout="2x1",
        trim="Deluxe",
        tagline="For larger groups, subject to route and luggage review.",
        best_for=["Large family groups", "Wedding guest movement",
                  "Group tours", "Corporate team travel"],
        specs=dict(seat_type=None, ac=None, charging=None, luggage=None, amenities=None),
        per_km=None, per_day=None, driver_allowance=None, min_km_per_day=None,
        photo_dir="/img/fleet/seater-17/",
    ),
]

# Attributes shown on every configuration card. Order matters — capacity first,
# because that is how a customer picks a vehicle.
CONFIG_SPEC_FIELDS = [
    ("seat_type", "Seat type"),
    ("ac", "Air conditioning"),
    ("charging", "Charging points"),
    ("luggage", "Luggage space"),
    ("amenities", "Amenities"),
]


# ------------------------------------------------------- group-size selector
# "Find Your Urbania". Editable recommendation rules — change these without
# touching a template.
def recommend(passengers):
    """Return (config_key, headline, detail) for a passenger count.

    Keep customer-facing recommendations useful without publishing awkward or
    unverified seat-count labels. Exact capacity and luggage fit are confirmed
    from the operating vehicle offered for the enquiry.
    """
    if passengers is None:
        return None, "Tell us your group size", ""
    if passengers > 16:
        return "seater-17", "Extended configuration", "Suitable for a larger group, subject to the exact vehicle and luggage requirement."
    if passengers > 13:
        return "seater-16", "Large-group configuration", "A practical starting point for a larger group with normal luggage."
    if passengers > 10:
        return "premium-12", "Premium configuration", "A comfortable starting point for a medium-sized group."
    return "luxury-maharaja", "Compact configuration", "A comfortable starting point for a smaller group."


# --------------------------------------------------------------------- rates
# Structure follows the one reference site that publishes rates at all. Their
# Delhi figures are NOT reused; ours are unset until the owner supplies them.
RATE_TABLE_COLUMNS = [
    ("Configuration", "config"),
    ("Capacity", "capacity"),
    ("Outstation", "per_km"),
    ("Per day", "per_day"),
    ("Driver allowance", "driver_allowance"),
    ("Minimum", "min_km_per_day"),
]

RATE_INCLUSIONS = [
    "Vehicle and driver for the journeys described in your quotation",
]
RATE_EXCLUSIONS = [
    "Toll and parking charges",
    "State tax and permits where applicable",
    "GST",
    "Driver night allowance where a trip runs overnight",
    "Extra hours and extra kilometres beyond those quoted",
]

RATE_NOTES = [
    ("Minimum billing", None),
    ("Billing basis", "Garage to garage"),
    ("GST", "5%"),
    ("Night allowance", None),
    ("Extra hour rate", None),
    ("Extra kilometre rate", None),
]


# ------------------------------------------------------------------- routes
# Destinations reachable from Hyderabad.
#
# DISTANCES AND DRIVE TIMES: approximate road distances from central Hyderabad via
# the usual highway route, researched 2026-10-03 and cross-checked across several
# independent distance sources (Yatra, Savaari, Uber Intercity, Holidify, Hampi.in,
# CoveringIndia). Where sources disagreed, the commoner band was taken and a round
# figure used. They are inherently approximate — routed distance varies with the
# route taken and the time of day — and every page states that. Recorded with
# sources in docs/FACTS_LEDGER.md. Do not tighten these into false precision.
ROUTES = [
    dict(name="Srisailam", region="Telangana", distance_km=214, drive_time="4h 45m",
         note="Temple town and dam, usually an overnight trip. The last stretch runs "
              "through a tiger reserve, so there are gate timings to plan around."),
    dict(name="Tirupati", region="Andhra Pradesh", distance_km=565, drive_time="10h",
         note="Popular pilgrimage run, often combined with an early start or an "
              "overnight stop."),
    dict(name="Vijayawada", region="Andhra Pradesh", distance_km=273, drive_time="4h 50m",
         note="City trip or onward stop, comfortable in a day."),
    dict(name="Warangal", region="Telangana", distance_km=147, drive_time="3h",
         note="Heritage sites and lake, comfortable as a day or overnight trip."),
    dict(name="Bangalore", region="Karnataka", distance_km=573, drive_time="10h",
         note="Long-distance outstation, usually overnight."),
    dict(name="Hampi", region="Karnataka", distance_km=377, drive_time="8h",
         note="Heritage weekend trip."),
    dict(name="Goa", region="Goa", distance_km=644, drive_time="11h",
         note="Multi-day coastal trip. Figure is to Panaji; North and South Goa "
              "endpoints differ by well over an hour."),
    dict(name="Ooty", region="Tamil Nadu", distance_km=845, drive_time="14h",
         note="Long multi-day run into the Nilgiris, normally with a night stop "
              "on the way."),
]

# Provenance for the figures above. The suite requires an entry for every route
# that publishes a distance, so a new destination cannot be added with an
# unsourced number — which is the guarantee the old "must be None" assertion was
# really providing, kept now that real figures exist.
ROUTE_DISTANCE_SOURCES = {
    "Srisailam": "yatra.com/distance-between/hyderabad-to-srisailam; rajadroptaxi.com — 213-215 km, 4h30-5h",
    "Tirupati": "savaari.com; uber.com/intercity — 560-574 km (~10h); a 625 km bus-site figure excluded as an outlier",
    "Vijayawada": "yatra.com; savaari.com — 272-275 km (~4h50); a 305 km figure excluded",
    "Warangal": "savaari.com; uber.com/intercity — 146-149 km (~3h)",
    "Bangalore": "uber.com/intercity 571 km; savaari.com 575 km — ~570-575 km (~10h); a 610 km figure excluded",
    "Hampi": "hampi.in; tusktravel.com — 375-380 km, 7h30-8h30",
    "Goa": "uber.com/intercity 629 km to coveringindia.com 659 km to Panaji; savaari.com 644 km — figure given is to Panaji, hence the wide band",
    "Ooty": "yatra.com 839 km; holidify.com 847 km; savaari.com 850 km — 839-850 km, ~14h; an 885 km figure excluded",
}

# Nearby areas named by the local competitor as service areas, useful for
# local-search relevance.
SERVICE_AREAS = ["Gachibowli", "HITEC City", "Kukatpally", "Banjara Hills",
                 "Jubilee Hills", "Secunderabad", "Shamshabad", "Kondapur"]


# ----------------------------------------------------------------- services
SERVICES = [
    dict(key="airport", name="Airport group transfers", href="/airport-group-transfer-hyderabad/",
         blurb="Arrivals, departures or both, with the group and their luggage planned together."),
    dict(key="outstation", name="Outstation group travel", href="/outstation-group-travel-hyderabad/",
         blurb="Multi-day trips across India using your own itinerary and stop order."),
    dict(key="corporate", name="Corporate travel", href="/corporate-group-transport-hyderabad/",
         blurb="Visiting teams and off-site groups moving between airport, hotel and venue."),
    dict(key="wedding", name="Wedding transportation", href="/wedding-transport-hyderabad/",
         blurb="Guest movement between hotels, venues and the airport across one day or several."),
    dict(key="family", name="Family group travel", href="/family-group-travel-hyderabad/",
         blurb="Comfortable group travel for families, including luggage and elders."),
    dict(key="sightseeing", name="Sightseeing &amp; day hire", href="/hyderabad-sightseeing-group-travel/",
         blurb="Full-day or multi-stop city travel on your own plan."),
    dict(key="pilgrimage", name="Pilgrimage tours", href="/services/pilgrimage-tours/",
         blurb="Temple and pilgrimage travel planned around your route, dates and group."),
    dict(key="events", name="Events &amp; group tours", href="/services/events/",
         blurb="Conference, event and tour group movement with a fixed schedule."),
]

# Shared components use these national intent pages. Hyderabad-specific pages
# remain in SERVICES for the verified local cohort, but must not be the default
# destination from the India-wide homepage or other shared components.
NATIONAL_SERVICES = [
    dict(key="airport", name="Airport group transfers", href="/services/airport-group-transfers/",
         blurb="Airport pickup and drop planning for groups, passengers and luggage."),
    dict(key="wedding", name="Wedding guest transport", href="/services/wedding-guest-transport/",
         blurb="Guest movement between hotels, venues and airports across a planned schedule."),
    dict(key="corporate", name="Corporate group transport", href="/services/corporate-group-transport/",
         blurb="Transport for teams, delegations, conferences and scheduled group movement."),
    dict(key="outstation", name="Outstation group travel", href="/services/outstation-group-travel/",
         blurb="Intercity and multi-day group travel built around your route and stop order."),
    dict(key="pilgrimage", name="Pilgrimage group travel", href="/services/pilgrimage-group-travel/",
         blurb="Pilgrimage travel planned around early starts, stops and the full itinerary."),
    dict(key="events", name="Events and group tours", href="/services/events-group-transport/",
         blurb="Fixed-schedule transport for events, conferences and organised groups."),
]


# -------------------------------------------------------------------- trust
# Every value is None until the owner supplies it. Nothing is fabricated, and
# the template will not print a number that was never given.
TRUST_FIELDS = [
    ("Google rating", None),
    ("Google reviews", None),
    ("Trips completed", None),
    ("Years operating", None),
    ("Vehicles in service", None),
    ("Professional drivers", None),
    ("Support hours", None),
]

TRUST_ASSURANCES = [
    "One clear contact point for your enquiry",
    "Vehicle options matched to your route and group",
    "Availability confirmed before anything is agreed",
    "Nothing is charged to request a quotation",
]


# ------------------------------------------------------------------ reviews
# Deliberately empty. Real Google reviews are pasted in by the owner; nothing
# is written on a customer's behalf.
REVIEWS = []

REVIEWS_EMPTY_MESSAGE = ("Customer reviews will be published here as they are received. "
                         "We do not write testimonials on customers' behalf, so this space "
                         "stays empty until there are genuine ones to show.")


# ---------------------------------------------------------------- photo slots
# Fixed filenames so real photographs drop in without touching code.
GALLERY_SLOTS = [
    ("exterior-front", "Force Urbania exterior, front view"),
    ("exterior-side", "Force Urbania exterior, side view"),
    ("exterior-rear", "Force Urbania exterior, rear three-quarter view"),
    ("fleet-lineup", "Force Urbania vehicles, fleet-lineup reference"),
]


# Seating references. Seat layout and legroom are the two things buyers ask about
# most, and the briefing calls them out explicitly. Real photographs drop into
# app/site/media/seating/<name>.jpg and this section switches from placeholder to
# photo automatically on the next build.
SEATING_SLOTS = [
    ("standard-seating", "Standard passenger seating reference"),
    ("premium-recliner", "Premium reclining captain-seat reference"),
    ("luxury-tan-interior", "Luxury tan interior reference"),
]

# Supplied asset dimensions prevent image layout shift and keep the gallery
# stable before lazy-loaded photos arrive.
MEDIA_DIMENSIONS = {
    "exterior-front": (1200, 900),
    "exterior-side": (1200, 900),
    "exterior-rear": (1200, 900),
    "fleet-lineup": (1536, 1152),
    "standard-seating": (1200, 800),
    "premium-recliner": (1200, 675),
    "luxury-tan-interior": (678, 452),
}

# Descriptions of the two seat layouts. Layout convention is what distinguishes
# the trims in the Indian market; nothing here claims a specific vehicle spec.
SEAT_LAYOUTS = [
    dict(key="1x1", label="1x1 layout",
         name="Luxury / Maharaja seating",
         blurb="A single seat either side of the aisle. The layout used for the most "
               "comfortable small-group travel, with armrests and space between passengers."),
    dict(key="2x1", label="2x1 layout",
         name="Standard group seating",
         blurb="Two seats on one side of the aisle and one on the other. A practical layout "
               "for larger-group travel, subject to the exact vehicle offered."),
]


# ------------------------------------------------------------------- pricing
# Commercial question set. Answers carry no invented figures; where a rate is
# required the answer points at the rates page and the quote flow.
PRICING_FAQS = [
    ("How much does Force Urbania rental in Hyderabad cost?",
     "Rates depend on the trip, not just the vehicle: distance, duration, whether it is a "
     "local package or outstation, and the configuration you need. Our rates page sets out "
     "how each charge is built up. Send your trip details and you receive a quotation for "
     "your actual itinerary rather than a rough number."),
    ("How is the outstation rate worked out?",
     "Outstation trips are billed per kilometre with a per-day driver allowance and a "
     "minimum kilometre requirement per day. Toll, parking, state permits and GST are "
     "additional where they apply. The rates page lists each component."),
    ("What is the driver allowance?",
     "A daily charge covering the driver's time away from base on outstation and overnight "
     "trips. It is separate from the per-kilometre rate."),
    ("Is there a minimum number of kilometres per day?",
     "Yes, on outstation bookings. A minimum daily distance applies because the vehicle and "
     "driver are committed for the whole day. The current minimum is stated on the rates page."),
    ("Are toll and parking included?",
     "No. Toll and parking are charged as additional, at actuals, so you pay what the route "
     "costs rather than an inflated flat figure."),
    ("Do you charge GST?",
     "Yes, GST applies as required by law. The applicable rate is shown on the rates page."),
    ("How many passengers and how much luggage fit?",
     "Capacity depends on the configuration. Luggage is the part most group plans get wrong: "
     "a vehicle that seats everyone may not also take everyone's large suitcases. Tell us both "
     "numbers and we will confirm what fits before you commit."),
    ("Can you handle airport transfers?",
     "Yes. Group airport transfers to and from Rajiv Gandhi International Airport are one of "
     "the main trip types we handle. Give us the flight timing and passenger count."),
    ("Do you do interstate trips?",
     "Interstate travel depends on the permits and operating arrangements in force at the time. "
     "Tell us the route and dates and we will confirm whether we can quote for it."),
    ("Can the vehicle run overnight or over several days?",
     "Yes, multi-day and overnight trips are quoted individually, including the driver "
     "night allowance and any minimum daily distance."),
    ("How far in advance should I book?",
     "For weekends, festival periods and wedding season, earlier is better because there is a "
     "single vehicle. We do not publish a guaranteed lead time — send the date and we will tell "
     "you honestly whether it can be covered."),
    ("Is availability guaranteed when I submit the form?",
     "No. Submitting an enquiry is a quotation request. It does not hold the vehicle, does not "
     "confirm availability and does not create a booking. A booking exists only once a quotation "
     "is accepted."),
]


# ---------------------------------------------------- WhatsApp prefill shape
WHATSAPP_FIELDS = ["From", "To", "Travel date", "Passengers", "Trip type"]
