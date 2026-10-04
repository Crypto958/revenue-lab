import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FUNCTION = ROOT / "website" / "urbania" / "netlify" / "functions" / "trip.mjs"
NETLIFY = ROOT / "netlify.toml"


class NetlifyBackendContractTests(unittest.TestCase):
    def test_function_exists_and_has_trip_contract(self):
        source = FUNCTION.read_text(encoding="utf-8")
        self.assertIn('getStore({ name: "trip-requests"', source)
        self.assertIn('request.method === "POST"', source)
        self.assertIn('request.method === "GET"', source)
        self.assertIn('missing_consent_or_contact', source)
        self.assertIn('return json({ ok: true, ref, status:', source)

    def test_netlify_rewrites_preserve_frontend_api_paths(self):
        config = NETLIFY.read_text(encoding="utf-8")
        self.assertRegex(config, r'from = "/api/trip"')
        self.assertRegex(config, r'from = "/api/trip/\*"')
        self.assertIn('directory = "website/urbania/netlify/functions"', config)

    def test_function_does_not_return_private_payload_on_status_lookup(self):
        source = FUNCTION.read_text(encoding="utf-8")
        status_block = source.split("async function getStatus", 1)[1]
        self.assertNotIn("payload", status_block.split("export default", 1)[0])


if __name__ == "__main__":
    unittest.main()
