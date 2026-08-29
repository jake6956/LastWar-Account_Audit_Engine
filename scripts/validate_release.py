#!/usr/bin/env python3
"""Fail-closed, release-version-neutral validation for LWAI Production trees."""
from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md", "SECURITY.md", "CONTRIBUTING.md",
    "engine/BOOTSTRAP.txt", "engine/BOOTSTRAP_FULL.txt", "engine/MANIFEST.json",
    "engine/modules/core/operating.txt", "engine/modules/core/persistence.txt",
    "engine/modules/core/accounts.txt", "engine/modules/core/guidance.txt",
    "engine/modules/release/runtime.txt", "engine/modules/release/bootstrap.txt",
    "engine/modules/adapters/storage.txt",
    "contracts/operating-canon.md", "contracts/export-bootstrap.md", "contracts/storage-adapter.md",
    "contracts/account-registry.md", "contracts/release.md", "contracts/migration.md",
    "contracts/guided-lifecycle-ingestion.md", "contracts/runtime-checkpoint-recovery.md",
    "schemas/workspace-schema.md", "schemas/account-registry.schema.json", "schemas/engine-manifest.schema.json",
    "docs/architecture.md", "docs/deployment.md", "docs/quick-install.md", "docs/runtime-recovery.md",
    "adapters/provider-matrix.md", "gold-assets/README.md", "gold-assets/manifest.json",
    "releases/LATEST.json", "releases/MIGRATIONS.json", "releases/CHANGELOG.md", "tests/RELEASE_GATES.md",
    "tests/reference_runtime.py", "tests/test_runtime_behavior.py",
    ".github/workflows/validate.yml", ".github/CODEOWNERS",
]

EXPECTED_REPO = "https://github.com/jake6956/LastWar-Account_Audit_Engine"
EXPECTED_BOOT = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt"
EXPECTED_MANIFEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json"
EXPECTED_FULL = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt"
EXPECTED_LATEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json"
EXPECTED_MIGRATIONS = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/MIGRATIONS.json"
EXPECTED_INSTALL = "https://tinyurl.com/2yxf7f5x"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def read_json(rel: str):
    try:
        return json.loads(read(rel))
    except Exception as exc:
        fail(f"invalid JSON in {rel}: {exc}")


def require(label: str, body: str, tokens: list[str]) -> None:
    missing = [token for token in tokens if token not in body]
    if missing:
        fail(f"{label} missing: {', '.join(missing)}")


def header_value(body: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(\S+)", body, re.M)
    if not match:
        fail(f"{key} header missing")
    return match.group(1)


def version_tuple(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError:
        fail(f"invalid numeric compatibility version: {value}")


def in_range(value: str, lower: str, upper: str) -> bool:
    v, lo, hi = version_tuple(value), version_tuple(lower), version_tuple(upper)
    return lo <= v <= hi


def git_blob_sha(rel: str) -> str:
    result = subprocess.run(
        ["git", "hash-object", rel],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def validate_manifest_schema_shape(schema: dict) -> None:
    required = set(schema.get("required") or [])
    expected = {
        "engine_version", "engine_api_version", "schema_version", "channel",
        "runtime_mode", "sanitized", "account_state_included", "integrity_mode", "modules",
    }
    if not expected.issubset(required):
        fail("engine-manifest schema does not describe current modular manifest")
    module_items = (((schema.get("properties") or {}).get("modules") or {}).get("items") or {})
    module_required = set(module_items.get("required") or [])
    for key in ["module_id", "module_version", "path", "dependencies", "engine_api", "workspace_schema", "integrity"]:
        if key not in module_required:
            fail(f"engine-manifest schema module requirement missing: {key}")


def validate_dag(entries: list[dict]) -> None:
    graph = {entry["module_id"]: list(entry.get("dependencies") or []) for entry in entries}
    state: dict[str, int] = {}

    def visit(node: str) -> None:
        if state.get(node) == 1:
            fail(f"module dependency cycle includes {node}")
        if state.get(node) == 2:
            return
        state[node] = 1
        for dep in graph[node]:
            if dep not in graph:
                fail(f"unresolved dependency {dep} for {node}")
            visit(dep)
        state[node] = 2

    for node in graph:
        visit(node)


def main() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"required file missing: {rel}")

    latest = read_json("releases/LATEST.json")
    manifest = read_json("engine/MANIFEST.json")
    migrations = read_json("releases/MIGRATIONS.json")
    manifest_schema = read_json("schemas/engine-manifest.schema.json")
    account_schema = read_json("schemas/account-registry.schema.json")

    loader = read("engine/BOOTSTRAP.txt")
    full = read("engine/BOOTSTRAP_FULL.txt")
    readme = read("README.md")
    workflow = read(".github/workflows/validate.yml")
    storage = read("engine/modules/adapters/storage.txt")
    storage_contract = read("contracts/storage-adapter.md")
    release_runtime = read("engine/modules/release/runtime.txt")

    version = latest.get("engine_version")
    schema_version = latest.get("schema_version")
    engine_api = latest.get("engine_api_version")
    if not version or not schema_version or not engine_api:
        fail("LATEST missing engine/schema/API identity")

    if header_value(loader, "engine_version") != version or header_value(full, "engine_version") != version:
        fail("loader/full fallback version mismatch with LATEST")
    if header_value(loader, "engine_api_version") != engine_api or header_value(full, "engine_api_version") != engine_api:
        fail("loader/full fallback API mismatch with LATEST")

    for obj, label in [(latest, "LATEST"), (manifest, "MANIFEST")]:
        if obj.get("engine_version") != version or obj.get("schema_version") != schema_version:
            fail(f"{label} version/schema mismatch")
        if obj.get("engine_api_version") != engine_api:
            fail(f"{label} engine API mismatch")
        if obj.get("sanitized") is not True or obj.get("account_state_included") is not False:
            fail(f"{label} sanitization flags invalid")
    if latest.get("channel") != "Production" or manifest.get("channel") != "Production":
        fail("candidate release metadata must identify Production channel")
    if manifest.get("integrity_mode") != "git_blob_sha1":
        fail("unsupported manifest integrity mode")

    if latest.get("github_repository") != EXPECTED_REPO:
        fail("LATEST repository authority invalid")
    if latest.get("github_bootstrap_source") != EXPECTED_BOOT:
        fail("LATEST bootstrap authority invalid")
    if latest.get("module_manifest_source") != EXPECTED_MANIFEST:
        fail("LATEST manifest authority invalid")
    if latest.get("full_fallback_source") != EXPECTED_FULL:
        fail("LATEST fallback authority invalid")
    if latest.get("migration_graph_source") != EXPECTED_MIGRATIONS:
        fail("LATEST migration graph authority invalid")
    if latest.get("preferred_install_url") != EXPECTED_INSTALL:
        fail("LATEST installer invalid")

    require("loader", loader, [
        "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "MODULE INTEGRITY",
        "CAPABILITY DISCOVERY", "RECOVERY-FIRST STARTUP", "MIGRATION-FIRST ACCOUNT DISCOVERY",
        "WAITING_USER", "active_account_id", EXPECTED_REPO, EXPECTED_LATEST,
        EXPECTED_MANIFEST, EXPECTED_MIGRATIONS, EXPECTED_FULL, EXPECTED_INSTALL,
    ])
    if len(loader.encode("utf-8")) > 9000:
        fail("thin loader exceeds 9KB bounded orchestration budget")
    for domain_token in [
        "GEAR / UPGRADE ORE", "SKILL MEDALS", "EXCLUSIVE WEAPONS",
        "DRONE / COMPONENTS / CHIPS", "EVENT STORES / BLACK MARKET / BOUNTY",
        "COMBAT DIAGNOSIS",
    ]:
        if domain_token in loader:
            fail(f"thin loader contains domain playbook: {domain_token}")

    require("full fallback", full, [
        "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO", "RUNTIME CHECKPOINT MODEL",
        "RUNTIME JOURNAL", "RECOVERY-FIRST STARTUP", "WRITE-AHEAD / IDEMPOTENCY",
        "WAITING_USER", "STORAGE ADAPTER API", "MODULE INTEGRITY", "ENGINE API / COMPATIBILITY",
        "GEAR / UPGRADE ORE", "SKILL MEDALS", "RESEARCH", "DRONE / COMPONENTS / CHIPS",
        "COMBAT DIAGNOSIS", "EVENT STORES / BLACK MARKET / BOUNTY",
        EXPECTED_REPO, EXPECTED_BOOT, EXPECTED_MANIFEST, EXPECTED_MIGRATIONS, EXPECTED_FULL, EXPECTED_INSTALL,
    ])

    require("storage adapter", storage, [
        "module_version: 2026-08-29.12.1", "storage-api/1", "CAPABILITY API",
        "atomic_append", "compare_and_swap", "PERSISTENCE PROFILES", "AUTHORITATIVE JOURNAL RULE",
    ])
    require("storage contract", storage_contract, [
        "Version: 2026-08-29.12", "storage-api/1", "Persistence profiles",
        "Authoritative journal rule", "compare-and-swap",
    ])
    require("release runtime", release_runtime, [
        "module_version: 2026-08-29.12.1", "MODULE INTEGRITY", "ENGINE API / COMPATIBILITY",
        "BEHAVIORAL VALIDATION", "LOADER BUDGET",
    ])

    validate_manifest_schema_shape(manifest_schema)

    entries = manifest.get("modules") or []
    if not entries:
        fail("manifest contains no modules")
    ids = [entry.get("module_id") for entry in entries]
    if None in ids or len(ids) != len(set(ids)):
        fail("module ids missing or duplicated")
    validate_dag(entries)

    by_id = {entry["module_id"]: entry for entry in entries}
    required_ids = ["core.operating", "core.persistence", "core.accounts", "core.guidance", "release.runtime", "release.bootstrap"]
    for module_id in required_ids:
        if module_id not in by_id or by_id[module_id].get("required") is not True:
            fail(f"required module not marked required: {module_id}")

    for entry in entries:
        rel = entry.get("path")
        if not rel or not (ROOT / rel).is_file():
            fail(f"missing module path for {entry.get('module_id')}")
        body = read(rel)
        require(entry["module_id"], body, [
            f"module_id: {entry['module_id']}",
            f"module_version: {entry['module_version']}",
            "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO",
        ])
        compat_api = entry.get("engine_api") or {}
        compat_schema = entry.get("workspace_schema") or {}
        if not in_range(engine_api, compat_api.get("min", ""), compat_api.get("max", "")):
            fail(f"engine API incompatible for {entry['module_id']}")
        if not in_range(schema_version, compat_schema.get("min", ""), compat_schema.get("max", "")):
            fail(f"workspace schema incompatible for {entry['module_id']}")
        integrity = entry.get("integrity") or {}
        if integrity.get("algorithm") != "git_blob_sha1" or not re.fullmatch(r"[0-9a-f]{40}", integrity.get("digest", "")):
            fail(f"invalid integrity metadata for {entry['module_id']}")
        actual = git_blob_sha(rel)
        if actual != integrity["digest"]:
            fail(f"integrity mismatch for {entry['module_id']}: manifest={integrity['digest']} actual={actual}")

    if by_id["core.guidance"].get("dependencies") != ["core.operating", "core.persistence", "core.accounts"]:
        fail("core.guidance dependency graph invalid")

    if account_schema.get("title") != "LWAI Workspace Account Registry":
        fail("account registry schema identity invalid")
    if "audit_sessions" not in (account_schema.get("properties") or {}):
        fail("account registry schema lost audit_sessions")

    edges = migrations.get("edges") or []
    migration = latest.get("migration") or {}
    migration_from = migration.get("from")
    if migration_from:
        matching = [edge for edge in edges if edge.get("from") == migration_from and edge.get("to") == version]
        if not matching:
            fail(f"missing migration graph edge {migration_from} -> {version}")
        edge = matching[0]
        if edge.get("schema_to") != schema_version or edge.get("local_state_action") != "preserve":
            fail("migration edge does not preserve expected schema/local state")
        if edge.get("requires_user_reonboarding") is not False:
            fail("hardening release must not require user re-onboarding")

    archive_rel = f"releases/{version}.json"
    if not (ROOT / archive_rel).is_file():
        fail(f"versioned release manifest missing: {archive_rel}")
    archive = read_json(archive_rel)
    if archive.get("engine_version") != version or archive.get("sanitized") is not True or archive.get("account_state_included") is not False:
        fail("versioned release manifest invalid")

    if f"**Engine version:** `{version}`" not in readme or EXPECTED_INSTALL not in readme:
        fail("README Production identity/install mismatch")
    require("workflow", workflow, [
        "python scripts/validate_release.py",
        "python -m unittest -v test_runtime_behavior.py",
        "fetch-depth: 0",
    ])

    public_text = "\n".join(
        read(rel) for rel in REQUIRED_FILES if rel.endswith((".md", ".txt", ".json", ".yml", ".py"))
    )
    private_markers = ["CP-20260829-011", "J-20260829-011", "PRIVATE_RC_STAGED"]
    for marker in private_markers:
        if marker in public_text:
            fail(f"candidate contains private release marker: {marker}")
    if re.search(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b", public_text, re.I):
        fail("candidate contains possible credential token")
    if re.search(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY", public_text):
        fail("candidate contains possible private key")

    print(
        f"PASS: LWAI Production {version} / API {engine_api} / schema {schema_version} "
        f"passed metadata, graph, integrity, privacy and loader-boundary checks"
    )


if __name__ == "__main__":
    main()
