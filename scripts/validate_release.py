#!/usr/bin/env python3
"""Static fail-closed checks for the public LWAI Production tree."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "engine" / "BOOTSTRAP.txt"
MANIFEST = ROOT / "releases" / "LATEST.json"
README = ROOT / "README.md"

REQUIRED_BOOTSTRAP_PHRASES = [
    "SANITIZED: YES",
    "ACCOUNT STATE INCLUDED: NO",
    "STEP 0 — REASONING MODE",
    "CORE OPERATING MODEL",
    "EVIDENCE HIERARCHY",
    "SELF-HEALING RULE",
    "SHARED GEAR / PRESET MODEL",
    "MARGINAL ROI",
    "SCREENSHOT HANDLING",
    "SKILL MEDALS",
    "EXCLUSIVE WEAPONS",
    "SQUAD-SLOT TECH",
    "RESEARCH",
    "DRONE / COMPONENTS / CHIPS",
    "DECORATIONS",
    "OPTIONAL CLOUD PERSISTENCE",
    "CAPABILITY DISCOVERY / GRACEFUL DEGRADATION",
    "CLOUD-NEUTRAL WORKSPACE SCHEMA",
    "ROLLING CONTEXT / RELOAD",
    "UPSTREAM ENGINE / LOCAL STATE SEPARATION",
    "GITHUB PRODUCTION HUB / DISTRIBUTION CONTRACT",
    "CENTRAL UPDATE CHANNEL",
    "HUB-AND-SPOKE INVARIANT",
    "DOCUMENTATION-AS-CODE",
    "COMMAND VOCABULARY",
    "HEALTH / REGRESSION TESTS",
    "STARTUP BEHAVIOR",
]

REQUIRED_REPO_FILES = [
    "README.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "engine/BOOTSTRAP.txt",
    "contracts/operating-canon.md",
    "contracts/export-bootstrap.md",
    "contracts/storage-adapter.md",
    "contracts/release.md",
    "contracts/migration.md",
    "schemas/workspace-schema.md",
    "schemas/engine-manifest.schema.json",
    "adapters/provider-matrix.md",
    "gold-assets/README.md",
    "gold-assets/manifest.json",
    "releases/LATEST.json",
    "releases/CHANGELOG.md",
    "docs/architecture.md",
    "docs/deployment.md",
    "tests/RELEASE_GATES.md",
    ".github/workflows/validate.yml",
    ".github/CODEOWNERS",
]

EXPECTED_REPO = "https://github.com/jake6956/LastWar-Account_Audit_Engine"
EXPECTED_RAW_BOOT = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/engine/BOOTSTRAP.txt"
EXPECTED_RAW_MANIFEST = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/main/releases/LATEST.json"

# Generic safety checks. The private Prod-Dev release gate also uses an
# account-specific denylist that must never be committed to the public repo.
GENERIC_FORBIDDEN = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "oauth/api token": re.compile(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b"),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}

TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def iter_public_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> None:
    for rel in REQUIRED_REPO_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")

    bootstrap = BOOT.read_text(encoding="utf-8")
    for phrase in REQUIRED_BOOTSTRAP_PHRASES:
        if phrase not in bootstrap:
            fail(f"bootstrap missing required section/phrase: {phrase}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    boot_match = re.search(r"^engine_version:\s*(\S+)", bootstrap, re.M)
    if not boot_match:
        fail("bootstrap engine_version header missing")
    version = boot_match.group(1)

    if manifest.get("engine_version") != version:
        fail("manifest engine_version does not match bootstrap")
    if manifest.get("sanitized") is not True:
        fail("manifest must assert sanitized=true")
    if manifest.get("account_state_included") is not False:
        fail("manifest must assert account_state_included=false")
    if manifest.get("github_repository") != EXPECTED_REPO:
        fail("manifest github_repository is missing or unexpected")
    if manifest.get("github_bootstrap_source") != EXPECTED_RAW_BOOT:
        fail("manifest github_bootstrap_source is missing or unexpected")

    for endpoint in (EXPECTED_REPO, EXPECTED_RAW_BOOT, EXPECTED_RAW_MANIFEST):
        if endpoint not in bootstrap:
            fail(f"bootstrap missing production endpoint: {endpoint}")

    readme = README.read_text(encoding="utf-8")
    if f"**Engine version:** `{version}`" not in readme:
        fail("README current Production version does not match manifest/bootstrap")

    # Scan the whole committed public text tree rather than only the bootstrap.
    # An account-specific/private denylist remains a separate pre-promotion gate.
    for path in iter_public_text_files():
        text = path.read_text(encoding="utf-8")
        for label, pattern in GENERIC_FORBIDDEN.items():
            if pattern.search(text):
                fail(f"{path.relative_to(ROOT)} contains possible {label}")

    archive = ROOT / "releases" / f"{version}.json"
    if not archive.exists():
        fail(f"versioned release manifest missing: {archive.relative_to(ROOT)}")

    print(f"PASS: LWAI Production {version} passed repository-wide static release checks")


if __name__ == "__main__":
    main()
