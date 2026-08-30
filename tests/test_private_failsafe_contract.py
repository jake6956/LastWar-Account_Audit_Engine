import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PrivateFailsafeMirrorContractTests(unittest.TestCase):
    def test_drive_mirror_is_a_pre_promotion_gate(self):
        body = (ROOT / "contracts/private-failsafe-mirror.md").read_text(encoding="utf-8")
        for token in (
            "Mandatory pre-promotion gate",
            "Promotion is blocked",
            "Post-merge synchronization",
            "Source-staging hygiene",
            "Private runtime-state hygiene",
            "Pre-promotion mirror failure: do not promote",
            "WAITING_USER",
            "RECOVERY_REQUIRED",
        ):
            self.assertIn(token, body)

    def test_drive_failsafe_never_becomes_public_version_authority(self):
        body = (ROOT / "contracts/private-failsafe-mirror.md").read_text(encoding="utf-8")
        latest = json.loads((ROOT / "releases/LATEST.json").read_text(encoding="utf-8"))
        self.assertIn("GitHub `main` remains authoritative sanitized Production", body)
        self.assertEqual(latest["live_ref_source"], "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main")
        self.assertFalse(latest["public_entrypoint_authority"])

    def test_flow_continuity_is_mandatory_manifest_core(self):
        manifest = json.loads((ROOT / "engine/MANIFEST.json").read_text(encoding="utf-8"))
        by_id = {module["module_id"]: module for module in manifest["modules"]}
        flow = by_id["core.flow-continuity"]
        self.assertTrue(flow["required"])
        self.assertEqual(flow["load_class"], "mandatory_core")
        self.assertEqual(flow["workspace_schema"], {"min": "2.1", "max": "2.3"})
        self.assertIn("core.flow-continuity", by_id["release.bootstrap"]["dependencies"])


if __name__ == "__main__":
    unittest.main()
