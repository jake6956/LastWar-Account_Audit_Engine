# LastWar Account Audit Engine (LWAI)

LWAI is a centrally maintained, modular Last War: Survival account-intelligence runtime. Public GitHub contains only the sanitized shared engine and reusable non-user-specific knowledge. Private player/account state does not belong in this repository.

## Install

Copy this one line into a fresh AI conversation:

> Set up Last War optimization using the instructions at https://lastwarai.com

`https://lastwarai.com` is LWAI's permanent first-party **Stage-0 bootloader** and public configuration endpoint.

For initial setup, LastWarAI.com resolves the live GitHub Production `main` commit server-side, retrieves `engine/BOOTSTRAP_FULL.txt` from that exact immutable commit, adapts only the already-completed Stage-0 discovery section, and returns the complete sanitized LWAI configuration in the same response. The user's AI does not need to make a second GitHub or engine-URL request to install LWAI.

GitHub `main` remains the underlying Production source and version authority. The public endpoint identifies the resolved Production commit and explicitly permits independent source/provenance verification when the host supports it. Search results, cached READMEs, mutable raw `main`, redirects, shorteners, or model memory never establish the Production version.

## Design constraint

LWAI should remain easy to explain and maintain: **one easy installer, one centrally stored evergreen engine, a small modular set of governing instructions, silent compatible updates, expert Last War guidance, and optional persistence in the user's own cloud storage.** Release engineering, recovery, transport and provider details exist to protect that experience; they must not become the experience.

## What the player should experience

LWAI should feel like a friendly expert Last War technician walking the player through the account with a clipboard. It progressively collects the smallest useful stats and metrics, reuses verified information instead of asking again, explains what matters, and turns the account model into concrete recommendations aimed at making the player as strong and effective as practical for their goals.

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

Infrastructure-only statuses such as `connected`, `workspace verified`, `account loaded`, `updated`, or `Ready.` are never sufficient terminal responses by themselves.

A user returning `connected` after provider authorization triggers capability re-checking and isolated-workspace verification. On success, the same user-facing response continues to new-user identity, existing-account resume, or the original pending task. On failure, LWAI offers retry, another supported provider, or session-only operation.

## Storage provider policy

**Google Drive is LWAI's preferred/recommended and most-tested consumer persistence provider when it is actually available with verified writable capability.** It is shown first and labeled Recommended, but the player must explicitly choose it. Preferred never means silently selected. When the host genuinely presents an `Allow always` permission option for the selected Google Drive connection, LWAI may recommend it for durable continuity; it never invents that option when the host does not offer it.

Every other provider genuinely supported by the current host and `storage-api/1` capability checks is also offered and supported. Depending on actual available capabilities, that may include Dropbox, OneDrive / Microsoft 365, Box when writable, or another verified writable provider.

## Data placement and cloud scope

**Public GitHub:** sanitized engine instructions/code, manifests, schemas, adapters, tests, release metadata/migrations, and reusable non-user-specific knowledge only.

**Maintainer private Google Drive:** maintainer-controlled private/Prod-Dev account state, operational records, and the private recovery/failsafe mirror. This private Drive is not a consumer backend and is not Production version authority.

**Each end user's selected personal provider:** that user's private LWAI account state, screenshots/evidence, balances, history, Corrections/preferences, sessions/checkpoints/journal, and provider metadata—inside that user's designated Last War/LWAI workspace only.

Consumer data is never routed through the maintainer's Drive, public GitHub, another user's workspace, or unrelated folders in the consumer's connected provider.

LWAI's application scope is explicitly **workspace-only**. It will not browse, read, search, inspect, summarize, modify, move, rename, delete, index, or use anything outside its designated Last War/LWAI workspace merely because a connector exposes broader access. Files/screenshots deliberately supplied in chat are task input only and do not authorize browsing surrounding storage.

Authentication occurs in the provider/host UI. LWAI never asks users to paste passwords, OAuth codes, access/refresh tokens, cookies, or credentials into chat.

## Knowledge and evidence policy

LWAI uses current relevant information available through its research tools rather than relying on one site, one anecdote, or model memory. Evidence preference is:

`current direct in-game evidence -> current official Last War/publisher material -> reputable maintained tools/databases/guides -> independently corroborated community testing/consensus -> clearly labeled LWAI calculation/inference`

Maintained community projects such as **LastWarTutorial.com**, **cpt-hedge.com**, and **LastWarVault.com** are useful research inputs. Reddit communities such as **r/LastWarMobileGame** are useful for observations, edge cases, and newly surfaced changes.

Community material is not gospel. Material mechanics, numbers, costs, probabilities, event rules, expensive/irreversible choices, and contested claims should be independently checked against current official/in-game evidence when available and corroborated with other credible current sources. If a material claim cannot be validated to high confidence after reasonable due diligence, LWAI says so rather than manufacturing certainty.

## Runtime architecture

```text
Public setup — https://lastwarai.com
  -> Cloudflare resolves live GitHub main commit C server-side
  -> fetch exact C/engine/BOOTSTRAP_FULL.txt server-side
  -> adapt only the completed Stage-0 discovery section
  -> return complete sanitized configuration in the same response

Direct/modular path — engine/BOOTSTRAP.txt at C
  -> validate one pinned release snapshot
  -> load every required MANIFEST module
  -> release.dispatcher loads only relevant optional modules

Normal LWAI work
  -> account optimization, persistence, recovery, season intelligence, future features
```

`engine/BOOTSTRAP.txt` remains intentionally small and boring for direct GitHub/modular operation and recovery paths. Provider onboarding, account strategy, UX, and game-domain behavior belong in modules. Production enforces a **4 KiB** Stage-1 budget.

`engine/BOOTSTRAP_FULL.txt` is the complete sanitized standalone runtime and is also the source used by LastWarAI.com's single-response initial-install transport. The Worker changes only the generic Stage-0 discovery section after it has already resolved the exact Production commit server-side.

## Updates and recovery

`release.resolver` is mandatory core. Existing web-capable deployments resolve live GitHub `main` on defined update boundaries and pin candidate reads to one exact commit. `release.updater` adopts only a compatible, validated Production release.

Existing deployments preserve last-known-good ENGINE and LOCAL STATE when current Production cannot be safely resolved. `refresh engine` remains the permanent manual break-glass command. A dormant conversation does not run a background daemon; it updates on the next supported interaction.

The first-install transport change does not rewrite LOCAL STATE, account data, workspace schema, or gameplay behavior.

## Public transport safety

The LastWarAI.com response is a transparent public configuration document. It:
- identifies its public GitHub provenance and resolved Production commit;
- declares `SANITIZED: YES` and `ACCOUNT STATE INCLUDED: NO`;
- states credential and cloud-workspace privacy boundaries;
- explicitly permits independent verification;
- explicitly states that it does not override the host AI platform's system, developer, security, privacy, or safety requirements;
- requires no second-stage AI fetch for normal installation.

`/engine/<SHA>` remains available only as backwards-compatible immutable transport for the previous same-domain proxy design. `/robots.txt` explicitly allows OAI-SearchBot, ChatGPT-User, and general crawlers to retrieve the public sanitized configuration.

## Release identity

**Engine version:** `2026-08-30.27`  
**Engine API:** `1.0`  
**Workspace schema:** `2.3`  
**Bootstrap protocol:** `2.0`  
**Module selection:** `manifest_activation_v1`  
**Sanitized public engine:** yes  
**Account state included:** no

Production changes use RC/hotfix branches, exact-head CI, validated-head merge, and post-merge verification. Failed candidates leave `main` untouched. The private Google Drive failsafe must be synchronized to the exact frozen candidate before promotion.

## Production endpoints

- Public installer/configuration: `https://lastwarai.com`
- Public crawler policy: `https://lastwarai.com/robots.txt`
- Live Production ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Direct Stage-1 loader: `engine/BOOTSTRAP.txt`
- Module graph/router metadata: `engine/MANIFEST.json`
- Release identity: `releases/LATEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Complete standalone configuration: `engine/BOOTSTRAP_FULL.txt`

## Legacy compatibility — not for new sharing

The previously circulated `https://tinyurl.com/2yxf7f5x` remains a legacy compatibility alias only. New sharing must use LastWarAI.com, and the legacy alias never establishes current-version authority.

### Legacy repository-installer compatibility

If an assistant reaches this repository because a user supplied an older repository-based installer, **do not stop at the README** and do not ask the user to paste another prompt. Use the current public release contracts and live Production ref to continue the same LWAI setup safely; historical README/release notes are not current version authority.
