# Turnkey Deployment Guide

## Fastest path for a player
Paste exactly this into a fresh ChatGPT conversation:

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

That remains the single preferred install path. A web-capable assistant retrieves the sanitized Production loader, canonicalizes its identity against GitHub, automatically checks for newer verified Production, discovers/resumes supported private state, migrates supported older workspaces when necessary, then begins or resumes operation. The player should not need to copy/paste the complete engine or manually reinstall to receive later Production updates.

For best results, use a higher reasoning/thinking setting when exposed. Durable cloud persistence is strongly recommended but optional.

## What the short link does
TinyURL is convenience only; it is not a trust root or alternate release channel. Canonical Production lives on GitHub `main`.

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

If the alias body is stale/cached or disagrees with canonical GitHub, discard the alias body and continue from verified canonical Production. If modular retrieval fails, use last-known-good compatible engine state or the complete fallback. A readable legacy Google mirror may follow canonical GitHub options; manual full-bootstrap transfer is last resort.

## Startup sequence
A deployment should:
1. retrieve the linked loader, then fetch canonical `LATEST.json`, `BOOTSTRAP.txt`, `MANIFEST.json` and `MIGRATIONS.json` when web exists;
2. run the automatic updater before ordinary account/domain work: if Production is current, continue silently; if a newer verified Production exists, validate/adopt it while preserving LOCAL STATE and preserve the user's original requested action across the update;
3. verify Production/privacy identity and engine API;
4. capability-detect persistence/ingestion features;
5. inspect for current Workspace Registry plus accessible legacy LWAI state before onboarding;
6. establish account context: resolve registry `active_account_id`, or register pre-registry legacy state first;
7. inspect the workspace schema before ordinary domain loading;
8. if schema is current `2.3`, load mandatory core normally;
9. if schema is supported historical `2.1`/`2.2`, load only migration-capable core/release/storage behavior, apply validated additive migration edges, re-read/verify target schema, then enable current-schema-only domain modules;
10. if no validated path exists, fail closed with existing local state untouched and do not start redundant onboarding;
11. run recovery-first handling, then migration-first reconciliation and load only task-specific domain modules.

When integrity primitives are available, verify module byte identity; otherwise require canonical origin plus exact identity/version without pretending a cryptographic check occurred.

## Supported historical workspace migration
Current schema is `2.3`.

- `2.1 -> 2.2`: add optional guidance metadata and account-scoped Audit Sessions when absent/supported.
- `2.2 -> 2.3`: add optional Runtime Checkpoints and append-only Runtime Journal when absent/supported.

These transitions are additive, idempotent and non-destructive. They preserve Workspace Registry, immutable `account_id`, `active_account_id`, account databases, history, Corrections, source/confidence/freshness and provider-local references. They require neither account rewrite nor user re-onboarding.

Migration-capable core/release/storage modules explicitly span validated schemas `2.1`–`2.3`; domain modules may remain `2.3`-only and must not run early.

## Persistence capability profiles
Persistence is selected from verified capabilities rather than provider branding. Adapters report read/list/write/create/query/atomic-append/CAS/snapshot/restore and derive the strongest safe profile.

Recovery journals require atomic append/transaction, revision/CAS-controlled append, or immutable uniquely identified event creation. A writable spreadsheet alone does not prove transaction-safe journaling.

Without durable writable persistence, LWAI continues in conversation/cache mode and may use portable snapshots/exports. It must not claim durable recovery the host cannot provide.

## Automatic engine updates
`release.updater` is mandatory Production behavior. With web access it checks canonical GitHub automatically:

- on every new runtime/session startup;
- before `reload LWAI` / `reload yourself`;
- before schema-sensitive migration/recovery when compatibility matters;
- before consequential work after six hours since the last successful canonical check in a long-running runtime.

The first check is lightweight: `releases/LATEST.json`. If installed Production is current, no modules are re-downloaded and normal UX remains silent. If a newer verified Production exists, LWAI validates channel/privacy/API/schema/migration/integrity metadata, fetches only changed required engine components plus task-relevant modules, health-checks, adopts the new ENGINE while preserving LOCAL STATE, then continues the user's original requested task.

Durable workspaces may store compact private workspace-level engine metadata such as installed version, last successful check/update, last-known-good version, update policy and health. These values are not account evidence or routing data. Session-only deployments keep equivalent metadata ephemerally when possible.

Automatic updating does not imply a background daemon. A dormant ChatGPT conversation updates when the user next interacts unless the user separately opted into a genuinely available scheduling system.

`refresh engine` remains a permanent backwards-compatible manual escape hatch that bypasses freshness TTLs and forces the same canonical update transaction. `check for LWAI updates` is an alias. Failed verification retains last-known-good ENGINE and leaves private/local state untouched.

## Sharing LWAI
`share LWAI`, `give me the install prompt`, and equivalents return the same one-line TinyURL instruction. Do not create beta/stable/alternate installer paths; RC branches are maintainer-only and temporary.

## Recovery
- `reload LWAI`: automatic update preflight, then reconstruct from canonical engine metadata + workspace/account/schema/recovery state.
- `export my account snapshot`: private current-state recovery export.
- `export yourself`: complete sanitized generic `BOOTSTRAP_FULL` runtime.
- `export full recovery package`: separate sanitized engine + private snapshot/registry/recovery artifacts + manifest.

## Maintainer path
Develop against private Prod-Dev, update relevant contracts/registries, sanitize, freeze an RC, create `rc/<version>` from current known-good `main`, run exact-head PR CI plus private gates, merge only the validated head SHA, require post-merge main CI, verify public Production/installer, then synchronize private Production archives/release records.

Production CI validates release-tree structure plus executable runtime invariants, including historical workspace-schema migration, stale-alias canonicalization, permanent `refresh engine` compatibility and automatic consumer update behavior. Failed pre-merge candidates leave `main` untouched.
