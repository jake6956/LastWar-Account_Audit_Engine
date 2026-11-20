"""Approved game research sources are registered by provenance, not blanket domain trust."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
def obj(p): return json.loads(read(p))


class ApprovedPublicSourceTests(unittest.TestCase):
    def test_conditional_official_wiki_in_production_gold_asset_registry(self):
        gold=obj("gold-assets/manifest.json")
        a={x["asset_id"]:x for x in gold["assets"]}
        self.assertIn("approved-public-sources-registry",a)
        entry=a["approved-public-sources-registry"]
        self.assertEqual(entry["path"],"gold-assets/sources/registry.json")
        self.assertTrue(entry["sanitized"])
        self.assertFalse(entry["account_state_included"])
        reg=obj(entry["path"])
        self.assertTrue(reg["sanitized"])
        self.assertFalse(reg["account_state_included"])
        self.assertEqual(reg["schema_version"],"lwai-approved-sources/1")
        sources={x["source_id"]:x for x in reg["sources"]}
        wiki=sources["last-war-official-wiki"]
        self.assertEqual(wiki["allowed_host"],"wiki.lastwar.com")
        self.assertEqual(wiki["approval"],"approved_conditional")
        self.assertTrue(reg["default_policy"]["no_bulk_mechanics_import"])

    def test_site_host_never_blindly_promotes_player_comments_to_official(self):
        wiki=obj("gold-assets/sources/registry.json")["sources"][0]
        classes={x["content_type"]:x["rank"] for x in wiki["classification_rules"]}
        self.assertEqual(classes["publisher_notice"],"official_publisher_material")
        self.assertEqual(classes["credited_player_guide"],"community_unverified_until_corroborated")
        self.assertEqual(classes["player_story_or_comment"],"not_approved_as_mechanics_evidence")
        for text in wiki["citation_rules"]+wiki["freshness_rules"]:
            self.assertNotIn("trust every article",text.lower())
        self.assertIn("in-game",str(wiki["freshness_rules"]))

    def test_modules_and_compiled_fallback_share_approved_source_contract(self):
        module=read("engine/modules/core/operating.txt")
        compiled=read("engine/BOOTSTRAP_FULL.txt")
        policy=read("contracts/approved-public-sources.md")
        for body in (module,compiled,policy):
            self.assertIn("gold-assets/sources/registry.json",body)
            self.assertIn("wiki.lastwar.com",body)
        self.assertIn("player-contributed guides",compiled)
        self.assertIn("comments",module)
        self.assertNotIn("wiki.lastwar.com",read("engine/BOOTSTRAP.txt"))

    def test_approval_does_not_become_canonical_account_data(self):
        reg=obj("gold-assets/sources/registry.json")
        self.assertTrue(reg["default_policy"]["consumer_cannot_modify_public_registry"])
        self.assertIn("private canonical",reg["default_policy"]["account_canonical_priority"])
        wiki=reg["sources"][0]
        self.assertIn("exact article",str(wiki["citation_rules"]))
        self.assertIn("Previews",str(wiki["freshness_rules"]))


if __name__=="__main__": unittest.main()
