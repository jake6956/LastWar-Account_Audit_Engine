# Durability-First Evidence Ingestion Contract

Version: 2026-09-28.45

## Purpose
Make screenshots, direct account updates, terse corrections and completed evidence batches durable account-state transactions rather than answer-local context when verified writable persistence is active.

The governing invariant is:

**Task relevance must never determine persistence relevance.**

Transaction shorthand: **observe -> persist -> reconcile -> verify**.

A screenshot opened to answer one question may expose several clear supported account facts. The response may focus on the user's question, but the durable ingestion pass must independently harvest every supported fact that belongs to the active account.

## Trigger
Run the ingestion transaction for:
- current in-game screenshots supplied directly by the user;
- direct factual account updates such as a level, balance, unlock, skill, gear, research, squad or system-state change;
- completed direct/document/guided evidence batches;
- current user corrections that establish account state.

Do not require a special save/remember command.

## Harvest boundary
Before recommendation/output filtering, enumerate all clearly identifiable supported account-state observations in the supplied evidence.

Persist/reconcile an observation unless it is:
- ambiguous, unreadable or materially uncertain;
- decorative/non-account UI with no useful state meaning;
- transient with no useful historical/freshness value;
- already stored identically with adequate source/freshness/provenance for the same observation.

Do not invent a label for an ambiguous icon/value. Preserve ambiguity instead.

Screenshot/file bytes do not need permanent retention merely because structured facts were harvested.

## Evidence semantics
Current direct user/in-game evidence outranks older durable state for the same field.

Classify each accepted fact using existing state-freshness rules:
- INVARIANT / CORRECTION — persists until superseded/revoked;
- MONOTONIC — current direct evidence becomes current canonical state; older evidence remains history/minimum-known context where appropriate;
- VOLATILE — persist the value as a timestamped observation with source/confidence and normal freshness/expiry behavior. A volatile observation is never timeless merely because it was recently ingested.

Recommendations, inferences and calculated targets are not account evidence.

## Durable transaction
When verified writable durable storage is active:
1. resolve active_account_id before mutation;
2. harvest all supported observations independent of the user's current task focus;
3. classify source/confidence/freshness semantics;
4. establish a provider transaction when available, otherwise an account-scoped write-ahead/checkpoint boundary before the first non-atomic multi-surface write;
5. reconcile/write canonical domain facts;
6. append material Change Log/history;
7. update or invalidate affected Hot Cache entries;
8. update State Health/freshness metadata;
9. update applicable account/workspace last_updated metadata;
10. invalidate/recompute dependent recommendations only after canonical state is coherent;
11. verification-read the affected durable surfaces;
12. mark the transaction COMMITTED only after the intended durable end state is verified.

A direct-evidence transaction may touch one or many domain tabs/namespaces. Physical provider layout does not change the coherence requirement.

## Partial failure
A provider/tool success response is not proof that the full account-state transaction committed.

If canonical/history/cache/health/metadata writes or final verification are incomplete:
- do not report or internally classify the transaction as durably committed;
- preserve verified successful writes;
- mark the account-scoped transaction/checkpoint RECOVERY_REQUIRED when durable recovery metadata is supported;
- record the first unverified/pending surface;
- on reload/recovery inspect actual durable artifacts and resume from the first unverified action;
- never duplicate verified writes merely to make all surfaces look synchronized;
- never repair an ingestion failure by resetting/re-onboarding the account.

## Batch behavior
A declared multi-upload batch still honors WAITING_USER / done boundaries. Harvest/commit after the declared batch closes unless guided-capture rules intentionally commit verified mini-batches independently.

Terse single-message updates are first-class evidence and should commit promptly; they do not need a batch wrapper.

## Account isolation
All harvested facts and recovery metadata are scoped to the resolved active_account_id. Evidence for Account A must never update Account B merely because names, host-session references or current tasks resemble one another.

Cross-account comparisons remain read-only unless the user explicitly switches accounts.

## Reload behavior
A successful verified commit must survive reload/new runtime without requiring the same evidence again while its freshness remains adequate.

Reload reads durable canonical facts, freshness metadata, Hot Cache/State Health and unresolved ingestion recovery work using normal recovery-first ordering.

## Session-only / read-only behavior
Without verified writable storage, retain best-effort current-session state and answer normally, but do not claim durable persistence. Existing persistence-upgrade UX may be offered when the durability benefit is material.

## Privacy
Structured private account facts remain only in the user's selected private LWAI workspace or current session. No account values, screenshot content, account identifiers, provider-local references or actual ingestion/checkpoint rows enter shared GitHub Production.

Sanitized Production may contain this generic contract, schemas, tests and behavioral examples only.

## Release gates
Promotion requires deterministic regressions proving:
- multi-fact evidence persists all clear supported facts even when the user asks about only one;
- newer direct monotonic state supersedes stale durable state;
- volatile values retain observation metadata/freshness semantics;
- ambiguous observations do not receive invented labels;
- partial write/verification failure is RECOVERY_REQUIRED/incomplete rather than falsely COMMITTED;
- a successful transaction survives a fresh runtime/reload;
- account isolation holds;
- public artifacts remain sanitized;
- standalone fallback preserves the same invariant.
