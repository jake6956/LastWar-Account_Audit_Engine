import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class PreferenceContractTests(unittest.TestCase):
    def setUp(self):
        self.module = read("engine/modules/core/preferences.txt")
        self.contract = read("contracts/preferences.md")
        self.fallback = read("engine/BOOTSTRAP_FULL.txt")
        self.manifest = json.loads(read("engine/MANIFEST.json"))
        self.schema = json.loads(read("schemas/preferences.schema.json"))
        self.latest = json.loads(read("releases/LATEST.json"))
        self.migrations = json.loads(read("releases/MIGRATIONS.json"))

    def test_preferences_module_is_mandatory(self):
        modules = {m["module_id"]: m for m in self.manifest["modules"]}
        pref = modules["core.preferences"]
        self.assertTrue(pref["required"])
        self.assertEqual(pref["load_class"], "mandatory_core")
        self.assertIn("core.preferences", modules["release.bootstrap"]["dependencies"])
        self.assertIn("WORKSPACE", self.module)
        self.assertIn("ACCOUNT", self.module)
        self.assertIn("SESSION", self.module)

    def test_explicit_preferences_beat_tentative_and_defaults(self):
        for body in (self.module, self.contract, self.fallback):
            self.assertRegex(body, r"(?i)current explicit")
            self.assertRegex(body, r"(?i)tentative")
            self.assertRegex(body, r"(?i)(LWAI default|defaults)")
        self.assertIn("User correction wins immediately", self.module)

    def test_account_preferences_are_isolated(self):
        for body in (self.module, self.contract, self.fallback):
            self.assertIn("account_id", body)
            self.assertRegex(body, r"(?i)account.*override.*workspace|workspace.*account")
        self.assertIn("account preferences never are", self.fallback.lower())
        self.assertIn("active account", self.contract.lower())

    def test_session_only_preferences_are_ephemeral(self):
        for body in (self.module, self.contract, self.fallback):
            self.assertRegex(body, r"(?i)session")
            self.assertRegex(body, r"(?i)ephemeral")
            self.assertRegex(body, r"(?i)(must not|without).*claim|false promise")

    def test_preferences_cannot_override_evidence_privacy_or_safety(self):
        for body in (self.module, self.contract, self.fallback):
            lower = body.lower()
            normalized = lower.replace("-", " ")
            for token in ("evidence", "privacy", "account isolation", "safety"):
                self.assertIn(token, normalized)
            self.assertRegex(lower, r"may not|never override|never:")

    def test_preference_user_controls_exist(self):
        combined = "\n".join((self.module, self.contract, self.fallback)).lower()
        for token in (
            "what preferences do you have saved",
            "remember that",
            "forget that preference",
            "reset my ux preferences",
            "reset preferences for this account",
            "export my preferences",
        ):
            self.assertIn(token, combined)

    def test_private_feedback_is_not_auto_published(self):
        for body in (self.module, self.contract, self.fallback):
            lower = body.lower()
            self.assertIn("feedback", lower)
            self.assertRegex(lower, r"never (automatically |auto-)?(publish|transmit)|never automatically published")
            self.assertIn("github", lower)

    def test_consequential_preferences_require_explicit_user_direction(self):
        for body in (self.module, self.contract, self.fallback):
            lower = body.lower()
            self.assertIn("spending", lower)
            self.assertIn("privacy", lower)
            self.assertRegex(lower, r"require explicit|must not be inferred|never infer")

    def test_preference_schema_has_self_correcting_metadata(self):
        pref = self.schema["$defs"]["preference"]
        required = set(pref["required"])
        for key in ("key", "scope", "category", "value", "source_type", "confidence", "status"):
            self.assertIn(key, required)
        props = pref["properties"]
        for key in ("first_seen", "last_seen", "last_confirmed", "notes"):
            self.assertIn(key, props)

    def test_preferences_release_edge_remains_preserved_in_current_release(self):
        self.assertEqual(self.latest["schema_version"], "2.3")
        self.assertFalse(self.latest["migration"]["requires_user_reonboarding"])
        self.assertFalse(self.latest["migration"]["requires_account_rewrite"])
        edge = next(
            e for e in self.migrations["edges"]
            if e["from"] == "2026-08-30.31" and e["to"] == "2026-08-31.32"
        )
        self.assertEqual(edge["schema_from"], "2.3")
        self.assertEqual(edge["schema_to"], "2.3")
        self.assertIn("core.preferences", {m["module_id"] for m in self.manifest["modules"]})

    def test_standalone_fallback_has_preferences_parity(self):
        self.assertIn(f"engine_version: {self.latest['engine_version']}", self.fallback)
        self.assertIn("PREFERENCES / PERSONALIZED UX", self.fallback)
        self.assertIn("Preferences.md", self.fallback)
        self.assertIn("WORKSPACE", self.fallback)
        self.assertIn("ACCOUNT", self.fallback)
        self.assertIn("SESSION", self.fallback)


if __name__ == "__main__":
    unittest.main()
