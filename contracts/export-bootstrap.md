# Export & Bootstrap Contract

Version: 2026-08-31.34

## Purpose
Define exactly what `export yourself` means, support one-line public installation, and keep fresh LWAI setup turnkey while degrading safely when tools/connectors are unavailable.

## Preferred end-user install
The default public install experience is one line:

`Set up Last War optimization using the instructions at https://lastwarai.com`

`https://lastwarai.com` is the permanent first-party public configuration endpoint. For a fresh install, Cloudflare resolves the live GitHub Production `main` commit server-side, retrieves `engine/BOOTSTRAP_FULL.txt` from that exact immutable commit, adapts only the already-completed generic Stage-0 discovery section, and returns the complete sanitized configuration in the same response.

The user's AI is not expected to fetch a second engine URL, retrieve GitHub JSON, locate a commit SHA, or assemble the modular runtime manually during normal first installation.

GitHub `main` remains the underlying Production source/version authority. The public response identifies the resolved commit and explicitly permits independent verification. The previously circulated `https://tinyurl.com/2yxf7f5x` is retained only as a legacy compatibility alias. New sharing uses LastWarAI.com. A third-party shortener, preview/interstitial, redirect, repository cache, mutable raw `main`, search index or model memory is never source/version authority.

## First-party installation contract
When a user explicitly asks to set up/install/initialize LWAI using the public installer URL:
1. retrieve LastWarAI.com rather than asking the user to paste a larger bootstrap;
2. consume the returned complete transparent sanitized configuration;
3. verify its declared Production/privacy identity and resolved GitHub commit when the host supports verification;
4. execute startup behavior rather than stopping at a documentation summary;
5. discover/resume supported existing LWAI state before genuine new-user onboarding.

The initial public response requires no second GitHub or engine fetch. Direct GitHub exact-commit resolution remains valid for runtime update/recovery, independent verification, and manual/direct modular operation.

## Direct/modular and fallback order
For direct/recovery operation when the first-party complete response is not available:
1. resolve canonical GitHub live `main` to a valid commit SHA C;
2. pin all candidate reads to C;
3. use `engine/BOOTSTRAP.txt` for the <=4 KiB direct/modular Stage-1 loader and MANIFEST-driven modules;
4. use exact-C `engine/BOOTSTRAP_FULL.txt` as the complete standalone fallback;
5. use last-known-good compatible local ENGINE when current Production cannot be safely resolved;
6. manual full-bootstrap transfer is the final no-remote-retrieval path.

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
The single-file engine export must contain: version/purpose; evidence hierarchy; state ledger; source-vs-derived separation; self-healing reconciliation; shared gear/preset model; independent resource lanes; marginal ROI; research dependencies; all domain playbooks; formation/orientation discipline; screenshot batching; empirical battle loop; phased onboarding; optional cloud persistence; cloud-neutral schema; reload/staleness; capability fallbacks; command vocabulary; health/regression tests; sanitization; upstream/local-state separation; provider adapters; optional Runtime Session provenance rules; Gold Assets rules; release/update behavior; public-install behavior; limitations; fresh-start behavior.

The standalone export must preserve the current UX contract: a genuinely new user gets one compact benefit-oriented persistence yes/no; if cloud is chosen, explicit provider selection precedes one compact workspace-only/no-password reassurance and provider authorization. The exhaustive internal workspace boundary remains authoritative but is not dumped into the initial choice.

## Runtime-session provenance export boundary
Sanitized engine exports may define the generic `runtime_session_id` / optional `host_platform` / optional `host_session_ref` schema and rules, but must never contain an actual consumer Runtime Session row, actual host conversation/session reference, conversation URL, or private provenance mapping. Host references are private observability metadata only and are never required for installation, onboarding, account recovery or optimization.

Do not instruct users to create ChatGPT shared links or retrieve conversation GUIDs to install or use LWAI. `export my account snapshot` or a private full recovery package may include compact runtime-session provenance only when useful for that user's recovery/audit history; it remains separate from the sanitized engine artifact and must never be promoted to shared Production.

## Capability detection
Never assume the new deployment has the same tools as the reference environment. Detect web/current research, image understanding, cloud connectors and write scope, spreadsheet/document writes, file export and automations when relevant.

Fallbacks:
- no cloud -> chat + periodic exports;
- read-only cloud -> reference only;
- writable files without sheets -> JSON/CSV/Markdown/TXT;
- no web -> use a manually supplied standalone bootstrap and mark volatile mechanics UNVERIFIED;
- no automation -> manual/return-time preflight only;
- no image understanding -> minimal transcription request.

## Source vs derived
Recommendations and calculations are derived state. They never become evidence for canonical account facts. Runtime/host session provenance is metadata and likewise never becomes game evidence.

## State transaction
For each update: parse supported facts -> compare canonical state -> update unambiguous facts with timestamp/source/confidence -> mark ambiguity instead of overwriting higher-confidence data -> append material changes with optional private `runtime_session_id` correlation -> invalidate/recompute dependencies -> refresh active cache -> answer naturally.

## Staleness / reload
Persistent workspace is canonical when available; conversation is cache. `reload LWAI` reads operating instructions, account context/recovery state, Hot Cache, Corrections, State Health, relevant domain state and recent material Change Log entries, reconciles, then resumes. Consequential decisions trigger the smallest relevant preflight automatically. Optional host-session provenance never changes active-account selection or recovery ordering.

## Distribution privacy and provenance
The first-party installer keeps the normal public prompt clean while still identifying public GitHub provenance and the exact resolved Production commit. This is not anonymity. Public provenance must remain truthful and discoverable; never falsify source identity.

## Sanitization
Remove player/account names, alliance/server identifiers, exact powers/inventories/current targets, personal spending history, diplomacy/politics, private screenshots, account-specific corrections, private cloud IDs/URLs, actual Runtime Session/host-session references, actual checkpoint/journal rows and auth details. Intentional public Production/Gold Asset/install endpoints and generic schema field names are allowed.

## Validation
A bootstrap is healthy only if a complete novice can initialize from the LastWarAI.com one-line instruction with one complete public configuration response, or from the standalone bootstrap when remote retrieval is unavailable, decline cloud storage, and still receive phased onboarding and full advisory behavior. Release validation must also prove immediate public SHA parity with canonical GitHub Production, compact staged persistence/security UX, stable `refresh engine` semantics, local-state preservation, and independence from third-party shorteners.
