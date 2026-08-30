# Private Failsafe Mirror Contract

Version: 2026-08-30.26

## Purpose
Keep the maintainer-controlled private Google Drive LWAI file set usable as an independent recovery/failsafe copy without making private storage a public runtime trust root or exposing private account data.

## Authority
GitHub `main` remains authoritative sanitized Production. `https://lastwarai.com` remains the preferred public Stage-0 transport and the live GitHub `main` commit SHA remains current-version authority.

The private Google Drive mirror is a disaster-recovery/failsafe artifact set. It must never override a newer verified GitHub Production identity and must never contain consumer account data in shared engine artifacts.

## Mandatory pre-promotion gate
Before opening/merging a Production release candidate, synchronize the private LWAI Drive failsafe set to the exact sanitized RC candidate and verify it. Promotion is blocked when this pre-promotion mirror gate is incomplete or unverifiable.

At minimum the candidate failsafe set must contain current, mutually consistent copies of:
- complete sanitized standalone fallback / Portable Instruction Set;
- release identity / LATEST metadata;
- engine module manifest including exact module versions/integrity identities;
- migration graph;
- public installer/recovery README guidance;
- critical operating, persistence, account, storage, runtime-recovery and user-flow-continuity contracts/modules;
- release candidate summary identifying engine version, API, schema, source branch/head and state-preservation behavior.

The mirror may use native Google Docs/Sheets representations rather than byte-identical Git files, but semantic identity/version/module lists must match the exact RC. A versioned candidate snapshot must be retained in the private Release Candidates area before Production merge.

## Post-merge synchronization
After exact validated-head merge and successful `main` CI/public endpoint verification:
1. verify the actual Production merge SHA/version;
2. update the private primary failsafe documents to the merged Production identity;
3. create/verify the versioned Production archive in the private Production Releases area;
4. update private release/engine module registries and changelog records;
5. record the post-merge mirror as synchronized only after re-reading the written artifacts.

A post-merge private mirror failure does not roll back healthy GitHub Production. Mark private mirror health degraded, preserve the prior failsafe set, and retry synchronization. The next release may not promote until the failsafe mirror is healthy again.

## Source-staging hygiene
The private `GitHub Source Staging` tree is a maintained recovery aid, not an empty placeholder. If file-for-file source mirroring is not supported by the active connector, maintain a versioned sanitized source/recovery snapshot that is sufficient to reconstruct the current Production engine, and explicitly record which representation is authoritative inside the failsafe set.

Do not claim a Drive source subtree is current when it is empty or incomplete. Empty/stale staging is a release-health failure to repair before the next promotion.

## Workspace boundary
All mirror operations are restricted to the known LWAI Drive workspace and its known release/module/failsafe folders. Never browse, search, inspect or mutate unrelated Google Drive content while performing synchronization.

## Private runtime-state hygiene
Before promotion, inspect LWAI-owned Runtime Checkpoints, Runtime Journal and Audit Sessions for unresolved release/onboarding work. `COMMITTED`/`COMPLETE` records require no replay. `WAITING_USER`, `OPEN` or `RECOVERY_REQUIRED` records must be classified and either safely resumed, intentionally preserved with an explicit next action, or resolved before claiming the workspace is clean. Never infer an interrupted conversation as implicit `done`.

## Release gate evidence
The private release record should capture, at minimum:
- candidate engine version and RC head SHA;
- Drive mirror synchronization time/status;
- no-dead-air/user-flow regression result;
- public installer validation result when available;
- exact-head public CI result;
- merged Production SHA and post-merge CI result;
- post-merge Drive mirror/archive synchronization status.

## Failure behavior
Pre-promotion mirror failure: do not promote.
Pre-promotion unresolved private release state: recover/resolve before promotion.
Post-merge mirror failure: keep validated GitHub Production, mark mirror degraded, retry; do not fabricate success.

This contract changes release hygiene only. It does not change Engine API 1.0, workspace schema 2.3, account state, provider authorization rules or the public trust chain.
