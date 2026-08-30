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
- provider-neutral workspace schema retains optional Runtime Sessions plus Runtime Checkpoints and Runtime Journal;
- storage adapter exposes `storage-api/1`, explicit capabilities, persistence profiles and concurrency-safe authoritative journal rules;
- thin loader is bounded to <= 9KB, contains orchestration/recovery/integrity behavior and does not embed known game-domain playbooks;
- BOOTSTRAP_FULL contains complete current account/guidance/recovery/session-provenance/storage/integrity and domain behavior;
- release validation derives expected version/API/schema from release metadata rather than hard-coded candidate numbers;
- migration graph contains the required edge from previous promoted Production to candidate and preserves local state where declared;
- deterministic runtime behavioral tests execute in CI for account isolation, nondestructive start-over/archive, legacy migration, Audit Session isolation, optional Runtime Session provenance isolation, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal surface and provider degradation;
- runtime-session tests prove operation without a host reference, prove duplicate host references do not merge Runtime Sessions/accounts, prove distinct host references do not duplicate immutable accounts, and prove a matching host reference cannot bypass `active_account_id` checkpoint isolation;
- README current Production identity matches release metadata and includes the one-line installer;
- generic credential/private-key leakage patterns and known private release markers are absent.

## Required private pre-promotion checks
- private-identifier/account/provider-reference denylist scan across exact candidate patch/tree;
- no actual Runtime Session rows/host-session references, Runtime Checkpoint/Runtime Journal rows or user-specific pending actions in public candidate;
- local-state preservation/migration test;
- module graph/full fallback parity test;
- capability/provider fallback test;
- legacy state reuse and multi-account isolation tests;
- guidance/direct-document-guided ingestion and explicit `done` boundary tests;
- account-scoped Audit Session isolation;
- runtime_session_id remains usable when host_session_ref is absent;
- host_session_ref remains optional/private and cannot become account identity, authentication, routing, recovery ordering, idempotency/deduplication or canonical game evidence;
- normal operation never asks the user to create a ChatGPT shared link or retrieve a conversation GUID;
- recovery after context loss following successful writes does not replay verified writes;
- persisted `WAITING_USER` boundary survives reload and does not finalize early;
- account-scoped checkpoint cannot resume/mutate under another `active_account_id`, even when host provenance matches;
- deleting/losing checkpoint or session-provenance storage cannot delete canonical account facts;
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
4. current and legacy startup ordering establish account context before account-scoped recovery;
5. an LWAI `runtime_session_id` exists without any host-session reference;
6. duplicate host-session references do not merge Runtime Sessions or account state;
7. distinct host-session references may belong to the same immutable account without creating duplicates;
8. Audit Session ownership remains account-scoped and may carry optional runtime_session_id provenance;
9. `WAITING_USER` prevents automatic continuation until boundary closes;
10. account-scoped checkpoints cannot cross `active_account_id`, including when host-session provenance matches;
11. verify-before-replay skips an already-durable write;
12. recovery applies only missing actions once;
13. checkpoint loss cannot destroy canonical facts;
14. journal exposure is append-only;
15. provider profiles degrade according to verified capabilities and never overclaim authoritative journal semantics.

## Non-executable contract regressions
- shared gear remains transferable within an account rather than hero-owned;
- default and specialist presets remain separate;
- squad-slot tech stays tied to actual deployment slot;
- formation left/right is explicit before lateral advice;
- stale volatile values do not drive consequential recommendations;
- research includes prerequisite/opportunity cost;
- user corrections supersede stale engine assumptions;
- engine refresh preserves Workspace Registry, `active_account_id`, every account-local namespace, Audit Sessions, optional Runtime Sessions, Runtime Checkpoints and Runtime Journal;
- no-cloud deployment still functions and does not claim durable checkpointing/provenance;
- unsupported provider capabilities are never invented;
- UID remains optional/private and declining it never blocks account creation;
- existing state is discovered before redundant onboarding;
- cross-account compare is read-only;
- archive/restore preserves immutable `account_id` and history;
- direct screenshots, supported bundles and guided capture preserve evidence/confidence rules;
- host-session provenance is metadata only and never becomes game evidence;
- actual consumer identities/runtime-session rows/host references/checkpoint rows/provider-local IDs/paths and user-specific pending actions never appear in public Production;
- failed/interrupted pre-merge releases preserve last-known-good main;
- post-merge secondary mirror/archive failure does not rewrite validated main.
