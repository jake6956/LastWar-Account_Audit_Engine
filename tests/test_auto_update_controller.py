import json
import unittest
from pathlib import Path

from update_controller import Candidate, EngineMetadata, run_update_transaction, should_auto_check

ROOT = Path(__file__).resolve().parents[1]


class AutomaticUpdateControllerTests(unittest.TestCase):
    def test_startup_reload_and_schema_sensitive_always_check_with_web(self):
        self.assertTrue(should_auto_check(web_available=True, startup=True, hours_since_last_success=0.1))
        self.assertTrue(should_auto_check(web_available=True, reload=True, hours_since_last_success=0.1))
        self.assertTrue(should_auto_check(web_available=True, schema_sensitive=True, hours_since_last_success=0.1))
        self.assertFalse(should_auto_check(web_available=False, startup=True, hours_since_last_success=None))

    def test_consequential_work_rechecks_at_six_hours_not_before(self):
        self.assertFalse(should_auto_check(web_available=True, consequential=True, hours_since_last_success=5.99))
        self.assertTrue(should_auto_check(web_available=True, consequential=True, hours_since_last_success=6.0))
        self.assertTrue(should_auto_check(web_available=True, consequential=True, hours_since_last_success=None))
        self.assertFalse(should_auto_check(web_available=True, consequential=False, hours_since_last_success=100))

    def test_force_refresh_bypasses_ttl(self):
        self.assertTrue(should_auto_check(web_available=True, force=True, hours_since_last_success=0.01))

    def test_newer_verified_production_updates_and_resumes_original_action(self):
        metadata = EngineMetadata("2026-08-29.17", "2026-08-29.17")
        result = run_update_transaction(
            metadata=metadata,
            candidate=Candidate("2026-08-29.18"),
            original_action="recommend next ore upgrade",
            now=100.0,
            check_required=True,
        )
        self.assertTrue(result.updated)
        self.assertEqual(result.active_version, "2026-08-29.18")
        self.assertEqual(result.resumed_action, "recommend next ore upgrade")
        self.assertEqual(metadata.installed_engine_version, "2026-08-29.18")
        self.assertEqual(metadata.last_known_good_engine_version, "2026-08-29.18")
        self.assertEqual(metadata.last_successful_engine_update, 100.0)

    def test_current_version_check_is_silent_noop(self):
        metadata = EngineMetadata("2026-08-29.18", "2026-08-29.18")
        result = run_update_transaction(
            metadata=metadata,
            candidate=Candidate("2026-08-29.18"),
            original_action="answer user",
            now=101.0,
            check_required=True,
        )
        self.assertTrue(result.checked)
        self.assertFalse(result.updated)
        self.assertFalse(result.degraded)
        self.assertEqual(result.resumed_action, "answer user")
        self.assertEqual(metadata.last_successful_update_check, 101.0)

    def test_rc_or_invalid_candidate_never_replaces_last_known_good(self):
        cases = [
            Candidate("2026-08-29.19", channel="RC"),
            Candidate("2026-08-29.19", sanitized=False),
            Candidate("2026-08-29.19", account_state_included=True),
            Candidate("2026-08-29.19", migration_chain_valid=False),
            Candidate("2026-08-29.19", integrity_valid=False),
            Candidate("2026-08-29.19", health_check_valid=False),
        ]
        for candidate in cases:
            with self.subTest(candidate=candidate):
                metadata = EngineMetadata("2026-08-29.18", "2026-08-29.18")
                result = run_update_transaction(
                    metadata=metadata,
                    candidate=candidate,
                    original_action="continue work",
                    now=102.0,
                    check_required=True,
                )
                self.assertFalse(result.updated)
                self.assertTrue(result.degraded)
                self.assertEqual(result.active_version, "2026-08-29.18")
                self.assertEqual(metadata.installed_engine_version, "2026-08-29.18")
                self.assertEqual(result.resumed_action, "continue work")

    def test_unavailable_update_source_preserves_engine(self):
        metadata = EngineMetadata("2026-08-29.18", "2026-08-29.18")
        result = run_update_transaction(
            metadata=metadata,
            candidate=None,
            original_action="continue safe task",
            now=103.0,
            check_required=True,
        )
        self.assertTrue(result.degraded)
        self.assertEqual(result.active_version, "2026-08-29.18")
        self.assertEqual(metadata.installed_engine_version, "2026-08-29.18")

    def test_release_updater_is_mandatory_and_bootstrap_depends_on_it(self):
        manifest = json.loads((ROOT / "engine/MANIFEST.json").read_text(encoding="utf-8"))
        by_id = {m["module_id"]: m for m in manifest["modules"]}
        self.assertIn("release.updater", by_id)
        self.assertTrue(by_id["release.updater"]["required"])
        self.assertEqual(by_id["release.updater"]["load_class"], "mandatory_core")
        self.assertIn("release.updater", by_id["release.bootstrap"]["dependencies"])

    def test_public_runtime_exposes_automatic_update_and_manual_break_glass(self):
        loader = (ROOT / "engine/BOOTSTRAP.txt").read_text(encoding="utf-8")
        full = (ROOT / "engine/BOOTSTRAP_FULL.txt").read_text(encoding="utf-8")
        updater = (ROOT / "engine/modules/release/updater.txt").read_text(encoding="utf-8")
        for body in (loader, full, updater):
            self.assertIn("AUTOMATIC", body.upper())
            self.assertIn("refresh engine", body)
        self.assertIn("resume the user's original", loader)
        self.assertIn("last_known_good_engine_version", updater)

    def test_single_installer_is_unchanged(self):
        loader = (ROOT / "engine/BOOTSTRAP.txt").read_text(encoding="utf-8")
        self.assertIn(
            "Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x",
            loader,
        )


if __name__ == "__main__":
    unittest.main()
