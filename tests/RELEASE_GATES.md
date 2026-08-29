# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required files exist, including thin loader, module graph, complete fallback, account-registry contract/schema and mandatory account module;
- thin loader contains required modular runtime, account-discovery/privacy, active-account routing and fallback behavior;
- full fallback contains the complete standalone runtime including current multi-account behavior;
- release manifest, module manifest, loader and full fallback versions match;
- manifests assert `sanitized=true` and `account_state_included=false`;
- module graph dependencies resolve and every required module exists, self-identifies, and carries sanitization headers;
- `core.accounts` is mandatory in multi-account Production;
- account-registry schema parses as valid JSON;
- README current Production version matches runtime/manifests;
- preferred install URL appears in runtime, README and quick-install documentation;
- generic email/token/private-key patterns are absent.

## Required Prod-Dev pre-promotion checks
These occur in the private proving ground and intentionally may use private knowledge that is never committed here:
- private-identifier denylist scan across the exact RC patch/tree;
- account-specific correction/inventory/power/identity leakage scan;
- current runtime/module graph vs documented contracts completeness diff;
- cloud/provider capability claims match actual connector behavior;
- local-state preservation/migration test;
- legacy single-account -> Workspace Registry migration preserves existing account database unchanged;
- account-isolation test with at least two synthetic account namespaces;
- noob cold-start acceptance test including optional UID/privacy reassurance;
- existing-account discovery acceptance test before Phase 1;
- one-line remote-install acceptance test;
- short-link redirect integrity check against the canonical raw GitHub loader;
- consequential-spend/regression scenario checks;
- public endpoint readability/integrity check.

## Regression scenarios
1. Shared gear remains transferable within an account rather than hero-owned.
2. Default and specialist presets remain separate.
3. Squad-slot tech is tied to actual deployment slot.
4. Formation left/right is explicit before lateral advice.
5. Stale resource balances/store prices do not drive major recommendations.
6. Research includes prerequisite and opportunity cost.
7. User correction supersedes stale engine assumptions.
8. `refresh engine` preserves Workspace Registry, `active_account_id`, and every account-local namespace.
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
21. Account switch flushes pending changes, clears account-scoped working cache, sets `active_account_id`, then loads the target state.
22. `start over` creates a new clean account and archives the prior registry entry by default rather than deleting it.
23. Cross-account compare mounts source accounts read-only and preserves the prior active account unless the user explicitly switches.
24. A screenname/alliance/server change updates mutable identity on the same immutable `account_id` when continuity is supported.
25. Legacy single-account migration creates/registers an immutable `account_id` and Workspace Registry without forcing re-onboarding or rewriting historical domain records.
26. A storage adapter unable to guarantee independent per-account writes does not claim full multi-account persistence support.
27. Actual consumer UID/screenname/alliance/server/private provider identifiers never appear in public Production artifacts.
