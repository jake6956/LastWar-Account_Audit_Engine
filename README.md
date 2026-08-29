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
  -> engine/MANIFEST.json
     -> mandatory core modules
     -> task-specific domain modules
     -> capability-specific adapters
     -> release/update/recovery modules

engine/BOOTSTRAP_FULL.txt
  -> complete standalone fallback
```

The loader stays intentionally small. Mandatory core behavior is loaded at startup, while domain modules are retrieved only when the current task requires them. This keeps active context bounded and allows individual engine components to evolve independently.

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

## Multi-account and recovery

Persistent deployments can manage multiple isolated accounts under a workspace registry. Each account receives an immutable LWAI-generated `account_id`; human-recognition metadata such as screenname, server, alliance, nickname and optional game UID remains private to the user's environment.

The runtime supports migration-first startup, nondestructive archive/restore, account switching, resumable audit sessions and recovery checkpoints. Recovery follows a verify-before-replay model so already committed writes are not duplicated after context loss.

LWAI does not require game passwords, session tokens, cookies or authentication captures for normal operation.

## Updates and self-healing

Production updates are centrally published through GitHub. A deployment can compare its current engine version with `releases/LATEST.json`, apply compatible engine updates and migrations, and preserve all user-local state.

If a module cannot be retrieved or validated, the runtime falls back to the last-known-good engine state or the complete `BOOTSTRAP_FULL.txt` artifact. Engine recovery must never overwrite private account state as a repair mechanism.

## Production endpoints

- Release metadata: `releases/LATEST.json`
- Thin loader: `engine/BOOTSTRAP.txt`
- Module graph: `engine/MANIFEST.json`
- Complete fallback: `engine/BOOTSTRAP_FULL.txt`
- Install alias: https://tinyurl.com/2yxf7f5x

## Repository layout

```text
engine/          loader, module graph, runtime modules and full fallback
contracts/       behavioral and release contracts
schemas/         provider-neutral workspace/account schemas
adapters/        persistence/provider mappings
docs/            deployment and architecture documentation
scripts/         release-validation tooling
tests/           regression and release-gate specifications
releases/        version manifests and changelog
gold-assets/     reusable sanitized shared assets
.github/         CI configuration
```

## Release discipline

Production changes follow a staged release path with sanitization checks, candidate validation, pull-request CI, exact-head verification and post-merge Production checks. User-specific state is excluded from release artifacts.

## Current Production

**Engine version:** `2026-08-29.11`

**Channel:** Production  
**Sanitized public engine:** yes  
**Account state included:** no
