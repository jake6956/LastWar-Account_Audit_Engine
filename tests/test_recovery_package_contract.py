import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_recovery_package import validate


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True
    ).stdout.strip()


class RecoveryPackageContractTests(unittest.TestCase):
    def build(self, output: Path, without_legacy: bool = False) -> None:
        cmd = [
            sys.executable,
            str(ROOT / "scripts/build_recovery_package.py"),
            "--source-commit", git_head(),
            "--output", str(output),
        ]
        if without_legacy:
            cmd.append("--without-legacy-fallback")
        subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)

    def test_recovery_package_is_deterministic_and_valid(self):
        with tempfile.TemporaryDirectory() as td:
            a = Path(td) / "a.zip"
            b = Path(td) / "b.zip"
            self.build(a)
            self.build(b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            manifest = validate(str(a), git_head())
            self.assertTrue(manifest["legacy_fallback_included"])
            self.assertEqual(manifest["primary_bootstrap"], "engine/BOOTSTRAP.txt")

    def test_package_can_be_complete_without_legacy_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            package = Path(td) / "modular.zip"
            self.build(package, without_legacy=True)
            manifest = validate(str(package), git_head())
            self.assertFalse(manifest["legacy_fallback_included"])
            with zipfile.ZipFile(package) as zf:
                names = set(zf.namelist())
            self.assertNotIn("engine/BOOTSTRAP_FULL.txt", names)
            engine_manifest = json.loads((ROOT / "engine/MANIFEST.json").read_text(encoding="utf-8"))
            for module in engine_manifest["modules"]:
                self.assertIn(module["path"], names)

    def test_tampered_payload_fails_validation(self):
        with tempfile.TemporaryDirectory() as td:
            original = Path(td) / "original.zip"
            tampered = Path(td) / "tampered.zip"
            self.build(original)
            with zipfile.ZipFile(original, "r") as src, zipfile.ZipFile(tampered, "w") as dst:
                for info in src.infolist():
                    data = src.read(info.filename)
                    if info.filename == "engine/BOOTSTRAP.txt":
                        data += b"\nTAMPERED\n"
                    dst.writestr(info, data)
            with self.assertRaises(SystemExit):
                validate(str(tampered), git_head())


if __name__ == "__main__":
    unittest.main()
