# LWAI Quick Install

## Copy this one line

`Set up Last War optimization. Read the live GitHub main ref at https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main, use its current commit.sha, then load and follow engine/BOOTSTRAP.txt from that exact commit.`

Paste it into a fresh ChatGPT conversation.

**Do not use the old TinyURL installer.** It is retired and is not a Production dependency.

## What happens

1. ChatGPT reads the live GitHub `main` branch ref and obtains its current `commit.sha`.
2. It loads `engine/BOOTSTRAP.txt` from that exact immutable commit.
3. Stage-1 validates the pinned release/manifest/migration identity.
4. Stage-1 loads every MANIFEST module with `required:true` in dependency order and hands off to the manifest entrypoint.
5. `release.dispatcher` selects optional modules from MANIFEST activation metadata and recursively includes their dependencies.
6. Existing LWAI state is discovered/migrated before genuine new-user onboarding.
7. A new user chooses session-only or an actually supported cloud provider; storage/provider behavior is module-owned.
8. After verified storage, onboarding continues automatically through identity, baseline and first evidence.
9. Future Production capabilities become available through MANIFEST registration; the installer and Stage-1 feature list do not need to change.

## Staying current

`release.resolver` resolves live GitHub `main`; `release.updater` pins each candidate transaction to one exact commit and adopts only validated Production. Existing deployments keep last-known-good ENGINE and LOCAL STATE if current Production cannot be resolved safely.

`refresh engine` remains the permanent manual break-glass command and uses the same resolver transaction.

## Cloud security boundary

LWAI is explicitly restricted to its own Last War / LWAI workspace. It will not browse, read, search, inspect, change, move, rename, delete, index or use unrelated connected-storage content—even if the connector technically exposes broader access. Other ChatGPT/app workspaces and personal files are off-limits.

Authentication happens in the provider/ChatGPT UI. LWAI never asks for passwords, OAuth codes, tokens, cookies or credentials in chat. For Google Drive, choose `Allow always` only when ChatGPT offers it; equivalent persistent authorization is recommended for other providers only when actually shown.

## Recovery

`engine/BOOTSTRAP_FULL.txt` remains the complete sanitized standalone fallback. Private account snapshots remain separate from the public engine.
