# LastWar Account Audit Engine (LWAI)

LWAI is a modular account-intelligence and optimization runtime for **Last War: Survival**. ChatGPT provides the conversational interface; the shared engine is centrally maintained in this repository; optional user persistence remains in the user's own supported storage.

## Install

Paste this single instruction into a fresh ChatGPT conversation:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

The installer retrieves the current sanitized Production loader from GitHub. The short URL is a convenience alias; GitHub `main` is the authoritative public Production source.

For best results, use a higher reasoning/thinking setting when the ChatGPT interface offers one.

## What LWAI does

LWAI builds and continuously reconciles a model of a player's account from screenshots, terse updates, current mechanics, resource constraints, battle evidence and user corrections. It uses that model to produce practical upgrade priorities, research plans, formation advice and account-wide optimization recommendations.

The runtime is designed for low-friction use. A player can provide compact updates such as a skill level, gear level or resource balance without completing a formal intake process. LWAI updates only the affected state and recomputes only what materially changed.

## Architecture

LWAI uses a thin-loader, modular-runtime design:

```text
engine/BOOTSTRAP.txt
  -> releases/LATEST.json
  -> engine/MANIFEST.json
     -> mandatory core modules
     -> task-specific domain modules
     -> capability-specific adapters
     -> release/update/recovery modules

engine/BOOTSTRAP_FULL.txt
  -> complete standalone fallback
```

The loader stays intentionally small and contains orchestration rather than game-domain playbooks. Mandatory core behavior is loaded at startup, while domain modules are retrieved only when the current task requires them. This keeps active context bounded and lets individual engine components evolve independently.

## Integrity and compatibility

Production declares an engine API version, workspace schema version and per-module compatibility range. `engine/MANIFEST.json` also pins each module to a Git blob identity so CI can verify that the manifest describes the exact checked-in bytes.

When a host can reproduce or inspect the same identity, LWAI can verify a fetched module before use. If that primitive is unavailable, the runtime falls back to canonical-origin plus exact module identity/version checks and last-known-good recovery rather than pretending a cryptographic verification occurred.

Version-to-version state transitions are declared in `releases/MIGRATIONS.json`. Engine-only releases preserve private user state in place; schema-changing releases require explicit migration behavior and preservation tests.

## Persistence model

LWAI separates shared engine behavior from private user state.

**GitHub Production contains:**
- sanitized runtime instructions and modules
- provider-neutral schemas and adapters
- release metadata and migrations
- validation tests and documentation
- reusable non-user-specific reference assets

**User-local storage may contain:**
- account identity and game state
- screenshots and evidence
- resource balances and battle history
- local corrections and preferences
- account-specific audit sessions and recovery state

Private account data is not required for the public repository and must not be committed here.

Durable storage is optional. Without a writable supported storage provider, LWAI can still operate within the active conversation and use portable snapshots/exports, but persistence and recovery are naturally limited by the host session.

## Storage adapters

Persistence is capability-driven, not provider-name-driven. An adapter reports what it can actually do—read, list, create/update, structured query, atomic append, compare-and-swap, snapshot and restore—and the runtime selects the strongest safe persistence profile available.

A provider is never treated as transaction-safe merely because it offers spreadsheets or cloud files. Recovery journals require atomic append, revision/CAS semantics, or immutable uniquely identified event records.

## Multi-account and recovery

Persistent deployments can manage multiple isolated accounts under a workspace registry. Each account receives an immutable LWAI-generated `account_id`; human-recognition metadata such as screenname, server, alliance, nickname and optional game UID remains private to the user's environment.

The runtime supports migration-first startup, including legacy pre-registry discovery: an older single-account LWAI database can be registered in place before `active_account_id` is required, then normal account-scoped recovery begins. Current registry-backed deployments resolve their active account before recovery. Nondestructive archive/restore, account switching, resumable audit sessions and recovery checkpoints remain supported.

Recovery follows a verify-before-replay model so already committed writes are not duplicated after context loss.

LWAI does not require game passwords, session tokens, cookies or authentication captures for normal operation.

## Updates and self-healing

Production updates are centrally published through GitHub. A deployment can compare its current engine version with `releases/LATEST.json`, apply compatible engine updates and migrations, and preserve all user-local state.

If a module cannot be retrieved or validated, the runtime falls back to the last-known-good engine state or the complete `BOOTSTRAP_FULL.txt` artifact. Engine recovery must never overwrite private account state as a repair mechanism.

## Validation

Production CI performs both structural validation and executable behavioral regression tests. Structural gates verify release/version parity, dependency graph validity, module byte identity, privacy markers, loader boundaries, compatibility metadata and fallback completeness. A deterministic reference state machine separately exercises account isolation, archive/start-over behavior, migration preservation, legacy/current startup ordering, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal semantics and provider degradation.

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
docs/            deployment and architecture documentation
scripts/         release-validation tooling
tests/           executable regressions and release-gate specifications
releases/        version manifests, migration graph and changelog
gold-assets/     reusable sanitized shared assets
.github/         CI configuration
```

## Release discipline

Production changes follow a staged release path with sanitization checks, candidate validation, pull-request CI, exact-head verification and post-merge Production checks. User-specific state is excluded from release artifacts.

## Current Production

**Engine version:** `2026-08-29.13`

**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Channel:** Production  
**Sanitized public engine:** yes  
**Account state included:** no
