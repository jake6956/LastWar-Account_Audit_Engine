# Release Engineering Contract

Contract revision: 2026-08-29.12

## Channels
- **Prod-Dev:** private live development/proving ground; may contain real account data and private provider references.
- **Release Candidate:** sanitized frozen candidate on GitHub `rc/<engine-version>` plus private release records.
- **Production:** sanitized public engine on GitHub `main`.

## Production invariant
`main` is last-known-good Production. A candidate must not reach `main` until the exact candidate head has passed required public CI and private gates. If candidate head changes after validation, validation is stale and must run again.

Repository settings SHOULD enforce this process mechanically with required PRs, required Production validation, blocked force-push and blocked branch deletion. When repository-control APIs are unavailable, process enforcement remains mandatory and the missing infrastructure control is tracked explicitly.

## Promotion path
`Private Prod-Dev -> frozen sanitized RC -> GitHub rc/<version> -> PR -> exact-head CI + private gates -> merge exact validated head -> main CI/public verification -> versioned private Production archive/release records`

## Public release tree
A complete candidate contains:
- bounded `engine/BOOTSTRAP.txt` orchestration loader;
- `releases/LATEST.json` Production identity;
- `releases/MIGRATIONS.json` explicit migration graph;
- `engine/MANIFEST.json` dependency/compatibility/integrity graph;
- independently versioned modules;
- `engine/BOOTSTRAP_FULL.txt` complete standalone fallback;
- contracts, schemas, docs and release metadata;
- static validator plus executable deterministic runtime regressions.

## Required automated gates
1. Release identity: loader/fallback/LATEST/MANIFEST engine version, engine API and schema agree.
2. Sanitization flags are true/false as required and credential/private-key patterns are absent.
3. Module DAG resolves without missing dependencies or cycles.
4. Required modules remain required and module headers match manifest identity/version.
5. Every module's Git blob byte identity matches manifest integrity metadata.
6. Module engine API/workspace schema ranges include current Production.
7. Manifest schema describes the actual modular manifest contract.
8. Required migration edge exists and declares local-state behavior.
9. Thin loader remains within bounded size and excludes known domain playbooks.
10. BOOTSTRAP_FULL retains complete current recovery/storage/domain behavior.
11. Storage adapter exposes explicit capability semantics and concurrency-safe journal rules.
12. Runtime behavioral tests execute and pass for account isolation/recovery/provider degradation.
13. README/release metadata/install endpoint are consistent.

## Required private gates
- denylist scan against actual private identities/account/provider references;
- no consumer-local checkpoint/journal rows or pending work in public candidate;
- local-state preservation and migration verification;
- account/session/checkpoint isolation;
- document/direct/guided ingestion and `done` boundary behavior;
- verify-before-replay/idempotency under interrupted writes;
- provider capability fallback/concurrency checks;
- BOOTSTRAP_FULL parity review;
- exact-head PR CI success;
- one-line installer verification.

## Consumer distribution hierarchy
1. Preferred human install alias: https://tinyurl.com/2yxf7f5x
2. Canonical raw loader: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt
3. Canonical release metadata: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
4. Canonical module graph: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json
5. Canonical full fallback: https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt
6. Secondary legacy mirror when readable.

The shortener is transport convenience only. GitHub `main` is authoritative.

## Merge discipline
- Create RC from current verified `main`.
- Freeze intended candidate changes before final CI.
- Open PR to `main` with target version, migration type and state-preservation statement.
- Read exact PR head SHA after all candidate writes.
- Require CI success associated with that exact head.
- Merge with `expected_head_sha`; if GitHub rejects because head moved, do not bypass it.
- Require post-merge main CI success.

## Failure behavior
Any pre-merge gate failure leaves `main` untouched. A post-merge secondary mirror/archive failure does not silently roll back healthy GitHub Production; record synchronization degradation and retry privately. Installer/TinyURL mismatch is a release-health failure requiring review, while direct canonical GitHub remains the source authority.

## Versioning and compatibility
Engine versions use `YYYY-MM-DD.N`. Production also declares `engine_api_version` and workspace schema version. Per-module API/schema ranges make compatibility explicit. `releases/MIGRATIONS.json` declares supported transitions.

Engine-only updates preserve private state in place and must not force re-onboarding. Schema-breaking transitions require explicit migration edge, reversible/snapshot-aware procedure where capabilities exist, and preservation tests before promotion.

## Rollback
Rollback is a new validated RC/PR targeting a known-good release tree. Never mutate private user state merely to make an older engine load. If a schema downgrade is unsafe, remain on last-known-good compatible engine instead of improvising data loss.

## Privacy
Production PRs contain generic engine behavior only. Actual account identity/state, private Drive IDs/paths, screenshots, balances, Corrections, battles, checkpoints/journal rows, credentials and user-specific pending work never enter GitHub.
