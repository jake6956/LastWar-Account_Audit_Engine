# LastWar Account Audit Engine (LWAI)

LWAI is a portable, self-healing account optimization framework for **Last War: Survival**. It turns screenshots, terse account updates, current mechanics, resource constraints and battle evidence into a continuously reconciled account model and decisive upgrade recommendations.

## One-line install

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

The short URL is a convenience alias, not a trust root. Canonical Production sources:
- Latest release: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
- Thin loader: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt
- Module graph: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json
- Complete fallback: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt

For best results, use HIGH reasoning/thinking when the product exposes that control. Durable persistence is strongly recommended but optional.

## Runtime recovery

2026-08-29.11 adds compact durable workflow recovery without treating chat history as a database. Conversation context remains volatile cache; canonical account databases and Workspace Registry remain durable truth. Optional workspace-level **Runtime Checkpoints** record the current safe workflow position, while an append-only **Runtime Journal** records material write-ahead/events.

Recovery is **verify-before-replay**. After Workspace Registry and `active_account_id` are resolved, LWAI inspects unresolved checkpoints plus their actual affected durable artifacts. Verified durable state outranks stale checkpoint claims; successful writes are not repeated merely because conversation context disappeared. `COMMITTED` is used only after the intended durable end state is verified.

A declared multi-upload boundary can persist as `WAITING_USER`, so a restart never turns context loss into implicit `done`. Account-scoped checkpoints carry `account_id` and cannot silently resume under another `active_account_id`. Checkpoint loss may reduce recovery convenience, but it cannot destroy canonical account facts.

Runtime recovery is deliberately compact. Actual checkpoint/journal rows, account identity, screenshots and provider-local references stay in the user's private workspace. LWAI never needs hidden chain-of-thought, raw internal reasoning or full transcripts for recovery.

See `contracts/runtime-checkpoint-recovery.md` and `docs/runtime-recovery.md`.

## Guided lifecycle

`core.guidance` is mandatory runtime behavior. LWAI discovers/reconciles accessible prior state before broad onboarding, preserves supported current facts, and asks only for information that is missing, ambiguous, contradictory or materially stale. Guidance adapts from explicit novice capture steps to terse expert updates without weakening evidence, privacy, account isolation or declared batch boundaries.

Large audits support direct screenshot batches, supported DOCX/PDF screenshot bundles, and phone-friendly guided capture. Multi-upload requests define a `done` boundary. Persistent deployments may maintain account-scoped Audit Sessions for detailed audit progress; Runtime Checkpoints persist only the surrounding generic workflow safe point when interruption matters.

Archive is nondestructive. Restore/unarchive preserves immutable `account_id` and history.

## Hub-and-spoke architecture

### Production engineering hub
This repository is the authoritative sanitized Production source: thin loader, module manifest, independently versioned modules, complete fallback, contracts, schemas, adapters, release tests/manifests and documentation.

### Private runtime spoke
Each deployment may manage one or more game accounts. Workspace-level private state includes Account Registry, `active_account_id`, optional guidance metadata, optional Runtime Checkpoints and Runtime Journal. Each account has an immutable LWAI-generated `account_id` and isolated canonical namespace for identity, heroes, gear, tech, resources, presets, battle history, local Corrections, cache/health state, screenshots/assets, preferences, snapshots and optional Audit Sessions.

Optional private game UID, screenname, alliance, server and nickname are human-recognition metadata; UID is never required. **Private player state and actual runtime checkpoint/journal rows must never be committed to this repository.**

## Existing accounts and alts

Before new-account onboarding, readable existing LWAI state is discovered and reconciled. Multiple plausible accounts are never silently selected. `active_account_id` controls mutable state routing; chat recency does not. Account switching flushes pending changes/session progress, safely pauses account-scoped pending workflows when necessary, clears account-scoped cache, then loads only the target account state. Cross-account comparison is read-only. `start over` creates a clean account and archives prior state by default rather than deleting it.

Legacy single-account deployments migrate non-destructively: generate immutable `account_id`, create/register Workspace Registry, register the existing database in place, set `active_account_id`, preserve history, and import supported legacy facts without forcing re-onboarding.

## Modular runtime

```text
engine/BOOTSTRAP.txt
  -> engine/MANIFEST.json
     -> engine/modules/core/*            mandatory
     -> engine/modules/domains/*         task-driven
     -> engine/modules/adapters/*        capability-driven
     -> engine/modules/release/*         update/health/recovery

engine/BOOTSTRAP_FULL.txt                 complete standalone fallback
```

Routine work loads mandatory core plus the smallest relevant domain module. A missing/bad module falls back safely and must never be repaired by overwriting local account state.

## Persistence and recovery model

- Conversation context = temporary cache.
- Workspace Registry/account databases = canonical durable state.
- Audit Sessions = detailed account-audit progress.
- Runtime Checkpoints = compact generic workflow position.
- Runtime Journal = append-only material event history.
- GitHub Production = sanitized engine/schema behavior only.

Structured writable providers should use checkpoint/journal tables or collections. Writable file-only providers may use a checkpoint index plus append-only JSONL/NDJSON or timestamped records. Read-only/no durable storage cannot claim persistent checkpoint recovery.

## Release model

`Prod-Dev (private) -> frozen private RC -> GitHub rc/<version> -> PR -> exact-head CI/private gates -> exact validated-head merge -> main verification -> installer verification -> private archive/release records`

Engine release transactions themselves use workspace/global recovery checkpoints when durable storage exists. Before retrying a branch, PR, merge, archive or mirror write, inspect the actual target. Interrupted pre-merge work preserves last-known-good main. A secondary mirror/archive failure after a validated merge is recorded for retry rather than silently rolling back healthy Production.

## Repository layout

```text
engine/          loader, module graph, modules and complete fallback
contracts/       operating/export/storage/account/release/guidance/recovery contracts
schemas/         provider-neutral workspace/account schemas
adapters/        persistence mappings
docs/            architecture/deployment/recovery documentation
scripts/         release validation tooling
tests/           regression and sanitization policies
releases/        manifests/changelog/version metadata
gold-assets/     reusable sanitized asset governance
.github/         CI validation
```

## Core invariants

- Optimize real combat effectiveness, not displayed power alone.
- Reuse accessible prior state before redundant onboarding.
- Newer high-confidence direct evidence supersedes stale inference.
- Shared gear is a transferable pool plus preset assignment within an account.
- Mutable state, Audit Sessions and account-scoped checkpoints never cross accounts implicitly.
- Reload resolves Workspace Registry and `active_account_id`, not chat recency.
- Recovery inspects durable artifacts before replay and never blindly duplicates verified writes.
- A declared `done` boundary survives reload when durable checkpointing exists.
- Runtime Journal is append-only in normal operation.
- Checkpoint loss cannot destroy canonical account facts.
- Hidden reasoning/full transcripts are never required for recovery.
- Engine refresh preserves all LOCAL STATE: registry, accounts, sessions, checkpoints, journal and provider metadata.
- UID is optional/private; passwords/session credentials are never normal onboarding data.
- GitHub holds only sanitized shared engine state; private workspaces hold player and operational state.
- URL shortening is transport convenience only; canonical GitHub sources remain authoritative.

## Current production

**Engine version:** `2026-08-29.11`  
**Preferred install URL:** https://tinyurl.com/2yxf7f5x

Google Drive remains the reference private Prod-Dev/runtime implementation. GitHub is the authoritative sanitized Production engineering hub.
