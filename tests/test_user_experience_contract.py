import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
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
        self.storage_contract = read("contracts/storage-adapter.md")
        self.readme = read("README.md")
        self.latest = json.loads(read("releases/LATEST.json"))

    def test_stage1_loader_is_small_orchestration_only(self):
        self.assertLessEqual(len(self.loader.encode("utf-8")), 4096)
        self.assertIn("Stage-1 orchestration only", self.loader)
        self.assertIn("release.resolver", self.loader)
        self.assertIn("release.updater", self.loader)
        for forbidden in (
            "Before we build your account",
            "Google Drive",
            "Allow always",
            "screenname",
            "strategic baseline",
            "domain.season-intelligence",
            "GEAR / UPGRADE ORE",
        ):
            self.assertNotIn(forbidden, self.loader)

    def test_stage0_installer_uses_live_branch_ref(self):
        self.assertEqual(self.latest["preferred_install_url"], LIVE_REF)
        for body in (self.loader, self.full, self.bootstrap, self.readme):
            self.assertIn(LIVE_REF, body)
        self.assertIn("Stage-0 bootloader", self.readme)
        self.assertIn("current commit SHA", self.readme)

    def test_primary_installer_does_not_require_third_party_shortener(self):
        for label, body in (
            ("loader", self.loader),
            ("full", self.full),
            ("release.bootstrap", self.bootstrap),
        ):
            self.assertNotIn(LEGACY_SHORTENER, body, label)
        self.assertIn("Do not use the old TinyURL installer", self.readme)

    def test_legacy_repo_installer_handoff_executes_without_repaste(self):
        lower = self.readme.lower()
        self.assertIn("assistant handoff / legacy-installer compatibility", lower)
        self.assertIn("execute the stage-0 bootloader below now", lower)
        self.assertIn("do not", lower)
        self.assertIn("ask the user to copy/paste a second prompt", lower)
        self.assertIn(LIVE_REF, self.readme)
        self.assertIn("stop rather than guessing", lower)

    def test_first_run_cloud_question_lives_in_modules_not_loader(self):
        question = "would you like me to use private cloud storage"
        self.assertNotIn(question, self.loader.lower())
        for body in (self.full, self.guidance, self.persistence, self.contract):
            self.assertIn(question, body.lower())

    def test_cloud_yes_requires_explicit_provider_choice(self):
        combined = "\n".join((self.full, self.guidance, self.persistence, self.storage, self.bootstrap, self.contract)).lower()
        self.assertIn("provider", combined)
        self.assertTrue("never default to google drive" in combined or "never silently choose google drive" in combined)

    def test_google_drive_permission_coaching_includes_allow_always(self):
        for body in (self.full, self.guidance, self.storage, self.contract):
            self.assertIn("Allow always", body)
            self.assertIn("Google Drive", body)

    def test_workspace_boundary_is_absolute_and_user_visible(self):
        combined = "\n".join((self.full, self.storage, self.contract, self.storage_contract, self.readme))
        self.assertIn("ABSOLUTE WORKSPACE BOUNDARY", self.storage)
        self.assertIn("LWAI is explicitly restricted to its own Last War workspace", combined)
        self.assertIn("outside that workspace", combined)
        self.assertIn("other ChatGPT/app workspaces", combined)
        self.assertIn("broader connector", combined)
        self.assertIn("provider-wide", combined)
        self.assertIn("unrelated provider", combined)
        self.assertIn("Workspace-only guardrail is active", self.storage)

    def test_workspace_boundary_prohibits_unrelated_storage_actions(self):
        lower = "\n".join((self.storage, self.storage_contract, self.contract)).lower()
        for verb in ("read", "list", "search", "inspect", "modify", "move", "rename", "delete"):
            self.assertIn(verb, lower)
        self.assertIn("outside", lower)
        self.assertIn("off-limits", lower)
        self.assertIn("do not perform provider-wide", lower)

    def test_credentials_are_never_requested(self):
        combined = "\n".join((self.full, self.storage, self.contract, self.storage_contract)).lower()
        for token in ("password", "oauth", "token", "cookies", "credentials"):
            self.assertIn(token, combined)
        self.assertTrue("never asks" in combined or "never request" in combined)

    def test_connected_is_recheck_trigger_not_proof(self):
        for body in (self.full, self.guidance, self.persistence, self.storage, self.contract):
            lower = body.lower()
            self.assertIn("connected", lower)
            self.assertTrue("re-check" in lower or "recheck" in lower or "capabilit" in lower)
            self.assertIn("verif", lower)

    def test_storage_success_is_not_terminal(self):
        for label, body in (
            ("full", self.full),
            ("guidance", self.guidance),
            ("storage", self.storage),
            ("bootstrap", self.bootstrap),
            ("UX contract", self.contract),
        ):
            lower = body.lower()
            self.assertIn("cloud storage connected and verified", lower, label)
            self.assertTrue(
                "immediately" in lower
                or "same user-facing response" in lower
                or "same response" in lower
                or "not a conversational terminal state" in lower
                or "resumes original work" in lower,
                label,
            )

    def test_verified_storage_advances_to_identity(self):
        for body in (self.full, self.guidance, self.accounts, self.contract):
            lower = body.lower()
            self.assertIn("screenname", lower)
            self.assertIn("server", lower)
            self.assertIn("alliance", lower)
            self.assertIn("uid", lower)

    def test_identity_advances_to_baseline_and_evidence_without_next(self):
        for body in (self.full, self.guidance, self.accounts, self.contract):
            lower = body.lower()
            self.assertIn("hq", lower)
            self.assertIn("baseline", lower)
            self.assertTrue("first evidence" in lower or "first highest-value" in lower or "first useful evidence" in lower)
            self.assertIn("next", lower)

    def test_multi_upload_done_boundary_and_waiting_user_survive(self):
        for body in (self.full, self.guidance, self.contract):
            lower = body.lower()
            self.assertIn("waiting_user", lower)
            self.assertIn("done", lower)

    def test_existing_user_gets_landing_or_resume(self):
        for body in (self.full, self.guidance, self.accounts, self.contract):
            lower = body.lower()
            self.assertTrue("landing" in lower or "loaded" in lower)
            self.assertTrue("resume" in lower or "unfinished" in lower)

    def test_friendly_update_status_remains_intact(self):
        self.assertIn("FRIENDLY UPDATE UX", self.updater)
        self.assertIn("Checking for updates", self.updater)
        self.assertIn("LWAI updated successfully", self.updater)
        self.assertIn("audit yourself", self.updater)


if __name__ == "__main__":
    unittest.main()
