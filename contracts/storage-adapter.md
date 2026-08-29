# Storage Adapter Contract

Version: 2026-08-29.5

LWAI maps one provider-neutral logical persistence model onto whatever storage capabilities a deployment actually has. Choose by verified capability, not brand assumptions.

## Core rules
1. Cloud persistence is strongly recommended but optional.
2. Writable providers are isolated in a dedicated LWAI workspace/folder; never modify unrelated files.
3. Logical schema is invariant across providers; physical file types may differ.
4. Do not claim a provider is writable, structured, or spreadsheet-capable until connector actions prove it.
5. Local account state survives upstream engine upgrades.
6. Provider migrations preserve canonical state, Change Log, Corrections and local configuration.

## Google Drive
When native Google Sheets actions exist, use Sheets for structured canonical state, Docs for canon/contracts/readmes/manifests and isolated Drive folders for assets. This is the reference adapter.

## Dropbox
Treat as writable file storage unless real workbook semantics are exposed. Prefer JSON/CSV for structured state and Markdown/TXT/JSON for contracts. Use XLSX only when workbook structure can be reliably read and updated.

## Box
Capability-detect. Search/reference-only Box is not canonical writable persistence. If write actions later exist, prefer provider-neutral JSON/CSV/Markdown/TXT unless real spreadsheet semantics are proven.

## OneDrive / Microsoft 365
Do not assume availability or Excel semantics. If a future connector exposes actual Excel workbook read/write operations, prefer Excel Online/XLSX for tabular state and Word/Markdown/TXT for contracts. Generic file storage alone uses JSON/CSV/Markdown/TXT.

## Generic writable cloud
Use the strongest reliable structured store actually exposed; otherwise store the logical schema in versioned JSON/CSV plus Markdown/TXT.

## Migration
Snapshot current canonical state and engine metadata -> export provider-neutral representation -> import -> validate entity counts, IDs, latest values, Corrections and Change Log continuity -> switch canonical provider only after reconciliation. Do not destroy the old canonical store before validation.

## GitHub role
GitHub is production engineering/source control, not live player state. Store sanitized bootstrap source, contracts, schemas, adapters, tests, migrations, releases and Gold Asset manifests here. Keep account facts, balances, screenshots, battle history, local corrections and provider credentials in each player’s private runtime workspace.
