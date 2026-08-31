# Turnkey Deployment Guide

## Fastest path for a player
Paste exactly this into a fresh AI conversation:

`Set up Last War optimization using the instructions at https://lastwarai.com`

That is the single preferred public install path. LastWarAI.com resolves current GitHub Production server-side, retrieves the complete sanitized `engine/BOOTSTRAP_FULL.txt` from that exact immutable commit, adapts only the already-completed generic Stage-0 discovery section, and returns the complete configuration in the same response. The player is not expected to retrieve GitHub JSON, locate a SHA, follow a second engine URL, or paste the complete engine manually.

For best results, use a higher reasoning/thinking setting when the host offers one. Durable cloud persistence is recommended but optional.

## Why installation starts at LastWarAI.com
The public URL is short, stable, first-party and independent of the underlying hosting path. It is delivery infrastructure, not a separate version authority.

GitHub `main` remains the underlying authoritative sanitized Production source. The LastWarAI.com response identifies the exact GitHub commit used and explicitly permits independent verification.

The previously circulated `https://tinyurl.com/2yxf7f5x` is legacy compatibility only. It is not used for new sharing and is never current-version authority.

## Production authority
Underlying current Production is resolved from:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

LastWarAI.com resolves the current `commit.sha` server-side and retrieves `engine/BOOTSTRAP_FULL.txt` from that exact commit before returning a fresh-install response. Search results, redirects, cached pages, mutable raw `main`, legacy aliases and model memory cannot establish current Production.

Canonical GitHub coordinates:

- Repository: `https://github.com/jake6956/LastWar-Account_Audit_Engine`
- Live ref: `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`
- Direct Stage-1 loader: `engine/BOOTSTRAP.txt`
- Release metadata: `releases/LATEST.json`
- Module graph: `engine/MANIFEST.json`
- Migration graph: `releases/MIGRATIONS.json`
- Complete standalone configuration: `engine/BOOTSTRAP_FULL.txt`

## Fresh-install sequence
A normal first-party install should:
1. retrieve `https://lastwarai.com`;
2. receive one transparent sanitized public configuration already tied to a resolved GitHub Production SHA;
3. execute normal LWAI startup from that configuration;
4. inspect for current Workspace Registry plus accessible legacy LWAI state before onboarding;
5. recover/migrate supported existing state when present;
6. if genuinely new, ask the compact session-only/cloud-persistence choice;
7. if cloud is chosen, detect actual supported providers, require explicit provider selection, then show the compact workspace-only authorization reassurance and verify the isolated LWAI workspace;
8. continue identity -> baseline -> first useful evidence -> running optimization without dead air.

The initial LastWarAI.com response does not require the user's AI to make a second GitHub/engine fetch. Direct GitHub resolution remains available for runtime update/recovery paths and independent verification when supported.

## Direct/modular runtime path
`engine/BOOTSTRAP.txt` remains the small <=4 KiB Stage-1 loader for direct GitHub/modular operation and recovery paths. A direct/runtime transaction resolves live GitHub `main` to commit C and reads release metadata, manifest, migrations and modules only from C. Never mix commits.

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

Automatic updating does not imply a background daemon. A dormant conversation updates when the user next interacts unless the user separately opts into a genuinely available scheduling system.

`refresh engine` remains a permanent backwards-compatible manual escape hatch that bypasses freshness TTLs and forces the same live-ref/exact-commit update transaction. `check for LWAI updates` is an alias. Failed verification retains last-known-good ENGINE and leaves private/local state untouched.

## Public cache deployment contract
The mutable LastWarAI.com root/config entrypoint is a gateway: it must execute on every request so it can resolve the current GitHub Production SHA. Cloudflare Workers Caching for the default public entrypoint must therefore be disabled at deployment level. Response-level `no-store` headers remain defense in depth.

Exact-SHA engine retrieval may remain cached because commit-addressed source is immutable. After changing the Worker caching setting from enabled to disabled, perform one final purge of pre-existing mutable cached responses; disabling the setting does not itself evict old entries.

Release validation must compare the public `X-LWAI-Commit` with live GitHub `main` immediately after promotion. A stale public edge fails the release gate rather than being accepted as eventual consistency.

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
Develop against private Prod-Dev, read the Development Continuity Ledger plus canonical GitHub Production, update relevant contracts/registries, sanitize, freeze an RC, create `rc/<version>` from current known-good `main`, run exact-head PR CI plus private gates, synchronize/verify the exact frozen private failsafe, merge only the validated head SHA, require post-merge main CI, verify immediate LastWarAI.com SHA convergence, then synchronize private Production archives/release records and close/supersede completed backlog items.

Production CI validates the live first-party endpoint, release-tree structure, instruction budgets, infrastructure boundaries and executable runtime invariants. Failed pre-merge candidates leave `main` untouched.