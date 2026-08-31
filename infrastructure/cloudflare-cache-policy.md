# LastWarAI.com Cloudflare Cache Contract

Status: required Production deployment contract  
Applies to: the default Worker entrypoint serving `/`, `/install`, and `/config.txt`

## Invariant

The mutable LastWarAI.com configuration entrypoint is a gateway/router. It must execute for every request so it can resolve the current GitHub Production `main` SHA before selecting exact immutable engine content.

**Cloudflare Workers Caching for the default entrypoint must be disabled (`cache.enabled = false`).** Response-level `Cache-Control: no-store` remains defense in depth, but it is not a substitute for disabling a cache that can sit in front of Worker execution.

The Worker may continue caching exact-SHA GitHub `BOOTSTRAP_FULL.txt` subrequests aggressively. A URL addressed by a validated immutable Git commit SHA is safe to cache.

## Required live deployment state

- default Worker entrypoint: Workers Caching disabled;
- mutable root/config/install responses: `Cache-Control: no-store, no-cache, must-revalidate, max-age=0` plus CDN/Surrogate no-store headers;
- live GitHub branch-ref subrequest: uncached;
- exact-SHA engine source subrequest: immutable long-lived cache permitted;
- `/engine/<SHA>` compatibility response: immutable long-lived cache permitted.

## One-time migration from a cached deployment

Disabling Workers Caching prevents future lookup/population but does not evict already cached Worker responses. After the setting is disabled and redeployed, perform one final purge of any existing cached mutable LastWarAI.com root/config/install response.

This purge is a migration action, not a per-release requirement.

## Release verification

After every Production merge:

1. resolve canonical GitHub `main` SHA;
2. request LastWarAI.com root and `/config.txt` immediately;
3. require both to return the same `X-LWAI-Commit` as GitHub `main` and identical configuration bodies;
4. fail the release checkpoint if the public edge serves a prior SHA;
5. never accept a stale public body as eventual consistency.

Normal engine/gameplay releases must not require Worker source edits, dashboard cache purges, or cache-rule changes.

## Source-control boundary

`infrastructure/cloudflare-worker.js` contains transport/provenance/discovery behavior only. It must not absorb Last War gameplay logic, provider onboarding, account strategy, schema-specific user behavior, or current engine-version literals. Those belong to the centrally versioned engine/modules.

If the live Cloudflare account differs from this contract, the live deployment must be corrected before OO-009 can be marked Production.