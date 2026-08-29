# Release Engineering Contract

Contract revision: 2026-08-29.7

## Channels
- **Prod-Dev:** private live development/proving ground using real account data.
- **Release Candidate:** sanitized frozen candidate for validation.
- **Production:** sanitized public engine for mass consumption on GitHub `main`.

## Production branch invariant
`main` is last-known-good Production. Future candidates must not be written directly to `main` before validation.

## Promotion path
`Private Prod-Dev validation -> sanitized source compile -> GitHub RC branch -> Pull Request -> CI + private release gates -> merge/squash to main -> versioned Production archive -> remote install endpoint/mirror synchronization`

Recommended RC branch name: `rc/<engine-version>`.

## Consumer distribution hierarchy
1. **Preferred human-facing install alias:** https://tinyurl.com/2yxf7f5x
2. **Authoritative raw Production bootstrap:** https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt
3. **Authoritative machine-readable manifest:** https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
4. **Secondary/legacy Google distribution mirror:** stable PUBLIC BOOTSTRAP document when readable.
5. **Manual full bootstrap:** fallback for deployments without remote web retrieval.

The shortener is transport convenience only. GitHub `main` is the source of truth. A short-link failure must not block a deployment that can access the direct raw GitHub source.

## Required gates
1. Sanitization: no private/account-specific identity or state.
2. Bootstrap completeness: all runtime contracts/playbooks/onboarding/fallbacks embedded.
3. Consistency: no contradictions across engine/contracts/schemas.
4. Graceful degradation: no assumption that cloud/web/automation/images/writable sheets exist.
5. Self-healing: source-vs-derived, freshness/confidence, reconciliation and reload present.
6. Noob usability: one bootstrap works from a fresh chat with no prior LWAI knowledge.
7. Regression checks: shared gear, preset separation, squad-slot tech, orientation discipline, volatile refresh, prerequisite-aware research and consequential-spend logic remain intact.
8. Local-state preservation: upstream engine refresh cannot erase deployment-local state.
9. Documentation-as-code: relevant source/docs/tests/version records updated.
10. GitHub RC CI: validation must pass on the RC/PR head.
11. Main protection by process: merge only the exact validated RC head SHA; if the head changes, revalidate before merge.
12. Remote-install integrity: preferred short alias resolves to the canonical raw Production bootstrap and a fresh web-capable assistant can bootstrap without requiring the user to paste the multi-page engine.
13. Distribution parity: after merge, GitHub `LATEST.json`, raw Production bootstrap and any active mirror must agree on engine version/material runtime behavior.

If any pre-merge gate fails, leave `main` untouched and keep the current public Production live. If a post-merge mirror/parity step fails, GitHub `main` remains authoritative and the affected mirror is marked synchronization-degraded until repaired. If only the short alias fails, direct GitHub Production remains the supported install path until the alias is repaired.

## Pull request discipline
- Create the RC branch from current `main`.
- Put all generic Production changes for that release on the RC branch.
- Open a PR to `main` with intended version, migration status and gate checklist.
- Require CI success plus private sanitization/noob/local-state/remote-install checks.
- Merge using the validated expected head SHA; squash is preferred for a compact Production history unless preserving multiple commits materially helps auditability.
- Never use Production PRs to carry private account data.

## Semi-anonymous distribution
The preferred end-user install line should contain only the neutral short URL rather than the maintainer/repository owner handle. This reduces casual source exposure but is not anonymity; users may resolve the URL and inspect public provenance. Do not conceal or falsify provenance if asked.

## Versioning
Use `YYYY-MM-DD.N`. Increment N for each production-ready engine revision on the same date. RC branch/PR uses the intended Production version. Experimental Prod-Dev changes need no public version until promotion.

## Rollback
Restore a known-good versioned Production source/artifact through a new validated rollback RC/PR. Keep stable consumer distribution aliases when possible; never silently rewrite private/local account state during rollback.

## Schema changes
Prefer backward compatibility. Breaking schema changes require migration instructions plus local-state preservation tests before promotion.

## Historical exception
The initial repository/bootstrap import was written directly to `main` while GitHub connectivity and CI were being established. Ordinary Production changes use the RC branch/PR gate above.
