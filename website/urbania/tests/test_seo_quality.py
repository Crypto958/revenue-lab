import json
import re
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
