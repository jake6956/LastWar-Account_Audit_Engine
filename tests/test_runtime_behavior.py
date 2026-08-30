import json
import unittest
from pathlib import Path

from reference_runtime import (
    ProviderCapabilities,
    RuntimeModel,
    canonicalize_installer_identity,
    installer_version_announcement,
    resolve_engine_version,
    should_check_engine_freshness,
    should_offer_persistence_reminder,
)

ROOT = Path(__file__).resolve().parents[1]


class DurableTarget:
    def __init__(self):
        self.applied = set()
        self.apply_count = {}

    def probe(self, action):
        return action in self.applied

    def apply(self, action):
        self.apply_count[action] = self.apply_count.get(action, 0) + 1
        self.applied.add(action)


class RuntimeBehaviorTests(unittest.TestCase):
    def test_active_account_routing_isolation(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.write_fact("ore", 100); rt.create_account("B"); rt.write_fact("ore", 25)
        self.assertEqual(rt.accounts["A"].facts["ore"], 100); self.assertEqual(rt.accounts["B"].facts["ore"], 25)
        rt.switch_account("A"); rt.write_fact("ore", 120)
        self.assertEqual(rt.accounts["A"].facts["ore"], 120); self.assertEqual(rt.accounts["B"].facts["ore"], 25)

    def test_start_over_archives_instead_of_deleting(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.write_fact("hero", "state"); rt.start_over("B")
        self.assertEqual(rt.accounts["A"].status, "ARCHIVED"); self.assertEqual(rt.accounts["A"].facts["hero"], "state"); self.assertEqual(rt.active_account_id, "B")
        rt.restore_account("A"); self.assertEqual(rt.accounts["A"].status, "ACTIVE")

    def test_legacy_migration_preserves_facts(self):
        rt = RuntimeModel(); source = {"gear": {"g1": 40}, "correction": "never regress"}; acct = rt.migrate_legacy("A", source)
        self.assertEqual(acct.account_id, "A"); self.assertEqual(acct.facts, source); self.assertEqual(rt.active_account_id, "A")

    def test_pre_registry_legacy_startup_registers_before_recovery(self):
        rt = RuntimeModel(); source = {"gear": {"g1": 40}, "correction": "never regress"}; steps = rt.startup_from_storage(legacy_facts=source)
        self.assertEqual(steps, ["legacy_discovery", "register_legacy", "resolve_active_account", "recovery_first", "migration_reconcile"])
        self.assertEqual(rt.active_account_id, "legacy"); self.assertEqual(rt.accounts["legacy"].facts, source)

    def test_current_registry_resolves_account_before_recovery(self):
        rt = RuntimeModel(); steps = rt.startup_from_storage(registry_accounts={"A": {"ore": 100}, "B": {"ore": 25}}, active_account_id="A")
        self.assertEqual(steps, ["load_registry", "resolve_active_account", "recovery_first", "migration_reconcile"])
        self.assertEqual(rt.active_account_id, "A")

    def test_new_user_without_writable_storage_is_prompted_before_onboarding(self):
        rt = RuntimeModel(); steps = rt.startup_from_storage(provider_capabilities=ProviderCapabilities(read=False, list=False))
        self.assertEqual(steps, ["first_run_persistence_prompt_connect_or_session"])
        self.assertEqual(rt.accounts, {}); self.assertIsNone(rt.active_account_id)
        self.assertNotIn("new_account_guidance", steps)

    def test_new_user_with_writable_storage_is_prompted_before_onboarding(self):
        caps = ProviderCapabilities(read=True, list=True, write=True, create=True)
        rt = RuntimeModel(); steps = rt.startup_from_storage(provider_capabilities=caps)
        self.assertEqual(steps, ["first_run_persistence_prompt_cloud_or_session"])
        self.assertEqual(rt.accounts, {}); self.assertNotIn("new_account_guidance", steps)

    def test_new_user_can_explicitly_continue_session_only(self):
        rt = RuntimeModel(); steps = rt.startup_from_storage(provider_capabilities=ProviderCapabilities(read=False, list=False), persistence_choice="continue session-only")
        self.assertEqual(steps, ["first_run_persistence_choice", "session_only_acknowledged", "new_account_guidance"])
        self.assertEqual(rt.accounts, {}); self.assertEqual(rt.persistence_mode, "SESSION_ONLY")

    def test_new_user_cloud_choice_creates_workspace_before_onboarding(self):
        caps = ProviderCapabilities(read=True, list=True, write=True, create=True, query=True)
        rt = RuntimeModel(); steps = rt.startup_from_storage(provider_capabilities=caps, persistence_choice="use cloud storage")
        self.assertEqual(steps, ["first_run_persistence_choice", "create_private_workspace", "verify_private_workspace", "new_account_guidance"])
        self.assertLess(steps.index("verify_private_workspace"), steps.index("new_account_guidance")); self.assertEqual(rt.persistence_mode, "DURABLE")

    def test_storage_connected_requires_capability_recheck_before_onboarding(self):
        rt = RuntimeModel(); steps = rt.startup_from_storage(provider_capabilities=ProviderCapabilities(read=False, list=False), persistence_choice="storage connected")
        self.assertEqual(steps, ["recheck_storage_capabilities"])
        self.assertNotIn("new_account_guidance", steps)

    def test_unverified_cloud_choice_fails_closed(self):
        rt = RuntimeModel()
        with self.assertRaises(RuntimeError):
            rt.startup_from_storage(provider_capabilities=ProviderCapabilities(read=True, write=False, create=False), persistence_choice="use cloud storage")
        self.assertEqual(rt.accounts, {})

    def test_existing_workspace_skips_first_run_persistence_prompt(self):
        rt = RuntimeModel(); steps = rt.startup_from_storage(registry_accounts={"A": {"ore": 100}}, active_account_id="A", provider_capabilities=ProviderCapabilities(read=False, list=False))
        self.assertEqual(steps, ["load_registry", "resolve_active_account", "recovery_first", "migration_reconcile"])
        self.assertEqual(rt.persistence_mode, "DURABLE")

    def test_session_only_reminder_requires_material_benefit(self):
        self.assertFalse(should_offer_persistence_reminder(session_only=True, material_benefit=False, reminded_this_runtime=False, do_not_ask_again=False))
        self.assertTrue(should_offer_persistence_reminder(session_only=True, material_benefit=True, reminded_this_runtime=False, do_not_ask_again=False))
        self.assertFalse(should_offer_persistence_reminder(session_only=False, material_benefit=True, reminded_this_runtime=False, do_not_ask_again=False))

    def test_session_only_reminder_once_per_runtime_and_seven_day_cooldown(self):
        rt = RuntimeModel(); rt.startup_from_storage(provider_capabilities=ProviderCapabilities(read=False, list=False), persistence_choice="continue session-only")
        rt.start_runtime_session("RS1")
        self.assertTrue(rt.consider_persistence_reminder(material_benefit=True, day=100))
        self.assertFalse(rt.consider_persistence_reminder(material_benefit=True, day=100))
        rt.start_runtime_session("RS2")
        self.assertFalse(rt.consider_persistence_reminder(material_benefit=True, day=103))
        rt.start_runtime_session("RS3")
        self.assertTrue(rt.consider_persistence_reminder(material_benefit=True, day=107))

    def test_session_only_do_not_ask_again_suppresses_future_reminders(self):
        rt = RuntimeModel(); rt.startup_from_storage(provider_capabilities=ProviderCapabilities(read=False, list=False), persistence_choice="continue session-only")
        rt.start_runtime_session("RS1"); self.assertTrue(rt.consider_persistence_reminder(material_benefit=True))
        rt.record_persistence_reminder_response("don't ask again")
        rt.start_runtime_session("RS2"); self.assertFalse(rt.consider_persistence_reminder(material_benefit=True))

    def test_workspace_schema_21_to_23_preserves_state(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.write_fact("ore", 100); rt.write_fact("correction", "keep me")
        facts_before = dict(rt.accounts["A"].facts); history_before = list(rt.accounts["A"].history); active_before = rt.active_account_id
        rt.set_workspace_schema("2.1"); applied = rt.migrate_workspace_schema("2.3")
        self.assertEqual(applied, ["2.1->2.2", "2.2->2.3"]); self.assertEqual(rt.workspace_schema_version, "2.3")
        self.assertEqual(rt.active_account_id, active_before); self.assertEqual(rt.accounts["A"].facts, facts_before); self.assertEqual(rt.accounts["A"].history, history_before)
        self.assertEqual(rt.workspace_optional_structures, {"guidance_metadata", "audit_sessions", "runtime_checkpoints", "runtime_journal"})

    def test_workspace_schema_migration_is_idempotent(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.set_workspace_schema("2.1"); rt.migrate_workspace_schema("2.3")
        structures = set(rt.workspace_optional_structures); facts = dict(rt.accounts["A"].facts)
        self.assertEqual(rt.migrate_workspace_schema("2.3"), []); self.assertEqual(rt.workspace_optional_structures, structures); self.assertEqual(rt.accounts["A"].facts, facts)

    def test_workspace_schema_migration_failure_preserves_original(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.write_fact("ore", 100); rt.set_workspace_schema("2.1"); original = dict(rt.accounts["A"].facts)
        with self.assertRaises(RuntimeError): rt.migrate_workspace_schema("2.3", fail_after_edge="2.1->2.2")
        self.assertEqual(rt.workspace_schema_version, "2.1"); self.assertEqual(rt.workspace_optional_structures, set()); self.assertEqual(rt.accounts["A"].facts, original); self.assertEqual(rt.active_account_id, "A")

    def test_registered_21_workspace_migrates_before_recovery(self):
        rt = RuntimeModel(); steps = rt.startup_from_storage(registry_accounts={"A": {"ore": 100}}, active_account_id="A", workspace_schema_version="2.1")
        self.assertEqual(steps, ["load_registry", "resolve_active_account", "workspace_schema_migrate", "recovery_first", "migration_reconcile"])
        self.assertEqual(rt.workspace_schema_version, "2.3"); self.assertEqual(rt.accounts["A"].facts["ore"], 100)

    def test_migration_capable_modules_bootstrap_legacy_schema(self):
        manifest = json.loads((ROOT / "engine/MANIFEST.json").read_text(encoding="utf-8")); by_id = {m["module_id"]: m for m in manifest["modules"]}
        ids = {"core.operating", "core.persistence", "core.accounts", "core.guidance", "release.runtime", "release.bootstrap", "adapters.storage"}
        for module_id in ids:
            self.assertEqual(by_id[module_id]["workspace_schema"]["min"], "2.1"); self.assertEqual(by_id[module_id]["workspace_schema"]["max"], "2.3")

    def test_domain_modules_blocked_before_target_schema(self):
        manifest = json.loads((ROOT / "engine/MANIFEST.json").read_text(encoding="utf-8")); domains = [m for m in manifest["modules"] if m["load_class"] == "domain_on_demand"]
        self.assertTrue(domains); self.assertTrue(all(m["workspace_schema"]["min"] == "2.3" for m in domains))

    def test_historical_workspace_schema_edges_exist(self):
        migrations = json.loads((ROOT / "releases/MIGRATIONS.json").read_text(encoding="utf-8")); pairs = {(e["from"], e["to"]) for e in migrations["workspace_schema_edges"]}
        self.assertIn(("2.1", "2.2"), pairs); self.assertIn(("2.2", "2.3"), pairs)
        for edge in migrations["workspace_schema_edges"]:
            self.assertEqual(edge["local_state_action"], "preserve"); self.assertFalse(edge["requires_user_reonboarding"]); self.assertFalse(edge["requires_account_rewrite"])

    def test_stale_alias_cannot_downgrade_canonical_production(self):
        self.assertEqual(canonicalize_installer_identity(alias_version="2026-08-29.13", canonical_version="2026-08-29.17", canonical_verified=True), "2026-08-29.17")
        self.assertIsNone(canonicalize_installer_identity(alias_version="2026-08-29.13", canonical_version=None, canonical_verified=False))

    def test_stale_alias_version_is_not_announced_as_active(self):
        announcement = installer_version_announcement(alias_version="2026-08-29.13", canonical_version="2026-08-29.17", canonical_verified=True)
        self.assertEqual(announcement, "Verified Production 2026-08-29.17")
        self.assertNotIn("2026-08-29.13", announcement)

    def test_engine_freshness_checks_every_runtime_startup(self):
        self.assertTrue(should_check_engine_freshness(web_available=True, startup=True, hours_since_last_success=0.1))
        self.assertFalse(should_check_engine_freshness(web_available=False, startup=True, hours_since_last_success=None))

    def test_engine_freshness_rechecks_after_six_hours_not_before(self):
        self.assertFalse(should_check_engine_freshness(web_available=True, startup=False, hours_since_last_success=5.99))
        self.assertTrue(should_check_engine_freshness(web_available=True, startup=False, hours_since_last_success=6.0))
        self.assertTrue(should_check_engine_freshness(web_available=True, startup=False, hours_since_last_success=None))

    def test_engine_freshness_adopts_only_newer_verified_production(self):
        self.assertEqual(resolve_engine_version(current_version="2026-08-29.16", canonical_version="2026-08-29.17", canonical_verified=True), "2026-08-29.17")
        self.assertEqual(resolve_engine_version(current_version="2026-08-29.17", canonical_version="2026-08-29.16", canonical_verified=True), "2026-08-29.17")
        self.assertEqual(resolve_engine_version(current_version="2026-08-29.16", canonical_version="2026-08-29.18", canonical_verified=False), "2026-08-29.16")
        self.assertEqual(resolve_engine_version(current_version="2026-08-29.16", canonical_version="2026-08-29.18", canonical_verified=True, canonical_channel="RC"), "2026-08-29.16")

    def test_runtime_session_exists_without_host_reference(self):
        rt = RuntimeModel(); rt.create_account("A"); session = rt.start_runtime_session("RS1", host_platform="chatgpt")
        self.assertEqual(session.runtime_session_id, "RS1"); self.assertEqual(session.account_id, "A"); self.assertIsNone(session.host_session_ref)

    def test_duplicate_host_ref_does_not_merge_runtime_sessions(self):
        rt = RuntimeModel(); rt.create_account("A")
        one = rt.start_runtime_session("RS1", host_platform="chatgpt", host_session_ref="opaque-ref", host_session_ref_source="runtime_exposed")
        two = rt.start_runtime_session("RS2", host_platform="chatgpt", host_session_ref="opaque-ref", host_session_ref_source="import")
        self.assertNotEqual(one.runtime_session_id, two.runtime_session_id); self.assertEqual(len(rt.runtime_sessions), 2); self.assertEqual(len(rt.accounts), 1)

    def test_distinct_host_refs_do_not_duplicate_account(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.start_runtime_session("RS1", host_session_ref="ref-one"); rt.start_runtime_session("RS2", host_session_ref="ref-two")
        self.assertEqual(list(rt.accounts), ["A"])

    def test_audit_session_is_account_scoped_and_links_provenance(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.start_runtime_session("RS-A", host_session_ref="same-host-ref"); rt.start_audit_session("S-A")
        rt.create_account("B"); rt.start_runtime_session("RS-B", host_session_ref="same-host-ref"); rt.start_audit_session("S-B")
        self.assertEqual(rt.accounts["A"].audit_session["account_id"], "A"); self.assertEqual(rt.accounts["B"].audit_session["account_id"], "B")
        self.assertEqual(rt.accounts["A"].audit_session["runtime_session_id"], "RS-A"); self.assertEqual(rt.accounts["B"].audit_session["runtime_session_id"], "RS-B")

    def test_waiting_user_boundary_survives_model_reload(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.start_runtime_session("RS1"); cp = rt.create_checkpoint("CP1", scope="AUDIT", account_id="A", objective="screens"); rt.enter_waiting_user("CP1", "reply done")
        target = DurableTarget(); rt.resume_checkpoint("CP1", durable_probe=target.probe, apply_action=target.apply)
        self.assertEqual(cp.status, "WAITING_USER"); self.assertEqual(target.apply_count, {})

    def test_checkpoint_cannot_cross_active_account_even_with_matching_host_ref(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.start_runtime_session("RS-A", host_session_ref="shared-host-ref"); rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="update", pending_actions=["x"])
        rt.create_account("B"); rt.start_runtime_session("RS-B", host_session_ref="shared-host-ref")
        with self.assertRaises(RuntimeError): rt.resume_checkpoint("CP1", durable_probe=lambda _: False, apply_action=lambda _: None)

    def test_verify_before_replay_does_not_duplicate_successful_write(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="write", pending_actions=["create-record"])
        target = DurableTarget(); target.applied.add("create-record"); rt.resume_checkpoint("CP1", durable_probe=target.probe, apply_action=target.apply)
        self.assertEqual(target.apply_count.get("create-record", 0), 0); self.assertEqual(rt.checkpoints["CP1"].status, "COMMITTED")

    def test_recovery_applies_only_unverified_actions_once(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="write", pending_actions=["one", "two"])
        target = DurableTarget(); target.applied.add("one"); rt.resume_checkpoint("CP1", durable_probe=target.probe, apply_action=target.apply)
        self.assertEqual(target.apply_count.get("one", 0), 0); self.assertEqual(target.apply_count.get("two", 0), 1); self.assertEqual(rt.checkpoints["CP1"].status, "COMMITTED")

    def test_committed_checkpoint_not_replayed_during_schema_migration(self):
        rt = RuntimeModel(); rt.create_account("A"); cp = rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="done"); cp.status = "COMMITTED"; journal_before = tuple(rt.journal)
        rt.set_workspace_schema("2.1"); rt.migrate_workspace_schema("2.3"); target = DurableTarget(); rt.resume_checkpoint("CP1", durable_probe=target.probe, apply_action=target.apply)
        self.assertEqual(target.apply_count, {}); self.assertEqual(rt.checkpoints["CP1"].status, "COMMITTED"); self.assertEqual(rt.journal, journal_before)

    def test_checkpoint_loss_cannot_destroy_canonical_facts(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.write_fact("ore", 100); rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="noop"); del rt.checkpoints["CP1"]
        self.assertEqual(rt.accounts["A"].facts["ore"], 100)

    def test_journal_surface_is_append_only_snapshot(self):
        rt = RuntimeModel(); rt.create_account("A"); rt.start_runtime_session("RS1"); rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="noop"); snapshot = rt.journal
        self.assertIsInstance(snapshot, tuple)
        with self.assertRaises(AttributeError): snapshot.append("mutate")

    def test_provider_profiles_and_journal_safety(self):
        self.assertEqual(ProviderCapabilities(read=False).persistence_profile, "NONE"); self.assertEqual(ProviderCapabilities(read=True).persistence_profile, "READ_ONLY")
        file_rw = ProviderCapabilities(read=True, write=True, create=True); self.assertEqual(file_rw.persistence_profile, "FILE_RW"); self.assertTrue(file_rw.can_authoritative_journal); self.assertTrue(file_rw.can_durable_persist)
        cas = ProviderCapabilities(read=True, write=True, create=True, compare_and_swap=True); self.assertEqual(cas.persistence_profile, "CAS_RW")
        transactional = ProviderCapabilities(read=True, write=True, create=True, query=True, atomic_append=True, compare_and_swap=True)
        self.assertEqual(transactional.persistence_profile, "TRANSACTIONAL_RW"); self.assertTrue(transactional.can_authoritative_journal)
        self.assertFalse(ProviderCapabilities(read=True, write=False, create=False).can_durable_persist)


if __name__ == "__main__":
    unittest.main()
