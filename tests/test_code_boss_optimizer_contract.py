import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DamageBossOptimizerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = (ROOT / "engine/modules/domains/combat-meta-battlefield.txt").read_text(encoding="utf-8")
        cls.full = (ROOT / "engine/BOOTSTRAP_FULL.txt").read_text(encoding="utf-8")
        cls.manifest = json.loads((ROOT / "engine/MANIFEST.json").read_text(encoding="utf-8"))
        cls.entry = next(m for m in cls.manifest["modules"] if m["module_id"] == "domain.combat-meta-battlefield")
        cls.season_entry = next(m for m in cls.manifest["modules"] if m["module_id"] == "domain.season-intelligence")

    def test_damage_boss_intents_route_to_combat_module(self):
        intents = set(self.entry["activation"]["intents"])
        for intent in [
            "boss", "world boss", "wanted boss", "code boss", "code 39", "code 64", "code 87",
            "rampage boss", "crystal boss", "crystal event boss", "special boss", "season boss", "seasonal boss",
        ]:
            self.assertIn(intent, intents)

    def test_seasonal_boss_intents_also_activate_season_intelligence(self):
        intents = set(self.season_entry["activation"]["intents"])
        for intent in ["crystal boss", "crystal event boss", "season boss", "seasonal boss"]:
            self.assertIn(intent, intents)

    def test_combat_module_loads_account_state_dependencies(self):
        deps = set(self.entry["dependencies"])
        for dep in ["core.accounts", "core.state-freshness", "domain.gear-heroes-skills-ew", "domain.research-drone-progression"]:
            self.assertIn(dep, deps)

    def test_boss_variants_are_not_interchangeable(self):
        for token in [
            "PVE DAMAGE-BOSS OPTIMIZER", "Wanted/Code Boss", "Rampage Boss", "Crystal Boss",
            "not interchangeable with one another", "Never transfer a Code Boss lineup rule to Crystal/Rampage",
        ]:
            self.assertIn(token, self.module)

    def test_code_matching_bonus_is_not_a_generic_mono_type_mandate(self):
        for token in [
            "Code 39 -> Aircraft", "Code 64 -> Missile", "Code 87 -> Tank", "+50% damage",
            "not an automatic five-matching-hero mandate",
        ]:
            self.assertIn(token, self.module)
        self.assertIn("current in-game boss text/direct evidence", self.module.lower())

    def test_rampage_is_weakness_specific(self):
        for token in [
            "RAMPAGE BOSS VARIANT", "Tank damage", "Aircraft", "Missile", "three attacks per boss",
            "Optimize each boss separately",
        ]:
            self.assertIn(token, self.module)

    def test_crystal_has_its_own_bonus_model(self):
        for token in [
            "CRYSTAL / SPECIAL BOSS VARIANT", "normal troop-counter mechanics are ignored",
            "+30% Attack damage", "five heroes of the same troop type", "+20% allied damage",
            "Extra Bonus panel", "Drone-chip damage effects remain relevant", "best single hit",
            "Do not import the Wanted/Code 4+1",
        ]:
            self.assertIn(token, self.module)

    def test_recommendation_uses_actual_account_maturity(self):
        for token in [
            "level", "stars", "attack/stat lines", "skill levels", "Exclusive Weapon",
            "squad-slot tech", "Drone/chip", "Decorations/Profession/global bonuses", "shared transferable gear pool",
        ]:
            self.assertIn(token, self.module)
        self.assertIn("Displayed hero or squad power is context only", self.module)

    def test_boss_gear_is_reassigned_when_survival_is_not_binding(self):
        for token in [
            "Gear is a shared transferable pool", "offensive Guns and Data Chips",
            "If the special boss can actually kill, debuff or disable heroes",
            "restore ordinary presets afterward",
        ]:
            self.assertIn(token, self.module)

    def test_missing_material_state_causes_targeted_refresh_not_canned_roster(self):
        self.assertIn("request only that smallest field/screen", self.module)
        self.assertIn("Never fill an account-specific gap with a canned maxed-whale roster", self.module)

    def test_empirical_same_account_results_are_first_class_evidence(self):
        for token in [
            "Controlled same-account boss results are first-class evidence",
            "Comparable community anecdotes are valuable hypothesis generators",
            "repeatable controlled same-account results are the strongest lineup evidence",
            "Change one high-value variable at a time",
            "Avoid overfitting a single crit/proc-heavy outlier",
            "investigate the discrepancy rather than defending the theory",
        ]:
            self.assertIn(token, self.module)

    def test_boss_output_is_account_specific_and_testable(self):
        for token in [
            "exact current bonus/weakness/restriction", "recommended five heroes",
            "strongest alternative lineup worth testing", "one controlled next-attempt test",
            "current best hit and next target",
        ]:
            self.assertIn(token, self.module)

    def test_standalone_fallback_has_equivalent_damage_boss_behavior(self):
        for token in [
            "PVE DAMAGE-BOSS OPTIMIZER", "RAMPAGE BOSS VARIANT", "CRYSTAL / SPECIAL BOSS VARIANT",
            "Controlled same-account boss results are first-class evidence",
            "Never fill an account-specific gap with a canned maxed-whale roster",
            "repeatable controlled same-account results are the strongest lineup evidence",
        ]:
            self.assertIn(token, self.full)


if __name__ == "__main__":
    unittest.main()
