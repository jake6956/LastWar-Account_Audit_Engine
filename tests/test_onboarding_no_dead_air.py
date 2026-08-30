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

    def test_production_continuity_module_contains_required_hard_guards(self):
        body = (ROOT / "engine/modules/core/flow-continuity.txt").read_text(encoding="utf-8")
        for token in (
            "NO-DEAD-AIR INVARIANT",
            "STORAGE AUTHORIZATION RETURN",
            "DURABLE ONBOARDING STAGES",
            "INTERRUPTION / RELOAD HANDOFF",
            "EXISTING USER CONTINUITY",
            "FAILURE CONTINUITY",
            "IDENTITY_PENDING",
            "BASELINE_PENDING",
            "FIRST_EVIDENCE_PENDING",
            "WAITING_USER",
            "Never return only `recheck_storage_capabilities`",
        ):
            self.assertIn(token, body)


if __name__ == "__main__":
    unittest.main()
