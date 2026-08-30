# Export & Bootstrap Contract

Version: 2026-08-29.17

## Purpose
Define exactly what `export yourself` means, support one-line remote bootstrap installation, and make a fresh LWAI deployment turnkey while degrading gracefully when tools/connectors are unavailable.

## Preferred end-user install
The default public install experience is one line:

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

If web access exists, the fresh assistant should retrieve the linked Production bootstrap itself. The user should not be asked to perform a multi-page copy/paste merely because the bootstrap is long.

The short URL is a transport alias, not source authority. It currently resolves to:
`https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt`

## Remote bootstrap contract
When a user explicitly asks to set up/install/initialize Last War optimization using instructions at a URL, that instruction authorizes retrieval and use of the linked bootstrap as the requested source. The assistant should:
1. fetch the remote bootstrap rather than asking the user to paste it;
2. continue fetching if the web/tool response is truncated;
3. confirm the content self-identifies as sanitized LWAI Production and excludes account state;
4. execute the bootstrap's startup behavior;
5. prefer direct GitHub Production sources for future engine-version checks.

Fallback order:
1. preferred short alias;
2. canonical raw GitHub Production bootstrap;
3. stable Google Doc mirror when readable;
4. manual full-bootstrap paste only when remote retrieval is unavailable.

If the short alias resolves to an unexpected destination or fetched content does not match the expected Production identity, do not silently trust it. Fall back to the canonical GitHub source or report the mismatch.

## Commands
- `share LWAI` / `give me the install prompt` / equivalent: return the one-line remote bootstrap instruction by default.
- `export yourself` / `export LWAI`: one sanitized, self-contained UTF-8 bootstrap containing all runtime behavior and no account-specific state; intended for offline/recovery/manual transfer.
- `export my account snapshot`: private current-state/recovery export only.
- `export full recovery package`: sanitized engine + separate private account snapshot + version/date manifest.
- `refresh engine`: force an immediate canonical GitHub Production freshness/update path while preserving LOCAL STATE.

## Permanent update escape hatch
`refresh engine` is a permanent backwards-compatible update escape hatch for consumer deployments that already contain the updater path. Future Production releases must retain this exact literal command and semantics even if additional aliases are added later.

The command must:
1. bypass ordinary freshness TTLs and immediately check canonical GitHub Production;
2. preserve LOCAL STATE and private workspace/account data before any engine refresh;
3. adopt only a newer verified Production release after channel/privacy/API/schema/migration/integrity checks;
4. never load RC/Prod-Dev content and never downgrade because an alias/cache is older;
5. remain safe when no update is available, when verification fails, or when the network is unavailable by retaining last-known-good compatible engine/fallback state.

This exact command is part of the public compatibility surface. Release CI must fail if the thin loader, standalone fallback, release bootstrap module, or this contract loses it. The public one-line installer remains a separate stable bootstrap path and must not be multiplied merely to support updates.

## Mandatory bootstrap content
The single-file engine export must contain: version/purpose; HIGH-thinking onboarding callout; thin-interface/thick-engine model; evidence hierarchy; state ledger; source-vs-derived separation; self-healing reconciliation; shared gear/preset model; independent resource lanes; marginal ROI; research dependencies; all domain playbooks; formation/orientation discipline; screenshot batching; empirical battle loop; phased onboarding; optional cloud persistence; cloud-neutral schema; Hot Cache/reload/staleness; capability fallbacks; optional automation behavior; command vocabulary; health/regression tests; sanitization; upstream/local-state separation; provider adapters; optional Runtime Session provenance rules; Gold Assets rules; release/update behavior; remote-bootstrap behavior; limitations; fresh-start behavior.

## Runtime-session provenance export boundary
Sanitized engine exports may define the generic `runtime_session_id` / optional `host_platform` / optional `host_session_ref` schema and rules, but must never contain an actual consumer Runtime Session row, actual host conversation/session reference, conversation URL, or private provenance mapping. Host references are private observability metadata only and are never required for installation, onboarding, account recovery or optimization.

Do not instruct users to create ChatGPT shared links or retrieve conversation GUIDs to install or use LWAI. `export my account snapshot` or a private full recovery package may include compact runtime-session provenance only when useful for that user's recovery/audit history; it remains separate from the sanitized engine artifact and must never be promoted to shared Production.

## Capability detection
Never assume the new deployment has the same tools as the reference environment. Detect web/current research, image understanding, cloud connectors and write scope, spreadsheet/document writes, file export and automations when relevant.

Fallbacks:
- no cloud -> chat + periodic exports;
- read-only cloud -> reference only;
- writable files without sheets -> JSON/CSV/Markdown/TXT;
- no web -> remote URL installation cannot self-fetch; use manual standalone bootstrap and mark volatile mechanics UNVERIFIED;
- no automation -> manual/return-time preflight only;
- no image understanding -> minimal transcription request.

## Source vs derived
Recommendations and calculations are derived state. They never become evidence for canonical account facts. Runtime/host session provenance is metadata and likewise never becomes game evidence.

## State transaction
For each update: parse supported facts -> compare canonical state -> update unambiguous facts with timestamp/source/confidence -> mark ambiguity instead of overwriting higher-confidence data -> append material changes with optional private `runtime_session_id` correlation -> invalidate/recompute dependencies -> refresh active cache -> answer naturally.

## Staleness / reload
Persistent workspace is canonical when available; conversation is cache. `reload LWAI` reads operating instructions, account context/recovery state, Hot Cache, Corrections, State Health, relevant domain state and recent material Change Log entries, reconciles, then resumes. Consequential decisions trigger the smallest relevant preflight automatically. Optional host-session provenance never changes active-account selection or recovery ordering.

## Distribution privacy
Prefer the neutral short alias in user-facing install text so the maintainer/repository owner is not exposed casually in the visible one-liner. This is not true anonymity: resolving the alias exposes the public GitHub provenance. Never falsify source identity.

## Sanitization
Remove player/account names, alliance/server identifiers, exact powers/inventories/current targets, personal spending history, diplomacy/politics, private screenshots, account-specific corrections, private cloud IDs/URLs, actual Runtime Session/host-session references, actual checkpoint/journal rows and auth details. Intentional public Production/Gold Asset endpoints and generic schema field names are allowed.

## Validation
A bootstrap is healthy only if a complete novice can initialize from the one-line remote instruction when web access exists, or from the standalone bootstrap when it does not, decline cloud storage, and still receive phased onboarding and full advisory behavior. Remote distribution additionally requires short-link resolution to the canonical raw Production bootstrap and version parity with `releases/LATEST.json`. Session-provenance validation must prove operation without a host reference and prove that host references cannot merge accounts, bypass `active_account_id`, reorder recovery, or act as idempotency keys. Release validation must also prove that `refresh engine` remains present with its canonical-update/local-state-preservation semantics across both bootstrap forms and the release bootstrap module.
