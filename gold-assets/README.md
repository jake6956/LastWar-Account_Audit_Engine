# LWAI Gold Assets

Gold Assets are sanitized, reusable, production-qualified reference artifacts shared across deployments without touching player-local state.

Examples:
- canonical diagrams/infographics;
- verified reference datasets;
- reusable templates;
- provider-neutral lookup data;
- stable images or reference documents that improve onboarding/analysis.

## Asset qualification
Every production asset must have:
- stable `asset_id`;
- version;
- type/format;
- source/provenance;
- validation status/date;
- compatibility/engine range;
- public readable location if referenced by consumer deployments;
- supersedes relationship if replacing an older asset;
- explicit statement that it contains no player-private state.

## Boundaries
Never place private screenshots, battle reports, inventories, account-specific derived artifacts, private Drive IDs, credentials or local corrections into Gold Assets.

A consumer may refresh Gold Assets independently from its local account state. Asset refresh must never replace local screenshots, notes, battle history or user-specific analysis.

Large binaries may live in a stable public object/file store while GitHub holds the manifest/provenance. Text-friendly production assets may live directly in this directory.

## Approved public source registry

`gold-assets/sources/registry.json` records public research entrypoints and article-level trust classification. Approval is permission to consult a source, not automatic adoption of every page or player comment as authoritative. Publisher announcements, player-contributed guides and comments retain distinct provenance tiers. A user account's canonical private state is never overwritten from this registry.
