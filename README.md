# LastWar Account Audit Engine (LWAI)

LWAI is a portable, self-healing account optimization framework for **Last War: Survival**. It turns screenshots, terse account updates, current mechanics, resource constraints, and battle evidence into a continuously reconciled account model and decisive upgrade recommendations.

## One-line install

The preferred consumer install is:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

Paste that single line into a fresh ChatGPT conversation. The assistant retrieves the small Production loader, validates the module manifest, loads mandatory core behavior, discovers any existing managed account state, and fetches domain modules only as needed. No multi-page mobile copy/paste is required when web access works.

The short URL is a convenience/distribution alias, not the trust root. Direct Production sources are:
- Latest release: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
- Thin loader: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt
- Module graph: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json
- Complete fallback: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt

For best results, switch reasoning/thinking to **HIGH** if the product exposes that control. Durable persistence is strongly recommended but optional.

## Distribution privacy

Normal sharing uses the neutral short URL so the repository owner/maintainer handle is not exposed in the visible end-user install instruction. This is intentionally **semi-anonymous convenience, not true anonymity**: anyone who resolves the short link can discover the public GitHub repository and provenance.

Private player identity and account state are a separate boundary. Optional game UID, screenname, alliance, server, account data, screenshots, balances, local corrections, provider identifiers and credentials belong only in the user's chosen private runtime workspace. They are not shared back to this Production repository.

## Hub-and-spoke architecture

### Production engineering hub — this repository
This repository is the authoritative sanitized Production engineering source. It contains only production-safe engine material: the thin loader, module manifest, independently versioned engine modules, complete recovery fallback, contracts, schemas, adapters, release tests/manifests, migration notes, qualified shared-asset metadata, and developer/operator documentation.

### Private runtime spoke — each player deployment
A persistent runtime may manage one or more game accounts. Workspace-level state contains an Account Registry and `active_account_id`. Each managed game account receives an immutable LWAI-generated `account_id` and its own isolated canonical database/logical namespace for identity, heroes, gear, tech, resources, presets, battle history, local corrections, cache/health state, screenshots/assets, preferences and snapshots.

Human-recognition identity may include an optional private game UID plus screenname, alliance, server and nickname. UID is useful but **never required**. Identity collection should include a short reassurance that these values are for the user's own internal/local account management and are not sent to shared LWAI Production.

**Private player state must never be committed to this repository.**

## Existing accounts and alts

Before new-account onboarding, a deployment with readable persistent LWAI storage checks for an existing Account Registry. It presents recognizable account choices and asks whether to resume one, create another, or start clean. Multiple plausible accounts are never selected silently.

Account switching is first-class. `active_account_id` controls mutable state routing; conversation recency does not. A switch flushes pending changes, clears account-scoped cache, loads the target state, and confirms the selected account. Cross-account comparisons are read-only. `start over` creates a clean account and archives the prior record by default rather than deleting it.

Legacy single-account LWAI deployments migrate non-destructively: generate an immutable `account_id`, create/register the Workspace Registry, register the existing database in place, set `active_account_id`, and preserve historical data without forcing re-onboarding.

## Modular runtime

Production uses a deliberately small default context surface:

```text
engine/BOOTSTRAP.txt
  -> engine/MANIFEST.json
     -> engine/modules/core/*            mandatory
     -> engine/modules/domains/*         loaded only when relevant
     -> engine/modules/adapters/*        loaded by verified capability
     -> engine/modules/release/*         update/health/migration behavior

engine/BOOTSTRAP_FULL.txt                 complete standalone recovery/runtime fallback
```

A routine gear update should not require loading season-store logic, release engineering, or unrelated domains. Small engine changes should normally modify only the affected module, manifest metadata, affected tests/contracts, release notes, and the compiled full fallback. The loader itself changes only when loader semantics change.

## Release model

`Prod-Dev (private) -> Release Candidate -> Production (GitHub) -> remote install endpoints / mirrors`

Production promotion fails closed if sanitization, module-graph completeness, fallback completeness, account isolation, local-state preservation, capability fallbacks, regression checks, documentation-as-code, CI, installer integrity, or endpoint parity fail.

## Repository layout

```text
engine/          thin loader, module graph, modules and complete fallback runtime
contracts/       operating/export/storage/account/release/migration contracts
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
- Preserve Workspace Registry, `active_account_id`, and all account-local state across upstream engine upgrades.
- Treat conversation context as cache when durable state exists.
- Newer high-confidence direct evidence supersedes stale inference.
- Recommendations are derived state and never become evidence for account facts.
- Shared gear is a transferable pool plus preset assignment within an account, not permanent hero ownership.
- Mutable state never crosses accounts implicitly.
- Reload and terse updates resolve through `active_account_id`, not conversational recency.
- Volatile game/store/season facts are refreshed before consequential use.
- Every material engine change updates its relevant module/contract/schema/test in the same release.
- A consumer deployment must work even with no cloud connector, no automation support, or limited tools.
- GitHub holds shared sanitized engine state; private runtime workspaces hold player state.
- URL shortening is transport convenience only; canonical GitHub sources remain authoritative.
- A missing/bad module must never be repaired by overwriting local account state.
- UID is optional/private and passwords/session credentials are never part of normal LWAI onboarding.

## Current production

**Engine version:** `2026-08-29.9`  
**Preferred install URL:** https://tinyurl.com/2yxf7f5x

Google Drive remains the reference private Prod-Dev/runtime implementation. GitHub is the authoritative sanitized Production engineering hub. End users normally need only the one-line install instruction above.