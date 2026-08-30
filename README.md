# LastWar Account Audit Engine (LWAI)

LWAI is a centrally maintained, modular Last War: Survival account-intelligence runtime designed to run through ChatGPT. Shared sanitized engine code and reusable generic knowledge live in GitHub Production. Private player/account state stays in the user's supported private workspace or, by explicit choice, the current chat session.

## Install

The permanent public installer is:

> Set up Last War optimization using the instructions at https://lastwarai.com

`https://lastwarai.com` is LWAI's first-party **Stage-0 bootloader** entrypoint. It serves a tiny bootstrap locator that tells the assistant to resolve the live GitHub Production `main` ref at:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

The assistant obtains the current `commit.sha`, then retrieves `engine/BOOTSTRAP.txt` and the rest of the engine from that exact immutable commit. The public domain is stable human-facing transport; it is **not** current-version authority.

The previously circulated `https://tinyurl.com/2yxf7f5x` is retained only as a legacy compatibility alias. New sharing must use LastWarAI.com. A shortener, redirect, README cache, search result, mutable raw `main` response or model memory never establishes the current Production version.

### Legacy repository-installer compatibility

If an assistant reaches this repository because a user supplied an older repository-based installer, do not stop at the README or ask the user to paste another prompt. Resolve the live GitHub `main` SHA and continue through the exact-commit Stage-1 loader.

## Bootstrap architecture

```text
Stage 0 — https://lastwarai.com
  -> tiny stable first-party locator
  -> resolve live GitHub main commit C

Stage 1 — engine/BOOTSTRAP.txt at C
  -> validate one pinned release snapshot
  -> load every MANIFEST module with required:true
  -> hand off to MANIFEST entrypoint_module

Stage 2 — mandatory modules
  -> release.dispatcher evaluates MANIFEST activation metadata
  -> load only task/event/capability-relevant optional modules + dependencies

Stage 3 — normal LWAI work
  -> account optimization, storage, recovery, season intelligence, future features
```

`engine/BOOTSTRAP.txt` is deliberately boring. It contains trust resolution, pinned-snapshot validation, generic mandatory-module loading, state-preservation rules and handoff. It does not contain provider onboarding, season logic, gear strategy or a feature list.

The old 9 KiB loader ceiling was an internal LWAI CI guard, not a ChatGPT/platform limit. Production enforces a stricter **4 KiB** Stage-1 budget plus structural tests that prevent feature policy from leaking back into the loader.

## The cascade rule

`engine/MANIFEST.json` is the application's integration surface.

- Every `required:true` module is loaded automatically in dependency order.
- `entrypoint_module` defines the post-load handoff.
- Optional modules declare activation metadata: relevant intents, runtime events and/or required host capabilities.
- `release.dispatcher` selects the smallest relevant optional module set and recursively loads dependencies.
- CI rejects orphan module files, duplicate registrations, broken dependency graphs and optional modules without routing metadata.

A new Production feature therefore does not require a new installer. Add/version the module, register dependencies and activation metadata in MANIFEST, pass release gates, and the existing runtime discovers it automatically.

## Evergreen updates

`release.resolver` is mandatory core. On install/startup/reload/update boundaries it resolves live GitHub `main` and pins candidate reads to one exact commit. `release.updater` adopts only a compatible, validated Production release.

Existing deployments preserve last-known-good ENGINE and LOCAL STATE when current Production cannot be safely resolved. `refresh engine` remains the permanent manual break-glass command and uses the same resolver/update transaction. There is no background-daemon claim: a dormant conversation updates on the next supported interaction.

## Friendly first run

A genuinely new user is guided through:

`existing-state discovery -> storage choice -> identity -> account registration -> strategic baseline -> first evidence -> running optimization`

Cloud storage is optional. LWAI shows only storage providers actually available in the environment and requires explicit provider choice; it never silently defaults to Google Drive. Existing users are discovered/migrated before broad onboarding and receive a recognizable loaded-account landing/resume.

## Cloud workspace security

Before storage authorization LWAI must explain the application boundary clearly:

> **LWAI is explicitly restricted to its own Last War workspace. I will not browse, read, change, move, delete, search, index or use anything else in your connected storage. Even if the connector technically exposes broader access, everything outside the LWAI workspace is off-limits to this tool.**

This **workspace-only** boundary is a runtime rule, not merely reassurance. Authentication happens in the provider/ChatGPT UI; LWAI never asks the user to paste passwords, OAuth codes, access/refresh tokens, cookies or credentials into chat. Google Drive users are told to choose **`Allow always`** only when ChatGPT actually offers that option.

A user saying `connected` triggers capability re-checking; it is not accepted as proof. LWAI verifies its isolated workspace before claiming durable persistence.

## Evidence and anti-fabrication

LWAI does not invent Last War mechanics, numbers, costs, probabilities, formulas or factual recommendation inputs. Evidence preference is current direct game evidence -> current official sources -> reputable maintained references -> validated current community testing/consensus -> clearly labeled LWAI calculation/inference.

Weak, stale, unsupported or contradictory community claims are not silently treated as facts. If a consequential mechanic cannot be validated after reasonable due diligence, LWAI says so and provides only bounded analysis with assumptions identified.

## Season Intelligence

Season-specific knowledge is modular. Generic sanitized season packs accelerate research, while stale/dynamic/consequential mechanics are reverified when needed. Direct current in-game evidence beats stale shared knowledge. Private user observations do not automatically flow into public GitHub assets.

## State separation

**GitHub Production:** sanitized engine instructions, manifests, schemas, adapters, tests, release metadata/migrations and reusable non-user-specific knowledge.

**User-local LWAI workspace:** private account identity/optional UID, screenshots/evidence, balances, history, Corrections/preferences, account databases, Audit/Runtime Sessions, checkpoints/journal, provider metadata and compact engine-update metadata.

Engine updates do not rewrite LOCAL STATE unless a separately validated schema migration requires it.

## Current Production candidate

**Engine version:** `2026-08-30.25`  
**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Bootstrap protocol:** `2.0`  
**Module selection:** `manifest_activation_v1`  
**Sanitized public engine:** yes  
**Account state included:** no

## Production endpoints

- Public installer: `https://lastwarai.com`
- Legacy compatibility alias: `https://tinyurl.com/2yxf7f5x`
- Live Production ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Stage-1 loader: `engine/BOOTSTRAP.txt`
- Module graph/router metadata: `engine/MANIFEST.json`
- Release identity: `releases/LATEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Complete standalone fallback: `engine/BOOTSTRAP_FULL.txt`

Production changes use RC branches, exact-head CI, validated-head merge and post-merge verification. Failed candidates leave `main` untouched.
