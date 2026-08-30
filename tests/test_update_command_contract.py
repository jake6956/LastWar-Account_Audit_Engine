import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class UpdateCommandContractTests(unittest.TestCase):
    def test_refresh_engine_is_permanent_public_escape_hatch(self):
        required = {
            "engine/BOOTSTRAP.txt": ["refresh engine", "LOCAL STATE"],
            "engine/BOOTSTRAP_FULL.txt": ["refresh engine", "LOCAL STATE"],
            "engine/modules/release/bootstrap.txt": ["`refresh engine`", "LOCAL STATE"],
            "engine/modules/release/updater.txt": ["`refresh engine`", "release.resolver"],
            "contracts/export-bootstrap.md": ["`refresh engine`"],
        }
        for rel, tokens in required.items():
            body = read(rel)
            for token in tokens:
                self.assertIn(token, body, f"{rel} lost permanent update contract token: {token}")

    def test_one_canonical_stage0_installer(self):
        latest = json.loads(read("releases/LATEST.json"))
        installer = latest["preferred_install_instruction"]
        self.assertEqual(latest["preferred_install_url"], LIVE_REF)
        self.assertIn(LIVE_REF, installer)
        self.assertIn("commit.sha", installer)

        for rel in (
            "README.md",
            "engine/modules/release/bootstrap.txt",
            "docs/quick-install.md",
            "releases/2026-08-30.24.json",
        ):
            self.assertIn(installer, read(rel), f"{rel} drifted from canonical Stage-0 installer")

        loader = read("engine/BOOTSTRAP.txt")
        self.assertIn(LIVE_REF, loader)
        self.assertNotIn(installer, loader, "Stage-1 must not duplicate the Stage-0 installer")
        self.assertNotIn("https://tinyurl.com/", loader)


if __name__ == "__main__":
    unittest.main()
