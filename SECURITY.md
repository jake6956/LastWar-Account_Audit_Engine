# Security / Privacy Boundary

LWAI Production is intentionally sanitized.

Do not commit:
- player names or identifiers tied to private state;
- alliance/server-specific private information;
- screenshots containing account data;
- resource balances, powers, current account targets or battle history;
- private cloud IDs/URLs;
- OAuth tokens, API keys, cookies or credentials;
- private Corrections or provider paths.

Public Production may contain only generic engine logic, schemas, adapters, tests, release metadata and intentionally public distribution/Gold Asset endpoints.

If private data is accidentally committed, stop release promotion, remove/rotate affected secrets where applicable, repair history if necessary and re-run sanitization gates before Production resumes.
