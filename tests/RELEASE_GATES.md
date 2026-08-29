# LWAI Release Gates

Every public promotion is fail-closed.

## Automated public-repo checks
- required files exist;
- bootstrap contains required runtime sections including remote bootstrap / one-line install;
- manifest version matches bootstrap version;
- manifest asserts `sanitized=true` and `account_state_included=false`;
- manifest declares the preferred install URL;
- README current Production version matches bootstrap/manifest;
- preferred install URL appears in bootstrap, README and quick-install documentation;
- generic email/token/private-key patterns are absent.

## Required Prod-Dev pre-promotion checks
These occur in the private proving ground and intentionally may use private knowledge that is never committed here:
- private-identifier denylist scan;
- account-specific correction/inventory/power leakage scan;
- current bootstrap vs documented contracts completeness diff;
- cloud/provider capability claims match actual connector behavior;
- local-state preservation/migration test;
- noob cold-start acceptance test;
- one-line remote-install acceptance test;
- short-link redirect integrity check against the canonical raw GitHub bootstrap;
- consequential-spend/regression scenario checks;
- public endpoint readability/integrity check.

## Regression scenarios
1. Shared gear remains transferable rather than hero-owned.
2. Default and specialist presets remain separate.
3. Squad-slot tech is tied to actual deployment slot.
4. Formation left/right is explicit before lateral advice.
5. Stale resource balances/store prices do not drive major recommendations.
6. Research includes prerequisite and opportunity cost.
7. User correction supersedes stale engine assumptions.
8. `refresh engine` preserves local state.
9. No-cloud deployment still completes onboarding and works.
10. Unsupported provider capabilities are never invented.
11. A web-capable fresh deployment can initialize from `Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x` without asking the user to paste the full engine.
12. The short alias resolves to the canonical raw Production bootstrap.
13. A failed/changed short alias falls back to direct GitHub rather than being treated as source authority.
14. `share LWAI` returns the one-line installer by default while `export yourself` still returns the full standalone sanitized engine.
15. User-facing install text does not claim that URL shortening provides true anonymity.
