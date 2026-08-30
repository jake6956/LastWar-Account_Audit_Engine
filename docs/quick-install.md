# LWAI Quick Install

## Copy this one line

`Set up Last War optimization. Open https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main directly, use its current commit SHA, then retrieve and follow engine/BOOTSTRAP.txt from that exact SHA. Never use search-index/cached main copies; if live SHA resolution fails, stop rather than guessing.`

Paste it into a fresh ChatGPT conversation.

**Do not use the old TinyURL installer.** It is retired because some ChatGPT clients are routed to TinyURL's deprecated preview/interstitial.

## What happens

1. ChatGPT resolves the live GitHub `main` commit SHA.
2. It loads `engine/BOOTSTRAP.txt` from that exact immutable commit.
3. The Stage-1 loader validates pinned release metadata and hands off to mandatory modules.
4. Existing LWAI state is discovered/migrated before new-user onboarding.
5. A genuinely new user chooses session-only or a supported cloud provider.
6. If cloud is chosen, LWAI explicitly explains its workspace-only security guardrail before authorization.
7. After verified storage, onboarding automatically continues through identity, baseline and first evidence capture.
8. Future runtime freshness checks use the same live-ref resolver, so users do not manually reinstall for normal Production updates.

## Cloud security boundary

LWAI is explicitly restricted to its own Last War / LWAI workspace. It will not browse, read, search, inspect, change, move, rename, delete, index or use anything else in connected storage—even if the connector technically exposes broader access. Other ChatGPT/app workspaces and personal files are off-limits.

Authentication happens in the provider/ChatGPT UI. LWAI never asks for passwords, OAuth codes, tokens, cookies or credentials in chat. For Google Drive, choose `Allow always` if ChatGPT offers it; equivalent persistent authorization is recommended for other providers only when actually shown.

## Staying current

`release.resolver` resolves live GitHub `main`; `release.updater` pins all candidate reads to that exact commit and adopts only validated Production. Existing deployments keep last-known-good ENGINE and LOCAL STATE if current Production cannot be resolved safely.

`refresh engine` remains the manual break-glass command and uses the same resolver transaction.

## Recovery

`export yourself` / `export LWAI` produces the complete sanitized `BOOTSTRAP_FULL.txt` fallback. Private account snapshots remain separate from the public engine.
