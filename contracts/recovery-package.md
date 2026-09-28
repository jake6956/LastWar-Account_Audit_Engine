# Recovery Package Contract

Version: 2026-09-28.48

## Purpose
Define a deterministic, sanitized, multi-file LWAI recovery package that can reconstruct the modular runtime and preserve the exact build provenance for the generated single-response artifact without depending on live remote retrieval.

The package is a fixed exact-commit recovery snapshot. It is not current-version authority and it is not a second engine architecture.

## Core design
`engine/BOOTSTRAP.txt` remains the thin recovery kernel. Canonical behavior remains modular. The supported ChatGPT fresh-install artifact is the deterministic compiled `engine/BOOTSTRAP_FULL.txt`; recovery packages preserve both the modular runtime and the compiler inputs that produce that artifact.

A recovery package contains one exact sanitized engine snapshot:
- `engine/BOOTSTRAP.txt`;
- `engine/MANIFEST.json`;
- `releases/LATEST.json`;
- `releases/MIGRATIONS.json`;
- the current versioned release manifest;
- every module path registered in MANIFEST;
- `engine/standalone/plan.json`;
- all seven owned `engine/standalone/*.txt` compact capsules;
- `scripts/build_bootstrap_full.py`;
- runtime schemas, selected runtime contracts, provider matrix and Gold Assets needed to reconstruct behavior;
- `RECOVERY_README.txt`;
- `RECOVERY_MANIFEST.json`;
- `SHA256SUMS`;
- when the existing package option is enabled, the generated `engine/BOOTSTRAP_FULL.txt` artifact.

The historical manifest field `legacy_fallback_included` is retained for package-format compatibility. In .48 it indicates whether the generated standalone `BOOTSTRAP_FULL.txt` artifact is present; it does not mean the artifact is separately authored or deprecated.

Private account/workspace state is never embedded in the sanitized engine package. A full user recovery export pairs the sanitized engine package with a separate private account snapshot.

## Deterministic construction
The package MUST be built from a clean exact Git checkout whose HEAD equals the declared `source_commit_sha`.
All payload paths are sorted and ZIP metadata is normalized so identical source bytes + options produce byte-identical ZIP bytes.
Each payload file has SHA-256 and byte length recorded in `RECOVERY_MANIFEST.json`.
`SHA256SUMS` covers every payload file plus `RECOVERY_MANIFEST.json`.
Manifest-registered module bytes must reproduce the declared Git blob SHA-1 in `engine/MANIFEST.json`.

The standalone compiler provenance is part of the package:
- `engine/standalone/plan.json` fingerprints every MANIFEST module used by the compact projection;
- every declared capsule must be present;
- `scripts/build_bootstrap_full.py` must be present;
- when `engine/BOOTSTRAP_FULL.txt` is included, the package contains both the generated artifact and the exact inputs/build logic needed to reproduce it.

No wall-clock build timestamp is embedded because it would break reproducibility.

## Recovery manifest identity
`RECOVERY_MANIFEST.json` records:
- package format version;
- engine/API/workspace-schema identity;
- exact source commit SHA;
- Production channel and sanitization flags;
- primary bootstrap path;
- module manifest path;
- migration graph path;
- whether the generated standalone artifact is included through the backward-compatible `legacy_fallback_included` field;
- generated file inventory with role, SHA-256 and byte length.

Compiler provenance files use distinct roles such as `compiled_fallback_plan`, `compiled_fallback_capsule`, and `compiled_fallback_builder`. The generated `BOOTSTRAP_FULL.txt` uses `compiled_fallback`.

The generated recovery manifest is an internal consistency root, not a signature. Hashes prove package consistency, not publisher authenticity. When live GitHub is available, exact commit provenance may be independently checked against canonical Production.

## Offline/manual recovery mode
A host may enter RECOVERY_PACKAGE mode only after:
1. package structure validates;
2. `SHA256SUMS` matches package bytes;
3. `RECOVERY_MANIFEST.json`, LATEST and MANIFEST agree on engine/API/schema/privacy identity;
4. every MANIFEST-required module is present;
5. available Git-blob integrity checks pass for module bytes.

Then:
- use `source_commit_sha` as fixed snapshot C for this recovery transaction;
- read candidate engine bytes locally from the package;
- load MANIFEST-required modules in dependency order and hand off through the normal entrypoint;
- preserve LOCAL STATE exactly as in normal startup;
- set resolver/update health to recovery-snapshot/degraded rather than falsely claiming live-current verification;
- when live-ref capability returns, `release.resolver` checks canonical GitHub Production and normal update logic may adopt a newer verified release.

Recovery package identity does not prove that its snapshot is newest live Production while offline.

The compiler inputs are build provenance, not a second activation path. Recovery may execute the modular runtime without `BOOTSTRAP_FULL.txt`; when the standalone artifact is needed, it may be independently regenerated/verified from the packaged compiler inputs.

## No-mix rule
One recovery transaction uses one source only.
Never combine package LATEST/MANIFEST/modules with network bytes from another commit.
If package validation fails, do not partially activate it.
A later live update is a separate pin-once transaction through the normal resolver.

## Failure behavior
Package corruption, missing files, identity mismatch, checksum mismatch, manifest-integrity mismatch or unsupported API/schema fails closed before activation.
Existing compatible deployments keep last-known-good ENGINE and LOCAL STATE.
Package failure never rewrites account/workspace state merely to make engine recovery succeed.
Missing or inconsistent standalone compiler provenance invalidates deterministic standalone reconstruction; it must not silently substitute hand-edited fallback bytes.

## Command semantics
- `export yourself` / `export LWAI`: emit the sanitized generated `BOOTSTRAP_FULL.txt` single-file runtime.
- `export full recovery package`: produce the sanitized deterministic multi-file recovery package plus a separate private account snapshot when private state is requested/available.
- `refresh engine`: remain the live canonical Production update escape hatch and is not replaced by package recovery.

## Transport boundary
The recovery package is independent of the supported ChatGPT first-install transport. Normal ChatGPT installation remains one response from the user-supplied bare `https://lastwarai.com` origin.

Existing direct/modular compatibility routes may use Stage-1 and exact-commit modules when host capabilities support them, but package recovery never depends on a second network hop and never authorizes a default modular cutover.

## Privacy
The package is sanitized public ENGINE/build provenance only. It must not contain player/account identity, UIDs, screenshots, balances, battles, Corrections, provider IDs, auth material, private release checkpoints, maintainer-private records or consumer Runtime Session rows.
