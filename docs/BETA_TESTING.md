# LWAI Public Beta Testing

LWAI Production `2026-08-29.15` is ready for controlled external beta testing.

## Install

Paste this into a fresh ChatGPT conversation:

> Set up Last War optimization using the instructions at https://tinyurl.com/2yxf7f5x

For best results, use a higher reasoning/thinking setting when the ChatGPT interface offers one.

## How to test

Use LWAI normally. Do not coach the assistant through the expected internal workflow unless it gets stuck; natural first-run behavior is part of the test.

Useful test paths include:

- brand-new user with no durable cloud storage;
- brand-new user with a supported writable cloud-storage connector;
- existing schema-2.1/2.2 or legacy single-account LWAI user upgrading from an earlier export/workspace;
- current LWAI user resuming an existing persistent workspace;
- multi-account switching, archive/restore and terse updates;
- long screenshot or document-bundle audits, including interruption/reload during a declared `done` upload boundary;
- engine refresh/reload after useful account state already exists;
- environments where the short-link body appears stale/cached while canonical GitHub Production is newer.

## What good behavior looks like

LWAI should install from the one-line instruction, re-check canonical GitHub Production, discover capabilities, preserve supported existing state, migrate supported older workspace schemas additively before normal domain work, avoid redundant onboarding, ask only for missing/ambiguous/materially stale information, keep accounts isolated, preserve declared upload boundaries, and degrade honestly when a capability is unavailable.

A supported older workspace that cannot complete migration must remain untouched and must not fall through to new-user onboarding.

The public GitHub engine must never contain a tester's private account state.

## Reporting a problem

Use the **Beta feedback** GitHub issue template when practical. Include the LWAI Production version, broad environment/capability information, whether this was a new or existing account, what you expected, what happened, and the smallest safe reproduction sequence.

**Do not post private account data to public GitHub issues.** Do not include game UID, screenname, alliance/server identity, screenshots, balances, battle history, private cloud file IDs/paths, account database contents, ChatGPT conversation/session references, passwords, cookies, session tokens or authentication captures.

If reproducing a problem requires private data, describe the failure generically instead of publishing the data.

## Current beta baseline

- Engine: `2026-08-29.15`
- Engine API: `1.0`
- Workspace schema: `2.3`
- Supported additive upgrade schemas: `2.1`, `2.2`
- Public engine: sanitized
- Public account state: none
