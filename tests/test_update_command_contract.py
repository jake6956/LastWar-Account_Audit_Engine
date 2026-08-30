from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


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

    def test_single_installer_remains_unchanged(self):
        loader = (ROOT / "engine/BOOTSTRAP.txt").read_text(encoding="utf-8")
        self.assertIn(
            "Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x",
            loader,
        )


if __name__ == "__main__":
    unittest.main()
