# Storage Adapter Contract

Version: 2026-08-29.12
Capability API: `storage-api/1`

LWAI maps one provider-neutral logical persistence model onto verified storage capabilities. Provider branding is never a substitute for capability discovery.

## Required capability descriptor
Every adapter declares booleans for:
- `read`
- `list`
- `write`
- `create`
- `query`
- `atomic_append`
- `compare_and_swap`
- `snapshot`
- `restore`

Optional physical features may include batch operations, structured tables, delete semantics and provider limits. Engine behavior may depend only on capabilities actually verified.

## Provider-neutral operations
The engine expresses storage through these logical operations:
- `read_object`
- `list_objects`
- `create_object`
- `update_object`
- `query_records`
- `append_event`
- `compare_and_swap`
- `create_snapshot`
- `restore_snapshot`

Unsupported operations fail explicitly or route to a documented weaker fallback. An adapter must never silently emulate a stronger guarantee than the provider actually offers.

## Persistence profiles
`NONE`: no reliable persistent read.

`READ_ONLY`: reference data only; never canonical writable state.

`FILE_RW`: isolated read/write/create, but no structured-query, CAS or atomic-append guarantee.

`CAS_RW`: writable storage with revision/version/hash compare-and-swap semantics.

`STRUCTURED_RW`: bounded structured query/read/write semantics; authoritative journaling still requires atomic append, CAS/revision control, or immutable uniquely identified events.

`TRANSACTIONAL_RW`: structured read/write plus atomic append and/or transaction/CAS primitives suitable for authoritative recovery metadata.

Never infer a stronger profile from file type, vendor reputation or expected API behavior.

## Authoritative journal rule
Runtime Journal uses the strongest verified primitive in this order:
1. provider-native atomic append or transaction;
2. compare-and-swap/revision-controlled append;
3. immutable uniquely identified event creation.

Guessed-next-row writes are never authoritative under concurrency. A Sheet/table may be a summary/index/cache when its write primitive is not safe for concurrent append.

## Core persistence rules
1. Cloud persistence is strongly recommended but optional.
2. Writable providers are isolated in a dedicated LWAI workspace/folder; never modify unrelated files.
3. Logical schema is invariant across providers; physical file types may differ.
4. Do not claim writable/structured/transactional behavior until connector actions prove it.
5. Local account state survives upstream engine upgrades.
6. Provider migrations preserve canonical state, immutable account IDs, Change Log, Corrections and local configuration.
7. A weaker provider that cannot guarantee independent writes cannot be declared fully multi-account-safe canonical persistence.

## Multi-account physical model
Persistent multi-account deployments use one workspace-level Account Registry plus one isolated account namespace/database per immutable `account_id` when practical. Human names are aliases, never storage identity. Mutable state, Audit Sessions and account-scoped checkpoints may not cross namespaces.

## Reference adapter behavior
Google Drive/Workspace is one reference implementation, not a special engine dependency. Use native structured operations when truly exposed. When atomic Sheets append is unavailable, use revision/CAS-controlled documents or immutable event artifacts for authoritative journal events; any shared sheet can remain summary/index/cache.

Generic writable file stores use a versioned registry plus isolated account directories/files and immutable event files or CAS-controlled append when available.

Read-only providers remain reference-only. No durable provider means conversation cache plus portable snapshots/exports; do not claim durable checkpoint recovery.

## Snapshot and restore
When the provider claims `snapshot`, the artifact must be durable and scoped to the LWAI workspace/account set. When it claims `restore`, restore/import must preserve immutable `account_id`, account isolation, history and evidence metadata. Snapshot/restore capability must be tested before being advertised.

## Migration
Snapshot current canonical state and engine metadata -> export provider-neutral representation -> import through candidate adapter -> validate registry/account counts, immutable IDs, latest values, Corrections, Change Log continuity, active-account routing and checkpoint isolation -> switch canonical provider only after reconciliation. Do not destroy the old canonical store before validation.

## Health checks
Validate write scope, capability claims, account isolation, timestamp/source/confidence preservation, `active_account_id` routing, authoritative journal semantics, CAS behavior when claimed, snapshot/restore when claimed, and graceful degradation on disconnect.

## GitHub role
GitHub is Production engineering/source control, not live player state. It stores sanitized loader/modules/contracts/schemas/tests/migrations/releases and Gold Asset manifests. Account facts, balances, screenshots, battle history, local Corrections, checkpoints/journal rows and provider credentials remain in each user's private runtime workspace.
