# Opt-In Modular Public Transport Contract

Version: 2026-09-28.47

## Purpose
Define the non-default Phase-2 transport experiment for LastWarAI.com without changing the supported root/install/config installer.

Production .46 is a compatibility-evidence release candidate, not authorization for default cutover.

## Default installer remains unchanged
The following mutable public endpoints remain the supported default and continue returning the complete exact-commit BOOTSTRAP_FULL configuration in one response:
- `/`
- `/install`
- `/config.txt`

The opt-in modular path remains absent from About, sitemap and normal install instructions. The already-retrievable root response may expose one explicit `MODULAR_COMPATIBILITY_ENTRY: https://lastwarai.com/modular`, but only as an opt-in handoff when the user's current instruction explicitly requests modular transport/testing. Normal root execution remains BOOTSTRAP_FULL.

## Opt-in modular bootstrap
`GET /modular`:
1. resolve canonical GitHub Production `main` server-side to exact 40-hex commit C;
2. retrieve exact-C `engine/BOOTSTRAP.txt`, `releases/LATEST.json`, and `engine/MANIFEST.json`;
3. validate matching Production/API/schema/sanitization identity;
4. return a small HTML bootstrap page containing Stage-1 plus a navigable exact-C resource index;
5. expose clickable links for Stage-1, LATEST, MANIFEST, MIGRATIONS, manifest schema, current versioned release, fallback and every manifest module (required and optional);
6. declare `RESOLVED_PRODUCTION_COMMIT`, `FIRST_PARTY_SNAPSHOT_BASE`, and `FIRST_PARTY_RESOURCE_INDEX`;
7. return `X-LWAI-Commit`, snapshot/index headers and transport version `3.3-chatgpt-linked-optin`;
8. use mutable no-store headers and `X-Robots-Tag: noindex, follow` so the user-supplied page is not searchable but ChatGPT may follow the exact links it exposes.

`GET /modular/config.txt` remains a plain-text compatibility alias exposing the same exact-C resource links.

Failure to resolve C or validate Stage-1 returns 503 and never falls back to guessed/cached mutable source.

## ChatGPT navigation rule
A fresh ChatGPT session may reliably retrieve the LastWarAI.com root while rejecting `/modular` when that deep path is supplied directly. Therefore the root response is the stable bootstrap entry and may hand off to `/modular` through one explicit page-provided compatibility link. `/modular` then becomes the authoritative exact-C navigation surface for the opt-in transaction.

ChatGPT MUST:
- start from the retrievable root when the modular path cannot be opened directly;
- when the user explicitly asked for modular transport/testing, follow the exact root-provided `MODULAR_COMPATIBILITY_ENTRY` before executing the fallback;
- follow exact-C resource hyperlinks exposed by `/modular`;
- prefer those page-provided links over constructing equivalent snapshot URLs;
- keep all candidate reads on the one C declared by the page;
- never substitute search/index results or a GitHub connector merely because an unlinked deep URL is unavailable.

`/modular` remains absent from sitemap/About/default install instructions. `noindex, follow` means link-following is allowed after explicit user intent. The root handoff is visible only as a compatibility instruction inside the default configuration and must not activate modular transport unless the user's current request explicitly asks for it.
## Exact-SHA same-origin snapshot
`GET /snapshot/C/<runtime-path>` is immutable transport for one validated 40-hex C.

Allowed runtime paths only:
- `engine/BOOTSTRAP.txt`
- `engine/BOOTSTRAP_FULL.txt` during transition
- `engine/MANIFEST.json`
- `engine/modules/**/*.txt`
- `releases/LATEST.json`
- `releases/MIGRATIONS.json`
- versioned `releases/YYYY-MM-DD.NN.json`
- `schemas/engine-manifest.schema.json`

Arbitrary repository browsing is forbidden. Empty segments, dot segments, traversal, backslashes, nulls, disallowed extensions/paths and invalid SHA shapes fail closed.

Snapshot responses:
- fetch only `raw.githubusercontent.com/<repo>/C/<runtime-path>`;
- never resolve mutable main;
- carry `X-LWAI-Commit: C` and `X-LWAI-Snapshot-Path`;
- use immutable one-year caching;
- are `noindex, nofollow`.

## Pin-once / no-mix
The modular wrapper supplies C once. Stage-1 uses that C and the supplied same-origin snapshot base for candidate reads.

One startup/update transaction must use one C. Do not mix:
- two snapshot SHAs;
- snapshot bytes and a different GitHub candidate SHA;
- mutable root/config bytes as modular candidate files.

Existing release.resolver/update no-mix, integrity, migration and last-known-good rules remain authoritative.

## Failure behavior
A missing/disallowed/corrupt required file causes modular startup to fail closed according to Stage-1/runtime recovery rules. Transport failure never mutates LOCAL STATE, recreates accounts or downgrades verified state.

The normal one-response installer remains available as compatibility fallback while the experiment is opt-in.

## Fresh-host compatibility matrix
Default cutover remains blocked until ChatGPT fresh-host evidence covers at minimum:

### Host retrieval profiles
- ChatGPT root-to-modular navigation: root is opened from the user's prompt, the explicit `MODULAR_COMPATIBILITY_ENTRY` is followed only when modular testing/use was requested, and exact-C resources are then followed from `/modular` page-provided links;
- ChatGPT without GitHub connector: LastWarAI.com resource links alone must be sufficient;
- partial retrieval: Stage-1 succeeds but one required snapshot module fails;
- stale/incorrect attempt: a different candidate SHA is presented after C is pinned;
- no modular support: host can still consume the unchanged one-response default installer.

### Required account continuity scenario
For every host proposed for default support:
1. start from `https://lastwarai.com`, explicitly request modular transport/testing, and follow the root-provided modular handoff;
2. load an existing durable LWAI account;
3. ingest a screenshot/direct evidence batch containing multiple supported facts;
4. verify the durability-first transaction COMMITTED across canonical state/history/cache/health/update metadata;
5. start a fresh runtime/session;
6. load the same durable account;
7. confirm the newly ingested facts survive without redundant evidence capture.

### Required failure scenario
After durable account load, simulate modular required-file failure. The host must retain last-known-good ENGINE and LOCAL STATE and must not trigger re-onboarding/account recreation.

## Promotion boundary
CI/source tests may promote an additive opt-in endpoint only when live default transport remains unchanged.

Default root/install/config cutover requires a later separate release after:
- opt-in endpoint is actually deployed;
- current Production SHA parity is verified live;
- fresh-host matrix evidence is recorded for supported hosts;
- rollback to the last one-response Production is proven.

## Privacy
The Worker remains transport-only. It contains no account state, gameplay rules, provider data or schema-specific user behavior. Snapshot transport exposes sanitized public Production runtime files only.
