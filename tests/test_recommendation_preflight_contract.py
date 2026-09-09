import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class RecommendationPreflightContractTests(unittest.TestCase):
    def test_core_requires_consequential_recommendation_preflight(self):
        core = read("engine/modules/core/operating.txt")
        for token in [
            "CONSEQUENTIAL RECOMMENDATION PREFLIGHT",
            "current direct user/in-game evidence -> verified current canonical active-account state",
            "affected recommendation is quarantined",
            "invalidate recommendations derived from the superseded value",
            "A user challenge to a consequential recommendation is itself a preflight trigger",
        ]:
            self.assertIn(token, core)

    def test_state_freshness_quarantines_direct_conflicts(self):
        state = read("engine/modules/core/state-freshness.txt")
        for token in [
            "RECOMMENDATION PREFLIGHT / CONFLICT QUARANTINE",
            "Current direct evidence outranks every older stored observation",
            "VOLATILE resource balances must be current enough for the proposed spend",
            "mark the affected recommendation invalid/pending reconciliation",
            "second request to confirm that answer",
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

    def test_full_fallback_has_preflight_parity(self):
        full = read("engine/BOOTSTRAP_FULL.txt")
        for token in [
            "CONSEQUENTIAL RECOMMENDATION PREFLIGHT",
            "RECOMMENDATION PREFLIGHT / CONFLICT QUARANTINE",
            "GEAR SPEND / ASSIGNMENT PREFLIGHT",
            "Never recommend upgrading a piece already at or beyond the proposed breakpoint",
        ]:
            self.assertIn(token, full)

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
