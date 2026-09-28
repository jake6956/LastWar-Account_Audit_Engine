import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CompiledBootstrapTests(unittest.TestCase):
    def test_checked_in_fallback_is_exact_compiler_output(self):
        proc = subprocess.run(
            [sys.executable, "scripts/build_bootstrap_full.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PASS: compiled single-response artifact is exact", proc.stdout)

    def test_compiler_inputs_are_modular_and_output_is_not_an_input(self):
        plan = (ROOT / "engine/standalone/plan.json").read_text(encoding="utf-8")
        self.assertNotIn('"path": "engine/BOOTSTRAP_FULL.txt"', plan)
        for name in (
            "01-release-bootstrap.txt",
            "02-governance-preferences.txt",
            "03-state-storage-onboarding.txt",
            "04-season-events.txt",
            "05-progression-economy.txt",
            "06-combat.txt",
            "07-routing-startup.txt",
        ):
            self.assertIn(name, plan)


if __name__ == "__main__":
    unittest.main()
