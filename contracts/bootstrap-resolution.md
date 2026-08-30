# Bootstrap Resolution Contract

Transport revision: 2026-08-30.28-hotfix
Engine compatibility: unchanged

## Goal

LWAI must remain centrally maintainable and evergreen without making a fresh ChatGPT session depend on direct access to GitHub's branch API. Public installation, live release discovery and trusted engine loading are separate layers:

```text
Stage 0 — permanent first-party installer at https://lastwarai.com
  -> server-side fetch live GitHub main
  -> return resolved immutable commit SHA + exact bootstrap URL
Stage 1 — engine/BOOTSTRAP.txt at that exact SHA
  -> validate pinned release metadata + module graph
Stage 2 — mandatory/on-demand modules at the same SHA
  -> runtime behavior
```

Stage 0 is deliberately tiny. Stage 1 contains orchestration only. Account onboarding, provider guidance, optimization logic and season/domain behavior belong to modules. `BOOTSTRAP_FULL.txt` is the complete emergency fallback and is not the normal load path.

## Public installer

Preferred public instruction:

`Set up Last War optimization using the instructions at https://lastwarai.com`

`https://lastwarai.com` is first-party discovery/live-resolution transport. It does not contain private state and does not replace GitHub as the underlying Production source.

The previously circulated `https://tinyurl.com/2yxf7f5x` remains a legacy compatibility alias only.

## Server-side live ref resolution

Underlying canonical current-version endpoint:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

The LastWarAI.com Worker retrieves this endpoint server-side for each successful install request. A successful Stage-0 response supplies:

- `RESOLUTION_STATUS: LIVE_GITHUB`
- `RESOLVED_PRODUCTION_COMMIT: C`, where C is exactly 40 lowercase hex characters
- `EXACT_BOOTSTRAP_URL`, whose path embeds the same C
- `LIVE_REF_SOURCE`, identifying the GitHub main branch endpoint

The client validates those fields and loads the exact bootstrap directly. **A fresh client must not be required to call GitHub's branch API again before starting.** This removes a host/browser/network capability from the critical installation path while preserving immutable commit pinning.

If the first-party server-side resolver itself cannot establish a valid live SHA, it returns HTTP 503 rather than fabricating or guessing a commit. Existing compatible deployments retain their normal last-known-good ENGINE behavior.

## Direct resolver compatibility

Stage 1 and `release.resolver` retain direct live-GitHub resolution for updater/reload/freshness operations when the host genuinely has that capability. They may also accept a valid `RESOLVED_PRODUCTION_COMMIT` handed off by Stage 0. Both paths converge on the same immutable-commit validation rules.

Search results, indexed GitHub HTML, README snapshots, mutable raw `main` bodies, aliases, redirects and model memory are never valid substitutes for a resolved SHA.

## Pin once

After establishing `production_commit_sha = C`, every candidate read in that transaction uses C: LATEST, MANIFEST, MIGRATIONS, BOOTSTRAP, required modules and fallback. Never mix revisions. Exact-SHA content is immutable, so cached exact-SHA content is safe.

## Cascading maintenance

`release.resolver` remains mandatory core and owns runtime freshness. `release.updater` calls it for startup/reload/TTL/manual checks. Stage 0 only removes direct branch-ref discovery from the initial client-side install path; it does not absorb account/provider/domain behavior.

The preferred public installer remains the stable first-party domain, so future internal GitHub/release implementation may evolve without changing the one-line public prompt.

## Loader budget

Production keeps the 4 KiB Stage-1 budget. Moving live-ref discovery server-side is specifically intended to keep Stage 1 simple rather than adding more client orchestration.

## State safety

Resolution, installer-transport changes and engine replacement never alter LOCAL STATE except through a separately validated workspace-schema migration. Resolver failure cannot trigger account recreation, re-onboarding, deletion or migration guessing.
