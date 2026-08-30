#!/usr/bin/env python3
"""Validate the live first-party LWAI Stage-0 locator without treating it as version authority."""
from __future__ import annotations

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PUBLIC_URL = "https://lastwarai.com"
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"

REQUIRED = [
    "LAST WAR AI — PUBLIC BOOTSTRAP LOCATOR",
    "SANITIZED: YES",
    "ACCOUNT STATE INCLUDED: NO",
    LIVE_REF,
    "commit.sha",
    "engine/BOOTSTRAP.txt",
    "exact immutable commit",
]

FORBIDDEN = [
    "engine_version:",
    "tinyurl.com/",
    "ACCOUNT STATE INCLUDED: YES",
]


def fail(message: str) -> None:
    print(f"FAIL: public entrypoint: {message}")
    raise SystemExit(1)


def main() -> None:
    request = Request(
        PUBLIC_URL,
        headers={"User-Agent": "LWAI-Release-Validation/1.0", "Accept": "text/plain,*/*;q=0.1"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            status = getattr(response, "status", 200)
            content_type = response.headers.get("Content-Type", "")
            body = response.read(16384).decode("utf-8")
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        fail(f"could not retrieve {PUBLIC_URL}: {exc}")

    if status != 200:
        fail(f"unexpected HTTP status {status}")
    if "text/plain" not in content_type.lower():
        fail(f"unexpected Content-Type {content_type!r}")
    for token in REQUIRED:
        if token not in body:
            fail(f"missing locator token: {token}")
    for token in FORBIDDEN:
        if token in body:
            fail(f"forbidden locator token present: {token}")

    print("PASS: first-party LastWarAI.com Stage-0 locator is reachable, sanitized, version-neutral and points to live GitHub exact-commit resolution")


if __name__ == "__main__":
    main()
