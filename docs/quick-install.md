# LWAI Quick Install

## Copy this one line

`Set up Last War optimization using the installation instructions at https://github.com/jake6956/LastWar-Account_Audit_Engine`

Paste it into a fresh ChatGPT conversation. The canonical GitHub repository README is the installation entrypoint and hands the assistant to `main/engine/BOOTSTRAP.txt`. A web-capable assistant should execute the sanitized Production loader itself; the user should not need to copy/paste the full standalone runtime.

Third-party URL shorteners are not required. A legacy TinyURL previously used for convenience began serving a deprecated preview/interstitial to some ChatGPT clients and is retired as an installation dependency.

## What happens next
1. The repository README directs ChatGPT to canonical `main/engine/BOOTSTRAP.txt` rather than acting as a documentation-only endpoint.
2. The assistant fetches canonical GitHub `LATEST.json`, `BOOTSTRAP.txt`, `MANIFEST.json` and `MIGRATIONS.json`; supplied aliases/caches are non-authoritative and cannot downgrade verified Production.
3. It verifies sanitized Production identity and confirms account state is not embedded.
4. It runs the automatic freshness/update preflight before ordinary account/domain work.
5. It capability-detects persistence/ingestion features rather than assuming them.
6. It discovers existing Workspace Registry/legacy state before onboarding and resolves the correct private account context.
7. If a supported older workspace is schema `2.1` or `2.2`, migration-capable core/release/storage behavior applies the validated additive path to current schema `2.3` while preserving canonical account state. Domain modules requiring `2.3` stay unloaded until migration verifies.
8. Existing users then run recovery-first/migration-first reconciliation and resume their state.
9. A genuinely new user is asked whether to use private cloud storage before identity intake. If yes, LWAI presents only supported providers and requires an explicit choice; if no, it continues session-only immediately.
10. After provider authorization, LWAI re-checks actual read/create/write capability before claiming persistence. Successful storage immediately advances to identity -> strategic baseline -> first useful evidence capture; it does not stop at a connection receipt.

Existing users with a valid workspace are not redundantly prompted for first-run storage setup. Read-only providers do not count as durable persistence.

If session-only was chosen, LWAI may later re-offer cloud storage only when the current workflow has a concrete durability benefit, such as a large audit, resumable upload boundary, multi-account work, substantial newly captured state, planned continuation in another chat/device, or a recovery limitation. It does not interrupt trivial work. Reminders are limited to once per runtime session; when reliable cross-session metadata exists, a seven-day minimum cooldown applies. `don't ask again` suppresses future benefit-triggered reminders until the user explicitly reopens persistence setup.

No validated workspace-schema path means setup pauses with existing state untouched; it does not guess a conversion or start the user over.

## Staying current
With web access, LWAI performs a lightweight canonical GitHub `LATEST.json` freshness check at every runtime/session startup before ordinary domain work. During a long-lived runtime it checks again before consequential work after six hours since the last successful canonical check. This is a metadata check, not a full re-download on every message.

When a newer verified Production exists, LWAI preserves private/local state, validates canonical release/module/migration metadata and compatibility/integrity, applies only validated migrations, then refreshes ENGINE and changed modules. It never auto-loads RC/Prod-Dev and never downgrades because an alias/cache is stale. `refresh engine` or `check for LWAI updates` forces the same check immediately.

## Canonical sources
GitHub `main` is both the installation authority and Production trust root.

Repository / public installer:
https://github.com/jake6956/LastWar-Account_Audit_Engine

Loader:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt

Release metadata:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json

Module graph:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json

Migration graph:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/MIGRATIONS.json

Complete standalone fallback:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt

Fallback order is repository README handoff -> canonical raw loader -> last-known-good compatible engine -> complete GitHub fallback -> manual full-runtime transfer. Third-party shorteners and the retired Google runtime mirror are not required.

## Existing-user compatibility
Current workspace schema is `2.3`. Supported historical transitions are:
- `2.1 -> 2.2`: optional guidance metadata and account-scoped Audit Sessions;
- `2.2 -> 2.3`: optional Runtime Checkpoints and append-only Runtime Journal.

Both are additive/idempotent and preserve Workspace Registry, immutable account identity, active account routing, canonical game facts/history, Corrections, evidence metadata and provider references. They do not require re-onboarding or account rewrite.

## Privacy
Public Production contains shared sanitized engine behavior only. Account identity, optional game UID, screenshots, balances, corrections, battles, sessions, recovery rows and provider-local references remain in the user's own environment. LWAI does not require game passwords/session tokens/authentication captures for normal operation.

## Offline / recovery install
Use `export yourself` to obtain the complete sanitized `BOOTSTRAP_FULL` runtime when a self-contained copy is required.
