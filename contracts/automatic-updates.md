# Automatic Consumer Engine Update Contract

Version: 2026-08-29.18

## Objective
Keep ordinary LWAI consumer deployments on the newest verified GitHub Production engine without requiring reinstall or routine manual update commands, while preserving all private/local account state and last-known-good rollback behavior.

## Authority
Canonical authority is GitHub Production `main` through `releases/LATEST.json`, `engine/MANIFEST.json`, `releases/MIGRATIONS.json`, `engine/BOOTSTRAP.txt` and canonical module paths. The TinyURL remains a single transport alias, not an update authority. RC/Prod-Dev content is never adopted automatically.

## Trigger policy
With web access, automatic update preflight occurs:
1. on every runtime/session startup before ordinary domain work;
2. before `reload LWAI` / `reload yourself` reconstructs working state;
3. before schema-sensitive migration/recovery when canonical compatibility matters;
4. before consequential work in a long-lived runtime once at least six hours have elapsed since the last successful canonical check.

No daemon/background process is implied. Dormant conversations update on the next interaction unless the user separately opts into an actually available scheduler.

## Transaction
A triggered check fetches canonical `LATEST.json` first. If installed Production is current, the check is a silent no-op. If a newer release exists, LWAI must verify Production channel, sanitization/account-state flags, engine API compatibility, workspace-schema compatibility, a declared migration chain, canonical loader/manifest identity and available module integrity before activation.

Fetch only changed required engine components plus task-relevant modules where modular loading is available. Preserve LOCAL STATE. Apply only validated migrations. Health-check the candidate before activation. Adopt the candidate atomically from the runtime's point of view, then resume and complete the user's original pending action under the new engine.

## Failure and rollback
Any retrieval, identity, privacy, compatibility, migration, integrity or post-update health failure retains last-known-good compatible ENGINE and leaves LOCAL STATE untouched. Never partially activate a failed candidate and never rewrite account data to repair engine uncertainty. Continue the user's requested task on last-known-good when safe; fail closed only when the retained engine cannot safely perform the requested operation.

## Optional workspace metadata
Durable providers may store compact workspace-level metadata only:
- `installed_engine_version`
- `last_successful_update_check`
- `last_successful_engine_update`
- `last_known_good_engine_version`
- `update_policy`
- `update_health`
- optional `last_update_error_summary`

These fields are operational engine metadata, not account evidence or routing data, and remain private to the user's deployment. Adding them to existing Workspace/Shared Engine Metadata is additive and does not by itself require a workspace schema bump.

## Manual compatibility escape hatch
`refresh engine` is a permanent backwards-compatible public command. It bypasses normal TTL rules and forces the same canonical update transaction while preserving LOCAL STATE. `check for LWAI updates` may remain an alias. Normal users should not need either command routinely.

## Distribution rule
There remains one public installer:

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

Automatic updating must never create beta/stable installers, per-user code branches, or alternate consumer release channels.
