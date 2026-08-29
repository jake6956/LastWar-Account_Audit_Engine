# Turnkey Deployment Guide

## Fastest path for a player
Paste exactly this into a fresh ChatGPT conversation:

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

That is the preferred install path. A web-capable assistant should retrieve the sanitized Production thin loader, validate Production identity, resolve required modules, then begin or resume operation. The player should not need to copy/paste the complete engine from a phone.

For best results, use a higher reasoning/thinking setting when the product exposes that control. Cloud persistence is strongly recommended but optional.

## What the short link does
The TinyURL is convenience only; it is not a trust root or anonymity boundary. Canonical Production lives on GitHub `main`.

Canonical loader:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt

Current release metadata:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json

Module graph:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json

Migration graph:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/MIGRATIONS.json

Complete fallback:
https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt

If the alias cannot be reached but direct GitHub can, use the canonical loader. If modular retrieval fails, use last-known-good compatible engine state or the complete fallback. A readable legacy Google mirror may be used after canonical GitHub options. Manual full-bootstrap transfer is the last fallback.

## Startup sequence
A fresh deployment should:
1. verify the loader is sanitized and contains no account state;
2. retrieve `LATEST.json` and `MANIFEST.json` when web access exists;
3. confirm engine/API/schema compatibility;
4. resolve mandatory module dependencies;
5. verify module byte identity when the host supports the Git blob verification primitive, otherwise verify canonical origin + exact module identity/version without pretending a hash check occurred;
6. capability-detect persistence and ingestion features;
7. resolve Workspace Registry and `active_account_id` when durable LWAI state exists;
8. run recovery-first and migration-first startup before redundant onboarding;
9. load task-specific domain modules only when needed.

## Persistence capability profiles
Persistence is selected from verified capabilities rather than provider branding. Adapters report read/list/write/create/query/atomic-append/CAS/snapshot/restore capabilities and derive the strongest safe persistence profile.

Recovery journals require atomic append/transaction, revision/CAS-controlled append, or immutable uniquely identified event creation. A writable spreadsheet alone does not prove transaction-safe journaling.

Without durable writable persistence, LWAI continues in conversation/cache mode and may use portable snapshots/exports. It must not claim durable recovery that the host cannot provide.

## Engine updates
A player may say `refresh engine` / `check for LWAI updates`. The deployment preserves LOCAL STATE first, checks `LATEST.json`, `MANIFEST.json` and `MIGRATIONS.json`, validates compatibility/integrity where supported, applies only required promoted migration edges and refreshes ENGINE only. Engine-only migrations never force re-onboarding or rewrite account state.

## Sharing LWAI
If a deployed instance is asked `share LWAI`, `give me the install prompt`, or equivalent, return the one-line TinyURL instruction by default. Do not dump the complete engine unless the user asks for the standalone/offline export.

## Recovery
- `reload LWAI`: reconstruct working context from durable local state and unresolved recovery metadata.
- `export my account snapshot`: private current-state recovery export.
- `export yourself`: complete sanitized generic `BOOTSTRAP_FULL` runtime.
- `export full recovery package`: separate sanitized engine + private snapshot/registry/recovery artifacts + manifest.

## Maintainer path
Develop against private Prod-Dev, update relevant contracts/registries, sanitize, freeze an RC, create `rc/<version>` from current known-good `main`, run exact-head PR CI plus private gates, merge only the validated head SHA, require post-merge main CI, verify public Production/installer, then synchronize private Production archives and release records.

Production CI validates both release-tree structure and executable runtime invariants. Failed pre-merge candidates leave `main` untouched.
