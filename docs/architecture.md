# LWAI Architecture

## System boundary
LWAI is a conversational application runtime with three deliberately separated planes:

1. **Interface/orchestration** — ChatGPT or another compatible conversational host.
2. **Shared engine/control plane** — sanitized, versioned GitHub Production.
3. **Private data plane** — each user's chosen writable storage environment, or volatile conversation state when no durable provider exists.

GitHub contains everything needed to know how LWAI operates and nothing needed to identify a player.

## Hub and spoke

### Hub: GitHub Production
GitHub `main` is the authoritative sanitized engine source. It contains the thin loader, release metadata, migration graph, module graph, independently versioned modules, schemas, adapters, tests, documentation, release manifests and complete fallback.

### Spokes: private deployments
Each deployment owns its Workspace Registry, immutable account IDs, mutable player identity, account facts, screenshots, balances, battle history, local Corrections, preferences, Audit Sessions, Runtime Checkpoints/Journal and provider-local references. Conversation is cache/interface, not durable authority when a canonical writable store exists.

## One-line distribution edge
Preferred public entrypoint:

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

The alias is transport convenience only. Canonical Production identity comes from:

- `releases/LATEST.json`
- `engine/BOOTSTRAP.txt`
- `engine/MANIFEST.json`
- `releases/MIGRATIONS.json`
- `engine/BOOTSTRAP_FULL.txt`

A legacy Google mirror can be a secondary fallback but is not a primary trust root.

## Thin loader boundary
`engine/BOOTSTRAP.txt` is intentionally orchestration-only and bounded by CI. It contains trust/version/API checks, capability discovery, dependency/integrity resolution, workspace/account/recovery ordering, update semantics and fallback. It does not carry Last War domain playbooks.

Domain logic lives in `engine/modules/domains/*`. Mandatory shared behavior lives in `engine/modules/core/*` and release modules. `BOOTSTRAP_FULL.txt` compiles the complete behavior for offline/recovery/manual transfer.

## Manifest, compatibility and integrity
`engine/MANIFEST.json` is both dependency graph and compatibility/integrity contract. It declares:

- Production engine/schema/API identity;
- load class and dependencies;
- shared vs local state scope;
- required/optional status;
- engine API range;
- workspace schema range;
- exact Git blob byte identity for each module.

CI reproduces each module's Git blob identity using the checkout. A host that can inspect/reproduce the same identity verifies fetched bytes before use. A host without that primitive must not claim cryptographic verification; it relies on canonical source + exact module identity/version plus last-known-good fallback.

## Migration graph
`releases/MIGRATIONS.json` defines supported version transitions. Engine-only edges preserve private state in place. Schema-changing edges require explicit transformations plus state-preservation tests before promotion. Missing required migration edges fail closed rather than inviting improvised transformations.

## Storage capability abstraction
Provider brand is not an architectural primitive. `storage-api/1` exposes verified capabilities for read/list/write/create/query/atomic-append/CAS/snapshot/restore and maps them to persistence profiles from NONE through TRANSACTIONAL_RW.

Recovery journaling requires atomic append/transaction, CAS/revision-controlled append, or immutable uniquely identified event creation. Guessed-next-row writes are not authoritative under concurrency.

## Runtime state layers
1. **ENGINE** — sanitized rules, modules, schemas, adapter contracts, commands, update/recovery logic.
2. **Workspace state** — Account Registry, `active_account_id`, provider metadata, optional recovery metadata.
3. **Account-local canonical state** — facts, evidence, Corrections, history, preferences, assets, sessions.
4. **Hot Cache** — compact derived working state; disposable/rebuildable.
5. **Gold Assets** — optional versioned sanitized shared references.

Engine refresh may replace layer 1 only unless an explicit validated migration transforms schema while preserving local meaning.

## Self-healing loop
Input -> resolve account -> parse supported facts -> compare canonical state -> reconcile by evidence/freshness/confidence -> record material change -> invalidate stale derived recommendations -> recompute affected targets -> refresh cache -> answer concisely.

Runtime/release recovery adds: inspect checkpoint intent -> inspect actual durable artifacts -> verify committed writes -> replay only genuinely missing work -> advance safe point -> commit only after intended durable end state is verified.

## Behavior-as-tested-code
Production CI has two independent layers:

- **release-tree validation** checks identity/version/API/schema parity, module DAG, module byte integrity, migration graph, privacy markers, loader budget and fallback completeness;
- **deterministic runtime regressions** execute account isolation, archive/start-over, migration preservation, Audit Session isolation, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal exposure and provider degradation.

The reference runtime is a test oracle for invariants, not a replacement for the conversational engine.

## Release loop
Private Prod-Dev -> frozen private RC -> GitHub `rc/<version>` -> exact-head PR CI + private gates -> exact validated-head merge -> main CI/public endpoint/installer verification -> private archive/release record synchronization.

Failed pre-merge candidates preserve last-known-good `main`. Post-merge secondary mirror/archive failure is recorded for retry rather than rolling back validated Production.

## Privacy boundary
The visible installer omits private player state entirely. Resolving the short URL exposes public repository provenance, so the distribution is low-friction rather than anonymous. Private user state never flows back into shared Production.

## Design objective
Installation friction approaches one line; active context stays bounded; domain modules load only when needed; durable users can recover across conversation loss; non-durable users degrade honestly; engine upgrades are centrally maintained; private state remains user-owned and isolated.
