# Recovery Package Contract

Version: 2026-09-28.44

## Purpose
Define a deterministic, sanitized, multi-file LWAI recovery package that can reconstruct the modular runtime without depending on live remote retrieval. This package is the recovery counterpart to the normal manifest-driven runtime; it is not a second engine architecture and it is not current-version authority.

Production .44 is an additive transition release. LastWarAI.com continues serving the complete single-response BOOTSTRAP_FULL configuration exactly as before. The recovery package is introduced and tested in parallel; no public transport cutover occurs in this release.

## Core design
The existing `engine/BOOTSTRAP.txt` remains the one thin install/recovery kernel. Do not create a second bootstrap kernel with overlapping behavior.

A recovery package contains one exact sanitized engine snapshot:
- `engine/BOOTSTRAP.txt`;
- `engine/MANIFEST.json`;
- `releases/LATEST.json`;
- `releases/MIGRATIONS.json`;
- the current versioned release manifest;
- every module path registered in MANIFEST;
- runtime schemas, selected runtime contracts, provider matrix and Gold Assets needed to reconstruct behavior;
- `RECOVERY_README.txt`;
- `RECOVERY_MANIFEST.json`;
- `SHA256SUMS`;
- during the .44 transition, `engine/BOOTSTRAP_FULL.txt` may also be included as a legacy compatibility fallback.

Private account/workspace state is never embedded in the sanitized engine package. A full user recovery export pairs the sanitized recovery package with a separate private account snapshot.

## Deterministic construction
The package MUST be built from a clean exact Git checkout whose HEAD equals the declared `source_commit_sha`.
All payload paths are sorted and ZIP metadata is normalized so identical source bytes + options produce byte-identical package ZIPs.
Each payload file has SHA-256 and byte length recorded in `RECOVERY_MANIFEST.json`.
`SHA256SUMS` covers every payload file plus `RECOVERY_MANIFEST.json`.
Manifest-registered module bytes must reproduce the declared Git blob SHA-1 in `engine/MANIFEST.json`.

No build timestamp is embedded in the package because wall-clock metadata would make otherwise identical packages non-reproducible.

## Recovery manifest identity
`RECOVERY_MANIFEST.json` records:
- package format version;
- engine/API/workspace-schema identity;
- exact source commit SHA;
- Production channel and sanitization flags;
- primary bootstrap path;
- module manifest path;
- migration graph path;
- whether the legacy standalone fallback is included;
- generated file inventory with role, SHA-256 and byte length.

The generated manifest is an internal consistency root, not a signature. Hashes prove package consistency, not publisher authenticity. When live GitHub is available, exact commit provenance may be independently checked against canonical Production.

## Offline/manual recovery mode
A host may enter RECOVERY_PACKAGE mode only after:
1. the package structure validates;
2. `SHA256SUMS` matches package bytes;
3. `RECOVERY_MANIFEST.json`, LATEST and MANIFEST agree on engine/API/schema/privacy identity;
4. every MANIFEST-required module is present;
5. available Git-blob integrity checks pass for module bytes.

Then:
- use `source_commit_sha` as fixed snapshot C for this recovery transaction;
- read all candidate engine bytes locally from the package;
- load MANIFEST-required modules in dependency order and hand off through the normal entrypoint;
- preserve LOCAL STATE exactly as in normal startup;
- set resolver/update health to a recovery-snapshot/degraded state rather than falsely claiming live-current verification;
- when live-ref capability becomes available, `release.resolver` checks canonical GitHub Production and normal update logic may adopt a newer verified release.

Recovery package identity does not prove the snapshot is the newest Production while offline.

## No-mix rule
One recovery transaction uses one source only.
Never combine package LATEST/MANIFEST/modules with network bytes from another commit.
If package validation fails, do not partially activate it.
If a live update is attempted later, it is a separate pin-once transaction through the normal resolver.

## Failure behavior
Package corruption, missing files, identity mismatch, checksum mismatch, manifest-integrity mismatch or unsupported API/schema fails closed before activation.
Existing compatible deployments keep last-known-good ENGINE and LOCAL STATE.
A package failure never rewrites account/workspace state merely to make engine recovery succeed.

## Command semantics
- `export yourself` / `export LWAI`: remains the legacy sanitized BOOTSTRAP_FULL single-file export during .44.
- `export full recovery package`: produce the sanitized deterministic multi-file recovery package plus a separate private account snapshot when private state is requested/available.
- `refresh engine`: remains the live canonical Production update escape hatch and is not replaced by package recovery.

## Transition / future cutover
The .44 package proves modular recovery independently of the public installer.
A later separately gated release may expose Stage-1 as the normal LastWarAI.com payload or otherwise change transport. That cutover must retain .43/.44 last-known-good compatibility and is not authorized merely because the recovery package exists.

## Privacy
The package is sanitized public ENGINE only. It must not contain player/account identity, UIDs, screenshots, balances, battles, Corrections, provider IDs, auth material, private release checkpoints, maintainer-private records or consumer Runtime Session rows.
