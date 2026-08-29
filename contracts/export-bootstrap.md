# Export & Bootstrap Contract

Version: 2026-08-29.7

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

## Mandatory bootstrap content
The single-file engine export must contain: version/purpose; HIGH-thinking onboarding callout; thin-interface/thick-engine model; evidence hierarchy; state ledger; source-vs-derived separation; self-healing reconciliation; shared gear/preset model; independent resource lanes; marginal ROI; research dependencies; all domain playbooks; formation/orientation discipline; screenshot batching; empirical battle loop; phased onboarding; optional cloud persistence; cloud-neutral schema; Hot Cache/reload/staleness; capability fallbacks; optional automation behavior; command vocabulary; health/regression tests; sanitization; upstream/local-state separation; provider adapters; Gold Assets rules; release/update behavior; remote-bootstrap behavior; limitations; fresh-start behavior.

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
Recommendations and calculations are derived state. They never become evidence for canonical account facts.

## State transaction
For each update: parse supported facts -> compare canonical state -> update unambiguous facts with timestamp/source/confidence -> mark ambiguity instead of overwriting higher-confidence data -> append material changes -> invalidate/recompute dependencies -> refresh active cache -> answer naturally.

## Staleness / reload
Persistent workspace is canonical when available; conversation is cache. `reload LWAI` reads operating instructions, Hot Cache, Corrections, State Health, relevant domain state and recent material Change Log entries, reconciles, then resumes. Consequential decisions trigger the smallest relevant preflight automatically.

## Distribution privacy
Prefer the neutral short alias in user-facing install text so the maintainer/repository owner is not exposed casually in the visible one-liner. This is not true anonymity: resolving the alias exposes the public GitHub provenance. Never falsify source identity.

## Sanitization
Remove player/account names, alliance/server identifiers, exact powers/inventories/current targets, personal spending history, diplomacy/politics, private screenshots, account-specific corrections, private cloud IDs/URLs and auth details. Intentional public Production/Gold Asset endpoints are allowed.

## Validation
A bootstrap is healthy only if a complete novice can initialize from the one-line remote instruction when web access exists, or from the standalone bootstrap when it does not, decline cloud storage, and still receive phased onboarding and full advisory behavior. Remote distribution additionally requires short-link resolution to the canonical raw Production bootstrap and version parity with `releases/LATEST.json`.
