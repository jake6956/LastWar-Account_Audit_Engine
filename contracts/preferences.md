# Preferences & Personalized UX Contract

Version: 2026-08-31.32

## Purpose
LWAI should become easier to work with as it learns how a player prefers to interact, without building an invasive profile or confusing preferences with account facts. The personalization layer is user-owned private state.

## Scope
Three preference scopes exist:
- **WORKSPACE** — applies across the user's LWAI accounts, such as response style, verbosity, capture cadence, formatting, and proactive-next-step behavior.
- **ACCOUNT** — applies only to one immutable `account_id`, such as strategic emphasis, squad priorities, event-timing preferences, and account-specific optimization choices.
- **SESSION** — ephemeral only; used for session-only deployments or explicitly temporary requests.

Durable WORKSPACE/ACCOUNT preferences exist only in the user's selected personal provider and dedicated LWAI workspace. Session-only deployments must not claim cross-chat persistence.

## Human-readable notebook
Provider-neutral logical artifacts are:
- workspace `Preferences.md` or equivalent;
- `accounts/<account_id>/Preferences.md` or equivalent.

Structured providers may use records/tables internally, but the user must be able to inspect a human-readable preference view. File providers should use readable Markdown when practical.

## Minimum preference record
A durable record should include:
`preference_id/key`, `scope`, `category`, `value`, `source_type`, `confidence`, `status`, `first_seen`, `last_seen`, `last_confirmed` when applicable, and concise `notes`.

Allowed source classes include explicit user statements, repeated low-risk behavior, tentative inference, and imported user artifacts. Status distinguishes active/tentative/superseded/revoked.

## Learning policy
- Explicit reusable user instructions are stored at high confidence in the correct scope unless clearly temporary.
- Repeated low-risk interaction choices may produce a tentative preference.
- Consequential or sensitive preferences must not be inferred from behavior alone. Spending willingness/budget, privacy/permission choices, destructive actions and irreversible strategic commitments require explicit user direction.
- Do not store one-off mood, jokes, incidental wording, full transcripts, hidden chain-of-thought, or unrelated biography.
- A user complaint can become local tool-feedback preference only to the extent it should change that user's future LWAI experience.
- Consumer feedback/preferences are never automatically transmitted to the maintainer, GitHub, Gold Assets or another user.

## Precedence
Current explicit instruction > latest explicit ACCOUNT preference > latest explicit WORKSPACE preference > tentative preference > LWAI default.

Account scope overrides workspace scope only for the active account. A new explicit correction supersedes older conflict immediately.

## Application boundaries
Preferences may change response shape, question sequencing, capture style, proactive suggestions, and selection among strategically valid options.

Preferences never override:
- direct/current/official game evidence;
- epistemic-integrity requirements;
- privacy/workspace isolation/credentials rules;
- account isolation;
- safety/recovery contracts;
- explicit current user intent.

If following a preference would materially worsen account value, LWAI should state the tradeoff and recommend the stronger option rather than blindly obeying the stored default.

## Guidance proficiency
`NEW`, `LEARNING`, `COMFORTABLE`, and `EXPERT` remain separate from preferences. Proficiency describes how much procedural hand-holding is normally useful. Preferences describe how this particular user wants the product to behave.

## User control
Natural language must support viewing, remembering, changing, re-scoping, forgetting, resetting and exporting preferences. Equivalent phrases are valid.

A preference list should be concise, grouped by WORKSPACE and active ACCOUNT, and identify tentative items when that matters.

## Durability and recovery
A single preference change is normally a small canonical write and does not require a dedicated Runtime Checkpoint. Verify before retry when an interrupted write is ambiguous. Preference-state loss may reduce personalization but must never corrupt canonical account/game facts.

## Privacy
Preferences and local tool feedback are PRIVATE LOCAL STATE. Actual consumer values never belong in public Production, the maintainer's Drive, another user's provider workspace, or shared reusable knowledge.

## Regression requirements
Production must prove:
- cloud-connected preference persistence;
- honest session-only ephemerality;
- explicit-over-inferred precedence;
- account-scope isolation;
- evidence/privacy/safety dominance over preferences;
- user inspect/change/revoke/reset controls;
- no automatic publication of private feedback.
