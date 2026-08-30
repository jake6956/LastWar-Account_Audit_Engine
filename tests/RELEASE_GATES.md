# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required loader, module graph, migration graph, full fallback, core/account/guidance/persistence modules, storage adapter, release modules, schemas, contracts and recovery documentation exist;
- `LATEST.json`, module manifest, loader and full fallback versions/API/schema agree;
- manifests assert `sanitized=true` and `account_state_included=false`;
- preferred public installer is the first-party `https://lastwarai.com` endpoint and the exact one-line instruction is synchronized across current docs/runtime metadata;
- previously circulated `https://tinyurl.com/2yxf7f5x` is recorded only as a legacy compatibility alias and is not a runtime dependency/version authority;
- live first-party Stage-0 endpoint returns HTTP 200 plaintext, sanitized/version-neutral locator content, the canonical GitHub live-ref URL, `commit.sha`, and exact-commit `engine/BOOTSTRAP.txt` handoff;
- public Stage-0 transport is explicitly non-authoritative for current version; current Production comes only from live GitHub `main` commit.sha;
- module graph dependencies resolve, contain no cycles and required modules are marked required;
- every module self-identifies with exact `module_id` / `module_version` and sanitization headers;
- every module declares engine API/workspace schema compatibility that includes current Production;
- every module `integrity.git_blob_sha1` exactly matches `git hash-object` for checked-out bytes;
- `schemas/engine-manifest.schema.json` describes the actual modular MANIFEST shape;
- migration-capable core/release/storage components support validated historical workspace schemas `2.1` through `2.3` while domain modules remain current-schema-only where intended;
- migration graph contains the required previous-Production edge and historical workspace-schema edges `2.1 -> 2.2 -> 2.3`;
- thin Stage-1 loader is <= 4 KiB, orchestration-only, contains live-ref/exact-commit resolution and does not embed public-installer, provider/account onboarding or game-domain policy;
- BOOTSTRAP_FULL contains complete current account/guidance/recovery/session/storage/integrity/migration/update and domain behavior;
- storage adapter exposes `storage-api/1`, explicit capabilities, persistence profiles, absolute workspace isolation and concurrency-safe journal rules;
- deterministic runtime tests execute for first-run persistence choice, contextual persistence reminders, canonical-version reporting, automatic engine freshness, account isolation, archive/start-over, legacy migration, current/legacy startup, workspace-schema migration, Audit Session isolation, Runtime Session provenance, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal, provider degradation and installer canonicalization;
- README current Production identity matches release metadata and includes the first-party one-line installer;
- generic credential/private-key leakage patterns and known private release markers are absent.

## Installer acceptance tests
1. Fresh user prompt is exactly `Set up Last War optimization using the instructions at https://lastwarai.com`.
2. `https://lastwarai.com` returns the small plaintext Stage-0 locator, not a redirect/interstitial or full account engine.
3. Locator includes no engine version and no private/account state.
4. Locator instructs the host to resolve `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main` and use current `commit.sha`.
5. Stage-1 and all trusted release/module reads use one exact immutable commit.
6. Stale/cached alias/README/raw-main content cannot override a newer live GitHub Production identity.
7. Legacy TinyURL may remain usable for an already-circulated prompt, but new `share LWAI` output never returns it.
8. Public-entrypoint failure never mutates LOCAL STATE and existing compatible deployments can retain last-known-good ENGINE.

## Required private pre-promotion checks
- private-identifier/account/provider-reference denylist scan across exact candidate patch/tree;
- no actual Runtime Session rows/host-session refs, Runtime Checkpoint/Journal rows, account IDs or user-specific pending actions in public candidate;
- local-state preservation/migration test;
- module graph/full fallback parity test;
- capability/provider fallback test;
- legacy state reuse and multi-account isolation tests;
- guidance/direct-document-guided ingestion and explicit `done` boundary tests;
- account-scoped Audit Session/checkpoint isolation;
- runtime_session_id remains usable when host_session_ref is absent and host_session_ref remains non-authoritative;
- recovery after context loss following successful writes does not replay verified writes;
- persisted `WAITING_USER` boundary survives reload and does not finalize early;
- Runtime Journal remains append-only using atomic append, CAS/revision control or immutable unique-event strategy;
- installer transport is non-authoritative and live GitHub exact-commit resolution is verified before active-version claims;
- exact-head PR CI succeeds on final candidate SHA;
- after merge, main CI succeeds including live LastWarAI.com endpoint validation;
- interrupted release before merge leaves last-known-good main unchanged.

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
- UID remains optional/private;
- existing state is discovered before redundant onboarding;
- supported older workspace schemas migrate before normal domain work;
- unsupported/no-path schemas fail closed rather than re-onboard;
- cross-account compare is read-only;
- archive/restore preserves immutable `account_id` and history;
- actual consumer identities/runtime rows/provider-local IDs/paths never appear in public Production;
- failed/interrupted pre-merge releases preserve last-known-good main.
