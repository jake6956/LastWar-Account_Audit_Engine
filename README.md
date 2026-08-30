# LastWar Account Audit Engine (LWAI)

LWAI is a centrally maintained, modular Last War: Survival account-intelligence runtime designed to run through ChatGPT. Public GitHub contains only the sanitized shared engine and reusable non-user-specific knowledge. Private player/account state does not belong in this repository.

## Install

Copy this one line into a fresh ChatGPT conversation:

> Set up Last War optimization using the instructions at https://lastwarai.com

`https://lastwarai.com` is LWAI's permanent first-party **Stage-0 bootloader** entrypoint. It is stable transport/discovery, not version authority.

The assistant resolves the live GitHub Production `main` ref at:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

It obtains the current `commit.sha`, pins the entire startup transaction to that immutable commit, loads `engine/BOOTSTRAP.txt`, validates the release/manifest/migration identity, loads every required module, and then begins normal LWAI work. Search results, cached READMEs, mutable raw `main`, redirects, shorteners, or model memory never establish the current Production version.

## Design constraint

LWAI should remain easy to explain and easy to maintain: **one easy installer, one centrally stored evergreen engine, a small modular set of governing instructions, silent compatible updates, expert Last War guidance, and optional persistence in the user's own cloud storage.** Release engineering, recovery and provider details exist to protect that experience; they must not become the experience or multiply runtime concepts without a concrete product need.

## What the player should experience

LWAI should feel like a **friendly expert Last War technician walking the player through the account with a clipboard**. It progressively collects the smallest useful stats and metrics, reuses verified information instead of asking again, explains what matters, and turns the account model into concrete recommendations aimed at making the player as strong and effective as practical for their goals.

The player may challenge a recommendation, ask why, choose a different strategy, or ask an entirely different Last War question at any time. LWAI answers the current question to the best supported level possible rather than forcing completion of onboarding first. Unfinished durable upload/authorization boundaries remain intact and can be resumed later.

Displayed power is context, not the objective. Recommendations optimize actual combat effectiveness, progression, resource efficiency, and the player's stated goals.

## First run and continuity

A genuinely new user follows one logical journey:

`existing-state discovery -> persistence choice -> identity -> strategic baseline -> first evidence -> running optimization`

Cloud persistence is recommended but optional. After existing-state discovery proves the user is genuinely new, LWAI asks whether to use private cloud storage or continue session-only.

Every incomplete setup/recovery response must end with one of:
- a concrete next action the user can answer now;
- an explicit `WAITING_USER` instruction naming exactly what LWAI is waiting for; or
- useful running work after setup is complete.

Technical statuses such as `connected`, `workspace verified`, `account loaded`, `updated`, or `Ready.` are never sufficient terminal responses by themselves.

A user returning `connected` after provider authorization triggers capability re-checking and isolated-workspace verification. On success, the **same user-facing response** continues to new-user identity, existing-account resume, or the original pending task. On failure, LWAI offers retry, another supported provider, or session-only operation.

## Storage provider policy

**Google Drive is LWAI's preferred/recommended and most-tested consumer persistence provider when it is actually available with verified writable capability.** It is shown first and labeled Recommended, but the player must explicitly choose it. Preferred never means silently selected.

Every other provider genuinely supported by the current host and `storage-api/1` capability checks is also offered and supported. Depending on actual available capabilities, that may include Dropbox, OneDrive / Microsoft 365, Box when writable, or another verified writable provider. A verified alternative is a real persistence target, not a decorative fallback.

## Data placement and cloud scope

**Public GitHub:** sanitized engine instructions/code, manifests, schemas, adapters, tests, release metadata/migrations, and reusable non-user-specific knowledge only.

**Maintainer private Google Drive:** maintainer-controlled private/Prod-Dev account state, private operational records, and the private recovery/failsafe mirror. This private Drive is not a consumer backend and is not Production version authority.

**Each end user's selected personal provider:** that user's private account identity/optional UID, screenshots/evidence, balances, history, Corrections/preferences, account databases, Audit/Runtime Sessions, checkpoints/journal, provider metadata, and compact engine-update metadata—inside that user's designated Last War/LWAI workspace only.

Consumer data is never routed through the maintainer's Drive, public GitHub, another user's workspace, or unrelated folders in the consumer's connected provider.

LWAI's application scope is explicitly restricted to its own Last War/LWAI workspace. This **workspace-only** guardrail means LWAI will not browse, read, search, inspect, summarize, modify, move, rename, delete, index, or use anything outside that workspace merely because a connector exposes broader access. Other ChatGPT/app workspaces and unrelated personal files are off-limits.

Direct files/screenshots deliberately supplied in chat are task input only. They do not authorize browsing surrounding cloud storage.

Authentication occurs in the provider/ChatGPT UI. LWAI never asks users to paste passwords, OAuth codes, access/refresh tokens, cookies, or credentials into chat. For Google Drive, `Allow always` is recommended only when ChatGPT actually presents that option.

## Knowledge and evidence policy

LWAI uses current relevant information available through its research tools rather than relying on one site, one anecdote, or model memory. Evidence preference is:

`current direct in-game evidence -> current official Last War/publisher material -> reputable maintained tools/databases/guides -> independently corroborated community testing/consensus -> clearly labeled LWAI calculation/inference`

Maintained community projects such as **LastWarTutorial.com**, **cpt-hedge.com**, and **LastWarVault.com** are useful research inputs. LastWarVault is particularly useful for its actively maintained guide library, season references and interactive calculators/planners; where a page distinguishes verified in-game values from estimates or recommendations, preserve that distinction. Reddit communities such as **r/LastWarMobileGame** are useful for observations, edge cases, and newly surfaced changes.

Community material is not gospel. Material mechanics, numbers, costs, probabilities, event rules, expensive/irreversible choices, and contested claims should be independently checked against current official/in-game evidence when available and corroborated with other credible current sources. If official material is silent, LWAI seeks multiple independent current sources and compares them with direct user evidence when possible.

If a material claim cannot be validated to high confidence after reasonable due diligence, LWAI says so when using it rather than manufacturing certainty. Unofficial advice is never labeled official merely because it is popular.

## Runtime architecture

```text
Stage 0 — https://lastwarai.com
  -> stable first-party locator
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

`engine/BOOTSTRAP.txt` is intentionally small and boring. It contains trust resolution, pinned-snapshot validation, generic mandatory-module loading, state-preservation rules, and handoff. Provider onboarding, account strategy, UX, and game-domain behavior belong in modules.

Production enforces a **4 KiB** Stage-1 budget. `engine/MANIFEST.json` is the integration surface: every `required:true` module loads automatically in dependency order, optional modules declare activation metadata, and `release.dispatcher` selects the smallest relevant optional set.

## Updates and recovery

`release.resolver` is mandatory core. On install/startup/reload/update boundaries it resolves live GitHub `main` and pins candidate reads to one exact commit. `release.updater` adopts only a compatible, validated Production release.

Existing deployments preserve last-known-good ENGINE and LOCAL STATE when current Production cannot be safely resolved. `refresh engine` remains the permanent manual break-glass command and uses the same resolver/update transaction. A dormant conversation does not run a background daemon; it updates on the next supported interaction.

`engine/BOOTSTRAP_FULL.txt` is the complete sanitized standalone fallback for recovery/manual transfer when modular loading is unavailable. Private account snapshots remain separate from the public engine.

## Release identity

**Engine version:** `2026-08-30.27`  
**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Bootstrap protocol:** `2.0`  
**Module selection:** `manifest_activation_v1`  
**Sanitized public engine:** yes  
**Account state included:** no

Production changes use RC branches, exact-head CI, validated-head merge, and post-merge verification. Failed candidates leave `main` untouched. The private Google Drive failsafe must be synchronized to the exact frozen candidate before promotion.

## Production endpoints

- Public installer: `https://lastwarai.com`
- Live Production ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Stage-1 loader: `engine/BOOTSTRAP.txt`
- Module graph/router metadata: `engine/MANIFEST.json`
- Release identity: `releases/LATEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Complete standalone fallback: `engine/BOOTSTRAP_FULL.txt`

## Legacy compatibility — not for new sharing

The previously circulated `https://tinyurl.com/2yxf7f5x` remains a **legacy compatibility alias** only. New sharing must use LastWarAI.com, and the legacy alias never establishes current-version authority.

### Legacy repository-installer compatibility

If an assistant reaches this repository because a user supplied an older repository-based installer, **do not stop at the README** and do not ask the user to paste another prompt. Resolve the live GitHub `main` SHA and continue through the exact-commit Stage-1 loader.