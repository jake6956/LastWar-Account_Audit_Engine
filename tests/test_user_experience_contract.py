import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_INSTALLER = "https://github.com/jake6956/LastWar-Account_Audit_Engine"
LEGACY_SHORTENER = "https://tinyurl.com/"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class UserExperienceContractTests(unittest.TestCase):
    def setUp(self):
        self.loader = read("engine/BOOTSTRAP.txt")
        self.full = read("engine/BOOTSTRAP_FULL.txt")
        self.guidance = read("engine/modules/core/guidance.txt")
        self.accounts = read("engine/modules/core/accounts.txt")
        self.persistence = read("engine/modules/core/persistence.txt")
        self.storage = read("engine/modules/adapters/storage.txt")
        self.bootstrap = read("engine/modules/release/bootstrap.txt")
        self.updater = read("engine/modules/release/updater.txt")
        self.contract = read("contracts/user-experience.md")
        self.readme = read("README.md")
        self.latest = json.loads(read("releases/LATEST.json"))

    def test_thin_loader_remains_bounded(self):
        self.assertLessEqual(len(self.loader.encode("utf-8")), 9000)

    def test_canonical_installer_uses_github_repository(self):
        self.assertEqual(self.latest["preferred_install_url"], CANONICAL_INSTALLER)
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("release.bootstrap", self.bootstrap),
            ("README", self.readme),
        ):
            self.assertIn(CANONICAL_INSTALLER, body, label)
        self.assertIn("ChatGPT installer handoff", self.readme)
        self.assertIn("engine/BOOTSTRAP.txt", self.readme)

    def test_primary_installer_does_not_require_third_party_shortener(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("release.bootstrap", self.bootstrap),
            ("README", self.readme),
        ):
            self.assertNotIn(LEGACY_SHORTENER, body, label)
        self.assertIn("Third-party URL shorteners", self.bootstrap)
        self.assertIn("never required trust roots", self.loader)

    def test_existing_onboarding_and_updater_contracts_remain_intact(self):
        self.assertIn("release.updater", self.loader)
        self.assertIn("refresh engine", self.loader)
        self.assertIn("LOCAL STATE", self.loader)
        self.assertIn("POST-STORAGE HANDOFF", self.loader)
        self.assertIn("Cloud storage connected and verified", self.loader)
        self.assertIn("screenname", self.loader.lower())
        self.assertIn("strategic baseline", self.loader.lower())
        self.assertIn("first highest-value evidence", self.loader.lower())

    def test_first_run_starts_with_plain_language_cloud_question(self):
        question = "would you like me to use private cloud storage"
        for body in (self.loader, self.full, self.guidance, self.persistence, self.bootstrap, self.contract):
            self.assertIn(question, body.lower())

    def test_cloud_yes_requires_explicit_provider_choice(self):
        for body in (self.loader, self.full, self.guidance, self.persistence, self.storage, self.bootstrap, self.contract):
            lower = body.lower()
            self.assertIn("provider", lower)
            self.assertTrue("explicit" in lower or "choose" in lower)
        combined = "\n".join((self.loader, self.full, self.guidance, self.persistence, self.storage, self.bootstrap, self.contract)).lower()
        self.assertIn("never default to google drive", combined)

    def test_google_drive_permission_coaching_includes_allow_always(self):
        for body in (self.loader, self.full, self.guidance, self.storage, self.bootstrap, self.contract):
            self.assertIn("Allow always", body)
            self.assertIn("Google Drive", body)

    def test_other_provider_guidance_is_present_without_fake_credentials(self):
        for provider in ("Dropbox", "OneDrive", "Box"):
            self.assertIn(provider, self.storage)
            self.assertIn(provider, self.full)
        lower = self.storage.lower()
        self.assertIn("do not invent", lower)
        self.assertIn("never ask", lower)
        self.assertIn("oauth", lower)

    def test_connected_is_recheck_trigger_not_proof(self):
        for body in (self.loader, self.full, self.guidance, self.persistence, self.storage, self.contract):
            lower = body.lower()
            self.assertIn("connected", lower)
            self.assertTrue(
                "re-detect" in lower or "recheck" in lower or "re-check" in lower or "capabilit" in lower,
                "storage connection acknowledgement must trigger capability verification",
            )
            self.assertTrue("verify" in lower or "verified" in lower)

    def test_later_persistence_acceptance_reruns_provider_flow(self):
        for body in (self.loader, self.full, self.guidance, self.persistence, self.bootstrap, self.contract):
            lower = body.lower()
            self.assertIn("provider", lower)
            self.assertTrue("rerun" in lower or "same provider chooser" in lower or "same chooser" in lower)

    def test_normal_bootstrap_ux_is_friendly_not_diagnostic_dump(self):
        for body in (self.loader, self.full, self.guidance, self.bootstrap, self.contract):
            self.assertIn("Getting LWAI ready", body)
            lower = body.lower()
            self.assertTrue("audit yourself" in lower or "debug" in lower)
        self.assertIn("FRIENDLY UPDATE UX", self.updater)
        self.assertIn("Checking for updates", self.updater)
        self.assertIn("LWAI updated successfully", self.updater)
        self.assertTrue("audit yourself" in self.updater.lower() or "debug" in self.updater.lower())

    def test_storage_success_requires_verification(self):
        self.assertIn("CONNECTION VERIFICATION", self.storage)
        self.assertIn("Cloud storage connected and verified", self.storage)
        self.assertIn("read", self.storage.lower())
        self.assertIn("write", self.storage.lower())
        self.assertIn("create", self.storage.lower())

    def test_storage_success_is_not_terminal(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("guidance", self.guidance),
            ("storage", self.storage),
            ("bootstrap", self.bootstrap),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertIn("cloud storage connected and verified", lower, label)
            self.assertTrue(
                "same response" in lower
                or "same user-facing response" in lower
                or "immediately continue" in lower
                or "immediately hand off" in lower
                or "return control immediately" in lower
                or "not a conversational" in lower,
                f"{label} does not explicitly prevent an orphan storage-success state",
            )

    def test_verified_storage_advances_to_identity(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("guidance", self.guidance),
            ("accounts", self.accounts),
            ("bootstrap", self.bootstrap),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertIn("screenname", lower, label)
            self.assertIn("server", lower, label)
            self.assertIn("alliance", lower, label)
            self.assertIn("uid", lower, label)
            self.assertTrue("optional" in lower and "identity" in lower, label)

    def test_identity_advances_to_strategic_baseline_without_next(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("guidance", self.guidance),
            ("accounts", self.accounts),
            ("bootstrap", self.bootstrap),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertIn("hq", lower, label)
            self.assertTrue("strategic baseline" in lower or "baseline" in lower, label)
            self.assertTrue("do not require" in lower or "never require" in lower or "without requiring" in lower, label)
            self.assertIn("next", lower, label)

    def test_baseline_advances_to_first_evidence_capture(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("guidance", self.guidance),
            ("accounts", self.accounts),
            ("bootstrap", self.bootstrap),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertTrue("first evidence" in lower or "first highest-value" in lower or "first useful evidence" in lower, label)
            self.assertTrue("main/default squad" in lower or "default squad" in lower or "main squad" in lower, label)

    def test_setup_turns_have_no_orphan_state(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("guidance", self.guidance),
            ("bootstrap", self.bootstrap),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertTrue(
                "orphan" in lower or "dead end" in lower or "terminal" in lower or "continuation invariant" in lower,
                label,
            )
            self.assertTrue("next actionable" in lower or "next action" in lower or "next useful" in lower, label)
            self.assertIn("waiting_user", lower, label)

    def test_onboarding_recovery_resumes_first_incomplete_stage(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("guidance", self.guidance),
            ("accounts", self.accounts),
            ("bootstrap", self.bootstrap),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertIn("first incomplete", lower, label)
            self.assertTrue(
                "never repeat" in lower or "does not repeat" in lower or "never restart" in lower or "never replay" in lower,
                label,
            )

    def test_existing_user_gets_landing_or_resume(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("guidance", self.guidance),
            ("accounts", self.accounts),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertTrue("landing" in lower or "loaded" in lower, label)
            self.assertTrue("resume" in lower or "unfinished" in lower, label)


if __name__ == "__main__":
    unittest.main()
