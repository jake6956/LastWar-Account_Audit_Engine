import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
PUBLIC_URL = "https://lastwarai.com"
LEGACY_URL = "https://tinyurl.com/2yxf7f5x"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class BootstrapResolutionContractTests(unittest.TestCase):
    def setUp(self):
        self.loader = read("engine/BOOTSTRAP.txt")
        self.full = read("engine/BOOTSTRAP_FULL.txt")
        self.resolver = read("engine/modules/release/resolver.txt")
        self.updater = read("engine/modules/release/updater.txt")
        self.bootstrap = read("engine/modules/release/bootstrap.txt")
        self.contract = read("contracts/bootstrap-resolution.md")
        self.latest = json.loads(read("releases/LATEST.json"))
        self.manifest = json.loads(read("engine/MANIFEST.json"))

    def test_first_party_stage0_and_live_ref_are_separate(self):
        self.assertEqual(self.latest["preferred_install_url"], PUBLIC_URL)
        self.assertFalse(self.latest["public_entrypoint_authority"])
        self.assertEqual(self.latest["live_ref_source"], LIVE_REF)
        for body in (self.full, self.bootstrap, self.contract):
            self.assertIn(PUBLIC_URL, body)
            self.assertIn(LIVE_REF, body)
        self.assertIn(LIVE_REF, self.loader)
        self.assertIn("live GitHub `main`", self.resolver)
        self.assertIn("Do not fabricate a SHA", self.resolver)

    def test_candidate_reads_are_pinned_to_one_commit(self):
        for token in (
            "PIN-ONCE SNAPSHOT",
            "releases/LATEST.json",
            "engine/MANIFEST.json",
            "releases/MIGRATIONS.json",
            "engine/BOOTSTRAP_FULL.txt",
            "Never mix",
        ):
            self.assertIn(token, self.resolver)
        self.assertIn("SAME C", self.updater)
        self.assertIn("Never mix commits", self.updater)

    def test_mutable_transport_cannot_be_current_authority(self):
        combined = "\n".join((self.loader, self.full, self.resolver, self.contract, self.bootstrap)).lower()
        for token in ("search", "raw `main`", "readme"):
            self.assertIn(token, combined)
        self.assertFalse(self.latest["mutable_source_urls_are_authority"])
        self.assertFalse(self.latest["public_entrypoint_authority"])
        self.assertEqual(self.latest["candidate_read_policy"], "resolve live main SHA first; pin all candidate reads to that exact commit")

    def test_resolver_is_mandatory_shared_dependency(self):
        by_id = {m["module_id"]: m for m in self.manifest["modules"]}
        self.assertTrue(by_id["release.resolver"]["required"])
        self.assertEqual(by_id["release.resolver"]["load_class"], "mandatory_core")
        self.assertIn("release.resolver", by_id["release.updater"]["dependencies"])
        self.assertIn("release.resolver", by_id["release.bootstrap"]["dependencies"])

    def test_stage1_loader_budget_is_4k(self):
        self.assertLessEqual(len(self.loader.encode("utf-8")), 4096)
        self.assertIn("Stage-1 orchestration only", self.loader)
        self.assertNotIn("Google Drive", self.loader)
        self.assertNotIn("screenname", self.loader.lower())
        self.assertNotIn("GEAR / UPGRADE ORE", self.loader)
        self.assertNotIn(PUBLIC_URL, self.loader)

    def test_fresh_install_fails_closed_without_live_ref(self):
        self.assertIn("Fresh install with no live ref capability", self.resolver)
        self.assertRegex(self.loader, re.compile(r"stop(?:s)? rather than guessing"))
        self.assertIn("last-known-good ENGINE", self.resolver)
        self.assertRegex(self.resolver, re.compile(r"40-lowercase-hex"))

    def test_legacy_shortener_is_compatibility_only(self):
        self.assertIn(LEGACY_URL, self.latest.get("legacy_install_urls", []))
        self.assertNotEqual(self.latest["preferred_install_url"], LEGACY_URL)
        self.assertNotIn(LEGACY_URL, self.loader)
        self.assertNotIn(LEGACY_URL, self.full)
        lower = self.bootstrap.lower()
        self.assertIn("legacy", lower)
        self.assertIn("compatibility", lower)


if __name__ == "__main__":
    unittest.main()
