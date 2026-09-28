import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_URL = "https://lastwarai.com"
WORKER_NAME = "lwai-bootstrap"


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class InfrastructureBoundaryTests(unittest.TestCase):
    def test_worker_remains_transport_only(self):
        worker = text("infrastructure/cloudflare-worker.js")
        self.assertIn('const REPOSITORY = "jake6956/LastWar-Account_Audit_Engine"', worker)
        self.assertIn("const LIVE_REF =", worker)
        self.assertIn("/branches/main", worker)
        self.assertIn("BOOTSTRAP_FULL.txt", worker)
        self.assertIn("X-LWAI-Commit", worker)
        self.assertIn("cacheTtl: 0", worker)
        self.assertIn("public, max-age=31536000, immutable", worker)
        for forbidden in (
            "Google Drive",
            "Dropbox",
            "Skill Medals",
            "Black Market",
            "strategic baseline",
            "workspace schema 2.3",
            "engine_version:",
        ):
            self.assertNotIn(forbidden, worker)

    def test_mutable_worker_response_is_defensively_no_store(self):
        worker = text("infrastructure/cloudflare-worker.js")
        for token in (
            "no-store, no-cache, must-revalidate, max-age=0",
            '"CDN-Cache-Control": "no-store"',
            '"Cloudflare-CDN-Cache-Control": "no-store"',
            '"Surrogate-Control": "no-store"',
        ):
            self.assertIn(token, worker)

    def test_wrangler_pins_real_worker_and_disables_front_cache(self):
        raw = text("wrangler.jsonc")
        config = json.loads(raw)
        self.assertEqual(config["name"], WORKER_NAME)
        self.assertEqual(config["main"], "infrastructure/cloudflare-worker.js")
        self.assertIs(config["workers_dev"], False)
        self.assertIs(config["preview_urls"], False)
        self.assertIs(config["cache"]["enabled"], False)
        # Dashboard-managed Custom Domain/routes stay outside this file unless
        # deliberately migrated; do not accidentally rewrite routing topology.
        self.assertNotIn("route", config)
        self.assertNotIn("routes", config)

    def test_cloudflare_deployment_contract_records_actual_topology(self):
        policy = text("infrastructure/cloudflare-cache-policy.md")
        for token in (
            WORKER_NAME,
            "lastwarai.com",
            "Workers Routes",
            "intentionally empty",
            "cache.enabled = false",
            "workers_dev = false",
            "preview_urls = false",
            "must be disabled",
            "one final purge",
            "not a per-release requirement",
            "must not require Worker source edits",
        ):
            self.assertIn(token, policy)

    def test_current_public_docs_describe_single_response_transport(self):
        for path in (
            "docs/architecture.md",
            "docs/deployment.md",
            "docs/quick-install.md",
            "docs/BETA_TESTING.md",
        ):
            body = text(path)
            self.assertIn(PUBLIC_URL, body, path)
            self.assertRegex(body.lower(), r"single-response|same response|one response", path)
            self.assertNotIn("serves only the tiny Stage-0 locator", body, path)
            self.assertNotIn("retrieves the public locator", body, path)
            self.assertNotIn("Production `2026-08-29.15`", body, path)

    def test_optin_modular_transport_is_not_default_discovery(self):
        worker = text("infrastructure/cloudflare-worker.js")
        self.assertIn('url.pathname === "/modular"', worker)
        self.assertIn("SNAPSHOT_BASE_URL", worker)
        self.assertIn("snapshotMatch", worker)
        self.assertIn("3.3-chatgpt-linked-optin", worker)
        self.assertIn("noindex, follow", worker)

        sitemap_block = worker.split("const SITEMAP =", 1)[1].split("const ABOUT_HTML", 1)[0]
        about_block = worker.split("const ABOUT_HTML =", 1)[1].split("function commonHeaders", 1)[0]
        self.assertNotIn("/modular", sitemap_block)
        self.assertNotIn("/modular", about_block)
        self.assertNotIn("FIRST_PARTY_SNAPSHOT_BASE", about_block)
        self.assertNotIn("FIRST_PARTY_RESOURCE_INDEX", about_block)

        # Default routes remain the one-response BOOTSTRAP_FULL transport.
        self.assertIn('url.pathname === "/"', worker)
        self.assertIn('url.pathname === "/install"', worker)
        self.assertIn('url.pathname === "/config.txt"', worker)
        self.assertIn("getEngine(sha)", worker)

        # Root may expose one explicit opt-in handoff for ChatGPT, but does not execute modular by default.
        self.assertIn("MODULAR COMPATIBILITY HANDOFF", worker)
        self.assertIn("MODULAR_COMPATIBILITY_ENTRY", worker)
        self.assertIn("If and only if the user's current instruction explicitly requests modular transport/testing", worker)

    def test_beta_doc_never_advertises_legacy_shortener(self):
        beta = text("docs/BETA_TESTING.md")
        self.assertNotIn("tinyurl.com/2yxf7f5x", beta)
        self.assertIn("X-LWAI-Commit", beta)


if __name__ == "__main__":
    unittest.main()
