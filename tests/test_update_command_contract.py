from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
STAGE0_FRAGMENT = "use its current commit SHA"


class UpdateCommandContractTests(unittest.TestCase):
    def test_refresh_engine_is_permanent_public_escape_hatch(self):
        required = {
            "engine/BOOTSTRAP.txt": ["refresh engine", "preserving LOCAL STATE"],
            "engine/BOOTSTRAP_FULL.txt": ["refresh engine", "LOCAL STATE"],
            "engine/modules/release/bootstrap.txt": ["`refresh engine`", "preserving LOCAL STATE"],
            "engine/modules/release/updater.txt": ["`refresh engine`", "release.resolver"],
            "contracts/export-bootstrap.md": ["`refresh engine`"],
        }
        for rel, tokens in required.items():
            body = (ROOT / rel).read_text(encoding="utf-8")
            for token in tokens:
                self.assertIn(token, body, f"{rel} lost permanent update contract token: {token}")

    def test_single_installer_is_live_ref_stage0(self):
        loader = (ROOT / "engine/BOOTSTRAP.txt").read_text(encoding="utf-8")
        bootstrap = (ROOT / "engine/modules/release/bootstrap.txt").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for body in (loader, bootstrap, readme):
            self.assertIn(LIVE_REF, body)
            self.assertIn(STAGE0_FRAGMENT, body)
        self.assertNotIn("https://tinyurl.com/", loader)
        self.assertNotIn("https://tinyurl.com/", bootstrap)


if __name__ == "__main__":
    unittest.main()
