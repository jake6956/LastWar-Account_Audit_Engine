import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

class EventStoreValueContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(read("engine/MANIFEST.json"))
        self.stores = read("engine/modules/domains/season-stores-paid.txt")
        self.full = read("engine/BOOTSTRAP_FULL.txt")

    def test_store_module_remains_reachable(self):
        by_id = {m["module_id"]: m for m in self.manifest["modules"]}
        self.assertIn("domain.season-stores-paid", by_id)
        mod = by_id["domain.season-stores-paid"]
        for intent in ("store", "black market", "event store"):
            self.assertIn(intent, mod["activation"]["intents"])

    def test_live_offer_and_price_tier_are_authoritative(self):
        lower = (self.stores + "\n" + self.full).lower()
        self.assertIn("current in-game screenshot", lower)
        self.assertIn("good item can still be a bad offer", lower)
        self.assertIn("unit price", lower)
        self.assertIn("buy", lower)
        self.assertIn("conditional", lower)
        self.assertIn("skip", lower)

    def test_reserve_and_carryover_are_evidence_based(self):
        lower = (self.stores + "\n" + self.full).lower()
        self.assertIn("reserve", lower)
        self.assertIn("carry-over", lower)
        self.assertIn("do not invent a reserve amount", lower)
        self.assertIn("cannot be validated", lower)

    def test_account_bottleneck_does_not_excuse_bad_rate(self):
        lower = self.stores.lower()
        self.assertIn("current bottlenecks", lower)
        self.assertIn("poor exchange rate", lower)
        self.assertIn("breakpoint", lower)

if __name__ == "__main__":
    unittest.main()
