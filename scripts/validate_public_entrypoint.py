#!/usr/bin/env python3
"""Validate the live first-party LWAI resolver + same-domain immutable engine proxy."""
from __future__ import annotations

import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PUBLIC_URL = "https://lastwarai.com"
INSTALL_PROMPT = "Set up Last War optimization using the instructions at https://lastwarai.com"
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"FAIL: public entrypoint: {message}")
    raise SystemExit(1)


def fetch_text(url: str, accept: str = "text/plain,*/*;q=0.1") -> tuple[int, object, str]:
    request = Request(url, headers={"User-Agent": "LWAI-Release-Validation/2.0", "Accept": accept})
    try:
        with urlopen(request, timeout=20) as response:
            return getattr(response, "status", 200), response.headers, response.read(65536).decode("utf-8")
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        fail(f"could not retrieve {url}: {exc}")


def field(body: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(\S+)\s*$", body, re.M)
    if not match:
        fail(f"live resolver response missing {name}")
    return match.group(1)


def main() -> None:
    status, headers, body = fetch_text(PUBLIC_URL)
    if status != 200:
        fail(f"unexpected HTTP status {status}")
    if "text/plain" not in headers.get("Content-Type", "").lower():
        fail(f"unexpected Content-Type {headers.get('Content-Type', '')!r}")
    if "no-store" not in headers.get("Cache-Control", "").lower():
        fail(f"root Cache-Control must include no-store, got {headers.get('Cache-Control', '')!r}")
    if headers.get("X-Content-Type-Options", "").lower() != "nosniff":
        fail("root X-Content-Type-Options must be nosniff")

    if INSTALL_PROMPT not in body:
        fail("root does not show canonical one-line installer")
    if "You do not need to copy anything else from this page" not in body:
        fail("root does not give clear human copy guidance")
    if field(body, "PASTED_CONTENT_MODE") != "CONTINUE_INSTALL":
        fail("pasted-content fallback is not enabled")
    if "Do not ask the user to repaste" not in body:
        fail("pasted-content path may still strand/restart the user")
    if "Do not call GitHub directly" not in body:
        fail("client is still being instructed to call GitHub directly")

    if field(body, "RESOLUTION_STATUS") != "LIVE_GITHUB_SERVER_SIDE":
        fail("root did not report server-side live GitHub resolution")
    sha = field(body, "RESOLVED_PRODUCTION_COMMIT")
    if not SHA_RE.fullmatch(sha):
        fail("resolved commit is not a valid 40-lowercase-hex SHA")
    engine_url = field(body, "ENGINE_URL")
    expected_engine_url = f"{PUBLIC_URL}/engine/{sha}"
    if engine_url != expected_engine_url:
        fail("ENGINE_URL is not same-domain and pinned to the resolved SHA")

    ref_status, _, ref_body = fetch_text(LIVE_REF, "application/vnd.github+json")
    if ref_status != 200:
        fail(f"live GitHub branch ref returned {ref_status}")
    try:
        live_sha = json.loads(ref_body)["commit"]["sha"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        fail(f"could not parse live GitHub commit SHA: {exc}")
    if sha != live_sha:
        fail(f"LastWarAI.com resolved {sha}, but GitHub main is {live_sha}")

    engine_status, engine_headers, engine_body = fetch_text(engine_url)
    if engine_status != 200:
        fail(f"same-domain pinned engine returned {engine_status}")
    if "text/plain" not in engine_headers.get("Content-Type", "").lower():
        fail("pinned engine is not text/plain")
    if engine_headers.get("X-LWAI-Commit", "") != sha:
        fail("pinned engine X-LWAI-Commit does not match resolved SHA")
    if "immutable" not in engine_headers.get("Cache-Control", "").lower():
        fail("pinned engine is not marked immutable")
    for token in (
        "LAST WAR AI — FIRST-PARTY IMMUTABLE ENGINE HANDOFF",
        f"RESOLVED_PRODUCTION_COMMIT: {sha}",
        "DO NOT repeat the GitHub branch-resolution step before beginning",
        "LAST WAR ACCOUNT INTELLIGENCE — COMPLETE PRODUCTION FALLBACK",
        "SANITIZED: YES",
        "ACCOUNT STATE INCLUDED: NO",
    ):
        if token not in engine_body:
            fail(f"same-domain pinned engine missing required token: {token}")

    print(f"PASS: LastWarAI.com is URL-safe, paste-safe, GitHub-client-independent, and pinned to live Production SHA {sha}")


if __name__ == "__main__":
    main()
