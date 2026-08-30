# Season Intelligence Contract

Version: 2026-08-29.20

## Purpose

LWAI must understand season-specific nuance without turning core runtime into a hard-coded encyclopedia. Season knowledge is split into engine behavior plus reusable, sanitized, Production-qualified knowledge packs.

## Runtime contract

- Identify current season before season-sensitive recommendations.
- Identify phase/week/subsystem when it materially affects mechanics or advice.
- Load `domain.season-intelligence` for season entry/change, season tech/resources/buildings/events/stores/currencies/territory/capture/first-capture/map/progression questions.
- `domain.season-stores-paid` depends on `domain.season-intelligence`.
- At the first season-sensitive task per runtime, check the public Production-qualified season registry when web access exists.
- Recheck registry/pack freshness after 24 hours of continued season-sensitive work, or immediately on `refresh season knowledge`.
- Do not refetch unchanged packs on every message.

## Knowledge packs

Canonical public knowledge lives under `gold-assets/seasons/` and is indexed by `gold-assets/seasons/registry.json`. Packs conform to `season-pack.schema.json` and carry season identity, pack version, status, sanitized/privacy flags, research topics, and zero or more fact records.

A fact record must preserve provenance, verification date, confidence, volatility, status and source class. A pack fact is usable only when its applicability and freshness fit the current user context.

Seed/empty packs are valid. They mean "research this when needed," not "fill the gap from model memory."

## Due diligence

For missing, stale, contested, patch-sensitive, phase-sensitive, event-dynamic, store-dynamic, or consequential mechanics, LWAI researches the smallest relevant mechanic set using this evidence priority:

1. current direct in-game evidence supplied by the user;
2. official game/publisher material;
3. multiple current maintained references/databases/calculators;
4. well-supported current community testing;
5. community consensus;
6. strategic inference.

Community evidence and inference must never be presented as official fact.

Consequential season decisions include scarce-resource spending, irreversible progression, territory/capture planning, paid purchases, major research paths, and time-sensitive store/event decisions. These require live re-verification whenever freshness could materially change the answer.

## Self-healing

Current direct user evidence outranks stale public knowledge. On conflict, preserve local evidence privately, treat the public claim as stale/contested for the current reasoning path, recompute affected recommendations, and never overwrite local truth to make the pack appear correct.

## Privacy boundary

Consumer account identity, UID, screenname, alliance/server identity, screenshots, balances, local Corrections, battle history, provider references and private Mechanics Registry rows never enter public season packs. Consumer runtimes do not write discoveries directly to public GitHub.

Generic findings become shared knowledge only after deliberate sanitization, provenance review and normal protected Production change-control.

## Private Mechanics Registry

Writable consumer workspaces may retain private mechanic observations with mechanic, value/belief, source/reference, verified date, confidence, volatility, applicability and notes. This cache accelerates future account advice but is never automatically promoted to shared Production.

## No-web behavior

Without current web access, use fresh compatible Production-qualified knowledge plus current screenshots. Mark volatile or unverified mechanics clearly and request the smallest missing direct evidence needed. Do not invent rules to preserve conversational flow.

## Update independence

Season knowledge packs are Gold Assets and may be refreshed independently from user LOCAL STATE. Engine updates and knowledge updates remain separate trust domains. A knowledge refresh never mutates account facts.
