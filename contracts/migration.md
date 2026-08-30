# Migration Contract

Version: 2026-08-29.15

## Principle
Engine/schema/provider changes must preserve deployment-local state. A breaking migration cannot be promoted until preservation is validated. Multi-account migrations preserve the Workspace Registry, active-account pointer, immutable account IDs and every account-local namespace independently.

## Migration graph
`releases/MIGRATIONS.json` is the machine-readable migration authority. It contains two related graphs:

- `edges`: promoted engine-version transitions.
- `workspace_schema_edges`: supported local workspace-schema transitions that may need to run when an existing deployment skips one or more historical engine releases.

Missing required paths fail closed rather than improvising state transformation.

## Historical workspace compatibility
Current workspace schema is `2.3`. Production explicitly supports additive migration from the two earlier multi-account schemas:

### 2.1 -> 2.2
Introduced with Guided Lifecycle. Preserve all existing registry/account state and optionally add, only when supported/absent:
- guidance proficiency metadata;
- account-scoped Audit Sessions.

### 2.2 -> 2.3
Introduced with Runtime Checkpointing. Preserve all prior state and optionally add, only when supported/absent:
- Runtime Checkpoints;
- append-only Runtime Journal.

Both transitions are nondestructive and idempotent. They do not require re-onboarding, change immutable `account_id`, rewrite canonical game facts/history, drop Corrections/evidence metadata, or replace provider references.

A deployment may be structurally newer than its stored schema-version marker because optional stores were added by earlier maintenance. Normalize the version only after verifying preservation invariants and current structures. Never infer that a version-string mismatch authorizes destructive rewriting.

## Migration-compatible bootstrap
`engine/MANIFEST.json` distinguishes migration-capable components from current-schema-only domain modules.

For an older supported workspace:
1. Verify canonical GitHub Production and the migration graph.
2. Resolve account context from an existing registry, or register pre-registry legacy state first.
3. Load only mandatory core/release components whose workspace compatibility includes the source schema, plus storage adapter behavior if migration requires provider writes and its range permits the source.
4. Keep domain/task modules that require target schema unloaded.
5. Apply workspace-schema edges sequentially with verify-before-write semantics.
6. Re-read workspace metadata, registry/account pointers and created optional structures.
7. Only after target schema is verified may normal current-schema domain loading and ordinary recovery continue.

If no validated path reaches current schema, preserve the workspace untouched and pause setup. Do not fall through to new-user onboarding.

## Compatibility
`engine/MANIFEST.json` declares `engine_api_version` plus per-module engine API and workspace-schema ranges. A module may load only inside its declared ranges. Migration-capable core/release/storage components may intentionally span supported historical workspace schemas; domain modules may remain target-schema-only.

## Required sequence
1. Resolve canonical current engine/schema/API versions and target migration path.
2. Resolve account context without inventing missing identifiers.
3. Snapshot canonical local state when durable snapshot capability exists.
4. Verify source workspace metadata/structures.
5. Apply transformations only to a reversible/copy-on-write target or with provider-level compare-and-swap/verify-before-write semantics.
6. Validate registry/account counts, immutable account IDs, `active_account_id`, latest canonical values, Corrections, Change Log continuity, evidence/confidence/freshness, preferences and provider-local references.
7. Rebuild Hot Cache from canonical state rather than blindly copying stale cache.
8. Validate newly introduced optional structures only when the provider supports them.
9. Re-read the workspace and confirm target schema before enabling target-schema-only domain behavior.
10. Retain prior known-good state/snapshot until successful operation is confirmed.

For an `engine_only` edge with unchanged workspace schema, preserve LOCAL STATE in place and refresh only ENGINE artifacts.

## Startup ordering across generations
- Current registry-backed deployment: load registry, resolve `active_account_id`, migrate supported older workspace schema if required, then run account-scoped recovery and ordinary reconciliation.
- Pre-registry legacy deployment: discover existing state, register it nondestructively, generate immutable `account_id`, create registry/set `active_account_id`, migrate schema if required, then run recovery.
- No registry/legacy state: genuinely-new-account guidance.

This prevents both circular account-routing dependencies and accidental re-onboarding of valid older deployments.

## Single-account -> multi-account migration
1. Discover and validate accessible legacy account state.
2. Generate immutable LWAI `account_id`.
3. Create workspace Account Registry and privacy/version metadata.
4. Register the existing canonical database in place; do not rewrite history merely to satisfy registry structure.
5. Add Account Identity when supported; UID remains optional/private.
6. Set `active_account_id`.
7. Preserve all existing domain state, Change Log, Corrections, preferences, screenshots/assets, snapshots and provider metadata.
8. Apply validated workspace-schema edges as required.
9. Run recovery/isolation checks and continue without broad re-onboarding.

## Multi-account invariants
- `account_id` is immutable and authoritative.
- Engine/schema migration preserves Workspace Registry, `active_account_id`, every registry entry and every account namespace.
- Account switches clear account-scoped working cache before loading target state.
- Cross-account comparison is read-only.
- `start over` archives rather than deletes by default.
- Provider migration cannot collapse isolated accounts into one ambiguous ledger.

## Alias/cache authority
The public one-line short URL is transport convenience only. If its fetched body is stale or differs from canonical GitHub `main`, `releases/LATEST.json` plus canonical `engine/BOOTSTRAP.txt`/`MANIFEST.json`/`MIGRATIONS.json` are authoritative. A stale alias/cache body may never downgrade a verified newer Production release.

## Never overwrite during engine refresh
Workspace Registry, `active_account_id`, identities/facts, screenshots, battles, balances, Corrections, formations/presets, provider references, preferences, Audit Sessions, Runtime Sessions, Runtime Checkpoints and Runtime Journal remain local unless an explicit validated schema edge adds or transforms metadata while preserving meaning.

## Privacy during migration
Game UID, identity, actual account IDs, provider IDs/paths, screenshots, balances, local Corrections, battle history and runtime/checkpoint rows stay private. Never copy them into shared GitHub Production, public Gold Assets or another deployment. Never request credentials/session tokens/auth captures as a migration requirement.

## Failure behavior
Fail closed to last known-good local state and engine. Migration failure must not trigger redundant onboarding, partially change schema version, collapse account namespaces, alter immutable IDs, replay COMMITTED recovery work, silently drop logical domains or expose private identity.
