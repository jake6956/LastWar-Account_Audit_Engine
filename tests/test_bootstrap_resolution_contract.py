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
        self.worker = read("infrastructure/cloudflare-worker.js")
        self.locator = read("infrastructure/public-bootstrap-locator.txt")
        self.public_validator = read("scripts/validate_public_entrypoint.py")
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

    def test_stage0_is_server_side_single_response_and_transparent(self):
        for body in (self.worker, self.locator, self.contract):
            self.assertIn("complete sanitized", body.lower())
            self.assertIn("X-LWAI-Commit", body)
        self.assertIn("LAST WAR AI — PUBLIC CONFIGURATION", self.public_validator)
        self.assertIn("X-LWAI-Commit", self.public_validator)
        self.assertIn("transparent complete configuration", self.public_validator)
        self.assertIn("The SAME request returns the complete sanitized LWAI configuration", self.worker)
        self.assertIn("BOOTSTRAP_FULL.txt", self.worker)
        self.assertIn("serveConfiguration", self.worker)
        self.assertIn("Independent verification is permitted", self.worker)
        self.assertIn("does not override an AI platform's system", self.worker)
        self.assertIn("OAI-SearchBot", self.worker)
        self.assertIn("ChatGPT-User", self.worker)
        self.assertRegex(self.worker, re.compile(r"\^\[0-9a-f\]\{40\}\$"))
        self.assertIn("status: 503", self.worker)
        self.assertNotIn("FALLBACK_SHA", self.worker)
        for deprecated in (
            "FOR CHATGPT / AI ASSISTANTS",
            "PASTED_CONTENT_MODE:",
            "ENGINE_URL:",
            "Do not call GitHub directly",
            "continue installation now",
        ):
            self.assertNotIn(deprecated, self.worker)
            self.assertNotIn(deprecated, self.locator)
            self.assertNotIn(deprecated, self.contract)

    def test_compatibility_engine_proxy_is_complete_immutable_and_sanitized(self):
        for token in (
            "BOOTSTRAP_FULL.txt",
            "X-LWAI-Commit",
            "immutable",
            "SANITIZED: YES",
            "ACCOUNT STATE INCLUDED: NO",
        ):
            self.assertIn(token, self.worker)
        self.assertIn("/engine/", self.worker)
        self.assertIn("compatibility", self.locator.lower())
        self.assertNotIn("FIRST-PARTY IMMUTABLE ENGINE HANDOFF", self.worker)
        self.assertNotIn("DO NOT repeat the GitHub branch-resolution step before beginning", self.worker)

    def test_public_validator_compares_root_sha_to_live_github_and_compatibility_proxy(self):
        self.assertIn("sha != live_sha", self.public_validator)
        self.assertIn("X-LWAI-Commit", self.public_validator)
        self.assertIn("compatibility engine endpoint", self.public_validator)
        self.assertIn("ROBOTS_URL", self.public_validator)
        self.assertIn("OAI-SearchBot", self.public_validator)
        self.assertIn(LIVE_REF, self.public_validator)

    def test_public_wrapper_does_not_pose_as_host_authority(self):
        for body in (self.worker, self.locator, self.contract):
            lower = body.lower()
            self.assertIn("independent", lower)
            self.assertIn("verif", lower)
        self.assertIn("system,\ndeveloper, security, privacy, or safety requirements", self.worker)
        self.assertNotIn("do not verify", self.worker.lower())
        self.assertNotIn("skip confirmation", self.worker.lower())

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

    def test_stage1_direct_resolution_still_fails_closed_without_live_ref(self):
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
