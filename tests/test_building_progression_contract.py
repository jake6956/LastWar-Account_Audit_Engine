import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

class BuildingProgressionContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(read("engine/MANIFEST.json"))
        self.buildings = read("engine/modules/domains/building-progression.txt")
        self.full = read("engine/BOOTSTRAP_FULL.txt")

    def test_building_module_is_reachable(self):
        by_id = {m["module_id"]: m for m in self.manifest["modules"]}
        self.assertIn("domain.building-progression", by_id)
        mod = by_id["domain.building-progression"]
        self.assertFalse(mod["required"])
        for intent in ("building", "headquarters", "hq upgrade", "barracks", "wall", "tech center"):
            self.assertIn(intent, mod["activation"]["intents"])

    def test_prerequisite_value_beats_lowest_level_cleanup(self):
        lower = (self.buildings + "\n" + self.full).lower()
        self.assertIn("prerequisite", lower)
        self.assertIn("do not recommend equalizing buildings", lower)
        self.assertIn("do not consume weeks of builder time", lower)
        self.assertIn("immediate hq", lower)

    def test_building_levels_and_timers_use_different_freshness(self):
        combined = self.buildings + "\n" + self.full
        self.assertIn("MONOTONIC", combined)
        self.assertIn("VOLATILE", combined)
        self.assertIn("expected_completion", combined)

    def test_mixed_barracks_and_event_timing_are_guarded(self):
        lower = (self.buildings + "\n" + self.full).lower()
        self.assertIn("mixed barracks levels", lower)
        self.assertIn("day 2", lower)
        self.assertIn("day 5", lower)
        self.assertIn("do not idle builders", lower)

if __name__ == "__main__":
    unittest.main()
