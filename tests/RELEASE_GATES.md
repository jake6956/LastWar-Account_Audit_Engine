# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required files exist, including thin loader, module graph, complete fallback, account-registry contract/schema, mandatory account module, mandatory guidance module, and guided-lifecycle contract;
- thin loader contains required modular runtime, migration-first account discovery/privacy, active-account routing, guidance/batch and fallback behavior;
- full fallback contains the complete standalone runtime including current multi-account and guided lifecycle behavior;
- release manifest, module manifest, loader and full fallback versions match;
- manifests assert `sanitized=true` and `account_state_included=false`;
- module graph dependencies resolve and every required module exists, self-identifies, and carries sanitization headers;
- `core.accounts` and `core.guidance` are mandatory in current Production;
- `core.guidance` depends on `core.operating`, `core.persistence`, and `core.accounts`;
- account-registry schema parses as valid JSON and includes optional guidance metadata plus `audit_sessions`;
- README current Production version matches runtime/manifests;
- preferred install URL appears in runtime, README and quick-install documentation;
- generic email/token/private-key patterns are absent.

## Required Prod-Dev pre-promotion checks
These occur in the private proving ground and intentionally may use private knowledge that is never committed here:
- private-identifier denylist scan across the exact RC patch/tree;
- account-specific correction/inventory/power/identity/private Drive ID/path leakage scan;
- current runtime/module graph vs documented contracts completeness diff;
- cloud/provider capability claims match actual connector behavior;
- local-state preservation/migration test;
- legacy state reuse test: supported current facts are imported/reconciled before redundant onboarding;
- legacy single-account -> Workspace Registry migration preserves existing account database unchanged;
- account-isolation test with at least two synthetic account namespaces;
- Audit Session isolation test with at least two synthetic account namespaces;
- noob cold-start acceptance test including optional UID/privacy reassurance and explicit upload guidance;
- experienced-user acceptance test preserving terse free-form updates;
- explicit `done` batch-boundary acceptance test;
- direct screenshot, supported DOCX/PDF bundle, and guided-capture evidence/confidence parity test;
- interrupted guided audit resume test on the same `active_account_id` and pending step;
- reversible archive/restore test preserving immutable `account_id` and history;
- existing-account discovery/migration-first acceptance test before Phase 1;
- one-line remote-install acceptance test;
- short-link redirect integrity check against the canonical raw GitHub loader;
- consequential-spend/regression scenario checks;
- public endpoint readability/integrity check for loader, manifest, `core.guidance`, and full fallback.

## Regression scenarios
1. Shared gear remains transferable within an account rather than hero-owned.
2. Default and specialist presets remain separate.
3. Squad-slot tech is tied to actual deployment slot.
4. Formation left/right is explicit before lateral advice.
5. Stale resource balances/store prices do not drive major recommendations.
6. Research includes prerequisite and opportunity cost.
7. User correction supersedes stale engine assumptions.
8. `refresh engine` preserves Workspace Registry, `active_account_id`, every account-local namespace, Audit Sessions, and guidance metadata.
9. No-cloud deployment still completes onboarding and works.
10. Unsupported provider capabilities are never invented.
11. A web-capable fresh deployment can initialize from `Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x` without asking the user to paste the full engine.
12. The short alias resolves to the canonical raw Production loader.
13. A failed/changed short alias falls back to direct GitHub rather than being treated as source authority.
14. `share LWAI` returns the one-line installer by default while `export yourself` still returns the complete standalone sanitized fallback.
15. User-facing install text does not claim that URL shortening provides true anonymity.
16. UID is requested as optional/private recognition metadata and declining it never blocks account creation or discovery.
17. Identity collection includes a brief, accurate reassurance that identity is for the user's own internal/local account management and is not copied into shared LWAI Production.
18. A fresh install with one existing account confirms that account before resume; multiple plausible accounts are never selected silently.
19. Reload resolves the Workspace Registry and `active_account_id`, not whichever account was most recently mentioned in chat.
20. After switching from Account A to Account B, a terse update can modify only B; A's canonical data and cache remain unchanged.
21. Account switch flushes pending changes/session progress, clears account-scoped working cache, sets `active_account_id`, then loads the target state and only its Audit Sessions.
22. `start over` creates a new clean account and archives the prior registry entry by default rather than deleting it.
23. Cross-account compare mounts source accounts read-only and preserves the prior active account unless the user explicitly switches.
24. A screenname/alliance/server change updates mutable identity on the same immutable `account_id` when continuity is supported.
25. Legacy single-account migration creates/registers an immutable `account_id` and Workspace Registry without forcing re-onboarding or rewriting historical domain records.
26. A storage adapter unable to guarantee independent per-account writes does not claim full multi-account persistence support.
27. Actual consumer UID/screenname/alliance/server/private provider identifiers never appear in public Production artifacts.
28. Prior accessible LWAI state is inspected before broad onboarding; supported current facts are not re-requested.
29. Missing/ambiguous/contradictory/materially stale data is requested in short strategic groups, not a giant form.
30. Every multi-upload request explicitly tells the user to reply `done`; if they declare the batch incomplete, no finalization occurs before `done` or equivalent.
31. A novice receives explicit enough capture instructions to complete the requested step without external documentation.
32. An EXPERT user can still send a terse update such as `Tesla EW19` without forced choreography.
33. Supported DOCX/PDF screenshot bundle ingestion never invents unreadable values and follows the same evidence/confidence rules as direct screenshots.
34. A phone user can complete a long audit via one hero/item/system guided mini-batch at a time.
35. After a validated mini-batch, LWAI persists/reconciles and auto-continues unless pause, consequential choice, ambiguity, tool/upload limit, or completion blocks it.
36. An interrupted guided audit resumes at the persisted current step only after the intended `active_account_id` is resolved.
37. Audit Session state from Account A cannot be resumed or mutated while Account B is active.
38. `restore account` / `unarchive <nickname>` preserves the archived account's immutable `account_id`, database, and history.
39. Guidance may become less verbose with successful usage but never disables privacy, evidence hierarchy, account isolation, or declared batch boundaries.
40. `core.guidance` and `BOOTSTRAP_FULL.txt` are publicly readable and describe migration-first, done-boundary, ingestion, session, and archive-recovery behavior.
