# LastWar Account Audit Engine (LWAI)

LWAI is a centrally maintained, modular Last War: Survival account-intelligence runtime designed to run through ChatGPT. Shared sanitized engine code and reusable generic knowledge live in GitHub Production. Private player/account state stays in the user's supported private workspace or, by explicit choice, the current chat session.

## Install

Paste this one line into a fresh ChatGPT conversation:

> Set up Last War optimization. Read the live GitHub main ref at https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main, use its current commit.sha, then load and follow engine/BOOTSTRAP.txt from that exact commit.

That sentence is LWAI's **Stage-0 bootloader**. It obtains the live current commit SHA (`commit.sha`) first. Every engine file used for that startup is then read from that same immutable commit.

**Do not use the old TinyURL installer.** It is retired. A shortener, README cache, search result, or mutable raw `main` response is never the authority for the current Production version.

## Bootstrap architecture

```text
Stage 0 — stable one-line installer
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

`engine/BOOTSTRAP.txt` is deliberately boring. It contains trust resolution, pinned-snapshot validation, generic mandatory-module loading, state-preservation rules and handoff. It does **not** contain Google Drive instructions, account onboarding scripts, season logic, gear strategy or a list of today's product features.

The old **9 KiB loader ceiling was an internal LWAI CI guard, not a ChatGPT/platform limit**. Production now enforces a stricter 4 KiB Stage-1 budget *plus* structural tests that prevent feature policy from leaking back into the loader. The point is delegation, not squeezing more prose into the bootloader.

## The cascade rule

`engine/MANIFEST.json` is the application's integration surface.

- Every `required:true` module is loaded automatically in dependency order.
- `entrypoint_module` defines the post-load handoff.
- Every optional module declares activation metadata: relevant intents, runtime events and/or required host capabilities.
- `release.dispatcher` selects the smallest relevant optional module set and recursively loads dependencies.
- CI rejects orphan module files, duplicate registrations, broken dependency graphs and optional modules without routing metadata.

Therefore a new Production feature does **not** require a new installer or Stage-1 edit. Add/version the module, register its dependencies and activation metadata in MANIFEST, pass release gates, and the existing runtime can discover it automatically.

## Evergreen updates

`release.resolver` is mandatory core. On install/startup/reload/update boundaries it resolves live GitHub `main` and pins candidate reads to one exact commit. `release.updater` checks Production at the defined freshness boundaries and adopts only a compatible, validated release.

Existing deployments preserve last-known-good ENGINE and LOCAL STATE when current Production cannot be safely resolved. `refresh engine` remains the permanent manual break-glass command and uses the same resolver/update transaction.

There is no claim of a background daemon: a dormant conversation updates on the next supported interaction.

## Friendly first run

A genuinely new user is guided through:

`existing-state discovery -> storage choice -> identity -> account registration -> strategic baseline -> first evidence -> running optimization`

Cloud storage is optional. LWAI must show only storage providers actually available in the current environment and require the user to choose one; it never silently defaults to Google Drive. Provider authorization and onboarding behavior live in modules, not the bootloader.

Every incomplete setup turn ends with a clear next action or explicit `WAITING_USER` instruction such as `reply connected` or `reply done`. Infrastructure success is never a conversational dead end. Existing users are discovered/migrated before broad onboarding and receive a recognizable loaded-account landing/resume.

## Cloud workspace security

Before storage authorization LWAI must explain the application boundary clearly:

> **LWAI is explicitly restricted to its own Last War workspace. I will not browse, read, change, move, delete, search, index or use anything else in your connected storage. Even if the connector technically exposes broader access, everything outside the LWAI workspace is off-limits to this tool.**

That includes personal files, sibling folders, other ChatGPT/app workspaces and unrelated provider content. Broader connector visibility is not permission for provider-wide exploration.

Authentication happens in the provider/ChatGPT UI. LWAI never asks the user to paste passwords, OAuth codes, access/refresh tokens, cookies or credentials into chat. Google Drive users are told to choose **`Allow always`** when ChatGPT actually offers that option. Equivalent persistent authorization is recommended for other providers only when genuinely available.

A user saying `connected` triggers capability re-checking; it is not accepted as proof. LWAI verifies its isolated workspace before claiming durable persistence.

## Evidence and anti-fabrication

LWAI does not invent Last War mechanics, numbers, costs, probabilities, formulas or factual recommendation inputs. Evidence preference is current direct game evidence -> current official sources -> reputable maintained references -> validated current community testing/consensus -> clearly labeled LWAI calculation/inference.

Weak, stale, unsupported or contradictory community claims are not silently treated as facts. If a consequential mechanic cannot be validated after reasonable due diligence, LWAI says so and may provide only a bounded recommendation with its assumptions/inference identified as LWAI-derived analysis rather than official Last War guidance.

## Season Intelligence

Season-specific knowledge is modular. Generic sanitized season packs accelerate research, while stale/dynamic/consequential mechanics are reverified when needed. Direct current in-game evidence beats stale shared knowledge. Private user observations do not automatically flow into public GitHub assets.

Future season modules and knowledge packs join the runtime through the same MANIFEST cascade rather than bootloader edits.

## State separation

**GitHub Production:** sanitized engine instructions, manifests, schemas, adapters, tests, release metadata/migrations and reusable non-user-specific knowledge.

**User-local LWAI workspace:** private account identity/optional UID, screenshots/evidence, balances, history, Corrections/preferences, account databases, Audit/Runtime Sessions, checkpoints/journal, provider metadata and compact engine-update metadata.

Engine updates do not rewrite LOCAL STATE unless a separately validated schema migration requires it.

## Current Production candidate

**Engine version:** `2026-08-30.24`  
**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Bootstrap protocol:** `2.0`  
**Module selection:** `manifest_activation_v1`  
**Sanitized public engine:** yes  
**Account state included:** no

## Production endpoints

- Live Production ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Stage-1 loader: `engine/BOOTSTRAP.txt`
- Module graph/router metadata: `engine/MANIFEST.json`
- Release identity: `releases/LATEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Complete standalone fallback: `engine/BOOTSTRAP_FULL.txt`

Production changes use RC branches, exact-head CI, protected validated-head merge and post-merge verification. Failed candidates leave `main` untouched.
