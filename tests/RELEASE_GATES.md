# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required loader, module graph, full fallback, core account/guidance/persistence modules, release runtime module, schemas, current contracts and recovery documentation exist;
- release manifest, module manifest, loader and full fallback versions match;
- manifests assert `sanitized=true` and `account_state_included=false`;
- module graph dependencies resolve and required modules self-identify with sanitization headers;
- `core.persistence`, `core.accounts`, `core.guidance`, `release.runtime` and `release.bootstrap` remain required;
- `core.guidance` depends on operating/persistence/accounts;
- account-registry schema retains optional guidance and Audit Sessions;
- provider-neutral workspace schema defines Runtime Checkpoints and Runtime Journal;
- thin loader and complete fallback include recovery-first startup, verify-before-replay, `WAITING_USER`, account checkpoint isolation and no hidden-reasoning/full-transcript persistence;
- core.persistence defines checkpoint statuses, append-only journal semantics, idempotency and provider fallbacks;
- release.runtime defines resumable release transactions and last-known-good behavior;
- README current Production version matches runtime/manifests;
- preferred install URL appears in runtime, README and quick-install documentation;
- versioned release metadata exists;
- generic credential/private-key leakage patterns are absent.

## Required private pre-promotion checks
- private-identifier/account/provider-reference denylist scan across exact candidate patch/tree;
- no actual Runtime Checkpoint/Runtime Journal rows or user-specific pending actions in public candidate;
- local-state preservation/migration test;
- module graph/full fallback parity test;
- capability/provider fallback test;
- legacy state reuse and multi-account isolation tests;
- guidance/direct-document-guided ingestion and explicit `done` boundary tests;
- account-scoped Audit Session isolation;
- recovery after context loss following several successful writes does not replay verified writes;
- a persisted `WAITING_USER` upload boundary survives reload and does not finalize early;
- an account-scoped checkpoint cannot resume or mutate while another `active_account_id` is active;
- deleting/losing checkpoint storage cannot delete canonical account facts;
- Runtime Journal remains append-only in normal operation;
- recovery is possible without hidden chain-of-thought/full chat transcript;
- interrupted release before merge leaves last-known-good main unchanged;
- release retry verifies branch/PR/commit/CI/archive state before replay;
- exact-head PR CI succeeds on the final candidate SHA;
- after merge, main CI succeeds and loader/manifest/fallback/modules/release metadata agree;
- public endpoints are readable and one-line installer resolves to canonical Production loader.

## Regression scenarios
1. Shared gear remains transferable within an account rather than hero-owned.
2. Default and specialist presets remain separate.
3. Squad-slot tech stays tied to actual deployment slot.
4. Formation left/right is explicit before lateral advice.
5. Stale volatile values do not drive consequential recommendations.
6. Research includes prerequisite/opportunity cost.
7. User corrections supersede stale engine assumptions.
8. Engine refresh preserves Workspace Registry, `active_account_id`, every account-local namespace, Audit Sessions, Runtime Checkpoints and Runtime Journal.
9. No-cloud deployment still functions and does not claim durable checkpointing.
10. Unsupported provider capabilities are never invented.
11. One-line install reaches canonical loader.
12. TinyURL remains transport convenience rather than authority.
13. UID remains optional/private and declining it never blocks account creation.
14. Existing state is discovered before redundant onboarding.
15. Reload resolves `active_account_id`, not chat recency.
16. Terse updates cannot cross account boundaries.
17. `start over` archives by default rather than deleting history.
18. Cross-account compare is read-only.
19. Archive/restore preserves immutable `account_id` and history.
20. Every multi-upload request defines and respects a `done` boundary.
21. Direct screenshot, supported document bundle and guided capture preserve the same evidence/confidence rules.
22. Audit Session state cannot cross `active_account_id`.
23. Context loss after several verified successful writes does not replay those writes.
24. A `WAITING_USER` `done` boundary survives reload.
25. Account A checkpoint cannot silently resume while Account B is active.
26. Runtime Checkpoints are operational metadata, not canonical account truth.
27. Checkpoint-store loss degrades recovery convenience but does not destroy canonical facts.
28. Runtime Journal is append-only in normal operation.
29. Checkpoint content excludes hidden chain-of-thought, raw internal reasoning, full transcripts and duplicate evidence blobs.
30. Structured providers use workspace-level checkpoint/journal stores; file-only providers have an append-only equivalent; read-only providers do not claim durable recovery.
31. Engine release retry verifies actual branch/PR/commit/CI state before repeating writes.
32. Failed/interrupted pre-merge release preserves last-known-good main.
33. Post-merge secondary mirror/archive failure does not silently rewrite a validated healthy main.
34. BOOTSTRAP_FULL carries the same recovery-first semantics as modular Production.
35. Actual consumer checkpoint/journal rows, account identities, provider-local IDs/paths and user-specific pending actions never appear in public Production.
