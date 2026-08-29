# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required loader, module graph, migration graph, full fallback, core/account/guidance/persistence modules, storage adapter, release modules, schemas, contracts and recovery documentation exist;
- `LATEST.json`, module manifest, loader and full fallback versions/API/schema agree;
- manifests assert `sanitized=true` and `account_state_included=false`;
- module graph dependencies resolve, contain no cycles and required modules are marked required;
- every module self-identifies with exact `module_id` / `module_version` and sanitization headers;
- every module declares engine API/workspace schema compatibility that includes current Production;
- every module `integrity.git_blob_sha1` exactly matches `git hash-object` for the checked-out bytes;
- `schemas/engine-manifest.schema.json` describes the actual modular MANIFEST shape rather than a legacy release manifest;
- `core.guidance` depends on operating/persistence/accounts;
- account-registry schema retains optional guidance and Audit Sessions;
- provider-neutral workspace schema retains Runtime Checkpoints and Runtime Journal;
- storage adapter exposes `storage-api/1`, explicit capabilities, persistence profiles and concurrency-safe authoritative journal rules;
- thin loader is bounded to <= 9KB, contains orchestration/recovery/integrity behavior and does not embed known game-domain playbooks;
- BOOTSTRAP_FULL contains complete current account/guidance/recovery/storage/integrity and domain behavior;
- release validation derives expected version/API/schema from release metadata rather than hard-coded candidate numbers;
- migration graph contains the required edge from previous promoted Production to candidate and preserves local state where declared;
- deterministic runtime behavioral tests execute in CI for account isolation, nondestructive start-over/archive, legacy migration, Audit Session isolation, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal surface and provider degradation;
- README current Production identity matches release metadata and includes the one-line installer;
- generic credential/private-key leakage patterns and known private release markers are absent.

## Required private pre-promotion checks
- private-identifier/account/provider-reference denylist scan across exact candidate patch/tree;
- no actual Runtime Checkpoint/Runtime Journal rows or user-specific pending actions in public candidate;
- local-state preservation/migration test;
- module graph/full fallback parity test;
- capability/provider fallback test;
- legacy state reuse and multi-account isolation tests;
- guidance/direct-document-guided ingestion and explicit `done` boundary tests;
- account-scoped Audit Session isolation;
- recovery after context loss following successful writes does not replay verified writes;
- persisted `WAITING_USER` boundary survives reload and does not finalize early;
- account-scoped checkpoint cannot resume/mutate under another `active_account_id`;
- deleting/losing checkpoint storage cannot delete canonical account facts;
- Runtime Journal remains append-only using atomic append, CAS/revision control or immutable unique-event strategy;
- recovery is possible without hidden chain-of-thought/full transcript;
- interrupted release before merge leaves last-known-good main unchanged;
- release retry verifies branch/PR/commit/CI/archive state before replay;
- exact-head PR CI succeeds on final candidate SHA;
- after merge, main CI succeeds and loader/manifest/fallback/modules/release metadata agree;
- public endpoints are readable and one-line installer resolves to canonical Production loader.

## Executable regression scenarios
The deterministic reference runtime must prove at minimum:
1. terse writes route only to `active_account_id`;
2. `start over` archives prior account rather than deleting it;
3. legacy migration preserves canonical facts;
4. Audit Session ownership remains account-scoped;
5. `WAITING_USER` prevents automatic continuation until boundary closes;
6. account-scoped checkpoints cannot cross `active_account_id`;
7. verify-before-replay skips an already-durable write;
8. recovery applies only missing actions once;
9. checkpoint loss cannot destroy canonical facts;
10. journal exposure is append-only;
11. provider profiles degrade according to verified capabilities and never overclaim authoritative journal semantics.

## Non-executable contract regressions
- shared gear remains transferable within an account rather than hero-owned;
- default and specialist presets remain separate;
- squad-slot tech stays tied to actual deployment slot;
- formation left/right is explicit before lateral advice;
- stale volatile values do not drive consequential recommendations;
- research includes prerequisite/opportunity cost;
- user corrections supersede stale engine assumptions;
- engine refresh preserves Workspace Registry, `active_account_id`, every account-local namespace, Audit Sessions, Runtime Checkpoints and Runtime Journal;
- no-cloud deployment still functions and does not claim durable checkpointing;
- unsupported provider capabilities are never invented;
- UID remains optional/private and declining it never blocks account creation;
- existing state is discovered before redundant onboarding;
- cross-account compare is read-only;
- archive/restore preserves immutable `account_id` and history;
- direct screenshots, supported bundles and guided capture preserve evidence/confidence rules;
- actual consumer identities/checkpoint rows/provider-local IDs/paths and user-specific pending actions never appear in public Production;
- failed/interrupted pre-merge releases preserve last-known-good main;
- post-merge secondary mirror/archive failure does not rewrite validated main.
