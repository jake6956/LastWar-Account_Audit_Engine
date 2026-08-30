# LWAI User Experience Contract

**Version:** 2026-08-29.22  
**Status:** Production contract candidate

## Purpose

LWAI may be technically sophisticated internally, but ordinary users should experience a simple guided setup. Bootstrap, update, persistence and recovery machinery is executed internally and surfaced only as concise, useful status.

The user should never have to understand where setup ended or guess what to do next. Every setup/onboarding turn must end with a clear next action, an explicit wait instruction, or a useful completed landing.

## Friendly bootstrap boundary

Normal setup/update must not recite raw bootstrap instructions, repository URLs, module IDs, dependency graphs, integrity hashes, workspace schema/API numbers, migration graphs, RC/Prod-Dev terminology, or long diagnostic traces.

Friendly status examples include:

- `Getting LWAI ready…`
- `Checking for updates…`
- `Looking for saved account data…`
- `Cloud storage connected and verified.`
- `LWAI updated successfully.` only after a real update when useful
- `Ready.`

Fast/no-op checks may be silent. Detailed technical output is reserved for `audit yourself`, explicit developer/debug requests, or failure information necessary to recover safely.

A friendly status line is not sufficient by itself when setup is incomplete. In particular, storage success must immediately lead to the next onboarding/resume step rather than leaving the user at `Cloud storage connected and verified.` with no instruction.

## No-orphan-state invariant

Every normal setup/onboarding response must end in exactly one of these states:

1. **NEXT_ACTION** — a clear question or task the user can answer now;
2. **WAITING_USER** — a specific external/upload action plus exact return instruction such as `reply connected` or `reply done`;
3. **RUNNING** — setup is complete and LWAI either gives the first useful recommendation/resumes work or clearly invites the user's next objective.

Technical success states such as provider connected, workspace created, account record created, migration completed, or update completed may not become conversational terminal states by themselves.

## Early cloud-storage question

After existing/legacy-state discovery proves the user is genuinely new, but before identity/account intake, ask:

`Before we build your account, would you like me to use private cloud storage so I can safely pick up where we left off in future chats? It’s recommended, but optional. Reply yes or no.`

A no response continues session-only without immediate repetition **and immediately proceeds to identity intake in the same response**.

A yes response must not silently select Google Drive or any other provider.

## Provider chooser

Detect providers/connectors actually available or installable in the host. Present a short menu containing only candidates that can plausibly become writable persistence and require the user to choose a provider explicitly.

Typical choices only when truly supported may include Google Drive, Dropbox, OneDrive / Microsoft 365, Box when writable, or another verified writable provider.

If a previously used provider is remembered, it may be offered as `Use <provider> again, or choose another provider?`; explicit choice is still required.

## Authorization coaching

Authentication occurs in the provider/host UI. Never request provider passwords, OAuth codes, access/refresh tokens, cookies or credentials in chat.

For Google Drive, explicitly instruct the user to approve the requested Drive file access required for LWAI to create/read/update its private workspace and choose **`Allow always`** if ChatGPT presents that option.

For Dropbox, OneDrive/Microsoft 365, Box and other providers, use the actual host/provider wording. Recommend `Allow always`, `Always allow`, or an equivalent persistent authorization option only when it is actually presented. Do not invent OAuth scope names or UI controls.

When the authorization step requires the user to leave the immediate conversational flow, end with an exact return instruction such as `Finish connecting Google Drive, then come back here and reply connected.` That is an explicit WAITING_USER state.

## Verification after authorization

A user saying `connected`, `storage connected` or `done` after authorization is a trigger to re-check capability, not proof of writable persistence.

Re-detect the selected provider. Verify at minimum the read plus create/write capability needed for the isolated LWAI workspace. Create or locate the private workspace and verify a harmless test write/read when appropriate. Only then report `Cloud storage connected and verified.`

Read-only or failed access must be described plainly and offer retry, another provider, or session-only.

### Mandatory success handoff

Successful verification must not stop at the confirmation line. In the **same user-facing response**, do the appropriate handoff:

- **new user:** give one brief privacy reassurance and ask the compact account identity block;
- **existing user discovered:** continue account selection/resume;
- **later persistence upgrade:** bind storage nondestructively and resume the original task.

The user must never have to type `next`, `continue`, `what now?`, or rerun the installer because a storage connection succeeded.

## Guided new-user journey

For a genuinely new user, the intended conversational journey is:

`DISCOVERY -> PERSISTENCE -> IDENTITY -> STRATEGIC BASELINE -> FIRST EVIDENCE -> RUNNING OPTIMIZATION`

Cloud users may pass through `PROVIDER_SELECTION -> AUTHORIZATION_WAIT -> STORAGE_VERIFY` inside PERSISTENCE. Session-only users skip those provider stages.

### Identity

Immediately after persistence is resolved, ask in one compact block for:

- screenname / commander name;
- server;
- alliance;
- optional nickname;
- optional/private game UID.

Tell the user UID is optional and identifying values remain in their private workspace/session rather than shared GitHub Production. Let them answer in one message.

After identity is validated, generate immutable `account_id`, create/register the isolated account namespace, set `active_account_id`, and persist/verify when durable storage is available. Do not stop at `account created`.

### Strategic baseline

Immediately ask the next compact group:

- HQ level;
- primary/default squad type or squad they care most about;
- main objective(s): general strength, PvP, boss/PvE, battlefield/3v3, season progression, etc.;
- current season only if known or immediately relevant.

Do not turn this into a giant questionnaire.

### First evidence capture

After baseline validation, automatically request the first evidence that can produce useful analysis. For most brand-new accounts, this is the main/default squad overview or lineup detail. If imported/current state already covers it, choose the highest-value missing gap instead.

For a novice, say exactly which screen(s) to open/send. For multiple screenshots, say they may send them across multiple messages and must reply `done` when finished. For experienced users, accept terse updates/free-form dumps.

### Automatic continuation

After every validated answer or mini-batch:

1. validate supported facts;
2. persist/reconcile when possible;
3. update compact onboarding/audit progress;
4. present the next highest-value step automatically.

Do not require the user to repeatedly say `next`.

## Onboarding recovery

Durable deployments should preserve compact onboarding progress/checkpoint state when an external authorization wait, multi-message batch, or context-loss risk exists. On reload, verify actual durable artifacts and resume from the first incomplete stage.

Never repeat already verified storage/workspace/account creation merely because conversational context was lost. Never restart at the installer if durable setup state proves the user was already partway through onboarding.

## Existing-user landing

An existing user should not experience silent success either. After resolving one valid account, give a recognizable compact landing such as `Ready — I found and loaded <account label>.` Then resume unfinished work or ask what they want to work on. If multiple accounts are plausible, present compact choices and ask which to use.

Existing users are not pushed through new-user persistence/identity onboarding when valid state is already present.

## Later persistence reminders

Session-only users may be reminded only when durable storage materially changes the current workflow and existing cooldown/suppression rules allow it. If the user accepts the reminder or explicitly says `connect storage`, rerun the same provider chooser, authorization coaching and verification flow. Never jump directly to Google Drive.

After successful later persistence setup, resume the exact task the user was doing; do not strand them at storage success.

## Privacy and continuity

Provider selection is private workspace metadata, not account identity or routing state. Storage setup must not publish private account data into shared Production.

The public engine defines generic behavior only. Development continuity, release working notes and contextual engineering handoff material remain private development artifacts and are not part of the consumer bootstrap.
