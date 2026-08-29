# Migration Contract

## Principle
Engine/schema/provider changes must preserve deployment-local state. A breaking migration cannot be promoted until preservation is validated. Multi-account migrations must preserve the workspace registry, active-account pointer, and every account-local namespace independently.

## Required sequence
1. Snapshot canonical local state, Workspace Registry when present, account identities, and engine/provider metadata.
2. Export a provider-neutral representation where possible.
3. Apply schema/adapter transformation to a copy or reversible target.
4. Validate registry/account counts, immutable account IDs, unique domain IDs, latest canonical values, Corrections, Change Log continuity, resource-lane targets, preferences, and provider-local database references.
5. Rebuild each account's Hot Cache from migrated canonical state rather than copying stale cache blindly.
6. Run State Health and account-isolation regression checks.
7. Switch canonical pointers only after validation passes.
8. Retain the prior known-good snapshot until the user/deployment has operated successfully.

## Single-account -> multi-account migration
For an existing LWAI deployment that predates the Workspace Registry:
1. Generate one immutable LWAI `account_id` for the existing game account.
2. Create a workspace-level Account Registry and record workspace schema/version/privacy metadata.
3. Register the existing canonical account database in place; do not rewrite historical domain data merely to satisfy the new registry structure.
4. Add an Account Identity record when the provider/schema supports it. UID remains optional/private and is not required for migration.
5. Set `active_account_id` to the migrated account.
6. Preserve all existing Heroes, Gear, Presets, Tech/queues, Resources, Drone, Decorations, Profession, season state, Battle Log, Change Log, Corrections, Hot Cache history, preferences, screenshots/assets, snapshots, and provider metadata.
7. Verify reload resolves through `active_account_id` and a terse update cannot target any other account namespace.
8. Do not force the user through new-account onboarding solely because multi-account support was added.

## Multi-account invariants
- `account_id` is immutable and authoritative; mutable identity fields do not create a new account automatically.
- Engine refresh must preserve Workspace Registry, `active_account_id`, every registry entry, and every account database/namespace.
- Account switches clear account-scoped working cache before loading the target account.
- Cross-account comparison is read-only and preserves the prior active account unless the user explicitly switches.
- `start over` archives the prior account entry and creates a new clean account by default; destructive deletion requires explicit user intent.
- Provider migration must preserve account isolation. A weaker provider that cannot guarantee independent writes cannot be declared a fully supported multi-account canonical store.

## Never overwrite during engine refresh
Workspace Registry, `active_account_id`, account identities, account facts, screenshots, battles, resource balances, local Corrections, formations/presets, provider credentials, provider-local database references, user preferences, and account-specific learned methods remain local unless an explicit migration transforms their schema while preserving meaning.

## Privacy during migration
Game UID and other identifying fields are private deployment-local metadata. They must never be copied into shared GitHub Production, public Gold Assets, public release manifests, or another user's deployment. Never request passwords, session tokens/cookies, captured authentication files, or game login credentials as a migration requirement.

## Failure behavior
Abort/rollback to the last known-good local state and engine. Do not partially promote a migration that loses data, collapses account namespaces, changes immutable IDs, silently drops logical domains, or exposes private identity.
