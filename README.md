# LastWar Account Audit Engine (LWAI)

LWAI is a portable, self-healing account optimization framework for **Last War: Survival**. It turns screenshots, terse account updates, current mechanics, resource constraints, and battle evidence into a continuously reconciled account model and decisive upgrade recommendations.

## Install / distribution

The easiest consumer install is the stable public bootstrap document:

**LWAI — PUBLIC BOOTSTRAP — LATEST**  
https://docs.google.com/document/d/1Mhg8YXX9jaZJVry5ZZ6_5d-xbE7A4A0tnfQVgFI2WC8/edit

Copy the entire bootstrap into a fresh ChatGPT conversation. For best results, switch reasoning/thinking to **HIGH** if the product exposes that control. Cloud persistence is strongly recommended but optional.

## Hub-and-spoke architecture

### Production engineering hub — this repository
This repository contains only sanitized, production-safe engine material:
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

## Release model

`Prod-Dev (private) -> Release Candidate -> Production (GitHub) -> stable public bootstrap mirror`

Production promotion fails closed if sanitization, bootstrap completeness, local-state preservation, capability fallbacks, regression checks, documentation-as-code, or endpoint integrity fail.

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

## Current production

**Engine version:** `2026-08-29.5`  
**Stable consumer endpoint:** https://docs.google.com/document/d/1Mhg8YXX9jaZJVry5ZZ6_5d-xbE7A4A0tnfQVgFI2WC8/edit

Google Drive remains the reference Prod-Dev/runtime implementation. GitHub is the sanitized production engineering hub. The Google Doc above is intentionally the simplest consumer-facing distribution path so users do not need GitHub knowledge to install LWAI.
