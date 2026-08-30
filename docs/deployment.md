# Turnkey Deployment Guide

## Fastest path for a player
Paste exactly this into a fresh ChatGPT conversation:

`Set up Last War optimization using the instructions at https://lastwarai.com`

That is the single preferred public install path. LastWarAI.com serves a tiny first-party Stage-0 locator. The assistant then resolves the live GitHub Production `main` ref, pins the current commit SHA, loads `engine/BOOTSTRAP.txt` from that exact commit, discovers/resumes supported private state, migrates supported older workspaces when necessary, and begins or resumes guided operation.

The player should not need to copy/paste the complete engine or manually reinstall to receive later Production updates. Durable cloud persistence is strongly recommended but optional.

## Why the installer starts at LastWarAI.com
The public URL should be short, stable and controlled by LWAI rather than a third-party shortener or a long implementation URL. LastWarAI.com can change hosting implementation without changing the installer users circulate.

It is transport/discovery only. It does not determine the current engine version.

The previously circulated `https://tinyurl.com/2yxf7f5x` is legacy compatibility only. It is not used for new sharing and is never current-version authority.

## Production authority
Current Production is resolved from:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

The assistant obtains current `commit.sha` and then reads trusted engine files only from that exact immutable commit. Search results, redirects, cached pages, mutable raw `main`, legacy aliases and model memory cannot establish current Production.

Canonical GitHub coordinates:

- Repository: `https://github.com/jake6956/LastWar-Account_Audit_Engine`
- Live ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Stage-1: `engine/BOOTSTRAP.txt` at resolved commit C
- Release metadata: `releases/LATEST.json` at C
- Module graph: `engine/MANIFEST.json` at C
- Migration graph: `releases/MIGRATIONS.json` at C
- Complete fallback: `engine/BOOTSTRAP_FULL.txt` at C

## Startup sequence
A deployment should:
1. retrieve the LastWarAI.com Stage-0 locator;
2. resolve live GitHub `main` and require a valid current commit SHA C;
3. retrieve Stage-1 plus release metadata/manifest/migrations from C only;
4. run the automatic updater before ordinary account/domain work while preserving the user's requested action;
5. verify Production/privacy identity and engine API;
6. capability-detect persistence/ingestion features;
7. inspect for current Workspace Registry plus accessible legacy LWAI state before onboarding;
8. establish account context: resolve registry `active_account_id`, or register pre-registry legacy state first;
9. inspect workspace schema before ordinary domain loading;
10. if schema is current `2.3`, load mandatory core normally;
11. if schema is supported historical `2.1`/`2.2`, load only migration-capable core/release/storage behavior, apply validated additive migration edges, re-read/verify target schema, then enable current-schema-only domain modules;
12. if no validated path exists, fail closed with existing local state untouched and do not start redundant onboarding;
13. run recovery-first handling and load only task-specific domain modules.

When integrity primitives are available, verify module byte identity; otherwise require exact-commit canonical origin plus exact identity/version without pretending a cryptographic check occurred.

## Supported historical workspace migration
Current schema is `2.3`.

- `2.1 -> 2.2`: add optional guidance metadata and account-scoped Audit Sessions when absent/supported.
- `2.2 -> 2.3`: add optional Runtime Checkpoints and append-only Runtime Journal when absent/supported.

These transitions are additive, idempotent and non-destructive. They preserve Workspace Registry, immutable `account_id`, `active_account_id`, account databases, history, Corrections, source/confidence/freshness and provider-local references. They require neither account rewrite nor user re-onboarding.

## Persistence capability profiles
Persistence is selected from verified capabilities rather than provider branding. Adapters report read/list/write/create/query/atomic-append/CAS/snapshot/restore and derive the strongest safe profile.

Recovery journals require atomic append/transaction, revision/CAS-controlled append, or immutable uniquely identified event creation. A writable spreadsheet alone does not prove transaction-safe journaling.

Without durable writable persistence, LWAI continues in conversation/cache mode and may use portable snapshots/exports. It must not claim durable recovery the host cannot provide.

## Automatic engine updates
`release.updater` is mandatory Production behavior. With web access it checks live GitHub Production automatically:

- on every new runtime/session startup;
- before `reload LWAI` / `reload yourself`;
- before schema-sensitive migration/recovery when compatibility matters;
- before consequential work after six hours since the last successful canonical check in a long-running runtime.

The first check is lightweight. If installed Production is current, normal UX remains silent. If a newer verified Production exists, LWAI validates channel/privacy/API/schema/migration/integrity metadata, fetches changed required components from one exact commit, health-checks, adopts the new ENGINE while preserving LOCAL STATE, then continues the user's original task.

Automatic updating does not imply a background daemon. A dormant ChatGPT conversation updates when the user next interacts unless the user separately opts into a genuinely available scheduling system.

`refresh engine` remains a permanent backwards-compatible manual escape hatch that bypasses freshness TTLs and forces the same live-ref/exact-commit update transaction. `check for LWAI updates` is an alias. Failed verification retains last-known-good ENGINE and leaves private/local state untouched.

## Sharing LWAI
`share LWAI`, `give me the install prompt`, and equivalents return:

`Set up Last War optimization using the instructions at https://lastwarai.com`

Do not create beta/stable/alternate public installer paths. RC branches are maintainer-only and temporary. The legacy TinyURL is compatibility-only for already-circulated instructions.

## Recovery
- `reload LWAI`: automatic update preflight, then reconstruct from canonical engine metadata + workspace/account/schema/recovery state.
- `export my account snapshot`: private current-state recovery export.
- `export yourself`: complete sanitized generic `BOOTSTRAP_FULL` runtime.
- `export full recovery package`: separate sanitized engine + private snapshot/registry/recovery artifacts + manifest.

## Maintainer path
Develop against private Prod-Dev, update relevant contracts/registries, sanitize, freeze an RC, create `rc/<version>` from current known-good `main`, run exact-head PR CI plus private gates, merge only the validated head SHA, require post-merge main CI, verify the live LastWarAI.com locator and GitHub Production, then synchronize private Production archives/release records.

Production CI validates the live first-party Stage-0 endpoint, release-tree structure and executable runtime invariants. Failed pre-merge candidates leave `main` untouched.
