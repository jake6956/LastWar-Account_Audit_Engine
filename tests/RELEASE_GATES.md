# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required loader, module graph, migration graph, full fallback, core/account/guidance/persistence modules, storage adapter, release modules, schemas, contracts and recovery documentation exist;
- `LATEST.json`, module manifest, loader and full fallback versions/API/schema agree;
- manifests assert `sanitized=true` and `account_state_included=false`;
- module graph dependencies resolve, contain no cycles and required modules are marked required;
- every module self-identifies with exact `module_id` / `module_version` and sanitization headers;
- every module declares engine API/workspace schema compatibility that includes current Production;
- migration-capable core/release/storage components explicitly support validated historical workspace schemas `2.1` through `2.3` while domain modules remain current-schema-only where intended;
- every module `integrity.git_blob_sha1` exactly matches `git hash-object` for checked-out bytes;
- `schemas/engine-manifest.schema.json` describes the actual modular MANIFEST shape;
- `core.guidance` depends on operating/persistence/accounts;
- account-registry schema retains optional guidance and Audit Sessions;
- provider-neutral workspace schema retains optional Runtime Sessions, Runtime Checkpoints and Runtime Journal;
- storage adapter exposes `storage-api/1`, explicit capabilities, persistence profiles and concurrency-safe journal rules;
- thin loader is <= 9KB, contains orchestration/recovery/integrity/migration-bootstrap behavior and does not embed game-domain playbooks;
- thin loader, mandatory core guidance/persistence/accounts, release bootstrap and BOOTSTRAP_FULL all contain an explicit genuinely-new-user persistence gate before identity onboarding;
- BOOTSTRAP_FULL contains complete current account/guidance/recovery/session/storage/integrity/migration and domain behavior;
- release validation derives expected version/API/schema from metadata rather than candidate constants;
- migration graph contains required previous-Production edge and historical workspace-schema edges `2.1 -> 2.2 -> 2.3`;
- deterministic runtime tests execute for first-run persistence choice, account isolation, archive/start-over, legacy migration, current/legacy startup, workspace-schema migration, Audit Session isolation, Runtime Session provenance, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal, provider degradation and installer canonicalization;
- new-user regressions prove no writable provider yields a connect-or-session prompt, writable storage yields a cloud-or-session prompt, session-only remains valid, cloud setup verifies before onboarding, and existing workspaces skip redundant persistence setup;
- workspace migration regressions prove canonical account facts/history/account_id/active_account_id survive `2.1 -> 2.3`, migration is idempotent, failed migration rolls back, and COMMITTED checkpoints are not replayed;
- manifest regressions prove migration-capable modules can bootstrap schema `2.1` and domain modules requiring `2.3` remain blocked before target schema;
- stale short-link/cache content cannot override a newer verified canonical GitHub Production identity;
- README current Production identity matches release metadata and includes the one-line installer;
- generic credential/private-key leakage patterns and known private release markers are absent.

## Required private pre-promotion checks
- private-identifier/account/provider-reference denylist scan across exact candidate patch/tree;
- no actual Runtime Session rows/host-session refs, Runtime Checkpoint/Journal rows, account IDs or user-specific pending actions in public candidate;
- local-state preservation/migration test;
- module graph/full fallback parity test;
- capability/provider fallback test;
- brand-new user without writable storage is explicitly offered supported-cloud connection or session-only before identity intake;
- brand-new user with verified writable storage is explicitly offered private workspace creation or session-only before identity intake;
- `storage connected` triggers capability re-detection and does not trust the declaration alone;
- session-only choice does not block normal use and does not produce repeated persistence nagging;
- existing valid workspace users do not receive redundant persistence prompts;
- legacy state reuse and multi-account isolation tests;
- existing schema-2.1/2.2 workspace migration test using sanitized fixtures only;
- migration failure leaves source workspace authoritative and suppresses redundant onboarding;
- guidance/direct-document-guided ingestion and explicit `done` boundary tests;
- account-scoped Audit Session isolation;
- runtime_session_id remains usable when host_session_ref is absent;
- host_session_ref remains optional/private and cannot become account identity, authentication, routing, recovery ordering, idempotency or game evidence;
- normal operation never asks the user to create a ChatGPT shared link or retrieve a conversation GUID;
- recovery after context loss following successful writes does not replay verified writes;
- persisted `WAITING_USER` boundary survives reload and does not finalize early;
- account-scoped checkpoint cannot resume/mutate under another `active_account_id`;
- deleting/losing checkpoint/provenance storage cannot delete canonical facts;
- Runtime Journal remains append-only using atomic append, CAS/revision control or immutable unique-event strategy;
- recovery works without hidden chain-of-thought/full transcript;
- installer alias is transport only and canonical GitHub metadata is checked before accepting version identity;
- interrupted release before merge leaves last-known-good main unchanged;
- release retry verifies branch/PR/commit/CI/archive state before replay;
- exact-head PR CI succeeds on final candidate SHA;
- after merge, main CI succeeds and loader/manifest/fallback/modules/release metadata agree;
- public endpoints are readable and one-line installer resolves to canonical Production loader.

## Executable regression scenarios
The deterministic reference runtime must prove at minimum:
1. a genuinely new user without writable persistence stops at a connect-or-session choice before onboarding;
2. a genuinely new user with writable persistence stops at a cloud-or-session choice before onboarding;
3. explicit session-only choice proceeds to onboarding without creating a durable workspace;
4. explicit cloud choice creates and verifies the private workspace before onboarding;
5. `storage connected` causes capability re-check rather than immediate onboarding;
6. unverified cloud choice fails closed;
7. an existing valid workspace bypasses the first-run persistence gate;
8. terse writes route only to `active_account_id`;
9. `start over` archives prior account rather than deleting it;
10. legacy migration preserves canonical facts;
11. current and pre-registry startup ordering establish account context before account-scoped recovery;
12. a registry-backed schema-2.1 workspace migrates to 2.3 before recovery/domain work;
13. `2.1 -> 2.3` migration preserves account facts/history/account routing;
14. repeated migration is a no-op;
15. simulated migration failure restores original schema/state;
16. migration-capable modules declare schema-2.1 support while domain modules can remain 2.3-only;
17. stale alias content cannot downgrade canonical Production;
18. an LWAI `runtime_session_id` exists without host-session reference;
19. duplicate/different host refs cannot merge/duplicate immutable accounts;
20. Audit Session ownership remains account-scoped;
21. `WAITING_USER` prevents continuation until boundary closes;
22. account-scoped checkpoints cannot cross `active_account_id`;
23. verify-before-replay skips already-durable writes;
24. recovery applies only missing actions once;
25. a COMMITTED checkpoint is not replayed during schema migration;
26. checkpoint loss cannot destroy canonical facts;
27. journal exposure is append-only;
28. provider profiles degrade according to verified capabilities.

## Non-executable contract regressions
- shared gear remains transferable within an account rather than hero-owned;
- default and specialist presets remain separate;
- squad-slot tech stays tied to actual deployment slot;
- formation left/right is explicit before lateral advice;
- stale volatile values do not drive consequential recommendations;
- research includes prerequisite/opportunity cost;
- user corrections supersede stale engine assumptions;
- engine refresh preserves Workspace Registry, `active_account_id`, every account namespace, Audit Sessions, optional Runtime Sessions, Runtime Checkpoints and Runtime Journal;
- no-cloud deployment functions without claiming durable recovery/provenance;
- unsupported provider capabilities are never invented;
- new-user persistence choice occurs before account identity collection;
- session-only remains a supported explicit choice;
- UID remains optional/private;
- existing state is discovered before redundant onboarding;
- supported older workspace schemas migrate before normal domain work;
- unsupported/no-path schemas fail closed rather than re-onboard;
- cross-account compare is read-only;
- archive/restore preserves immutable `account_id` and history;
- direct screenshots, supported bundles and guided capture preserve evidence/confidence rules;
- host-session provenance is metadata only;
- actual consumer identities/runtime rows/provider-local IDs/paths never appear in public Production;
- failed/interrupted pre-merge releases preserve last-known-good main;
- post-merge secondary mirror/archive failure does not rewrite validated main.
