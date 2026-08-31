# LWAI Architecture

## System boundary
LWAI is a conversational application runtime with four deliberately separated planes:

1. **Public distribution edge** — first-party `https://lastwarai.com` single-response configuration delivery.
2. **Interface/orchestration** — ChatGPT or another compatible conversational host.
3. **Shared engine/control plane** — sanitized, versioned GitHub Production.
4. **Private data plane** — each user's chosen writable storage environment, or volatile conversation state when no durable provider exists.

GitHub contains everything needed to know how LWAI operates and nothing needed to identify a player.

## Hub and spoke

### Hub: GitHub Production
GitHub `main` is the authoritative sanitized engine source. It contains the Stage-1 loader, release metadata, migration graph, module graph, independently versioned modules, schemas, adapters, tests, documentation, release manifests and complete fallback.

### Spokes: private deployments
Each deployment owns its Workspace Registry, immutable account IDs, mutable player identity, account facts, screenshots, balances, battle history, local Corrections, preferences, Audit Sessions, Runtime Checkpoints/Journal and provider-local references. Conversation is cache/interface, not durable authority when a canonical writable store exists.

## One-line distribution edge
Preferred public instruction:

`Set up Last War optimization using the instructions at https://lastwarai.com`

LastWarAI.com is the stable first-party installation endpoint. For a fresh install, Cloudflare resolves the live GitHub Production `main` commit server-side, retrieves `engine/BOOTSTRAP_FULL.txt` from that exact immutable commit, adapts only the already-completed generic Stage-0 discovery section, and returns the complete sanitized configuration in the same response. The user's AI does not need a second GitHub or engine-URL request to install LWAI.

The endpoint identifies the resolved commit and permits independent verification. GitHub `main` remains the underlying Production source/version authority. The previously circulated TinyURL remains a legacy compatibility alias only; it is not a normal install dependency or trust root.

## Production authority
Underlying current-version authority begins at:

`https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`

For normal first-party installation, Cloudflare resolves commit C and fetches the complete fallback from exact C before returning the response. For direct/modular startup and update transactions, trusted reads are pinned to one exact C:

- `releases/LATEST.json`
- `engine/BOOTSTRAP.txt`
- `engine/MANIFEST.json`
- `releases/MIGRATIONS.json`
- required/task-relevant modules
- `engine/BOOTSTRAP_FULL.txt`

Search/index results, redirects, README snapshots, mutable raw `main`, public aliases and model memory cannot establish current Production.

## Thin loader boundary
`engine/BOOTSTRAP.txt` remains intentionally orchestration-only and bounded by CI at 4 KiB for direct GitHub/modular operation and recovery paths. It contains live-ref resolution, pinned-snapshot validation, mandatory-module loading, local-state preservation, update/recovery handoff and fallback. It does not carry provider onboarding or Last War domain playbooks.

Domain logic lives in `engine/modules/domains/*`. Mandatory shared behavior lives in `engine/modules/core/*` and release modules. `BOOTSTRAP_FULL.txt` is the complete sanitized standalone/recovery runtime and the source used by LastWarAI.com's single-response initial-install transport.

## Manifest, compatibility and integrity
`engine/MANIFEST.json` is both dependency graph and compatibility/integrity contract. It declares Production engine/schema/API identity; load classes/dependencies; shared vs local state scope; required/optional status; API/schema ranges; activation metadata; and exact Git blob byte identity for each module.

CI reproduces module Git blob identity using the checkout. A host without that primitive must not claim cryptographic verification; it relies on exact-commit pinning, canonical source and last-known-good fallback.

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
Production CI has four layers:

- **public-entrypoint validation** checks that LastWarAI.com returns one transparent complete sanitized configuration, exposes the resolved SHA, matches live GitHub Production, and is not serving a stale mutable response;
- **release-tree validation** checks identity/version/API/schema parity, module DAG, module byte integrity, migration graph, privacy markers, 4 KiB loader boundary and fallback completeness;
- **instruction-budget validation** reports Stage-1, mandatory-core, optional-module and complete-fallback growth against explicit budgets;
- **deterministic runtime regressions** execute account isolation, archive/start-over, migration preservation, Audit Session isolation, `WAITING_USER`, verify-before-replay, checkpoint-loss tolerance, append-only journal exposure, provider degradation, UX staging and infrastructure-boundary behavior.

## Public cache boundary
The mutable LastWarAI.com entrypoint is a gateway/router and must execute for every request so it can resolve current GitHub Production. Deployment-level Workers Caching for the default entrypoint must therefore be disabled. Exact-SHA engine retrieval remains safe to cache immutably because commit-addressed GitHub content cannot change. Response-level `no-store` headers remain defense in depth, not a substitute for disabling front-of-Worker caching.

## Release loop
Private Prod-Dev -> frozen private RC -> GitHub `rc/<version>` -> exact-head PR CI + private gates -> exact validated-head merge -> main CI/public entrypoint verification -> private archive/release record synchronization.

Failed pre-merge candidates preserve last-known-good `main`.

## Privacy boundary
The public configuration contains sanitized engine material only. Public GitHub provenance remains discoverable and truthful. Private user state never flows back into shared Production.

## Design objective
Installation friction is one stable first-party line; first install is one transparent public configuration response; active context stays bounded; domain modules load only when needed; durable users can recover across conversation loss; non-durable users degrade honestly; engine upgrades are centrally maintained; private state remains user-owned and isolated.