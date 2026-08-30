# LastWar Account Audit Engine (LWAI)

LWAI is a centrally maintained, modular Last War: Survival account-intelligence runtime designed to run through ChatGPT. Shared engine code and reusable sanitized knowledge live in GitHub Production; each user's private account state stays in their own supported storage workspace or, by explicit choice, the current chat session.

## Install

Paste this one line into a fresh ChatGPT conversation:

> Set up Last War optimization. Open https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main directly, use its current commit SHA, then retrieve and follow engine/BOOTSTRAP.txt from that exact SHA. Never use search-index/cached main copies; if live SHA resolution fails, stop rather than guessing.

That sentence is LWAI's **Stage-0 bootloader**. It resolves the live GitHub `main` commit first, then pins the entire bootstrap/update transaction to that immutable commit. Cached GitHub README/raw-main/search results cannot determine the active Production version.

**Do not use the old TinyURL installer.** It is retired. Some ChatGPT clients are still being sent to TinyURL's deprecated preview/interstitial, so the short link is no longer a supported installation dependency.

## Why the bootstrap is now intentionally tiny

The runtime is layered:

```text
Stage 0: installer sentence in the user's message
  -> resolve live GitHub main commit SHA
Stage 1: engine/BOOTSTRAP.txt at that exact SHA
  -> validate/pin release metadata and load mandatory modules
Stage 2: modules
  -> operating rules, persistence, accounts, guidance, updates, adapters and task-specific domains
```

`engine/BOOTSTRAP.txt` is orchestration only. It does not contain account onboarding scripts, storage-provider playbooks, season logic, gear strategy or other domain behavior. Those live in independently versioned modules and are pulled through the Production manifest.

The old 9 KiB loader ceiling was an internal CI guard, **not a ChatGPT/platform limit**. Production now enforces a stricter 4 KiB Stage-1 budget so policy cannot creep back into the loader. The correct response to loader bloat is delegation, not raising the ceiling.

## Evergreen update model

`release.resolver` is mandatory core. At install/startup/reload/update boundaries it resolves the current live GitHub `main` SHA. `release.updater` then reads `LATEST`, `MANIFEST`, `MIGRATIONS`, loader and required modules only from that exact immutable commit.

This means one base-layer fix cascades through the system on the next successful runtime freshness check. Existing deployments preserve last-known-good ENGINE and LOCAL STATE if current Production cannot be safely resolved. `refresh engine` remains the manual break-glass command and uses the same resolver transaction.

## Cloud persistence and explicit workspace-only security guardrails

Cloud persistence is optional but recommended for continuity, large audits, multi-account use and recovery. LWAI presents only providers/connectors actually available in the current host and requires an explicit choice; it never silently defaults to Google Drive.

Before authorization, LWAI must tell the user this explicitly:

> **LWAI is restricted to its own Last War workspace. It will not browse, read, change, move, delete, search, index or use anything else in your connected storage. Even if the connector technically exposes broader access, everything outside the LWAI workspace is off-limits to this tool.**

That includes personal files, sibling folders, other ChatGPT/app workspaces and unrelated documents. A broader provider permission surface is not permission for LWAI to use unrelated content.

Authentication happens in the provider/ChatGPT UI. LWAI never asks the user to paste passwords, OAuth codes, access/refresh tokens, cookies or credentials into chat. For Google Drive, users are told to approve the requested workspace access and choose **`Allow always`** if ChatGPT presents that option. Equivalent persistent authorization is recommended for other providers only when actually offered.

A user's `connected` message is not accepted as proof. LWAI re-checks capabilities, locates/creates only its dedicated workspace, verifies a harmless workspace-local read/write operation when appropriate, then confirms both the connection and the active workspace-only guardrail.

## Friendly first run

A new user is guided through:

`existing-state discovery -> storage choice -> identity -> account registration -> strategic baseline -> first evidence -> running optimization`

Every setup turn must end with a clear next action, an explicit `WAITING_USER` instruction such as `reply connected` / `reply done`, or a useful running-state landing. Infrastructure success is never a conversational dead end.

Existing users are discovered/migrated before broad onboarding and receive a recognizable loaded-account landing/resume. Durable setup checkpoints resume from the first incomplete verified stage after context loss rather than repeating storage/account creation.

## Evidence and anti-fabrication contract

LWAI does not invent Last War mechanics, numbers, costs, probabilities, formulas or factual recommendation inputs. Current direct in-game evidence and official sources take priority. Community evidence must be current, relevant, reputable and corroborated where material. Stale anecdotes, unsupported spreadsheets, recycled claims and low-quality reposts are weak evidence.

If a material fact cannot be validated after reasonable due diligence, LWAI says so. It may still provide the best bounded recommendation from supported inputs, but calculations/inference/heuristics are labeled as LWAI-derived analysis rather than official Last War guidance.

## Architecture

Mandatory core includes:

- `core.operating` — global evidence/provenance and optimization rules
- `core.persistence` — state boundaries, migration and recovery
- `core.accounts` — immutable account identity and isolation
- `core.guidance` — onboarding, guided capture and resumable audits
- `release.runtime` — release transaction behavior
- `release.resolver` — live-ref resolution and exact-commit pinning
- `release.updater` — automatic freshness/adoption
- `release.bootstrap` — startup handoff/orchestration

Capability adapters such as `adapters.storage` and domain modules such as Season Intelligence load only when needed.

`engine/BOOTSTRAP_FULL.txt` remains a complete sanitized standalone recovery fallback. Normal installs use the modular path.

## State separation

**GitHub Production contains:** sanitized runtime instructions, schemas, adapters, tests, release metadata/migrations and reusable non-user-specific reference assets.

**User-local LWAI workspace may contain:** private account identity, optional UID, screenshots/evidence, balances, battle history, Corrections/preferences, account databases, Audit Sessions, checkpoints/journal, provider metadata and compact engine-update metadata.

LWAI does not use unrelated connected-storage content.

## Current Production

**Engine version:** `2026-08-30.24`  
**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Channel:** Production  
**Sanitized public engine:** yes  
**Account state included:** no

## Production endpoints

- Live Production ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Stage-1 loader: `engine/BOOTSTRAP.txt`
- Module graph: `engine/MANIFEST.json`
- Release identity: `releases/LATEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Complete fallback: `engine/BOOTSTRAP_FULL.txt`

Production changes use short-lived RC branches, exact-head CI, validated-head merge and post-merge verification. Failed candidates leave `main` untouched.
