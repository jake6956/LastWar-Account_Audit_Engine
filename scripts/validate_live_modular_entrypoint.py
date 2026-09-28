#!/usr/bin/env python3
"""Validate the deployed opt-in modular LastWarAI.com transport without changing default routes."""
from __future__ import annotations

import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

PUBLIC = "https://lastwarai.com"
MODULAR = f"{PUBLIC}/modular"
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"FAIL: live modular transport: {message}")
    raise SystemExit(1)


def fetch(url: str, accept: str = "text/plain,*/*;q=0.1") -> tuple[int, object, str]:
    req = Request(url, headers={"User-Agent": "LWAI-Modular-Live-Validation/1.0", "Accept": accept})
    try:
        with urlopen(req, timeout=20) as response:
            return getattr(response, "status", 200), response.headers, response.read(262144).decode("utf-8")
    except HTTPError as exc:
        body = exc.read(32768).decode("utf-8", errors="replace")
        return exc.code, exc.headers, body
    except (URLError, TimeoutError, UnicodeDecodeError) as exc:
        fail(f"could not retrieve {url}: {exc}")


def main() -> None:
    ref_status, _, ref_body = fetch(LIVE_REF, "application/vnd.github+json")
    if ref_status != 200:
        fail(f"GitHub live ref returned {ref_status}")
    try:
        live_sha = json.loads(ref_body)["commit"]["sha"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        fail(f"could not parse GitHub live SHA: {exc}")
    if not SHA_RE.fullmatch(live_sha):
        fail("GitHub live SHA invalid")

    root_status, root_headers, root_body = fetch(PUBLIC)
    if root_status != 200:
        fail(f"default root returned {root_status}")
    if root_headers.get("X-LWAI-Transport-Version") != "3.1":
        fail("default root transport version changed")
    if root_headers.get("X-LWAI-Commit") != live_sha:
        fail("default root SHA does not match live Production")
    if "COMPLETE PRODUCTION FALLBACK" not in root_body:
        fail("default root no longer contains complete fallback")

    status, headers, body = fetch(MODULAR)
    if status != 200:
        fail(f"/modular returned {status}; candidate Worker may not be deployed")
    if headers.get("X-LWAI-Transport-Version") != "3.2-modular-optin":
        fail("/modular transport-version header mismatch")
    if headers.get("X-LWAI-Commit") != live_sha:
        fail("/modular SHA does not match live Production")
    if headers.get("X-Robots-Tag", "").lower() != "noindex, nofollow":
        fail("/modular must be noindex, nofollow")
    if "no-store" not in headers.get("Cache-Control", "").lower():
        fail("/modular must be no-store")
    snapshot_base = headers.get("X-LWAI-Snapshot-Base", "")
    expected_base = f"{PUBLIC}/snapshot/{live_sha}/"
    if snapshot_base != expected_base:
        fail(f"snapshot base mismatch: {snapshot_base!r}")
    for token in (
        "OPT-IN MODULAR CONFIGURATION",
        f"RESOLVED_PRODUCTION_COMMIT: {live_sha}",
        f"FIRST_PARTY_SNAPSHOT_BASE: {expected_base}",
        "PRODUCTION BOOTSTRAP",
        "SANITIZED: YES",
        "ACCOUNT STATE INCLUDED: NO",
    ):
        if token not in body:
            fail(f"/modular body missing {token!r}")
    if "COMPLETE PRODUCTION FALLBACK" in body:
        fail("/modular unexpectedly contains BOOTSTRAP_FULL")

    manifest_url = expected_base + "engine/MANIFEST.json"
    m_status, m_headers, m_body = fetch(manifest_url, "application/json,*/*;q=0.1")
    if m_status != 200:
        fail(f"snapshot manifest returned {m_status}")
    if m_headers.get("X-LWAI-Commit") != live_sha:
        fail("snapshot manifest SHA mismatch")
    if m_headers.get("X-LWAI-Snapshot-Path") != "engine/MANIFEST.json":
        fail("snapshot manifest path header mismatch")
    if "immutable" not in m_headers.get("Cache-Control", "").lower():
        fail("snapshot manifest is not immutable")
    try:
        manifest = json.loads(m_body)
    except json.JSONDecodeError as exc:
        fail(f"snapshot manifest is invalid JSON: {exc}")
    if manifest.get("channel") != "Production" or manifest.get("sanitized") is not True:
        fail("snapshot manifest Production/sanitization identity invalid")
    if manifest.get("account_state_included") is not False:
        fail("snapshot manifest unexpectedly includes account state")

    module_url = expected_base + "engine/modules/core/operating.txt"
    mod_status, mod_headers, mod_body = fetch(module_url)
    if mod_status != 200:
        fail(f"snapshot module returned {mod_status}")
    if mod_headers.get("X-LWAI-Commit") != live_sha:
        fail("snapshot module SHA mismatch")
    if "module_id: core.operating" not in mod_body:
        fail("snapshot module body mismatch")

    for bad in (
        f"{PUBLIC}/snapshot/{live_sha}/README.md",
        f"{PUBLIC}/snapshot/{live_sha}/contracts/bootstrap-resolution.md",
        f"{PUBLIC}/snapshot/NOT-A-SHA/engine/MANIFEST.json",
    ):
        bad_status, _, _ = fetch(bad)
        if bad_status != 404:
            fail(f"disallowed snapshot path did not return 404: {bad} -> {bad_status}")

    about_status, _, about_body = fetch(f"{PUBLIC}/about", "text/html,*/*;q=0.1")
    if about_status != 200:
        fail("/about unavailable")
    if "/modular" in about_body:
        fail("opt-in modular path leaked into default About discovery")

    sitemap_status, _, sitemap_body = fetch(f"{PUBLIC}/sitemap.xml", "application/xml,*/*;q=0.1")
    if sitemap_status != 200:
        fail("/sitemap.xml unavailable")
    if "/modular" in sitemap_body:
        fail("opt-in modular path leaked into sitemap")

    print(
        "PASS: deployed opt-in modular transport matches live Production, preserves default root, "
        "serves exact-SHA immutable runtime snapshots, rejects disallowed paths, and remains undiscovered by default"
    )


if __name__ == "__main__":
    main()
