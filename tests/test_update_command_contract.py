import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
PUBLIC_URL = "https://lastwarai.com"
LEGACY_URL = "https://tinyurl.com/2yxf7f5x"


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

    def test_one_canonical_public_installer(self):
        latest = json.loads(read("releases/LATEST.json"))
        installer = latest["preferred_install_instruction"]
        self.assertEqual(latest["preferred_install_url"], PUBLIC_URL)
        self.assertEqual(installer, f"Set up Last War optimization using the instructions at {PUBLIC_URL}")
        self.assertIn(LEGACY_URL, latest.get("legacy_install_urls", []))
        self.assertFalse(latest["public_entrypoint_authority"])
        self.assertEqual(latest["live_ref_source"], LIVE_REF)

        for rel in (
            "README.md",
            "engine/modules/release/bootstrap.txt",
            "engine/BOOTSTRAP_FULL.txt",
            "docs/quick-install.md",
            "contracts/bootstrap-resolution.md",
            "releases/2026-08-30.25.json",
        ):
            self.assertIn(installer, read(rel), f"{rel} drifted from canonical public installer")

        loader = read("engine/BOOTSTRAP.txt")
        self.assertIn(LIVE_REF, loader)
        self.assertNotIn(installer, loader, "Stage-1 must not duplicate the public transport installer")
        self.assertNotIn(LEGACY_URL, loader)

    def test_legacy_alias_is_compatibility_only(self):
        latest = json.loads(read("releases/LATEST.json"))
        self.assertIn(LEGACY_URL, latest["legacy_install_urls"])
        for rel in ("README.md", "docs/quick-install.md", "engine/modules/release/bootstrap.txt"):
            lower = read(rel).lower()
            self.assertIn("legacy", lower)
            self.assertIn("compatibility", lower)
        self.assertNotEqual(latest["preferred_install_url"], LEGACY_URL)


if __name__ == "__main__":
    unittest.main()
