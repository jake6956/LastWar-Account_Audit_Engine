# Storage Provider Matrix

Capability contract: `storage-api/1`

This matrix is advisory. Runtime capability detection always wins over static provider assumptions. Google Drive is the preferred/recommended and most-tested consumer persistence provider when a writable adapter is actually available, but provider choice always requires explicit user selection and verified capabilities.

| Environment | Likely profile | Preferred state form | Authoritative journal strategy | Canonical writable? | Rule |
|---|---|---|---|---|---|
| Google Drive / Workspace with native structured writes | STRUCTURED_RW or CAS_RW | Sheets/Docs + isolated folders | Native atomic append if actually exposed; otherwise revision/CAS-controlled Doc or immutable event artifacts | Yes when verified | Preferred/recommended when available; never infer capability from brand and never silently select |
| Generic database/transactional connector | TRANSACTIONAL_RW when atomic/CAS primitives are verified | Native structured records | Provider transaction/atomic append | Yes | Advertise only verified operations |
| Dropbox / generic writable files | FILE_RW; CAS_RW only if revision preconditions exist | JSON/CSV/Markdown/TXT + account directories | Immutable uniquely identified event files or verified CAS append | Yes for supported semantics | Fully supported when required capabilities verify; do not pretend file storage is a spreadsheet/database engine |
| Box search/reference-only | READ_ONLY | Reference files only | None | No | Use another writable provider or session exports |
| OneDrive / Microsoft 365 | Capability-detect | Excel/Word only if real workbook/document operations exist; otherwise files | Depends on verified transaction/CAS/create primitives | Capability-detect | Fully supported when required capabilities verify; brand name does not imply workbook semantics |
| Browser/session only | NONE | Conversation cache + exports | None | No | Continue fully but do not claim durable recovery |

## Provider choice
When the user opts into cloud persistence, show Google Drive first as **Recommended** if it is actually available and writable. Also show every other genuinely supported writable provider exposed by the host. Recommendation is not consent: the user explicitly selects the provider. If Google Drive is unavailable, a verified alternative remains a supported persistence target.

## Consumer data boundary
Each consumer's private LWAI data is stored only inside that consumer's selected personal provider and dedicated Last War/LWAI workspace. Consumer account data never routes through public GitHub, the maintainer's private Google Drive, another user's workspace, or unrelated folders in the consumer's provider account. Direct files deliberately supplied in chat are task inputs only and do not broaden provider scope.

## Capability descriptor
Adapters report booleans for `read`, `list`, `write`, `create`, `query`, `atomic_append`, `compare_and_swap`, `snapshot` and `restore`.

Persistence profiles are derived from those verified capabilities, not manually selected by brand.

## Required behaviors
- isolate LWAI writes from unrelated user files;
- preserve logical domains even when physical storage differs;
- preserve source/confidence/timestamps/immutable IDs;
- keep Workspace Registry and account namespaces isolated;
- maintain Change Log and Corrections continuity;
- use only concurrency-safe authoritative journal strategies;
- survive disconnect without corrupting canonical state;
- support provider-neutral export before migration when practical;
- validate snapshot/restore before advertising those capabilities;
- never overwrite local state during engine refresh.

## Journal safety
Authoritative Runtime Journal events require one of:
1. provider-native atomic append/transaction;
2. compare-and-swap or revision-controlled append;
3. immutable uniquely identified event creation.

A guessed-next-row shared-table write is never authoritative under concurrency. Unsafe tables may remain summary/index/cache only.