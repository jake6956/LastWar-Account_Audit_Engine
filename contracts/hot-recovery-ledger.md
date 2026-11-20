# Hot Recovery Ledger / Cross-Chat Continuity Contract

Production candidate 2026-11-19.52 | Engine API 1.0 | Workspace schema 2.3 unchanged | Sanitized shared ENGINE only.

## Commands
Within LWAI, recognize `LWAI catch up`, `catch up on LWAI`, `resume LWAI`, `where were we?`, and contextual `catch up`, in addition to `reload LWAI`. The host's conversation ID or user memory is never a requirement.

## Private storage
Keep one optional **LWAI — Active Recovery Ledger** (or provider-native logical equivalent) only in each user's chosen dedicated LWAI workspace. It contains a short current resume digest plus append-only material events, not account truth, transcript history, or a public repo artifact. Cloud writes are provider-capability-aware and must be read back before claiming persistence. Existing workspaces initialize it lazily; do not reset or re-onboard. Current account data continues to live in canonical records.

## Event shape and durability
Each event has `event_id`, `occurred_at` (UTC), `scope` (WORKSPACE or ACCOUNT), nullable `account_id`, optional `checkpoint_id`, `event_type`, `action`, `result`, boolean `verified`, optional `evidence_ref`, and `next_action`. Duplicate ID with different content is an error. Persist intent before consequential multi-artifact operations; write/audit success requires verification; failures are RECOVERY_REQUIRED. Event types describe important objective changes, decisions, writes, checks, releases, blockers and WAITING_USER boundaries. Do not save every chat turn.

## TTL and continuity
Hot events expire after 72 hours and at most 32 recent ordinary events are displayed. Reads ignore expired entries; compact on the next successful mutation. Unresolved OPEN/WAITING_USER/RECOVERY_REQUIRED checkpoints and necessary event pointers never expire until verified terminal status. Canonical account history and Change Log use their own retention; do not delete them. File-only providers may use a digest file plus immutable individual event records; structured providers may use native records.

## Recovery
Refresh live engine, resolve Registry/active_account_id, read the ledger and unresolved checkpoint/journal, verify actual referenced artifacts, and load relevant canonical account facts. Report separately what was verified, what remains pending, and the next safe action. The ledger is operational metadata, never proof of a current game number or successful deployment. Fail honestly when storage unavailable; do not fill holes from conversational memory.

## Safety
ACCOUNT events require account_id and never cross account boundaries; WORKSPACE events contain no account-private fields. Never put consumer records/IDs in public GitHub, other users' workspaces, or maintainer storage. Do not store full transcripts, hidden reasoning, tokens, passwords, or duplicated screenshots. Existing Engine API 1.0 / schema 2.3 and account records remain intact.
