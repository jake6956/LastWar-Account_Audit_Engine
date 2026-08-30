"""Deterministic reference model for LWAI runtime invariants.

This is not the conversational engine. It is an executable state-machine model used by
CI to prove core persistence/account/recovery/migration contracts independently of prompt wording.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Callable


SUPPORTED_SCHEMA_EDGES = {
    "2.1": ("2.2", {"guidance_metadata", "audit_sessions"}),
    "2.2": ("2.3", {"runtime_checkpoints", "runtime_journal"}),
}


def canonicalize_installer_identity(*, alias_version: str | None, canonical_version: str | None, canonical_verified: bool) -> str | None:
    """Canonical GitHub Production wins over alias/cache content."""
    if canonical_verified:
        if canonical_version is None:
            raise ValueError("verified canonical identity requires a version")
        return canonical_version
    return None


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

    @property
    def can_durable_persist(self) -> bool:
        return self.read and (self.write or self.create)


def first_run_persistence_gate(capabilities: ProviderCapabilities, choice: str | None = None) -> str:
    """Resolve the mandatory new-user persistence decision before identity onboarding."""
    if choice is None:
        return "PROMPT_CLOUD_OR_SESSION" if capabilities.can_durable_persist else "PROMPT_CONNECT_OR_SESSION"
    normalized = choice.strip().lower().replace("_", " ")
    if normalized in {"continue session-only", "continue session only", "session-only", "session only"}:
        return "SESSION_ONLY"
    if normalized in {"use cloud storage", "use cloud", "cloud"}:
        if not capabilities.can_durable_persist:
            raise RuntimeError("cloud choice requires verified writable persistence")
        return "CREATE_PRIVATE_WORKSPACE"
    if normalized in {"storage connected", "connected"}:
        return "RECHECK_CAPABILITIES"
    raise ValueError("unrecognized persistence choice")


@dataclass
class Account:
    account_id: str
    status: str = "ACTIVE"
    facts: dict[str, Any] = field(default_factory=dict)
    history: list[tuple[str, Any, Any]] = field(default_factory=list)
    audit_session: dict[str, Any] | None = None


@dataclass(frozen=True)
class RuntimeSession:
    runtime_session_id: str
    account_id: str | None = None
    host_platform: str | None = None
    host_session_ref: str | None = None
    host_session_ref_source: str | None = None


@dataclass
class Checkpoint:
    checkpoint_id: str
    scope: str
    account_id: str | None
    objective: str
    runtime_session_id: str | None = None
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
    runtime_session_id: str | None = None


class RuntimeModel:
    def __init__(self) -> None:
        self.accounts: dict[str, Account] = {}
        self.active_account_id: str | None = None
        self.runtime_sessions: dict[str, RuntimeSession] = {}
        self.current_runtime_session_id: str | None = None
        self.checkpoints: dict[str, Checkpoint] = {}
        self._journal: list[JournalEvent] = []
        self.workspace_schema_version = "2.3"
        self.workspace_optional_structures = {"guidance_metadata", "audit_sessions", "runtime_checkpoints", "runtime_journal"}

    @property
    def journal(self) -> tuple[JournalEvent, ...]:
        return tuple(self._journal)

    def set_workspace_schema(self, version: str, *, optional_structures: set[str] | None = None) -> None:
        self.workspace_schema_version = version
        if optional_structures is not None:
            self.workspace_optional_structures = set(optional_structures)
        elif version == "2.1":
            self.workspace_optional_structures = set()
        elif version == "2.2":
            self.workspace_optional_structures = {"guidance_metadata", "audit_sessions"}
        elif version == "2.3":
            self.workspace_optional_structures = {"guidance_metadata", "audit_sessions", "runtime_checkpoints", "runtime_journal"}
        else:
            self.workspace_optional_structures = set()

    def migrate_workspace_schema(self, target: str = "2.3", *, fail_after_edge: str | None = None) -> list[str]:
        """Apply only validated additive schema edges, atomically from the model's view."""
        if self.workspace_schema_version == target:
            return []
        original = (
            self.workspace_schema_version,
            set(self.workspace_optional_structures),
            deepcopy(self.accounts),
            self.active_account_id,
            deepcopy(self.checkpoints),
            list(self._journal),
        )
        version = self.workspace_schema_version
        structures = set(self.workspace_optional_structures)
        applied: list[str] = []
        try:
            while version != target:
                edge = SUPPORTED_SCHEMA_EDGES.get(version)
                if edge is None:
                    raise RuntimeError(f"no validated workspace migration from {version} to {target}")
                next_version, additions = edge
                structures.update(additions)
                edge_name = f"{version}->{next_version}"
                applied.append(edge_name)
                version = next_version
                if fail_after_edge == edge_name:
                    raise RuntimeError("simulated migration failure")
            self.workspace_schema_version = version
            self.workspace_optional_structures = structures
            return applied
        except Exception:
            (
                self.workspace_schema_version,
                self.workspace_optional_structures,
                self.accounts,
                self.active_account_id,
                self.checkpoints,
                self._journal,
            ) = original
            raise

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
        workspace_schema_version: str | None = None,
        provider_capabilities: ProviderCapabilities | None = None,
        persistence_choice: str | None = None,
    ) -> list[str]:
        if workspace_schema_version is not None:
            self.set_workspace_schema(workspace_schema_version)
        if registry_accounts is not None:
            steps = ["load_registry"]
            for account_id, facts in registry_accounts.items():
                account = self.create_account(account_id, activate=False)
                account.facts = dict(facts)
            if active_account_id is None or active_account_id not in self.accounts:
                raise RuntimeError("current registry requires a valid active_account_id")
            self.active_account_id = active_account_id
            steps.append("resolve_active_account")
            if self.workspace_schema_version != "2.3":
                self.migrate_workspace_schema("2.3")
                steps.append("workspace_schema_migrate")
            steps.extend(["recovery_first", "migration_reconcile"])
            return steps
        if legacy_facts is not None:
            steps = ["legacy_discovery"]
            self.migrate_legacy("legacy", legacy_facts)
            steps.extend(["register_legacy", "resolve_active_account"])
            if self.workspace_schema_version != "2.3":
                self.migrate_workspace_schema("2.3")
                steps.append("workspace_schema_migrate")
            steps.extend(["recovery_first", "migration_reconcile"])
            return steps

        caps = provider_capabilities or ProviderCapabilities(read=False, list=False)
        decision = first_run_persistence_gate(caps, persistence_choice)
        if decision == "PROMPT_CLOUD_OR_SESSION":
            return ["first_run_persistence_prompt_cloud_or_session"]
        if decision == "PROMPT_CONNECT_OR_SESSION":
            return ["first_run_persistence_prompt_connect_or_session"]
        if decision == "RECHECK_CAPABILITIES":
            return ["recheck_storage_capabilities"]
        if decision == "CREATE_PRIVATE_WORKSPACE":
            return ["first_run_persistence_choice", "create_private_workspace", "verify_private_workspace", "new_account_guidance"]
        if decision == "SESSION_ONLY":
            return ["first_run_persistence_choice", "session_only_acknowledged", "new_account_guidance"]
        raise AssertionError("unhandled persistence decision")

    def start_runtime_session(self, runtime_session_id: str, *, host_platform: str | None = None, host_session_ref: str | None = None, host_session_ref_source: str | None = None, account_id: str | None = None) -> RuntimeSession:
        if runtime_session_id in self.runtime_sessions:
            raise ValueError("runtime_session_id must be unique")
        if account_id is None:
            account_id = self.active_account_id
        if account_id is not None and account_id not in self.accounts:
            raise ValueError("runtime session account_id must reference an existing account")
        session = RuntimeSession(runtime_session_id, account_id, host_platform, host_session_ref, host_session_ref_source)
        self.runtime_sessions[runtime_session_id] = session
        self.current_runtime_session_id = runtime_session_id
        return session

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
        self.accounts[account_id].status = "ACTIVE"

    def start_audit_session(self, session_id: str) -> None:
        if self.active_account_id is None:
            raise RuntimeError("active account required")
        self.accounts[self.active_account_id].audit_session = {"session_id": session_id, "account_id": self.active_account_id, "runtime_session_id": self.current_runtime_session_id, "status": "OPEN"}

    def create_checkpoint(self, checkpoint_id: str, *, scope: str, objective: str, account_id: str | None = None, pending_actions: list[str] | None = None) -> Checkpoint:
        if checkpoint_id in self.checkpoints:
            raise ValueError("checkpoint already exists")
        cp = Checkpoint(checkpoint_id, scope, account_id, objective, self.current_runtime_session_id, pending_actions=list(pending_actions or []))
        self.checkpoints[checkpoint_id] = cp
        self.append_journal(checkpoint_id, "BEGIN", "checkpoint", verified=True)
        return cp

    def enter_waiting_user(self, checkpoint_id: str, boundary: str) -> None:
        cp = self.checkpoints[checkpoint_id]
        self._assert_checkpoint_scope(cp)
        cp.status = "WAITING_USER"
        cp.pending_user_input = boundary
        self.append_journal(checkpoint_id, "WAITING_USER", boundary, verified=True)

    def append_journal(self, checkpoint_id: str, event_type: str, action: str, *, verified: bool, safe_point_after: str | None = None) -> JournalEvent:
        checkpoint = self.checkpoints.get(checkpoint_id)
        event = JournalEvent(f"J{len(self._journal)+1}", checkpoint_id, event_type, action, verified, safe_point_after, checkpoint.runtime_session_id if checkpoint else self.current_runtime_session_id)
        self._journal.append(event)
        return event

    def resume_checkpoint(self, checkpoint_id: str, *, durable_probe: Callable[[str], bool], apply_action: Callable[[str], None]) -> None:
        cp = self.checkpoints[checkpoint_id]
        self._assert_checkpoint_scope(cp)
        if cp.status in {"WAITING_USER", "COMMITTED"}:
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
            self.append_journal(checkpoint_id, "WRITE_SUCCESS", action, verified=True, safe_point_after=action)
        cp.pending_actions = remaining
        if not cp.pending_actions:
            cp.status = "COMMITTED"
            self.append_journal(checkpoint_id, "COMMIT", "checkpoint", verified=True)

    def _assert_checkpoint_scope(self, cp: Checkpoint) -> None:
        if cp.account_id is not None and cp.account_id != self.active_account_id:
            raise RuntimeError("account-scoped checkpoint cannot cross active_account_id")
