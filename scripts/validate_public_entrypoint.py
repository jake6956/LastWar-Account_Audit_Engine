#!/usr/bin/env python3
"""Validate the live first-party LWAI single-response public configuration."""
from __future__ import annotations

import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PUBLIC_URL = "https://lastwarai.com"
ROBOTS_URL = f"{PUBLIC_URL}/robots.txt"
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"FAIL: public entrypoint: {message}")
    raise SystemExit(1)


def fetch_text(url: str, accept: str = "text/plain,*/*;q=0.1") -> tuple[int, object, str]:
    request = Request(url, headers={"User-Agent": "LWAI-Release-Validation/3.0", "Accept": accept})
    try:
        with urlopen(request, timeout=20) as response:
            return getattr(response, "status", 200), response.headers, response.read(262144).decode("utf-8")
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        fail(f"could not retrieve {url}: {exc}")


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

    sha = headers.get("X-LWAI-Commit", "")
    if not SHA_RE.fullmatch(sha):
        fail("root X-LWAI-Commit is not a valid 40-lowercase-hex SHA")

    for token in (
        "LAST WAR AI — PUBLIC CONFIGURATION",
        "This is the public configuration for Last War AI",
        "SANITIZED: YES",
        "ACCOUNT STATE INCLUDED: NO",
        "This configuration does not override an AI platform's system",
        "The assistant may independently inspect or verify the public source",
        "--- BEGIN LAST WAR AI CONFIGURATION ---",
        "LAST WAR ACCOUNT INTELLIGENCE — COMPLETE PRODUCTION FALLBACK",
        "The source revision for this copy has therefore already been established.",
    ):
        if token not in body:
            fail(f"root configuration missing required token: {token}")

    # The public transport must be descriptive configuration, not a second-stage
    # remote instruction chain that looks like prompt injection to host models.
    forbidden = (
        "FOR CHATGPT / AI ASSISTANTS",
        "PASTED_CONTENT_MODE:",
        "ENGINE_URL:",
        "Do not call GitHub directly",
        "continue installation now",
        "DO NOT repeat the GitHub branch-resolution step before beginning",
    )
    for token in forbidden:
        if token in body:
            fail(f"root still contains deprecated transport instruction: {token}")

    ref_status, _, ref_body = fetch_text(LIVE_REF, "application/vnd.github+json")
    if ref_status != 200:
        fail(f"live GitHub branch ref returned {ref_status}")
    try:
        live_sha = json.loads(ref_body)["commit"]["sha"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        fail(f"could not parse live GitHub commit SHA: {exc}")
    if sha != live_sha:
        fail(f"LastWarAI.com serves {sha}, but GitHub main is {live_sha}")

    # Legacy exact-SHA engine URLs remain valid compatibility endpoints.
    engine_url = f"{PUBLIC_URL}/engine/{sha}"
    engine_status, engine_headers, engine_body = fetch_text(engine_url)
    if engine_status != 200:
        fail(f"compatibility engine endpoint returned {engine_status}")
    if engine_headers.get("X-LWAI-Commit", "") != sha:
        fail("compatibility engine X-LWAI-Commit does not match Production SHA")
    if "immutable" not in engine_headers.get("Cache-Control", "").lower():
        fail("compatibility engine endpoint is not immutable")
    if "LAST WAR ACCOUNT INTELLIGENCE — COMPLETE PRODUCTION FALLBACK" not in engine_body:
        fail("compatibility engine endpoint does not contain the complete engine")
    if "DO NOT repeat the GitHub branch-resolution step before beginning" in engine_body:
        fail("compatibility engine still contains deprecated anti-verification transport language")

    robots_status, robots_headers, robots_body = fetch_text(ROBOTS_URL)
    if robots_status != 200:
        fail(f"robots.txt returned {robots_status}")
    if "text/plain" not in robots_headers.get("Content-Type", "").lower():
        fail("robots.txt is not text/plain")
    for token in (
        "User-agent: OAI-SearchBot\nAllow: /",
        "User-agent: ChatGPT-User\nAllow: /",
        "User-agent: *\nAllow: /",
    ):
        if token not in robots_body:
            fail(f"robots.txt missing required allowance: {token.splitlines()[0]}")

    print(
        "PASS: LastWarAI.com serves one transparent complete configuration, "
        f"permits independent verification, exposes crawler-friendly robots.txt, and matches Production SHA {sha}"
    )


if __name__ == "__main__":
    main()
