# Provider-Neutral LWAI Workspace Schema

Version: 2026-08-29.10

A writable deployment should preserve workspace-level account routing plus isolated logical equivalents of every account-local domain below, even if a provider maps them onto different physical file types. The 2026-08-29.10 schema change is additive and backward-compatible: it adds optional guidance metadata and resumable Audit Sessions without destructively transforming existing account state.

## Workspace-level state

| Domain | Minimum fields |
|---|---|
| Account Registry | account_id, nickname, optional_private_game_uid, uid_suffix, screenname, alliance, server, active, status, guidance_level_optional, active_audit_session_id_optional, last_identity_confirmed, last_updated, database_provider, database_artifact_id_or_path, database_artifact_title, notes |
| Workspace Metadata | workspace_schema_version, active_account_id, account_discovery_policy, provider_adapter, privacy_policy, guidance_level_optional, engine_version, last_engine_refresh |
| Shared Engine Metadata | module_manifest_version, installed_module_versions, upstream_endpoints, fallback_version, health_status |
| Shared Artifact Registry | artifact_id, class, environment, canonical, public, format, update_trigger, source, retention, notes |

`account_id` is an immutable LWAI-generated primary key. UID is optional/private recognition metadata and must never be required for account creation or copied into shared Production. Guidance proficiency may be stored as NEW, LEARNING, COMFORTABLE or EXPERT and is an interaction preference/state only; it never relaxes privacy, evidence, batch-boundary or account-isolation rules.

## Account-local state

Every managed account has an isolated canonical database/logical namespace containing these domains. Mutable rows or audit-session state from one account must never be written into another account's namespace implicitly.

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
- `account_id` is mandatory on every persisted session. Resolve `active_account_id` before resuming or mutating one.
- Valid status values are ACTIVE, PAUSED, COMPLETE and ABANDONED.
- Recommended ingestion modes are direct_batch, document_bundle and guided_capture.
- Batch completion state must record declared boundaries such as `done`; a session must not finalize a declared multi-upload batch early.
- Interrupted audits resume at the persisted current_step only after the intended account is resolved.
- Guidance level may adapt over time but cannot weaken evidence, privacy, account isolation or explicit batch-boundary rules.

## Migration-first startup rules
- Discover Workspace Registry and accessible prior LWAI state before asking broad onboarding questions.
- Reuse/import supported confirmed current facts with source, confidence and freshness preserved.
- Ask only for missing, ambiguous, contradictory or materially stale information.
- Persist migrated/validated state immediately when writable storage exists.
- Never claim access to unrelated prior conversations that are not actually available.

## Account routing and archive rules
- Resolve `active_account_id` before any mutable account transaction.
- Reload order begins with Workspace Metadata/Account Registry, then the active account identity/cache/state and that account's unfinished Audit Session when applicable.
- A context switch flushes current pending changes/session progress, clears account-scoped working cache, sets `active_account_id`, then loads the target namespace and only its Audit Sessions.
- Cross-account comparisons are read-only and preserve the prior `active_account_id` unless the user explicitly switches.
- `start over` creates a new account_id/namespace and archives the old registry entry by default; it does not delete historical state implicitly.
- Archive is reversible. Restoring an archived account preserves its original immutable account_id and history.

## Data rules
- Canonical/observed state and derived recommendations are separate.
- All consequential canonical facts should carry source and confidence.
- Monotonic stale values become `minimum_known`, not assumed exact.
- Volatile values become stale aggressively and cannot drive major decisions without refresh.
- Corrections persist until explicitly revoked within their account.
- Change Log is append-oriented; cache eviction never destroys historical audit data.
- IDs and timestamps survive provider migrations.
- Engine updates preserve Account Registry, `active_account_id`, all Account Identity records, all account-local namespaces, Audit Sessions and provider-local references.
- Identity fields, screenshots and account-local session contents are private deployment-local data. Shared GitHub Production and public Gold Assets contain schemas/rules only, never a consumer's actual identity values or account evidence.
