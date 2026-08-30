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

## Remote-bootstrap trust boundary
The preferred human-facing installer is the first-party `https://lastwarai.com` endpoint. It serves only a small sanitized Stage-0 locator. The public domain is **not** current-version authority.

Current Production is established by resolving live GitHub `main` at `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`, obtaining its current `commit.sha`, and pinning trusted engine reads to that exact immutable commit.

The previously circulated `https://tinyurl.com/2yxf7f5x` is legacy compatibility only. A third-party shortener, redirect/interstitial, search result, cached README, mutable raw `main` body or model memory is never an independent trust root.

The first-party domain keeps the normal public instruction short without pretending the source is anonymous. Resolving the locator exposes public GitHub provenance; do not falsify authorship/provenance.

If public transport fails, do not guess current Production and never repair installer uncertainty by changing LOCAL STATE. Existing compatible deployments retain last-known-good ENGINE/LOCAL STATE when live Production cannot be safely resolved.

If private data is accidentally committed, stop release promotion, remove/rotate affected secrets where applicable, repair history if necessary and re-run sanitization gates before Production resumes.
