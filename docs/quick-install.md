# LWAI Quick Install

## Copy this one line

`Set up Last War optimization using the instructions at https://lastwarai.com`

Paste it into a fresh ChatGPT conversation.

`https://lastwarai.com` is the permanent first-party public installer. It serves only the tiny Stage-0 locator; it does not establish the current engine version.

The previously circulated `https://tinyurl.com/2yxf7f5x` is legacy compatibility only. Do not use it for new sharing and never treat a shortener response as Production authority.

## What happens

1. ChatGPT retrieves the public locator from LastWarAI.com.
2. The locator tells it to read the live GitHub `main` branch ref at `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main` and obtain its current `commit.sha`.
3. It loads `engine/BOOTSTRAP.txt` from that exact immutable commit.
4. Stage-1 validates the pinned release/manifest/migration identity.
5. Stage-1 loads every MANIFEST module with `required:true` in dependency order and hands off to the manifest entrypoint.
6. `release.dispatcher` selects optional modules from MANIFEST activation metadata and recursively includes their dependencies.
7. Existing LWAI state is discovered/migrated before genuine new-user onboarding.
8. A new user chooses session-only or an actually supported cloud provider; storage/provider behavior is module-owned.
9. Future Production capabilities become available through MANIFEST registration; the public installer does not need to change.

## Trust model

The public domain is human-facing discovery/transport. Current Production is established only by the live GitHub `main` ref and its exact `commit.sha`. Search results, redirects, cached READMEs, mutable raw `main`, shorteners and model memory cannot determine the current version.

All trusted engine files for one startup/update transaction come from the same exact commit.

## Staying current

`release.resolver` resolves live GitHub `main`; `release.updater` pins each candidate transaction to one exact commit and adopts only validated Production. Existing deployments keep last-known-good ENGINE and LOCAL STATE if current Production cannot be resolved safely.

`refresh engine` remains the permanent manual break-glass command and uses the same resolver transaction.

## Cloud security boundary

LWAI is explicitly restricted to its own Last War / LWAI workspace. It will not browse, read, search, inspect, change, move, rename, delete, index or use unrelated connected-storage content—even if the connector technically exposes broader access. Other ChatGPT/app workspaces and personal files are off-limits.

Authentication happens in the provider/ChatGPT UI. LWAI never asks for passwords, OAuth codes, tokens, cookies or credentials in chat. For Google Drive, choose `Allow always` only when ChatGPT offers it.

## Recovery

`engine/BOOTSTRAP_FULL.txt` remains the complete sanitized standalone fallback. Private account snapshots remain separate from the public engine.
