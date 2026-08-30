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
- thin loader, core persistence/guidance, release bootstrap and BOOTSTRAP_FULL contain benefit-triggered persistence-reminder behavior rather than generic recurring nagging;
- release bootstrap/loader/full fallback require canonical-only active-version reporting and automatic canonical GitHub freshness checks;
- BOOTSTRAP_FULL contains complete current account/guidance/recovery/session/storage/integrity/migration/update and domain behavior;
- release validation derives expected version/API/schema from metadata rather than candidate constants;
- migration graph contains required previous-Production edge and historical workspace-schema edges `2.1 -> 2.2 -> 2.3`;
- deterministic runtime tests execute for first-run persistence choice, contextual persistence reminders, canonical-version reporting, automatic engine freshness, account isolation, archive/start-over, legacy migration, current/legacy startup, workspace-schema migration, Audit Session isolation, Runtime Session provenance, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal, provider degradation and installer canonicalization;
- new-user regressions prove no writable provider yields a connect-or-session prompt, writable storage yields a cloud-or-session prompt, session-only remains valid, cloud setup verifies before onboarding, and existing workspaces skip redundant first-run persistence setup;
- persistence-reminder regressions prove a concrete material benefit is required, reminders are capped at one per runtime session, reliable cross-session metadata enforces a seven-day minimum cooldown, and explicit do-not-ask-again suppresses later reminders;
- freshness regressions prove every web-capable runtime startup checks canonical Production, long-lived runtimes recheck after six hours before consequential work, and only newer verified Production may replace the current engine;
- canonical-version regression proves stale alias/cache versions are not announced as active engine generations;
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
- session-only choice does not block normal use or immediately repeat the persistence prompt;
- later persistence reminders occur only when an explicit current-workflow durability benefit exists;
- persistence reminders never occur more than once in one runtime session, honor reliable seven-day cooldown state, and honor `don't ask again` until explicitly reopened;
- existing valid workspace users do not receive redundant first-run persistence prompts;
- installer UX does not describe stale alias/cache version strings as loaded/active engines; only verified canonical GitHub Production is announced;
- every web-capable runtime startup performs a lightweight canonical GitHub freshness check before ordinary domain work;
- a long-lived runtime repeats the canonical freshness check before consequential work only after the six-hour TTL, rather than refetching every message;
- auto-refresh accepts only newer verified Production and rejects older, unverified and RC/Prod-Dev content;
- engine freshness/update never mutates private account state except through separately validated schema migrations when one actually exists;
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
8. session-only persistence reminders require a material workflow benefit;
9. session-only reminders occur at most once per runtime session and respect a reliable seven-day cooldown;
10. `don't ask again` suppresses subsequent benefit-triggered reminders;
11. terse writes route only to `active_account_id`;
12. `start over` archives prior account rather than deleting it;
13. legacy migration preserves canonical facts;
14. current and pre-registry startup ordering establish account context before account-scoped recovery;
15. a registry-backed schema-2.1 workspace migrates to 2.3 before recovery/domain work;
16. `2.1 -> 2.3` migration preserves account facts/history/account routing;
17. repeated migration is a no-op;
18. simulated migration failure restores original schema/state;
19. migration-capable modules declare schema-2.1 support while domain modules can remain 2.3-only;
20. stale alias content cannot downgrade canonical Production;
21. a stale alias version is not announced as the active engine when newer canonical Production is verified;
22. every web-capable runtime startup requires a canonical engine freshness check;
23. long-lived runtime freshness rechecks after six hours, not before;
24. only newer verified Production is adopted; older, unverified and RC content leaves current Production unchanged;
25. an LWAI `runtime_session_id` exists without host-session reference;
26. duplicate/different host refs cannot merge/duplicate immutable accounts;
27. Audit Session ownership remains account-scoped;
28. `WAITING_USER` prevents continuation until boundary closes;
29. account-scoped checkpoints cannot cross `active_account_id`;
30. verify-before-replay skips already-durable writes;
31. recovery applies only missing actions once;
32. a COMMITTED checkpoint is not replayed during schema migration;
33. checkpoint loss cannot destroy canonical facts;
34. journal exposure is append-only;
35. provider profiles degrade according to verified capabilities.

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
- benefit-triggered reminders are contextual and suppressible rather than a generic timer-driven nag;
- engine freshness checks are lightweight metadata checks until a newer verified Production is discovered;
- alias/cache version strings never become authoritative active-version reporting;
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
