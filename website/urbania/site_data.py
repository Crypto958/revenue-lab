#!/usr/bin/env python3
"""
Urbania Hyderabad — single editable content source.

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
site describe ONE 17-seat vehicle. Flip this only once the owner confirms which
vehicles actually exist.
"""

# --------------------------------------------------------------------- flags
# Owner must confirm which Urbania configurations actually exist. Until then the
# configuration and rate sections publish their ARCHITECTURE (layout, guidance,
# indexable headings) but show to-be-confirmed values instead of asserting a
# fleet. See docs/IMPROVEMENT_PLAN.md.
FLEET_CONFIRMED = False

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
    """Rupee placeholder. Renders '₹XX' when unset, never a guessed figure."""
    if value is None:
        return "&#8377;XX"
    return f"&#8377;{value}"


# --------------------------------------------------------------------- fleet
# Passenger capacity per the owner's brief. seat_layout and trim mirror the
# convention the Indian market uses (1x1 vs 2x1, Deluxe/Premium/Luxury).
# Specs are intentionally None: the owner has not supplied them.
CONFIGURATIONS = [
    dict(
        key="luxury-maharaja",
        name="Luxury / Maharaja",
        seats_label="9&ndash;10 seater",
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
        seats_label="12&ndash;13 seater",
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
        seats_label="16 seater",
        seats_min=16, seats_max=16,
        seat_layout="2x1",
        trim="Deluxe",
        tagline="A full group in one vehicle.",
        best_for=["Outstation group travel", "Pilgrimage tours",
                  "Corporate off-sites", "Event and conference groups"],
        specs=dict(seat_type=None, ac=None, charging=None, luggage=None, amenities=None),
        per_km=None, per_day=None, driver_allowance=None, min_km_per_day=None,
        photo_dir="/img/fleet/seater-16/",
    ),
    dict(
        key="seater-17",
        name="Standard",
        seats_label="17 seater",
        seats_min=17, seats_max=17,
        seat_layout="2x1",
        trim="Deluxe",
        tagline="Our maximum capacity, in a single vehicle.",
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

    Honest about the ceiling: more than 17 cannot travel in one Urbania.
    """
    if passengers is None:
        return None, "Tell us your group size", ""
    if passengers > 17:
        return (None, "One Urbania cannot carry this group",
                "A 17-seat Urbania is the largest we can offer, so a group this size needs a "
                "different arrangement. Tell us the numbers and we will say honestly whether it "
                "can be covered at all.")
    if passengers > 16:
        return "seater-17", "17 seater Urbania", "The largest group we can carry in one vehicle."
    if passengers > 13:
        return "seater-16", "16 seater Urbania", "Comfortable for this group size with normal luggage."
    if passengers > 10:
        return "premium-12", "12&ndash;13 seater Premium Urbania", "Premium seating with room to spread out."
    if passengers >= 9:
        return "luxury-maharaja", "9&ndash;10 seater Luxury / Maharaja Urbania", "The most comfortable option for a group this size."
    return "luxury-maharaja", "9&ndash;10 seater Luxury / Maharaja Urbania", "More vehicle than this group needs — a comfortable choice."


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
    ("GST", None),
    ("Night allowance", None),
    ("Extra hour rate", None),
    ("Extra kilometre rate", None),
]


# ------------------------------------------------------------------- routes
# Destinations reachable from Hyderabad. Distances, journey times and prices
# are deliberately None: the brief says not to invent them, and both are easy
# to get wrong without a checked source.
ROUTES = [
    dict(name="Srisailam", region="Telangana", distance_km=None, drive_time=None,
         note="Temple town and dam, usually an overnight trip."),
    dict(name="Tirupati", region="Andhra Pradesh", distance_km=None, drive_time=None,
         note="Popular pilgrimage run, often combined with an early start."),
    dict(name="Vijayawada", region="Andhra Pradesh", distance_km=None, drive_time=None,
         note="City trip or onward stop."),
    dict(name="Warangal", region="Telangana", distance_km=None, drive_time=None,
         note="Heritage sites and lake, comfortable as a day or overnight trip."),
    dict(name="Bangalore", region="Karnataka", distance_km=None, drive_time=None,
         note="Long-distance outstation, usually overnight."),
    dict(name="Hampi", region="Karnataka", distance_km=None, drive_time=None,
         note="Heritage weekend trip."),
    dict(name="Goa", region="Goa", distance_km=None, drive_time=None,
         note="Multi-day coastal trip."),
]

# Nearby areas named by the local competitor as service areas, useful for
# local-search relevance.
SERVICE_AREAS = ["Gachibowli", "HITEC City", "Kukatpally", "Banjara Hills",
                 "Jubilee Hills", "Secunderabad", "Shamshabad", "Kondapur"]


# ----------------------------------------------------------------- services
SERVICES = [
    dict(key="airport", name="Airport group transfers", href="/airport-group-transfer-hyderabad/",
         blurb="Arrivals, departures or both, with the group and their luggage in one vehicle."),
    dict(key="outstation", name="Outstation group travel", href="/outstation-group-travel-hyderabad/",
         blurb="Multi-day trips out of Hyderabad using your own itinerary and stop order."),
    dict(key="corporate", name="Corporate travel", href="/corporate-group-transport-hyderabad/",
         blurb="Visiting teams and off-site groups moving between airport, hotel and venue."),
    dict(key="wedding", name="Wedding transportation", href="/wedding-transport-hyderabad/",
         blurb="Guest movement between hotels, venues and the airport across one day or several."),
    dict(key="family", name="Family group travel", href="/family-group-travel-hyderabad/",
         blurb="One vehicle for the whole family, including luggage and elders."),
    dict(key="sightseeing", name="Sightseeing &amp; day hire", href="/hyderabad-sightseeing-group-travel/",
         blurb="Full-day or multi-stop city travel on your own plan."),
    dict(key="pilgrimage", name="Pilgrimage tours", href="/services/pilgrimage-tours/",
         blurb="Temple and pilgrimage runs within Telangana, Andhra Pradesh and beyond."),
    dict(key="events", name="Events &amp; group tours", href="/services/events/",
         blurb="Conference, event and tour group movement with a fixed schedule."),
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
    "You deal with the operator, not a call centre",
    "One vehicle, so the group stays together",
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
    ("exterior-front", "Front three-quarter, exterior"),
    ("exterior-side", "Side profile"),
    ("exterior-rear", "Rear three-quarter"),
    ("entry", "Open door and step-in"),
    ("interior-rows", "Seat rows from the front"),
    ("interior-aisle", "Aisle and legroom"),
    ("interior-seats", "Seat detail and trim"),
    ("ac", "Air-conditioning vents"),
    ("charging", "Charging points"),
    ("luggage", "Luggage bay with cases"),
    ("night-interior", "Interior at night"),
    ("driver-area", "Driver area and dashboard"),
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
