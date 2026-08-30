#!/usr/bin/env python3
"""Validate the live first-party LWAI Stage-0 server-side resolver."""
from __future__ import annotations

import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PUBLIC_URL = "https://lastwarai.com"
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
RAW_PREFIX = "https://raw.githubusercontent.com/jake6956/LastWar-Account_Audit_Engine/"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"FAIL: public entrypoint: {message}")
    raise SystemExit(1)


def fetch_text(url: str, accept: str = "text/plain,*/*;q=0.1") -> tuple[int, object, str]:
    request = Request(url, headers={"User-Agent": "LWAI-Release-Validation/1.0", "Accept": accept})
    try:
        with urlopen(request, timeout=15) as response:
            return getattr(response, "status", 200), response.headers, response.read(32768).decode("utf-8")
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
        fail(f"Cache-Control must include no-store, got {headers.get('Cache-Control', '')!r}")
    if headers.get("X-Content-Type-Options", "").lower() != "nosniff":
        fail("X-Content-Type-Options must be nosniff")

    if field(body, "RESOLUTION_STATUS") != "LIVE_GITHUB":
        fail("live resolver did not report LIVE_GITHUB")
    sha = field(body, "RESOLVED_PRODUCTION_COMMIT")
    if not SHA_RE.fullmatch(sha):
        fail("resolved commit is not a valid 40-lowercase-hex SHA")
    exact_bootstrap = field(body, "EXACT_BOOTSTRAP_URL")
    expected_bootstrap = f"{RAW_PREFIX}{sha}/engine/BOOTSTRAP.txt"
    if exact_bootstrap != expected_bootstrap:
        fail("EXACT_BOOTSTRAP_URL does not match resolved SHA")
    if field(body, "LIVE_REF_SOURCE") != LIVE_REF:
        fail("LIVE_REF_SOURCE drifted from canonical GitHub main endpoint")
    if "Do NOT require the user/client to retrieve the GitHub branch API again" not in body:
        fail("Stage-0 response does not remove the fragile client-side branch-API hop")

    ref_status, _, ref_body = fetch_text(LIVE_REF, "application/vnd.github+json")
    if ref_status != 200:
        fail(f"live GitHub branch ref returned {ref_status}")
    try:
        live_sha = json.loads(ref_body)["commit"]["sha"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        fail(f"could not parse live GitHub commit SHA: {exc}")
    if sha != live_sha:
        fail(f"LastWarAI.com resolved {sha}, but GitHub main is {live_sha}")

    boot_status, _, boot_body = fetch_text(exact_bootstrap)
    if boot_status != 200 or "LAST WAR ACCOUNT INTELLIGENCE — PRODUCTION BOOTSTRAP" not in boot_body:
        fail("resolved exact-commit bootstrap is not retrievable/valid")

    print(f"PASS: LastWarAI.com server-side resolver returned live immutable Production SHA {sha}")


if __name__ == "__main__":
    main()
