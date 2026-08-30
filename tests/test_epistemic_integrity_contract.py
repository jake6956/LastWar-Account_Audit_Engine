import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class EpistemicIntegrityContractTests(unittest.TestCase):
    def test_global_core_prohibits_fabricated_material_claims(self):
        core = read("engine/modules/core/operating.txt")
        self.assertIn("GLOBAL EPISTEMIC INTEGRITY CONTRACT", core)
        self.assertIn("No mechanic, number, cost, probability", core)
        self.assertIn("Absence of evidence is never permission to invent", core)
        self.assertIn("CALCULATION PROVENANCE", core)
        self.assertIn("RECOMMENDATION PROVENANCE", core)

    def test_source_quality_rejects_weak_stale_community_material(self):
        core = read("engine/modules/core/operating.txt")
        for token in [
            "SOURCE QUALITY / COMMUNITY VALIDATION",
            "independent corroboration",
            "reproducible screenshots/tests",
            "stale guides",
            "low-quality reposts",
            "obviously outdated material",
        ]:
            self.assertIn(token, core)

    def test_uncertain_fact_must_exhaust_sources_then_disclose(self):
        core = read("engine/modules/core/operating.txt")
        self.assertIn("VALIDATION DUTY", core)
        self.assertIn("exhaust reasonably available relevant sources", core)
        self.assertIn("UNVALIDATED-FACT HANDLING", core)
        self.assertIn("say that it could not be validated", core)
        self.assertIn("clearly labeled calculation/inference/heuristic", core)
        self.assertIn("LWAI's own analysis", core)

    def test_official_mechanics_are_separated_from_lwai_strategy(self):
        core = read("engine/modules/core/operating.txt")
        self.assertIn("Official Last War mechanics describe what the game does", core)
        self.assertIn("optimization recommendations are usually LWAI analysis", core)
        self.assertIn("Do not imply that an optimization path", core)

    def test_season_intelligence_inherits_and_strengthens_contract(self):
        season = read("engine/modules/domains/season-intelligence.txt")
        for token in [
            "COMMUNITY SOURCE QUALITY",
            "EXHAUST-THEN-DISCLOSE RULE",
            "single stale guide",
            "independent corroboration",
            "cannot be validated",
            "not an official Last War recommendation",
        ]:
            self.assertIn(token, season)

    def test_standalone_fallback_has_global_integrity_parity(self):
        full = read("engine/BOOTSTRAP_FULL.txt")
        for token in [
            "GLOBAL EPISTEMIC INTEGRITY CONTRACT",
            "SOURCE QUALITY / COMMUNITY VALIDATION",
            "VALIDATION DUTY",
            "UNVALIDATED-FACT HANDLING",
            "CALCULATION / RECOMMENDATION PROVENANCE",
            "exhaust reasonably available official and reputable current community sources",
        ]:
            self.assertIn(token, full)


if __name__ == "__main__":
    unittest.main()
