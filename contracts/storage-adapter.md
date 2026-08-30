# Storage Adapter Contract

Version: 2026-08-30.26
Capability API: `storage-api/1`

LWAI maps one provider-neutral persistence model onto verified storage capabilities. Provider branding is never a substitute for capability discovery.

## Data placement invariant

Public GitHub contains sanitized engine code, contracts, schemas, tests, release metadata and reusable non-user-specific knowledge only. Private maintainer/Prod-Dev state and private failsafe artifacts remain in the maintainer-controlled private LWAI Google Drive workspace and are never copied into public GitHub.

Consumer/player account state is never stored in the maintainer's Drive or in GitHub. Each end user's private LWAI state is stored only in that user's explicitly selected personal storage provider, inside that user's dedicated Last War / LWAI workspace. Session-only users remain in the current conversation/runtime and are told that cross-chat durability is limited.

## Absolute workspace boundary

A connected provider account is **not** an LWAI data source. LWAI may operate only inside the dedicated Last War / LWAI workspace created or explicitly adopted for this tool.

While operating as LWAI it must never read, list, search, inspect, summarize, index, modify, move, rename, delete, or otherwise touch provider content outside that workspace—even if the connector technically exposes broader access. Unrelated folders, other ChatGPT/app workspaces, personal documents, photos, spreadsheets, backups and all sibling content are out of scope.

Provider authorization can be broader than the application's logical scope. Broader connector capability is not permission to use unrelated content. Workspace discovery must use the minimum operation needed to locate the known LWAI workspace by its marker/name/identifier or create it when absent; provider-wide exploratory browsing is prohibited.

A user may explicitly upload or reference an external file in chat. That file may be consumed as explicit task input, but this does not authorize browsing its storage neighborhood or altering the external source in place.

## Mandatory user reassurance

Before authorization LWAI must tell the user, in plain language, that it has explicit workspace-only guardrails. Wording may vary, but must preserve this meaning:

> LWAI is explicitly restricted to its own Last War workspace. I will not browse, read, change, move, delete, or use anything else in your connected storage. Even if the connector technically exposes broader access, everything outside the LWAI workspace is off-limits to this tool.

Also state that authentication happens in the provider/ChatGPT UI and LWAI never asks for passwords, OAuth codes, tokens, cookies or similar credentials in chat.

After successful verification, briefly confirm that the workspace-only guardrail is active. Describe this accurately as an application/runtime guardrail; do not claim provider-side ACL enforcement LWAI does not control.

## Required capability descriptor

Every adapter declares booleans for `read`, `list`, `write`, `create`, `query`, `atomic_append`, `compare_and_swap`, `snapshot`, and `restore`. Every capability is scoped to the LWAI workspace. Optional physical features may include batch operations, structured tables, delete semantics and provider limits. Engine behavior may depend only on capabilities actually verified.

## Provider-neutral operations

`read_object`, `list_objects`, `create_object`, `update_object`, `query_records`, `append_event`, `compare_and_swap`, `create_snapshot`, and `restore_snapshot` are valid only when their target resolves inside the active LWAI workspace. Unsupported operations fail explicitly or route to a documented weaker fallback; adapters never silently emulate stronger guarantees.

## Persistence profiles

`NONE`: no reliable persistent read.  
`READ_ONLY`: reference data only; never canonical writable state.  
`FILE_RW`: isolated read/write/create, no structured-query/CAS/atomic-append guarantee.  
`CAS_RW`: writable storage with revision/version/hash compare-and-swap.  
`STRUCTURED_RW`: bounded structured query/read/write; authoritative journal still requires atomic append, CAS/revision control, or immutable unique events.  
`TRANSACTIONAL_RW`: structured read/write plus atomic append/transaction/CAS suitable for authoritative recovery metadata.

Never infer a stronger profile from file type, vendor reputation or expected API behavior.

## Provider preference, selection and authorization

Cloud persistence is recommended but optional. **Google Drive is LWAI's preferred/recommended and most-tested consumer storage provider when it is actually available with verified writable capability.** Present it first and label it Recommended/Preferred when appropriate.

Preference is not consent. The user must explicitly choose Google Drive or another offered provider; never silently select a provider. Detect providers actually available/installable and offer every genuinely supported writable alternative. Supported alternatives may include Dropbox, OneDrive / Microsoft 365, Box when writable, or another provider that satisfies `storage-api/1` read/write/create verification.

A fully verified alternative provider is a supported persistence target, not a degraded fake option. Capability differences may change implementation details and recovery guarantees, but account isolation, workspace-only scope, privacy and no-dead-air handoff remain mandatory.

Before opening authorization, show the workspace-only reassurance above.

For Google Drive, explain the guardrail, approve access needed for the LWAI workspace, and choose **`Allow always`** if ChatGPT offers it. For Dropbox, OneDrive/Microsoft 365, Box or another supported provider, use the actual host/provider wording and recommend an equivalent persistent authorization option only when truly shown. Never invent OAuth scope names or request credentials in chat.

A user saying `connected` is a recheck trigger, not proof. Re-detect capability, locate/create only the LWAI workspace, perform a harmless workspace-local write/read when appropriate, and then confirm connection plus the active workspace-only guardrail. Successful verification immediately returns to the next user-visible onboarding/resume step; it may not end on connection status alone.

## Authoritative journal rule

Runtime Journal uses the strongest verified primitive in this order: provider-native atomic append/transaction; compare-and-swap/revision-controlled append; immutable uniquely identified event creation. Guessed-next-row writes are never authoritative under concurrency.

## Multi-account physical model

Persistent multi-account deployments use one workspace-level Account Registry plus an isolated account namespace/database per immutable `account_id` when practical. Human names are aliases, never storage identity. Mutable state, Audit Sessions and account-scoped checkpoints may not cross account namespaces or escape the LWAI workspace.

## Snapshot, restore and migration

Snapshots and restores remain inside the LWAI workspace and preserve immutable `account_id`, account isolation, history and evidence metadata. Provider migration exports only LWAI state and imports it into the candidate provider's dedicated LWAI workspace. Never inspect or alter unrelated provider content during migration. Do not destroy the old LWAI store until reconciliation succeeds.

## Health checks

Validate workspace scope isolation, capability claims, account isolation, timestamp/source/confidence preservation, `active_account_id` routing, authoritative journal semantics, CAS when claimed, snapshot/restore when claimed, and graceful degradation on disconnect.

## GitHub role

GitHub is sanitized Production engineering/source control, not live player state and not private Prod-Dev storage. Account facts, balances, screenshots, battle history, local Corrections, checkpoints/journal rows and provider-local state remain inside each user's private LWAI workspace. Unrelated connected-storage content is never part of LWAI state.