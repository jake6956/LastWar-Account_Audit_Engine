# Provider-Neutral LWAI Workspace Schema

Version: 2026-08-29.5

A writable deployment should preserve logical equivalents of every domain below even if a provider collapses them into fewer physical files.

| Domain | Minimum fields |
|---|---|
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
| Mechanics Registry | mechanic, current_belief, source_type, reference, last_verified, confidence, volatility, notes |
| Hot Cache | key, current_value, domain, freshness_class, updated, source, confidence, dependent_targets, status |
| State Health | domain_key, health_status, issue_type, last_checked, required_action, blocking_level, notes |
| Staleness Policy | data_class, freshness_guideline, stale_behavior, refresh_method, notes |
| Engine Metadata | engine_version, provider_adapter, canonical_store, upstream_endpoint, last_engine_refresh, schema_version |
| Artifact Registry | artifact_id, class, environment, canonical, public, format, update_trigger, source, retention, notes |
| Snapshots | dated recovery artifact references |

## Data rules
- Canonical/observed state and derived recommendations are separate.
- All consequential canonical facts should carry source and confidence.
- Monotonic stale values become `minimum_known`, not assumed exact.
- Volatile values become stale aggressively and cannot drive major decisions without refresh.
- Corrections persist until explicitly revoked.
- Change Log is append-oriented; cache eviction never destroys historical audit data.
- IDs and timestamps survive provider migrations.
