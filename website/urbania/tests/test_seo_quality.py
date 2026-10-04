import json
import re
import unittest
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit


PROJECT = Path(__file__).resolve().parents[1]
SITE = PROJECT / "app" / "site"
BASE = "https://urbanloop.co"


def pages():
    return sorted(SITE.rglob("*.html"))


def attr(text, pattern):
    match = re.search(pattern, text, re.S)
    return match.group(1) if match else ""


class SEOQualityTests(unittest.TestCase):
    def test_no_placeholder_domain_is_shipped(self):
        for path in SITE.rglob("*"):
            if path.is_file() and path.suffix in {".html", ".xml", ".txt"}:
                self.assertNotIn("urbania-hyderabad.example", path.read_text(encoding="utf-8"), str(path))

    def test_indexable_pages_have_unique_metadata_and_canonicals(self):
        seen = {"title": {}, "description": {}, "h1": {}}
        for path in pages():
            text = path.read_text(encoding="utf-8")
            robots = attr(text, r'<meta name="robots" content="([^"]+)"')
            if robots.startswith("noindex"):
                continue
            values = {
                "title": attr(text, r"<title>(.*?)</title>"),
                "description": attr(text, r'<meta name="description" content="([^"]*)"'),
                "h1": attr(text, r"<h1[^>]*>(.*?)</h1>"),
            }
            canonical = attr(text, r'<link rel="canonical" href="([^"]+)"')
            self.assertTrue(canonical.startswith(BASE + "/"), str(path))
            for key, value in values.items():
                normalized = re.sub(r"<[^>]+>", " ", value)
                normalized = re.sub(r"\s+", " ", normalized).strip().lower()
                self.assertTrue(normalized, f"missing {key}: {path}")
                if normalized in seen[key]:
                    self.fail(f"duplicate {key}: {path} and {seen[key][normalized]}")
                seen[key][normalized] = path

    def test_sitemap_contains_only_indexable_existing_pages(self):
        sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
        urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(all(url.startswith(BASE + "/") for url in urls))
        for path in pages():
            text = path.read_text(encoding="utf-8")
            rel = "/" if path == SITE / "index.html" else "/" + str(path.relative_to(SITE).parent) + "/"
            in_map = BASE + rel in urls
            noindex = 'content="noindex' in text
            self.assertEqual(in_map, not noindex, f"sitemap/indexability mismatch: {rel}")

    def test_json_ld_is_parseable(self):
        for path in pages():
            text = path.read_text(encoding="utf-8")
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
            self.assertGreaterEqual(len(blocks), 2, str(path))
            for block in blocks:
                json.loads(block)

    def test_destination_routes_use_destination_hub(self):
        for path in (SITE / "destinations").glob("hyderabad-to-*/index.html"):
            text = path.read_text(encoding="utf-8")
            self.assertIn('href="/destinations/"', text, str(path))

    def test_internal_page_links_resolve_without_treating_assets_as_pages(self):
        known = {"/"}
        for path in pages():
            if path == SITE / "index.html":
                continue
            known.add("/" + str(path.relative_to(SITE).parent).replace("\\", "/") + "/")
        asset_prefixes = ("/media/", "/style.css", "/favicon.svg", "/og.png")
        broken = []
        for path in pages():
            text = path.read_text(encoding="utf-8")
            for href in re.findall(r'href="(/[^"#?]*)', text):
                href = unescape(href)
                if href.startswith(asset_prefixes) or href.startswith("/api/"):
                    continue
                target = href if href == "/" or href.endswith("/") else href + "/"
                if target not in known:
                    broken.append((str(path.relative_to(SITE)), href))
        self.assertEqual(broken, [], f"broken internal page links: {broken[:20]}")

    def test_indexable_images_have_alt_text_and_dimensions(self):
        missing = []
        for path in pages():
            for tag in re.findall(r"<img\b[^>]*>", path.read_text(encoding="utf-8"), re.I):
                if 'aria-hidden="true"' in tag:
                    continue
                if not re.search(r'\balt="[^"]+"', tag):
                    missing.append((str(path.relative_to(SITE)), "alt"))
                if not re.search(r'\bwidth="\d+"', tag) or not re.search(r'\bheight="\d+"', tag):
                    missing.append((str(path.relative_to(SITE)), "dimensions"))
        self.assertEqual(missing, [], f"image accessibility/performance gaps: {missing}")

    def test_national_shared_pages_do_not_leak_local_service_copy(self):
        local_terms = ("hyderabad", "telangana", "rgia", "shamshabad")
        for rel in ("index.html", "find-a-vehicle/index.html", "how-it-works/index.html", "guides/index.html"):
            text = (SITE / rel).read_text(encoding="utf-8").lower()
            leaked = {term: text.count(term) for term in local_terms if term in text}
            self.assertEqual(leaked, {}, f"local copy leaked into shared page {rel}: {leaked}")

    def test_national_service_cohort_is_crawlable_and_linked_from_india(self):
        india = (SITE / "india/index.html").read_text(encoding="utf-8")
        paths = (
            "/services/airport-group-transfers/",
            "/services/wedding-guest-transport/",
            "/services/corporate-group-transport/",
            "/services/outstation-group-travel/",
            "/services/pilgrimage-group-travel/",
            "/services/events-group-transport/",
        )
        sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
        for path in paths:
            self.assertIn(f'href="{path}"', india)
            self.assertIn(BASE + path, sitemap)
            page = SITE / path.strip("/") / "index.html"
            text = page.read_text(encoding="utf-8")
            self.assertIn('content="index, follow', text)
            self.assertIn(f'href="{BASE}{path}"', text)


if __name__ == "__main__":
    unittest.main()
