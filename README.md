# LastWar Account Audit Engine (LWAI)

LWAI is a portable, self-healing account optimization framework for **Last War: Survival**. It turns screenshots, terse account updates, current mechanics, resource constraints, and battle evidence into a continuously reconciled account model and decisive upgrade recommendations.

## One-line install

The preferred consumer install is now:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

Paste that single line into a fresh ChatGPT conversation. The assistant should retrieve the Production bootstrap itself, validate it, and begin phased onboarding. No multi-page mobile copy/paste is required when web access works.

The short URL is a convenience/distribution alias, not the trust root. It resolves to the canonical raw Production bootstrap on GitHub. Direct sources remain:
- Latest manifest: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
- Raw bootstrap: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt
- Legacy/secondary Google mirror: https://docs.google.com/document/d/1Mhg8YXX9jaZJVry5ZZ6_5d-xbE7A4A0tnfQVgFI2WC8/edit

For best results, switch reasoning/thinking to **HIGH** if the product exposes that control. Cloud persistence is strongly recommended but optional.

## Distribution privacy

Normal sharing uses the neutral short URL so the repository owner/maintainer handle is not exposed in the visible end-user install instruction. This is intentionally **semi-anonymous convenience, not true anonymity**: anyone who resolves the short link can discover the public GitHub repository and provenance.

## Hub-and-spoke architecture

### Production engineering hub — this repository
This repository is the authoritative sanitized Production engineering source and contains only production-safe engine material:
- compiled bootstrap source
- runtime/behavior contracts
- provider-neutral schemas
- storage adapters and fallbacks
- regression/release tests
- release manifests and changelog
- migration notes
- production-qualified Gold Asset metadata
- developer/operator documentation

### Private runtime spoke — each player deployment
Each player keeps private state in their own environment:
- account facts and screenshots
- hero/gear/tech/resource state
- presets and formations
- battle history and local corrections
- Hot Cache / State Health / staleness metadata
- provider credentials and local file paths

**Private player state must never be committed to this repository.**

### Distribution endpoints
The TinyURL alias is the preferred human-facing bootstrap entrypoint. GitHub raw Production is authoritative. The stable Google Doc remains a secondary/legacy distribution fallback for environments where it is readable.

## Release model

`Prod-Dev (private) -> Release Candidate -> Production (GitHub) -> remote install endpoints / mirrors`

Production promotion fails closed if sanitization, bootstrap completeness, local-state preservation, capability fallbacks, regression checks, documentation-as-code, CI, short-link integrity, or endpoint parity fail.

## Repository layout

```text
engine/          complete bootstrap/runtime source
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
- Every material engine change updates its relevant contract/schema/test in the same release.
- A consumer deployment must work even with no cloud connector, no automation support, or limited tools.
- GitHub holds shared engine state; private runtime workspaces hold player state.
- URL shortening is transport convenience only; canonical GitHub sources remain authoritative.

## Current production

**Engine version:** `2026-08-29.7`  
**Preferred install URL:** https://tinyurl.com/2yxf7f5x

Google Drive remains the reference private Prod-Dev/runtime implementation. GitHub is the authoritative sanitized Production engineering hub. End users normally need only the one-line install instruction above.
