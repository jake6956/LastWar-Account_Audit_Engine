"""Deterministic reference model for LWAI runtime invariants.

This is not the conversational engine. It is an executable state-machine model used by
CI to prove core persistence/account/recovery contracts independently of prompt wording.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class ProviderCapabilities:
    read: bool = True
    list: bool = True
    write: bool = False
    create: bool = False
    query: bool = False
    atomic_append: bool = False
    compare_and_swap: bool = False
    snapshot: bool = False
    restore: bool = False

    @property
    def persistence_profile(self) -> str:
        if not self.read:
            return "NONE"
        if not self.write and not self.create:
            return "READ_ONLY"
        if self.atomic_append and self.compare_and_swap and self.query:
            return "TRANSACTIONAL_RW"
        if self.query:
            return "STRUCTURED_RW"
        if self.compare_and_swap:
            return "CAS_RW"
        return "FILE_RW"

    @property
    def can_authoritative_journal(self) -> bool:
        return self.atomic_append or self.compare_and_swap or self.create


@dataclass
class Account:
    account_id: str
    status: str = "ACTIVE"
    facts: dict[str, Any] = field(default_factory=dict)
    history: list[tuple[str, Any, Any]] = field(default_factory=list)
    audit_session: dict[str, Any] | None = None


@dataclass
class Checkpoint:
    checkpoint_id: str
    scope: str
    account_id: str | None
    objective: str
    status: str = "OPEN"
    last_safe_point: str | None = None
    completed_actions: list[str] = field(default_factory=list)
    pending_actions: list[str] = field(default_factory=list)
    pending_user_input: str | None = None


@dataclass(frozen=True)
class JournalEvent:
    journal_id: str
    checkpoint_id: str
    event_type: str
    action: str
    verified: bool
    safe_point_after: str | None = None


class RuntimeModel:
    def __init__(self) -> None:
        self.accounts: dict[str, Account] = {}
        self.active_account_id: str | None = None
        self.checkpoints: dict[str, Checkpoint] = {}
        self._journal: list[JournalEvent] = []

    @property
    def journal(self) -> tuple[JournalEvent, ...]:
        return tuple(self._journal)

    def create_account(self, account_id: str, *, activate: bool = True) -> Account:
        if account_id in self.accounts:
            raise ValueError("account_id is immutable and unique")
        account = Account(account_id=account_id)
        self.accounts[account_id] = account
        if activate:
            self.active_account_id = account_id
        return account

    def migrate_legacy(self, account_id: str, legacy_facts: dict[str, Any]) -> Account:
        account = self.create_account(account_id)
        account.facts = dict(legacy_facts)
        return account

    def startup_from_storage(
        self,
        *,
        registry_accounts: dict[str, dict[str, Any]] | None = None,
        active_account_id: str | None = None,
        legacy_facts: dict[str, Any] | None = None,
    ) -> list[str]:
        """Return the durable startup sequence while enforcing legacy-first bootstrap.

        A current registry permits active-account resolution before recovery. A legacy
        pre-registry account must first be discovered and registered so an immutable
        account_id/active_account_id actually exists; only then may recovery run.
        """
        if registry_accounts is not None:
            steps = ["load_registry"]
            for account_id, facts in registry_accounts.items():
                account = self.create_account(account_id, activate=False)
                account.facts = dict(facts)
            if active_account_id is None or active_account_id not in self.accounts:
                raise RuntimeError("current registry requires a valid active_account_id")
            self.active_account_id = active_account_id
            steps.extend(["resolve_active_account", "recovery_first", "migration_reconcile"])
            return steps

        if legacy_facts is not None:
            steps = ["legacy_discovery"]
            self.migrate_legacy("legacy", legacy_facts)
            steps.extend(["register_legacy", "resolve_active_account", "recovery_first", "migration_reconcile"])
            return steps

        return ["new_account_guidance"]

    def switch_account(self, account_id: str) -> None:
        account = self.accounts.get(account_id)
        if account is None or account.status == "ARCHIVED":
            raise ValueError("target account is unavailable")
        self.active_account_id = account_id

    def write_fact(self, key: str, value: Any) -> None:
        if self.active_account_id is None:
            raise RuntimeError("active_account_id must resolve before mutation")
        account = self.accounts[self.active_account_id]
        old = account.facts.get(key)
        account.facts[key] = value
        account.history.append((key, old, value))

    def start_over(self, new_account_id: str) -> Account:
        if self.active_account_id is not None:
            self.accounts[self.active_account_id].status = "ARCHIVED"
        return self.create_account(new_account_id)

    def restore_account(self, account_id: str) -> None:
        account = self.accounts[account_id]
        account.status = "ACTIVE"

    def start_audit_session(self, session_id: str) -> None:
        if self.active_account_id is None:
            raise RuntimeError("active account required")
        self.accounts[self.active_account_id].audit_session = {
            "session_id": session_id,
            "account_id": self.active_account_id,
            "status": "OPEN",
        }

    def create_checkpoint(
        self,
        checkpoint_id: str,
        *,
        scope: str,
        objective: str,
        account_id: str | None = None,
        pending_actions: list[str] | None = None,
    ) -> Checkpoint:
        if checkpoint_id in self.checkpoints:
            raise ValueError("checkpoint already exists")
        cp = Checkpoint(
            checkpoint_id=checkpoint_id,
            scope=scope,
            account_id=account_id,
            objective=objective,
            pending_actions=list(pending_actions or []),
        )
        self.checkpoints[checkpoint_id] = cp
        self.append_journal(checkpoint_id, "BEGIN", "checkpoint", verified=True)
        return cp

    def enter_waiting_user(self, checkpoint_id: str, boundary: str) -> None:
        cp = self.checkpoints[checkpoint_id]
        self._assert_checkpoint_scope(cp)
        cp.status = "WAITING_USER"
        cp.pending_user_input = boundary
        self.append_journal(checkpoint_id, "WAITING_USER", boundary, verified=True)

    def append_journal(
        self,
        checkpoint_id: str,
        event_type: str,
        action: str,
        *,
        verified: bool,
        safe_point_after: str | None = None,
    ) -> JournalEvent:
        event = JournalEvent(
            journal_id=f"J{len(self._journal)+1}",
            checkpoint_id=checkpoint_id,
            event_type=event_type,
            action=action,
            verified=verified,
            safe_point_after=safe_point_after,
        )
        self._journal.append(event)
        return event

    def resume_checkpoint(
        self,
        checkpoint_id: str,
        *,
        durable_probe: Callable[[str], bool],
        apply_action: Callable[[str], None],
    ) -> None:
        cp = self.checkpoints[checkpoint_id]
        self._assert_checkpoint_scope(cp)
        if cp.status == "WAITING_USER":
            return

        remaining: list[str] = []
        for action in cp.pending_actions:
            if durable_probe(action):
                if action not in cp.completed_actions:
                    cp.completed_actions.append(action)
                self.append_journal(checkpoint_id, "VERIFY", action, verified=True)
                continue
            try:
                apply_action(action)
            except Exception:
                cp.status = "RECOVERY_REQUIRED"
                remaining.append(action)
                self.append_journal(checkpoint_id, "WRITE_FAILURE", action, verified=False)
                remaining.extend(a for a in cp.pending_actions if a not in cp.completed_actions and a != action)
                cp.pending_actions = list(dict.fromkeys(remaining))
                return
            if not durable_probe(action):
                cp.status = "RECOVERY_REQUIRED"
                remaining.append(action)
                self.append_journal(checkpoint_id, "VERIFY", action, verified=False)
                continue
            cp.completed_actions.append(action)
            cp.last_safe_point = action
            self.append_journal(
                checkpoint_id,
                "WRITE_SUCCESS",
                action,
                verified=True,
                safe_point_after=action,
            )

        cp.pending_actions = remaining
        if not cp.pending_actions:
            cp.status = "COMMITTED"
            self.append_journal(checkpoint_id, "COMMIT", "checkpoint", verified=True)

    def _assert_checkpoint_scope(self, cp: Checkpoint) -> None:
        if cp.account_id is not None and cp.account_id != self.active_account_id:
            raise RuntimeError("account-scoped checkpoint cannot cross active_account_id")
