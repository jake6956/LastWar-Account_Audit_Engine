"""Regression tests for non-destructive, idempotent derived-view migration plans."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from plan_derived_views import plan_preset_alias_links


class DerivedViewPlanTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"row": 8, "label": "Default Tank", "power": 45.272127},
            {"row": 11, "label": "Default Missile", "power": 36.074593},
            {"row": 14, "label": "Default Air", "power": 32.712996},
            {"row": 22, "label": "Wall defense position 1", "power": 45.272127},
            {"row": 23, "label": "Wall defense position 2", "power": 36.074593},
            {"row": 24, "label": "Wall defense position 3", "power": 32.712996},
            {"row": 31, "label": "Observed Tank lineup (current exact)", "power": 45.272127},
            {"row": 33, "label": "Observed Missile lineup (current exact)", "power": 36.074593},
            {"row": 35, "label": "Observed Air lineup (current exact)", "power": 32.712996},
        ]

    def test_exact_current_aliases_become_references(self):
        p = plan_preset_alias_links(99, self.rows)
        self.assertEqual(len(p["requests"]), 6)
        self.assertEqual(p["conflicts"], [])
        self.assertFalse(p["verified"])
        self.assertTrue(p["mark_revision_after_readback"])
        values = [r["updateCells"]["rows"][0]["values"][0]["userEnteredValue"]["formulaValue"]
                  for r in p["requests"]]
        self.assertEqual(values, ["=B8", "=B11", "=B14", "=B8", "=B11", "=B14"])

    def test_idempotent_after_formulas_verified(self):
        for row in self.rows:
            if row["label"].startswith(("Wall defense", "Observed")):
                source = {"Wall defense position 1": 8, "Wall defense position 2": 11,
                          "Wall defense position 3": 14, "Observed Tank lineup (current exact)": 8,
                          "Observed Missile lineup (current exact)": 11,
                          "Observed Air lineup (current exact)": 14}[row["label"]]
                row["power"] = f"=B{source}"
        p = plan_preset_alias_links(99, self.rows)
        self.assertEqual(p["requests"], [])
        self.assertEqual(p["conflicts"], [])

    def test_conflicting_snapshot_is_preserved(self):
        self.rows[3]["power"] = 44.2
        p = plan_preset_alias_links(99, self.rows)
        self.assertEqual(len(p["requests"]), 5)
        self.assertIn("non-identical", p["conflicts"][0]["reason"])

    def test_protected_or_validated_cells_are_preserved(self):
        self.rows[3]["power"] = {"userEnteredValue": {"numberValue": 45.272127},
                                 "dataValidation": {"condition": {"type": "NUMBER_EQ"}}}
        p = plan_preset_alias_links(99, self.rows)
        self.assertEqual(len(p["requests"]), 5)
        self.assertIn("protected or validated", p["conflicts"][0]["reason"])

    def test_ambiguous_canonical_source_is_not_guessed(self):
        self.rows.append({"row": 40, "label": "Default Tank", "power": 47.0})
        p = plan_preset_alias_links(99, self.rows)
        self.assertEqual(len(p["requests"]), 4)
        self.assertEqual(len(p["conflicts"]), 2)

    def test_public_engine_and_standalone_share_policy(self):
        for path in ["engine/modules/core/persistence.txt",
                     "engine/modules/adapters/storage.txt",
                     "engine/standalone/03-state-storage-onboarding.txt",
                     "contracts/storage-adapter.md"]:
            body = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("derived_view_revision", body)
            self.assertIn("canonical", body.lower())
        fallback = (ROOT / "engine/BOOTSTRAP_FULL.txt").read_text(encoding="utf-8")
        self.assertIn("DERIVED DASHBOARD VIEWS / SAFE REPAIR", fallback)


if __name__ == "__main__":
    unittest.main()
