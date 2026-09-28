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
ENGINE_FRESHNESS_TTL_HOURS = 6
PERSISTENCE_REMINDER_COOLDOWN_DAYS = 7


def _engine_version_key(value: str) -> tuple[int, ...]:
    date_part, release_part = value.rsplit(".", 1)
    year, month, day = (int(x) for x in date_part.split("-"))
    return year, month, day, int(release_part)


def canonicalize_installer_identity(*, alias_version: str | None, canonical_version: str | None, canonical_verified: bool) -> str | None:
    """Canonical GitHub Production wins over alias/cache content."""
    if canonical_verified:
        if canonical_version is None:
            raise ValueError("verified canonical identity requires a version")
        return canonical_version
    return None


def installer_version_announcement(*, alias_version: str | None, canonical_version: str | None, canonical_verified: bool) -> str | None:
    """Only the verified canonical version is announced as active; alias versions stay diagnostic."""
    canonical = canonicalize_installer_identity(
        alias_version=alias_version,
        canonical_version=canonical_version,
        canonical_verified=canonical_verified,
    )
    return None if canonical is None else f"Verified Production {canonical}"


def should_check_engine_freshness(*, web_available: bool, startup: bool, hours_since_last_success: float | None) -> bool:
    """Check canonical GitHub on every runtime startup and every six hours in long-lived runtimes."""
    if not web_available:
        return False
    if startup:
        return True
    if hours_since_last_success is None:
        return True
    return hours_since_last_success >= ENGINE_FRESHNESS_TTL_HOURS


def resolve_engine_version(
    *,
    current_version: str,
    canonical_version: str | None,
    canonical_verified: bool,
    canonical_channel: str = "Production",
) -> str:
    """Adopt only a newer verified Production version; otherwise preserve last-known-good."""
    if not canonical_verified or canonical_channel != "Production" or canonical_version is None:
        return current_version
    if _engine_version_key(canonical_version) > _engine_version_key(current_version):
        return canonical_version
    return current_version


def should_offer_persistence_reminder(
    *,
    session_only: bool,
    material_benefit: bool,
    reminded_this_runtime: bool,
    do_not_ask_again: bool,
    days_since_last_reminder: int | None = None,
) -> bool:
    """Contextual cloud reminder gate; never a generic timer-driven nag."""
    if not session_only or not material_benefit or reminded_this_runtime or do_not_ask_again:
        return False
    if days_since_last_reminder is not None and days_since_last_reminder < PERSISTENCE_REMINDER_COOLDOWN_DAYS:
        return False
    return True


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
    fact_metadata: dict[str, dict[str, Any]] = field(default_factory=dict)
    history: list[tuple[str, Any, Any]] = field(default_factory=list)
    hot_cache: dict[str, Any] = field(default_factory=dict)
    state_health: dict[str, dict[str, Any]] = field(default_factory=dict)
    last_updated: str | None = None
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
        self.persistence_mode = "UNKNOWN"
        self.persistence_reminders_suppressed = False
        self._persistence_reminded_sessions: set[str] = set()
        self.persistence_last_reminder_day: int | None = None
        self.workspace_last_updated: str | None = None
        self._ingestion_counter = 0

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
            self.persistence_mode = "DURABLE"
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
            self.persistence_mode = "DURABLE"
            return ["first_run_persistence_choice", "create_private_workspace", "verify_private_workspace", "new_account_guidance"]
        if decision == "SESSION_ONLY":
            self.persistence_mode = "SESSION_ONLY"
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

    def consider_persistence_reminder(self, *, material_benefit: bool, day: int | None = None) -> bool:
        runtime_id = self.current_runtime_session_id or "volatile-runtime"
        reminded = runtime_id in self._persistence_reminded_sessions
        days_since = None
        if day is not None and self.persistence_last_reminder_day is not None:
            days_since = day - self.persistence_last_reminder_day
        eligible = should_offer_persistence_reminder(
            session_only=self.persistence_mode == "SESSION_ONLY",
            material_benefit=material_benefit,
            reminded_this_runtime=reminded,
            do_not_ask_again=self.persistence_reminders_suppressed,
            days_since_last_reminder=days_since,
        )
        if eligible:
            self._persistence_reminded_sessions.add(runtime_id)
            if day is not None:
                self.persistence_last_reminder_day = day
        return eligible

    def record_persistence_reminder_response(self, response: str) -> None:
        normalized = response.strip().lower()
        if normalized in {"don't ask again", "do not ask again", "never ask again"}:
            self.persistence_reminders_suppressed = True

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

    def ingest_direct_evidence(
        self,
        observations: list[dict[str, Any]],
        *,
        observed_at: str,
        source: str = "direct",
        task_keys: set[str] | None = None,
        fail_after: str | None = None,
    ) -> dict[str, Any]:
        """Harvest every clear supported fact; task relevance never filters persistence."""
        if self.active_account_id is None:
            raise RuntimeError("active_account_id must resolve before evidence ingestion")
        account = self.accounts[self.active_account_id]
        accepted: list[dict[str, Any]] = []
        skipped: list[str] = []
        for raw in observations:
            key = raw.get("key")
            if not raw.get("supported", True) or raw.get("ambiguous", False) or raw.get("decorative", False) or not key:
                skipped.append(key or "<ambiguous>")
                continue
            value = raw.get("value")
            prior_meta = account.fact_metadata.get(key, {})
            if (
                account.facts.get(key) == value
                and prior_meta.get("observed_at") == observed_at
                and prior_meta.get("source") == source
                and prior_meta.get("confidence") == raw.get("confidence", "HIGH")
            ):
                skipped.append(key)
                continue
            accepted.append({
                "key": key,
                "value": value,
                "state_class": raw.get("state_class", "MONOTONIC"),
                "confidence": raw.get("confidence", "HIGH"),
            })

        # task_keys affects answer focus only, never the durable fact set.
        _ = task_keys
        if not accepted:
            return {"committed": True, "persisted_keys": [], "skipped_keys": skipped, "checkpoint_id": None}

        durable = self.persistence_mode == "DURABLE"
        checkpoint = None
        surfaces = ["canonical", "history", "hot_cache", "state_health", "metadata", "verify"]
        if durable:
            self._ingestion_counter += 1
            checkpoint = self.create_checkpoint(
                f"INGEST-{self._ingestion_counter}",
                scope="ACCOUNT",
                account_id=self.active_account_id,
                objective="direct evidence durable commit",
                pending_actions=list(surfaces),
            )
            self.append_journal(checkpoint.checkpoint_id, "INTENT", "persist direct evidence transaction", verified=True)

        def record_surface(surface: str) -> None:
            if checkpoint is not None:
                checkpoint.completed_actions.append(surface)
                checkpoint.pending_actions = [x for x in surfaces if x not in checkpoint.completed_actions]
                self.append_journal(checkpoint.checkpoint_id, "WRITE_SUCCESS", surface, verified=False)

        def fail(surface: str) -> None:
            if fail_after != surface:
                return
            if checkpoint is not None:
                checkpoint.status = "RECOVERY_REQUIRED"
                checkpoint.pending_actions = [x for x in surfaces if x not in checkpoint.completed_actions]
                self.append_journal(checkpoint.checkpoint_id, "WRITE_FAILURE", surface, verified=False)
            raise RuntimeError(f"simulated evidence transaction failure after {surface}")

        old_values = {item["key"]: account.facts.get(item["key"]) for item in accepted}
        for item in accepted:
            key = item["key"]
            account.facts[key] = item["value"]
            account.fact_metadata[key] = {
                "state_class": item["state_class"],
                "observed_at": observed_at,
                "source": source,
                "confidence": item["confidence"],
            }
        record_surface("canonical")
        fail("canonical")

        for item in accepted:
            key = item["key"]
            if old_values[key] != item["value"]:
                account.history.append((key, old_values[key], item["value"]))
        record_surface("history")
        fail("history")

        for item in accepted:
            account.hot_cache[item["key"]] = item["value"]
        record_surface("hot_cache")
        fail("hot_cache")

        for item in accepted:
            account.state_health[item["key"]] = {
                "health_status": "CURRENT",
                "last_checked": observed_at,
                "source": source,
            }
        record_surface("state_health")
        fail("state_health")

        account.last_updated = observed_at
        self.workspace_last_updated = observed_at
        record_surface("metadata")
        fail("metadata")

        coherent = all(
            account.facts[item["key"]] == item["value"]
            and account.hot_cache.get(item["key"]) == item["value"]
            and account.state_health.get(item["key"], {}).get("health_status") == "CURRENT"
            and account.fact_metadata.get(item["key"], {}).get("observed_at") == observed_at
            for item in accepted
        )
        if not coherent or fail_after == "verify":
            if checkpoint is not None:
                checkpoint.status = "RECOVERY_REQUIRED"
                checkpoint.pending_actions = ["verify"]
                self.append_journal(checkpoint.checkpoint_id, "VERIFY", "direct evidence transaction", verified=False)
            raise RuntimeError("direct evidence durable verification failed")

        if checkpoint is not None:
            checkpoint.completed_actions.append("verify")
            checkpoint.pending_actions = []
            checkpoint.last_safe_point = "verified evidence commit"
            checkpoint.status = "COMMITTED"
            self.append_journal(checkpoint.checkpoint_id, "VERIFY", "direct evidence transaction", verified=True, safe_point_after=checkpoint.last_safe_point)
            self.append_journal(checkpoint.checkpoint_id, "COMMIT", "direct evidence transaction", verified=True, safe_point_after=checkpoint.last_safe_point)

        return {
            "committed": True,
            "persisted_keys": [item["key"] for item in accepted],
            "skipped_keys": skipped,
            "checkpoint_id": checkpoint.checkpoint_id if checkpoint else None,
        }

    def durable_account_snapshot(self, account_id: str | None = None) -> dict[str, Any]:
        account_id = account_id or self.active_account_id
        if account_id is None or account_id not in self.accounts:
            raise RuntimeError("account snapshot requires a valid account")
        account = self.accounts[account_id]
        return {
            "account_id": account.account_id,
            "status": account.status,
            "facts": deepcopy(account.facts),
            "fact_metadata": deepcopy(account.fact_metadata),
            "history": deepcopy(account.history),
            "hot_cache": deepcopy(account.hot_cache),
            "state_health": deepcopy(account.state_health),
            "last_updated": account.last_updated,
            "workspace_last_updated": self.workspace_last_updated,
        }

    def load_durable_account_snapshot(self, snapshot: dict[str, Any], *, activate: bool = True) -> Account:
        account = self.create_account(snapshot["account_id"], activate=activate)
        account.status = snapshot.get("status", "ACTIVE")
        account.facts = deepcopy(snapshot.get("facts", {}))
        account.fact_metadata = deepcopy(snapshot.get("fact_metadata", {}))
        account.history = deepcopy(snapshot.get("history", []))
        account.hot_cache = deepcopy(snapshot.get("hot_cache", {}))
        account.state_health = deepcopy(snapshot.get("state_health", {}))
        account.last_updated = snapshot.get("last_updated")
        self.workspace_last_updated = snapshot.get("workspace_last_updated")
        self.persistence_mode = "DURABLE"
        return account

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
