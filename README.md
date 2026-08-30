# LastWar Account Audit Engine (LWAI)

LWAI is a modular account-intelligence and optimization runtime for **Last War: Survival**. ChatGPT is the conversational interface; the shared engine is centrally maintained here; user-specific state stays in the user's own supported storage or, by explicit choice, in the current session only.

## Install

Paste this single instruction into a fresh ChatGPT conversation:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

The short URL is only a convenience alias. Canonical GitHub `main` is authoritative; stale alias/cache content cannot downgrade a newer verified release. There is one **single public installer** and one Production line.

For best results, use a higher reasoning/thinking setting when the ChatGPT interface offers one.

## Friendly first run

LWAI first looks for an existing Workspace Registry, legacy LWAI state, supported snapshots/exports, and available persistence capabilities. Existing users resume or migrate before broad onboarding.

A genuinely new user is asked an early plain-language question before identity/account intake:

> Before we build your account, would you like me to use private cloud storage so I can safely pick up where we left off in future chats? It’s recommended, but optional. Reply yes or no.

If the answer is **no**, LWAI continues session-only.

If the answer is **yes**, LWAI detects storage providers/connectors that are actually available or installable and shows a short provider menu. The user explicitly chooses the provider. LWAI does **not** silently default to Google Drive.

Typical choices, only when genuinely supported by the current host, may include Google Drive, Dropbox, OneDrive / Microsoft 365, Box when writable, or another verified writable provider. Read-only storage is reference-only and is not treated as durable persistence.

After the user chooses a provider, LWAI gives concise authorization instructions. For Google Drive, the user is told to approve the requested Drive file access and choose **`Allow always`** if ChatGPT presents that option. For other providers, LWAI follows the actual host/provider wording and recommends the equivalent persistent authorization option only when it is genuinely shown. LWAI never asks the user to paste provider passwords, OAuth codes or tokens into chat.

A user saying `connected` is not accepted as proof. LWAI re-checks capability and verifies the private workspace before reporting `Cloud storage connected and verified.`

If a session-only user later accepts a contextual persistence reminder—or says `connect storage`—LWAI runs the same provider chooser, authorization and verification flow again. It never jumps directly to Google Drive. Existing reminder limits remain: only when cloud materially benefits the current workflow, max once per runtime session, a seven-day cooldown when reliable cross-session metadata exists, and explicit suppression with `don't ask again`.

## Friendly bootstrap and update UX

The bootstrap source contains technical trust, integrity, compatibility, migration and recovery logic, but normal users do not need to watch it scroll by. LWAI executes that machinery internally and uses short status only when useful, such as:

- `Getting LWAI ready…`
- `Checking for updates…`
- `Looking for saved account data…`
- `Cloud storage connected and verified.`
- `LWAI updated successfully.`
- `Ready.`

Fast/no-op work may be silent. URLs, module names, hashes, schema/API numbers, migration graphs, RC terminology and detailed traces are reserved for `audit yourself`, explicit developer/debug requests, or failure details required for recovery.

## What LWAI does

LWAI builds and continuously reconciles a model of a player's account from screenshots, terse updates, current mechanics, resource constraints, battle evidence and user corrections. It uses that model to produce practical upgrade priorities, research plans, formation advice and account-wide optimization recommendations.

A player can provide compact updates such as a skill level, gear level or resource balance without completing a formal intake. LWAI updates only affected state and recomputes only what materially changed.

## Architecture

```text
engine/BOOTSTRAP.txt
  -> releases/LATEST.json
  -> engine/MANIFEST.json
  -> releases/MIGRATIONS.json
     -> mandatory core/release modules
        -> release.updater
     -> task-specific domain modules
     -> capability-specific adapters

engine/BOOTSTRAP_FULL.txt
  -> complete standalone fallback
```

The thin loader is bounded orchestration rather than a game-domain monolith. Mandatory core behavior loads first; domain modules load only when needed. `release.updater` is mandatory core and owns automatic consumer engine-update orchestration.

## Existing users and migration

LWAI discovers supported prior state before onboarding. Current registry-backed users resume their existing immutable account identity and canonical database; older pre-registry single-account deployments are registered nondestructively rather than rebuilt.

Production supports explicit workspace-schema migration for supported older deployments:

- schema `2.1 -> 2.2`: optional guidance metadata and Audit Sessions;
- schema `2.2 -> 2.3`: optional Runtime Checkpoints and Runtime Journal.

These migrations are additive and idempotent. They preserve canonical account facts, immutable `account_id`, `active_account_id`, history, Corrections, evidence metadata and provider references. Domain modules that require schema `2.3` remain blocked until migration is verified. If no validated path exists, setup fails closed instead of guessing or re-onboarding the user.

## Persistence model

**GitHub Production contains:** sanitized runtime instructions/modules, provider-neutral schemas/adapters, release metadata/migrations, tests/documentation, and reusable non-user-specific reference assets.

**User-local storage may contain:** account identity/game state, screenshots/evidence, balances/battle history, local corrections/preferences, audit/recovery state, optional runtime-session provenance, selected-provider metadata, and compact workspace-level engine-update metadata.

Private account data and actual runtime-session/host-conversation references are never required in this public repository.

Persistence is capability-driven, not provider-name-driven. An adapter reports verified read/list/create/write/query/atomic-append/CAS/snapshot/restore capability and LWAI selects the strongest safe profile available. Recovery journals require actual atomic append, revision/CAS semantics, or immutable uniquely identified events.

## Multi-account, provenance and recovery

Persistent deployments can manage multiple isolated accounts under a workspace registry. Each account receives immutable LWAI-generated `account_id`; screenname, server, alliance, nickname and optional game UID remain private.

The runtime supports account switching, nondestructive archive/restore, migration-first startup, resumable audits and verify-before-replay checkpoints. Optional `runtime_session_id` provenance may be stored privately; a host conversation/session reference is optional and non-authoritative. It is never account identity, authentication, routing, recovery ordering or write deduplication.

LWAI does not require game passwords, provider passwords, session tokens, cookies, OAuth codes or authentication captures for normal operation.

## Automatic updates and self-healing

Production updates are centrally published through GitHub and automatically pulled by web-capable deployments. `release.updater` checks canonical `releases/LATEST.json`:

- on every runtime/session startup before ordinary account/domain work;
- before `reload LWAI` / `reload yourself`;
- before schema-sensitive migration/recovery when compatibility matters;
- before consequential work in a long-lived runtime once at least six hours have elapsed since the last successful canonical check.

If installed Production is current, the check is silent. If a newer verified Production exists, LWAI preserves LOCAL STATE, validates channel/privacy/API/schema/migration/integrity metadata, fetches changed required engine components, applies only validated migrations, health-checks, adopts the newer ENGINE, then resumes the user's original pending action.

Failed update verification never partially activates a candidate. LWAI retains last-known-good compatible engine state or the complete `BOOTSTRAP_FULL.txt` fallback and leaves private account state untouched. It never auto-loads RC/Prod-Dev and never downgrades because an alias/cache is stale.

Automatic updating does not imply a background daemon. A dormant ChatGPT conversation updates on the next user interaction unless the user separately opts into an actually available scheduler.

`refresh engine` remains the permanent backwards-compatible manual escape hatch and bypasses freshness TTLs to force the same canonical update transaction. `check for LWAI updates` is an alias.

## Validation

Production CI performs structural validation plus executable deterministic regressions. Gates cover release/version parity, module graph and byte integrity, privacy markers, loader boundaries, compatibility, first-run persistence choice, explicit provider selection, provider permission coaching, Google Drive `Allow always` guidance, post-authorization capability verification, contextual persistence reminders, friendly bootstrap/update UX, automatic engine updating, permanent `refresh engine` compatibility, account isolation, archive/start-over, migration preservation, runtime-session provenance, `WAITING_USER`, verify-before-replay, checkpoint loss, append-only journal semantics, provider degradation and historical workspace-schema migration.

## Production endpoints

- Release metadata: `releases/LATEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Thin loader: `engine/BOOTSTRAP.txt`
- Module graph: `engine/MANIFEST.json`
- Complete fallback: `engine/BOOTSTRAP_FULL.txt`
- Install alias: https://tinyurl.com/2yxf7f5x

## Release discipline

Production changes use short-lived RC branches with sanitization checks, exact-head PR CI, validated-head merge and post-merge verification. Failed candidates leave `main` untouched.

## Current Production

**Engine version:** `2026-08-29.19`

**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Channel:** Production  
**Sanitized public engine:** yes  
**Account state included:** no
