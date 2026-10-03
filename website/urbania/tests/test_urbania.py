import importlib.util
import gzip
import json
import os
from pathlib import Path
import re
import shutil
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
        """Figures that were never checked must not be published.

        Distances are now genuinely sourced, so the assertion changed from "must be
        absent" to "must be sourced": publishing a distance requires an entry in
        ROUTE_DISTANCE_SOURCES. That keeps the original guarantee — no unsourced
        number reaches a page — now that real figures exist.
        """
        d = self.data
        for c in d.CONFIGURATIONS:
            self.assertIsNone(c["per_km"], f'{c["key"]} has an invented per_km rate')
            self.assertIsNone(c["per_day"], f'{c["key"]} has an invented per_day rate')
            self.assertIsNone(c["driver_allowance"])
            self.assertIsNone(c["min_km_per_day"])
            for field, val in c["specs"].items():
                self.assertIsNone(val, f'{c["key"]}.{field} invented')
        for r in d.ROUTES:
            if r["distance_km"] is None:
                continue
            self.assertIsInstance(r["distance_km"], int,
                                  f'{r["name"]} distance must be a whole number of km')
            self.assertTrue(20 <= r["distance_km"] <= 2500,
                            f'{r["name"]} distance {r["distance_km"]} km is implausible')
            self.assertTrue(r["drive_time"],
                            f'{r["name"]} publishes a distance but no drive time')
            self.assertTrue(d.ROUTE_DISTANCE_SOURCES.get(r["name"]),
                            f'{r["name"]} publishes a distance with NO RECORDED SOURCE')
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
        """A rupee figure may appear only if it traces to sourced data.

        This originally banned EVERY rupee figure, because at the time none were
        verified. The indicative market ranges are now researched and authorised
        (Category B), so the guarantee was re-stated rather than dropped: each
        rendered figure must come from RATE_INDICATIVE or CONFIGURATIONS. An
        invented number still cannot reach a page.
        """
        import site_data
        allowed = set()
        for r in site_data.RATE_INDICATIVE:
            for v in (r["low"], r["high"]):
                allowed.add(site_data.money(v).replace("&#8377;", ""))
        for c in site_data.CONFIGURATIONS:
            for k in ("per_km", "per_day", "driver_allowance", "min_km_per_day"):
                v = c.get(k)
                if v is not None:
                    allowed.add(site_data.money(v).replace("&#8377;", ""))
        self.assertTrue(allowed, "no sourced rupee figures — test would pass vacuously")

        offenders = []
        for page in sorted(SITE.rglob("*.html")):
            html = page.read_text(encoding="utf-8")
            for m in re.finditer(r"&#8377;([0-9][0-9,]*)", html):
                if m.group(1) not in allowed:
                    offenders.append((page.relative_to(SITE).as_posix(), m.group(0)))
        self.assertEqual(offenders, [], f"unsourced rupee figures rendered: {offenders[:6]}")


class NewArchitectureTests(unittest.TestCase):
    """The new sections, funnel entry point and SEO architecture."""

    def test_hero_carries_the_primary_keyword(self):
        """The H1 must carry the keyword as TEXT. Asserting the exact markup made
        this break on a presentational change — the headline is now split across
        two lines with the second in the accent colour — even though the heading
        itself is unchanged. Compare the rendered text instead.
        """
        home = (SITE / "index.html").read_text(encoding="utf-8")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", home, re.S)
        self.assertIsNotNone(m, "no <h1> found on the homepage")
        text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip()
        self.assertIn("Force Urbania rental in Hyderabad", text,
                      f"H1 text does not carry the primary keyword: {text!r}")
        self.assertIn("Premium group transportation for airport transfers", home)

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

    def test_no_placeholder_state_is_published(self):
        """The site must not publish placeholder boxes.

        This test previously asserted the OPPOSITE — that the trust tiles and the
        empty-reviews box were present. Those were the loudest "unfinished" signal
        on the page, so they were removed and the guard is now on their absence.
        """
        problems = []
        for p in SITE.rglob("*.html"):
            t = p.read_text(encoding="utf-8")
            rel = p.relative_to(SITE).as_posix()
            if 'class="tcard"' in t and "To be confirmed" in t:
                problems.append((rel, "trust tiles showing To be confirmed"))
            if 'class="rev-empty"' in t:
                problems.append((rel, "empty reviews box"))
            if "&#8377;XX" in t:
                problems.append((rel, "placeholder price"))
        self.assertEqual(problems, [], f"placeholder state published: {problems}")

    def test_no_page_repeats_its_h1_as_a_section_heading(self):
        """A section H2 that repeats the page H1 verbatim reads as a copy-paste
        error, competes with the H1 in search results, and tells the reader they
        have already seen this. The rates page did exactly that.
        """
        problems = []
        for p in SITE.rglob("*.html"):
            t = p.read_text(encoding="utf-8")
            m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S)
            if not m:
                continue
            norm = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip().lower().rstrip(".")
            h1 = norm(m.group(1))
            if not h1:
                continue
            for h2 in re.findall(r"<h2[^>]*>(.*?)</h2>", t, re.S):
                if norm(h2) == h1:
                    problems.append((p.relative_to(SITE).as_posix(), h1))
        self.assertEqual(problems, [], f"H2 duplicates the H1: {problems}")

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
        # ISOLATION: these tests exercise the pipeline LOGIC, so they must not
        # depend on which real photos happen to ship. They previously read the
        # live media/ tree and asserted it was EMPTY — which broke the moment
        # real media was added, and would break again on every real photo.
        # Point MEDIA_ROOT at a throwaway dir instead.
        self._orig_media_root = SEC.MEDIA_ROOT
        self._tmp = tempfile.mkdtemp(prefix="urbania-media-")
        SEC.MEDIA_ROOT = self._tmp
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        for path in getattr(self, "_made", []):
            if os.path.exists(path):
                os.remove(path)
        self.SEC.MEDIA_ROOT = self._orig_media_root
        shutil.rmtree(self._tmp, ignore_errors=True)

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
        """The seating section's real content is the LAYOUT comparison (which is
        structural text, not a photo). Slot *filenames* only appear in placeholder
        mode, so asserting them here made this test a check on build mode rather
        than on content.
        """
        import site_data
        block = self.SEC.seating_block()
        self.assertIn("1x1", block)
        self.assertIn("2x1", block)
        for layout in site_data.SEAT_LAYOUTS:
            self.assertIn(layout["name"], block,
                          f"seating layout {layout['name']!r} missing from the section")
        if not site_data.SHOW_MEDIA_PLACEHOLDERS:
            for name, _ in site_data.SEATING_SLOTS:
                self.assertNotIn(f"{name}.jpg", block,
                                 f"seating section publishes the filename {name}.jpg")


class ShippedMediaTests(unittest.TestCase):
    """Guards on the media that ACTUALLY ships.

    Deliberately a separate class from MediaPipelineTests: that one isolates
    MEDIA_ROOT to a temp dir to test the logic, so it can never notice a defect
    in the real assets. These run against the real tree.
    """

    def setUp(self):
        import build_sections as SEC
        import site_data
        self.SEC, self.DATA = SEC, site_data

    # ---- dependency-free JPEG dimension reader -------------------------------
    @staticmethod
    def _jpeg_size(path):
        """Width/height from a JPEG's SOF marker.

        The project deliberately has no Pillow, and this exact defect — a source
        image whose aspect ratio fights the CSS box — is invisible to any test
        that only checks the file exists. Parsing the header directly costs
        ~20 lines and catches it.
        """
        with open(path, "rb") as fh:
            data = fh.read()
        if data[:2] != b"\xff\xd8":
            raise AssertionError(f"{path} is not a JPEG")
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h = int.from_bytes(data[i + 5:i + 7], "big")
                w = int.from_bytes(data[i + 7:i + 9], "big")
                return w, h
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
            else:
                i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
        raise AssertionError(f"no SOF marker found in {path}")

    def test_shipped_hero_poster_is_portrait_like_its_box(self):
        """The hero still box is portrait; a landscape poster gets centre-cropped
        by object-fit:cover and can cut the wordmark in half. That shipped once —
        the wordmark rendered as 'anLoop'. Poster and box must agree.
        """
        path = self.SEC.media_path("hero", "hero-poster.jpg")
        if not os.path.exists(path):
            self.skipTest("no hero poster shipped yet")
        w, h = self._jpeg_size(path)
        self.assertGreater(h, w, f"hero poster is {w}x{h} — landscape in a "
                                 f"portrait box will be centre-cropped")

    def test_shipped_gallery_photos_are_landscape_like_their_box(self):
        """The gallery figure box is 274x206 — 1.333 (4:3). A portrait source is
        centre-cropped top and bottom, so the two tiles in one row end up
        inconsistently framed. Measured in the DOM, not assumed.
        """
        import site_data
        checked = 0
        for name, _ in site_data.GALLERY_SLOTS:
            url = self.SEC.find_image("gallery", name)
            if not url:
                continue
            path = self.SEC.media_path("gallery", os.path.basename(url))
            w, h = self._jpeg_size(path)
            self.assertGreater(w, h, f"gallery photo {name} is {w}x{h} — portrait "
                                     f"in a 4:3 box will be cropped top and bottom")
            checked += 1
        if not checked:
            self.skipTest("no gallery photos shipped yet")

    def test_shipped_gallery_photos_render_as_figures(self):
        import site_data
        block = self.SEC.gallery_block()
        supplied = [n for n, _ in site_data.GALLERY_SLOTS
                    if self.SEC.find_image("gallery", n)]
        self.assertTrue(supplied, "no gallery photos shipped")
        for name in supplied:
            self.assertIn(f'/media/gallery/{name}.', block,
                          f"shipped gallery photo {name} did not render")
        self.assertEqual(block.count('class="gfig"'), len(supplied),
                         "rendered figure count != shipped photo count")

    def test_shipped_media_never_claims_ownership(self):
        """Whatever ships, the caption must state provenance honestly.

        The blacklist is checked as WHOLE phrases that can only appear in a
        positive ownership claim. A bare substring like "photograph of our"
        false-positives on the disclaimer "not a photograph of our own vehicle",
        which says the opposite — so the disclaimer is asserted first and the
        blacklist restricted to claims that cannot be a negation.
        """
        if self.DATA.ASSETS_ARE_OUR_VEHICLE:
            self.skipTest("owner has asserted these are our own vehicle")
        hero = self.SEC.hero_visual()
        if 'class="hv-still"' in hero or "<video" in hero:
            self.assertIn("representative image", hero)
            self.assertIn("not a photograph of our own vehicle", hero)
            for claim in ("of our Force Urbania.", "our vehicle is shown",
                          "Photograph of our vehicle", "<b>Our vehicle"):
                self.assertNotIn(claim, hero,
                                 f"shipped media implies ownership: {claim!r}")

    def test_built_pages_never_publish_media_filenames(self):
        """A dashed placeholder naming the expected file is a shot list for the
        owner; on a live page ten of them make the site look unfinished. With the
        flag off, no built page may carry a slot box.
        """
        if self.DATA.SHOW_MEDIA_PLACEHOLDERS:
            self.skipTest("placeholder mode is deliberately on")
        offenders = [p.relative_to(SITE).as_posix()
                     for p in SITE.rglob("*.html")
                     if 'class="gslot"' in p.read_text(encoding="utf-8")]
        self.assertEqual(offenders, [],
                         f"built pages publish media filenames: {offenders}")

    def test_every_referenced_media_url_resolves(self):
        """Any /media/... URL in the built HTML must point at a file that exists —
        otherwise the page ships a broken image."""
        missing = []
        for page in SITE.rglob("*.html"):
            text = page.read_text(encoding="utf-8")
            for url in set(re.findall(r'(?:src|href)="(/media/[^"]+)"', text)):
                if not (SITE / url.lstrip("/")).exists():
                    missing.append((page.relative_to(SITE).as_posix(), url))
        self.assertEqual(missing, [], f"built pages reference missing media: {missing}")


class BrandWiringTests(unittest.TestCase):
    """The identity in brand/logo/ must actually be wired into the pages.

    The identity was built and then never used: every page shipped as
    "Urbania Hyderabad" behind a "17" tile while the real wordmark sat unread in
    brand/logo/. Nothing failed, because no test asserted the wiring.
    """

    def setUp(self):
        import build_ui
        self.UI = build_ui

    def test_brand_name_is_the_locked_name(self):
        self.assertEqual(self.UI.BRAND, "UrbanLoop")
        self.assertEqual(self.UI.TAGLINE, "Premium Group Mobility")

    def test_header_inlines_the_real_mark_not_a_tile(self):
        h = self.UI.header()
        self.assertIn('class="brandmark"', h, "header does not use the master mark")
        self.assertIn("<path", h, "mark is not inline vector artwork")
        self.assertNotIn('class="mk"', h, "header still renders the placeholder tile")
        self.assertNotIn(">17<", h)

    def test_footer_inlines_the_real_mark(self):
        f = self.UI.footer()
        self.assertIn('class="brandmark"', f)
        self.assertNotIn('class="mk"', f)

    def test_missing_brand_asset_raises_instead_of_falling_back(self):
        """A silent placeholder is exactly the failure that shipped."""
        orig = self.UI.BRAND_DIR
        try:
            self.UI.BRAND_DIR = "/nonexistent/brand/dir"
            with self.assertRaises(SystemExit):
                self.UI.brand_svg("urbanloop-lockup-horizontal-dark.svg")
        finally:
            self.UI.BRAND_DIR = orig

    def test_no_built_page_carries_the_old_brand_or_tile(self):
        offenders = []
        for page in SITE.rglob("*.html"):
            text = page.read_text(encoding="utf-8")
            rel = page.relative_to(SITE).as_posix()
            if "Urbania Hyderabad" in text:
                offenders.append((rel, "old brand name"))
            if 'class="mk"' in text:
                offenders.append((rel, "placeholder 17 tile"))
        self.assertEqual(offenders, [], f"stale branding in built pages: {offenders}")

    def test_dial_links_are_well_formed(self):
        """Numeric strings get masked as **** in tool output, so a hand-typed
        href silently corrupts every call button. Derive it and assert it."""
        digits = self.UI.PHONE_HREF.replace("tel:+", "")
        self.assertTrue(digits.isdigit(), f"PHONE_HREF has non-digits: {digits!r}")
        self.assertEqual(len(digits), 12, f"expected 12 digits, got {len(digits)}")
        self.assertNotIn("*", self.UI.PHONE_HREF)
        # and it must actually appear on the pages
        self.assertIn(self.UI.PHONE_HREF, (SITE / "index.html").read_text(encoding="utf-8"))


class CompressionTests(unittest.TestCase):
    """Text assets are gzipped; binaries are not; content is byte-identical."""

    @classmethod
    def setUpClass(cls):
        import socket
        cls.port = int(os.environ.get("URBANIA_TEST_PORT", "8140"))
        try:
            with socket.create_connection(("127.0.0.1", cls.port), timeout=2):
                pass
        except OSError:
            raise unittest.SkipTest(f"no server on :{cls.port}")

    def _get(self, path, accept="gzip"):
        req = Request(f"http://127.0.0.1:{self.port}{path}",
                      headers={"Accept-Encoding": accept} if accept else {})
        try:
            with urlopen(req, timeout=10) as r:
                return r.status, dict(r.headers), r.read()
        except HTTPError as e:
            return e.code, dict(e.headers), e.read()

    def test_html_is_gzipped_and_decodes_identically(self):
        """The whole point is a smaller payload that is still the same document."""
        _, h_gz, body_gz = self._get("/")
        self.assertEqual(h_gz.get("Content-Encoding"), "gzip",
                         "HTML is not compressed — pages ship ~90 KB each")
        self.assertEqual(gzip.decompress(body_gz).decode("utf-8")[:15], "<!DOCTYPE html>")
        _, _, body_plain = self._get("/", accept=None)
        self.assertEqual(gzip.decompress(body_gz), body_plain,
                         "gzipped body differs from the plain body")
        self.assertLess(len(body_gz), len(body_plain) * 0.5,
                        "compression saved almost nothing")

    def test_directory_urls_are_compressed_too(self):
        """'/' and '/about/' are directories. A naive isfile() check skips them and
        compresses only CSS — which is exactly the bug this guards."""
        for path in ("/", "/about/", "/rates/force-urbania-rental-rates-hyderabad/"):
            _, h, _ = self._get(path)
            self.assertEqual(h.get("Content-Encoding"), "gzip", f"{path} not compressed")

    def test_binary_assets_are_not_gzipped(self):
        jpg = (SITE / "media" / "hero" / "hero-split.jpg")
        if not jpg.exists():
            self.skipTest("no jpeg shipped")
        _, h, body = self._get("/media/hero/hero-split.jpg")
        self.assertNotEqual(h.get("Content-Encoding"), "gzip",
                            "JPEG compressed — wasteful and pointless")
        self.assertEqual(body[:2], b"\xff\xd8", "served bytes are not the JPEG")

    def test_404_stays_404_when_compressed(self):
        status, h, _ = self._get("/definitely-missing")
        self.assertEqual(status, 404)
        self.assertEqual(h.get("Content-Encoding"), "gzip")

    def test_no_accept_encoding_gets_a_plain_body(self):
        _, h, body = self._get("/", accept=None)
        self.assertIsNone(h.get("Content-Encoding"))
        self.assertEqual(body[:15], b"<!DOCTYPE html>")


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
