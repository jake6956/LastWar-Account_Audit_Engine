#!/usr/bin/env python3
"""Build a deterministic sanitized LWAI multi-file recovery package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
HEX40 = re.compile(r"^[0-9a-f]{40}$")
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)

RUNTIME_CONTRACTS = [
    "contracts/account-registry.md",
    "contracts/automatic-updates.md",
    "contracts/bootstrap-resolution.md",
    "contracts/export-bootstrap.md",
    "contracts/guided-lifecycle-ingestion.md",
    "contracts/migration.md",
    "contracts/operating-canon.md",
    "contracts/preferences.md",
    "contracts/recommendation-governance.md",
    "contracts/recovery-package.md",
    "contracts/runtime-checkpoint-recovery.md",
    "contracts/season-intelligence.md",
    "contracts/storage-adapter.md",
    "contracts/user-experience.md",
]
STATIC_RUNTIME = [
    "engine/BOOTSTRAP.txt",
    "engine/MANIFEST.json",
    "releases/LATEST.json",
    "releases/MIGRATIONS.json",
    "schemas/account-registry.schema.json",
    "schemas/engine-manifest.schema.json",
    "schemas/preferences.schema.json",
    "schemas/recovery-package.schema.json",
    "schemas/workspace-schema.md",
    "adapters/provider-matrix.md",
    "docs/quick-install.md",
    "docs/runtime-recovery.md",
]


def read_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True
    ).stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def role_for(path: str, module_paths: set[str]) -> str:
    if path == "engine/BOOTSTRAP.txt":
        return "bootstrap"
    if path == "engine/BOOTSTRAP_FULL.txt":
        return "legacy_fallback"
    if path == "engine/MANIFEST.json":
        return "module_manifest"
    if path == "releases/LATEST.json":
        return "release_metadata"
    if path == "releases/MIGRATIONS.json":
        return "migration_graph"
    if path.startswith("releases/"):
        return "versioned_release"
    if path in module_paths:
        return "module"
    if path.startswith("schemas/"):
        return "schema"
    if path.startswith("contracts/"):
        return "runtime_contract"
    if path.startswith("adapters/"):
        return "adapter_metadata"
    if path.startswith("gold-assets/"):
        return "gold_asset"
    if path.startswith("docs/"):
        return "recovery_documentation"
    if path == "RECOVERY_README.txt":
        return "recovery_readme"
    return "runtime_asset"


def recovery_readme(engine_version: str, source_commit: str, legacy: bool) -> bytes:
    legacy_line = (
        "This transition package also includes engine/BOOTSTRAP_FULL.txt as a legacy compatibility fallback.\n"
        if legacy else
        "This package intentionally does not include the legacy standalone fallback.\n"
    )
    body = f"""LWAI RECOVERY PACKAGE

Engine version: {engine_version}
Source commit: {source_commit}
SANITIZED: YES
ACCOUNT STATE INCLUDED: NO

PURPOSE
This is a fixed, exact-commit modular recovery snapshot. It is not proof that this is the newest live Production while offline.

RECOVERY
1. Validate SHA256SUMS and RECOVERY_MANIFEST.json before loading engine instructions.
2. Use engine/BOOTSTRAP.txt as the recovery kernel.
3. Treat source commit {source_commit} as snapshot C and load all MANIFEST-required modules from this package only.
4. Never mix package bytes with network bytes in the same recovery transaction.
5. Keep private account/workspace state separate and preserve LOCAL STATE.
6. When live GitHub access becomes available, run the normal resolver/update path to check current Production.

{legacy_line}
If validation fails, do not partially activate this package.
"""
    return body.encode("utf-8")


def collect_payload(source_commit: str, include_legacy_fallback: bool) -> tuple[dict[str, bytes], dict]:
    if not HEX40.fullmatch(source_commit):
        raise SystemExit("source commit must be 40 lowercase hex")
    head = git_head()
    if head != source_commit:
        raise SystemExit(f"checkout HEAD {head} does not match declared source commit {source_commit}")

    latest = read_json("releases/LATEST.json")
    manifest = read_json("engine/MANIFEST.json")
    if latest.get("engine_version") != manifest.get("engine_version"):
        raise SystemExit("LATEST/MANIFEST engine version mismatch")
    if latest.get("engine_api_version") != manifest.get("engine_api_version"):
        raise SystemExit("LATEST/MANIFEST API mismatch")
    if latest.get("schema_version") != manifest.get("schema_version"):
        raise SystemExit("LATEST/MANIFEST schema mismatch")
    for obj, label in ((latest, "LATEST"), (manifest, "MANIFEST")):
        if obj.get("channel") != "Production" or obj.get("sanitized") is not True or obj.get("account_state_included") is not False:
            raise SystemExit(f"{label} privacy/channel identity invalid")

    version_rel = f"releases/{latest['engine_version']}.json"
    module_paths = {m["path"] for m in manifest.get("modules", [])}
    paths = set(STATIC_RUNTIME + RUNTIME_CONTRACTS + [version_rel])
    paths.update(module_paths)

    gold_root = ROOT / "gold-assets"
    for item in gold_root.rglob("*"):
        if item.is_file():
            paths.add(item.relative_to(ROOT).as_posix())

    if include_legacy_fallback:
        paths.add("engine/BOOTSTRAP_FULL.txt")

    payload: dict[str, bytes] = {}
    for rel in sorted(paths):
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"required recovery payload missing: {rel}")
        payload[rel] = path.read_bytes()

    for mod in manifest.get("modules", []):
        rel = mod["path"]
        expected = (mod.get("integrity") or {}).get("digest")
        actual = git_blob_sha1(payload[rel])
        if expected != actual:
            raise SystemExit(f"module integrity mismatch while packaging {mod['module_id']}: {expected} != {actual}")

    payload["RECOVERY_README.txt"] = recovery_readme(
        latest["engine_version"], source_commit, include_legacy_fallback
    )
    return payload, manifest


def build(output: Path, source_commit: str, include_legacy_fallback: bool) -> None:
    payload, module_manifest = collect_payload(source_commit, include_legacy_fallback)
    latest = read_json("releases/LATEST.json")
    module_paths = {m["path"] for m in module_manifest.get("modules", [])}

    records = []
    for rel in sorted(payload):
        data = payload[rel]
        records.append({
            "path": rel,
            "role": role_for(rel, module_paths),
            "sha256": sha256(data),
            "bytes": len(data),
        })

    recovery_manifest = {
        "package_format_version": "1.0",
        "engine_version": latest["engine_version"],
        "engine_api_version": latest["engine_api_version"],
        "workspace_schema_version": latest["schema_version"],
        "source_commit_sha": source_commit,
        "channel": "Production",
        "sanitized": True,
        "account_state_included": False,
        "primary_bootstrap": "engine/BOOTSTRAP.txt",
        "module_manifest": "engine/MANIFEST.json",
        "migration_graph": "releases/MIGRATIONS.json",
        "legacy_fallback_included": include_legacy_fallback,
        "generated_by": "scripts/build_recovery_package.py",
        "files": records,
    }
    manifest_bytes = (json.dumps(recovery_manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")

    checksums = {rel: sha256(data) for rel, data in payload.items()}
    checksums["RECOVERY_MANIFEST.json"] = sha256(manifest_bytes)
    sums_bytes = "".join(f"{checksums[rel]}  {rel}\n" for rel in sorted(checksums)).encode("utf-8")

    members = dict(payload)
    members["RECOVERY_MANIFEST.json"] = manifest_bytes
    members["SHA256SUMS"] = sums_bytes

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in sorted(members):
            info = zipfile.ZipInfo(rel, ZIP_EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, members[rel], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--without-legacy-fallback", action="store_true")
    args = parser.parse_args()
    build(Path(args.output), args.source_commit, not args.without_legacy_fallback)
    print(args.output)


if __name__ == "__main__":
    main()
