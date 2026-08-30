import unittest

from reference_runtime import ProviderCapabilities, RuntimeModel


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
        rt = RuntimeModel()
        rt.create_account("A")
        rt.write_fact("ore", 100)
        rt.create_account("B")
        rt.write_fact("ore", 25)
        self.assertEqual(rt.accounts["A"].facts["ore"], 100)
        self.assertEqual(rt.accounts["B"].facts["ore"], 25)
        rt.switch_account("A")
        rt.write_fact("ore", 120)
        self.assertEqual(rt.accounts["A"].facts["ore"], 120)
        self.assertEqual(rt.accounts["B"].facts["ore"], 25)

    def test_start_over_archives_instead_of_deleting(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.write_fact("hero", "state")
        rt.start_over("B")
        self.assertEqual(rt.accounts["A"].status, "ARCHIVED")
        self.assertEqual(rt.accounts["A"].facts["hero"], "state")
        self.assertEqual(rt.active_account_id, "B")
        rt.restore_account("A")
        self.assertEqual(rt.accounts["A"].status, "ACTIVE")

    def test_legacy_migration_preserves_facts(self):
        rt = RuntimeModel()
        source = {"gear": {"g1": 40}, "correction": "never regress"}
        acct = rt.migrate_legacy("A", source)
        self.assertEqual(acct.account_id, "A")
        self.assertEqual(acct.facts, source)
        self.assertEqual(rt.active_account_id, "A")

    def test_pre_registry_legacy_startup_registers_before_recovery(self):
        rt = RuntimeModel()
        source = {"gear": {"g1": 40}, "correction": "never regress"}
        steps = rt.startup_from_storage(legacy_facts=source)
        self.assertEqual(
            steps,
            [
                "legacy_discovery",
                "register_legacy",
                "resolve_active_account",
                "recovery_first",
                "migration_reconcile",
            ],
        )
        self.assertEqual(rt.active_account_id, "legacy")
        self.assertEqual(rt.accounts["legacy"].facts, source)
        self.assertLess(steps.index("register_legacy"), steps.index("recovery_first"))

    def test_current_registry_resolves_account_before_recovery(self):
        rt = RuntimeModel()
        steps = rt.startup_from_storage(
            registry_accounts={"A": {"ore": 100}, "B": {"ore": 25}},
            active_account_id="A",
        )
        self.assertEqual(
            steps,
            ["load_registry", "resolve_active_account", "recovery_first", "migration_reconcile"],
        )
        self.assertEqual(rt.active_account_id, "A")
        self.assertEqual(rt.accounts["A"].facts["ore"], 100)

    def test_runtime_session_exists_without_host_reference(self):
        rt = RuntimeModel()
        rt.create_account("A")
        session = rt.start_runtime_session("RS1", host_platform="chatgpt")
        self.assertEqual(session.runtime_session_id, "RS1")
        self.assertEqual(session.account_id, "A")
        self.assertIsNone(session.host_session_ref)
        self.assertEqual(rt.current_runtime_session_id, "RS1")

    def test_duplicate_host_ref_does_not_merge_runtime_sessions(self):
        rt = RuntimeModel()
        rt.create_account("A")
        one = rt.start_runtime_session(
            "RS1", host_platform="chatgpt", host_session_ref="opaque-ref", host_session_ref_source="runtime_exposed"
        )
        two = rt.start_runtime_session(
            "RS2", host_platform="chatgpt", host_session_ref="opaque-ref", host_session_ref_source="import"
        )
        self.assertNotEqual(one.runtime_session_id, two.runtime_session_id)
        self.assertEqual(len(rt.runtime_sessions), 2)
        self.assertEqual(len(rt.accounts), 1)
        self.assertEqual(one.account_id, "A")
        self.assertEqual(two.account_id, "A")

    def test_distinct_host_refs_do_not_duplicate_account(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.start_runtime_session("RS1", host_session_ref="ref-one")
        rt.start_runtime_session("RS2", host_session_ref="ref-two")
        self.assertEqual(list(rt.accounts), ["A"])
        self.assertEqual(rt.runtime_sessions["RS1"].account_id, "A")
        self.assertEqual(rt.runtime_sessions["RS2"].account_id, "A")

    def test_audit_session_is_account_scoped_and_links_provenance(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.start_runtime_session("RS-A", host_session_ref="same-host-ref")
        rt.start_audit_session("S-A")
        rt.create_account("B")
        rt.start_runtime_session("RS-B", host_session_ref="same-host-ref")
        rt.start_audit_session("S-B")
        self.assertEqual(rt.accounts["A"].audit_session["account_id"], "A")
        self.assertEqual(rt.accounts["B"].audit_session["account_id"], "B")
        self.assertEqual(rt.accounts["A"].audit_session["runtime_session_id"], "RS-A")
        self.assertEqual(rt.accounts["B"].audit_session["runtime_session_id"], "RS-B")

    def test_waiting_user_boundary_survives_model_reload(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.start_runtime_session("RS1")
        cp = rt.create_checkpoint("CP1", scope="AUDIT", account_id="A", objective="screens")
        rt.enter_waiting_user("CP1", "reply done")
        self.assertEqual(cp.status, "WAITING_USER")
        self.assertEqual(cp.pending_user_input, "reply done")
        self.assertEqual(cp.runtime_session_id, "RS1")
        target = DurableTarget()
        rt.resume_checkpoint("CP1", durable_probe=target.probe, apply_action=target.apply)
        self.assertEqual(cp.status, "WAITING_USER")
        self.assertEqual(target.apply_count, {})

    def test_checkpoint_cannot_cross_active_account_even_with_matching_host_ref(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.start_runtime_session("RS-A", host_session_ref="shared-host-ref")
        rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="update", pending_actions=["x"])
        rt.create_account("B")
        rt.start_runtime_session("RS-B", host_session_ref="shared-host-ref")
        with self.assertRaises(RuntimeError):
            rt.resume_checkpoint("CP1", durable_probe=lambda _: False, apply_action=lambda _: None)

    def test_verify_before_replay_does_not_duplicate_successful_write(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="write", pending_actions=["create-record"])
        target = DurableTarget()
        target.applied.add("create-record")
        rt.resume_checkpoint("CP1", durable_probe=target.probe, apply_action=target.apply)
        self.assertEqual(target.apply_count.get("create-record", 0), 0)
        self.assertEqual(rt.checkpoints["CP1"].status, "COMMITTED")

    def test_recovery_applies_only_unverified_actions_once(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.create_checkpoint(
            "CP1",
            scope="ACCOUNT",
            account_id="A",
            objective="write",
            pending_actions=["one", "two"],
        )
        target = DurableTarget()
        target.applied.add("one")
        rt.resume_checkpoint("CP1", durable_probe=target.probe, apply_action=target.apply)
        self.assertEqual(target.apply_count.get("one", 0), 0)
        self.assertEqual(target.apply_count.get("two", 0), 1)
        self.assertEqual(rt.checkpoints["CP1"].status, "COMMITTED")

    def test_checkpoint_loss_cannot_destroy_canonical_facts(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.write_fact("ore", 100)
        rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="noop")
        del rt.checkpoints["CP1"]
        self.assertEqual(rt.accounts["A"].facts["ore"], 100)

    def test_journal_surface_is_append_only_snapshot(self):
        rt = RuntimeModel()
        rt.create_account("A")
        rt.start_runtime_session("RS1")
        rt.create_checkpoint("CP1", scope="ACCOUNT", account_id="A", objective="noop")
        snapshot = rt.journal
        self.assertIsInstance(snapshot, tuple)
        with self.assertRaises(AttributeError):
            snapshot.append("mutate")
        self.assertEqual(len(rt.journal), 1)
        self.assertEqual(rt.journal[0].runtime_session_id, "RS1")

    def test_provider_profiles_and_journal_safety(self):
        self.assertEqual(ProviderCapabilities(read=False).persistence_profile, "NONE")
        self.assertEqual(ProviderCapabilities(read=True).persistence_profile, "READ_ONLY")
        file_rw = ProviderCapabilities(read=True, write=True, create=True)
        self.assertEqual(file_rw.persistence_profile, "FILE_RW")
        self.assertTrue(file_rw.can_authoritative_journal)
        cas = ProviderCapabilities(read=True, write=True, create=True, compare_and_swap=True)
        self.assertEqual(cas.persistence_profile, "CAS_RW")
        transactional = ProviderCapabilities(
            read=True,
            write=True,
            create=True,
            query=True,
            atomic_append=True,
            compare_and_swap=True,
        )
        self.assertEqual(transactional.persistence_profile, "TRANSACTIONAL_RW")
        self.assertTrue(transactional.can_authoritative_journal)


if __name__ == "__main__":
    unittest.main()
