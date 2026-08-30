# LastWar Account Audit Engine (LWAI)

LWAI is a modular account-intelligence and optimization runtime for **Last War: Survival**. ChatGPT provides the conversational interface; the shared engine is centrally maintained in this repository; optional user persistence remains in the user's own supported storage.

## Install

Paste this single instruction into a fresh ChatGPT conversation:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

The short URL is a convenience alias. Canonical GitHub `main` is authoritative; the loader re-checks canonical Production metadata so stale alias/cache content cannot downgrade a newer verified release.

For best results, use a higher reasoning/thinking setting when the ChatGPT interface offers one.

## What LWAI does

LWAI builds and continuously reconciles a model of a player's account from screenshots, terse updates, current mechanics, resource constraints, battle evidence and user corrections. It uses that model to produce practical upgrade priorities, research plans, formation advice and account-wide optimization recommendations.

A player can provide compact updates such as a skill level, gear level or resource balance without completing a formal intake. LWAI updates only affected state and recomputes only what materially changed.

## Architecture

```text
engine/BOOTSTRAP.txt
  -> releases/LATEST.json
  -> engine/MANIFEST.json
  -> releases/MIGRATIONS.json
     -> mandatory core/release modules
     -> task-specific domain modules
     -> capability-specific adapters

engine/BOOTSTRAP_FULL.txt
  -> complete standalone fallback
```

The thin loader stays intentionally bounded and contains orchestration rather than game-domain playbooks. Mandatory core behavior loads first; domain modules load only when needed.

## Existing users and migration

LWAI discovers supported prior state before onboarding. Current registry-backed users resume their existing immutable account identity and canonical database; older pre-registry single-account deployments are registered nondestructively rather than rebuilt.

Production `2026-08-29.15` also restores explicit workspace-schema migration for supported older multi-account deployments:

- schema `2.1 -> 2.2`: optional guidance metadata and Audit Sessions;
- schema `2.2 -> 2.3`: optional Runtime Checkpoints and Runtime Journal.

These migrations are additive and idempotent. They preserve canonical account facts, immutable `account_id`, `active_account_id`, history, Corrections, evidence metadata and provider references. Domain modules that require schema `2.3` remain blocked until migration is verified. If no validated path exists, setup fails closed instead of guessing or re-onboarding the user.

## Integrity and compatibility

Production declares an engine API version, workspace schema version and per-module compatibility range. `engine/MANIFEST.json` pins each module to a Git blob identity so CI can verify the exact checked-in bytes.

Migration-capable core/release/storage components may explicitly support older validated workspace schemas; ordinary domain components may remain current-schema-only. `releases/MIGRATIONS.json` defines both promoted engine transitions and supported workspace-schema transitions.

## Persistence model

**GitHub Production contains:**
- sanitized runtime instructions and modules;
- provider-neutral schemas/adapters;
- release metadata and migrations;
- validation tests/documentation;
- reusable non-user-specific reference assets.

**User-local storage may contain:**
- account identity and game state;
- screenshots/evidence;
- balances and battle history;
- local corrections/preferences;
- account-specific audit/recovery state;
- optional runtime-session provenance.

Private account data and actual runtime-session/host-conversation references are never required in this public repository.

Durable storage is optional. Without writable supported storage, LWAI still operates in the active conversation and can use portable snapshots/exports, but persistence/recovery are naturally limited by the host session.

## Storage adapters

Persistence is capability-driven, not provider-name-driven. An adapter reports verified read/list/create/update/query/atomic-append/CAS/snapshot/restore capability and LWAI selects the strongest safe profile available. Recovery journals require actual atomic append, revision/CAS semantics, or immutable uniquely identified events.

## Multi-account, provenance and recovery

Persistent deployments can manage multiple isolated accounts under a workspace registry. Each account receives immutable LWAI-generated `account_id`; screenname, server, alliance, nickname and optional game UID remain private.

The runtime supports account switching, nondestructive archive/restore, migration-first startup, resumable audits and verify-before-replay checkpoints.

When durable persistence exists, LWAI may generate a private `runtime_session_id`. A host conversation/session reference may also be stored when safely exposed, but it is optional and non-authoritative. It is never account identity, authentication, routing, recovery ordering or write deduplication.

LWAI does not require game passwords, session tokens, cookies or authentication captures for normal operation.

## Updates and self-healing

Production updates are centrally published through GitHub. A deployment compares current engine/workspace state with canonical release/migration metadata, applies only validated compatible transitions and preserves all user-local state.

If required engine content cannot be retrieved or validated, LWAI retains last-known-good compatible engine state or uses the complete `BOOTSTRAP_FULL.txt` fallback. Engine repair never overwrites private account state.

## Validation

Production CI performs structural validation plus executable deterministic regressions. Gates cover release/version parity, module graph and byte integrity, privacy markers, loader boundaries, compatibility, account isolation, archive/start-over, migration preservation, legacy/current startup ordering, runtime-session provenance, `WAITING_USER`, verify-before-replay, checkpoint loss, append-only journal semantics, provider degradation, historical workspace-schema migration and stale-alias canonicalization.

## Production endpoints

- Release metadata: `releases/LATEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Thin loader: `engine/BOOTSTRAP.txt`
- Module graph: `engine/MANIFEST.json`
- Complete fallback: `engine/BOOTSTRAP_FULL.txt`
- Install alias: https://tinyurl.com/2yxf7f5x

## Repository layout

```text
engine/          loader, module graph, runtime modules and full fallback
contracts/       behavioral and release contracts
schemas/         provider-neutral workspace/account/engine schemas
adapters/        persistence/provider mappings
docs/            deployment, beta and architecture documentation
scripts/         release-validation tooling
tests/           executable regressions and release-gate specifications
releases/        version manifests, migration graph and changelog
gold-assets/     reusable sanitized shared assets
.github/         CI and issue templates
```

## Release discipline

Production changes follow short-lived staged RC branches with sanitization checks, exact-head PR CI, validated-head merge and post-merge verification. Users always install the single canonical Production line; RC branches are not alternate installers.

## Current Production

**Engine version:** `2026-08-29.15`

**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Channel:** Production  
**Sanitized public engine:** yes  
**Account state included:** no
