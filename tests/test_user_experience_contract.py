import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
PUBLIC_URL = "https://lastwarai.com"
LEGACY_URL = "https://tinyurl.com/2yxf7f5x"
FIRST_RUN_PROMPT = (
    "Would you like me to save your LWAI setup in your own cloud storage so I can pick up "
    "where we left off in future chats? Recommended, but optional. Reply yes or no."
)
COMPACT_REASSURANCE = (
    "LWAI will use only its dedicated Last War/LWAI workspace; everything else in your connected "
    "storage is off-limits. Connect through the provider/ChatGPT UI, and never paste passwords or login codes here."
)


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
        self.bootstrap_contract = read("contracts/bootstrap-resolution.md")
        self.quick_install = read("docs/quick-install.md")
        self.readme = read("README.md")
        self.latest = json.loads(read("releases/LATEST.json"))

    def test_stage1_loader_is_small_orchestration_only(self):
        self.assertLessEqual(len(self.loader.encode("utf-8")), 4096)
        self.assertIn("Stage-1 orchestration only", self.loader)
        self.assertIn("release.resolver", self.loader)
        self.assertIn("release.updater", self.loader)
        for forbidden in (
            "save your LWAI setup",
            "Google Drive",
            "Allow always",
            "screenname",
            "strategic baseline",
            "domain.season-intelligence",
            "GEAR / UPGRADE ORE",
        ):
            self.assertNotIn(forbidden, self.loader)

    def test_stage0_uses_first_party_entrypoint_then_live_ref(self):
        self.assertEqual(self.latest["preferred_install_url"], PUBLIC_URL)
        self.assertEqual(self.latest["live_ref_source"], LIVE_REF)
        self.assertFalse(self.latest["public_entrypoint_authority"])
        for body in (self.full, self.bootstrap, self.bootstrap_contract, self.quick_install, self.readme):
            self.assertIn(PUBLIC_URL, body)
        for body in (self.full, self.bootstrap, self.bootstrap_contract, self.readme):
            self.assertIn(LIVE_REF, body)
        self.assertIn(LIVE_REF, self.loader)
        self.assertIn("Stage 0 — https://lastwarai.com", self.bootstrap_contract)

    def test_primary_installer_is_first_party_not_third_party_shortener(self):
        self.assertEqual(
            self.latest["preferred_install_instruction"],
            f"Set up Last War optimization using the instructions at {PUBLIC_URL}",
        )
        self.assertIn(LEGACY_URL, self.latest.get("legacy_install_urls", []))
        self.assertNotIn(LEGACY_URL, self.loader)
        self.assertNotIn(LEGACY_URL, self.full)
        self.assertNotIn(LEGACY_URL, self.readme)
        for body in (self.bootstrap, self.bootstrap_contract, self.quick_install):
            lower = body.lower()
            self.assertIn("legacy", lower)
            self.assertIn("compatibility", lower)

    def test_legacy_repo_installer_handoff_executes_without_repaste(self):
        lower = self.bootstrap.lower()
        self.assertIn("legacy alias", lower)
        self.assertIn("already-circulated installer", lower)
        self.assertIn("compatibility-only", lower)
        contract_lower = self.bootstrap_contract.lower()
        self.assertIn("the user is not expected to retrieve github json", contract_lower)
        self.assertIn("paste another url", contract_lower)
        self.assertIn(LIVE_REF, self.bootstrap_contract)

    def test_first_run_cloud_question_is_compact_and_staged(self):
        self.assertNotIn(FIRST_RUN_PROMPT, self.loader)
        for body in (self.full, self.guidance, self.persistence, self.contract):
            self.assertIn(FIRST_RUN_PROMPT, body)
        for forbidden in ("OAuth", "cookies", "browse, read", "access/refresh tokens"):
            self.assertNotIn(forbidden, FIRST_RUN_PROMPT)
        self.assertIn("not a security briefing", self.persistence.lower())
        self.assertIn("not a security briefing", self.guidance.lower())

    def test_cloud_yes_requires_explicit_provider_choice(self):
        combined = "\n".join((self.full, self.guidance, self.persistence, self.storage, self.bootstrap, self.contract)).lower()
        self.assertIn("provider", combined)
        self.assertTrue("never default to google drive" in combined or "never silently choose google drive" in combined)

    def test_compact_reassurance_occurs_after_provider_selection(self):
        for body in (self.full, self.guidance, self.storage, self.contract, self.storage_contract):
            self.assertIn(COMPACT_REASSURANCE, body)
        for body in (self.guidance, self.persistence, self.storage, self.contract, self.storage_contract):
            lower = body.lower()
            self.assertRegex(lower, r"after .*provider|only after .*provider")

    def test_google_drive_permission_coaching_includes_allow_always(self):
        for body in (self.full, self.guidance, self.storage, self.contract):
            self.assertIn("Allow always", body)
            self.assertIn("Google Drive", body)

    def test_workspace_boundary_remains_absolute_internally(self):
        combined = "\n".join((self.full, self.storage, self.storage_contract))
        self.assertIn("ABSOLUTE WORKSPACE BOUNDARY", self.storage)
        self.assertIn("outside that workspace", combined)
        self.assertIn("other ChatGPT/app workspaces", combined)
        self.assertIn("broader connector", combined)
        self.assertIn("provider-wide", combined)
        self.assertIn("unrelated provider", combined)
        self.assertIn("Workspace-only guardrail is active", self.storage)

    def test_workspace_boundary_prohibits_unrelated_storage_actions(self):
        lower = "\n".join((self.storage, self.storage_contract)).lower()
        for verb in ("read", "list", "search", "inspect", "modify", "move", "rename", "delete"):
            self.assertIn(verb, lower)
        self.assertIn("outside", lower)
        self.assertIn("off-limits", lower)
        self.assertIn("do not perform provider-wide", lower)

    def test_credentials_are_never_requested_internally(self):
        combined = "\n".join((self.full, self.storage, self.contract, self.storage_contract)).lower()
        for token in ("password", "oauth", "token", "cookies", "credentials"):
            self.assertIn(token, combined)
        self.assertTrue("never asks" in combined or "never request" in combined or "never paste" in combined)

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
