# Production Changelog

## 2026-08-29.6

- Activated GitHub as the authoritative sanitized Production engineering/source-control hub.
- Preserved each player's cloud/chat workspace as the private runtime spoke; no local account state flows into the public repository.
- Added stable machine-readable `releases/LATEST.json` and raw `engine/BOOTSTRAP.txt` update sources.
- Kept the stable Google Doc as the lowest-friction consumer distribution mirror and fallback update source.
- Formalized consumer engine refresh order: preserve local state -> check GitHub Production manifest -> apply migrations if required -> refresh generic engine layer -> run health checks; fall back to Google Doc or local last-known-good engine.
- Added repository schemas, storage adapter matrix, migration contract, release gates, security boundary, contribution rules and architecture/deployment documentation.
- Added GitHub Actions static Production validation.
- Added explicit hub-and-spoke synchronization/version parity as a release health check.

## 2026-08-29.5

- Compiled Production bootstrap made self-contained.
- Added provider capability abstraction and provider-neutral logical schema.
- Added local-state vs upstream-engine separation.
- Added Gold Assets concept for sanitized shared references.
- Added documentation-as-code release gate.
- Added stable public Production update endpoint.
- Added graceful degradation for cloud/web/image/automation differences.
- Added formal Prod-Dev -> RC -> Production release model.
- Imported the known-good Production engine into the GitHub engineering hub.

## 2026-08-29.4

- Added lossless domain playbooks for screenshots, gear/Ore, Skill Medals, EW, hero shards/WoH, squad-slot tech, counter/meta modeling, formations, Drone/chips, Decorations, Profession/global bonuses, research, stores/paid value, season systems and Battlefield-vs-dueling behavior.
- Formalized recommendation contract and noob-safe onboarding.

## 2026-08-29.3

- Formalized `export yourself`, account snapshot and full recovery package semantics.
- Added capability discovery, cloud-neutral workspace schema, state transaction protocol, reload/staleness behavior, command vocabulary and health tests.

## Earlier Prod-Dev evolution

- Established thin-interface/thick-engine interaction.
- Added rolling Hot Cache, Change Log, Corrections, State Health and staleness model.
- Added external durable-memory architecture and self-healing reconciliation.
