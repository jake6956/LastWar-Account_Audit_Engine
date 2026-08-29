#!/usr/bin/env python3
"""Fail-closed static checks for LWAI Production release trees."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md", "SECURITY.md", "CONTRIBUTING.md",
    "engine/BOOTSTRAP.txt", "engine/BOOTSTRAP_FULL.txt", "engine/MANIFEST.json",
    "engine/modules/core/operating.txt", "engine/modules/core/persistence.txt",
    "engine/modules/core/accounts.txt", "engine/modules/core/guidance.txt",
    "engine/modules/release/runtime.txt", "engine/modules/release/bootstrap.txt",
    "contracts/operating-canon.md", "contracts/export-bootstrap.md", "contracts/storage-adapter.md",
    "contracts/account-registry.md", "contracts/release.md", "contracts/migration.md",
    "contracts/guided-lifecycle-ingestion.md", "contracts/runtime-checkpoint-recovery.md",
    "schemas/workspace-schema.md", "schemas/account-registry.schema.json", "schemas/engine-manifest.schema.json",
    "docs/architecture.md", "docs/deployment.md", "docs/quick-install.md", "docs/runtime-recovery.md",
    "adapters/provider-matrix.md", "gold-assets/README.md", "gold-assets/manifest.json",
    "releases/LATEST.json", "releases/CHANGELOG.md", "tests/RELEASE_GATES.md",
    ".github/workflows/validate.yml", ".github/CODEOWNERS",
]

EXPECTED_REPO = "https://github.com/jake6956/LastWar-Account_Audit_Engine"
EXPECTED_BOOT = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt"
EXPECTED_MANIFEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json"
EXPECTED_FULL = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt"
EXPECTED_LATEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json"
EXPECTED_INSTALL = "https://tinyurl.com/2yxf7f5x"


def fail(message):
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def require(label, body, tokens):
    missing = [token for token in tokens if token not in body]
    if missing:
        fail(f"{label} missing: {', '.join(missing)}")


def header_version(body):
    match = re.search(r"^engine_version:\s*(\S+)", body, re.M)
    if not match:
        fail("engine_version header missing")
    return match.group(1)


def main():
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"required file missing: {rel}")

    loader = read("engine/BOOTSTRAP.txt")
    full = read("engine/BOOTSTRAP_FULL.txt")
    persistence = read("engine/modules/core/persistence.txt")
    guidance = read("engine/modules/core/guidance.txt")
    runtime = read("engine/modules/release/runtime.txt")
    workspace = read("schemas/workspace-schema.md")
    recovery_contract = read("contracts/runtime-checkpoint-recovery.md")
    recovery_doc = read("docs/runtime-recovery.md")

    version = header_version(loader)
    if version != "2026-08-29.11" or header_version(full) != version:
        fail("loader/full fallback version mismatch")

    require("loader", loader, [
        "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "RECOVERY-FIRST STARTUP",
        "Runtime Checkpoints", "Runtime Journal", "WAITING_USER", "active_account_id",
        "ACCOUNT DISCOVERY / MIGRATION-FIRST STARTUP", "BATCH / DONE RULE",
        EXPECTED_REPO, EXPECTED_LATEST, EXPECTED_MANIFEST, EXPECTED_FULL, EXPECTED_INSTALL,
    ])
    require("full fallback", full, [
        "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "RUNTIME CHECKPOINT MODEL",
        "RUNTIME JOURNAL", "RECOVERY-FIRST STARTUP", "WRITE-AHEAD / IDEMPOTENCY",
        "WAITING_USER", "RELEASE TRANSACTION RECOVERY", "active_account_id",
        EXPECTED_REPO, EXPECTED_BOOT, EXPECTED_MANIFEST, EXPECTED_FULL, EXPECTED_INSTALL,
    ])
    require("core.persistence", persistence, [
        "module_version: 2026-08-29.11.1", "RUNTIME CHECKPOINT MODEL", "RUNTIME JOURNAL",
        "RECOVERY-FIRST RELOAD", "WRITE-AHEAD / IDEMPOTENCY", "RECOVERY_REQUIRED",
        "append-only", "WAITING_USER", "ACCOUNT ISOLATION", "CONTEXT BUDGET",
    ])
    require("core.guidance", guidance, [
        "module_version: 2026-08-29.11.1", "RUNTIME CHECKPOINT INTEGRATION",
        "WAITING_USER", "BATCH BOUNDARY RULE", "active_account_id",
    ])
    require("release.runtime", runtime, [
        "module_version: 2026-08-29.11.1", "RELEASE TRANSACTION CHECKPOINT",
        "VERIFY-BEFORE-REPLAY", "CI_PASSED", "POST_MERGE_VERIFIED", "last-known-good",
    ])
    require("workspace schema", workspace, [
        "Version: 2026-08-29.11", "Runtime Checkpoints", "Runtime Journal",
        "append-only", "RECOVERY_REQUIRED", "active_account_id",
    ])
    require("recovery contract", recovery_contract, [
        "Runtime Checkpoints", "Runtime Journal", "WAITING_USER", "verify-before-replay",
        "hidden chain-of-thought", "append-only",
    ])
    require("recovery docs", recovery_doc, [
        "Recovery procedure", "Runtime Checkpoints", "Runtime Journal", "WAITING_USER", "Privacy",
    ])

    latest = json.loads(read("releases/LATEST.json"))
    manifest = json.loads(read("engine/MANIFEST.json"))
    account_schema = json.loads(read("schemas/account-registry.schema.json"))
    if latest.get("engine_version") != version or manifest.get("engine_version") != version:
        fail("LATEST/MANIFEST version mismatch")
    if latest.get("schema_version") != "2.3" or manifest.get("schema_version") != "2.3":
        fail("schema version mismatch")
    for obj, label in [(latest, "LATEST"), (manifest, "MANIFEST")]:
        if obj.get("sanitized") is not True or obj.get("account_state_included") is not False:
            fail(f"{label} sanitization flags invalid")
    if latest.get("github_repository") != EXPECTED_REPO or latest.get("github_bootstrap_source") != EXPECTED_BOOT:
        fail("LATEST source endpoints invalid")
    if latest.get("preferred_install_url") != EXPECTED_INSTALL:
        fail("LATEST installer invalid")

    if account_schema.get("title") != "LWAI Workspace Account Registry":
        fail("account registry schema identity invalid")
    if "audit_sessions" not in (account_schema.get("properties") or {}):
        fail("account registry schema lost audit_sessions")

    entries = manifest.get("modules") or []
    ids = [entry.get("module_id") for entry in entries]
    if not entries or None in ids or len(ids) != len(set(ids)):
        fail("module ids missing or duplicated")
    id_set = set(ids)
    by_id = {entry["module_id"]: entry for entry in entries}
    for entry in entries:
        rel = entry.get("path")
        if not rel or not (ROOT / rel).is_file():
            fail(f"missing module path for {entry.get('module_id')}")
        body = read(rel)
        require(entry["module_id"], body, [
            f"module_id: {entry['module_id']}", "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO"
        ])
        for dep in entry.get("dependencies", []):
            if dep not in id_set:
                fail(f"unresolved dependency {dep} for {entry['module_id']}")

    required_ids = ["core.operating", "core.persistence", "core.accounts", "core.guidance", "release.runtime", "release.bootstrap"]
    for module_id in required_ids:
        if module_id not in by_id or by_id[module_id].get("required") is not True:
            fail(f"required module not marked required: {module_id}")
    if by_id["core.guidance"].get("dependencies") != ["core.operating", "core.persistence", "core.accounts"]:
        fail("core.guidance dependency graph invalid")
    for module_id in ["core.persistence", "core.guidance", "release.runtime"]:
        if by_id[module_id].get("module_version") != "2026-08-29.11.1":
            fail(f"{module_id} version not advanced to .11")

    archive_rel = f"releases/{version}.json"
    archive = json.loads(read(archive_rel))
    if archive.get("engine_version") != version or archive.get("sanitized") is not True or archive.get("account_state_included") is not False:
        fail("versioned release manifest invalid")

    readme = read("README.md")
    if f"**Engine version:** `{version}`" not in readme or EXPECTED_INSTALL not in readme:
        fail("README Production identity/install mismatch")
    quick = read("docs/quick-install.md")
    if EXPECTED_INSTALL not in quick or EXPECTED_BOOT not in quick:
        fail("quick-install endpoint mismatch")

    # Candidate-specific privacy guard: generic public artifacts define recovery behavior only.
    public_recovery = "\n".join([loader, full, persistence, guidance, runtime, workspace, recovery_contract, recovery_doc, readme])
    private_markers = [
        "CP-" + "20260829" + "-011",
        "J-" + "20260829" + "-011",
    ]
    for marker in private_markers:
        if marker in public_recovery:
            fail("candidate contains local checkpoint/journal identifier")
    if re.search(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b", public_recovery, re.I):
        fail("candidate contains possible credential token")
    if re.search(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY", public_recovery):
        fail("candidate contains possible private key")

    print(f"PASS: LWAI Production {version} passed runtime-recovery release checks")


if __name__ == "__main__":
    main()
