# LastWar Account Audit Engine (LWAI)

LWAI is a portable, self-healing account optimization framework for **Last War: Survival**. It turns screenshots, terse account updates, current mechanics, resource constraints, and battle evidence into a continuously reconciled account model and decisive upgrade recommendations.

## One-line install

The preferred consumer install is:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

Paste that single line into a fresh ChatGPT conversation. The assistant retrieves the small Production loader, validates the module manifest, loads mandatory core behavior, discovers/migrates any accessible existing LWAI state, and fetches domain modules only as needed. No multi-page mobile copy/paste is required when web access works.

The short URL is a convenience/distribution alias, not the trust root. Direct Production sources are:
- Latest release: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
- Thin loader: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt
- Module graph: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json
- Complete fallback: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt

For best results, switch reasoning/thinking to **HIGH** if the product exposes that control. Durable persistence is strongly recommended but optional.

## Guided lifecycle

2026-08-29.10 adds `core.guidance` as mandatory runtime behavior. A new installer assumes the player may already have used an older LWAI prompt or supplied account data. It discovers/reconciles accessible prior state first, preserves supported current facts, and asks only for information that is missing, ambiguous, contradictory or materially stale.

The interaction model is deliberately human: a personable technician with a clipboard rather than a form wizard. New users receive explicit instructions; experienced users can still send terse updates. Multi-upload requests tell the user exactly what to send and explicitly ask them to reply `done` when the batch is complete. A declared batch is not finalized early.

Large screenshot audits support three equivalent evidence paths:
- direct screenshot batches across multiple messages;
- supported DOCX/PDF screenshot bundles for desktop workflows;
- phone-friendly guided capture, one hero/item/system mini-batch at a time.

Persistent deployments may maintain account-scoped resumable Audit Sessions so long audits can continue across context loss without losing position. Audit Session state is isolated by `active_account_id` and cannot cross accounts.

Archived accounts are recoverable. Archive remains nondestructive, and restore/unarchive preserves the immutable `account_id` and historical state.

## Distribution privacy

Normal sharing uses the neutral short URL so the repository owner/maintainer handle is not exposed in the visible end-user install instruction. This is intentionally **semi-anonymous convenience, not true anonymity**: anyone who resolves the short link can discover the public GitHub repository and provenance.

Private player identity and account state are a separate boundary. Optional game UID, screenname, alliance, server, account data, screenshots, balances, local corrections, Audit Sessions, provider identifiers and credentials belong only in the user's chosen private runtime workspace. They are not shared back to this Production repository.

## Hub-and-spoke architecture

### Production engineering hub — this repository
This repository is the authoritative sanitized Production engineering source. It contains only production-safe engine material: the thin loader, module manifest, independently versioned engine modules, complete recovery fallback, contracts, schemas, adapters, release tests/manifests, migration notes, qualified shared-asset metadata, and developer/operator documentation.

### Private runtime spoke — each player deployment
A persistent runtime may manage one or more game accounts. Workspace-level state contains an Account Registry and `active_account_id`. Each managed game account receives an immutable LWAI-generated `account_id` and its own isolated canonical database/logical namespace for identity, heroes, gear, tech, resources, presets, battle history, local corrections, cache/health state, screenshots/assets, preferences, snapshots and optional Audit Sessions.

Human-recognition identity may include an optional private game UID plus screenname, alliance, server and nickname. UID is useful but **never required**. Identity collection should include a short reassurance that these values are for the user's own internal/local account management and are not sent to shared LWAI Production.

**Private player state must never be committed to this repository.**

## Existing accounts and alts

Before new-account onboarding, a deployment with readable persistent or accessible prior LWAI state performs migration-first discovery. It reuses supported current facts, presents recognizable account choices where needed, and asks only for remaining gaps. Multiple plausible accounts are never selected silently.

Account switching is first-class. `active_account_id` controls mutable state routing; conversation recency does not. A switch flushes pending changes/session progress, clears account-scoped cache, loads the target state, and confirms the selected account. Cross-account comparisons are read-only. `start over` creates a clean account and archives the prior record by default rather than deleting it.

Legacy single-account LWAI deployments migrate non-destructively: generate an immutable `account_id`, create/register the Workspace Registry, register the existing database in place, set `active_account_id`, preserve historical data, and import supported legacy facts with evidence metadata without forcing re-onboarding.

## Modular runtime

Production uses a deliberately small default context surface:

```text
engine/BOOTSTRAP.txt
  -> engine/MANIFEST.json
     -> engine/modules/core/*            mandatory, including core.guidance
     -> engine/modules/domains/*         loaded only when relevant
     -> engine/modules/adapters/*        loaded by verified capability
     -> engine/modules/release/*         update/health/migration behavior

engine/BOOTSTRAP_FULL.txt                 complete standalone recovery/runtime fallback
```

A routine gear update should not require loading season-store logic, release engineering, or unrelated domains. Small engine changes should normally modify only the affected module, manifest metadata, affected tests/contracts, release notes, and the compiled full fallback. The loader itself changes only when loader semantics change.

## Release model

`Prod-Dev (private) -> Release Candidate -> Production (GitHub) -> remote install endpoints / mirrors`

Production promotion fails closed if sanitization, module-graph completeness, fallback completeness, migration-first behavior, account isolation, session isolation, local-state preservation, capability fallbacks, regression checks, documentation-as-code, CI, installer integrity, or endpoint parity fail.

## Repository layout

```text
engine/          thin loader, module graph, modules and complete fallback runtime
contracts/       operating/export/storage/account/release/migration/guidance contracts
schemas/         provider-neutral workspace and account-registry schemas
adapters/        provider-specific persistence mappings
scripts/         release validation tooling
tests/           regression and sanitization policies
releases/        manifests/changelog/version metadata
gold-assets/     reusable sanitized asset metadata/governance
docs/            architecture/deployment/operator documentation
.github/          CI validation
```

## Core invariants

- Optimize real combat effectiveness, not displayed power alone.
- Preserve Workspace Registry, `active_account_id`, all account-local state and Audit Sessions across upstream engine upgrades.
- Treat conversation context as cache when durable state exists.
- Reuse accessible prior LWAI state before redundant onboarding.
- Ask only for missing, ambiguous, contradictory or materially stale information.
- Newer high-confidence direct evidence supersedes stale inference.
- Recommendations are derived state and never become evidence for account facts.
- Shared gear is a transferable pool plus preset assignment within an account, not permanent hero ownership.
- Mutable state and Audit Sessions never cross accounts implicitly.
- Reload and terse updates resolve through `active_account_id`, not conversational recency.
- Multi-upload requests explicitly define a `done` boundary and do not finalize early.
- Direct screenshot, supported document-bundle and guided capture modes follow the same evidence/confidence rules.
- Volatile game/store/season facts are refreshed before consequential use.
- Every material engine change updates its relevant module/contract/schema/test in the same release.
- A consumer deployment must work even with no cloud connector, no automation support, or limited tools.
- GitHub holds shared sanitized engine state; private runtime workspaces hold player state.
- URL shortening is transport convenience only; canonical GitHub sources remain authoritative.
- A missing/bad module must never be repaired by overwriting local account state.
- UID is optional/private and passwords/session credentials are never part of normal LWAI onboarding.
- Archive/restore preserves immutable `account_id` and history.

## Current production

**Engine version:** `2026-08-29.10`  
**Preferred install URL:** https://tinyurl.com/2yxf7f5x

Google Drive remains the reference private Prod-Dev/runtime implementation. GitHub is the authoritative sanitized Production engineering hub. End users normally need only the one-line install instruction above.
