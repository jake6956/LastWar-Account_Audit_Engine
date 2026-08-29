# Provider-Neutral LWAI Workspace Schema

Version: 2026-08-29.11

A writable deployment should preserve workspace-level account routing, compact workflow-recovery state, and isolated logical equivalents of every account-local domain below, even if a provider maps them onto different physical file types. The 2026-08-29.11 schema change is additive and backward-compatible: Runtime Checkpoints and Runtime Journal are optional durable operational stores; they do not replace or duplicate canonical account databases.

## Workspace-level state

| Domain | Minimum fields |
|---|---|
| Account Registry | account_id, nickname, optional_private_game_uid, uid_suffix, screenname, alliance, server, active, status, guidance_level_optional, active_audit_session_id_optional, last_identity_confirmed, last_updated, database_provider, database_artifact_id_or_path, database_artifact_title, notes |
| Workspace Metadata | workspace_schema_version, active_account_id, account_discovery_policy, provider_adapter, privacy_policy, guidance_level_optional, engine_version, last_engine_refresh |
| Shared Engine Metadata | module_manifest_version, installed_module_versions, upstream_endpoints, fallback_version, health_status |
| Shared Artifact Registry | artifact_id, class, environment, canonical, public, format, update_trigger, source, retention, notes |
| Runtime Checkpoints (optional) | checkpoint_id, scope, account_id_nullable, objective, current_phase, status, last_safe_point, completed_actions, pending_actions, pending_user_input, active_modules, affected_artifacts, important_assumptions, resume_instruction, started_at, updated_at, owner_context, notes |
| Runtime Journal (optional, append-only) | journal_id, checkpoint_id, timestamp, event_type, scope, account_id_nullable, artifact, action, result, verified, safe_point_after, next_action, error_or_blocker, notes |

`account_id` is an immutable LWAI-generated primary key. UID is optional/private recognition metadata and must never be required for account creation or copied into shared Production. Guidance proficiency may be NEW, LEARNING, COMFORTABLE or EXPERT and never relaxes privacy/evidence/batch/isolation rules.

Runtime Checkpoints/Journal are private deployment state and may contain local account IDs, provider references or pending-user status. Shared GitHub Production contains this schema only, never actual consumer rows.

## Runtime Checkpoint rules
- Supported scopes include ACCOUNT, AUDIT, ENGINE_RELEASE, MIGRATION, MAINTENANCE, IMPORT and PROVIDER_SETUP; implementations may add bounded provider-specific scopes.
- `account_id` is mandatory for account-scoped checkpoints and nullable only for true workspace/global work.
- Valid statuses: OPEN, WAITING_USER, COMMITTED, ABORTED, RECOVERY_REQUIRED.
- `last_safe_point` advances only after material durable state is verified enough to make replay safe.
- Before replay, inspect affected durable artifacts; verified durable state outranks stale checkpoint claims.
- Do not replay verified successful writes. Create operations verify equivalent objects do not already exist; updates compare current durable value/version before replacement.
- COMMITTED means intended durable end state was verified, not merely that a tool call returned success.
- Checkpoint deletion/loss may reduce recovery convenience but must never destroy canonical account facts.
- Do not store hidden chain-of-thought, raw reasoning, full transcripts or duplicated evidence blobs.

## Runtime Journal rules
- Append-only during normal operation. Never rewrite prior events to make history look cleaner.
- Recommended event types: BEGIN, INTENT, WRITE_ATTEMPT, WRITE_SUCCESS, WRITE_FAILURE, VERIFY, SAFE_POINT, WAITING_USER, RESUME, COMMIT, ABORT.
- Each event records the result/verification state and the next safe action.
- For providers with atomic transactions, use them; the journal still records application-level workflow boundaries when interruption matters.

## Provider mappings
- Structured writable storage: workspace-level Runtime Checkpoints and Runtime Journal tables/sheets/collections.
- Writable file-only storage: checkpoint index plus append-only JSONL/NDJSON or timestamped JSON/Markdown journal records.
- Read-only/no durable storage: best-effort compact session checkpoint only; never claim disk durability.

## Account-local state

Every managed account has an isolated canonical database/logical namespace. Mutable rows, Audit Sessions and account-scoped checkpoint work from one account must never be applied to another implicitly.

| Domain | Minimum fields |
|---|---|
| Account Identity | account_id, nickname, game_uid_optional_private, uid_suffix, screenname, alliance, server, last_identity_confirmed, updated, source, confidence, notes |
| Dashboard | metric, value, updated, freshness, confidence, note |
| Heroes | hero, class, stars, level, role, power, skills, EW, WoH, updated, source, confidence, notes |
| Gear Pool | gear_id, type, level, mythic_state, stars, segments, effects, current_wearer, preset_uses, next_breakpoint, next_cost, updated, source, confidence |
| Presets | preset, squad_slot, unit_type, power, front_left, front_right, back_left, back_center, back_right, gear_profile, purpose, updated, source, confidence |
| Tech | tree, node, current_level, max_level, effect, prerequisites, cost_time, combat_scope, updated, source, confidence |
| Research Queue | tech_center, current_research, target_path, ETA, strategic_lane, updated |
| Resources | resource, current_amount, reserved_amount, current_target, breakpoint_cost_remaining, updated, source, confidence |
| Drone | subsystem, item, level_stars_progress, effect, unit_type, target, updated, source, confidence |
| Decorations | item, level, effect, next_breakpoint, cost_priority, updated, source, confidence |
| Profession | path, skill, level, effect, priority, updated, source, confidence |
| Overlord/Season Systems | system, item_node, state, next_breakpoint, cost, priority, updated, source, confidence |
| Battle Log | date, mode, attacker_defender, own_preset, opponent_type, own_power, opponent_power, result, formation, first_death, damage_summary, notable_enemy_state, notes |
| Change Log | timestamp, domain, key, old_value, new_value, source, confidence, reason |
| Corrections | invariant_or_regression_rule, status, source, date_added, notes |
| Mechanics Observations | mechanic, current_belief, source_type, reference, last_verified, confidence, volatility, notes |
| Hot Cache | key, current_value, domain, freshness_class, updated, source, confidence, dependent_targets, status |
| State Health | domain_key, health_status, issue_type, last_checked, required_action, blocking_level, notes |
| Staleness Policy | data_class, freshness_guideline, stale_behavior, refresh_method, notes |
| Preferences | key, value, updated, source, notes |
| Audit Sessions (optional) | session_id, account_id, audit_type, domain, requested_items, completed_items, pending_items, ambiguous_items, current_step, started_at, updated_at, ingestion_mode, guidance_level, status, notes |
| Snapshots | dated recovery artifact references |
| Assets | screenshots/report references, account_id, captured_at, source, notes |

## Audit Session rules
- Audit Sessions are optional, resumable and always account-scoped.
- Resolve `active_account_id` before resuming/mutating one.
- Valid status values are ACTIVE, PAUSED, COMPLETE and ABANDONED.
- Recommended ingestion modes: direct_batch, document_bundle, guided_capture.
- Batch completion records declared boundaries such as `done`; declared multi-upload batches do not finalize early.
- Audit Sessions track detailed requested/completed evidence; Runtime Checkpoints should only reference surrounding safe-point state when recovery matters.

## Recovery-first startup
- Load mandatory core and Workspace Registry.
- Resolve `active_account_id`.
- Inspect unresolved Runtime Checkpoints and recent related Runtime Journal events before ordinary continuation.
- For each relevant OPEN/WAITING_USER/RECOVERY_REQUIRED checkpoint, inspect actual affected durable artifacts and verify what committed.
- Preserve WAITING_USER/`done` boundaries across reload.
- Never resume an account-scoped checkpoint under another active_account_id.
- Resume at the first unverified/pending action; mark COMMITTED only after intended durable end state is verified.

## Migration-first startup rules
- Discover Workspace Registry and accessible prior LWAI state before broad onboarding.
- Reuse/import supported confirmed current facts with source/confidence/freshness preserved.
- Ask only for missing, ambiguous, contradictory or materially stale information.
- Persist migrated/validated state immediately when writable storage exists.
- Never claim access to unrelated prior conversations that are not actually available.

## Account routing and archive rules
- Resolve `active_account_id` before mutable account transactions and account-scoped checkpoint recovery.
- A context switch flushes pending canonical changes/Audit Session progress, records or safely pauses relevant checkpoint work, clears account-scoped cache, sets active_account_id, then loads target state.
- Cross-account comparisons are read-only and preserve prior active_account_id unless explicitly switched.
- `start over` creates a new account_id/namespace and archives old registry entry by default; it does not delete history implicitly.
- Archive is reversible and preserves immutable account_id/history.

## Data rules
- Canonical/observed state and derived recommendations are separate.
- Consequential canonical facts carry source/confidence.
- Monotonic stale values become `minimum_known`; volatile values become stale aggressively.
- Corrections persist until explicitly revoked within their account.
- Change Log is append-oriented; cache eviction never destroys history.
- IDs/timestamps survive provider migration.
- Engine updates preserve Account Registry, active_account_id, Account Identity records, all account-local namespaces, Audit Sessions, Runtime Checkpoints, Runtime Journal and provider-local references.
- Shared GitHub Production/public Gold Assets contain schemas/rules only, never consumer identity/evidence/checkpoint rows.
