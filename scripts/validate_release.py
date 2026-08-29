#!/usr/bin/env python3
"""Static release checks for the public LWAI production tree."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "engine" / "BOOTSTRAP.txt"
MANIFEST = ROOT / "releases" / "LATEST.json"

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
    "DOCUMENTATION-AS-CODE",
    "COMMAND VOCABULARY",
    "HEALTH / REGRESSION TESTS",
    "STARTUP BEHAVIOR",
]

REQUIRED_REPO_FILES = [
    "README.md",
    "engine/BOOTSTRAP.txt",
    "contracts/operating-canon.md",
    "contracts/export-bootstrap.md",
    "contracts/storage-adapter.md",
    "contracts/release.md",
    "schemas/workspace-schema.md",
    "adapters/provider-matrix.md",
    "gold-assets/README.md",
    "releases/LATEST.json",
    "releases/CHANGELOG.md",
    "docs/architecture.md",
]

# Generic public-repo safety checks. A private Prod-Dev denylist should be run
# before promotion and is deliberately NOT committed to this public repository.
GENERIC_FORBIDDEN = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "oauth token": re.compile(r"\b(?:ghp|github_pat|sk)-[A-Za-z0-9_\-]{12,}\b"),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def main() -> None:
    for rel in REQUIRED_REPO_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")

    text = BOOT.read_text(encoding="utf-8")
    for phrase in REQUIRED_BOOTSTRAP_PHRASES:
        if phrase not in text:
            fail(f"bootstrap missing required section/phrase: {phrase}")

    for label, pattern in GENERIC_FORBIDDEN.items():
        if pattern.search(text):
            fail(f"bootstrap contains possible {label}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    boot_match = re.search(r"^engine_version:\s*(\S+)", text, re.M)
    if not boot_match:
        fail("bootstrap engine_version header missing")
    if manifest.get("engine_version") != boot_match.group(1):
        fail("manifest engine_version does not match bootstrap")
    if manifest.get("sanitized") is not True:
        fail("manifest must assert sanitized=true")
    if manifest.get("account_state_included") is not False:
        fail("manifest must assert account_state_included=false")

    print(f"PASS: LWAI production tree {manifest['engine_version']} passed static release checks")


if __name__ == "__main__":
    main()
