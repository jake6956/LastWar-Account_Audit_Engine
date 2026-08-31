import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

class VsTimingContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(read("engine/MANIFEST.json"))
        self.events = read("engine/modules/domains/events-vs-arms-race.txt")
        self.gear = read("engine/modules/domains/gear-heroes-skills-ew.txt")
        self.full = read("engine/BOOTSTRAP_FULL.txt")

    def test_vs_timing_module_is_registered_and_reachable(self):
        by_id = {m["module_id"]: m for m in self.manifest["modules"]}
        self.assertIn("domain.events-vs-arms-race", by_id)
        event = by_id["domain.events-vs-arms-race"]
        self.assertFalse(event["required"])
        self.assertEqual(event["load_class"], "domain_on_demand")
        for intent in ("alliance duel", "hero day", "arms race", "skill medals", "upgrade ore"):
            self.assertIn(intent, event["activation"]["intents"])
        self.assertIn("domain.events-vs-arms-race", by_id["domain.gear-heroes-skills-ew"]["dependencies"])

    def test_current_2026_vp_pattern_and_stale_guide_guard(self):
        for token in (
            "Day 1 Monday — Radar Training — 1 VP",
            "Day 2 Tuesday — Base Expansion / City Building — 1 VP",
            "Day 3 Wednesday — Age of Science / Tech Research — 1 VP",
            "Day 4 Thursday — Train Heroes / Hero Training — 2 VP",
            "Day 5 Friday — Total Mobilization — 3 VP",
            "Day 6 Saturday — Enemy Buster — 4 VP",
            "1/2/2/2/2/4",
            "1/1/1/2/3/4",
        ):
            self.assertIn(token, self.events)
        self.assertIn("current in-game event panels", self.events)
        self.assertIn("not an immutable game constant", self.events)

    def test_hero_resources_default_to_day4(self):
        combined = self.events + "\n" + self.gear + "\n" + self.full
        for resource in ("Skill Medals", "Hero Shards", "Hero EXP"):
            self.assertIn(resource, combined)
        self.assertIn("default Day 4", self.events)
        self.assertIn("VS Day 4", self.gear)
        self.assertIn("Day 4 / Train Heroes", self.full)

    def test_upgrade_ore_is_not_held_for_current_vs_or_arms_race(self):
        lower = (self.events + "\n" + self.gear + "\n" + self.full).lower()
        self.assertIn("upgrade ore", lower)
        self.assertIn("do not hold ore", lower)
        self.assertIn("vs or arms race", lower)
        self.assertIn("reverify", lower)

    def test_exact_points_require_current_account_evidence(self):
        lower = self.events.lower()
        self.assertIn("never promise a universal point total", lower)
        self.assertIn("alliance duel research", lower)
        self.assertIn("current user screenshot", lower)
        self.assertIn("label assumptions", lower)

    def test_event_timing_is_not_more_important_than_account_value(self):
        combined = (self.events + "\n" + self.full).lower()
        self.assertIn("event timing is an optimization layer", combined)
        self.assertIn("urgency override", combined)
        self.assertIn("do not optimize a player's account solely for weekly vs score", combined)

    def test_arms_race_requires_live_phase_check(self):
        lower = self.events.lower()
        self.assertIn("arms race double-dip", lower)
        self.assertIn("current arms race phase", lower)
        self.assertIn("do not assume one universal arms race phase schedule", lower)

if __name__ == "__main__":
    unittest.main()
