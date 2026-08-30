# Bootstrap Resolution Contract

Version: 2026-08-30.25

## Goal

LWAI must remain centrally maintainable and evergreen without trusting a mutable web-cache snapshot. Public installation, release discovery and trusted engine loading are separate layers:

```text
Stage 0 — permanent first-party installer at https://lastwarai.com
  -> serve tiny locator text
  -> resolve live GitHub main commit SHA
Stage 1 — engine/BOOTSTRAP.txt at that exact SHA
  -> validate pinned release metadata + module graph
Stage 2 — mandatory/on-demand modules at the same SHA
  -> runtime behavior
```

Stage 0 is deliberately tiny. Stage 1 contains orchestration only. Account onboarding, provider guidance, optimization logic and season/domain behavior belong to modules. `BOOTSTRAP_FULL.txt` is the complete emergency fallback and is not the normal load path.

## Public installer

Preferred public instruction:

`Set up Last War optimization using the instructions at https://lastwarai.com`

`https://lastwarai.com` is a first-party discovery/transport endpoint. It is not current-version authority and may be reimplemented behind the same domain without changing the installer contract.

The previously circulated `https://tinyurl.com/2yxf7f5x` is a legacy compatibility alias only. It may help an already-distributed prompt reach LWAI, but it is never preferred and never authoritative.

## Live ref resolution

Canonical current-version endpoint:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

Resolve `commit.sha` using a genuinely live GitHub connector/API or live git transport. A valid SHA is exactly 40 lowercase hex characters. Search results, indexed GitHub HTML, README snapshots, raw `main` bodies, aliases, redirects and model memory are not current-version authority.

If fresh installation cannot establish a live SHA, fail closed rather than silently installing an older cached engine. Existing compatible deployments keep last-known-good ENGINE and LOCAL STATE.

## Pin once

After resolving `production_commit_sha = C`, every candidate read in that transaction uses C: LATEST, MANIFEST, MIGRATIONS, BOOTSTRAP, required modules and fallback. Never mix revisions. Exact-SHA content is immutable, so cached exact-SHA content is safe.

If the initial Stage-0/bootstrap text arrived through mutable public transport, it may only direct the resolver. Trusted Stage-1 and release identity are re-read from exact C.

## Cascading maintenance

`release.resolver` is mandatory core and owns the live-ref algorithm. `release.updater` must call it for startup/reload/TTL/manual freshness checks. `release.bootstrap` delegates account/provider UX to core modules.

The preferred public installer is release metadata plus a first-party stable domain. Internal GitHub/release implementation may evolve without requiring a new public URL.

## Loader budget

The previous 9 KiB loader ceiling was an internal CI guard, not a ChatGPT limit. Production enforces a 4 KiB Stage-1 budget to prevent policy/domain leakage. Raising the budget is not an acceptable fix for loader bloat.

## State safety

Resolution, installer-transport changes and engine replacement never alter LOCAL STATE except through a separately validated workspace-schema migration. Resolver failure cannot trigger account recreation, re-onboarding, deletion or migration guessing.
