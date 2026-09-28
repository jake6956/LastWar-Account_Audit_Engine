# LastWarAI.com Cloudflare Cache Contract

Status: required Production deployment contract  
Worker service/application: `lwai-bootstrap`  
Primary custom domain: `lastwarai.com`  
Cloudflare control surface: Workers & Pages -> `lwai-bootstrap`  
Applies to: the default Worker entrypoint serving `/`, `/install`, and `/config.txt`, plus the non-default `/modular` experiment and immutable `/snapshot/<SHA>/<runtime-path>` transport

## Recorded topology

`lastwarai.com` is attached directly to the `lwai-bootstrap` Worker as a Custom Domain/application route. The zone-level **Workers Routes** table is intentionally empty and is not the control surface for this deployment. An empty Workers Routes page does not mean the Worker is detached.

The canonical Worker source is `infrastructure/cloudflare-worker.js`. The canonical deploy/cache configuration is `wrangler.jsonc`. Do not ask an operator to rediscover the Worker name or infer it from the zone route table.

Dashboard-managed Custom Domain routing is intentionally preserved by omitting `route`/`routes` from Wrangler. Because Wrangler otherwise defaults to publishing the Worker on `workers.dev`, the canonical config must explicitly set `workers_dev = false` and `preview_urls = false`. Production should be exposed through the recorded custom domain, not an accidental public `*.workers.dev` alias or version-preview endpoint.

## Invariant

The mutable LastWarAI.com configuration entrypoint is a gateway/router. It must execute for every request so it can resolve the current GitHub Production `main` SHA before selecting exact immutable engine content.

**Cloudflare Workers Caching for the default entrypoint must be disabled (`cache.enabled = false`).** Response-level `Cache-Control: no-store` remains defense in depth, but it is not a substitute for disabling a cache that can sit in front of Worker execution.

The Worker may continue caching exact-SHA GitHub `BOOTSTRAP_FULL.txt` subrequests aggressively. A URL addressed by a validated immutable Git commit SHA is safe to cache.

## Required live deployment state

- Worker service: `lwai-bootstrap`;
- custom domain: `lastwarai.com`;
- dashboard-managed Custom Domain retained; zone Workers Routes may remain empty;
- `workers.dev` production alias disabled (`workers_dev = false`);
- Worker Preview URLs disabled (`preview_urls = false`);
- default Worker entrypoint: Workers Caching disabled;
- `wrangler.jsonc`: `name = lwai-bootstrap`, `main = infrastructure/cloudflare-worker.js`, `workers_dev = false`, `preview_urls = false`, `cache.enabled = false`;
- mutable root/config/install responses: `Cache-Control: no-store, no-cache, must-revalidate, max-age=0` plus CDN/Surrogate no-store headers;
- live GitHub branch-ref subrequest: uncached;
- exact-SHA engine source subrequest: immutable long-lived cache permitted;
- `/engine/<SHA>` compatibility response: immutable long-lived cache permitted.


## Phase-2 opt-in modular transport

Production .46 may add a non-default `/modular` endpoint and immutable `/snapshot/<SHA>/<runtime-path>` exact-commit proxy without changing the supported default installer.

- `/modular` is mutable and MUST use the same no-store/no-cache posture as root/config because it resolves live GitHub Production server-side on each request.
- `/modular` MUST be `noindex, follow`: absent from default About/sitemap/public install discovery, but allowed to expose exact-C links that ChatGPT may follow after the user explicitly supplies the modular URL.
- `/snapshot/<SHA>/<runtime-path>` is immutable only after validating a 40-lowercase-hex SHA and a strict runtime-file allowlist. Exact-SHA snapshot responses may use one-year immutable caching.
- `/modular` MUST generate its resource index from exact-C LATEST + MANIFEST and link all manifest modules plus required release/schema/fallback artifacts; linked resources remain exact-SHA snapshot URLs.
- Snapshot transport MUST NOT expose arbitrary repository browsing and MUST reject traversal, dot segments, backslashes/nulls and disallowed paths before raw retrieval.
- Snapshot responses MUST carry the exact requested commit and path in response headers so host-side pin/no-mix checks can be audited.
- The root/install/config path continues serving BOOTSTRAP_FULL in one response until a later separately gated cutover release.

## One-time migration from a cached deployment

Disabling Workers Caching prevents future lookup/population but does not evict already cached Worker responses. After the `lwai-bootstrap` setting is disabled and the Worker version is redeployed, perform one final purge of any existing cached mutable LastWarAI.com root/config/install response.

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

`wrangler.jsonc` is deployment configuration, not gameplay behavior. Keep the worker identity, custom-domain routing posture, and cache contract there; do not add provider/account/optimization policy.

If the live Cloudflare account differs from this contract, the live deployment must be corrected before OO-009 can be marked Production.
