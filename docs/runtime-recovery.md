# LWAI Runtime Recovery

Production 2026-08-29.11 adds durable workflow recovery without turning the conversation transcript into a database.

## Mental model

- Conversation context is volatile cache.
- Workspace Registry and account databases are canonical durable state.
- Audit Sessions persist detailed account-audit progress.
- Runtime Checkpoints persist compact generic workflow position.
- Runtime Journal is append-only write-ahead/event history.
- GitHub Production contains only sanitized schemas and behavior, never consumer rows.

## When to checkpoint

Use event-driven checkpoints for multi-artifact changes, migrations, account switches with pending work, `WAITING_USER` upload boundaries, meaningful audit/import phases, release promotion, tool blockers, or any operation where blind replay could duplicate/overwrite durable state. Atomic routine account updates do not need a separate checkpoint.

## Recovery procedure

1. Load mandatory core and Workspace Registry.
2. Resolve `active_account_id`.
3. Read unresolved checkpoint plus recent journal events.
4. Inspect actual affected durable artifacts.
5. Treat verified durable state as authoritative.
6. Do not replay verified successful writes.
7. Resume at the first unverified/pending action.
8. Advance safe point only after verification.
9. Mark `COMMITTED` only when the intended durable end state is verified.

If stored intent and durable state disagree, use `RECOVERY_REQUIRED` rather than guessing.

## Account isolation

Account-scoped checkpoints carry `account_id`. They cannot resume under another `active_account_id`. Workspace/global workflows such as engine releases may omit account_id but must not contain consumer account-private values in public artifacts.

## Batch recovery

When a requested screenshot/document batch is waiting for `done`, persist `WAITING_USER` plus the concise expected boundary when supported. Reload preserves the boundary; context loss never means the batch is complete.

## Provider behavior

Structured writable providers use checkpoint/journal tables or collections. File-only providers use a checkpoint index plus append-only JSONL/NDJSON or timestamped records. Read-only/no durable providers cannot promise persistent recovery.

## Privacy

Do not persist hidden chain-of-thought, raw internal reasoning, full transcripts, passwords/tokens, duplicated screenshots, or large evidence blobs in checkpoint state. Actual checkpoint rows, account identities and provider-local references stay private to the deployment.

## Release engineering

Release checkpoints are verify-before-replay transactions. Before retrying a branch, PR, merge, archive, or mirror write, inspect the actual target first. Pre-merge interruption leaves last-known-good main intact. After validated merge, a secondary mirror/archive failure is recorded and retried without silently rewriting healthy Production.
