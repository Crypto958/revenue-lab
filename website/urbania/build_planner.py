#!/usr/bin/env python3
"""
Adaptive group-trip planner for the group-travel site.

Design rules honoured here:
 - Every trip mode's fields are SERVER-RENDERED in the HTML (not built in JS), so the
   planner never hides content from crawlers. JS only shows/hides.
 - Progressive disclosure: Trip type -> Route -> Dates -> Group/Luggage -> Vehicle -> Contact -> Summary.
 - No "Book now". No implied availability. CTA language varies by mode as specified.
 - Vehicle categories are described as PREFERENCE / REQUEST categories, never as live inventory.
 - Submission produces a TRIP REQUEST with a reference ID, delivered to WhatsApp.
"""

# ---------------------------------------------------------------- field builders
def f_text(name, label, ph="", req=False, typ="text", hint="", half=False):
    h = f'<span class="hint">{hint}</span>' if hint else ""
    r = " required" if req else ""
    # placeholder is invalid on date/time inputs — browsers ignore it and validators flag it
    ph_attr = f' placeholder="{ph}"' if ph and typ not in ("date", "time") else ""
    return (f'<label class="pl-f{" half" if half else ""}"><span>{label}{" *" if req else ""}</span>'
            f'<input type="{typ}" name="{name}"{ph_attr}{r}>{h}</label>')

def f_select(name, label, opts, req=False, half=False):
    o = "".join(f'<option value="{x}">{x}</option>' for x in opts)
    return (f'<label class="pl-f{" half" if half else ""}"><span>{label}{" *" if req else ""}</span>'
            f'<select name="{name}"{" required" if req else ""}>{o}</select></label>')

def f_area(name, label, ph="", half=False):
    return (f'<label class="pl-f{" half" if half else ""}"><span>{label}</span>'
            f'<textarea name="{name}" placeholder="{ph}"></textarea></label>')

def f_chips(name, label, opts, req=False, multi=False):
    t = "checkbox" if multi else "radio"
    c = "".join(f'<label class="pl-chip"><input type="{t}" name="{name}" value="{o}"'
                f'{" required" if req and not multi else ""}>{o}</label>' for o in opts)
    return f'<div class="pl-f pl-full"><span class="pl-lab">{label}{" *" if req else ""}</span><div class="pl-chips">{c}</div></div>'

def f_row(*fields):
    return f'<div class="pl-row">{"".join(fields)}</div>'

# ---------------------------------------------------------------- trip modes
# CTA wording per mode is specified by the product brief.
MODES = [
    dict(key="local", label="City / Local", cta="Find local options",
         blurb="Point-to-point travel anywhere in India, with optional stops.",
         date_ui="single",
         fields=[
             f_row(f_text("pickup", "Pickup point", "Area, hotel or address", req=True, half=True),
                   f_text("destination", "Destination", "Where the group is going", req=True, half=True)),
             f_text("stops", "Stops you want to make", "Optional — list them in order"),
             f_row(f_text("date", "Travel date", req=True, typ="date", half=True),
                   f_text("start_time", "Start time", typ="time", half=True)),
             f_row(f_select("duty", "How long do you need the vehicle?", ["A few hours", "Full day", "Multiple days", "Not sure"], req=True, half=True),
                   f_text("end_time", "Approximate finish time", typ="time", half=True)),
             f_row(f_text("passengers", "Passengers", "Number of people", req=True, typ="number", half=True),
                   f_select("luggage", "Luggage", ["Cabin bags only", "A few large suitcases", "One large suitcase each", "Heavy — lots of bags", "Not sure"], half=True)),
         ]),
    dict(key="airport", label="Airport", cta="Request airport options",
         blurb="Group arrivals and departures at Rajiv Gandhi International Airport.",
         date_ui="single",
         fields=[
             f_chips("airport_direction", "What do you need?", ["Airport pickup", "Airport drop", "Round trip"], req=True),
             f_row(f_text("airport", "Airport", "Rajiv Gandhi International (or another)", half=True),
                   f_text("address", "Hotel, home or office address", "", half=True)),
             f_text("flight_no", "Flight number", "Optional — helps us plan the pickup"),
             f_row(f_text("date", "Travel date", req=True, typ="date", half=True),
                   f_text("flight_time", "Landing or departure time", typ="time", half=True)),
             f_row(f_text("passengers", "Passengers", "Including children", req=True, typ="number", half=True),
                   f_select("cabin_bags", "Cabin bags", ["None", "1 per person", "More than 1 per person", "Not sure"], half=True)),
             f_row(f_select("large_bags", "Large suitcases", ["None", "1–5", "6–10", "11–17", "More than 17", "Not sure"], req=True, half=True),
                   f_select("return_leg", "Return transfer needed?", ["Yes, same day", "Yes, on a later date", "One way only", "Not sure"], half=True)),
         ]),
    dict(key="outstation", label="Outstation", cta="Check outstation options",
         blurb="Intercity and multi-day travel. Outstation trips depend on the permissions and arrangements that apply at the time — we confirm before quoting.",
         date_ui="range",
         fields=[
             f_chips("trip_shape", "Trip type", ["One way", "Round trip", "Multi-city"], req=True),
             f_row(f_text("pickup", "Pickup point", "Starting address", req=True, half=True),
                   f_text("destinations", "Destination(s)", "Main destination", req=True, half=True)),
             f_text("add_stop", "Any stops on the way", "Optional"),
             f_row(f_text("return_date", "Return date", typ="date", half=True),
                   f_select("overnight", "Overnight stays", ["None", "1 night", "2–3 nights", "4+ nights", "Not sure"], half=True)),
             f_row(f_text("passengers", "Passengers", "", req=True, typ="number", half=True),
                   f_select("luggage", "Luggage", ["Cabin bags only", "A few large suitcases", "One large suitcase each", "Heavy — lots of bags", "Not sure"], half=True)),
             f_text("est_km", "Approximate distance", "Optional — or select \u201cNot sure\u201d in the summary"),
         ]),
    dict(key="wedding", label="Wedding / Event", cta="Plan my event transport",
         blurb="Guest movement across a wedding or event schedule.",
         date_ui="range",
         fields=[
             f_row(f_text("guests", "Guests needing transport", "Total, across the movements", req=True, typ="number", half=True),
                   f_select("movement_pattern", "How do the movements run?", ["Single transfer", "Several transfers on one day", "Multi-day transport", "Not sure yet"], req=True, half=True)),
             f_chips("event_needs", "What do you need covered?", ["Airport pickups", "Hotel to venue", "Home to venue", "Guest transfers", "Late-night return", "Multi-day schedule"], multi=True),
             f_row(f_text("main_pickup", "Main pickup point", "Hotel, home or airport", half=True),
                   f_text("venue", "Venue", "Where the event is", half=True)),
             f_text("extra_pickups", "Additional pickup points", "List them — we will work out a sensible order"),
             f_row(f_select("vehicles_known", "How many vehicles?", ["One", "Two or more", "Not sure — please advise"], half=True),
                   f_text("date_from", "First date", typ="date", half=True)),
             f_text("schedule_notes", "Anything else about the schedule", "Optional"),
         ]),
    dict(key="corporate", label="Corporate", cta="Request corporate transport",
         blurb="Teams, delegations and scheduled movement across a visit.",
         date_ui="range",
         fields=[
             f_row(f_text("company", "Company", "Optional", half=True),
                   f_text("team_size", "Team size", "", req=True, typ="number", half=True)),
             f_row(f_text("duty_window", "Duty window", "e.g. 09:00–18:00", half=True),
                   f_text("date_from", "Date", typ="date", half=True)),
             f_text("return_date", "Return or final date", "Optional, for multi-day visits"),
             f_row(f_text("pickup", "Pickup point", "Airport, hotel or office", half=True),
                   f_text("destination", "Destination", "Office, venue or site", half=True)),
             f_text("stops", "Multiple stops", "List them in order"),
             f_chips("corporate_needs", "What is the visit for?", ["Airport transfers", "Conference", "Off-site or team day", "Client visits", "Multi-day programme"], multi=True),
             f_select("invoice_requirement", "Do you need a tax invoice?", ["Not sure", "Yes — our finance team needs one", "No"]),
         ]),
    dict(key="sightseeing", label="Sightseeing / Day Trip", cta="Request day trip quote",
         blurb="Multi-stop city travel on your own itinerary. Transport only — no guides or tickets.",
         date_ui="range",
         fields=[
             f_row(f_text("pickup", "Pickup point", "Where the group starts", req=True, half=True),
                   f_text("start_time", "Start time", typ="time", half=True)),
             f_text("itinerary", "Places you want to visit", "List the stops in the order you would like"),
             f_row(f_select("duration", "How long?", ["A few hours", "Full day", "Multiple days", "Not sure"], req=True, half=True),
                   f_text("passengers", "Passengers", "", req=True, typ="number", half=True)),
             f_chips("route_help", "Would you like help planning the route?", ["Yes — suggest a sensible order", "No — we have our own route"]),
         ]),
    dict(key="family", label="Family / Group Holiday", cta="Plan family trip",
         blurb="Family groups travelling together, including children and luggage.",
         date_ui="range",
         fields=[
             f_row(f_text("pickup", "Pickup point", "", req=True, half=True),
                   f_text("destination", "Destination", "", req=True, half=True)),
             f_text("stops", "Stops along the way", "Optional"),
             f_row(f_text("adults", "Adults", "", typ="number", half=True),
                   f_text("children", "Children", "Including infants", typ="number", half=True)),
             f_row(f_text("date_from", "Travel date", typ="date", half=True),
                   f_text("return_date", "Return date", "Optional", typ="date", half=True)),
             f_select("luggage", "Luggage", ["Cabin bags only", "A few large suitcases", "One large suitcase each", "Heavy — lots of bags", "Prams or bulky items", "Not sure"]),
         ]),
    dict(key="pilgrimage", label="Pilgrimage", cta="Plan pilgrimage transport",
         blurb="Temple and pilgrimage travel for groups, including early starts and multi-day routes.",
         date_ui="range",
         fields=[
             f_row(f_text("pickup", "Pickup point", "Starting address", req=True, half=True),
                   f_text("temple", "Temple or destination", "e.g. Tirupati, Srisailam, Shirdi", req=True, half=True)),
             f_text("add_stop", "Any other stops", "Optional — list them in the order you want"),
             f_row(f_text("date", "Travel date", req=True, typ="date", half=True),
                   f_text("return_date", "Return date", "Leave blank if undecided", typ="date", half=True)),
             f_row(f_text("passengers", "Passengers", "Including children and elders", req=True, typ="number", half=True),
                   f_select("luggage", "Luggage", ["Cabin bags only", "A few large suitcases", "One large suitcase each", "Heavy — lots of bags", "Not sure"], half=True)),
             f_select("early_start", "Does the day start early?", ["Yes — before 6am", "No", "Not sure"], half=True),
         ]),
    dict(key="hotel", label="Hotel / Resort", cta="Request hotel transfer",
         blurb="Transfers between hotels, resorts and venues for groups.",
         date_ui="single",
         fields=[
             f_row(f_text("pickup", "Pickup point", "Hotel, resort or address", req=True, half=True),
                   f_text("destination", "Destination", "Where the group is going", req=True, half=True)),
             f_row(f_text("date", "Travel date", req=True, typ="date", half=True),
                   f_text("pickup_time", "Pickup time", typ="time", half=True)),
             f_row(f_text("passengers", "Passengers", "", req=True, typ="number", half=True),
                   f_select("luggage", "Luggage", ["Cabin bags only", "A few large suitcases", "One large suitcase each", "Heavy — lots of bags", "Not sure"], half=True)),
             f_select("return_leg", "Return transfer needed?",
                      ["Yes, same day", "Yes, on a later date", "One way only", "Not sure"], half=True),
         ]),
    dict(key="custom", label="Custom", cta="Tell us your plan",
         blurb="Anything that does not fit the other modes. Describe it and we will work out what is needed.",
         date_ui="range",
         fields=[
             f_text("plan", "Describe your trip", "What you want to do, in your own words"),
             f_row(f_text("pickup", "Pickup point", "", req=True, half=True),
                   f_text("date_from", "Start date", typ="date", half=True)),
             f_row(f_text("return_date", "End date", "Flexible is fine", typ="date", half=True),
                   f_text("passengers", "Passengers", "", req=True, typ="number", half=True)),
             f_text("stages", "Staged stops", "List each stop if you have them"),
         ]),
]

VEHICLE_PREF = f_chips(
    "vehicle_pref",
    "Vehicle preference",
    ["Force Urbania", "Recommend the best option for my group"],
    req=False)

CONTACT = (
    f_row(f_text("contact_name", "Your name", "", req=True, half=True),
          f_text("contact_phone", "Phone number", "We reply by phone or WhatsApp", req=True, typ="tel", half=True))
    + f_text("contact_email", "Email", "Optional — include it if you would prefer a written quotation", typ="email")
    + f_text("whatsapp", "WhatsApp number", "Only if it differs from the phone number above", typ="tel")
    + f'<label class="pl-consent"><input type="checkbox" name="consent" required>'
      f'<span>I agree that my trip details may be used to prepare a quotation and reply to me, as described in the '
      f'<a href="/privacy/">privacy notice</a>.</span></label>'
    # Bot trap, restored when the planner replaced the standalone form. Hidden
    # from humans and assistive tech; anything typed here means a bot, and
    # app/server.py:create_trip() then silently stores nothing.
    + '<input type="text" name="_hp" tabindex="-1" autocomplete="off" aria-hidden="true" '
      'style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">'
)

def _mode_block(m, first):
    """Server-rendered field group for one trip mode."""
    return (f'<div class="pl-mode{" on" if first else ""}" data-mode="{m["key"]}" '
            f'data-cta="{m["cta"]}" data-dateui="{m["date_ui"]}">'
            f'<p class="pl-blurb">{m["blurb"]}</p>'
            + "".join(m["fields"]) + VEHICLE_PREF + '</div>')

def planner(preset=""):
    chips = "".join(
        f'<button type="button" class="pl-tab{" on" if (m["key"] == preset or (not preset and i == 0)) else ""}" '
        f'data-mode="{m["key"]}" role="tab" aria-selected="{"true" if (m["key"] == preset or (not preset and i == 0)) else "false"}">'
        f'{m["label"]}</button>' for i, m in enumerate(MODES))
    blocks = "".join(_mode_block(m, i == 0 and not preset) for i, m in enumerate(MODES))
    summary_rows = (
        '<div class="pl-sgrid" id="pl-sgrid"></div>'
        '<p class="pl-snote">Check the details above. You can go back and edit anything.</p>')
    return f'''<div class="planner" id="planner" data-preset="{preset}">
  <div class="pl-tabs" role="tablist" aria-label="Trip type">{chips}</div>
  <form id="plform" novalidate>
    <div class="pl-modes">{blocks}</div>
    <div class="pl-contact" id="pl-contact" style="display:none">
      <h3 class="pl-h">Where should we send your quotation?</h3>
      <p class="pl-help">Your trip details are captured first. Now add your contact details so we can send the quotation after checking the route and availability.</p>
      {CONTACT}
    </div>
    <div class="pl-summary" id="pl-summary">
      <h3 class="pl-h">Your trip summary</h3>
      {summary_rows}
      <p id="pl-status" class="pl-help" role="status">We will check suitable vehicle options for this route and date.</p>
      <div class="pl-summary-actions">
        <button type="button" class="btn ghost" id="pl-edit">Edit details</button>
        <button type="submit" class="btn" id="pl-send">Send my enquiry</button>
      </div>
    </div>
    <div class="pl-foot">
      <button type="submit" class="btn wide" id="pl-next">Review my trip</button>
      <p class="pl-disclaim"><b>This is a quotation request.</b> Sending it does not confirm vehicle availability
      and does not create a booking. UrbanLoop checks suitability and availability, then sends you a quotation.</p>
    </div>
  </form>
  <!-- OUTSIDE the form on purpose. done() hides the form on success; while this
       lived inside it, the confirmation was hidden with it and the customer saw
       the form vanish with no acknowledgement at all. -->
  <div id="pl-result" tabindex="-1" aria-live="polite"></div>
  <noscript><div style="padding:18px 20px;border-top:1px solid var(--line);background:#FFF7E6;font-size:14.5px">
    <b>This planner needs JavaScript.</b> You can still get a quotation — call
    <a href="%PHONE_HREF%" style="color:var(--accent);font-weight:600">%PHONE%</a> or email your trip details:
    trip type, route, dates, number of passengers and the luggage you are carrying. We will reply with a quotation.
  </div></noscript>
</div>'''

# ---------------------------------------------------------------- CSS
PLANNER_CSS = """
.planner{background:#fff;border:1px solid var(--line-2);border-radius:18px;box-shadow:0 18px 50px rgba(14,27,42,.10);overflow:hidden}
.pl-tabs{display:flex;gap:7px;overflow-x:auto;padding:14px 16px 12px;border-bottom:1px solid var(--line);
background:var(--alt);scrollbar-width:none}
.pl-tabs::-webkit-scrollbar{display:none}
.pl-tab{flex:none;background:#fff;border:1px solid var(--line-2);color:var(--ink-2);padding:12px 16px;border-radius:100px;
font-size:14px;font-family:inherit;font-weight:500;cursor:pointer;white-space:nowrap;transition:.15s;min-height:44px;
display:inline-flex;align-items:center}
.pl-tab:hover{border-color:var(--ink-3);color:var(--ink)}
.pl-tab.on{background:var(--accent);border-color:var(--accent);color:#fff}
.pl-modes{padding:20px 20px 4px}
@media(max-width:560px){.pl-modes{padding:16px 14px 2px}.pl-contact,.pl-summary{padding:16px 14px}}
.pl-mode{display:none}.pl-mode.on{display:block;animation:plfade .22s ease}
@keyframes plfade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.pl-blurb{font-size:14px;color:var(--ink-3);margin-bottom:16px;line-height:1.5}
.pl-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:560px){.pl-row{grid-template-columns:1fr;gap:0}}
.pl-f{display:block;margin-bottom:15px}
.pl-f>span,.pl-lab{display:block;font-size:13.5px;font-weight:600;color:var(--ink);margin-bottom:7px}
.pl-f .hint{display:block;font-weight:400;font-size:12.5px;color:var(--ink-3);margin-top:5px}
.pl-f input,.pl-f select,.pl-f textarea{width:100%;background:#fff;border:1px solid var(--line-2);border-radius:9px;
padding:12px 13px;font-size:16px;font-family:inherit;color:var(--ink)}
.pl-f textarea{min-height:74px;resize:vertical}
.pl-f input:focus,.pl-f select:focus,.pl-f textarea:focus{outline:0;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.pl-f.bad input,.pl-f.bad select,.pl-f.bad textarea{border-color:#B42318}
.pl-chips{display:flex;flex-wrap:wrap;gap:8px}
.pl-chip{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line-2);border-radius:100px;
padding:9px 14px;font-size:14.5px;color:var(--ink-2);cursor:pointer;background:#fff;transition:.15s}
.pl-chip:hover{border-color:var(--ink-3)}
.pl-chip input{width:auto;margin:0;accent-color:var(--accent)}
.pl-chip:has(input:checked){border-color:var(--accent);background:var(--accent-soft);color:var(--accent-2);font-weight:600}
.pl-full{margin-bottom:15px}
.pl-contact,.pl-summary{padding:18px 20px;border-top:1px solid var(--line);background:var(--alt)}
.pl-h{font-size:17px;margin-bottom:14px}
.pl-help{font-size:13.5px;color:var(--ink-3);margin:-5px 0 16px;line-height:1.5}
.pl-consent{display:flex;gap:11px;align-items:flex-start;font-size:13px;color:var(--ink-2);line-height:1.5;margin-top:6px}
.pl-consent input{margin-top:3px;accent-color:var(--accent);flex:none;width:auto}
.pl-summary{display:none}.pl-summary.on{display:block}
.pl-sgrid{display:grid;gap:9px;margin-bottom:16px}
.pl-srow{display:grid;grid-template-columns:170px 1fr;gap:12px;font-size:14.5px;padding:8px 0;border-bottom:1px solid var(--line)}
@media(max-width:560px){.pl-srow{grid-template-columns:1fr;gap:2px}}
.pl-srow b{color:var(--ink-3);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.04em}
/* the result's numbered steps: the number column does not need 170px */
.pl-steps .pl-srow{grid-template-columns:34px 1fr}
.pl-steps .pl-srow b{font-family:var(--mono);font-size:14px;color:var(--accent);letter-spacing:0}
@media(max-width:560px){.pl-steps .pl-srow{grid-template-columns:28px 1fr;gap:6px}}
.pl-srow span{color:var(--ink)}
.pl-snote{font-size:13px;color:var(--ink-3)}
.pl-summary-actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.pl-foot{padding:18px 20px 22px;border-top:1px solid var(--line)}
.pl-disclaim{font-size:13px;color:var(--ink-3);margin-top:13px;line-height:1.55}
.pl-veh{display:grid;gap:12px;margin-top:18px}
.pl-vcard{border:1px solid var(--line-2);border-radius:14px;padding:18px;background:#fff}
.pl-vcard.feat{border-color:var(--accent);background:linear-gradient(180deg,var(--accent-soft),#fff 62%)}
.pl-vtag{display:inline-block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);
border:1px solid var(--accent);border-radius:100px;padding:3px 9px;margin-bottom:10px;font-weight:600}
.pl-ref{font-family:var(--mono);font-size:15px;background:#fff;border:1px dashed var(--line-2);border-radius:8px;
padding:10px 13px;display:inline-block;margin:10px 0}
"""

# ---------------------------------------------------------------- JS
PLANNER_JS = """<script>
(function(){
  var pl=document.getElementById('planner'); if(!pl) return;
  var form=document.getElementById('plform'),
      tabs=[].slice.call(pl.querySelectorAll('.pl-tab')),
      modes=[].slice.call(pl.querySelectorAll('.pl-mode')),
      summary=document.getElementById('pl-summary'),
      contact=document.getElementById('pl-contact'),
      status=document.getElementById('pl-status'),
      result=document.getElementById('pl-result'),
      nextBtn=document.getElementById('pl-next');
  var current=pl.getAttribute('data-preset')||'local', stage='form';
  var WA="%WA%", EP="%ENDPOINT%";

  function activate(k){
    current=k; stage='form';
    tabs.forEach(function(t){var on=t.getAttribute('data-mode')===k;
      t.classList.toggle('on',on); t.setAttribute('aria-selected',on?'true':'false');});
    modes.forEach(function(m){m.classList.toggle('on',m.getAttribute('data-mode')===k);});
    summary.classList.remove('on'); result.innerHTML='';
    var cta=pl.querySelector('.pl-mode[data-mode="'+k+'"]').getAttribute('data-cta');
    nextBtn.textContent=cta; nextBtn.className='btn wide';
    pl.querySelector('.pl-foot').style.display='';
    summary.style.display='none';
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){activate(t.getAttribute('data-mode'));});});

  function labelFor(el){
    var l=el.closest('label'); if(!l) return el.name;
    var s=l.querySelector('span'); return s?s.textContent.replace(/\\s*\\*/,'').trim():el.name;
  }
  function validate(includeContact){
    var scope=pl.querySelector('.pl-mode[data-mode="'+current+'"]'), bad=false;
    [].slice.call(scope.querySelectorAll('[required]')).forEach(function(el){
      var ok = el.type==='radio' ? !!scope.querySelector('input[name="'+el.name+'"]:checked') : !!el.value.trim();
      if(el.type!=='radio'){ var L=el.closest('label'); if(L){ L.classList.toggle('bad',!ok); el.setAttribute('aria-invalid',ok?'false':'true'); } }
      if(!ok) bad=true;
    });
    var c=document.getElementById('plform');
    if(includeContact) [].slice.call(c.querySelectorAll('.pl-contact [required]')).forEach(function(el){
      var ok = el.type==='checkbox' ? el.checked : !!el.value.trim();
      var L=el.closest('label'); if(L&&el.type!=='checkbox'){ L.classList.toggle('bad',!ok); el.setAttribute('aria-invalid',ok?'false':'true'); }
      if(!ok) bad=true;
    });
    if(bad){ var f=pl.querySelector('.pl-f.bad input, .pl-f.bad select, .pl-f.bad textarea'); if(f){f.focus();f.scrollIntoView({block:'center',behavior:'smooth'});} }
    return !bad;
  }
  function collect(){
    var o={trip_type:current}, scope=pl.querySelector('.pl-mode[data-mode="'+current+'"]');
    var labels={};
    [].slice.call(scope.querySelectorAll('.pl-f')).forEach(function(w){
      var s=w.querySelector('span,.pl-lab'), i=w.querySelector('input,select,textarea');
      if(s&&i&&i.name) labels[i.name]=s.textContent.replace(/\\s*\\*/,'').trim();
    });
    [].slice.call(scope.querySelectorAll('input,select,textarea')).forEach(function(el){
      var k=labels[el.name]||el.name.replace(/_/g,' ');
      if(el.type==='radio'||el.type==='checkbox'){
        if(el.checked) o[k]=(o[k]?o[k]+', ':'')+el.value;
      } else if(el.value.trim()) o[k]=el.value.trim();
    });
    [].slice.call(form.querySelectorAll('.pl-contact input,.pl-contact textarea')).forEach(function(el){
      if(el.type==='checkbox'){ if(el.checked) o[el.name]='Yes'; }
      else if(el.value.trim()) o[el.name]=el.value.trim();
    });
    o.source_page=location.pathname; o.submitted_at=new Date().toISOString();
    var q=new URLSearchParams(location.search);
    ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid'].forEach(function(x){ if(q.get(x)) o[x]=q.get(x); });
    return o;
  }
  function ref(){ var s='GT'+Date.now().toString(36).toUpperCase().slice(-6); return s; }
  function showSummary(){
    var o=collect(), g=document.getElementById('pl-sgrid'); g.innerHTML='';
    Object.keys(o).forEach(function(k){
      if(k==='submitted_at'||k==='consent') return;
      var row=document.createElement('div'); row.className='pl-srow';
      row.innerHTML='<b>'+k.replace(/_/g,' ')+'</b><span></span>';
      row.querySelector('span').textContent=o[k];
      g.appendChild(row);
    });
    pl.querySelector('.pl-foot').style.display='none';
    summary.style.display='block'; summary.classList.add('on');
    contact.style.display='block';
    status.textContent='Availability check started. We will confirm the suitable vehicle arrangement for your route and dates before sending the quotation.';
    if(EP){
      var check=Object.assign({},o,{stage:'availability_check'});
      fetch(EP,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(check)})
        .then(function(r){return r.json().catch(function(){return {};});})
        .then(function(j){if(j&&j.ref){try{localStorage.setItem('availabilityRef',j.ref);}catch(err){}}});
    }
    summary.scrollIntoView({block:'center',behavior:'smooth'});
  }
  nextBtn.addEventListener('click',function(e){ e.preventDefault(); if(validate(false)) showSummary(); });
  document.getElementById('pl-edit').addEventListener('click',function(){
    summary.classList.remove('on'); summary.style.display='none';
    pl.querySelector('.pl-foot').style.display='';
    pl.querySelector('.pl-modes').scrollIntoView({block:'start',behavior:'smooth'});
  });
  form.addEventListener('submit',function(e){
    e.preventDefault();
    if(!validate(true)) return;
    var hp=form.querySelector('input[name=_hp]'); if(hp&&hp.value) return;
    var o=collect(), clientRef=ref();
    o.stage='quote_request';
    try{ if(localStorage.getItem('availabilityRef')) o.availability_ref=localStorage.getItem('availabilityRef'); }catch(err){}
    function lines(id){ return 'Trip request '+id+'\\n'+
      Object.keys(o).map(function(k){return k.replace(/_/g,' ')+': '+o[k];}).join('\\n'); }
    function waFor(id){ return WA?('https://wa.me/'+WA+'?text='+encodeURIComponent(lines(id))):''; }
    function done(id, serverOk){
      try{ localStorage.setItem('lastTripRef',id); }catch(err){}
      var wa=waFor(id);
      form.style.display='none';
      result.innerHTML='<div style="padding:22px 20px"><h3 class="pl-h">'
        +'Quote request received</h3>'
        +'<div class="pl-ref">'+id+'</div>'
        +'<p class="lede" style="font-size:16px">Thank you &mdash; your reference is above. Here is what happens next:</p>'
        +'<div class="pl-sgrid pl-steps" style="margin-top:14px">'
        +'<div class="pl-srow"><b>1</b><span>We check the route, dates and group requirements, then identify a suitable vehicle arrangement.</span></div>'
        +'<div class="pl-srow"><b>2</b><span>We confirm vehicle availability for your dates.</span></div>'
        +'<div class="pl-srow"><b>3</b><span>We send you a quotation with the inclusions and terms.</span></div>'
        +'<div class="pl-srow"><b>4</b><span>A booking is confirmed only after you accept the quotation.</span></div>'
        +'</div>'
        +'<p class="pl-disclaim" style="margin-top:16px">This is a quotation request and does not confirm vehicle '
        +'availability or create a booking.'+(serverOk?'':' We could not reach our system, so please also send this '
        +'on WhatsApp to make sure it reaches us.')+'</p>'
        +'<p style="margin-top:14px;display:flex;gap:14px;flex-wrap:wrap">'
        +(wa?'<a class="btn" href="'+wa+'" target="_blank" rel="noopener">Send a copy on WhatsApp</a>':'')
        +'<a class="btn ghost" href="/">Back to start</a></p>'
        +'<p class="small" style="margin-top:12px">Keep your reference number. You can check progress at '
        +'<code>/api/trip/'+id+'</code>.</p></div>';
      result.focus(); result.scrollIntoView({block:'start',behavior:'smooth'});
    }
    if(EP){
      fetch(EP,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
        body:JSON.stringify(o)})
        .then(function(r){ return r.json().catch(function(){ return {}; }).then(function(j){ return {ok:r.ok&&j.ok,ref:j.ref}; }); })
        .then(function(j){
          var id=j.ok&&j.ref?j.ref:clientRef;
          if(j.ok){ done(id,true); } else { if(WA) window.open(waFor(clientRef),'_blank'); done(clientRef,false); }
        })
        .catch(function(){ if(WA) window.open(waFor(clientRef),'_blank'); done(clientRef,false); });
    }
    else if(WA){ window.open(waFor(clientRef),'_blank'); done(clientRef,true); }
    else { done(clientRef,true); }
  });
  // Prefill from the hero journey bar (?from=&to=&date=&pax=). Field names
  // differ per trip mode (pickup vs main_pickup, destination vs destinations),
  // so try the active mode's own names in order. Values only — never invents one.
  var PRE={from:['pickup','main_pickup','address','airport'],
           to:['destination','destinations','venue','itinerary','plan'],
           date:['date','date_from','return_date'],
           pax:['passengers','guests','team_size','adults']};
  function prefill(){
    var q; try{ q=new URLSearchParams(location.search); }catch(err){ return; }
    var scope=pl.querySelector('.pl-mode.on')||pl;
    Object.keys(PRE).forEach(function(k){
      var v=q.get(k); if(!v) return;
      var names=PRE[k];
      for(var i=0;i<names.length;i++){
        var el=scope.querySelector('[name="'+names[i]+'"]'); if(!el) continue;
        if(el.tagName==='SELECT'){
          var hit=[].slice.call(el.options).filter(function(o){
            return o.value===v||o.text===v;})[0];
          if(hit) el.value=hit.value;
        } else if(el.type!=='checkbox'&&el.type!=='radio'){ el.value=v; }
        break;
      }
    });
  }
  activate(current);
  prefill();
})();
</script>"""
