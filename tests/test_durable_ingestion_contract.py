import unittest
from pathlib import Path

from reference_runtime import RuntimeModel

ROOT = Path(__file__).resolve().parents[1]


class DurableEvidenceIngestionTests(unittest.TestCase):
    def durable_runtime(self, account_id="A"):
        rt = RuntimeModel()
        rt.create_account(account_id)
        rt.persistence_mode = "DURABLE"
        return rt

    def test_multifact_screenshot_persists_all_supported_facts_not_only_task_fact(self):
        rt = self.durable_runtime()
        result = rt.ingest_direct_evidence(
            [
                {"key": "drone.level", "value": 156, "state_class": "MONOTONIC"},
                {"key": "overlord.attack_level", "value": 70, "state_class": "MONOTONIC"},
                {"key": "upgrade_ore", "value": 112700, "state_class": "VOLATILE"},
            ],
            observed_at="2026-09-28T01:00:00-05:00",
            task_keys={"drone.level"},
        )
        self.assertTrue(result["committed"])
        self.assertEqual(set(result["persisted_keys"]), {"drone.level", "overlord.attack_level", "upgrade_ore"})
        self.assertEqual(rt.accounts["A"].facts["overlord.attack_level"], 70)
        self.assertEqual(rt.accounts["A"].hot_cache["upgrade_ore"], 112700)

    def test_newer_direct_monotonic_fact_supersedes_stale_durable_value(self):
        rt = self.durable_runtime()
        rt.write_fact("drone.level", 153)
        rt.ingest_direct_evidence(
            [{"key": "drone.level", "value": 156, "state_class": "MONOTONIC"}],
            observed_at="2026-09-28T01:01:00-05:00",
        )
        self.assertEqual(rt.accounts["A"].facts["drone.level"], 156)
        self.assertIn(("drone.level", 153, 156), rt.accounts["A"].history)

    def test_volatile_observation_persists_freshness_metadata(self):
        rt = self.durable_runtime()
        rt.ingest_direct_evidence(
            [{"key": "upgrade_ore", "value": 112700, "state_class": "VOLATILE", "confidence": "HIGH"}],
            observed_at="2026-09-28T01:02:00-05:00",
            source="screenshot",
        )
        meta = rt.accounts["A"].fact_metadata["upgrade_ore"]
        self.assertEqual(meta["state_class"], "VOLATILE")
        self.assertEqual(meta["observed_at"], "2026-09-28T01:02:00-05:00")
        self.assertEqual(meta["source"], "screenshot")
        self.assertEqual(rt.accounts["A"].state_health["upgrade_ore"]["health_status"], "CURRENT")

    def test_ambiguous_or_unsupported_observation_is_not_invented(self):
        rt = self.durable_runtime()
        result = rt.ingest_direct_evidence(
            [
                {"key": "known.level", "value": 7},
                {"key": "mystery_icon", "value": 9, "ambiguous": True},
                {"key": None, "value": 12, "ambiguous": True},
                {"key": "decorative_badge", "value": "gold", "decorative": True},
            ],
            observed_at="2026-09-28T01:03:00-05:00",
        )
        self.assertEqual(result["persisted_keys"], ["known.level"])
        self.assertNotIn("mystery_icon", rt.accounts["A"].facts)
        self.assertNotIn("decorative_badge", rt.accounts["A"].facts)

    def test_partial_write_failure_is_recovery_required_not_committed(self):
        rt = self.durable_runtime()
        with self.assertRaises(RuntimeError):
            rt.ingest_direct_evidence(
                [{"key": "drone.level", "value": 156, "state_class": "MONOTONIC"}],
                observed_at="2026-09-28T01:04:00-05:00",
                fail_after="canonical",
            )
        cp = rt.checkpoints["INGEST-1"]
        self.assertEqual(cp.status, "RECOVERY_REQUIRED")
        self.assertEqual(rt.accounts["A"].facts["drone.level"], 156)
        self.assertNotIn("drone.level", rt.accounts["A"].hot_cache)
        self.assertFalse(any(event.event_type == "COMMIT" for event in rt.journal if event.checkpoint_id == "INGEST-1"))
        self.assertIn("history", cp.pending_actions)

    def test_successful_transaction_is_verified_before_commit(self):
        rt = self.durable_runtime()
        result = rt.ingest_direct_evidence(
            [{"key": "drone.level", "value": 156}],
            observed_at="2026-09-28T01:05:00-05:00",
        )
        cp = rt.checkpoints[result["checkpoint_id"]]
        self.assertEqual(cp.status, "COMMITTED")
        events = [event.event_type for event in rt.journal if event.checkpoint_id == cp.checkpoint_id]
        self.assertEqual(events[-2:], ["VERIFY", "COMMIT"])
        self.assertEqual(cp.last_safe_point, "verified evidence commit")

    def test_successful_transaction_survives_fresh_runtime(self):
        rt = self.durable_runtime()
        rt.ingest_direct_evidence(
            [
                {"key": "drone.level", "value": 156, "state_class": "MONOTONIC"},
                {"key": "upgrade_ore", "value": 112700, "state_class": "VOLATILE"},
            ],
            observed_at="2026-09-28T01:06:00-05:00",
        )
        snapshot = rt.durable_account_snapshot()

        fresh = RuntimeModel()
        fresh.load_durable_account_snapshot(snapshot)
        self.assertEqual(fresh.accounts["A"].facts["drone.level"], 156)
        self.assertEqual(fresh.accounts["A"].hot_cache["upgrade_ore"], 112700)
        self.assertEqual(fresh.accounts["A"].fact_metadata["upgrade_ore"]["state_class"], "VOLATILE")
        self.assertEqual(fresh.accounts["A"].last_updated, "2026-09-28T01:06:00-05:00")

    def test_ingestion_preserves_active_account_isolation(self):
        rt = self.durable_runtime("A")
        rt.ingest_direct_evidence(
            [{"key": "drone.level", "value": 156}],
            observed_at="2026-09-28T01:07:00-05:00",
        )
        rt.create_account("B")
        rt.persistence_mode = "DURABLE"
        rt.ingest_direct_evidence(
            [{"key": "drone.level", "value": 140}],
            observed_at="2026-09-28T01:08:00-05:00",
        )
        self.assertEqual(rt.accounts["A"].facts["drone.level"], 156)
        self.assertEqual(rt.accounts["B"].facts["drone.level"], 140)

    def test_public_contract_is_durability_first_and_sanitized(self):
        body = (ROOT / "contracts/evidence-ingestion.md").read_text(encoding="utf-8")
        for token in (
            "Task relevance must never determine persistence relevance",
            "observe",
            "persist",
            "reconcile",
            "verification-read",
            "RECOVERY_REQUIRED",
            "active_account_id",
            "ACCOUNT STATE",
        ):
            self.assertIn(token, body)
        self.assertNotIn("Jake", body)
        self.assertNotIn("Server 1901", body)


if __name__ == "__main__":
    unittest.main()
