from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_INSTALLER = "Set up Last War optimization using the installation instructions at https://github.com/jake6956/LastWar-Account_Audit_Engine"


class UpdateCommandContractTests(unittest.TestCase):
    def test_refresh_engine_is_permanent_public_escape_hatch(self):
        required = {
            "engine/BOOTSTRAP.txt": [
                "refresh engine",
                "force canonical ENGINE update preserving LOCAL STATE",
            ],
            "engine/BOOTSTRAP_FULL.txt": [
                "refresh engine",
                "LOCAL STATE",
            ],
            "engine/modules/release/bootstrap.txt": [
                "`refresh engine`",
                "force the same canonical freshness path immediately",
                "Preserve LOCAL STATE",
            ],
            "contracts/export-bootstrap.md": [
                "`refresh engine`",
                "permanent backwards-compatible update escape hatch",
            ],
        }
        for rel, tokens in required.items():
            body = (ROOT / rel).read_text(encoding="utf-8")
            for token in tokens:
                self.assertIn(token, body, f"{rel} lost permanent update contract token: {token}")

    def test_single_installer_remains_canonical(self):
        loader = (ROOT / "engine/BOOTSTRAP.txt").read_text(encoding="utf-8")
        bootstrap = (ROOT / "engine/modules/release/bootstrap.txt").read_text(encoding="utf-8")
        contract = (ROOT / "contracts/export-bootstrap.md").read_text(encoding="utf-8")
        for body in (loader, bootstrap, contract):
            self.assertIn(CANONICAL_INSTALLER, body)
        self.assertNotIn("https://tinyurl.com/", loader)
        self.assertNotIn("https://tinyurl.com/", bootstrap)
        self.assertNotIn("https://tinyurl.com/", contract)


if __name__ == "__main__":
    unittest.main()
