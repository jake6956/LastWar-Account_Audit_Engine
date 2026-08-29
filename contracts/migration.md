# Migration Contract

## Principle
Engine/schema/provider changes must preserve deployment-local state. A breaking migration cannot be promoted until preservation is validated.

## Required sequence
1. Snapshot canonical local state and engine/provider metadata.
2. Export a provider-neutral representation where possible.
3. Apply schema/adapter transformation to a copy or reversible target.
4. Validate entity/row counts, unique IDs, latest canonical values, Corrections, Change Log continuity, resource-lane targets and local preferences.
5. Rebuild Hot Cache from migrated canonical state rather than copying stale cache blindly.
6. Run State Health and regression checks.
7. Switch canonical pointer only after validation passes.
8. Retain the prior known-good snapshot until the user/deployment has operated successfully.

## Never overwrite during engine refresh
Account facts, screenshots, battles, resource balances, local corrections, formations/presets, provider credentials, user preferences and account-specific learned methods remain local unless the migration transforms their schema while preserving meaning.

## Failure behavior
Abort/rollback to last known-good local state and engine. Do not partially promote a migration that loses data or silently drops logical domains.
