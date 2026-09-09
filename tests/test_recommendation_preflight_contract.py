import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class RecommendationPreflightContractTests(unittest.TestCase):
    def test_core_requires_proactive_consequential_recommendation_preflight(self):
        core = read("engine/modules/core/operating.txt")
        for token in [
            "CONSEQUENTIAL RECOMMENDATION PREFLIGHT",
            "Preflight is proactive",
            "The user must never be required to challenge the expert to trigger validation",
            "current direct user/in-game evidence -> verified current canonical active-account state",
            "affected recommendation is quarantined",
            "invalidate recommendations derived from the superseded value",
            "The prior answer is never evidence for itself",
        ]:
            self.assertIn(token, core)

    def test_goal_first_contract_controls_every_recommendation(self):
        core = read("engine/modules/core/operating.txt")
        for token in [
            "GOAL-FIRST OPTIMIZATION CONTRACT",
            "Every recommendation MUST be ranked against the user's stated goal(s)",
            "Never silently replace the user's objective",
            "ask the smallest goal/priority question required before ranking",
            "present that bounded selection",
            "best-supported action for this account, at this time, for the user's stated objective",
        ]:
            self.assertIn(token, core)

    def test_material_unknown_blocks_false_single_winner(self):
        core = read("engine/modules/core/operating.txt")
        self.assertIn("If yes, ask for the smallest current user evidence capable of resolving it before naming a definitive winner", core)
        self.assertIn("Never use a low-confidence single recommendation where a material unknown could reasonably reverse it", core)
        self.assertIn("Do not make the user perform quality assurance on the expert", core)

    def test_state_freshness_is_proactive_and_goal_relative(self):
        state = read("engine/modules/core/state-freshness.txt")
        for token in [
            "Recommendation preflight is mandatory before the recommendation is emitted",
            "proactively rather than waiting for the user to challenge the answer",
            "A user should not need to ask `are you sure?` to activate validation",
            "GOAL RELEVANCE",
            "Do not silently optimize for displayed power, generic progression, event score, PvP, PvE",
        ]:
            self.assertIn(token, state)

    def test_gear_spend_preflight_blocks_stale_breakpoint_advice(self):
        gear = read("engine/modules/domains/gear-heroes-skills-ew.txt")
        for token in [
            "GEAR SPEND / ASSIGNMENT PREFLIGHT",
            "current spendable resource balance",
            "Current readable screenshots/direct user observations outrank persisted or remembered gear values",
            "Never recommend upgrading a piece already at or beyond the proposed breakpoint",
            "prior recommendation itself as evidence",
            "Upgrade Ore and other spendable balances are VOLATILE",
        ]:
            self.assertIn(token, gear)

    def test_private_state_does_not_leak_into_contract(self):
        public = "\n".join([
            read("engine/modules/core/operating.txt"),
            read("engine/modules/core/state-freshness.txt"),
            read("engine/modules/domains/gear-heroes-skills-ew.txt"),
            read("engine/BOOTSTRAP_FULL.txt"),
        ])
        for forbidden in ["134.1k", "Stetmann Armor", "Kimberly Armor", "CP-20260909-GEAR01"]:
            self.assertNotIn(forbidden, public)


if __name__ == "__main__":
    unittest.main()
