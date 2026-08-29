# LWAI Quick Install

## Copy this one line

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

Paste it into a fresh ChatGPT conversation. A web-capable assistant should retrieve the sanitized Production thin loader itself. You should not need to copy/paste the full standalone runtime.

## What happens next
1. The user instruction authorizes retrieval of the linked Production loader.
2. The assistant verifies sanitized Production identity and confirms account state is not embedded.
3. It reads current release/module metadata, resolves compatible mandatory modules and verifies module byte identity when the host supports that primitive.
4. It capability-detects persistence and ingestion features rather than assuming them.
5. If prior LWAI state exists, it resolves the private Workspace Registry/active account, performs recovery-first and migration-first startup, and reuses current state before asking for anything again.
6. If this is genuinely new, guided phased onboarding begins. Durable storage is recommended when supported but remains optional.

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

Fallback order is short alias -> canonical loader -> last-known-good compatible engine when available -> complete GitHub fallback -> readable legacy mirror -> manual full-runtime transfer.

## Privacy
Public Production contains shared sanitized engine behavior only. Account identity, optional game UID, screenshots, balances, corrections, battles, sessions, recovery rows and provider-local references remain in the user's own environment. LWAI does not require game passwords/session tokens/authentication captures for normal operation.

## Offline / recovery install
Use `export yourself` to obtain the complete sanitized `BOOTSTRAP_FULL` runtime when a self-contained copy is required.
