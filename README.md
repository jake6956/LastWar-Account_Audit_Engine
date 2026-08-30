# LastWar Account Audit Engine (LWAI)

LWAI is a centrally maintained, modular Last War: Survival account-intelligence runtime designed to run through ChatGPT. Shared sanitized engine code and reusable generic knowledge live in public GitHub Production. Private player/account state does not.

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

`engine/BOOTSTRAP.txt` is deliberately boring. It contains trust resolution, pinned-snapshot validation, generic mandatory-module loading, state-preservation rules and handoff. Provider onboarding, account strategy and game-domain behavior belong in modules.

Production enforces a **4 KiB** Stage-1 budget plus structural tests that prevent feature policy from leaking back into the loader.

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

## Intended user experience

LWAI should feel like a **friendly expert Last War technician walking the player through the account with a clipboard**: progressively collecting the smallest useful stats and metrics, explaining what matters, and turning the account model into concrete recommendations intended to make the player as strong and effective as practical for their goals.

The user may challenge a recommendation, ask why, choose a different strategy, or ask an entirely different Last War question at any time. LWAI should answer the current question to the best supported level possible rather than forcing the user to finish onboarding first. Unfinished durable upload/authorization boundaries are preserved instead of silently discarded.

## Friendly first run and no dead air

A genuinely new user is guided through:

`existing-state discovery -> storage choice -> identity -> account registration -> strategic baseline -> first evidence -> running optimization`

The mandatory `core.flow-continuity` module enforces that every setup/recovery response ends with a concrete next action, an explicit WAITING_USER instruction, or useful running work. Technical statuses such as `connected`, `workspace verified`, `account loaded`, `updated`, or `Ready.` cannot be terminal responses by themselves.

A user returning `connected` after provider authorization is rechecked and verified internally, then the **same user-facing response** advances to identity, existing-account resume, or the original pending task. Verification failure offers retry, another provider, or session-only. Durable onboarding stages map to explicit resume prompts so an interrupted conversation never silently stalls or restarts already-verified setup.

## Storage provider policy

Cloud persistence is recommended but optional.

**Google Drive is LWAI's preferred/recommended and most-tested consumer storage provider when it is actually available with verified writable capability.** It should be shown first and labeled Recommended. The user still explicitly chooses it; preferred does not mean silently selected.

Every other provider genuinely supported by the current host and `storage-api/1` capability checks is also offered and supported, including Dropbox, OneDrive / Microsoft 365, Box when writable, or another verified writable provider. A verified alternative is a real persistence target, not a decorative fallback.

## Cloud workspace security

Before storage authorization LWAI must explain the application boundary clearly:

> **LWAI is explicitly restricted to its own Last War workspace. I will not browse, read, change, move, delete, search, index or use anything else in your connected storage. Even if the connector technically exposes broader access, everything outside the LWAI workspace is off-limits to this tool.**

This **workspace-only** boundary is a runtime rule, not merely reassurance. Authentication happens in the provider/ChatGPT UI; LWAI never asks the user to paste passwords, OAuth codes, access/refresh tokens, cookies or credentials into chat. Google Drive users are told to choose **`Allow always`** only when ChatGPT actually offers that option.

A user saying `connected` triggers capability re-checking; it is not accepted as proof. LWAI verifies its isolated workspace before claiming durable persistence, then immediately continues the pending onboarding/resume flow rather than stopping at a connection status.

## Data placement / privacy boundary

**Public GitHub:** sanitized engine instructions/code, manifests, schemas, adapters, tests, release metadata/migrations and reusable non-user-specific knowledge only.

**Maintainer private Google Drive:** maintainer-controlled private/Prod-Dev account state, private operational records and the private recovery/failsafe mirror. This private Drive is not a consumer backend and is not Production version authority.

**Each end user's personal provider:** that user's private account identity/optional UID, screenshots/evidence, balances, history, Corrections/preferences, account databases, Audit/Runtime Sessions, checkpoints/journal, provider metadata and compact engine-update metadata—inside that user's designated Last War/LWAI workspace only.

Consumer data is never routed through the maintainer's Drive, GitHub, another user's workspace or unrelated folders in the consumer's connected provider. Direct files/screenshots a user deliberately supplies in chat are task input only; they do not expand cloud-storage scope.

Engine updates do not rewrite LOCAL STATE unless a separately validated schema migration requires it.

## Knowledge and evidence policy

LWAI should use current relevant information available through its research tools rather than relying on one site or model memory. Evidence preference is:

`current direct in-game evidence -> current official Last War/publisher material -> reputable maintained tools/databases/guides -> independently corroborated community testing/consensus -> clearly labeled LWAI calculation/inference`

Maintained community projects such as **LastWarTutorial.com** and **cpt-hedge.com** are useful research sources. Reddit communities such as **r/LastWarMobileGame** are useful for observations, edge cases and newly surfaced changes.

Community material is not gospel. Material mechanics, numbers, costs, probabilities, event rules, expensive/irreversible choices and contested claims should be independently checked against current official/in-game evidence when available and corroborated with other credible current sources. If official material is silent, LWAI should seek multiple independent current sources and compare them with direct user evidence.

If a material claim cannot be validated to high confidence after reasonable due diligence, LWAI says so when using it rather than manufacturing certainty. Unofficial advice is never labeled official merely because it is popular.

## Season Intelligence

Season-specific knowledge is modular. Generic sanitized season packs accelerate research, while stale/dynamic/consequential mechanics are reverified when needed. Direct current in-game evidence beats stale shared knowledge. Private user observations do not automatically flow into public GitHub assets.

## Current Production candidate

**Engine version:** `2026-08-30.26`  
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

Production changes use RC branches, exact-head CI, validated-head merge and post-merge verification. Failed candidates leave `main` untouched, and the private Google Drive failsafe must be synchronized to the exact frozen candidate before promotion.