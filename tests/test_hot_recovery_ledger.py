import sys
import unittest
from pathlib import Path
from datetime import datetime, timedelta, timezone
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from continuity_ledger import project_recovery
NOW = datetime(2026, 11, 20, tzinfo=timezone.utc)


def event(eid, hours_ago, account=None, cp=None, verified=True):
    return dict(event_id=eid, occurred_at=(NOW-timedelta(hours=hours_ago)).isoformat(),
                scope="ACCOUNT" if account else "WORKSPACE", account_id=account,
                checkpoint_id=cp, event_type="VERIFY" if verified else "INTENT",
                action="operation", result="ok" if verified else "planned",
                verified=verified, evidence_ref="test", next_action="continue")


class HotRecoveryLedgerTests(unittest.TestCase):
    def test_ttl_and_pinned_open(self):
        cps = [dict(checkpoint_id="cp", scope="WORKSPACE", status="RECOVERY_REQUIRED")]
        view = project_recovery([event("old", 73),event("new", 2),event("pinned", 200, cp="cp")], cps, now=NOW)
        self.assertEqual({e["event_id"] for e in view["recent_events"]}, {"new","pinned"})
        self.assertEqual(len(view["open_checkpoints"]), 1)

    def test_terminal_work_does_not_pin(self):
        cps = [dict(checkpoint_id="cp", scope="WORKSPACE", status="COMMITTED")]
        self.assertFalse(project_recovery([event("old", 100, cp="cp")], cps, now=NOW)["recent_events"])

    def test_account_isolation(self):
        cps = [dict(checkpoint_id="a", scope="ACCOUNT", account_id="A", status="OPEN"),
               dict(checkpoint_id="b", scope="ACCOUNT", account_id="B", status="WAITING_USER")]
        view=project_recovery([event("a",1,"A"),event("b",1,"B"),event("w",1)],cps,active_account_id="A",now=NOW)
        self.assertEqual({e["event_id"] for e in view["recent_events"]},{"a","w"})
        self.assertEqual([c["checkpoint_id"] for c in view["open_checkpoints"]],["a"])

    def test_missing_account_id_fail_closed(self):
        bad=event("a",1,"A");bad.pop("account_id")
        with self.assertRaises(ValueError): project_recovery([bad],[],active_account_id="A",now=NOW)

    def test_conflicting_duplicate_fail_closed(self):
        e=event("x",1)
        with self.assertRaises(ValueError): project_recovery([e,{**e,"result":"other"}],[],now=NOW)

    def test_intent_is_not_verified(self):
        view=project_recovery([event("intent",1,verified=False)],[],now=NOW)
        self.assertFalse(view["recent_events"][0]["verified"])

    def test_bounded(self):
        view=project_recovery([event(str(i),1) for i in range(40)],[],now=NOW)
        self.assertEqual(len(view["recent_events"]),32)

    def test_module_compiled_parity(self):
        core=(ROOT/"engine/modules/core/persistence.txt").read_text()
        compiled=(ROOT/"engine/BOOTSTRAP_FULL.txt").read_text()
        for marker in ("HOT RECOVERY LEDGER","72","catch up"):
            self.assertIn(marker,core)
            self.assertIn(marker,compiled)


if __name__ == "__main__": unittest.main()
