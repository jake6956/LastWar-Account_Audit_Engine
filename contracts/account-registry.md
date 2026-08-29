# Account Registry & Multi-Account Contract

## Purpose
Define how LWAI discovers, identifies, resumes, switches, compares and isolates multiple Last War accounts without exposing private identity or corrupting state.

## Identity model
Every managed account has an immutable LWAI-generated `account_id` used as the database/storage primary key. Human-recognition fields are mutable metadata: optional/private game UID, screenname, alliance, server, nickname, HQ, primary unit type and updated dates. UID is useful but never required.

At identity collection, briefly explain that identifying values are for the user's own internal/local account management and are not sent to the shared LWAI Production repository. Never request game passwords, session cookies/tokens, captured auth files or equivalent credentials for normal operation.

## Workspace registry
A persistent deployment maintains a workspace-level registry separate from account-local state. Minimum account fields: `account_id`, `nickname`, `game_uid`, `uid_suffix`, `screenname`, `alliance`, `server`, `active`, `status`, `last_identity_confirmed`, `last_updated`, `database_provider`, `database_artifact_id_or_path`, `database_artifact_title`, `notes`.

Workspace metadata includes `active_account_id`, `workspace_schema_version`, account-discovery policy, provider adapter and privacy policy.

## Isolation
Each account has its own canonical database/logical namespace for Account Identity, Heroes, Gear Pool, Presets, Tech/queues, Resources, Drone, Decorations, Profession, Season/Overlord, Battle Log, Change Log, Corrections, local mechanics observations, Hot Cache, State Health, staleness state, screenshots/assets, preferences and snapshots. Shared generic engine/mechanics material may be reused. Mutable account facts never cross accounts implicitly.

## Discovery
Before new-account Phase 1 when readable persistent LWAI state exists, look for the registry, enumerate active/non-archived accounts, present compact recognizable labels, then ask whether to resume, create another account or start clean. Do not silently choose between multiple plausible accounts. Confirm even one strong match after a fresh install/migration. Legacy single-account state migrates in place rather than forcing re-onboarding.

## Context switching
A switch transaction flushes/logs pending changes for the current account, clears account-scoped cache, sets `active_account_id`, loads target identity/cache/corrections/health/state, confirms the target compactly, and routes later terse updates only to that account. Reload resolves `active_account_id`, never conversational recency.

## Start over
Starting over creates a new clean account and archives the prior entry by default. Destructive deletion requires explicit user intent after disclosure of what will be removed.

## Cross-account comparison
Comparisons mount selected accounts read-only, do not merge/overwrite source data, and preserve the prior active account unless the user explicitly switches.

## Identity sanity checks
Periodically or when evidence conflicts, confirm screenname, alliance, server and optionally UID. Update mutable identity fields on the same account when continuity is supported. Preserve immutable `account_id`.

## Migration
Single-account -> multi-account: generate `account_id`; create registry; register existing canonical database in place; add Account Identity when supported; set `active_account_id`; preserve domain state; run reload/isolation checks. No re-onboarding solely because the runtime gained multi-account support.
