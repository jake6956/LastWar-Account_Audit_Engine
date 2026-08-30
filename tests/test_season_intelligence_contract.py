import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SeasonIntelligenceContractTests(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def read_json(self, rel):
        return json.loads(self.read(rel))

    def test_module_is_reachable_and_stores_depend_on_it(self):
        manifest = self.read_json("engine/MANIFEST.json")
        modules = {m["module_id"]: m for m in manifest["modules"]}
        self.assertIn("domain.season-intelligence", modules)
        season = modules["domain.season-intelligence"]
        self.assertEqual(season["load_class"], "domain_on_demand")
        self.assertFalse(season["required"])
        self.assertIn("domain.season-intelligence", modules["domain.season-stores-paid"]["dependencies"])

    def test_module_enforces_due_diligence_and_self_healing(self):
        body = self.read("engine/modules/domains/season-intelligence.txt").lower()
        for token in [
            "season identity / phase",
            "first season-sensitive task",
            "24 hours",
            "due diligence / live re-verification",
            "consequential gate",
            "current direct user evidence outranks",
            "consumer runtime never writes",
            "refresh season knowledge",
            "no-web fallback",
        ]:
            self.assertIn(token, body)

    def test_public_registry_and_seed_packs_are_sanitized(self):
        registry = self.read_json("gold-assets/seasons/registry.json")
        self.assertTrue(registry["sanitized"])
        self.assertFalse(registry["account_state_included"])
        self.assertEqual(registry["schema_version"], "season-knowledge/1")
        self.assertTrue(registry["policy"]["consequential_live_reverification"])
        self.assertFalse(registry["policy"]["consumer_public_writeback"])
        self.assertGreaterEqual(len(registry["packs"]), 3)
        for entry in registry["packs"]:
            path = ROOT / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            pack = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(pack["schema_version"], "season-knowledge/1")
            self.assertTrue(pack["sanitized"])
            self.assertFalse(pack["account_state_included"])
            self.assertIsInstance(pack["facts"], list)
            self.assertIsInstance(pack["research_topics"], list)

    def test_gold_assets_register_season_registry(self):
        gold = self.read_json("gold-assets/manifest.json")
        assets = {a["asset_id"]: a for a in gold["assets"]}
        self.assertIn("season-intelligence-registry", assets)
        asset = assets["season-intelligence-registry"]
        self.assertEqual(asset["status"], "production-qualified")
        self.assertEqual(asset["path"], "gold-assets/seasons/registry.json")
        self.assertFalse(asset["account_state_included"])

    def test_stage1_loader_does_not_embed_season_policy(self):
        loader = self.read("engine/BOOTSTRAP.txt")
        full = self.read("engine/BOOTSTRAP_FULL.txt")
        manifest = self.read("engine/MANIFEST.json")
        self.assertNotIn("domain.season-intelligence", loader)
        self.assertIn("domain.season-intelligence", manifest)
        self.assertIn("SEASON INTELLIGENCE", full)
        self.assertIn("refresh season knowledge", full)
        self.assertNotIn("fact_id", loader)
        self.assertLessEqual(len(loader.encode("utf-8")), 4096)

    def test_contract_preserves_privacy_boundary(self):
        contract = self.read("contracts/season-intelligence.md").lower()
        for token in [
            "production-qualified knowledge packs",
            "community evidence and inference must never be presented as official fact",
            "consumer runtimes do not write discoveries directly to public github",
            "private mechanics registry",
            "knowledge refresh never mutates account facts",
        ]:
            self.assertIn(token, contract)


if __name__ == "__main__":
    unittest.main()
