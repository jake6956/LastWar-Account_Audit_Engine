import unittest
from pathlib import Path

from reference_runtime import RuntimeModel

ROOT = Path(__file__).resolve().parents[1]


class ModularTransportCompatibilityTests(unittest.TestCase):
    def test_worker_exposes_optin_without_replacing_default_routes(self):
        worker = (ROOT / "infrastructure/cloudflare-worker.js").read_text(encoding="utf-8")
        for token in (
            'url.pathname === "/modular"',
            "/snapshot/",
            "3.2-modular-optin",
            "FIRST_PARTY_SNAPSHOT_BASE",
            "noindex, nofollow",
        ):
            self.assertIn(token, worker)
        for route in ('url.pathname === "/"', 'url.pathname === "/install"', 'url.pathname === "/config.txt"'):
            self.assertIn(route, worker)

    def test_contract_blocks_default_cutover_without_fresh_host_evidence(self):
        contract = (ROOT / "contracts/modular-transport.md").read_text(encoding="utf-8")
        for token in (
            "Default installer remains unchanged",
            "same-origin-only host",
            "partial retrieval",
            "fresh runtime/session",
            "LOCAL STATE",
            "default cutover remains blocked",
        ):
            self.assertIn(token, contract)

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
