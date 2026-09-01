import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CodeBossOptimizerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = (ROOT / "engine/modules/domains/combat-meta-battlefield.txt").read_text(encoding="utf-8")
        cls.full = (ROOT / "engine/BOOTSTRAP_FULL.txt").read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "engine/MANIFEST.json").read_text(encoding="utf-8"))
        cls.entry = next(m for m in cls.manifest["modules"] if m["module_id"] == "domain.combat-meta-battlefield")

    def test_code_boss_intents_route_to_combat_module(self):
        intents = set(self.entry["activation"]["intents"])
        for intent in ["boss", "wanted boss", "code boss", "code 39", "code 64", "code 87"]:
            self.assertIn(intent, intents)

    def test_combat_module_loads_account_state_dependencies(self):
        deps = set(self.entry["dependencies"])
        for dep in ["core.accounts", "core.state-freshness", "domain.gear-heroes-skills-ew", "domain.research-drone-progression"]:
            self.assertIn(dep, deps)

    def test_matching_bonus_is_not_a_generic_mono_type_mandate(self):
        for token in [
            "Code 39 -> Aircraft", "Code 64 -> Missile", "Code 87 -> Tank", "+50% damage",
            "not an automatic five-matching-hero mandate", "plausible hybrid lineups", "current boss/default preset",
        ]:
            self.assertIn(token, self.module)
        self.assertIn("current in-game boss text/direct evidence", self.module.lower())

    def test_recommendation_uses_actual_account_maturity(self):
        for token in [
            "level", "stars", "attack/stat lines", "skill levels", "Exclusive Weapons",
            "squad-slot tech", "Drone/chips", "Decorations/Profession/global bonuses", "shared transferable gear pool",
        ]:
            self.assertIn(token, self.module)
        self.assertIn("Displayed power is context only", self.module)

    def test_boss_gear_is_reassigned_for_damage_not_pvp_survival(self):
        for token in [
            "Gear is a shared transferable pool", "offensive Guns and Data Chips",
            "Armor/Radar/frontline-tanking value is normally irrelevant", "Do not preserve a PvP tank-frontline gear layout",
        ]:
            self.assertIn(token, self.module)

    def test_missing_material_state_causes_targeted_refresh_not_canned_roster(self):
        self.assertIn("request only that smallest field/screen", self.module)
        self.assertIn("Never fill an account-specific gap with a canned maxed-whale roster", self.module)

    def test_user_results_outrank_generic_lineup_charts(self):
        self.assertIn("The user's repeatable measured boss damage outranks generic tier lists and static lineup charts", self.module)
        self.assertIn("one controlled next-attempt test", self.module)

    def test_standalone_fallback_has_equivalent_code_boss_behavior(self):
        for token in [
            "WANTED / CODE BOSS OPTIMIZER", "not an automatic five-matching-hero mandate",
            "offensive Guns and Data Chips", "Never fill an account-specific gap with a canned maxed-whale roster",
            "repeatable measured boss damage outranks generic tier lists/static lineup charts",
        ]:
            self.assertIn(token, self.full)


if __name__ == "__main__":
    unittest.main()
