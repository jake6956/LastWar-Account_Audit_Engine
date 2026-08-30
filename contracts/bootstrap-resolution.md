# Bootstrap Resolution Contract

Version: 2026-08-30.24

## Goal

LWAI must remain centrally maintainable and evergreen without trusting a mutable web-cache snapshot. Installation and updates therefore use three layers:

```text
Stage 0 — one-line installer in the user's message
  -> resolve live GitHub main commit SHA
Stage 1 — engine/BOOTSTRAP.txt at that exact SHA
  -> validate pinned release metadata + module graph
Stage 2 — mandatory/on-demand modules at the same SHA
  -> runtime behavior
```

Stage 0 contains only the minimum instructions needed to escape search/index caching. Stage 1 contains orchestration only. Account onboarding, provider guidance, optimization logic and season/domain behavior belong to modules. `BOOTSTRAP_FULL.txt` is the complete emergency fallback and is not the normal load path.

## Public installer

`Set up Last War optimization. Open https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main directly, use its current commit SHA, then retrieve and follow engine/BOOTSTRAP.txt from that exact SHA. Never use search-index/cached main copies; if live SHA resolution fails, stop rather than guessing.`

The user's message itself is the Stage-0 bootloader. There is no URL-shortener, README or mutable raw-file hop before live ref resolution.

## Live ref resolution

Canonical live-ref endpoint:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

Resolve `commit.sha` using a genuinely live GitHub connector/API or live git transport. A valid SHA is exactly 40 lowercase hex characters. Search results, indexed GitHub HTML, README snapshots, raw `main` bodies, aliases and model memory are not current-version authority.

If fresh installation cannot establish a live SHA, fail closed rather than silently installing an older cached engine. Existing compatible deployments keep last-known-good ENGINE and LOCAL STATE.

## Pin once

After resolving `production_commit_sha = C`, every candidate read in that transaction uses C: LATEST, MANIFEST, MIGRATIONS, BOOTSTRAP, required modules and fallback. Never mix revisions. Exact-SHA content is immutable, so cached exact-SHA content is safe.

## Cascading maintenance

`release.resolver` is mandatory core and owns the live-ref algorithm. `release.updater` must call it for startup/reload/TTL/manual freshness checks. `release.bootstrap` delegates account/provider UX to core modules. This gives a single base-layer fix path: resolver/bootstrap changes propagate to every current deployment after the next successful resolver transaction.

## Loader budget

The previous 9 KiB loader ceiling was an internal CI guard, not a ChatGPT limit. Production now enforces a 4 KiB Stage-1 budget to prevent policy/domain leakage. Raising the budget is not an acceptable fix for loader bloat.

## State safety

Resolution and engine replacement never alter LOCAL STATE except through a separately validated workspace-schema migration. Resolver failure cannot trigger account recreation, re-onboarding, deletion or migration guessing.
