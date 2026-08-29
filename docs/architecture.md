# LWAI Architecture

## Hub and spoke

### Hub: GitHub Production engineering
GitHub holds sanitized, version-controlled engine material only. It is the engineering source for Production, not a player's live database.

### Spokes: private player deployments
Each player's account state lives in their chosen local persistence environment (Google Drive/Sheets in the reference implementation, or a capability-appropriate alternative). Conversation is an interface/cache, not durable authority when a canonical store exists.

### Distribution edge
Human installation is intentionally tiny even though the runtime engine is large. The preferred public entrypoint is:

`Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x`

The assistant retrieves the full Production bootstrap. The TinyURL is transport convenience and semi-anonymous presentation only; it is not source authority. The canonical sources are:

- https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json
- https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt

The stable Google Doc remains a secondary/legacy mirror when readable. Manual multi-page paste is the final fallback when remote retrieval is unavailable.

## Remote bootstrap trust flow
User one-line instruction -> explicit authorization to retrieve URL -> follow alias -> verify expected sanitized LWAI Production identity -> consume full bootstrap -> execute STARTUP BEHAVIOR.

If the alias target is unexpected, bypass it and fetch the canonical GitHub Production source. Routine `refresh engine` also uses direct GitHub sources rather than the shortener.

## Runtime layers
1. **Engine layer** — generic sanitized rules, schemas, adapters, playbooks, commands and health checks.
2. **Local state layer** — player facts, corrections, preferences, resources, screenshots, battles, provider metadata.
3. **Hot Cache** — compact active working state derived from canonical local storage.
4. **Audit/history** — Change Log, snapshots, Mechanics Registry and empirical Battle Log.
5. **Gold Assets** — optional versioned sanitized shared references.

## Self-healing loop
Input -> parse supported facts -> compare canonical state -> reconcile by evidence/freshness/confidence -> log material change -> invalidate stale derived recommendations -> recompute affected resource lanes -> refresh Hot Cache -> answer concisely.

## Release loop
Prod-Dev private experimentation -> documentation-as-code update -> sanitized candidate -> GitHub RC branch/PR -> CI + private release gates -> merge exact validated candidate to Production -> verify raw Production/version manifest -> verify short alias -> synchronize secondary archives/mirrors.

## Privacy boundary
The visible installer intentionally omits the maintainer/repository handle, reducing casual attribution/exposure during community sharing. This is not cryptographic anonymity: resolving the alias exposes public GitHub provenance. Private player state never flows into the shared hub.

## Design goal
Context-window loss should be an inconvenience, not data loss, and installation friction should be nearly zero. A fresh conversation can initialize from one line, `reload LWAI` from durable local state, and `refresh engine` from direct GitHub Production without overwriting player data.
