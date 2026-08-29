# Provider-Neutral LWAI Workspace Schema

Version: 2026-08-29.9

A writable deployment should preserve workspace-level account routing plus isolated logical equivalents of every account-local domain below, even if a provider maps them onto different physical file types.

## Workspace-level state

| Domain | Minimum fields |
|---|---|
| Account Registry | account_id, nickname, optional_private_game_uid, uid_suffix, screenname, alliance, server, active, status, last_identity_confirmed, last_updated, database_provider, database_artifact_id_or_path, database_artifact_title, notes |
| Workspace Metadata | workspace_schema_version, active_account_id, account_discovery_policy, provider_adapter, privacy_policy, engine_version, last_engine_refresh |
| Shared Engine Metadata | module_manifest_version, installed_module_versions, upstream_endpoints, fallback_version, health_status |
| Shared Artifact Registry | artifact_id, class, environment, canonical, public, format, update_trigger, source, retention, notes |

`account_id` is an immutable LWAI-generated primary key. UID is optional/private recognition metadata and must never be required for account creation or copied into shared Production.

## Account-local state

Every managed account has an isolated canonical database/logical namespace containing these domains. Mutable rows from one account must never be written into another account's namespace implicitly.

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
| Snapshots | dated recovery artifact references |
| Assets | screenshots/report references, account_id, captured_at, source, notes |

## Account routing rules
- Resolve `active_account_id` before any mutable account transaction.
- Reload order begins with Workspace Metadata/Account Registry, then the active account identity/cache/state.
- A context switch flushes current pending changes, clears account-scoped working cache, sets `active_account_id`, then loads the target namespace.
- Cross-account comparisons are read-only and preserve the prior `active_account_id` unless the user explicitly switches.
- `start over` creates a new account_id/namespace and archives the old registry entry by default; it does not delete historical state implicitly.

## Data rules
- Canonical/observed state and derived recommendations are separate.
- All consequential canonical facts should carry source and confidence.
- Monotonic stale values become `minimum_known`, not assumed exact.
- Volatile values become stale aggressively and cannot drive major decisions without refresh.
- Corrections persist until explicitly revoked within their account.
- Change Log is append-oriented; cache eviction never destroys historical audit data.
- IDs and timestamps survive provider migrations.
- Engine updates preserve Account Registry, `active_account_id`, all Account Identity records, all account-local namespaces, and provider-local references.
- Identity fields are private deployment-local metadata. Shared GitHub Production and public Gold Assets contain schemas/rules only, never a consumer's actual identity values.
