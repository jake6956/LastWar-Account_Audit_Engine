# Turnkey Deployment Guide

## Fastest path for a player
1. Open the stable Production bootstrap: https://docs.google.com/document/d/1Mhg8YXX9jaZJVry5ZZ6_5d-xbE7A4A0tnfQVgFI2WC8/edit
2. Copy the entire document into a fresh ChatGPT conversation.
3. Switch reasoning/thinking to **HIGH** if the product exposes that control.
4. Follow Phase 1 onboarding.
5. Optionally connect a supported cloud provider when LWAI recommends durable persistence.

The player does not need GitHub knowledge.

## If cloud persistence is accepted
The deployment capability-detects the provider, creates an isolated LWAI workspace, maps the provider-neutral schema onto the strongest supported structured storage and never touches unrelated files.

## Engine updates
A player may say `refresh engine` / `check for LWAI updates`. The deployment preserves all local account state, checks the Production update source, applies only generic Production engine changes, follows migrations if required and runs health checks afterward.

## Recovery
- `reload LWAI`: reconstruct working context from durable local state.
- `export my account snapshot`: private current-state recovery export.
- `export yourself`: sanitized generic engine only.
- `export full recovery package`: separate engine + private snapshot + manifest.

## Operator / maintainer path
Develop against a private Prod-Dev deployment, record every material change in relevant canonical documentation, sanitize, freeze a Release Candidate, run release gates, commit/publish Production to GitHub, then update the stable public bootstrap mirror in place.
