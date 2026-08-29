# LWAI Architecture

## Hub and spoke

### Hub: GitHub Production engineering
GitHub holds sanitized, version-controlled engine material only. It is the engineering source for Production, not a player's live database.

### Spokes: private player deployments
Each player's account state lives in their chosen local persistence environment (Google Drive/Sheets in the reference implementation, or a capability-appropriate alternative). Conversation is an interface/cache, not durable authority when a canonical store exists.

### Distribution edge
The stable consumer-facing bootstrap is intentionally simple:

https://docs.google.com/document/d/1Mhg8YXX9jaZJVry5ZZ6_5d-xbE7A4A0tnfQVgFI2WC8/edit

The GitHub source counterpart is:

https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt

The Google Doc is the easiest install surface; GitHub is the production engineering/source-control hub.

## Runtime layers
1. **Engine layer** — generic sanitized rules, schemas, adapters, playbooks, commands and health checks.
2. **Local state layer** — player facts, corrections, preferences, resources, screenshots, battles, provider metadata.
3. **Hot Cache** — compact active working state derived from canonical local storage.
4. **Audit/history** — Change Log, snapshots, Mechanics Registry and empirical Battle Log.
5. **Gold Assets** — optional versioned sanitized shared references.

## Self-healing loop
Input -> parse supported facts -> compare canonical state -> reconcile by evidence/freshness/confidence -> log material change -> invalidate stale derived recommendations -> recompute affected resource lanes -> refresh Hot Cache -> answer concisely.

## Release loop
Prod-Dev private experimentation -> documentation-as-code update -> sanitized candidate -> release checks -> versioned Production in GitHub -> stable public bootstrap mirror update.

## Design goal
Context-window loss should be an inconvenience, not data loss. A fresh conversation can `reload LWAI` from durable local state, while `refresh engine` updates the generic Production layer without overwriting player data.
