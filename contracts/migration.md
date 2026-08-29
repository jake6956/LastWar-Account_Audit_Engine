# Migration Contract

Version: 2026-08-29.13

## Principle
Engine/schema/provider changes must preserve deployment-local state. A breaking migration cannot be promoted until preservation is validated. Multi-account migrations preserve the Workspace Registry, active-account pointer, immutable account IDs and every account-local namespace independently.

## Migration graph
`releases/MIGRATIONS.json` is the machine-readable migration graph. Each supported edge declares `from`, `to`, schema versions, migration type, local-state action, whether re-onboarding/account rewrite is required, relevant tests and notes.

Ordinary engine refresh must follow an explicit graph edge when crossing promoted versions. Missing required edges fail closed rather than improvising a state transformation. Engine-only edges may preserve the current workspace schema without rewriting account state.

## Compatibility
`engine/MANIFEST.json` declares `engine_api_version` plus per-module engine API and workspace-schema ranges. A module that excludes the current engine API/workspace schema is incompatible and must not load. Schema-breaking changes require an explicit migration edge and local-state survival tests before promotion.

## Required sequence
1. Resolve current promoted engine/schema/API versions and target edge.
2. Snapshot canonical local state, Workspace Registry when present, account identities and engine/provider metadata when durable snapshot capability exists.
3. Export a provider-neutral representation where practical for schema/provider migrations.
4. Apply transformation to a copy or reversible target.
5. Validate registry/account counts, immutable account IDs, unique domain IDs, latest canonical values, Corrections, Change Log continuity, resource-lane targets, preferences and provider-local database references.
6. Rebuild Hot Cache from migrated canonical state rather than blindly copying stale cache.
7. Run State Health, account-isolation and recovery regression checks.
8. Switch canonical pointers only after validation passes.
9. Retain prior known-good snapshot until the deployment has operated successfully.

For an `engine_only` edge with unchanged workspace schema, preserve LOCAL STATE in place and refresh only ENGINE artifacts; no account rewrite or user re-onboarding is permitted.

## Startup ordering across generations
A current registry-backed deployment and a pre-registry legacy deployment have different valid prerequisites:

- If a current Workspace Registry exists, load it and resolve `active_account_id` before account-scoped recovery. Then inspect unresolved Runtime Checkpoints/Journal and continue migration/reconciliation.
- If no Workspace Registry exists but accessible legacy LWAI single-account state exists, do **not** require `active_account_id` first. Discover the legacy state, register it nondestructively, generate its immutable LWAI `account_id`, create the Workspace Registry, set `active_account_id`, and only then run recovery-first continuation.
- If neither a registry nor legacy state exists, proceed to genuinely-new-account guidance/onboarding.

This ordering prevents a circular dependency where an older deployment is asked to supply account-routing metadata that did not exist in that generation. Legacy discovery before registry creation is not permission to bypass account isolation after the account context has been established.

## Single-account -> multi-account migration
For an existing deployment that predates Workspace Registry:
1. Discover and validate the accessible legacy LWAI account database/state before requiring `active_account_id`.
2. Generate one immutable LWAI `account_id` for the existing game account.
3. Create workspace-level Account Registry and record workspace schema/version/privacy metadata.
4. Register the existing canonical account database in place; do not rewrite historical domain data merely to satisfy new registry structure.
5. Add Account Identity when supported. UID remains optional/private and is not required for migration.
6. Set `active_account_id` to the migrated account.
7. Preserve all existing domain state, Change Log, Corrections, preferences, screenshots/assets, snapshots and provider metadata.
8. After account context exists, run recovery-first checks for any supported recovery metadata, then verify reload/account isolation.
9. Do not force new-account onboarding solely because multi-account support was added.

## Multi-account invariants
- `account_id` is immutable and authoritative; mutable identity fields do not create a new account automatically.
- Engine refresh preserves Workspace Registry, `active_account_id`, every registry entry and every account database/namespace.
- Account switches clear account-scoped working cache before loading the target account.
- Cross-account comparison is read-only and preserves prior active account unless explicitly switched.
- `start over` archives prior account and creates a clean one by default; deletion requires explicit intent.
- Provider migration preserves account isolation. A weaker provider that cannot guarantee independent writes cannot be declared fully supported canonical multi-account storage.

## Never overwrite during engine refresh
Workspace Registry, `active_account_id`, account identities/facts, screenshots, battles, balances, local Corrections, formations/presets, provider credentials/references, user preferences, Audit Sessions, Runtime Checkpoints and Runtime Journal remain local unless an explicit validated migration transforms their schema while preserving meaning.

## Privacy during migration
Game UID and identifying fields are private deployment-local metadata. Never copy them into shared GitHub Production, public Gold Assets, release manifests or another user's deployment. Never request passwords, session tokens/cookies, captured authentication files or game login credentials as a migration requirement.

## Failure behavior
Abort/rollback to last known-good local state and engine. Do not partially promote a migration that loses data, collapses account namespaces, changes immutable IDs, silently drops logical domains or exposes private identity.
