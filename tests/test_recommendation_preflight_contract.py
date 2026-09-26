import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


class RecommendationPreflightContractTests(unittest.TestCase):
    def test_confirmed_defects_are_auto_captured_without_second_user_instruction(self):
        governance = read("engine/modules/core/recommendation-governance.txt")
        operating = read("engine/modules/core/operating.txt")
        for token in [
            "AUTO DEFECT CAPTURE",
            "without waiting for another instruction",
            "Account-specific corrections belong in LOCAL account state/Corrections",
            "Reusable/generalizable failures belong in the public engine",
        ]:
            self.assertIn(token, governance)
        for token in [
            "A confirmed LWAI miss automatically enters defect-capture handling",
            "Do not wait for the user to separately request documentation or a code fix",
            "If the defect is reusable across users",
        ]:
            self.assertIn(token, operating)

    def test_tech_tree_terminal_topology_is_direct_evidence(self):
        research = read("engine/modules/domains/research-drone-progression.txt")
        for token in [
            "TECH-TREE TOPOLOGY EVIDENCE",
            "visible connector lines",
            "no outgoing connector",
            "terminal/bottom boundary",
            "Never invent downstream unlocks beyond a visibly terminal node",
            "cropped or structural continuation is ambiguous",
        ]:
            self.assertIn(token, research)

    def test_standalone_fallback_has_auto_defect_and_topology_parity(self):
        full = read("engine/BOOTSTRAP_FULL.txt")
        for token in [
            "AUTO DEFECT CAPTURE",
            "without waiting for another instruction",
            "TECH-TREE TOPOLOGY EVIDENCE",
            "Never invent downstream unlocks beyond a visibly terminal node",
        ]:
            self.assertIn(token, full)

    def test_core_requires_proactive_consequential_recommendation_preflight(self):
        core = read("engine/modules/core/operating.txt")
        for token in [
            "CONSEQUENTIAL RECOMMENDATION PREFLIGHT",
            "Preflight is proactive",
            "The user must never be required to challenge the expert to trigger validation",
            "current direct user/in-game evidence -> verified current canonical active-account state",
            "quarantine the affected recommendation",
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
        self.assertIn("The user must never be required to challenge the expert to trigger validation", core)

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

    def test_irreversible_transaction_requires_exact_next_step_evidence(self):
        governance = read("engine/modules/core/recommendation-governance.txt")
        for token in [
            "IRREVERSIBLE TRANSACTION-EVIDENCE GATE",
            "summary-state evidence is not automatically sufficient to authorize the next click",
            "actual executable transaction",
            "exact next-step resource requirements",
            "opening choice chests",
            "smallest resolving transaction/confirmation screen",
            "planning rather than permission to execute an unverified step",
        ]:
            self.assertIn(token, governance)

    def test_gear_summary_icon_cannot_authorize_hidden_promotion_step(self):
        gear = read("engine/modules/domains/gear-heroes-skills-ew.txt")
        for token in [
            "GEAR TRANSACTION-STEP EVIDENCE GATE",
            "do not prove the internal promotion segment or exact next-step cost",
            "current Promote/Upgrade screen",
            "current promotion sub-stage/segment",
            "exact Upgrade Ore cost",
            "regular blueprint requirement",
            "Mythic blueprint requirement",
            "Do not infer that a visible 4-star item is one click from Mythic",
            "exact current-step shortfall and chest/conversion value are verified",
        ]:
            self.assertIn(token, gear)

    def test_standalone_fallback_has_transaction_evidence_parity(self):
        full = read("engine/BOOTSTRAP_FULL.txt")
        for token in [
            "IRREVERSIBLE TRANSACTION-EVIDENCE GATE",
            "GEAR TRANSACTION-STEP EVIDENCE GATE",
            "current Promote/Upgrade screen",
            "Do not infer that a visible 4-star item is one click from Mythic",
        ]:
            self.assertIn(token, full)

    def test_gear_spend_preflight_reconciles_current_preset_and_shared_pool(self):
        gear = read("engine/modules/domains/gear-heroes-skills-ew.txt")
        for token in [
            "PRESET / SHARED-POOL RECONCILIATION",
            "current preset or presets relevant to the user's objective",
            "Never merge distinct preset assignments into one fictional permanently hero-owned loadout",
            "same transferable piece",
            "smallest resolving evidence",
        ]:
            self.assertIn(token, gear)

    def test_transferable_piece_identity_is_distinct_from_current_holder_and_preset_use(self):
        gear = read("engine/modules/domains/gear-heroes-skills-ew.txt")
        for token in [
            "PHYSICAL PIECE IDENTITY / HOLDER ATTRIBUTION",
            "A transferable gear piece, its current holder, its use in a preset, and a proposed reassignment are four separate concepts",
            "Verified canonical current-holder data outranks inferred ownership from preset context",
            "Do not relabel the same physical piece as another hero's gear merely because a specialist preset uses it",
            "state that move as a separate future action",
            "do not imply the reassignment already exists",
            "Preset observations never redefine physical-piece ownership by themselves",
        ]:
            self.assertIn(token, gear)

    def test_current_holder_conflict_prefers_newer_verified_holder_without_erasing_preset_history(self):
        gear = read("engine/modules/domains/gear-heroes-skills-ew.txt")
        self.assertIn("newer verified holder evidence controls current attribution", gear)
        self.assertIn("older preset observation remains historical preset context", gear)
        self.assertIn("physical-piece identity, current holder, or current preset state is ambiguous", gear)

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
