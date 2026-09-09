import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

class GovernanceConsistencyTests(unittest.TestCase):
    def test_canonical_governance_contract_exists(self):
        c = read("contracts/recommendation-governance.md")
        for token in ["G-001 Goal-first","G-002 Proactive validation","G-003 Evidence sufficiency","G-004 Research before guess","G-005 Decision procedure","G-006 No false winner","G-008 Governance monotonicity","G-010 Output semantics"]:
            self.assertIn(token,c)

    def test_operating_surfaces_do_not_retain_legacy_uncertainty_escape_hatches(self):
        bodies = [read("contracts/operating-canon.md"), read("engine/modules/core/flow-continuity.txt"), read("engine/modules/domains/season-intelligence.txt")]
        forbidden = ["Uncertainty should reduce confidence, not halt useful reasoning", "give the best defensible recommendation", "best bounded recommendation using validated facts"]
        for body in bodies:
            for token in forbidden:
                self.assertNotIn(token, body)

    def test_goal_is_not_silently_overridden_by_generic_value(self):
        prefs = read("engine/modules/core/preferences.txt")
        self.assertIn("governing decision intent", prefs)
        self.assertIn("Never override the governing objective", prefs)
        flow = read("engine/modules/core/flow-continuity.txt")
        self.assertIn("ranked against the user’s explicit current/account objective", flow)

    def test_guidance_routes_every_recommendation_through_preflight(self):
        import json
        manifest = json.loads(read("engine/MANIFEST.json"))
        modules = {m["module_id"]: m for m in manifest["modules"]}
        self.assertTrue(modules["core.recommendation-governance"]["required"])
        self.assertIn("core.recommendation-governance", modules["release.bootstrap"]["dependencies"])
        self.assertIn("CANONICAL DECISION PIPELINE", read("engine/modules/core/recommendation-governance.txt"))

    def test_guidance_is_governed_by_mandatory_preflight_module(self):
        import json
        manifest = json.loads(read("engine/MANIFEST.json"))
        modules = {m["module_id"]: m for m in manifest["modules"]}
        self.assertTrue(modules["core.recommendation-governance"]["required"])
        self.assertIn("core.recommendation-governance", modules["release.bootstrap"]["dependencies"])
        gov = read("engine/modules/core/recommendation-governance.txt")
        self.assertIn("Before a consequential recommendation is emitted", gov)
        self.assertIn("The user is never required to ask `are you sure?`", gov)

    def test_full_fallback_has_governance_parity(self):
        full = read("engine/BOOTSTRAP_FULL.txt")
        for token in ["RECOMMENDATION GOVERNANCE / PROACTIVE PREFLIGHT", "governing explicit objective", "The user never has to ask `are you sure?`", "release-blocking defect", "Never recommend upgrading a piece already at or beyond the proposed breakpoint"]:
            self.assertIn(token, full)

    def test_user_challenge_is_not_required_for_validation(self):
        ux = read("contracts/user-experience.md")
        flow = read("engine/modules/core/flow-continuity.txt")
        self.assertIn("The user should not need to challenge the expert to trigger validation", ux)
        self.assertIn("validation must already have happened proactively before the first answer", flow)

    def test_governance_module_is_mandatory_and_cross_cutting(self):
        import json
        manifest = json.loads(read("engine/MANIFEST.json"))
        modules = {m["module_id"]: m for m in manifest["modules"]}
        gov = modules["core.recommendation-governance"]
        self.assertTrue(gov["required"])
        self.assertEqual(gov["load_class"], "mandatory_core")
        self.assertIn("core.recommendation-governance", modules["release.bootstrap"]["dependencies"])
        body = read("engine/modules/core/recommendation-governance.txt")
        for token in ["CANONICAL DECISION PIPELINE", "PROACTIVE CERTAINTY", "NO FALSE WINNER", "RESEARCH BEFORE GUESS", "GOVERNANCE MONOTONICITY", "OUTPUT SEMANTICS"]:
            self.assertIn(token, body)


if __name__ == "__main__":
    unittest.main()
