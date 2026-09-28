# Opt-In Modular Public Transport Contract

Version: 2026-09-28.46

## Purpose
Define the non-default Phase-2 transport experiment for LastWarAI.com without changing the supported root/install/config installer.

Production .46 is a compatibility-evidence release candidate, not authorization for default cutover.

## Default installer remains unchanged
The following mutable public endpoints remain the supported default and continue returning the complete exact-commit BOOTSTRAP_FULL configuration in one response:
- `/`
- `/install`
- `/config.txt`

The opt-in modular path is not linked from About, sitemap, install instructions or other default discovery surfaces in .46.

## Opt-in modular bootstrap
`GET /modular` and `GET /modular/config.txt`:
1. resolve canonical GitHub Production `main` server-side to exact 40-hex commit C;
2. retrieve `engine/BOOTSTRAP.txt` from exact C;
3. sanity-check Stage-1 Production/sanitization/modular identity;
4. return a transparent wrapper plus Stage-1 in the same response;
5. declare:
   - `RESOLVED_PRODUCTION_COMMIT: C`
   - `FIRST_PARTY_SNAPSHOT_BASE: https://lastwarai.com/snapshot/C/`
6. return `X-LWAI-Commit: C`, `X-LWAI-Snapshot-Base`, and transport version `3.2-modular-optin`;
7. use mutable no-store headers and `X-Robots-Tag: noindex, nofollow`.

Failure to resolve C or validate Stage-1 returns 503 and never falls back to guessed/cached mutable source.

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
Default cutover remains blocked until fresh-host evidence covers at minimum:

### Host retrieval profiles
- same-origin-only host: LastWarAI.com available; direct GitHub/raw access unavailable;
- normal web host: LastWarAI.com and GitHub available;
- partial retrieval: Stage-1 succeeds but one required snapshot module fails;
- stale/incorrect attempt: a different candidate SHA is presented after C is pinned;
- no modular support: host can still consume the unchanged one-response default installer.

### Required account continuity scenario
For every host proposed for default support:
1. start from the opt-in modular endpoint;
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
