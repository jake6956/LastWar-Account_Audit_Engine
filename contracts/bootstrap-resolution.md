# Bootstrap Resolution Contract

Transport revision: 2026-09-28.46-optin-modular
Engine compatibility: unchanged

## Goal

LWAI must remain centrally maintainable and evergreen without making a fresh AI session depend on direct GitHub network access or a multi-hop remote instruction chain. Public installation, trusted Production resolution, and complete configuration delivery are separated cleanly:

```text
Stage 0 — https://lastwarai.com
  -> Cloudflare resolves live GitHub main server-side
  -> Cloudflare retrieves BOOTSTRAP_FULL.txt from exact commit C
  -> Cloudflare adapts only the generic Stage-0 discovery section
  -> the same HTTP response returns the complete sanitized configuration
Runtime
  -> normal LWAI account guidance, persistence, recovery and optimization behavior
```

The user's AI needs only LastWarAI.com during initial installation. GitHub remains the source repository and underlying Production authority, but branch resolution and exact-content retrieval happen server-side.

## Public installer

Preferred instruction:

`Set up Last War optimization using the instructions at https://lastwarai.com`

The sentence remains stable across releases. The user is not expected to retrieve GitHub JSON, find a SHA, paste another URL, upload BOOTSTRAP.txt, or perform other technical setup.

Deprecated URL shorteners are unsupported. The supported public installer is LastWarAI.com.

## Server-side live resolution

Underlying authority:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

Cloudflare retrieves the current `commit.sha` server-side. C must be exactly 40 lowercase hexadecimal characters. Cloudflare then retrieves `engine/BOOTSTRAP_FULL.txt` from that exact immutable commit and sanity-checks the expected complete-engine marker plus `SANITIZED: YES` and `ACCOUNT STATE INCLUDED: NO`.

If Cloudflare cannot establish a valid live SHA or retrieve/validate the exact engine, the root fails closed with HTTP 503. Never invent or substitute a commit.

## Single-response public configuration

A successful root response is UTF-8 `text/plain`, includes `X-LWAI-Commit: C`, and contains:

- transparent product purpose and public provenance;
- explicit sanitized/no-account-state declarations;
- explicit credential and cloud-workspace privacy boundaries;
- an explicit statement that the configuration does not override the host AI platform's system, developer, security, privacy or safety requirements;
- permission for independent source/provenance verification when the host supports it;
- the complete sanitized LWAI engine from exact commit C.

The public wrapper must not require a second engine URL fetch and must not contain anti-verification language such as instructions to avoid checking the public source. It is a configuration delivery document, not a chain of instructions embedded in an unrelated webpage.

## First-party Stage-0 adaptation

`engine/BOOTSTRAP_FULL.txt` intentionally retains the generic direct-source Stage-0 resolver because it is also the standalone/manual recovery artifact. When LastWarAI.com has already resolved C, the Worker replaces only the Stage-0 discovery section with a transparent statement that this copy was delivered after server-side Production resolution and that the resolved commit may be independently verified.

No account, persistence, gameplay, evidence, continuity, update, or optimization policy is rewritten by the Worker.

## Phase-2 opt-in modular transport

Production .46 may expose a non-default `/modular` endpoint for compatibility testing while leaving `/`, `/install` and `/config.txt` unchanged.

The opt-in Worker resolves live Production C server-side, retrieves exact-C `engine/BOOTSTRAP.txt`, and returns Stage-1 plus:
- `RESOLVED_PRODUCTION_COMMIT: C`;
- `FIRST_PARTY_SNAPSHOT_BASE: https://lastwarai.com/snapshot/C/`.

Stage-1 candidate reads may then use the exact-C same-origin snapshot base instead of direct GitHub/raw retrieval. The snapshot path accepts only a strict runtime allowlist and carries the requested commit/path in response headers. It never resolves mutable main and is immutable/cacheable because C is explicit.

The opt-in endpoint is `noindex, nofollow`, is absent from About/sitemap/default install instructions, and is not authorization for default cutover. Failure preserves LOCAL STATE and falls back through normal last-known-good/default installer behavior; never splice snapshot files from different SHAs or mix snapshot bytes with a different network candidate.

Default cutover remains a later separately gated release after live deployment and fresh-host compatibility evidence, including durable account load -> multi-fact evidence commit -> fresh runtime recovery.

## Compatibility endpoint

`GET /engine/C` remains available for compatibility with the previous same-domain engine-proxy transport. It accepts only a valid 40-hex SHA, fetches `engine/BOOTSTRAP_FULL.txt` from exact GitHub commit C, applies the same Stage-0 delivery adaptation, returns `X-LWAI-Commit: C`, and uses immutable caching.

New installations do not require this second request.

## robots.txt / discoverability

`GET /robots.txt` explicitly allows:

- `OAI-SearchBot`
- `ChatGPT-User`
- general crawlers (`User-agent: *`)

This does not weaken application-level privacy or authorization boundaries; it only permits retrieval of the public sanitized configuration.

## Pin once

Pin once to immutable commit C for each startup/update transaction. Never mix release metadata, manifest, migration graph, modules, or fallback content from different commits.

## Stage 1 compatibility and 4 KiB budget

`engine/BOOTSTRAP.txt` remains the small orchestration-only Stage-1 loader for direct GitHub/modular operation and recovery paths. The complete first-party root response is an installation transport optimization, not permission to move provider, account, gameplay, or onboarding policy into the loader.

Production keeps the existing 4 KiB Stage-1 budget.

## Trust model

GitHub main remains underlying Production authority. LastWarAI.com is first-party delivery infrastructure. Exact-SHA repository content remains immutable. Search results, cached README pages, mutable raw main, URL shorteners, redirects and model memory are not substitutes for C.

The first-party transport exists to remove host-specific GitHub accessibility from the end-user critical path, not to weaken pinning or verification.

## Recovery-package compatibility

Production .44 introduces a deterministic sanitized multi-file recovery package without changing the public Stage-0 response. A validated package carries exact Stage-1, LATEST, MANIFEST, MIGRATIONS, every manifest module, runtime schemas/contracts/assets, RECOVERY_MANIFEST and SHA256SUMS.

When live ref resolution is unavailable, explicit manual/offline recovery may use the package `source_commit_sha` as one fixed snapshot C. This does not establish newest live Production. Package recovery sets degraded/recovery-snapshot freshness, reads the entire transaction from package bytes, preserves LOCAL STATE, and runs the canonical live resolver when network capability returns. Package and network candidate bytes must never be mixed in one transaction.

During .44 the package may include BOOTSTRAP_FULL as a compatibility file, but validation must also prove the modular package is structurally complete without it. LastWarAI.com root/install/config continues to serve the existing complete single-response BOOTSTRAP_FULL transport in this release.

## Runtime/update compatibility

Existing runtime resolver/update behavior remains compatible. Existing deployments retain last-known-good ENGINE and LOCAL STATE on later resolver failures. `refresh engine` continues to use the canonical resolver/update transaction.

A later simplification release may route runtime update checks through LastWarAI.com as well; that is separate from this installation transport hotfix.

## State safety

Installer/resolver/transport changes never alter LOCAL STATE except through a separately validated workspace-schema migration. Transport failure cannot trigger account recreation, re-onboarding, deletion or migration guessing.
