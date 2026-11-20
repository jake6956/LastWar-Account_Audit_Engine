# LastWar Account Audit Engine (LWAI)

LWAI is a centrally maintained Last War: Survival account-intelligence and optimization system. It uses player-provided account evidence and current game information to give practical recommendations for combat strength, progression, research, and resource use.

## Install

Copy this into a fresh AI conversation:

> Set up Last War optimization using the instructions at https://lastwarai.com

`https://lastwarai.com` is the supported public entrypoint and resolves the current Production engine automatically.

## What LWAI does

- Builds a reusable account baseline from screenshots, stats, and other evidence the player supplies.
- Prioritizes upgrades, research, and resource use based on the player's actual account state and goals.
- Reuses verified information instead of repeatedly asking for the same data.
- Uses current evidence and clearly distinguishes verified facts from estimates or inference.
- Supports optional private persistence in a dedicated LWAI workspace in a user-selected supported cloud provider; session-only use is also supported.

## Resume in another chat

With your LWAI private storage connected, say **LWAI catch up** or **resume LWAI**. The runtime reads a compact private recovery ledger, unresolved checkpoints, and current canonical account records rather than relying on the old conversation. Ordinary recent material events expire after 72 hours; unfinished work remains pinned. This requires the LWAI runtime and access to that workspace; it does not grant automatic access to unrelated ChatGPT conversations.

## Privacy

This public repository contains only the sanitized shared engine and reusable non-user-specific knowledge. Private player/account state does not belong in this repository.

If cloud persistence is enabled, LWAI uses only its dedicated Last War/LWAI workspace in the provider the user explicitly selects. Authentication happens through the host/provider UI; users should never paste passwords, login codes, access tokens, refresh tokens, or cookies into chat.

## Public source

GitHub `main` is the authoritative public Production source.

- Live Production ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Current release metadata: `releases/LATEST.json`
- Bootstrap loader: `engine/BOOTSTRAP.txt`
- Complete standalone configuration: `engine/BOOTSTRAP_FULL.txt`
- Module manifest: `engine/MANIFEST.json`

Runtime behavior, provider adapters, release engineering, recovery details, gameplay canon, and historical release notes live in their canonical files rather than being duplicated here.
