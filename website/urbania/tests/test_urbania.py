import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tarfile
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

    def test_tar_flag_array_survives_set_u_on_macos_bash(self):
        """macOS ships bash 3.2, where "${arr[@]}" on an EMPTY array is fatal
        under `set -u`. An earlier version of this script aborted mid-push with
        'TAR_FLAGS[@]: unbound variable'. The expansion must be guard-safe."""
        self.assertIn('${TAR_FLAGS[@]+"${TAR_FLAGS[@]}"}', self.script)
        self.assertNotIn('tar czf - "${TAR_FLAGS[@]}"', self.script)

        # the actual failure mode: empty array under `set -u` must not abort
        probe = subprocess.run(
            ["/bin/bash", "-c",
             'set -euo pipefail; a=(); printf "%s" ${a[@]+"${a[@]}"}; echo ok'],
            capture_output=True, text=True)
        self.assertEqual(probe.returncode, 0, probe.stderr)
        self.assertIn("ok", probe.stdout)

    def test_tar_flags_are_probed_by_use_not_by_help(self):
        # bsdtar's abbreviated --help does not list --no-mac-metadata even
        # though it accepts it, so a --help grep silently detects nothing.
        self.assertNotIn("--help 2>&1 | grep -q -- '--no-mac-metadata'", self.script)
        self.assertIn("--no-mac-metadata --no-xattrs", self.script)

    def test_apple_double_twins_are_actually_excluded(self):
        """`--exclude='._*'` alone does NOT stop bsdtar writing AppleDouble
        twins -- the archive still carried 102 members for 51 files, and GNU tar
        then made 51 ._* files on the VPS. Assert the archive matches the tree."""
        app = PROJECT / "app"
        real_files = sum(len(f) for _, _, f in os.walk(app)
                         if "data" not in _ and "__pycache__" not in _)
        if not real_files:
            self.skipTest("app tree not built")
        out = "/tmp/_urbania_tar_test.tgz"
        subprocess.run(["tar", "czf", out, "--no-mac-metadata", "--no-xattrs",
                        "--exclude=./data", "--exclude=./.admin_token", "."],
                       cwd=app, check=True, capture_output=True)
        with tarfile.open(out) as tf:
            names = tf.getnames()
        twins = [n for n in names if os.path.basename(n).startswith("._")]
        self.assertEqual(twins, [], f"archive still carries AppleDouble twins: {twins[:5]}")


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


class ContentHonestyTests(unittest.TestCase):
    """The brief forbids inventing specs, rates, distances, numbers or reviews.

    These tests enforce that at the source, so a placeholder cannot silently
    become a fabricated figure later.
    """

    def setUp(self):
        import site_data
        self.data = site_data

    def test_no_invented_rates_distances_or_counts(self):
        d = self.data
        for c in d.CONFIGURATIONS:
            self.assertIsNone(c["per_km"], f'{c["key"]} has an invented per_km rate')
            self.assertIsNone(c["per_day"], f'{c["key"]} has an invented per_day rate')
            self.assertIsNone(c["driver_allowance"])
            self.assertIsNone(c["min_km_per_day"])
            for field, val in c["specs"].items():
                self.assertIsNone(val, f'{c["key"]}.{field} invented')
        for r in d.ROUTES:
            self.assertIsNone(r["distance_km"], f'{r["name"]} has an invented distance')
            self.assertIsNone(r["drive_time"], f'{r["name"]} has an invented drive time')
        for label, val in d.TRUST_FIELDS:
            self.assertIsNone(val, f'trust field "{label}" is a fabricated number')
        self.assertEqual(d.REVIEWS, [], "reviews must not be fabricated")

    def test_unset_values_render_as_visible_placeholders(self):
        d = self.data
        self.assertNotIn("None", d.tbc(None))
        self.assertRegex(d.tbc(None), r"To be confirmed")
        # nb: &#8377; (the rupee entity) contains digits, so compare exactly
        # rather than scanning for digits.
        self.assertEqual(d.money(None), "&#8377;XX",
                         "an unset rate must render a placeholder, never a figure")
        self.assertEqual(d.tbc(None, suffix=" km"), "To be confirmed km")

    def test_group_size_recommendation_covers_9_to_17(self):
        d = self.data
        for n in range(9, 18):
            key, headline, detail = d.recommend(n)
            self.assertIsNotNone(key, f"{n} passengers resolved to no configuration")
            keys = {c["key"] for c in d.CONFIGURATIONS}
            self.assertIn(key, keys, f"{n} passengers -> unknown config {key}")
            self.assertTrue(headline and detail)

    def test_over_17_is_declined_not_absorbed(self):
        d = self.data
        key, headline, detail = d.recommend(18)
        self.assertIsNone(key)
        self.assertTrue(detail, "declining must still explain")
        for n in (18, 20, 40):
            self.assertEqual(len(d.recommend(n)), 3, "recommend() must always return a 3-tuple")

    def test_no_superlative_claims_in_rendered_pages(self):
        # The brief forbids '#1', 'best', 'largest' style unsupported claims.
        pattern = re.compile(r"#1\b|\bbest in (?:class|India)\b|\blargest\b", re.I)
        offenders = []
        for page in sorted(SITE.rglob("*.html")):
            visible = re.sub(r"<!--.*?-->", "", page.read_text(encoding="utf-8"), flags=re.S)
            visible = re.sub(r"<(script|style)\b.*?</\1>", "", visible, flags=re.S | re.I)
            m = pattern.search(visible)
            if m:
                offenders.append((str(page.relative_to(SITE)), m.group(0)))
        self.assertEqual(offenders, [], f"unsupported claims found: {offenders[:5]}")

    def test_no_fabricated_rupee_figures_are_rendered(self):
        for page in sorted(SITE.rglob("*.html")):
            html = page.read_text(encoding="utf-8")
            found = re.findall(r"&#8377;\d", html)
            self.assertEqual(found, [], f"{page.relative_to(SITE)} renders a rupee figure {found[:3]}")


class NewArchitectureTests(unittest.TestCase):
    """The new sections, funnel entry point and SEO architecture."""

    def test_hero_carries_the_primary_keyword(self):
        home = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("<h1>Force Urbania rental in Hyderabad</h1>", home)
        self.assertIn("Premium group travel for up to 17 passengers", home)

    def test_journey_bar_is_step_one_only(self):
        home = (SITE / "index.html").read_text(encoding="utf-8")
        bar = re.search(r'<form class="jbar".*?</form>', home, re.S)
        self.assertIsNotNone(bar, "hero journey bar is missing")
        markup = bar.group(0)
        for field in ("from", "to", "date", "pax"):
            self.assertIn(f'name="{field}"', markup)
        # step 1 must capture trip details only, never personal data
        self.assertNotIn("contact_", markup, "step 1 must not ask for contact details")
        self.assertNotIn("consent", markup)
        # and it must degrade without JS
        self.assertIn('method="get"', markup)
        self.assertIn('action="/request-quote/"', markup)

    def test_planner_accepts_the_journey_bar_handoff(self):
        src = (PROJECT / "build_planner.py").read_text(encoding="utf-8")
        self.assertIn("prefill", src)
        self.assertIn("URLSearchParams", src)
        # field names differ per mode, so more than one name must be tried
        self.assertIn("main_pickup", src)
        self.assertIn("destinations", src)

    def test_config_cards_cover_every_configuration(self):
        home = (SITE / "index.html").read_text(encoding="utf-8")
        import site_data
        self.assertEqual(home.count('class="cfgcard"'), len(site_data.CONFIGURATIONS))

    def test_group_size_selector_is_server_rendered(self):
        # must work and be indexable without JS
        home = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="fy-pax"', home)
        self.assertIn('id="fy-card"', home)

    def test_trust_and_reviews_are_placeholder_state(self):
        home = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertGreater(home.count('class="tcard"'), 0)
        self.assertIn("rev-empty", home)

    def test_seo_pages_exist_for_every_declared_route(self):
        import site_data
        expected = ["/rates/force-urbania-rental-rates-hyderabad/"]
        expected += [f'/fleet/{c["key"]}/' for c in site_data.CONFIGURATIONS]
        expected += [f'/destinations/hyderabad-to-{r["name"].lower()}/' for r in site_data.ROUTES]
        expected += [s["href"] for s in site_data.SERVICES if s["href"].startswith("/services/")]
        for path in expected:
            f = SITE / path.strip("/") / "index.html"
            self.assertTrue(f.exists(), f"declared page missing: {path}")

    def test_every_declared_page_is_in_the_sitemap(self):
        import site_data
        sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
        expected = [f'/fleet/{c["key"]}/' for c in site_data.CONFIGURATIONS]
        expected += [f'/destinations/hyderabad-to-{r["name"].lower()}/' for r in site_data.ROUTES]
        for path in expected:
            self.assertIn(path, sitemap, f"{path} missing from sitemap.xml")

    def test_submission_confirmation_lives_outside_the_form(self):
        """done() sets form.style.display='none' on success. While #pl-result sat
        inside that form the customer saw it vanish with no acknowledgement —
        and inner_text() still returned the text, so the flow test passed."""
        for rel in ("request-quote", ""):
            page = (SITE / rel / "index.html").read_text(encoding="utf-8")
            form = re.search(r'<form id="plform".*?</form>', page, re.S)
            self.assertIsNotNone(form, f"{rel or '/'} has no planner form")
            self.assertIn('id="pl-result"', page, f"{rel or '/'} has no result container")
            self.assertNotIn(
                'id="pl-result"', form.group(0),
                "the confirmation must sit OUTSIDE the form that gets hidden on success")

    def test_no_broken_internal_links(self):
        broken = []
        for page in sorted(SITE.rglob("*.html")):
            html = page.read_text(encoding="utf-8")
            for href in re.findall(r'href="(/[^"#?]*)"', html):
                if href.startswith("//"):
                    continue
                target = SITE / href.lstrip("/")
                if href.endswith("/") or target.is_dir():
                    target = target / "index.html"
                if not target.exists():
                    broken.append((str(page.relative_to(SITE)), href))
        self.assertEqual(broken[:10], [], f"{len(broken)} broken internal links")


class HtmlValidityTests(unittest.TestCase):
    """Catch malformed markup that renders as a layout bug.

    A missing </div> in fleet_status_note() made the quote bar a child of a
    display:flex notice, squashing the form inputs to a sliver. Every content
    test passed; only the screenshot showed it. This checks tag balance.
    """

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
            "meta", "param", "source", "track", "wbr",
            # svg primitives commonly self-closed
            "path", "rect", "circle", "line", "polygon", "polyline", "ellipse", "use", "stop"}

    def _balance(self, text):
        from html.parser import HTMLParser

        problems = []
        stack = []

        class P(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag in HtmlValidityTests.VOID:
                    return
                stack.append((tag, self.getpos()[0]))

            def handle_startendtag(self, tag, attrs):
                pass

            def handle_endtag(self, tag):
                if tag in HtmlValidityTests.VOID:
                    return
                if not stack:
                    problems.append(f"stray </{tag}> at line {self.getpos()[0]}")
                    return
                if stack[-1][0] == tag:
                    stack.pop()
                else:
                    # find a match further down
                    for i in range(len(stack) - 1, -1, -1):
                        if stack[i][0] == tag:
                            unclosed = stack[i + 1:]
                            for t, ln in unclosed:
                                problems.append(f"<{t}> opened line {ln} never closed")
                            del stack[i:]
                            break
                    else:
                        problems.append(f"stray </{tag}> at line {self.getpos()[0]}")

        parser = P(convert_charrefs=True)
        parser.feed(text)
        for t, ln in stack:
            problems.append(f"<{t}> opened line {ln} never closed")
        return problems

    def test_no_unclosed_structural_tags(self):
        offenders = {}
        for page in sorted(SITE.rglob("*.html")):
            problems = self._balance(page.read_text(encoding="utf-8"))
            if problems:
                offenders[str(page.relative_to(SITE))] = problems[:4]
        self.assertEqual(offenders, {}, f"unbalanced markup: {offenders}")

    def test_section_builders_emit_balanced_fragments(self):
        # check the components directly, so a new one cannot ship unbalanced
        import build_sections as SEC
        fragments = {
            "fleet_status_note": SEC.fleet_status_note(),
            "find_your_urbania": SEC.find_your_urbania(),
            "config_cards": SEC.config_cards(),
            "rates_table": SEC.rates_table(),
            "services_grid": SEC.services_grid(),
            "routes_grid": SEC.routes_grid(),
            "trust_strip": SEC.trust_strip(),
            "reviews_block": SEC.reviews_block(),
            "gallery_block": SEC.gallery_block(),
            "pricing_faq_block": SEC.pricing_faq_block(),
            "journey_bar": SEC.journey_bar(),
        }
        offenders = {}
        for name, frag in fragments.items():
            problems = self._balance(frag)
            if problems:
                offenders[name] = problems[:4]
        self.assertEqual(offenders, {}, f"unbalanced component markup: {offenders}")


class MediaPipelineTests(unittest.TestCase):
    """Photos and video must drop in without code changes — and their absence
    must fall back to a labelled illustration, never to stock imagery."""

    def setUp(self):
        import build_sections as SEC
        self.SEC = SEC
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        for path in getattr(self, "_made", []):
            if os.path.exists(path):
                os.remove(path)

    def _place(self, kind, name, ext=".png"):
        """Drop a file into the media tree.

        The build only checks existence, never image validity, so a stub header
        is enough here — and it keeps the test from depending on Pillow, which
        is deliberately not installed in this project.
        """
        os.makedirs(self.SEC.media_path(kind), exist_ok=True)
        p = self.SEC.media_path(kind, name + ext)
        with open(p, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n" + b"media-pipeline-test")
        # track the exact path: an earlier version tracked (kind, name) and only
        # swept image extensions, so a test .mp4 leaked and broke later tests
        self._made = getattr(self, "_made", []) + [p]
        return p

    def test_placeholder_state_when_no_media(self):
        st = self.SEC.media_status()
        for key, val in st.items():
            self.assertFalse(val, f"unexpected media present: {key}={val}")

    def test_missing_media_returns_none(self):
        self.assertIsNone(self.SEC.find_image("gallery", "does-not-exist"))

    def test_unknown_filenames_are_ignored(self):
        """A stray file must not be picked up as a slot."""
        self._place("gallery", "totally-made-up")
        self.assertIsNone(self.SEC.find_image("gallery", "exterior-front"))
        self.assertIsNone(self.SEC.find_image("gallery", "totally-made-up-suffix"))

    def test_gallery_slot_switches_to_photo_when_supplied(self):
        import re
        self._place("gallery", "exterior-front")
        block = self.SEC.gallery_block()
        self.assertIn('class="gfig"', block, "supplied photo did not render")
        self.assertIn("/media/gallery/exterior-front.png", block)

    def test_hero_uses_still_when_poster_supplied(self):
        self._place("hero", "hero-poster")
        hero = self.SEC.hero_visual()
        self.assertIn('class="hv-still"', hero)
        self.assertIn("/media/hero/hero-poster.png", hero)
        self.assertNotIn("Illustrative diagram", hero)

    def test_hero_uses_video_when_supplied(self):
        self._place("hero", "hero-poster")
        self._place("hero", "hero", ext=".mp4")
        hero = self.SEC.hero_visual()
        self.assertIn("<video", hero)
        for attr in ("autoplay", "muted", "loop", "playsinline", "poster="):
            self.assertIn(attr, hero, f"hero video missing {attr}")
        # a phone must get the still, not an autoplaying video
        self.assertIn('class="hv-mobile"', hero)

    def test_hero_falls_back_to_labelled_illustration(self):
        hero = self.SEC.hero_visual()
        self.assertIn("Illustrative diagram", hero)
        self.assertIn("not a photograph of the actual", hero)

    def test_alt_text_matches_provenance_flag(self):
        """The alt text must never claim ownership the owner has not asserted."""
        import site_data
        alt = self.SEC._alt_text()
        if site_data.ASSETS_ARE_OUR_VEHICLE:
            self.assertNotIn("representative", alt)
        else:
            self.assertIn("representative image", alt,
                          "alt text claims ownership while the flag is False")

    def test_seating_section_covers_the_reference_set(self):
        block = self.SEC.seating_block()
        self.assertIn("1x1", block)
        self.assertIn("2x1", block)
        import site_data
        for name, caption in site_data.SEATING_SLOTS:
            self.assertIn(name, block, f"seating slot {name} missing from the section")


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

    def get(self, path):
        req = Request(f"http://127.0.0.1:{self.port}{path}", method="GET")
        try:
            with urlopen(req, timeout=3) as response:
                return response.status, response.read().decode("utf-8", "replace")
        except HTTPError as e:
            return e.code, e.read().decode("utf-8", "replace")

    def test_unknown_path_serves_the_branded_404(self):
        """A missing URL must return the site's own page, not the stock Python
        error page, and must still carry a 404 status."""
        status, body = self.get("/definitely-missing")
        self.assertEqual(status, 404)
        self.assertIn("skip-link", body, "branded 404 page was not served")
        self.assertNotIn("Error response", body, "stock Python error page leaked through")

    def test_api_miss_still_returns_json_not_html(self):
        # the branded page is for pages; API/dynamic routes keep their contract
        req = Request(f"http://127.0.0.1:{self.port}/api/trip",
                      data=json.dumps({"_hp": ""}).encode(),
                      headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urlopen(req, timeout=3) as response:
                status, body = response.status, json.loads(response.read())
        except HTTPError as e:
            status, body = e.code, json.loads(e.read())
        self.assertEqual(status, 400)
        self.assertIn("error", body)
        self.assertEqual(body.get("error"), "missing_consent_or_contact")

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
