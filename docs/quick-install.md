# LWAI Quick Install

## Copy this one line

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

Paste it into a fresh ChatGPT conversation. A web-capable assistant should retrieve the sanitized Production thin loader itself. You should not need to copy/paste the full standalone runtime.

## What happens next
1. The instruction authorizes retrieval of the linked loader.
2. The assistant treats the short-link body as transport only and re-checks canonical GitHub `LATEST.json`, `BOOTSTRAP.txt`, `MANIFEST.json` and `MIGRATIONS.json`; stale/cached alias content cannot downgrade verified Production.
3. It verifies sanitized Production identity and confirms account state is not embedded.
4. It capability-detects persistence/ingestion features rather than assuming them.
5. It discovers existing Workspace Registry/legacy state before onboarding and resolves the correct private account context.
6. If a supported older workspace is schema `2.1` or `2.2`, migration-capable core/release/storage behavior applies the validated additive path to current schema `2.3` while preserving canonical account state. Domain modules requiring `2.3` stay unloaded until migration verifies.
7. Recovery-first and migration-first reconciliation then resume existing work/state. Only a genuinely new deployment begins phased onboarding.

No validated workspace-schema path means setup pauses with existing state untouched; it does not guess a conversion or start the user over.

## Canonical sources
The short URL is transport convenience only. GitHub `main` is authoritative.

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

Fallback order is short alias -> canonical loader -> last-known-good compatible engine when available -> complete GitHub fallback -> readable legacy mirror -> manual full-runtime transfer. When alias content and canonical GitHub disagree, canonical GitHub wins rather than falling backward to the alias body.

## Existing-user compatibility
Current workspace schema is `2.3`. Supported historical transitions are:
- `2.1 -> 2.2`: optional guidance metadata and account-scoped Audit Sessions;
- `2.2 -> 2.3`: optional Runtime Checkpoints and append-only Runtime Journal.

Both are additive/idempotent and preserve Workspace Registry, immutable account identity, active account routing, canonical game facts/history, Corrections, evidence metadata and provider references. They do not require re-onboarding or account rewrite.

## Privacy
Public Production contains shared sanitized engine behavior only. Account identity, optional game UID, screenshots, balances, corrections, battles, sessions, recovery rows and provider-local references remain in the user's own environment. LWAI does not require game passwords/session tokens/authentication captures for normal operation.

## Offline / recovery install
Use `export yourself` to obtain the complete sanitized `BOOTSTRAP_FULL` runtime when a self-contained copy is required.
