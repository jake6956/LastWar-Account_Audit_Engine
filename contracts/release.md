# Release Engineering Contract

Version: 2026-08-29.5

## Channels
- **Prod-Dev:** private live development/proving ground using real account data.
- **Release Candidate:** sanitized frozen candidate for validation.
- **Production:** sanitized public engine for mass consumption.

## Promotion path
`Prod-Dev validation -> sanitized source update -> frozen RC -> release gates -> Production archive -> stable public LATEST mirror`

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
10. Stable endpoint: consumer LATEST remains the stable distribution URL.

If any gate fails, Production remains at the previous known-good build.

## Versioning
Use `YYYY-MM-DD.N`. Increment N for each production-ready revision that day. RC uses intended Production version. Experimental Prod-Dev changes need no public version until promotion.

## Rollback
Restore a known-good versioned Production artifact to the same stable consumer endpoint. Never require consumers to adopt a new link for routine releases.

## Schema changes
Prefer backward compatibility. Breaking schema changes require migration instructions plus local-state preservation tests before promotion.
