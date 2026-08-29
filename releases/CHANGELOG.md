# Production Changelog

## 2026-08-29.12

- Added executable deterministic runtime regression tests for account routing/isolation, nondestructive start-over/archive, legacy migration, Audit Session isolation, `WAITING_USER`, verify-before-replay/idempotency, checkpoint-loss tolerance, append-only journal exposure and provider capability degradation.
- Changed Production CI from static release-tree validation only to static validation plus behavioral state-machine tests.
- Replaced candidate-specific hard-coded validation with metadata-derived engine/version/schema/API checks.
- Added `engine_api_version` and explicit per-module engine API/workspace schema compatibility ranges.
- Added Git blob byte-identity integrity markers for every module and CI verification against `git hash-object`.
- Replaced the stale legacy engine-manifest schema with a schema describing the actual modular `engine/MANIFEST.json` contract.
- Added `releases/MIGRATIONS.json` as an explicit machine-readable migration graph; `.11 -> .12` is engine-only, schema-preserving and does not require re-onboarding/account rewrite.
- Formalized `storage-api/1` with provider-neutral read/list/write/create/query/atomic-append/CAS/snapshot/restore capabilities and explicit persistence profiles.
- Prohibited guessed-next-row writes as authoritative recovery journal append under concurrency; require atomic append/transaction, revision/CAS, or immutable unique-event strategy.
- Reduced `engine/BOOTSTRAP.txt` to bounded orchestration only; game-domain progression playbooks now live solely in modules and the complete fallback.
- Added a 9KB thin-loader budget and CI guard against domain-playbook leakage into the loader.
- Rebuilt `BOOTSTRAP_FULL.txt` with current storage-capability, compatibility, integrity and behavior-as-tested-code semantics while retaining complete standalone domain behavior.
- Preserved workspace schema `2.3` and all private user/account/runtime state unchanged.

## 2026-08-29.11

- Added workspace-level event-driven Runtime Checkpoints for bounded multi-step work whose interruption would otherwise be ambiguous.
- Added append-only Runtime Journal write-ahead/event history with verified safe points and explicit next actions.
- Added recovery-first startup after Workspace Registry/`active_account_id` resolution: inspect checkpoint/journal plus actual durable artifacts before ordinary continuation.
- Added verify-before-replay/idempotency rules so context loss never causes verified successful writes to be duplicated blindly.
- Added durable `WAITING_USER` handling so declared multi-upload `done` boundaries survive reload; context loss is never implicit batch completion.
- Added account-scoped checkpoint isolation: checkpoint work from one account cannot silently resume while another `active_account_id` is selected.
- Added checkpoint-loss tolerance: operational recovery metadata may disappear without destroying canonical account facts.
- Explicitly prohibited persistence of hidden chain-of-thought, raw internal reasoning, full chat transcripts, or duplicated evidence blobs.
- Added provider-neutral structured/file-only/no-durable-storage checkpoint fallbacks.
- Added resumable engine-release transactions with safe points for private RC staging, GitHub RC creation, CI, merge, post-merge verification, record synchronization, and final commit.
- Preserved last-known-good Production on interrupted/failed pre-merge releases and preserved validated main if a secondary mirror/archive update fails post-merge.
- Updated `core.persistence`, `core.guidance`, `release.runtime`, workspace schema, thin loader, complete fallback, release metadata and recovery regression gates.

## 2026-08-29.10

- Added mandatory `core.guidance` with dependencies on `core.operating`, `core.persistence`, and `core.accounts`.
- Added migration-first startup: inspect accessible prior LWAI state before broad onboarding, preserve source/confidence/freshness, and ask only for missing, ambiguous, contradictory, or materially stale information.
- Added adaptive guidance states (NEW, LEARNING, COMFORTABLE, EXPERT) while keeping privacy, evidence hierarchy, account isolation, and batch-boundary rules invariant.
- Added explicit multi-upload completion boundaries: users are told what to send and to reply `done`; declared batches are not finalized early.
- Added three evidence-equivalent ingestion modes: direct screenshot batches, supported DOCX/PDF screenshot bundles, and phone-friendly guided capture.
- Added account-scoped resumable Audit Sessions with current step, requested/completed/pending/ambiguous items, ingestion mode, guidance level, timestamps, and status.
- Added safe auto-continuation after each validated mini-batch so users do not have to repeatedly request the next step.
- Added missing/stale-only capture rules so current high-confidence fields are not redundantly re-requested.
- Added reversible archive recovery through list/restore/unarchive behavior while preserving immutable `account_id` and history.
- Added session-isolation gates preventing Audit Session state from crossing `active_account_id` boundaries.
- Updated provider-neutral workspace/account-registry schema with optional guidance metadata and Audit Sessions.
- Rebuilt `BOOTSTRAP_FULL.txt` for guided-lifecycle parity and expanded release CI/static gates for guidance, migration-first behavior, archive restore, batch boundaries, ingestion modes, and session isolation.

## 2026-08-29.9

- Added `core.accounts` as mandatory Production behavior for account identity, discovery, isolation, switching and migration.
- Added a workspace-level Account Registry with immutable LWAI-generated `account_id` and `active_account_id` routing.
- Added optional/private game UID plus screenname, alliance, server and nickname as human-recognition metadata; UID is never required for onboarding or account creation.
- Added concise identity/privacy reassurance: identifying values are for the user's own internal/local account management and are not copied into shared LWAI Production.
- Explicitly prohibited routine collection of game passwords, session tokens/cookies, captured authentication files or login credentials.
- Added existing-account discovery before new-account Phase 1, including recognizable account choices and confirmation rather than silently selecting among plausible accounts.
- Added isolated per-account canonical databases/logical namespaces and provider rules that refuse to claim full multi-account persistence when independent safe writes cannot be guaranteed.
- Added first-class context switching through `active_account_id`; reload and terse updates no longer infer account routing from conversational recency.
- Added nondestructive `start over`: create a new clean account and archive the prior registry entry by default.
- Added read-only cross-account comparison that preserves the prior active account unless the user explicitly switches.
- Added identity sanity checks for mutable screenname/alliance/server/optional UID while preserving immutable `account_id` when account continuity is supported.
- Added non-destructive migration from legacy single-account LWAI: register the existing canonical database in place without re-onboarding or rewriting historical domain data.
- Added provider-neutral Account Registry schema, multi-account workspace schema, account-registry contract and expanded migration contract.
- Expanded CI/release gates for account-module completeness, account-registry schema validation, isolation, active-account routing, optional UID behavior, privacy, nondestructive start-over, read-only comparison and migration preservation.
- Rebuilt `BOOTSTRAP_FULL.txt` so the standalone recovery path carries the same multi-account/privacy semantics as the modular loader.

## 2026-08-29.8

- Replaced the monolithic default Production bootstrap with a small `engine/BOOTSTRAP.txt` thin loader.
- Added `engine/MANIFEST.json` as the versioned Production module graph with required/optional modules, dependencies, state scope and load classes.
- Added independently versioned mandatory core, domain-on-demand, capability-on-demand storage, and release/runtime modules under `engine/modules/`.
- Added `engine/BOOTSTRAP_FULL.txt` as the complete sanitized standalone disaster-recovery/offline/manual-transfer runtime.
- Changed default context behavior so routine work loads only mandatory core plus the smallest relevant domain module instead of the entire engine.
- Added fail-closed module retrieval behavior: retry canonical GitHub, retain last-known-good engine where possible, then fall back to `BOOTSTRAP_FULL.txt`; never repair engine failure by overwriting local account state.
- Reworked CI validation to check thin-loader integrity, module-graph dependency resolution, module self-identification/sanitization, required-core coverage, full-fallback completeness and release/version parity.
- Preserved the same one-line TinyURL installer and engine/local-state separation; this release changes engine packaging, not account-state schema.

## 2026-08-29.7

- Added one-line remote bootstrap installation: `Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`.
- Verified the short URL resolves exactly to the canonical raw GitHub Production bootstrap.
- Removed the practical need for users to copy/paste the full multi-page bootstrap when web access is available; the assistant retrieves the Production instructions itself.
- Added remote-install fallback order: short alias -> direct raw GitHub bootstrap -> Google distribution mirror -> manual standalone bootstrap only as a last resort.
- Added `share LWAI` / `give me the install prompt` behavior to return the short one-line installer instead of dumping the full engine.
- Preserved `export yourself` as the complete offline/recovery/self-contained bootstrap path.
- Added supply-chain rule: the URL shortener is transport convenience only; GitHub `main`, `releases/LATEST.json`, and `engine/BOOTSTRAP.txt` remain authoritative.
- Added semi-anonymous distribution behavior: normal public sharing uses the neutral short URL so the maintainer handle is not visible in the install line, while explicitly avoiding claims of true anonymity.
- Added remote-bootstrap health/regression tests and quick-install documentation.

## 2026-08-29.6

- Activated GitHub as the authoritative sanitized Production engineering/source-control hub.
- Preserved each player's cloud/chat workspace as the private runtime spoke; no local account state flows into the public repository.
- Added stable machine-readable `releases/LATEST.json` and raw `engine/BOOTSTRAP.txt` update sources.
- Kept the stable Google Doc as the lowest-friction consumer distribution mirror and fallback update source.
- Formalized consumer engine refresh order: preserve local state -> check GitHub Production manifest -> apply migrations if required -> refresh generic engine layer -> run health checks; fall back to Google Doc or local last-known-good engine.
- Added repository schemas, storage adapter matrix, migration contract, release gates, security boundary, contribution rules and architecture/deployment documentation.
- Added GitHub Actions static Production validation.
- Added explicit hub-and-spoke synchronization/version parity as a release health check.

## 2026-08-29.5

- Compiled Production bootstrap made self-contained.
- Added provider capability abstraction and provider-neutral logical schema.
- Added local-state vs upstream-engine separation.
- Added Gold Assets concept for sanitized shared references.
- Added documentation-as-code release gate.
- Added stable public Production update endpoint.
- Added graceful degradation for cloud/web/image/automation differences.
- Added formal Prod-Dev -> RC -> Production release model.
- Imported the known-good Production engine into the GitHub engineering hub.

## 2026-08-29.4

- Added lossless domain playbooks for screenshots, gear/Ore, Skill Medals, EW, hero shards/WoH, squad-slot tech, counter/meta modeling, formations, Drone/chips, Decorations, Profession/global bonuses, research, stores/paid value, season systems and Battlefield-vs-dueling behavior.
- Formalized recommendation contract and noob-safe onboarding.

## 2026-08-29.3

- Formalized `export yourself`, account snapshot and full recovery package semantics.
- Added capability discovery, cloud-neutral workspace schema, state transaction protocol, reload/staleness behavior, command vocabulary and health tests.

## Earlier Prod-Dev evolution

- Established thin-interface/thick-engine interaction.
- Added rolling Hot Cache, Change Log, Corrections, State Health and staleness model.
- Added external durable-memory architecture and self-healing reconciliation.
