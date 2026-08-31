# LWAI Public Beta Testing

LWAI is in controlled external testing against the current live Production release. Do not use a hard-coded historical version or legacy installer as the beta baseline; resolve the current public configuration when the test begins.

## Install

Paste this into a fresh AI conversation:

> Set up Last War optimization using the instructions at https://lastwarai.com

For best results, use a higher reasoning/thinking setting when the host offers one.

LastWarAI.com returns the complete sanitized current configuration in one response after resolving the live GitHub Production commit server-side. A tester should not have to retrieve GitHub JSON, locate a SHA, or follow a second engine URL.

## How to test

Use LWAI normally. Do not coach the assistant through the expected internal workflow unless it gets stuck; natural first-run behavior is part of the test.

Useful test paths include:

- brand-new user choosing session-only;
- brand-new user choosing cloud persistence and an actually supported writable provider;
- verify the first persistence question is short and benefit-oriented rather than a security manifesto;
- after provider selection, verify one compact workspace-only/no-password reassurance appears before authorization;
- existing schema-2.1/2.2 or legacy single-account LWAI user upgrading from an earlier export/workspace;
- current LWAI user resuming an existing persistent workspace;
- multi-account switching, archive/restore and terse updates;
- long screenshot or document-bundle audits, including interruption/reload during a declared `done` upload boundary;
- engine refresh/reload after useful account state already exists;
- immediate post-release LastWarAI.com verification to detect stale public edge content;
- another AI/model or device with different web/connector capabilities.

## What good behavior looks like

LWAI should install from the one-line instruction, receive one transparent complete public configuration, discover supported existing state before onboarding, preserve/migrate supported state, avoid redundant questions, keep accounts isolated, preserve declared upload boundaries, and degrade honestly when a capability is unavailable.

For a genuine new user, cloud persistence is recommended but optional. The initial choice should be simple. If cloud is selected, the user chooses the provider explicitly; Google Drive may be recommended when genuinely available, but it is never silently selected. The workspace-security contract remains strict internally while the user-facing authorization reassurance stays concise.

A supported older workspace that cannot complete migration must remain untouched and must not fall through to new-user onboarding.

The public GitHub engine must never contain a tester's private account state.

## Reporting a problem

Use the **Beta feedback** GitHub issue template when practical. Include the Production version reported by the live configuration, broad environment/capability information, whether this was a new or existing account, what you expected, what happened, and the smallest safe reproduction sequence.

**Do not post private account data to public GitHub issues.** Do not include game UID, screenname, alliance/server identity, screenshots, balances, battle history, private cloud file IDs/paths, account database contents, conversation/session references, passwords, cookies, session tokens or authentication captures.

If reproducing a problem requires private data, describe the failure generically instead of publishing the data.

## Current beta baseline

At test time, record:

- the live `X-LWAI-Commit` returned by LastWarAI.com;
- the engine version reported by that configuration;
- Engine API and workspace schema;
- host/model/device and relevant web/storage capabilities.

The public engine must report `SANITIZED: YES` and `ACCOUNT STATE INCLUDED: NO`. Historical release notes are context only; they are not the current test authority.