# Bootstrap Resolution Contract

Transport revision: 2026-08-30.28-hotfix
Engine compatibility: unchanged

## Goal

LWAI must remain centrally maintainable and evergreen without making a fresh ChatGPT session depend on direct GitHub network access. Public installation, live release discovery and trusted engine loading are separated cleanly:

```text
Stage 0 — https://lastwarai.com
  -> Cloudflare resolves live GitHub main server-side
  -> return immutable commit C + https://lastwarai.com/engine/C
Pinned engine transport
  -> Cloudflare fetches BOOTSTRAP_FULL.txt from exact GitHub commit C server-side
  -> return complete sanitized engine to the client
Runtime
  -> continue account discovery/onboarding/recovery and normal LWAI work
```

The user's ChatGPT session needs only LastWarAI.com during installation. GitHub remains the source repository and underlying Production authority, but branch resolution and exact-content retrieval happen server-side.

## Public installer

Preferred instruction:

`Set up Last War optimization using the instructions at https://lastwarai.com`

The root page also supports accidental full-page paste. In either URL mode or pasted-content mode, the assistant continues installation without asking the player to retrieve GitHub JSON, find a SHA, paste another prompt, or restart.

The previously circulated TinyURL remains compatibility-only.

## Server-side live resolution

Underlying authority:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

Cloudflare retrieves the current `commit.sha` server-side. A successful root response supplies:

- `PASTED_CONTENT_MODE: CONTINUE_INSTALL`
- `RESOLUTION_STATUS: LIVE_GITHUB_SERVER_SIDE`
- `RESOLVED_PRODUCTION_COMMIT: C`
- `ENGINE_URL: https://lastwarai.com/engine/C`

C must be exactly 40 lowercase hexadecimal characters. The client validates the format and fetches ENGINE_URL from LastWarAI.com. It must not be required to call GitHub directly during installation.

If Cloudflare cannot establish a valid live SHA, root fails closed with HTTP 503 and a plain-language retry instruction. Never invent or substitute a commit.

## Same-domain immutable engine transport

`GET /engine/C` accepts only a valid 40-hex SHA and fetches `engine/BOOTSTRAP_FULL.txt` from exact GitHub commit C server-side. Before returning it, the Worker sanity-checks the expected complete-engine header plus `SANITIZED: YES` and `ACCOUNT STATE INCLUDED: NO`.

The response contains a short first-party handoff declaring that Stage-0 live resolution is complete for this startup and that C is `production_commit_sha`, followed by the complete sanitized engine. The response includes `X-LWAI-Commit: C` and an immutable cache policy. No user/account state is ever proxied or stored.

## Trust model

GitHub main remains underlying Production authority. LastWarAI.com is first-party live-resolution and transport infrastructure. Exact-SHA repository content remains immutable. Search results, cached README pages, mutable raw main, URL shorteners, redirects and model memory are not substitutes for C.

The first-party transport exists to remove host-specific GitHub accessibility from the end-user critical path, not to weaken pinning.

## Runtime/update compatibility

Existing runtime resolver/update behavior remains compatible. A Stage-0 handoff may satisfy the initial live-resolution requirement for that startup, so the engine must not redundantly block initial onboarding by immediately repeating the same GitHub branch lookup. Existing deployments still retain last-known-good ENGINE and LOCAL STATE on later resolver failures.

A later dedicated simplification release may make the same first-party transport the preferred runtime-update transport as well; that is not required to correct the fresh-install failure.

## State safety

Installer/resolver/transport changes never alter LOCAL STATE except through a separately validated workspace-schema migration. Transport failure cannot trigger account recreation, re-onboarding, deletion or migration guessing.
