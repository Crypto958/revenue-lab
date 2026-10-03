import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PROJECT = Path(__file__).resolve().parents[1]
APP = PROJECT / "app"
SITE = APP / "site"


def load_server():
    spec = importlib.util.spec_from_file_location("urbania_server", APP / "server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BuildContractTests(unittest.TestCase):
    def test_builder_sources_compile_on_default_python(self):
        for filename in ("build_ui.py", "build_planner.py", "build_pages.py", "build_v3.py"):
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(PROJECT / filename)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_public_phone_link_is_complete_and_dialable(self):
        result = subprocess.run(
            [sys.executable, "-c", "import build_ui; print(build_ui.PHONE_HREF)"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        href = result.stdout.strip()
        self.assertNotIn("*", href)
        self.assertRegex(href, r"^tel:\+\d{10,15}$")

    def test_planner_uses_api_contact_and_consent_contract(self):
        # The planner is now the only funnel, so it carries the contract that
        # app/server.py:create_trip() validates.
        src = (PROJECT / "build_planner.py").read_text(encoding="utf-8")
        for field in ('"contact_name"', '"contact_phone"', '"contact_email"'):
            self.assertIn(field, src)
        self.assertIn('name="consent"', src)
        self.assertIn("checkbox", src)
        # required checkbox must be validated by checked-state, not string value
        self.assertIn("el.type==='checkbox' ? el.checked", src)
        # no legacy mis-keyed names survive
        self.assertNotIn('f_text("name"', src)
        self.assertNotIn('f_text("phone"', src)

    def test_planner_javascript_checks_http_success(self):
        src = (PROJECT / "build_planner.py").read_text(encoding="utf-8")
        self.assertIn("ok:r.ok&&j.ok", src)
        self.assertNotIn(".then(function(){ done(true); })", src)

    def test_quote_pages_post_to_the_real_endpoint(self):
        for rel in ("request-quote", ""):
            page = (SITE / rel / "index.html").read_text(encoding="utf-8")
            self.assertIn('EP="/api/trip"', page, f"{rel or '/'} has no API endpoint wired")

    def test_planner_carries_the_bot_honeypot(self):
        # The standalone form had a hidden _hp trap; the planner replaced it and
        # silently lost the trap, leaving the server-side honeypot dead code.
        src = (PROJECT / "build_planner.py").read_text(encoding="utf-8")
        self.assertIn('name="_hp"', src)
        self.assertIn("hp&&hp.value", src)
        for rel in ("request-quote", ""):
            page = (SITE / rel / "index.html").read_text(encoding="utf-8")
            self.assertIn('name="_hp"', page, f"{rel or '/'} lost the honeypot")
            self.assertIn('aria-hidden="true"', page)

    def test_all_generated_pages_have_skip_link_and_main_landmark(self):
        pages = sorted(SITE.rglob("*.html"))
        self.assertGreaterEqual(len(pages), 20)
        for page in pages:
            text = page.read_text(encoding="utf-8")
            self.assertIn('class="skip-link"', text, str(page))
            self.assertEqual(text.count('<main id="main-content">'), 1, str(page))
            self.assertEqual(text.count("</main>"), 1, str(page))

    def test_mobile_whatsapp_does_not_float_over_forms(self):
        source = (PROJECT / "build_ui.py").read_text(encoding="utf-8")
        self.assertIn("grid-template-columns:repeat(3,1fr)", source)
        self.assertIn("@media(max-width:860px){.sticky{display:grid}.wa{display:none}", source)


class DeploymentContractTests(unittest.TestCase):
    """Regression tests for deploy.sh restart logic.

    The remote restart script runs as a shell whose own command line contains
    the launch command ('python3 server.py'). So any pkill/pgrep -f matching
    that filename also matches the shell executing it: the restart kills its
    own SSH connection (exit 255) and leaves the site down with no listener.
    The server must therefore be stopped by PORT.
    """

    def setUp(self):
        self.script = (PROJECT.parents[1] / "deploy.sh").read_text(encoding="utf-8")

    def test_restart_never_pkill_matches_the_server_filename(self):
        self.assertIsNone(
            re.search(r"^\s*pkill\b", self.script, re.M),
            "deploy.sh must not stop the server by command-pattern match",
        )

    def test_restart_stops_the_listener_by_port(self):
        self.assertIn("sport = :8100", self.script)
        self.assertIn("OLD_PID=", self.script)

    def test_status_pgrep_cannot_match_its_own_shell(self):
        self.assertNotIn('pgrep -f "http.server|server.py"', self.script)
        self.assertIn('pgrep -f "[h]ttp.server|[s]erver.py"', self.script)

    def test_failed_health_check_fails_the_deploy(self):
        self.assertNotIn("|| echo 'NO RESPONSE'", self.script)
        self.assertIn("curl -fsS -m 5 http://127.0.0.1:8100/health", self.script)


class SingleFunnelTests(unittest.TestCase):
    """There must be exactly one quote funnel.

    Two parallel implementations (the homepage planner and a standalone
    /request-quote/ form) drifted: different fields, different validation, and
    different payload key styles that the server had to paper over with
    `d.get("Pickup point") or d.get("pickup")`. /request-quote/ now renders the
    planner so there is one implementation to maintain.
    """

    def test_legacy_quote_funnel_is_gone_from_source(self):
        for name in ("build_pages.py", "build_v3.py", "build_ui.py"):
            src = (PROJECT / name).read_text(encoding="utf-8")
            self.assertNotIn("def quote_form(", src, f"{name} still defines the legacy form")
            self.assertNotIn("QUOTE_JS", src, f"{name} still references QUOTE_JS")

    def test_request_quote_page_renders_the_planner(self):
        page = (SITE / "request-quote" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="planner"', page)
        self.assertIn('id="plform"', page)
        self.assertIn('id="pl-next"', page)
        # the old form's signature must not be present anywhere on the page
        self.assertNotIn('name="trip_type"', page)
        self.assertNotIn("mailto:", page)

    def test_no_page_ships_two_funnels(self):
        for page in SITE.rglob("index.html"):
            html = page.read_text(encoding="utf-8")
            planners = html.count('id="planner"')
            self.assertLessEqual(
                planners, 1, f"{page.relative_to(SITE)} ships {planners} planners"
            )

    def test_force_urbania_page_does_not_presume_a_trip_type(self):
        # The product page used the 'local' preset, which pre-selected
        # 'City / Local' for every visitor regardless of their actual trip.
        page = (SITE / "force-urbania-hire-hyderabad" / "index.html").read_text(encoding="utf-8")
        self.assertIn('data-preset="custom"', page)
        self.assertNotIn('data-preset="local"', page)


class ServerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_module = load_server()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.server_module.DATA = cls.tmp.name
        cls.server_module.DB = os.path.join(cls.tmp.name, "trips.db")
        cls.server_module.ADMIN_TOKEN = "test-admin-token"
        cls.server_module._hits = {}
        cls.server_module.init_db()
        cls.httpd = cls.server_module.ThreadingHTTPServer(("127.0.0.1", 0), cls.server_module.H)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=2)
        cls.tmp.cleanup()

    def post_json(self, path, payload, headers=None):
        request_headers = {"Content-Type": "application/json"}
        request_headers.update(headers or {})
        req = Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=json.dumps(payload).encode(),
            headers=request_headers,
            method="POST",
        )
        with urlopen(req, timeout=3) as response:
            return response.status, json.loads(response.read())

    def test_planner_payload_shape_is_accepted(self):
        """The planner's collect() emits human-labelled keys for trip fields
        ('Pickup point') and snake_case keys for contact fields
        ('contact_phone'). Because the planner is now the ONLY funnel, the API
        must accept exactly that shape."""
        status, body = self.post_json("/api/trip", {
            "trip_type": "wedding",
            "Pickup point": "Banjara Hills",
            "Destination": "Ramoji Film City",
            "Travel date": "2026-11-14",
            "Passengers": "14",
            "contact_name": "Meera",
            "contact_phone": "9812345678",
            "contact_email": "meera@example.com",
            "consent": "Yes",
            "source_page": "/request-quote/",
        })
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        self.assertTrue(body["ref"].startswith("GT"))
        self.assertNotEqual(body["ref"], "GT000000", "honeypot path was taken")

        # the owner-facing summary must read sensibly from labelled keys
        conn = sqlite3.connect(self.server_module.DB)
        summary, email = conn.execute(
            "SELECT summary, email FROM trips WHERE ref=?", (body["ref"],)
        ).fetchone()
        conn.close()
        self.assertIn("wedding", summary)
        self.assertIn("Banjara Hills", summary)
        self.assertIn("2026-11-14", summary)
        self.assertIn("14 pax", summary)
        self.assertEqual(email, "meera@example.com")

    def test_trip_api_preserves_contact_email(self):
        status, body = self.post_json(
            "/api/trip",
            {
                "trip_type": "airport",
                "contact_name": "Test Traveller",
                "contact_phone": "9999999999",
                "contact_email": "traveller@example.test",
                "consent": "Yes",
                "pickup": "Banjara Hills",
                "destination": "HYD Airport",
            },
        )
        self.assertEqual(status, 200)
        with sqlite3.connect(self.server_module.DB) as conn:
            email = conn.execute("SELECT email FROM trips WHERE ref=?", (body["ref"],)).fetchone()[0]
        self.assertEqual(email, "traveller@example.test")

    def test_admin_browser_form_updates_status(self):
        _, body = self.post_json(
            "/api/trip",
            {
                "trip_type": "local",
                "contact_name": "Admin Test",
                "contact_phone": "9999999998",
                "consent": "Yes",
            },
        )
        payload = urlencode({"ref": body["ref"], "status": "BOOKED"}).encode()
        req = Request(
            f"http://127.0.0.1:{self.port}/admin/status",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded", "X-Admin-Token": "test-admin-token"},
            method="POST",
        )
        with urlopen(req, timeout=3) as response:
            result = json.loads(response.read())
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "BOOKED")

    def test_admin_board_marks_current_status_selected(self):
        _, body = self.post_json(
            "/api/trip",
            {
                "trip_type": "wedding",
                "contact_name": "Board Test",
                "contact_phone": "9999999997",
                "consent": "Yes",
            },
        )
        self.post_json(
            "/admin/status",
            {"ref": body["ref"], "status": "FOLLOW_UP"},
            {"X-Admin-Token": "test-admin-token"},
        )
        req = Request(
            f"http://127.0.0.1:{self.port}/admin?token=test-admin-token",
            headers={"X-Admin-Token": "test-admin-token"},
        )
        with urlopen(req, timeout=3) as response:
            html = response.read().decode()
        row = html[html.index(body["ref"]):]
        self.assertIn('<option selected>FOLLOW_UP</option>', row)


if __name__ == "__main__":
    unittest.main()
