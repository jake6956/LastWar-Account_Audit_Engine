# LWAI User Experience Contract

**Version:** 2026-08-29.19  
**Status:** Production contract candidate

## Purpose

LWAI may be technically sophisticated internally, but ordinary users should experience a simple guided setup. Bootstrap, update, persistence and recovery machinery is executed internally and surfaced only as concise, useful status.

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

## Early cloud-storage question

After existing/legacy-state discovery proves the user is genuinely new, but before identity/account intake, ask:

`Before we build your account, would you like me to use private cloud storage so I can safely pick up where we left off in future chats? It’s recommended, but optional. Reply yes or no.`

A no response continues session-only without immediate repetition.

A yes response must not silently select Google Drive or any other provider.

## Provider chooser

Detect providers/connectors actually available or installable in the host. Present a short menu containing only candidates that can plausibly become writable persistence and require the user to choose a provider explicitly.

Typical choices only when truly supported may include Google Drive, Dropbox, OneDrive / Microsoft 365, Box when writable, or another verified writable provider.

If a previously used provider is remembered, it may be offered as `Use <provider> again, or choose another provider?`; explicit choice is still required.

## Authorization coaching

Authentication occurs in the provider/host UI. Never request provider passwords, OAuth codes, access/refresh tokens, cookies or credentials in chat.

For Google Drive, explicitly instruct the user to approve the requested Drive file access required for LWAI to create/read/update its private workspace and choose `Allow always` if ChatGPT presents that option.

For Dropbox, OneDrive/Microsoft 365, Box and other providers, use the actual host/provider wording. Recommend `Allow always`, `Always allow`, or an equivalent persistent authorization option only when it is actually presented. Do not invent OAuth scope names or UI controls.

## Verification after authorization

A user saying `connected`, `storage connected` or `done` after authorization is a trigger to re-check capability, not proof of writable persistence.

Re-detect the selected provider. Verify at minimum the read plus create/write capability needed for the isolated LWAI workspace. Create or locate the private workspace and verify a harmless test write/read when appropriate. Only then report `Cloud storage connected and verified.`

Read-only or failed access must be described plainly and offer retry, another provider, or session-only.

## Later persistence reminders

Session-only users may be reminded only when durable storage materially changes the current workflow and existing cooldown/suppression rules allow it. If the user accepts the reminder or explicitly says `connect storage`, rerun the same provider chooser, authorization coaching and verification flow. Never jump directly to Google Drive.

## Privacy and continuity

Provider selection is private workspace metadata, not account identity or routing state. Storage setup must not publish private account data into shared Production.

The public engine defines generic behavior only. Development continuity, release working notes and contextual engineering handoff material remain private development artifacts and are not part of the consumer bootstrap.
