# Export & Bootstrap Contract

Version: 2026-08-30.25

## Purpose
Define exactly what `export yourself` means, support one-line remote bootstrap installation, and make a fresh LWAI deployment turnkey while degrading gracefully when tools/connectors are unavailable.

## Preferred end-user install
The default public install experience is one line:

`Set up Last War optimization using the instructions at https://lastwarai.com`

`https://lastwarai.com` is the permanent first-party human-facing entrypoint. It serves a tiny sanitized Stage-0 locator. The locator is transport/discovery only and does not establish the current engine version.

After retrieving the locator, the assistant resolves the live GitHub Production `main` branch ref at `https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main`, obtains its current `commit.sha`, then retrieves `engine/BOOTSTRAP.txt` and all trusted engine material from that exact immutable commit.

The previously circulated `https://tinyurl.com/2yxf7f5x` is retained only as a legacy compatibility alias. New sharing must use LastWarAI.com. A third-party shortener, preview/interstitial, redirect, repository cache, raw mutable `main`, search index or model memory is never source/version authority.

## Remote bootstrap contract
When a user explicitly asks to set up/install/initialize Last War optimization using the public installer URL, that instruction authorizes retrieval and use of the public sanitized Stage-0 locator. The assistant should:
1. fetch the first-party locator rather than asking the user to paste a larger bootstrap;
2. read the live GitHub `main` branch ref and obtain a valid current commit SHA;
3. fetch `engine/BOOTSTRAP.txt` from that exact SHA;
4. confirm pinned release content self-identifies as sanitized LWAI Production and excludes account state;
5. execute startup behavior rather than stopping at a documentation summary;
6. keep all trusted reads in one startup/update transaction pinned to that same exact commit.

Fallback order:
1. first-party `https://lastwarai.com` Stage-0 locator;
2. canonical GitHub live-ref resolver when its coordinates are already known from trusted LWAI material;
3. last-known-good compatible local engine/module state when available;
4. exact-commit canonical GitHub `BOOTSTRAP_FULL.txt` after a live commit is resolved;
5. manual full-bootstrap transfer only when remote retrieval is unavailable.

A supplied legacy alias/cache may be ignored if unavailable, stale, preview-gated or inconsistent. Never repair transport failure by changing user-local account state.

## Commands
- `share LWAI` / `give me the install prompt` / equivalent: return `Set up Last War optimization using the instructions at https://lastwarai.com`.
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
The single-file engine export must contain: version/purpose; evidence hierarchy; state ledger; source-vs-derived separation; self-healing reconciliation; shared gear/preset model; independent resource lanes; marginal ROI; research dependencies; all domain playbooks; formation/orientation discipline; screenshot batching; empirical battle loop; phased onboarding; optional cloud persistence; cloud-neutral schema; reload/staleness; capability fallbacks; command vocabulary; health/regression tests; sanitization; upstream/local-state separation; provider adapters; optional Runtime Session provenance rules; Gold Assets rules; release/update behavior; remote-bootstrap behavior; limitations; fresh-start behavior.

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

## Distribution privacy and provenance
The first-party installer keeps the normal public prompt clean while still resolving to public GitHub Production. This is not anonymity. Public provenance must remain truthful and discoverable; never falsify source identity.

## Sanitization
Remove player/account names, alliance/server identifiers, exact powers/inventories/current targets, personal spending history, diplomacy/politics, private screenshots, account-specific corrections, private cloud IDs/URLs, actual Runtime Session/host-session references, actual checkpoint/journal rows and auth details. Intentional public Production/Gold Asset/install endpoints and generic schema field names are allowed.

## Validation
A bootstrap is healthy only if a complete novice can initialize from the LastWarAI.com one-line instruction when web access exists, or from the standalone bootstrap when it does not, decline cloud storage, and still receive phased onboarding and full advisory behavior. Remote distribution must verify the first-party locator, live-ref/exact-commit handoff, release identity/version parity with `releases/LATEST.json`, and independence from third-party shorteners. Release validation must also prove that `refresh engine` remains present with canonical-update/local-state-preservation semantics across both bootstrap forms and the release bootstrap module.
