#!/usr/bin/env python3
"""Fail-closed static checks for modular LWAI Production."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "engine" / "BOOTSTRAP.txt"
FULL = ROOT / "engine" / "BOOTSTRAP_FULL.txt"
MODULE_MANIFEST = ROOT / "engine" / "MANIFEST.json"
LATEST = ROOT / "releases" / "LATEST.json"
README = ROOT / "README.md"
QUICK_INSTALL = ROOT / "docs" / "quick-install.md"
ACCOUNT_SCHEMA = ROOT / "schemas" / "account-registry.schema.json"
ACCOUNT_MODULE = ROOT / "engine" / "modules" / "core" / "accounts.txt"
GUIDANCE_MODULE = ROOT / "engine" / "modules" / "core" / "guidance.txt"

EXPECTED_REPO = "https://github.com/jake6956/LastWar-Account_Audit_Engine"
EXPECTED_RAW_BOOT = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt"
EXPECTED_RAW_MANIFEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json"
EXPECTED_MODULE_MANIFEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json"
EXPECTED_FULL = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt"
EXPECTED_INSTALL_URL = "https://tinyurl.com/2yxf7f5x"

REQUIRED_LOADER_PHRASES = [
    "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "runtime_mode: modular",
    "LOADER PROCEDURE", "ACCOUNT DISCOVERY / MIGRATION-FIRST STARTUP", "ACCOUNT IDENTITY / PRIVACY",
    "CONTEXT SWITCHING", "START-OVER SAFETY", "IDENTITY SANITY CHECK", "GUIDED INTERACTION",
    "BATCH / DONE RULE", "active_account_id", "UID is useful but optional", "core.guidance",
    "CORE OPERATING MODEL", "EVIDENCE HIERARCHY", "SELF-HEALING RULE",
    "UPSTREAM ENGINE / LOCAL STATE SEPARATION", "REMOTE BOOTSTRAP / ONE-LINE INSTALL",
    "PRIVACY / SEMI-ANONYMIZED DISTRIBUTION", "DOCUMENTATION-AS-CODE",
    "HEALTH / REGRESSION TESTS", "STARTUP BEHAVIOR",
]

REQUIRED_FULL_PHRASES = [
    "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "runtime_mode: standalone_fallback",
    "STEP 0 — REASONING MODE", "CORE OPERATING MODEL", "EVIDENCE HIERARCHY", "STATE LEDGER",
    "SELF-HEALING RULE", "ACCOUNT REGISTRY / PRIMARY KEY", "HUMAN-RECOGNITION IDENTITY",
    "UID POLICY / PRIVACY REASSURANCE", "WORKSPACE REGISTRY", "ACCOUNT DATABASE ISOLATION",
    "EXISTING-ACCOUNT DISCOVERY", "MIGRATION FROM SINGLE-ACCOUNT LWAI", "ARCHIVED ACCOUNT RECOVERY",
    "CONTEXT SWITCHING", "CROSS-ACCOUNT OPERATIONS", "START-OVER SAFETY", "IDENTITY SANITY CHECK",
    "GUIDED INTERACTION PRINCIPLE", "ADAPTIVE GUIDANCE", "UNOBTRUSIVE INTERVIEW", "AUDIT SESSION STATE",
    "INGESTION MODES", "BATCH / DONE RULE", "active_account_id", "SHARED GEAR / PRESET MODEL",
    "MARGINAL ROI", "SCREENSHOT HANDLING", "GEAR / UPGRADE ORE", "SKILL MEDALS", "EXCLUSIVE WEAPONS",
    "SQUAD-SLOT TECH", "RESEARCH", "DRONE / COMPONENTS / CHIPS", "DECORATIONS",
    "OPTIONAL CLOUD PERSISTENCE", "CAPABILITY DISCOVERY / GRACEFUL DEGRADATION",
    "CLOUD-NEUTRAL WORKSPACE SCHEMA", "ROLLING CONTEXT / RELOAD",
    "UPSTREAM ENGINE / LOCAL STATE SEPARATION", "GITHUB PRODUCTION HUB / DISTRIBUTION CONTRACT",
    "CENTRAL UPDATE CHANNEL", "HUB-AND-SPOKE INVARIANT", "REMOTE BOOTSTRAP / ONE-LINE INSTALL",
    "PRIVACY / SEMI-ANONYMIZED DISTRIBUTION", "DOCUMENTATION-AS-CODE", "COMMAND VOCABULARY",
    "HEALTH / REGRESSION TESTS", "STARTUP BEHAVIOR",
]

REQUIRED_ACCOUNT_MODULE_PHRASES = [
    "UID is optional", "PRIVACY / USER REASSURANCE", "WORKSPACE REGISTRY", "ACCOUNT DATABASE ISOLATION",
    "MIGRATION-FIRST DISCOVERY", "EXISTING-ACCOUNT DISCOVERY", "ARCHIVE / RESTORE", "START-OVER SAFETY",
    "CONTEXT SWITCHING", "CROSS-ACCOUNT OPERATIONS", "IDENTITY SANITY CHECK",
    "MIGRATION FROM SINGLE-ACCOUNT LWAI", "AUDIT SESSION ISOLATION", "REGRESSION INVARIANTS", "active_account_id",
]

REQUIRED_GUIDANCE_MODULE_PHRASES = [
    "MIGRATION-FIRST / ENHANCEMENT-NOT-RESET", "UNOBTRUSIVE INTERVIEW", "AUDIT SESSION STATE",
    "DIRECT CHAT BATCH", "DOCUMENT BUNDLE", "GUIDED CAPTURE", "AUTO-CONTINUE RULE", "BATCH BOUNDARY RULE",
    "MISSING/STALE-ONLY COLLECTION", "ARCHIVED ACCOUNT RECOVERY", "reply `done`", "active_account_id",
]

REQUIRED_REPO_FILES = [
    "README.md", "SECURITY.md", "CONTRIBUTING.md", "engine/BOOTSTRAP.txt", "engine/BOOTSTRAP_FULL.txt",
    "engine/MANIFEST.json", "engine/modules/core/accounts.txt", "engine/modules/core/guidance.txt",
    "contracts/operating-canon.md", "contracts/export-bootstrap.md", "contracts/storage-adapter.md",
    "contracts/account-registry.md", "contracts/release.md", "contracts/migration.md", "contracts/guided-lifecycle-ingestion.md",
    "schemas/workspace-schema.md", "schemas/account-registry.schema.json", "schemas/engine-manifest.schema.json",
    "adapters/provider-matrix.md", "gold-assets/README.md", "gold-assets/manifest.json",
    "releases/LATEST.json", "releases/CHANGELOG.md", "docs/architecture.md", "docs/deployment.md",
    "docs/quick-install.md", "tests/RELEASE_GATES.md", ".github/workflows/validate.yml", ".github/CODEOWNERS",
]

GENERIC_FORBIDDEN = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "oauth/api token": re.compile(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b"),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def version_from(text: str) -> str:
    m = re.search(r"^engine_version:\s*(\S+)", text, re.M)
    if not m:
        fail("engine_version header missing")
    return m.group(1)


def iter_public_text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> None:
    for rel in REQUIRED_REPO_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")

    loader = BOOT.read_text(encoding="utf-8")
    full = FULL.read_text(encoding="utf-8")
    accounts = ACCOUNT_MODULE.read_text(encoding="utf-8")
    guidance = GUIDANCE_MODULE.read_text(encoding="utf-8")
    for phrase in REQUIRED_LOADER_PHRASES:
        if phrase not in loader:
            fail(f"thin loader missing required phrase: {phrase}")
    for phrase in REQUIRED_FULL_PHRASES:
        if phrase not in full:
            fail(f"full fallback missing required phrase: {phrase}")
    for phrase in REQUIRED_ACCOUNT_MODULE_PHRASES:
        if phrase not in accounts:
            fail(f"account module missing required phrase: {phrase}")
    for phrase in REQUIRED_GUIDANCE_MODULE_PHRASES:
        if phrase not in guidance:
            fail(f"guidance module missing required phrase: {phrase}")

    version = version_from(loader)
    if version_from(full) != version:
        fail("BOOTSTRAP_FULL version does not match thin loader")

    latest = json.loads(LATEST.read_text(encoding="utf-8"))
    manifest = json.loads(MODULE_MANIFEST.read_text(encoding="utf-8"))
    account_schema = json.loads(ACCOUNT_SCHEMA.read_text(encoding="utf-8"))
    if account_schema.get("title") != "LWAI Workspace Account Registry":
        fail("account registry schema title missing/unexpected")
    required_schema_fields = set(account_schema.get("required", []))
    if not {"workspace_schema_version", "accounts"}.issubset(required_schema_fields):
        fail("account registry schema missing required workspace fields")
    if "audit_sessions" not in account_schema.get("properties", {}):
        fail("account registry schema missing optional audit_sessions")
    account_item_props = (((account_schema.get("properties") or {}).get("accounts") or {}).get("items") or {}).get("properties") or {}
    if "guidance_level" not in account_item_props:
        fail("account registry account item missing guidance_level")

    if latest.get("engine_version") != version or manifest.get("engine_version") != version:
        fail("release/module manifest version does not match loader")
    if latest.get("sanitized") is not True or manifest.get("sanitized") is not True:
        fail("manifests must assert sanitized=true")
    if latest.get("account_state_included") is not False or manifest.get("account_state_included") is not False:
        fail("manifests must assert account_state_included=false")
    if latest.get("github_repository") != EXPECTED_REPO:
        fail("LATEST github_repository unexpected")
    if latest.get("github_bootstrap_source") != EXPECTED_RAW_BOOT:
        fail("LATEST github_bootstrap_source unexpected")
    if latest.get("preferred_install_url") != EXPECTED_INSTALL_URL:
        fail("LATEST preferred_install_url unexpected")

    module_ids = set()
    entries = manifest.get("modules") or []
    if not entries:
        fail("module manifest has no modules")
    for entry in entries:
        mid = entry.get("module_id")
        path = entry.get("path")
        if not mid or mid in module_ids:
            fail(f"invalid/duplicate module_id: {mid}")
        module_ids.add(mid)
        if not path or not (ROOT / path).is_file():
            fail(f"module path missing for {mid}: {path}")
        text = (ROOT / path).read_text(encoding="utf-8")
        if f"module_id: {mid}" not in text:
            fail(f"module self-identification mismatch: {mid}")
        if "SANITIZED: YES" not in text or "ACCOUNT STATE INCLUDED: NO" not in text:
            fail(f"module sanitization headers missing: {mid}")
    for entry in entries:
        for dep in entry.get("dependencies", []):
            if dep not in module_ids:
                fail(f"unresolved dependency {dep} for {entry.get('module_id')}")
    for required in ("core.operating", "core.persistence", "core.accounts", "core.guidance", "release.runtime", "release.bootstrap"):
        match = next((e for e in entries if e.get("module_id") == required), None)
        if not match or match.get("required") is not True:
            fail(f"required core module not marked required: {required}")
    account_entry = next(e for e in entries if e.get("module_id") == "core.accounts")
    if account_entry.get("path") != "engine/modules/core/accounts.txt":
        fail("core.accounts path unexpected")
    guidance_entry = next(e for e in entries if e.get("module_id") == "core.guidance")
    if guidance_entry.get("path") != "engine/modules/core/guidance.txt":
        fail("core.guidance path unexpected")
    if guidance_entry.get("dependencies") != ["core.operating", "core.persistence", "core.accounts"]:
        fail("core.guidance dependencies unexpected")

    for endpoint in (EXPECTED_REPO, EXPECTED_RAW_BOOT, EXPECTED_RAW_MANIFEST, EXPECTED_MODULE_MANIFEST, EXPECTED_FULL, EXPECTED_INSTALL_URL):
        if endpoint not in loader and endpoint not in full:
            fail(f"Production endpoint missing from runtime: {endpoint}")

    readme = README.read_text(encoding="utf-8")
    if f"**Engine version:** `{version}`" not in readme:
        fail("README Production version mismatch")
    if EXPECTED_INSTALL_URL not in readme:
        fail("README missing preferred installer")
    quick = QUICK_INSTALL.read_text(encoding="utf-8")
    if EXPECTED_INSTALL_URL not in quick or EXPECTED_RAW_BOOT not in quick:
        fail("quick-install documentation missing required installer/fallback")

    for path in iter_public_text_files():
        text = path.read_text(encoding="utf-8")
        for label, pattern in GENERIC_FORBIDDEN.items():
            if pattern.search(text):
                fail(f"{path.relative_to(ROOT)} contains possible {label}")

    archive = ROOT / "releases" / f"{version}.json"
    if not archive.exists():
        fail(f"versioned release manifest missing: {archive.relative_to(ROOT)}")

    print(f"PASS: modular guided multi-account LWAI Production {version} passed repository-wide static release checks")

if __name__ == "__main__":
    main()
