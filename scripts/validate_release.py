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
    "engine/modules/release/runtime.txt", "engine/modules/release/resolver.txt",
    "engine/modules/release/updater.txt", "engine/modules/release/bootstrap.txt",
    "engine/modules/adapters/storage.txt",
    "contracts/operating-canon.md", "contracts/export-bootstrap.md", "contracts/storage-adapter.md",
    "contracts/account-registry.md", "contracts/release.md", "contracts/migration.md",
    "contracts/guided-lifecycle-ingestion.md", "contracts/runtime-checkpoint-recovery.md",
    "contracts/user-experience.md", "contracts/bootstrap-resolution.md",
    "schemas/workspace-schema.md", "schemas/account-registry.schema.json", "schemas/engine-manifest.schema.json",
    "docs/architecture.md", "docs/deployment.md", "docs/quick-install.md", "docs/runtime-recovery.md",
    "adapters/provider-matrix.md", "gold-assets/README.md", "gold-assets/manifest.json",
    "releases/LATEST.json", "releases/MIGRATIONS.json", "releases/CHANGELOG.md", "tests/RELEASE_GATES.md",
    "tests/reference_runtime.py", "tests/test_runtime_behavior.py", "tests/test_user_experience_contract.py",
    "tests/test_bootstrap_resolution_contract.py", ".github/workflows/validate.yml", ".github/CODEOWNERS",
]

REPO = "https://github.com/jake6956/LastWar-Account_Audit_Engine"
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
RAW_BOOT = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt"
RAW_MANIFEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/MANIFEST.json"
RAW_FULL = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP_FULL.txt"
RAW_LATEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json"
RAW_MIGRATIONS = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/MIGRATIONS.json"
LEGACY_SHORTENER_PREFIX = "https://tinyurl.com/"
CURRENT_SCHEMA = "2.3"
HISTORICAL_SCHEMA_PATH = [("2.1", "2.2"), ("2.2", "2.3")]
MIGRATION_CAPABLE = {
    "core.operating", "core.persistence", "core.accounts", "core.guidance",
    "release.runtime", "release.resolver", "release.updater", "release.bootstrap", "adapters.storage",
}
REQUIRED_MODULES = {
    "core.operating", "core.persistence", "core.accounts", "core.guidance",
    "release.runtime", "release.resolver", "release.updater", "release.bootstrap",
}


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
    except (ValueError, AttributeError):
        fail(f"invalid numeric compatibility version: {value}")


def in_range(value: str, lower: str, upper: str) -> bool:
    return version_tuple(lower) <= version_tuple(value) <= version_tuple(upper)


def git_blob_sha(rel: str) -> str:
    result = subprocess.run(["git", "hash-object", rel], cwd=ROOT, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def validate_manifest_schema_shape(schema: dict) -> None:
    required = set(schema.get("required") or [])
    expected = {"engine_version", "engine_api_version", "schema_version", "channel", "runtime_mode", "sanitized", "account_state_included", "integrity_mode", "modules"}
    if not expected.issubset(required):
        fail("engine-manifest schema does not describe current modular manifest")
    module_items = (((schema.get("properties") or {}).get("modules") or {}).get("items") or {})
    module_required = set(module_items.get("required") or [])
    for key in ["module_id", "module_version", "path", "dependencies", "engine_api", "workspace_schema", "integrity"]:
        if key not in module_required:
            fail(f"engine-manifest schema module requirement missing: {key}")


def validate_dag(entries: list[dict]) -> None:
    graph = {e["module_id"]: list(e.get("dependencies") or []) for e in entries}
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


def validate_workspace_schema_graph(migrations: dict) -> None:
    if migrations.get("workspace_schema_current") != CURRENT_SCHEMA:
        fail("migration graph current workspace schema mismatch")
    pairs = {(e.get("from"), e.get("to")): e for e in migrations.get("workspace_schema_edges") or []}
    for pair in HISTORICAL_SCHEMA_PATH:
        edge = pairs.get(pair)
        if not edge:
            fail(f"missing historical workspace schema edge {pair[0]} -> {pair[1]}")
        if edge.get("local_state_action") != "preserve" or edge.get("requires_user_reonboarding") is not False or edge.get("requires_account_rewrite") is not False:
            fail(f"workspace schema edge {pair[0]} -> {pair[1]} is not nondestructive")


def validate_modules(entries: list[dict], engine_api: str, schema_version: str) -> dict[str, dict]:
    by_id = {e["module_id"]: e for e in entries}
    for module_id in REQUIRED_MODULES:
        if module_id not in by_id or by_id[module_id].get("required") is not True:
            fail(f"required module not marked required: {module_id}")
    for entry in entries:
        module_id = entry["module_id"]
        rel = entry.get("path")
        if not rel or not (ROOT / rel).is_file():
            fail(f"missing module path for {module_id}")
        body = read(rel)
        require(module_id, body, [f"module_id: {module_id}", f"module_version: {entry['module_version']}", "SANITIZED: YES", "ACCOUNT STATE INCLUDED: NO"])
        api = entry.get("engine_api") or {}; schema = entry.get("workspace_schema") or {}
        if not in_range(engine_api, api.get("min", ""), api.get("max", "")):
            fail(f"engine API incompatible for {module_id}")
        if not in_range(schema_version, schema.get("min", ""), schema.get("max", "")):
            fail(f"current workspace schema incompatible for {module_id}")
        if module_id in MIGRATION_CAPABLE:
            if schema.get("min") != "2.1" or schema.get("max") != CURRENT_SCHEMA:
                fail(f"migration-capable module does not span 2.1-{CURRENT_SCHEMA}: {module_id}")
        elif entry.get("load_class") == "domain_on_demand":
            if schema.get("min") != CURRENT_SCHEMA or schema.get("max") != CURRENT_SCHEMA:
                fail(f"domain module must remain current-schema-only: {module_id}")
        integrity = entry.get("integrity") or {}
        if integrity.get("algorithm") != "git_blob_sha1" or not re.fullmatch(r"[0-9a-f]{40}", integrity.get("digest", "")):
            fail(f"invalid integrity metadata for {module_id}")
        actual = git_blob_sha(rel)
        if actual != integrity["digest"]:
            fail(f"integrity mismatch for {module_id}: manifest={integrity['digest']} actual={actual}")
    if by_id["core.guidance"].get("dependencies") != ["core.operating", "core.persistence", "core.accounts"]:
        fail("core.guidance dependency graph invalid")
    if "release.resolver" not in by_id["release.updater"].get("dependencies", []):
        fail("release.updater must depend on release.resolver")
    for dep in ["release.resolver", "release.updater"]:
        if dep not in by_id["release.bootstrap"].get("dependencies", []):
            fail(f"release.bootstrap must depend on {dep}")
    return by_id


def validate_loader_boundary(loader: str) -> None:
    if len(loader.encode("utf-8")) > 4096:
        fail("Stage-1 loader exceeds 4KiB orchestration budget")
    require("Stage-1 loader", loader, [
        "Stage-1 orchestration only", "LIVE REF / CACHE SAFETY", "PINNED SNAPSHOT",
        "MODULE HANDOFF", "release.resolver", "release.updater", "refresh engine",
        "LOCAL STATE", "WAITING_USER", LIVE_REF,
    ])
    forbidden = [
        "Before we build your account", "Allow always", "Google Drive", "Dropbox", "OneDrive", "Box",
        "screenname", "strategic baseline", "GEAR / UPGRADE ORE", "SKILL MEDALS",
        "DRONE / COMPONENTS / CHIPS", "EVENT STORES / BLACK MARKET / BOUNTY", "COMBAT DIAGNOSIS",
        "domain.season-intelligence",
    ]
    for token in forbidden:
        if token in loader:
            fail(f"Stage-1 loader leaked delegated policy/domain content: {token}")


def validate_resolution_contract(latest: dict, loader: str, full: str, readme: str) -> None:
    resolver = read("engine/modules/release/resolver.txt")
    updater = read("engine/modules/release/updater.txt")
    bootstrap = read("engine/modules/release/bootstrap.txt")
    contract = read("contracts/bootstrap-resolution.md")
    if latest.get("preferred_install_url") != LIVE_REF:
        fail("LATEST preferred_install_url is not live branch-ref endpoint")
    if latest.get("live_ref_source") != LIVE_REF or latest.get("mutable_source_urls_are_authority") is not False:
        fail("LATEST live-ref/cache authority metadata invalid")
    for label, body in [("loader", loader), ("full", full), ("resolver", resolver), ("bootstrap", bootstrap), ("resolution contract", contract), ("README", readme)]:
        if LIVE_REF not in body:
            fail(f"{label} missing live Production ref")
    require("resolver", resolver, [
        "LIVE REF RESOLUTION", "PIN-ONCE SNAPSHOT", "production_commit_sha",
        "40-lowercase-hex", "Do not fabricate a SHA", "cached raw `main` files",
        "Fresh install with no live ref capability", "release.updater",
    ])
    require("updater", updater, ["`release.resolver` is the only Production freshness authority", "SAME C", "Never mix commits", "refresh engine"])
    require("resolution contract", contract, ["Stage 0", "Stage 1", "Pin once", "4 KiB", "search/index caching"])
    for label, body in [("loader", loader), ("full fallback", full), ("release.bootstrap", bootstrap)]:
        if LEGACY_SHORTENER_PREFIX in body:
            fail(f"{label} still advertises/requires legacy shortener")


def validate_storage_security(full: str) -> None:
    storage = read("engine/modules/adapters/storage.txt")
    contract = read("contracts/storage-adapter.md")
    ux = read("contracts/user-experience.md")
    combined = "\n".join([storage, contract, ux, full])
    require("storage adapter", storage, [
        "ABSOLUTE WORKSPACE BOUNDARY", "USER-VISIBLE SECURITY REASSURANCE", "storage-api/1",
        "Never silently choose Google Drive", "Allow always", "CONNECTION VERIFICATION",
        "Workspace-only guardrail is active", "Dropbox", "OneDrive", "Box",
    ])
    for phrase in [
        "outside that workspace", "other ChatGPT/app workspaces", "broader connector",
        "never asks for passwords", "provider-wide", "unrelated provider",
    ]:
        if phrase.lower() not in combined.lower():
            fail(f"workspace security contract missing concept: {phrase}")
    if "LWAI is explicitly restricted to its own Last War workspace" not in combined:
        fail("user-facing workspace guardrail reassurance missing")


def validate_friendly_ux(full: str) -> None:
    guidance = read("engine/modules/core/guidance.txt")
    persistence = read("engine/modules/core/persistence.txt")
    storage = read("engine/modules/adapters/storage.txt")
    bootstrap = read("engine/modules/release/bootstrap.txt")
    updater = read("engine/modules/release/updater.txt")
    contract = read("contracts/user-experience.md")
    question = "would you like me to use private cloud storage"
    for label, body in [("full", full), ("guidance", guidance), ("persistence", persistence), ("UX contract", contract)]:
        if question not in body.lower():
            fail(f"{label} lost early plain-language cloud choice")
    combined = "\n".join([full, guidance, persistence, storage, bootstrap, contract]).lower()
    if "never default to google drive" not in combined and "never silently choose google drive" not in combined:
        fail("provider flow does not prohibit silent Google Drive default")
    for label, body in [("full", full), ("guidance", guidance), ("storage", storage), ("UX contract", contract)]:
        require(label, body, ["Google Drive", "Allow always"])
    require("friendly updater", updater, ["FRIENDLY UPDATE UX", "Checking for updates", "LWAI updated successfully", "audit yourself"])
    for token in ["WAITING_USER", "strategic baseline", "first", "screenname"]:
        if token.lower() not in combined:
            fail(f"guided onboarding contract lost: {token}")


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

    version = latest.get("engine_version"); schema_version = latest.get("schema_version"); engine_api = latest.get("engine_api_version")
    if not version or not schema_version or not engine_api:
        fail("LATEST missing engine/schema/API identity")
    if schema_version != CURRENT_SCHEMA:
        fail("Production current schema unexpectedly changed")
    if header_value(loader, "engine_version") != version or header_value(full, "engine_version") != version:
        fail("loader/full fallback version mismatch with LATEST")
    if header_value(loader, "engine_api_version") != engine_api or header_value(full, "engine_api_version") != engine_api:
        fail("loader/full fallback API mismatch with LATEST")
    for obj, label in [(latest, "LATEST"), (manifest, "MANIFEST")]:
        if obj.get("engine_version") != version or obj.get("schema_version") != schema_version or obj.get("engine_api_version") != engine_api:
            fail(f"{label} identity mismatch")
        if obj.get("sanitized") is not True or obj.get("account_state_included") is not False:
            fail(f"{label} sanitization flags invalid")
        if obj.get("channel") != "Production":
            fail(f"{label} must identify Production channel")
    if manifest.get("integrity_mode") != "git_blob_sha1":
        fail("unsupported manifest integrity mode")

    # Mutable raw URLs may remain as convenience metadata, but cannot be authority.
    expected_metadata = {
        "github_repository": REPO,
        "github_bootstrap_source": RAW_BOOT,
        "module_manifest_source": RAW_MANIFEST,
        "full_fallback_source": RAW_FULL,
        "migration_graph_source": RAW_MIGRATIONS,
    }
    for key, expected in expected_metadata.items():
        if latest.get(key) != expected:
            fail(f"LATEST {key} invalid")

    validate_loader_boundary(loader)
    validate_resolution_contract(latest, loader, full, readme)
    validate_storage_security(full)
    validate_friendly_ux(full)
    validate_manifest_schema_shape(manifest_schema)
    validate_workspace_schema_graph(migrations)

    entries = manifest.get("modules") or []
    if not entries:
        fail("manifest contains no modules")
    ids = [e.get("module_id") for e in entries]
    if None in ids or len(ids) != len(set(ids)):
        fail("module ids missing or duplicated")
    validate_dag(entries)
    validate_modules(entries, engine_api, schema_version)

    if account_schema.get("title") != "LWAI Workspace Account Registry" or "audit_sessions" not in (account_schema.get("properties") or {}):
        fail("account registry schema identity/coverage invalid")

    migration = latest.get("migration") or {}
    migration_from = migration.get("from")
    if migration_from:
        matching = [e for e in migrations.get("edges") or [] if e.get("from") == migration_from and e.get("to") == version]
        if not matching:
            fail(f"missing migration graph edge {migration_from} -> {version}")
        edge = matching[0]
        if edge.get("schema_to") != schema_version or edge.get("local_state_action") != "preserve" or edge.get("requires_user_reonboarding") is not False or edge.get("requires_account_rewrite") is not False:
            fail("release migration edge is not state-preserving")

    archive_rel = f"releases/{version}.json"
    if not (ROOT / archive_rel).is_file():
        fail(f"versioned release manifest missing: {archive_rel}")
    archive = read_json(archive_rel)
    if archive.get("engine_version") != version or archive.get("schema_version") != schema_version or archive.get("sanitized") is not True or archive.get("account_state_included") is not False:
        fail("versioned release manifest identity/privacy invalid")

    if f"**Engine version:** `{version}`" not in readme or LIVE_REF not in readme:
        fail("README Production identity/install mismatch")
    require("README", readme, ["Stage-0 bootloader", "4 KiB", "Do not use the old TinyURL installer", "Allow always", "workspace-only", "release.resolver"])
    require("workflow", workflow, ["python scripts/validate_release.py", "test_runtime_behavior.py", "test_user_experience_contract.py", "test_bootstrap_resolution_contract.py", "fetch-depth: 0"])

    # Standalone fallback remains genuinely useful when modular load fails.
    require("full fallback", full, [
        "GLOBAL EPISTEMIC INTEGRITY CONTRACT", "WORKSPACE SCHEMA MIGRATION", "MIGRATION-COMPATIBLE BOOTSTRAP",
        "RUNTIME CHECKPOINT MODEL", "RUNTIME JOURNAL", "RECOVERY-FIRST STARTUP", "WRITE-AHEAD / IDEMPOTENCY",
        "STORAGE ADAPTER API", "GEAR / UPGRADE ORE", "SKILL MEDALS", "RESEARCH", "DRONE / COMPONENTS / CHIPS",
        "EVENT STORES / BLACK MARKET / BOUNTY", "COMBAT DIAGNOSIS", "SEASON INTELLIGENCE",
    ])

    public_text = "\n".join(read(rel) for rel in REQUIRED_FILES if rel.endswith((".md", ".txt", ".json", ".yml", ".py")))
    for marker in ["CP-20260829-011", "J-20260829-011", "CP-20260829-015", "J-20260829-015", "PRIVATE_RC_STAGED"]:
        if marker in public_text:
            fail(f"candidate contains private release marker: {marker}")
    if re.search(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b", public_text, re.I):
        fail("candidate contains possible credential token")
    if re.search(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY", public_text):
        fail("candidate contains possible private key")

    print(f"PASS: LWAI Production {version} / API {engine_api} / schema {schema_version} passed live-ref, pinned-snapshot, graph, integrity, privacy, workspace-security, migration, UX and 4KiB loader-boundary checks")


if __name__ == "__main__":
    main()
