# Contributing to LWAI

LWAI changes are documentation-as-code changes. A behavior change is incomplete until its runtime source, relevant contract/schema, tests and release metadata agree.

## Change workflow
1. Develop/test against a private Prod-Dev deployment.
2. Separate generic engine improvement from account-specific observations.
3. Update relevant source/contracts/schemas/tests.
4. Sanitize.
5. Freeze an RC.
6. Run automated and private pre-promotion gates.
7. Promote only if every applicable gate passes.
8. Update versioned Production metadata and stable distribution mirror.

## Design rules
- Prefer direct evidence over inference.
- Preserve local state across engine upgrades.
- Capability-detect external services rather than assuming features.
- Fail closed on release uncertainty; do not break last known-good Production.
- Avoid adding complexity to the consumer interface unless it improves actual decisions.
- Keep the bootstrap self-contained even when source is modular.
