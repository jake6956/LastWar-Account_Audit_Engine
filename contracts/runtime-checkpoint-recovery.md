# Runtime Checkpoint & Transaction Recovery Contract

Release: 2026-08-29.11  
Scope: generic sanitized engine behavior only  
Account state included: no

## Purpose

LWAI treats conversation context as volatile cache. Canonical account data remains authoritative durable state. Runtime Checkpoints add compact workflow-position persistence for bounded operations whose interruption would otherwise be ambiguous; Runtime Journal adds append-only write-ahead/event history. Neither is a transcript store or substitute account database.

## Runtime Checkpoints

Minimum provider-neutral fields: `checkpoint_id`, `scope`, nullable `account_id`, `objective`, `current_phase`, `status`, `last_safe_point`, `completed_actions`, `pending_actions`, `pending_user_input`, `active_modules`, `affected_artifacts`, `important_assumptions`, `resume_instruction`, `started_at`, `updated_at`, `owner_context`, `notes`.

Statuses are `OPEN`, `WAITING_USER`, `COMMITTED`, `ABORTED`, and `RECOVERY_REQUIRED`.

Account-scoped checkpoints require `account_id` and may never silently resume under another `active_account_id`. Workspace/global checkpoints may omit account_id only when the workflow is genuinely account-independent.

## Runtime Journal

The Runtime Journal is append-only in normal operation. Minimum fields: `journal_id`, `checkpoint_id`, `timestamp`, `event_type`, `scope`, nullable `account_id`, `artifact`, `action`, `result`, `verified`, `safe_point_after`, `next_action`, `error_or_blocker`, `notes`.

Recommended events include `BEGIN`, `INTENT`, `WRITE_ATTEMPT`, `WRITE_SUCCESS`, `WRITE_FAILURE`, `VERIFY`, `SAFE_POINT`, `WAITING_USER`, `RESUME`, `COMMIT`, and `ABORT`.

## Recovery-first startup

Recovery uses a strict **verify-before-replay** invariant. After mandatory core and Workspace Registry are available, resolve `active_account_id`, inspect unresolved checkpoints and related recent journal entries, then inspect their actual durable artifacts. Verified durable state outranks stale checkpoint claims. Do not replay verified successful writes. Resume at the first unverified or pending action. Mark `COMMITTED` only after the intended durable end state is verified.

Creation retries must first verify an equivalent object does not already exist. Updates compare the current durable value/version before replacement. A lost checkpoint store may reduce recovery convenience but must never destroy canonical account facts.

## WAITING_USER

Declared multi-upload boundaries such as `reply done` survive reload when durable checkpointing exists. Context loss is never implicit batch completion. Checkpoints store only concise pending-input state; detailed audit evidence remains in the account-scoped Audit Session/canonical evidence stores.

## Privacy and context budget

Actual consumer checkpoint/journal rows, account identities, screenshots, provider-local IDs/paths, and user-specific pending actions are private deployment state and are never published to shared Production. Never persist hidden chain-of-thought, raw internal reasoning, full chat transcripts, or duplicated evidence blobs. Store only operational facts needed for safe recovery.

## Provider fallbacks

Structured writable storage should use workspace-level checkpoint/journal tables or collections. Writable file-only storage may use a checkpoint index plus append-only JSONL/NDJSON or timestamped records. Read-only/no durable storage uses best-effort conversational recovery only and must not claim disk durability.

## Release transactions

Engine releases use workspace/global checkpoints when durable persistence exists. Journal private RC staging, GitHub RC creation, candidate identity, exact-head CI, merge, post-merge verification, installer verification, and private archive/release-record synchronization. Interrupted pre-merge releases preserve last-known-good Production. Secondary mirror/archive failures after a validated merge are recorded as pending recovery rather than rolling back healthy main automatically.
