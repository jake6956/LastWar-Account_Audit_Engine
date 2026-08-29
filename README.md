# LastWar Account Audit Engine (LWAI)

LWAI is a portable, self-healing account optimization framework for **Last War: Survival**. It turns screenshots, terse account updates, current mechanics, resource constraints, and battle evidence into a continuously reconciled account model and decisive upgrade recommendations.

## One-line install

The preferred consumer install is:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

Paste that single line into a fresh ChatGPT conversation. The assistant should retrieve the small Production loader itself, validate the module manifest, load mandatory core behavior, and fetch domain modules only as needed. No multi-page mobile copy/paste is required when web access works.

The short URL is a convenience/distribution alias, not the trust root. Direct Production sources are:
- Latest release: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
- Thin loader: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt
- Module graph: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json
- Complete fallback: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt

For best results, switch reasoning/thinking to **HIGH** if the product exposes that control. Cloud persistence is strongly recommended but optional.

## Distribution privacy

Normal sharing uses the neutral short URL so the repository owner/maintainer handle is not exposed in the visible end-user install instruction. This is intentionally **semi-anonymous convenience, not true anonymity**: anyone who resolves the short link can discover the public GitHub repository and provenance.

## Hub-and-spoke architecture

### Production engineering hub — this repository
This repository is the authoritative sanitized Production engineering source. It contains only production-safe engine material: the thin loader, module manifest, independently versioned engine modules, complete recovery fallback, contracts, schemas, adapters, release tests/manifests, migration notes, qualified shared-asset metadata, and developer/operator documentation.

### Private runtime spoke — each player deployment
Each player keeps private state in their own environment: account facts and screenshots; hero/gear/tech/resource state; presets/formations; battle history/local corrections; Hot Cache/State Health/staleness metadata; and provider credentials/local file paths.

**Private player state must never be committed to this repository.**

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

Production promotion fails closed if sanitization, module-graph completeness, fallback completeness, local-state preservation, capability fallbacks, regression checks, documentation-as-code, CI, installer integrity, or endpoint parity fail.

## Repository layout

```text
engine/          thin loader, module graph, modules and complete fallback runtime
contracts/       operating/export/storage/release/migration contracts
schemas/         provider-neutral workspace schemas
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
- Preserve local account state across upstream engine upgrades.
- Treat conversation context as cache when durable state exists.
- Newer high-confidence direct evidence supersedes stale inference.
- Recommendations are derived state and never become evidence for account facts.
- Shared gear is a transferable pool plus preset assignment, not permanent hero ownership.
- Volatile game/store/season facts are refreshed before consequential use.
- Every material engine change updates its relevant module/contract/schema/test in the same release.
- A consumer deployment must work even with no cloud connector, no automation support, or limited tools.
- GitHub holds shared sanitized engine state; private runtime workspaces hold player state.
- URL shortening is transport convenience only; canonical GitHub sources remain authoritative.
- A missing/bad module must never be repaired by overwriting local account state.

## Current production

**Engine version:** `2026-08-29.8`  
**Preferred install URL:** https://tinyurl.com/2yxf7f5x

Google Drive remains the reference private Prod-Dev/runtime implementation. GitHub is the authoritative sanitized Production engineering hub. End users normally need only the one-line install instruction above.