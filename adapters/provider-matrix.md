# Storage Provider Matrix

This matrix describes default adapter behavior. Runtime capability detection always wins over static assumptions.

| Provider | Preferred structured state | Contracts/docs | Assets | Canonical writable? | Rule |
|---|---|---|---|---|---|
| Google Drive | Google Sheets when native read/write actions exist | Google Docs | Drive files/folders | Yes when write actions exist | Reference full-workspace adapter |
| Dropbox | JSON/CSV unless true workbook semantics exist | Markdown/TXT/JSON | Normal files | Capability-detect | Do not pretend file storage is a spreadsheet engine |
| Box | None if connector is search/reference only | Reference-only unless writes exist | Reference files | Not assumed | Use another writable provider if write scope is absent |
| OneDrive / Microsoft 365 | Excel Online/XLSX only if actual workbook read/write exists | Word/Markdown/TXT | OneDrive files | Capability-detect | Brand name does not imply workbook semantics |
| Generic writable cloud | Strongest actual structured store; otherwise JSON/CSV | Markdown/TXT/JSON | Files | Capability-detect | Preserve logical schema and audit metadata |
| No cloud | Conversation + exported snapshots | Plain text exports | User uploads | No | Continue fully; never block onboarding |

## Required adapter behaviors
- isolate LWAI writes from unrelated user files;
- preserve logical domains even if physical storage differs;
- preserve source/confidence/timestamps/IDs;
- maintain Change Log and Corrections continuity;
- survive disconnect without corrupting local state;
- support provider-neutral export before migration;
- never overwrite local state during engine refresh.
