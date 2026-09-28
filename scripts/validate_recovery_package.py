#!/usr/bin/env python3
"""Validate an LWAI deterministic multi-file recovery package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import PurePosixPath
import re
import sys
import zipfile

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
CREDENTIAL = re.compile(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b", re.I)
PRIVATE_MARKERS = (
    "PRIVATE_" + "RC_STAGED",
    "BEGIN " + "RSA PRIVATE KEY",
    "BEGIN " + "EC PRIVATE KEY",
    "BEGIN " + "OPENSSH PRIVATE KEY",
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def parse_sums(data: bytes) -> dict[str, str]:
    result = {}
    for line in data.decode("utf-8").splitlines():
        digest, sep, path = line.partition("  ")
        if not sep or not HEX64.fullmatch(digest) or not path:
            fail("invalid SHA256SUMS line")
        if path in result:
            fail(f"duplicate checksum path: {path}")
        result[path] = digest
    return result


def validate(path: str, expected_commit: str | None = None) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            fail("duplicate ZIP member")
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts or name.startswith("/"):
                fail(f"unsafe ZIP path: {name}")
        required_top = {"RECOVERY_MANIFEST.json", "RECOVERY_README.txt", "SHA256SUMS"}
        if not required_top.issubset(names):
            fail("missing recovery control file")

        raw = {name: zf.read(name) for name in names}

    manifest = json.loads(raw["RECOVERY_MANIFEST.json"].decode("utf-8"))
    for key in (
        "package_format_version", "engine_version", "engine_api_version",
        "workspace_schema_version", "source_commit_sha", "channel", "sanitized",
        "account_state_included", "primary_bootstrap", "module_manifest",
        "migration_graph", "legacy_fallback_included", "generated_by", "files",
    ):
        if key not in manifest:
            fail(f"recovery manifest missing {key}")
    if manifest["package_format_version"] != "1.0":
        fail("unsupported recovery package format")
    if not HEX40.fullmatch(manifest["source_commit_sha"]):
        fail("invalid source commit")
    if expected_commit and manifest["source_commit_sha"] != expected_commit:
        fail("source commit does not match expected commit")
    if manifest["channel"] != "Production" or manifest["sanitized"] is not True or manifest["account_state_included"] is not False:
        fail("package privacy/channel identity invalid")
    if manifest["primary_bootstrap"] != "engine/BOOTSTRAP.txt":
        fail("unexpected primary bootstrap")
    if manifest["module_manifest"] != "engine/MANIFEST.json" or manifest["migration_graph"] != "releases/MIGRATIONS.json":
        fail("unexpected manifest/migration path")
    if manifest["generated_by"] != "scripts/build_recovery_package.py":
        fail("unexpected recovery builder identity")

    file_records = {row["path"]: row for row in manifest["files"]}
    if len(file_records) != len(manifest["files"]):
        fail("duplicate payload path in recovery manifest")
    expected_names = set(file_records) | {"RECOVERY_MANIFEST.json", "SHA256SUMS"}
    if set(raw) != expected_names:
        extra = sorted(set(raw) - expected_names)
        missing = sorted(expected_names - set(raw))
        fail(f"ZIP inventory mismatch extra={extra} missing={missing}")

    for rel, row in file_records.items():
        data = raw.get(rel)
        if data is None:
            fail(f"payload missing: {rel}")
        if row.get("bytes") != len(data) or row.get("sha256") != sha256(data):
            fail(f"payload digest/length mismatch: {rel}")

    sums = parse_sums(raw["SHA256SUMS"])
    expected_sums = {rel: sha256(data) for rel, data in raw.items() if rel != "SHA256SUMS"}
    if sums != expected_sums:
        fail("SHA256SUMS does not exactly match package bytes")

    latest = json.loads(raw["releases/LATEST.json"].decode("utf-8"))
    engine_manifest = json.loads(raw["engine/MANIFEST.json"].decode("utf-8"))
    if not (
        manifest["engine_version"] == latest.get("engine_version") == engine_manifest.get("engine_version")
        and manifest["engine_api_version"] == latest.get("engine_api_version") == engine_manifest.get("engine_api_version")
        and manifest["workspace_schema_version"] == latest.get("schema_version") == engine_manifest.get("schema_version")
    ):
        fail("package/LATEST/MANIFEST identity mismatch")
    for obj, label in ((latest, "LATEST"), (engine_manifest, "MANIFEST")):
        if obj.get("channel") != "Production" or obj.get("sanitized") is not True or obj.get("account_state_included") is not False:
            fail(f"{label} privacy/channel identity invalid")

    for mod in engine_manifest.get("modules", []):
        rel = mod["path"]
        if rel not in raw:
            fail(f"manifest module missing from package: {mod['module_id']}")
        expected = (mod.get("integrity") or {}).get("digest")
        if expected != git_blob_sha1(raw[rel]):
            fail(f"module git-blob integrity mismatch: {mod['module_id']}")

    fallback_present = "engine/BOOTSTRAP_FULL.txt" in raw
    if fallback_present != bool(manifest["legacy_fallback_included"]):
        fail("standalone fallback inclusion flag does not match package contents")

    forbidden_prefixes = ("tests/", "infrastructure/", ".git/")
    for name, data in raw.items():
        if name.startswith(forbidden_prefixes):
            fail(f"development/infrastructure file leaked into recovery package: {name}")
        if name == "contracts/private-failsafe-mirror.md":
            fail("maintainer-private failsafe contract leaked into consumer recovery package")
        if name.endswith((".txt", ".md", ".json", ".py", ".js", ".yml", ".yaml")):
            text = data.decode("utf-8", errors="ignore")
            if CREDENTIAL.search(text):
                fail(f"possible credential token in {name}")
            for marker in PRIVATE_MARKERS:
                if marker in text:
                    fail(f"private marker in {name}: {marker}")

    readme = raw["RECOVERY_README.txt"].decode("utf-8")
    for token in ("fixed, exact-commit modular recovery snapshot", "Never mix package bytes with network bytes", "LOCAL STATE"):
        if token not in readme:
            fail(f"recovery README missing: {token}")

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("package")
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    validate(args.package, args.expected_commit)
    print("PASS: recovery package structure, identity, checksums, module integrity, privacy and no-mix contract validated")


if __name__ == "__main__":
    main()
