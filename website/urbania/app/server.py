#!/usr/bin/env python3
"""
Group travel site — application server.

Serves the static site AND provides the missing backend:
  POST /api/trip              accept a TRIP REQUEST, store it, return a server-issued reference
  GET  /api/trip/<REF>        public status lookup for a customer (no personal data returned)
  GET  /admin                 owner pipeline board (requires ADMIN_TOKEN)
  POST /admin/status          owner updates a trip's status (requires ADMIN_TOKEN)
  GET  /health                liveness

Storage: SQLite at data/trips.db. No external dependencies (Python standard library only).

Security notes:
  - ADMIN_TOKEN comes from the environment. If unset, the admin area is DISABLED entirely
    rather than falling back to a default password.
  - The customer-facing lookup never returns name, phone, email or address.
  - Simple per-IP rate limiting on the public endpoint.
"""
import os, sys, json, sqlite3, secrets, threading, time, re, mimetypes, html, gzip, io
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
DATA = os.path.join(ROOT, "data")
DB = os.path.join(DATA, "trips.db")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "").strip()
PORT = int(os.environ.get("PORT", "8100"))

# Trip request lifecycle, as specified.
STATUSES = ["NEW", "QUALIFYING", "OWN_VEHICLE_POSSIBLE", "PARTNER_SOURCING", "QUOTES_RECEIVED",
            "CUSTOMER_QUOTED", "FOLLOW_UP", "BOOKED", "LOST", "CANCELLED", "COMPLETED"]
OPEN_STATUSES = ["NEW", "QUALIFYING", "OWN_VEHICLE_POSSIBLE", "PARTNER_SOURCING",
                 "QUOTES_RECEIVED", "CUSTOMER_QUOTED", "FOLLOW_UP"]

_lock = threading.Lock()
_hits = {}          # ip -> [timestamps]
RATE_MAX, RATE_WINDOW = 12, 600      # 12 submissions per IP per 10 minutes


def db():
    os.makedirs(DATA, exist_ok=True)
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    c = db()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS trips (
      ref TEXT PRIMARY KEY,
      created_at TEXT NOT NULL,
      trip_type TEXT, status TEXT NOT NULL DEFAULT 'NEW',
      customer_name TEXT, phone TEXT, email TEXT,
      summary TEXT NOT NULL, payload TEXT NOT NULL,
      source_page TEXT, utm_source TEXT, utm_medium TEXT, utm_campaign TEXT,
      referrer TEXT, ip_hash TEXT, notes TEXT, updated_at TEXT
    );
    CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ref TEXT NOT NULL, at TEXT NOT NULL, kind TEXT NOT NULL, detail TEXT
    );
    """)
    c.commit(); c.close()


def new_ref(c):
    """Server-issued reference. Retries on the vanishingly unlikely collision."""
    for _ in range(8):
        r = "GT" + secrets.token_hex(3).upper()
        if not c.execute("SELECT 1 FROM trips WHERE ref=?", (r,)).fetchone():
            return r
    raise RuntimeError("could not allocate reference")


def log_event(c, ref, kind, detail=""):
    c.execute("INSERT INTO events(ref,at,kind,detail) VALUES(?,?,?,?)",
              (ref, datetime.now(timezone.utc).isoformat(), kind, detail))


def rate_ok(ip):
    now = time.time()
    with _lock:
        q = [t for t in _hits.get(ip, []) if now - t < RATE_WINDOW]
        if len(q) >= RATE_MAX:
            _hits[ip] = q
            return False
        q.append(now); _hits[ip] = q
    return True


def build_summary(d):
    """Human-readable one-liner for the pipeline board."""
    bits = [d.get("trip_type", "trip")]
    for k in ("Pickup point", "pickup", "Destination", "destination", "destinations"):
        if d.get(k):
            bits.append(str(d[k])); break
    for k in ("Travel date", "date", "Start date", "date_from"):
        if d.get(k):
            bits.append(str(d[k])); break
    for k in ("Passengers", "passengers", "Guests needing transport", "guests", "Team size", "team_size"):
        if d.get(k):
            bits.append(str(d[k]) + " pax"); break
    return " · ".join(bits)[:180]


# ------------------------------------------------------------------ handler
class H(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=SITE, **kw)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # ---------- static asset headers (caching + hardening)
    def send_response(self, *a, **kw):
        self._cc_sent = False
        super().send_response(*a, **kw)

    def send_header(self, keyword, value):
        if keyword.lower() == "cache-control":
            self._cc_sent = True
        super().send_header(keyword, value)

    def end_headers(self):
        if not getattr(self, "_cc_sent", False):
            p = self.path.split("?")[0].lower()
            if p.endswith((".css", ".svg", ".png", ".jpg", ".jpeg", ".webp",
                           ".avif", ".woff2", ".ico")):
                # revalidate so a rebuild always propagates; still avoids a full refetch
                self.send_header("Cache-Control", "public, max-age=3600, must-revalidate")
            elif p.endswith((".html", "/")) or "." not in p.rsplit("/", 1)[-1]:
                self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
            else:
                self.send_header("Cache-Control", "public, max-age=600")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    # ---------- helpers
    TEXT_ASSETS = (".html", ".css", ".svg", ".js", ".txt", ".xml", ".webmanifest")

    def send_head(self):
        """Serve compressible text assets gzipped, in one shot.

        Every page is ~90 KB of HTML uncompressed (the brand mark is inlined as
        vector artwork), so gzip takes it to roughly 12-15 KB. The brief is
        mobile-first and most enquiries are expected from a phone, so this is worth
        doing centrally. Binary types are untouched.

        Handled here rather than in copyfile() because SimpleHTTPRequestHandler has
        already sent Content-Length by the time copyfile() runs, and a compressed
        body under an uncompressed length would corrupt the response.
        """
        path = self.translate_path(self.path)
        # A directory serves its index.html, so "/" and "/about/" are files too —
        # without this the homepage is a directory path, os.path.isfile() is False,
        # and the site's biggest pages silently skip compression while CSS gets it.
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        if (os.path.isfile(path)
                and path.lower().endswith(self.TEXT_ASSETS)
                and "gzip" in (self.headers.get("Accept-Encoding") or "")):
            try:
                with open(path, "rb") as fh:
                    body = gzip.compress(fh.read(), 6)
            except OSError:
                return super().send_head()
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(path))
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Vary", "Accept-Encoding")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command == "HEAD":
                return None
            # the parent's do_GET streams whatever this returns straight to the socket
            return io.BytesIO(body)
        return super().send_head()

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, s, code=200):
        body = s.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > 200_000:
            return {}
        raw = self.rfile.read(n)
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type == "application/x-www-form-urlencoded":
            parsed = parse_qs(raw.decode("utf-8", "replace"), keep_blank_values=True)
            return {key: values[-1] if values else "" for key, values in parsed.items()}
        try:
            return json.loads(raw.decode("utf-8", "replace"))
        except Exception:
            return {}

    def _admin_ok(self, q):
        if not ADMIN_TOKEN:
            return False
        tok = (q.get("token", [""])[0] or self.headers.get("X-Admin-Token", "")).strip()
        return secrets.compare_digest(tok, ADMIN_TOKEN)

    # ---------- routes
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/health":
            return self._json({"ok": True, "time": datetime.now(timezone.utc).isoformat()})
        if u.path == "/admin":
            return self.admin_board(parse_qs(u.query))
        m = re.fullmatch(r"/api/trip/(GT[0-9A-F]{6})", u.path)
        if m:
            return self.public_status(m.group(1))
        if not ADMIN_TOKEN and u.path.startswith("/admin"):
            return self._html("<h1>Admin disabled</h1><p>Set ADMIN_TOKEN in the environment to enable the pipeline board.</p>", 503)
        return super().do_GET()

    def do_POST(self):
        u = urlparse(self.path)
        if u.path == "/api/trip":
            return self.create_trip()
        if u.path == "/admin/status":
            return self.update_status(parse_qs(u.query))
        return self._json({"ok": False, "error": "not found"}, 404)

    # ---------- branded error pages
    def send_error(self, code, message=None, explain=None):
        """Serve the site's own 404 page for unknown paths.

        The parent handler emits a bare stock error page, so /404.html was
        reachable but any unknown URL (say /definitely-missing) got the plain
        Python page instead of the branded one. The status stays 404 so search
        engines are not told a missing page exists.
        """
        if code == 404:
            try:
                with open(os.path.join(SITE, "404.html"), "rb") as fh:
                    body = fh.read()
            except OSError:
                return super().send_error(code, message, explain)
            self.send_response(404)
            compressed = "gzip" in (self.headers.get("Accept-Encoding") or "")
            if compressed:
                body = gzip.compress(body, 6)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            if compressed:
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Vary", "Accept-Encoding")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
            return
        return super().send_error(code, message, explain)

    # ---------- API
    def create_trip(self):
        ip = self.client_address[0]
        if not rate_ok(ip):
            return self._json({"ok": False, "error": "rate_limited"}, 429)
        d = self._body()
        if not isinstance(d, dict) or not d:
            return self._json({"ok": False, "error": "empty"}, 400)
        if str(d.get("_hp", "")).strip():                      # honeypot
            return self._json({"ok": True, "ref": "GT000000"})  # silently accept, store nothing
        phone = str(d.get("contact phone") or d.get("contact_phone") or "").strip()
        name = str(d.get("contact name") or d.get("contact_name") or "").strip()
        if not phone or not name or str(d.get("consent", "")).lower() not in ("yes", "true"):
            return self._json({"ok": False, "error": "missing_consent_or_contact"}, 400)
        with _lock:
            c = db()
            ref = new_ref(c)
            now = datetime.now(timezone.utc).isoformat()
            c.execute("""INSERT INTO trips(ref,created_at,trip_type,status,customer_name,phone,email,
                         summary,payload,source_page,utm_source,utm_medium,utm_campaign,referrer,
                         ip_hash,updated_at)
                         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                      (ref, now, str(d.get("trip_type", "")), "NEW", name, phone,
                       str(d.get("contact_email") or d.get("contact email") or d.get("email") or ""),
                       build_summary(d), json.dumps(d), str(d.get("source_page", "")),
                       str(d.get("utm_source", "")), str(d.get("utm_medium", "")), str(d.get("utm_campaign", "")),
                       str(d.get("referrer", "")), secrets.token_hex(8), now))
            log_event(c, ref, "CREATED", "status=NEW")
            c.commit()
            row = dict(c.execute("SELECT * FROM trips WHERE ref=?", (ref,)).fetchone())
            c.close()
        # Owner notification record. WhatsApp delivery to the owner is done by the client
        # (the customer's device opens WhatsApp); this file is the durable server-side record.
        try:
            os.makedirs(DATA, exist_ok=True)
            with open(os.path.join(DATA, "notifications.log"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"at": row["created_at"], "ref": ref, "summary": row["summary"],
                                     "name": row["customer_name"], "phone": row["phone"],
                                     "trip_type": row["trip_type"]}, ensure_ascii=False) + "\n")
        except Exception:
            pass
        return self._json({"ok": True, "ref": ref, "status": "NEW"})

    def public_status(self, ref):
        c = db()
        r = c.execute("SELECT ref,trip_type,status,created_at FROM trips WHERE ref=?", (ref,)).fetchone()
        c.close()
        if not r:
            return self._json({"ok": False, "error": "not_found"}, 404)
        return self._json({"ok": True, "ref": r["ref"], "trip_type": r["trip_type"],
                           "status": r["status"], "created_at": r["created_at"]})

    def update_status(self, q):
        if not self._admin_ok(q):
            return self._json({"ok": False, "error": "unauthorised"}, 401)
        d = self._body()
        ref, st = str(d.get("ref", "")), str(d.get("status", "")).upper()
        if st not in STATUSES:
            return self._json({"ok": False, "error": "bad_status"}, 400)
        with _lock:
            c = db()
            if not c.execute("SELECT 1 FROM trips WHERE ref=?", (ref,)).fetchone():
                c.close(); return self._json({"ok": False, "error": "not_found"}, 404)
            c.execute("UPDATE trips SET status=?, updated_at=? WHERE ref=?",
                      (st, datetime.now(timezone.utc).isoformat(), ref))
            log_event(c, ref, "STATUS", st); c.commit(); c.close()
        return self._json({"ok": True, "ref": ref, "status": st})

    # ---------- owner board
    def admin_board(self, q):
        if not self._admin_ok(q):
            return self._html("<h1>Not authorised</h1><p>Append <code>?token=…</code> with the admin token.</p>", 401)
        tok = q.get("token", [""])[0]
        c = db()
        rows = c.execute("""SELECT ref,created_at,trip_type,status,customer_name,phone,summary,source_page,notes
                            FROM trips ORDER BY created_at DESC LIMIT 200""").fetchall()
        counts = {s: c.execute("SELECT COUNT(*) FROM trips WHERE status=?", (s,)).fetchone()[0] for s in STATUSES}
        c.close()
        opens = sum(counts[s] for s in OPEN_STATUSES)
        kpis = (f"<div class=k><b>{len(rows)}</b><span>requests shown</span></div>"
                f"<div class=k><b>{opens}</b><span>open</span></div>"
                f"<div class=k><b>{counts['BOOKED']}</b><span>booked</span></div>"
                f"<div class=k><b>{counts['LOST']}</b><span>lost</span></div>")
        trs = ""
        for r in rows:
            new = " new" if r["status"] == "NEW" else ""
            opts = "".join(
                f'<option{" selected" if s == r["status"] else ""}>{s}</option>'
                for s in STATUSES
            )
            trs += (f'<tr class="{new}"><td><code>{r["ref"]}</code><br><span class=t>{r["created_at"][:16].replace("T"," ")}</span></td>'
                    f'<td>{html.escape(r["trip_type"] or "")}</td>'
                    f'<td>{html.escape(r["summary"] or "")}<br><span class=t>from {html.escape(r["source_page"] or "")}</span></td>'
                    f'<td>{html.escape(r["customer_name"] or "")}<br><span class=t>{html.escape(r["phone"] or "")}</span></td>'
                    f'<td><form method=post action="/admin/status?token={html.escape(tok)}">'
                    f'<input type=hidden name=ref value="{r["ref"]}">'
                    f'<select name=status>{opts}</select> '
                    f'<button>Save</button></form></td></tr>')
        page = f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Trip requests</title><style>
body{{font:15px/1.5 system-ui,sans-serif;margin:0;padding:22px;background:#F4F7F9;color:#0E1B2A}}
h1{{font-size:22px;margin:0 0 4px}} .sub{{color:#5C6B7A;margin-bottom:18px}}
.kpis{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}}
.k{{background:#fff;border:1px solid #E1E8ED;border-radius:10px;padding:12px 16px;min-width:110px}}
.k b{{display:block;font-size:24px}} .k span{{font-size:12px;color:#71818F;text-transform:uppercase;letter-spacing:.05em}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #E1E8ED;border-radius:10px;overflow:hidden}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid #EAF0F4;vertical-align:top;font-size:14px}}
th{{background:#EAF0F4;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:#48596B}}
tr.new td:first-child{{border-left:3px solid #116A7B}}
.t{{color:#8292A0;font-size:12px}} code{{font-family:ui-monospace,monospace;font-weight:600}}
select,button{{font:inherit;padding:7px 9px;border:1px solid #CDD8E0;border-radius:7px;background:#fff}}
button{{background:#116A7B;color:#fff;border-color:#116A7B;cursor:pointer}}
@media(max-width:760px){{.kpis{{gap:8px}} .k{{flex:1 1 44%}}}}</style>
<h1>Trip requests</h1><div class=sub>Westbridge-style pipeline · statuses follow the trip-request lifecycle</div>
<div class=kpis>{kpis}</div>
<table><tr><th>Reference</th><th>Type</th><th>Trip</th><th>Customer</th><th>Status</th></tr>{trs}</table>
<p class=sub style="margin-top:18px">Reference IDs are issued by the server. Customer lookup: <code>/api/trip/&lt;REF&gt;</code>.
This board never exposes the payload to the public.</p>"""
        return self._html(page)


def main():
    init_db()
    if not ADMIN_TOKEN:
        print("WARNING: ADMIN_TOKEN not set — /admin is disabled.", file=sys.stderr)
    print(f"serving {SITE} on 0.0.0.0:{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), H).serve_forever()


if __name__ == "__main__":
    main()
