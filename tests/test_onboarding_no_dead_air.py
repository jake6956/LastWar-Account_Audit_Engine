import unittest
from pathlib import Path

from onboarding_flow import (
    INFRASTRUCTURE_ONLY_TERMINALS,
    resume_user_action,
    storage_authorization_return_steps,
    terminal_is_user_visible_action,
)
from reference_runtime import ProviderCapabilities

ROOT = Path(__file__).resolve().parents[1]


class OnboardingNoDeadAirTests(unittest.TestCase):
    def test_connected_success_rechecks_verifies_and_reaches_identity(self):
        caps = ProviderCapabilities(read=True, list=True, write=True, create=True)
        steps = storage_authorization_return_steps(caps)
        self.assertEqual(
            steps,
            [
                "recheck_storage_capabilities",
                "locate_or_create_private_workspace",
                "verify_private_workspace",
                "persist_identity_pending",
                "new_account_guidance",
            ],
        )
        self.assertTrue(terminal_is_user_visible_action(steps))

    def test_connected_failure_offers_choices_instead_of_dead_air(self):
        caps = ProviderCapabilities(read=True, list=True, write=False, create=False)
        steps = storage_authorization_return_steps(caps)
        self.assertEqual(
            steps,
            [
                "recheck_storage_capabilities",
                "storage_verification_failed_offer_retry_other_provider_or_session_only",
            ],
        )
        self.assertTrue(terminal_is_user_visible_action(steps))

    def test_existing_user_storage_return_lands_on_resume_or_question(self):
        caps = ProviderCapabilities(read=True, list=True, write=True, create=True)
        steps = storage_authorization_return_steps(caps, existing_user=True)
        self.assertEqual(steps[-1], "user_facing_loaded_account_resume_or_question")
        self.assertTrue(terminal_is_user_visible_action(steps))

    def test_later_persistence_upgrade_resumes_original_action(self):
        caps = ProviderCapabilities(read=True, list=True, write=True, create=True)
        steps = storage_authorization_return_steps(caps, later_persistence_upgrade=True)
        self.assertEqual(steps[-1], "resume_original_user_action")
        self.assertTrue(terminal_is_user_visible_action(steps))

    def test_every_durable_onboarding_phase_has_a_visible_resume_action(self):
        expected = {
            "PERSISTENCE_DECISION": "ask_cloud_yes_or_no",
            "PROVIDER_SELECTION": "ask_provider_choice",
            "AUTHORIZATION_WAIT": "finish_connection_then_reply_connected",
            "IDENTITY_PENDING": "ask_identity_block",
            "BASELINE_PENDING": "ask_strategic_baseline",
            "FIRST_EVIDENCE_PENDING": "request_first_account_evidence",
            "RUNNING": "resume_pending_objective_or_ask_what_to_work_on",
        }
        for stage, action in expected.items():
            self.assertEqual(resume_user_action(stage), action)

    def test_waiting_user_requires_and_preserves_exact_pending_instruction(self):
        self.assertEqual(
            resume_user_action("WAITING_USER", pending_user_input="reply done after the requested screenshots"),
            "reply done after the requested screenshots",
        )
        with self.assertRaises(ValueError):
            resume_user_action("WAITING_USER")

    def test_infrastructure_only_states_are_never_accepted_as_terminal(self):
        for terminal in INFRASTRUCTURE_ONLY_TERMINALS:
            self.assertFalse(terminal_is_user_visible_action([terminal]), terminal)

    def test_production_continuity_and_onboarding_modules_split_without_losing_guards(self):
        continuity = (ROOT / "engine/modules/core/flow-continuity.txt").read_text(encoding="utf-8")
        onboarding = (ROOT / "engine/modules/flows/onboarding.txt").read_text(encoding="utf-8")
        for token in (
            "NO-DEAD-AIR INVARIANT",
            "INTERRUPTION / RELOAD HANDOFF",
            "EXISTING USER CONTINUITY",
            "FAILURE CONTINUITY",
            "WAITING_USER",
        ):
            self.assertIn(token, continuity)
        for token in (
            "STORAGE AUTHORIZATION RETURN",
            "DURABLE ONBOARDING STAGES / RECOVERY",
            "IDENTITY_PENDING",
            "BASELINE_PENDING",
            "FIRST_EVIDENCE_PENDING",
            "WAITING_USER",
            "Never return only `recheck_storage_capabilities`",
        ):
            self.assertIn(token, onboarding)

    def test_verified_single_account_resumes_without_storage_creation(self):
        from onboarding_flow import installer_resume_route
        account = {"account_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "screenname": "ExampleCommander", "server": "1234", "uid_suffix": "4321", "game_uid": "0000000012344321", "database_pointer_verified": True, "status": "ACTIVE"}
        route, labels = installer_resume_route("verified", [account])
        self.assertEqual(route, "RESUME_SINGLE")
        self.assertIn("Server 1234", labels[0])
        self.assertIn("Account ID aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", labels[0])
        self.assertNotIn(account["game_uid"], labels[0])
        self.assertIn("••••4321", labels[0])

    def test_multiple_saved_accounts_require_selection(self):
        from onboarding_flow import installer_resume_route
        one = {"account_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "screenname": "ExampleOne", "server": "1001", "database_pointer_verified": True, "status": "ACTIVE"}
        two = {"account_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb", "screenname": "ExampleTwo", "server": "1002", "database_pointer_verified": True, "status": "ACTIVE"}
        route, labels = installer_resume_route("verified", [one, two])
        self.assertEqual(route, "SELECT_EXISTING")
        self.assertEqual(len(labels), 2)

    def test_invalid_registry_pointer_fails_closed(self):
        from onboarding_flow import installer_resume_route
        bad = {"account_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "screenname": "ExampleOne", "server": "1001", "database_pointer_verified": False, "status": "ACTIVE"}
        self.assertEqual(installer_resume_route("verified", [bad])[0], "RECOVERY_REQUIRED")

    def test_disconnected_known_storage_and_failed_reads_require_recovery(self):
        from onboarding_flow import installer_resume_route
        self.assertEqual(installer_resume_route("error")[0], "RECOVERY_REQUIRED")
        self.assertEqual(installer_resume_route("not_connected", prior_storage_indicated=True)[0], "RECONNECT_EXISTING_STORAGE")

    def test_original_fresh_user_entry_is_unchanged(self):
        from onboarding_flow import installer_resume_route
        self.assertEqual(installer_resume_route("not_connected")[0], "FIRST_RUN_PERSISTENCE")
        self.assertEqual(installer_resume_route("verified", [])[0], "FIRST_RUN_PERSISTENCE")

    def test_legacy_and_archived_accounts_do_not_reonboard(self):
        from onboarding_flow import installer_resume_route
        self.assertEqual(installer_resume_route("verified", [], legacy_state=True)[0], "RECOVER_LEGACY")
        archived = {"account_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "status": "ARCHIVED"}
        self.assertEqual(installer_resume_route("verified", [archived])[0], "RESTORE_ARCHIVED")

    def test_compiled_and_modular_resume_contracts_present(self):
        full = (ROOT / "engine/BOOTSTRAP_FULL.txt").read_text(encoding="utf-8")
        accounts = (ROOT / "engine/modules/core/accounts.txt").read_text(encoding="utf-8")
        onboarding = (ROOT / "engine/modules/flows/onboarding.txt").read_text(encoding="utf-8")
        bootstrap = (ROOT / "engine/modules/release/bootstrap.txt").read_text(encoding="utf-8")
        self.assertIn("EXISTING-STORAGE REINSTALL / RESUME GATE", full)
        self.assertIn("INSTALLER RE-RUN / VERIFIED ACCOUNT RESUME", accounts)
        self.assertIn("EXISTING-STORAGE RESUME GATE", onboarding)
        self.assertIn("INSTALLER RE-RUN ROUTING", bootstrap)
        for body in (full, accounts, onboarding, bootstrap):
            self.assertIn("server", body.lower())
            self.assertIn("Resume", body)


if __name__ == "__main__":
    unittest.main()
