"""Read-preflight regression coverage: no chat memory or Hot Cache fallback."""
import unittest
from pathlib import Path
from reference_runtime import RuntimeModel

ROOT = Path(__file__).resolve().parents[1]
OLD = "2026-08-01T10:00:00-05:00"
NEW = "2026-10-12T10:00:00-05:00"
NOW = "2026-10-13T10:00:00-05:00"


class CanonicalReadPreflightTests(unittest.TestCase):
    def runtime(self):
        rt = RuntimeModel()
        rt.create_account("synthetic-A")
        rt.persistence_mode = "DURABLE"
        return rt

    def seeded_snapshot(self):
        rt = self.runtime()
        rt.ingest_direct_evidence([
            {"key": "squad.primary_power", "value": 42.0, "state_class": "VOLATILE"},
            {"key": "drone.level", "value": 177, "state_class": "MONOTONIC"},
        ], observed_at=NEW, source="screenshot")
        return rt.durable_account_snapshot()

    def test_new_session_reads_newer_canonical_not_old_memory_or_hot_cache(self):
        snapshot = self.seeded_snapshot()
        fresh = self.runtime()
        fresh.accounts["synthetic-A"].hot_cache["squad.primary_power"] = 31.0
        fresh.accounts["synthetic-A"].facts["drone.level"] = 150
        invoked = []
        def provider(account_id):
            invoked.append(account_id)
            return snapshot
        view = fresh.resolve_account_view(fetch_canonical=provider,
            required_keys=["squad.primary_power", "drone.level"], now=NOW, max_volatile_age_hours=48)
        self.assertEqual(invoked, ["synthetic-A"])
        self.assertEqual(view["status"], "VERIFIED")
        self.assertEqual(view["fields"]["squad.primary_power"]["value"], 42.0)
        self.assertEqual(view["fields"]["drone.level"]["value"], 177)
        self.assertEqual(view["fields"]["drone.level"]["observed_at"], NEW)

    def test_dedicated_domain_record_beats_same_day_preset_description(self):
        snapshot = self.seeded_snapshot()
        # Same-day preset text is a non-authoritative projection, not a field source.
        snapshot["preset_notes"] = {"drone.level": 176, "updated_at": NEW}
        rt = self.runtime()
        view = rt.resolve_account_view(
            fetch_canonical=lambda _: snapshot, required_keys=["drone.level"])
        self.assertEqual(view["fields"]["drone.level"]["value"], 177)
        source_contract = (ROOT / "engine/modules/core/state-freshness.txt").read_text(encoding="utf-8")
        self.assertIn("DOMAIN OWNERSHIP PRECEDENCE", source_contract)
        self.assertIn("preset descriptions", source_contract)
        standalone = (ROOT / "engine/BOOTSTRAP_FULL.txt").read_text(encoding="utf-8")
        self.assertIn("Authoritative domain owner records outrank", standalone)

    def test_provider_error_does_not_silently_use_old_cache(self):
        rt = self.runtime()
        rt.accounts["synthetic-A"].facts["drone.level"] = 100
        def fail(_):
            raise OSError("simulated provider outage")
        view = rt.resolve_account_view(fetch_canonical=fail, required_keys=["drone.level"])
        self.assertEqual(view["status"], "NOT_VERIFIED")
        self.assertNotIn("drone.level", view["fields"])

    def test_wrong_account_cannot_satisfy_preflight(self):
        rt = self.runtime()
        view = rt.resolve_account_view(
            fetch_canonical=lambda _: {"account_id": "synthetic-B", "facts": {"drone.level": 300}},
            required_keys=["drone.level"])
        self.assertEqual(view["status"], "NOT_VERIFIED")
        self.assertIn("mismatch", view["reason"])

    def test_newer_direct_field_overrides_only_that_field(self):
        rt = self.runtime()
        view = rt.resolve_account_view(
            fetch_canonical=lambda _: self.seeded_snapshot(),
            required_keys=["squad.primary_power", "drone.level"],
            session_observations=[{"key": "drone.level", "value": 178, "observed_at": NOW, "source": "direct"}],
            now=NOW, max_volatile_age_hours=48)
        self.assertEqual(view["fields"]["drone.level"]["value"], 178)
        self.assertEqual(view["fields"]["squad.primary_power"]["value"], 42.0)

    def test_older_direct_update_does_not_rewind_state(self):
        rt = self.runtime()
        view = rt.resolve_account_view(
            fetch_canonical=lambda _: self.seeded_snapshot(),
            required_keys=["drone.level"],
            session_observations=[{"key": "drone.level", "value": 150, "observed_at": OLD, "source": "direct"}])
        self.assertEqual(view["fields"]["drone.level"]["value"], 177)

    def test_same_time_contradiction_is_quarantined(self):
        rt = self.runtime()
        view = rt.resolve_account_view(
            fetch_canonical=lambda _: self.seeded_snapshot(),
            required_keys=["drone.level"],
            session_observations=[{"key": "drone.level", "value": 200, "observed_at": NEW, "source": "screenshot"}])
        self.assertEqual(view["fields"]["drone.level"]["status"], "CONFLICT")
        self.assertEqual(view["status"], "PARTIAL")

    def test_volatile_field_ages_without_rewriting_monotonic(self):
        rt = self.runtime()
        view = rt.resolve_account_view(
            fetch_canonical=lambda _: self.seeded_snapshot(),
            required_keys=["squad.primary_power", "drone.level"],
            now=NOW, max_volatile_age_hours=12)
        self.assertEqual(view["fields"]["squad.primary_power"]["status"], "STALE")
        self.assertEqual(view["fields"]["drone.level"]["status"], "VERIFIED_OBSERVED")

    def test_legacy_value_without_provenance_is_not_claimed_current(self):
        rt = self.runtime()
        view = rt.resolve_account_view(
            fetch_canonical=lambda _: {"account_id": "synthetic-A", "facts": {"drone.level": 155}},
            required_keys=["drone.level"])
        self.assertEqual(view["fields"]["drone.level"]["status"], "HISTORICAL_UNVERIFIED")

    def test_standalone_and_modular_contain_same_guardrail(self):
        module = (ROOT / "engine/modules/core/state-freshness.txt").read_text(encoding="utf-8")
        bootstrap = (ROOT / "engine/modules/release/bootstrap.txt").read_text(encoding="utf-8")
        standalone = (ROOT / "engine/BOOTSTRAP_FULL.txt").read_text(encoding="utf-8")
        for token in ("CANONICAL READ PREFLIGHT", "active_account_id", "NOT VERIFIED"):
            self.assertIn(token, module)
            self.assertIn(token, standalone)
        self.assertIn("CANONICAL READ PREFLIGHT", bootstrap)
        self.assertIn("Before any account-specific summary", standalone)


if __name__ == "__main__":
    unittest.main()
