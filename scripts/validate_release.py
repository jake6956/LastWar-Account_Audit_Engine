#!/usr/bin/env python3
"""Fail-closed static checks for modular LWAI Production."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "engine/BOOTSTRAP.txt"
FULL = ROOT / "engine/BOOTSTRAP_FULL.txt"
MANIFEST = ROOT / "engine/MANIFEST.json"
LATEST = ROOT / "releases/LATEST.json"
README = ROOT / "README.md"
QUICK = ROOT / "docs/quick-install.md"
ACCOUNT_SCHEMA = ROOT / "schemas/account-registry.schema.json"
WORKSPACE_SCHEMA = ROOT / "schemas/workspace-schema.md"
PERSISTENCE = ROOT / "engine/modules/core/persistence.txt"
ACCOUNTS = ROOT / "engine/modules/core/accounts.txt"
GUIDANCE = ROOT / "engine/modules/core/guidance.txt"
RUNTIME = ROOT / "engine/modules/release/runtime.txt"
RECOVERY_CONTRACT = ROOT / "contracts/runtime-checkpoint-recovery.md"
RECOVERY_DOC = ROOT / "docs/runtime-recovery.md"

EXPECTED_REPO = "https://github.com/jake6956/LastWar-Account_Audit_Engine"
EXPECTED_RAW_BOOT = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt"
EXPECTED_LATEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json"
EXPECTED_MODULE_MANIFEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json"
EXPECTED_FULL = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt"
EXPECTED_INSTALL = "https://tinyurl.com/2yxf7f5x"

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

LOADER_PHRASES = [
    "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "runtime_mode: modular",
    "RECOVERY-FIRST STARTUP", "Runtime Checkpoints", "Runtime Journal", "verify-before-replay",
    "WAITING_USER", "active_account_id", "hidden chain-of-thought", "ACCOUNT DISCOVERY / MIGRATION-FIRST STARTUP",
    "BATCH / DONE RULE", "UPSTREAM ENGINE / LOCAL STATE SEPARATION", "HEALTH / REGRESSION TESTS",
]
FULL_PHRASES = [
    "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "runtime_mode: standalone_fallback",
    "STEP 0 — REASONING MODE", "CORE OPERATING MODEL", "ACCOUNT REGISTRY / PRIMARY KEY",
    "GUIDED INTERACTION PRINCIPLE", "AUDIT SESSION STATE", "RUNTIME CHECKPOINT MODEL", "RUNTIME JOURNAL",
    "RECOVERY-FIRST STARTUP", "WRITE-AHEAD / IDEMPOTENCY", "WAITING_USER", "hidden chain-of-thought",
    "CLOUD-NEUTRAL WORKSPACE SCHEMA", "RELEASE TRANSACTION RECOVERY", "HEALTH / REGRESSION TESTS",
]
PERSISTENCE_PHRASES = [
    "module_version: 2026-08-29.11.1", "RUNTIME CHECKPOINT MODEL", "RUNTIME JOURNAL",
    "RECOVERY-FIRST RELOAD", "WRITE-AHEAD / IDEMPOTENCY", "WAITING_USER / BATCH RECOVERY",
    "ACCOUNT ISOLATION", "CONTEXT BUDGET", "append-only", "COMMITTED", "RECOVERY_REQUIRED",
]
GUIDANCE_PHRASES = [
    "module_version: 2026-08-29.11.1", "RUNTIME CHECKPOINT INTEGRATION", "WAITING_USER",
    "BATCH BOUNDARY RULE", "reply done", "active_account_id", "Recovery never requires hidden reasoning",
]
RUNTIME_PHRASES = [
    "module_version: 2026-08-29.11.1", "RELEASE TRANSACTION CHECKPOINT", "VERIFY-BEFORE-REPLAY",
    "PRIVATE_RC_STAGED", "CI_PASSED", "POST_MERGE_VERIFIED", "COMMITTED", "last-known-good",
]
WORKSPACE_PHRASES = [
    "Version: 2026-08-29.11", "Runtime Checkpoints", "Runtime Journal", "append-only",
    "RECOVERY_REQUIRED", "Recovery-first startup", "active_account_id",
]

GENERIC_FORBIDDEN = {
    "oauth/api token": re.compile(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b"),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py"}


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def text(path):
    return path.read_text(encoding="utf-8")


def version_from(s):
    m = re.search(r"^engine_version:\s*(\S+)", s, re.M)
    if not m:
        fail("engine_version header missing")
    return m.group(1)


def require_phrases(label, body, phrases):
    for phrase in phrases:
        if phrase not in body:
            fail(f"{label} missing required phrase: {phrase}")


def iter_public_text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main():
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")

    loader = text(BOOT)
    full = text(FULL)
    persistence = text(PERSISTENCE)
    accounts = text(ACCOUNTS)
    guidance = text(GUIDANCE)
    runtime = text(RUNTIME)
    workspace = text(WORKSPACE_SCHEMA)
    contract = text(RECOVERY_CONTRACT)
    recovery_doc = text(RECOVERY_DOC)

    require_phrases("loader", loader, LOADER_PHRASES)
    require_phrases("full fallback", full, FULL_PHRASES)
    require_phrases("core.persistence", persistence, PERSISTENCE_PHRASES)
    require_phrases("core.guidance", guidance, GUIDANCE_PHRASES)
    require_phrases("release.runtime", runtime, RUNTIME_PHRASES)
    require_phrases("workspace schema", workspace, WORKSPACE_PHRASES)
    require_phrases("recovery contract", contract, ["Runtime Checkpoints", "Runtime Journal", "verify-before-replay", "WAITING_USER", "hidden chain-of-thought"])
    require_phrases("recovery doc", recovery_doc, ["Recovery procedure", "Do not replay verified successful writes", "WAITING_USER", "Privacy"])

    for phrase in ["UID is optional", "WORKSPACE REGISTRY", "ACCOUNT DATABASE ISOLATION", "active_account_id"]:
        if phrase not in accounts:
            fail(f"core.accounts missing required phrase: {phrase}")

    version = version_from(loader)
    if version != "2026-08-29.11":
        fail(f"unexpected candidate version: {version}")
    if version_from(full) != version:
        fail("BOOTSTRAP_FULL version does not match thin loader")

    latest = json.loads(text(LATEST))
    manifest = json.loads(text(MANIFEST))
    account_schema = json.loads(text(ACCOUNT_SCHEMA))
    if latest.get("engine_version") != version or manifest.get("engine_version") != version:
        fail("release/module manifest version does not match loader")
    if latest.get("schema_version") != "2.3" or manifest.get("schema_version") != "2.3":
        fail("schema version must be 2.3")
    if latest.get("sanitized") is not True or manifest.get("sanitized") is not True:
        fail("manifests must assert sanitized=true")
    if latest.get("account_state_included") is not False or manifest.get("account_state_included") is not False:
        fail("manifests must assert account_state_included=false")
    if latest.get("github_repository") != EXPECTED_REPO or latest.get("github_bootstrap_source") != EXPECTED_RAW_BOOT:
        fail("LATEST authoritative endpoint mismatch")
    if latest.get("preferred_install_url") != EXPECTED_INSTALL:
        fail("LATEST install alias mismatch")

    if account_schema.get("title") != "LWAI Workspace Account Registry":
        fail("account registry schema title missing/unexpected")
    if "audit_sessions" not in account_schema.get("properties", {}):
        fail("account registry schema lost audit_sessions")

    entries = manifest.get("modules") or []
    module_ids = {e.get("module_id") for e in entries}
    if None in module_ids or len(module_ids) != len(entries):
        fail("invalid/duplicate module ids")
    for entry in entries:
        path = ROOT / entry.get("path", "")
        if not path.is_file():
            fail(f"module path missing: {entry.get('module_id')}")
        body = text(path)
        if f"module_id: {entry.get('module_id')}" not in body:
            fail(f"module self-identification mismatch: {entry.get('module_id')}")
        if "SANITIZED: YES" not in body or "ACCOUNT STATE INCLUDED: NO" not in body:
            fail(f"module sanitization headers missing: {entry.get('module_id')}")
        for dep in entry.get("dependencies", []):
            if dep not in module_ids:
                fail(f"unresolved dependency {dep} for {entry.get('module_id')}")

    required = {e["module_id"]: e for e in entries if e.get("required") is True}
    for mid in ["core.operating", "core.persistence", "core.accounts", "core.guidance", "release.runtime", "release.bootstrap"]:
        if mid not in required:
            fail(f"required core module not marked required: {mid}")
    if required["core.guidance"].get("dependencies") != ["core.operating", "core.persistence", "core.accounts"]:
        fail("core.guidance dependencies unexpected")
    if required["core.persistence"].get("module_version") != "2026-08-29.11.1":
        fail("core.persistence manifest version mismatch")
    if required["core.guidance"].get("module_version") != "2026-08-29.11.1":
        fail("core.guidance manifest version mismatch")
    if required["release.runtime"].get("module_version") != "2026-08-29.11.1":
        fail("release.runtime manifest version mismatch")

    for endpoint in [EXPECTED_REPO, EXPECTED_RAW_BOOT, EXPECTED_LATEST, EXPECTED_MODULE_MANIFEST, EXPECTED_FULL, EXPECTED_INSTALL]:
        if endpoint not in loader and endpoint not in full:
            fail(f"Production endpoint missing from runtime: {endpoint}")

    readme = text(README)
    if f"**Engine version:** `{version}`" not in readme:
        fail("README Production version mismatch")
    if EXPECTED_INSTALL not in readme:
        fail("README missing preferred installer")
    quick = text(QUICK)
    if EXPECTED_INSTALL not in quick or EXPECTED_RAW_BOOT not in quick:
        fail("quick-install documentation missing required installer/fallback")

    archive = ROOT / "releases" / f"{version}.json"
    if not archive.exists():
        fail("versioned release manifest missing")
    archive_json = json.loads(text(archive))
    if archive_json.get("engine_version") != version or archive_json.get("account_state_included") is not False:
        fail("versioned release manifest identity mismatch")

    forbidden_literals = [
        "CP-" + "20260829" + "-011",
        "J-" + "20260829" + "-011",
        "drive.google.com/drive/" + "folders/",
    ]
    for path in iter_public_text_files():
        body = text(path)
        for literal in forbidden_literals:
            if literal in body:
                fail(f"{path.relative_to(ROOT)} contains private/local recovery identifier")
        for label, pattern in GENERIC_FORBIDDEN.items():
            if pattern.search(body):
                fail(f"{path.relative_to(ROOT)} contains possible {label}")

    print(f"PASS: LWAI Production {version} passed modular recovery release checks")


if __name__ == "__main__":
    main()
