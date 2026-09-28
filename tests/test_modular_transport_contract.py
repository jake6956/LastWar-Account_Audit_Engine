import unittest
from pathlib import Path

from reference_runtime import RuntimeModel

ROOT = Path(__file__).resolve().parents[1]


class ModularTransportCompatibilityTests(unittest.TestCase):
    def test_worker_exposes_optin_without_replacing_default_routes(self):
        worker = (ROOT / "infrastructure/cloudflare-worker.js").read_text(encoding="utf-8")
        for token in (
            'url.pathname === "/modular"',
            "SNAPSHOT_BASE_URL",
            "snapshotMatch",
            "3.3-chatgpt-linked-optin",
            "FIRST_PARTY_SNAPSHOT_BASE",
            "FIRST_PARTY_RESOURCE_INDEX",
            "renderModularHtml",
            "noindex, follow",
            "MODULAR_COMPATIBILITY_ENTRY",
            "If and only if the user's current instruction explicitly requests modular transport/testing",
        ):
            self.assertIn(token, worker)
        for route in ('url.pathname === "/"', 'url.pathname === "/install"', 'url.pathname === "/config.txt"'):
            self.assertIn(route, worker)

    def test_contract_blocks_default_cutover_without_fresh_host_evidence(self):
        contract = (ROOT / "contracts/modular-transport.md").read_text(encoding="utf-8")
        for token in (
            "Default installer remains unchanged",
            "root-provided modular handoff",
            "ChatGPT user-initiated navigation",
            "page-provided links",
            "partial retrieval",
            "fresh runtime/session",
            "LOCAL STATE",
            "Default cutover remains blocked",
        ):
            self.assertIn(token, contract)

    def test_modular_page_links_every_manifest_module(self):
        worker = (ROOT / "infrastructure/cloudflare-worker.js").read_text(encoding="utf-8")
        self.assertIn("manifest.modules.map", worker)
        self.assertIn("exactSnapshotUrl(sha, path)", worker)
        self.assertIn('module.required ? "Required" : "Optional"', worker)
        self.assertIn('module.required ? "required-module" : "optional-module"', worker)
        self.assertIn('meta name="robots" content="noindex,follow"', worker)
        self.assertIn("Do <strong>not</strong> synthesize", worker)

    def test_required_durable_account_fresh_runtime_matrix(self):
        # Existing durable account loaded after a modular-style fresh startup.
        prior = RuntimeModel()
        prior.create_account("A")
        prior.persistence_mode = "DURABLE"
        prior.ingest_direct_evidence(
            [{"key": "drone.level", "value": 155, "state_class": "MONOTONIC"}],
            observed_at="2026-09-27T22:00:00-05:00",
        )
        existing_snapshot = prior.durable_account_snapshot()

        host_one = RuntimeModel()
        host_one.load_durable_account_snapshot(existing_snapshot)
        result = host_one.ingest_direct_evidence(
            [
                {"key": "drone.level", "value": 156, "state_class": "MONOTONIC"},
                {"key": "overlord.attack_level", "value": 70, "state_class": "MONOTONIC"},
                {"key": "upgrade_ore", "value": 112700, "state_class": "VOLATILE"},
            ],
            observed_at="2026-09-28T08:30:00-05:00",
            source="screenshot",
            task_keys={"drone.level"},
        )
        self.assertTrue(result["committed"])

        persisted = host_one.durable_account_snapshot()
        host_two = RuntimeModel()
        host_two.load_durable_account_snapshot(persisted)

        self.assertEqual(host_two.accounts["A"].facts["drone.level"], 156)
        self.assertEqual(host_two.accounts["A"].facts["overlord.attack_level"], 70)
        self.assertEqual(host_two.accounts["A"].facts["upgrade_ore"], 112700)
        self.assertEqual(host_two.accounts["A"].hot_cache["upgrade_ore"], 112700)
        self.assertEqual(host_two.accounts["A"].state_health["drone.level"]["health_status"], "CURRENT")


if __name__ == "__main__":
    unittest.main()
