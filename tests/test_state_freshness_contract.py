import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

class StateFreshnessContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(read("engine/MANIFEST.json"))
        self.fresh = read("engine/modules/core/state-freshness.txt")
        self.research = read("engine/modules/domains/research-drone-progression.txt")
        self.full = read("engine/BOOTSTRAP_FULL.txt")

    def test_freshness_module_is_mandatory(self):
        by_id = {m["module_id"]: m for m in self.manifest["modules"]}
        self.assertIn("core.state-freshness", by_id)
        self.assertTrue(by_id["core.state-freshness"]["required"])
        self.assertEqual(by_id["core.state-freshness"]["load_class"], "mandatory_core")

    def test_state_classes_are_distinct(self):
        for token in ("INVARIANT / CORRECTION", "MONOTONIC", "VOLATILE"):
            self.assertIn(token, self.fresh)
        self.assertIn("minimum-known state", self.fresh)

    def test_queue_identity_and_timer_are_separate(self):
        combined = self.fresh + "\n" + self.research + "\n" + self.full
        self.assertIn("queue_identity", combined)
        self.assertIn("remaining_at_observation", combined)
        self.assertIn("timer_freshness", combined)
        self.assertIn("separate", combined.lower())

    def test_no_redundant_refresh_and_no_fake_eta(self):
        lower = (self.fresh + "\n" + self.research + "\n" + self.full).lower()
        self.assertIn("do not ask for a new screenshot merely because time passed", lower)
        self.assertIn("smallest useful refresh", lower)
        self.assertIn("never invent an exact timestamp or eta", lower)
        self.assertIn("do not manufacture a new countdown", lower)

if __name__ == "__main__":
    unittest.main()
