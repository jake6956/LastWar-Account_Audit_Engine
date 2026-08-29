# Turnkey Deployment Guide

## Fastest path for a player
Paste exactly this into a fresh ChatGPT conversation:

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

That is the preferred install path. The assistant should retrieve the full Production bootstrap itself, validate it, then begin phased onboarding. The player should not need to copy/paste the multi-page engine from a phone.

For best results, switch reasoning/thinking to **HIGH** if the product exposes that control. Cloud persistence is strongly recommended but optional.

## What the short link does
The neutral TinyURL currently resolves to the canonical raw GitHub Production bootstrap. It is used for convenience and reduced casual maintainer exposure in the visible install line. It is not a security authority or true anonymity layer.

Canonical direct bootstrap:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt

If the alias cannot be reached but direct GitHub can, use the direct source. If GitHub cannot be reached, try the stable Google distribution mirror when readable. Only require a manual full-bootstrap paste when the deployment has no usable remote retrieval path.

## Remote bootstrap acceptance behavior
A fresh assistant receiving the one-line instruction should treat the user's request as explicit authorization to retrieve and use the linked bootstrap. It should not ask the user to manually paste the linked content if web access can read it. If retrieval is truncated, fetch the remaining content until required runtime sections are available, then execute `STARTUP BEHAVIOR`.

## If cloud persistence is accepted
The deployment capability-detects the provider, creates an isolated LWAI workspace, maps the provider-neutral schema onto the strongest supported structured storage and never touches unrelated files.

## Engine updates
A player may say `refresh engine` / `check for LWAI updates`. The deployment preserves all local account state, checks direct GitHub Production (`releases/LATEST.json` + `engine/BOOTSTRAP.txt`), applies only generic Production engine changes, follows migrations if required and runs health checks afterward. Routine updates should not depend on the URL shortener.

## Sharing LWAI
If a deployed instance is asked `share LWAI`, `give me the install prompt`, or equivalent, return the one-line TinyURL instruction by default. Do not dump the full engine unless the user asks for the standalone/offline export.

## Recovery
- `reload LWAI`: reconstruct working context from durable local state.
- `export my account snapshot`: private current-state recovery export.
- `export yourself`: complete sanitized generic engine for offline/manual recovery.
- `export full recovery package`: separate engine + private snapshot + manifest.

## Operator / maintainer path
Develop against a private Prod-Dev deployment, update all relevant canonical documentation, sanitize, freeze a Release Candidate, run private gates, commit the candidate to an RC branch, open a PR, require CI + remote-install integrity, merge only the validated head into GitHub Production, then synchronize secondary mirrors/archives.
