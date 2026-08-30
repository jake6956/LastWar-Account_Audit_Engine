import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProductInvariantTests(unittest.TestCase):
    def test_public_release_is_sanitized_engine_only(self):
        latest = json.loads(text("releases/LATEST.json"))
        manifest = json.loads(text("engine/MANIFEST.json"))
        self.assertTrue(latest["sanitized"])
        self.assertFalse(latest["account_state_included"])
        self.assertTrue(manifest["sanitized"])
        self.assertFalse(manifest["account_state_included"])
        boundary = text("contracts/private-failsafe-mirror.md")
        self.assertIn("Public GitHub contains sanitized ENGINE only", boundary)
        self.assertIn("Maintainer private/Prod-Dev", boundary)
        self.assertIn("private LWAI Google Drive workspace", boundary)
        self.assertIn("Consumer/player data never uses the maintainer's Drive", boundary)

    def test_consumer_data_is_workspace_scoped_to_their_provider(self):
        storage = text("contracts/storage-adapter.md")
        flow = text("engine/modules/core/flow-continuity.txt")
        for required in (
            "only in that user's explicitly selected personal storage provider",
            "dedicated Last War / LWAI workspace",
            "never read, list, search, inspect, summarize, index, modify, move, rename, delete",
        ):
            self.assertIn(required, storage)
        self.assertIn("Consumer state is never routed through the maintainer's Drive, GitHub", flow)
        self.assertIn("Direct files/screenshots the user deliberately supplies in chat are task input only", flow)

    def test_google_drive_is_preferred_but_never_silent_selection(self):
        flow = text("engine/modules/core/flow-continuity.txt")
        ux = text("contracts/user-experience.md")
        matrix = text("adapters/provider-matrix.md")
        for body in (flow, ux, matrix):
            self.assertIn("Google Drive", body)
            self.assertRegex(body, r"(?i)(preferred|recommended)")
            self.assertRegex(body, r"(?i)(explicit|silently select|silent consent)")
        self.assertIn("Dropbox", flow)
        self.assertIn("OneDrive / Microsoft 365", flow)
        self.assertIn("Box when writable", flow)

    def test_friendly_expert_experience_accepts_challenges_and_topic_changes(self):
        flow = text("engine/modules/core/flow-continuity.txt")
        ux = text("contracts/user-experience.md")
        fallback = text("engine/BOOTSTRAP_FULL.txt")
        for body in (flow, ux, fallback):
            self.assertRegex(body, r"(?i)friendly expert Last War technician|friendly expert technician")
            self.assertRegex(body, r"(?i)challenge a recommendation")
            self.assertRegex(body, r"(?i)(different|unrelated|another) Last War question")
        self.assertIn("Do not force the user to complete onboarding before answering a legitimate Last War question", flow)

    def test_research_sources_are_inputs_not_gospel(self):
        flow = text("engine/modules/core/flow-continuity.txt")
        fallback = text("engine/BOOTSTRAP_FULL.txt")
        readme = text("README.md")
        for body in (flow, fallback, readme):
            self.assertIn("LastWarTutorial.com", body)
            self.assertIn("cpt-hedge.com", body)
            self.assertIn("r/LastWarMobileGame", body)
            self.assertRegex(body, r"(?i)official|in-game")
            self.assertRegex(body, r"(?i)high confidence")
        self.assertIn("These named community sources are research inputs, never automatic authority", flow)
        self.assertIn("independently check the claim against current official/in-game evidence", flow)

    def test_no_dead_air_contract_still_dominates_setup(self):
        flow = text("engine/modules/core/flow-continuity.txt")
        fallback = text("engine/BOOTSTRAP_FULL.txt")
        for body in (flow, fallback):
            self.assertIn("USER_ACTION", body)
            self.assertIn("WAITING_USER", body)
            self.assertIn("RUNNING", body)
            self.assertIn("connected", body)
            self.assertIn("same user-facing response", body.lower())
        self.assertNotIn("connected is sufficient proof", flow.lower())

    def test_manifest_loads_expert_continuity_module_mandatorily(self):
        manifest = json.loads(text("engine/MANIFEST.json"))
        modules = {m["module_id"]: m for m in manifest["modules"]}
        mod = modules["core.flow-continuity"]
        self.assertTrue(mod["required"])
        self.assertEqual(mod["module_version"], "2026-08-30.26.2")
        self.assertIn("expert_experience", mod["state_scope"])
        self.assertIn("research_source_policy", mod["state_scope"])
        self.assertIn("data_placement", mod["state_scope"])
        self.assertIn("core.flow-continuity", modules["release.bootstrap"]["dependencies"])


if __name__ == "__main__":
    unittest.main()
