# Modular Transport Compatibility Contract

Version: 2026-09-28.48

## Purpose
Document the retained non-default modular/recovery transport and the supported ChatGPT bootstrap boundary. Multi-request modular transport remains useful for direct/recovery-capable hosts and diagnostics, but it is not the supported fresh-install path for ChatGPT.

## Supported default installer
The supported ChatGPT installer is one fetch of the user-supplied bare origin:

`https://lastwarai.com`

The Worker resolves canonical GitHub Production `main` server-side to exact commit C and returns the complete exact-C compiled `engine/BOOTSTRAP_FULL.txt` configuration in the same response. `/`, `/install`, and `/config.txt` remain the supported default one-response transport.

The public response is transport, not version authority. GitHub live `main` commit.sha remains current Production authority.

## ChatGPT host evidence
Fresh-host testing established this retrieval model for the supported ChatGPT path:
- an initial user-supplied bare LastWarAI origin is retrievable;
- path variants and query-string variants are not reliably retrievable through the same fresh-web path;
- a page-provided second network hop is not reliably retrievable, including a second valid bare LastWarAI hostname.

Therefore supported ChatGPT bootstrap is treated as a one-fetch host. Do not require a second URL, GitHub connector, search substitution, query transport, path transport, or hostname chaining for normal installation.

Default modular cutover is closed for the supported ChatGPT host unless host retrieval capabilities materially change and are deliberately revalidated.

## Retained compatibility endpoints
The existing non-default compatibility surfaces may remain available:
- `GET /modular`
- `GET /modular/config.txt`
- `GET /snapshot/C/<runtime-path>`

They are not normal install dependencies and are absent from default install discovery.

`/modular` may resolve live Production C, return Stage-1 and declare:
- `RESOLVED_PRODUCTION_COMMIT: C`
- `FIRST_PARTY_SNAPSHOT_BASE: https://lastwarai.com/snapshot/C/`

`/snapshot/C/<runtime-path>` remains exact-SHA/immutable transport for allowlisted sanitized runtime files only. Arbitrary repository browsing, invalid SHA shapes, traversal, dot segments, backslashes/nulls, and disallowed paths fail closed.

## Pin-once / no-mix
Any direct/modular/recovery transaction uses one C. Never mix:
- two snapshot SHAs;
- snapshot bytes with a different GitHub candidate SHA;
- mutable root/config bytes as modular candidate files;
- recovery-package bytes with network candidate bytes.

Existing resolver/updater integrity, migration, and last-known-good rules remain authoritative.

## Failure behavior
Compatibility transport failure never mutates LOCAL STATE, recreates accounts, forces re-onboarding, downgrades verified state, or authorizes guessed current Production. Use last-known-good compatible ENGINE or validated recovery material when available.

The supported one-response root remains independent of compatibility-route failure.

## Durable-state regression
Transport architecture changes must continue proving that durable account state survives runtime loss:
1. load an existing durable account;
2. ingest a multi-fact screenshot/direct-evidence batch;
3. verify the durability-first transaction COMMITTED across canonical state/history/cache/health metadata;
4. start a fresh runtime/session;
5. load the same durable account;
6. confirm the new facts survive without redundant capture.

This regression protects persistence semantics even though supported ChatGPT fresh install is single-response.

## Compiled single-response architecture
Canonical behavior remains modular in GitHub. The supported ChatGPT artifact is generated deterministically from owned compact standalone capsules plus MANIFEST identity. `engine/BOOTSTRAP_FULL.txt` is compiler output, not a second hand-authored runtime.

CI must regenerate the artifact and fail on any byte mismatch. A source-module change must update the standalone ownership fingerprint so its compact projection is explicitly reviewed.

## Privacy
All public transport artifacts are sanitized ENGINE only. They contain no player/account state, private provider references, credentials, screenshots, or maintainer-private state.
