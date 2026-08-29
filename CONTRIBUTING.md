# Contributing to LWAI

LWAI changes are documentation-as-code changes. A behavior change is incomplete until its runtime source, relevant contract/schema, tests and release metadata agree.

## Change workflow
1. Develop/test against a private Prod-Dev deployment.
2. Separate generic engine improvement from account-specific observations.
3. Update relevant source/contracts/schemas/tests/build inputs.
4. Sanitize and assign the intended Production version.
5. Create a GitHub RC branch from current `main`, conventionally `rc/<engine-version>`.
6. Put the complete sanitized candidate on that branch and open a PR to `main`.
7. Run GitHub CI plus private pre-promotion gates: account-specific leakage denylist, noob cold start, provider/capability checks, migration/local-state preservation, regression scenarios and docs-as-code consistency.
8. Merge only the exact validated PR head SHA after all gates pass; if the head changes, revalidate.
9. Update versioned Production metadata/archive and synchronize the stable Google distribution mirror.
10. Verify parity among GitHub `LATEST.json`, raw `engine/BOOTSTRAP.txt` and the Google mirror.

`main` is last-known-good Production. Failed candidates stay on their RC branch/PR and do not replace `main`.

## Design rules
- Prefer direct evidence over inference.
- Preserve local state across engine upgrades.
- Capability-detect external services rather than assuming features.
- Fail closed on release uncertainty; do not break last-known-good Production.
- Never commit private player/runtime state to this repository.
- Avoid adding complexity to the consumer interface unless it improves actual decisions.
- Keep the bootstrap self-contained even when source is modular.
