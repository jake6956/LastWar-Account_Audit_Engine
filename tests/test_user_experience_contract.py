import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class UserExperienceContractTests(unittest.TestCase):
    def setUp(self):
        self.loader = read("engine/BOOTSTRAP.txt")
        self.full = read("engine/BOOTSTRAP_FULL.txt")
        self.guidance = read("engine/modules/core/guidance.txt")
        self.persistence = read("engine/modules/core/persistence.txt")
        self.storage = read("engine/modules/adapters/storage.txt")
        self.bootstrap = read("engine/modules/release/bootstrap.txt")
        self.updater = read("engine/modules/release/updater.txt")
        self.contract = read("contracts/user-experience.md")

    def test_thin_loader_remains_bounded(self):
        self.assertLessEqual(len(self.loader.encode("utf-8")), 9000)

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
            self.assertTrue("not proof" in lower or "is not proof" in lower or "confirmation is not proof" in lower)

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


if __name__ == "__main__":
    unittest.main()
