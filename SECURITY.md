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
The preferred human-facing installer uses `https://tinyurl.com/2yxf7f5x` to reduce visible source/maintainer exposure and make mobile installation practical. A URL shortener is **not** an independent trust root. Canonical authority remains GitHub Production `main`, specifically `releases/LATEST.json` and `engine/BOOTSTRAP.txt`.

A deployment should not silently execute content if the known short alias resolves to an unexpected destination or the fetched document does not self-identify as sanitized LWAI Production with account state excluded. Fall back to the direct canonical GitHub source or report the integrity mismatch.

The short URL provides only semi-anonymous presentation: the repository owner is absent from the visible install line, but resolving the URL exposes public provenance. Do not describe this as true anonymity and do not falsify authorship/provenance.

If private data is accidentally committed, stop release promotion, remove/rotate affected secrets where applicable, repair history if necessary and re-run sanitization gates before Production resumes.
