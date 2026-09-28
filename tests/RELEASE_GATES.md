# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required loader, module graph, migration graph, full fallback, core/account/guidance/persistence modules, storage adapter, release modules, schemas, contracts and recovery documentation exist;
- `LATEST.json`, module manifest, loader and full fallback versions/API/schema agree;
- manifests assert `sanitized=true` and `account_state_included=false`;
- preferred public installer is the first-party `https://lastwarai.com` endpoint and the exact one-line instruction is synchronized across current docs/runtime metadata;
- deprecated URL shorteners are unsupported and absent from active runtime/current release metadata; historical release records may retain them only as history;
- supported LastWarAI.com root/config endpoints return HTTP 200 plaintext, the complete sanitized exact-commit BOOTSTRAP_FULL configuration, current `X-LWAI-Commit`, strong no-store headers and live GitHub Production parity;
- first-party transport remains delivery infrastructure rather than version authority; current Production comes from live GitHub `main` commit.sha;
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
- recommendation-governance contract is present and automated consistency tests prove goal-first optimization, proactive preflight, no-false-winner behavior, research-before-guess, irreversible transaction-evidence gating, automatic confirmed-defect capture, module monotonicity and fallback parity;
- research topology tests prove visibly terminal tech nodes cannot be given invented downstream unlocks and ambiguous/cropped continuation requests resolving evidence;
- deterministic runtime tests execute for first-run persistence choice, contextual persistence reminders, canonical-version reporting, automatic engine freshness, account isolation, archive/start-over, legacy migration, current/legacy startup, workspace-schema migration, Audit Session isolation, Runtime Session provenance, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal, provider degradation and installer canonicalization;
- README current Production identity matches release metadata and includes the first-party one-line installer;
- generic credential/private-key leakage patterns and known private release markers are absent.

## Installer acceptance tests
1. Fresh user prompt is exactly `Set up Last War optimization using the instructions at https://lastwarai.com`.
2. `https://lastwarai.com`, `/install` and `/config.txt` remain the supported default one-response BOOTSTRAP_FULL transport until an explicitly promoted cutover release.
3. Root/config expose current `X-LWAI-Commit`, sanitized/no-account-state identity, strong mutable no-cache headers and exact live-GitHub Production parity.
4. Stage-1 and all trusted release/module reads use one exact immutable commit; stale/cached alias/README/raw-main content cannot override newer live GitHub Production.
5. Deprecated URL shorteners are unsupported; `share LWAI` returns only the LastWarAI.com installer.
6. Public-entrypoint failure never mutates LOCAL STATE and existing compatible deployments can retain last-known-good ENGINE.
7. During .47 ChatGPT compatibility testing, `/modular` is opt-in/noindex-but-followable, resolves C server-side, returns Stage-1 plus `FIRST_PARTY_SNAPSHOT_BASE` and `FIRST_PARTY_RESOURCE_INDEX`, and links every exact-C runtime artifact without altering root/install/config.
8. `/snapshot/C/<runtime-path>` accepts only exact 40-hex C plus allowlisted runtime paths, is immutable, rejects traversal/disallowed paths before raw retrieval, and never resolves mutable main.
9. Default modular cutover remains blocked until live deployment plus fresh ChatGPT evidence passes: page-linked exact-C resource traversal, durable account load -> multi-fact screenshot/direct-update commit -> fresh runtime recovery, and failure/rollback preservation.

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


## Deterministic recovery-package gate
Every candidate must build a sanitized multi-file recovery package from the exact candidate SHA and validate it before promotion.

Required checks:
- identical source + options produce byte-identical ZIP bytes;
- RECOVERY_MANIFEST / LATEST / MANIFEST identity agrees;
- SHA256SUMS covers exact package payload bytes;
- every MANIFEST module exists and reproduces its declared Git blob identity;
- no package/network mixing is permitted during recovery;
- a package built without BOOTSTRAP_FULL is still structurally complete for modular recovery;
- tampering with a payload file fails validation;
- no account/private maintainer state appears in the package;
- the exact validated RC package is mirrored privately before merge and the actual Production package is archived after merge.

Production .44 does not change the LastWarAI.com root/install/config payload. Public transport cutover is a later separately gated release.


## Durability-first evidence-ingestion gate
Every candidate that changes account ingestion/persistence must prove:
- task relevance never filters the persistence set for clear supported direct evidence;
- canonical facts, material history, Hot Cache, State Health/freshness and update metadata reconcile coherently;
- verification precedes COMMITTED;
- partial multi-surface failure remains RECOVERY_REQUIRED/incomplete;
- successful evidence survives a fresh runtime without redundant recapture;
- ambiguous observations are not assigned invented labels;
- active-account isolation and sanitized distribution boundaries remain intact;
- standalone fallback preserves equivalent behavior.


## Opt-in modular transport gate
Before any release containing Phase-2 Worker changes:
- actual Worker source is executed under mocked upstreams in CI;
- root/install/config one-response behavior is proven unchanged;
- /modular resolves exactly one live Production SHA and returns only Stage-1 plus same-origin exact-SHA snapshot base;
- /snapshot rejects arbitrary repository browsing, traversal, invalid SHA shapes and disallowed paths before upstream retrieval;
- every manifest module, required and optional, is exposed as a clickable exact-C link on `/modular`;
- `/modular` remains absent from About/sitemap/default install discovery while using `noindex, follow` for user-initiated ChatGPT navigation;
- exact-SHA snapshot responses are immutable and carry auditable commit/path headers;
- invalid live-ref or Stage-1 sanity fails closed;
- /modular remains absent from About/sitemap/default install discovery;
- .45 durability continuity is tested across a fresh runtime;
- a green CI candidate is not sufficient for default cutover: live opt-in deployment and supported-host compatibility evidence are separate gates.
