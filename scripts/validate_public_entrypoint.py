#!/usr/bin/env python3
"""Validate the live first-party LWAI Stage-0 locator against the canonical repo payload."""
from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_URL = "https://lastwarai.com"
CANONICAL_PAYLOAD = ROOT / "infrastructure/public-bootstrap-locator.txt"


def fail(message: str) -> None:
    print(f"FAIL: public entrypoint: {message}")
    raise SystemExit(1)


def normalize(value: str) -> str:
    return value.replace("\r\n", "\n").rstrip("\n")


def main() -> None:
    if not CANONICAL_PAYLOAD.is_file():
        fail("canonical locator payload is missing from the release tree")
    expected = CANONICAL_PAYLOAD.read_text(encoding="utf-8")

    request = Request(
        PUBLIC_URL,
        headers={"User-Agent": "LWAI-Release-Validation/1.0", "Accept": "text/plain,*/*;q=0.1"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            status = getattr(response, "status", 200)
            content_type = response.headers.get("Content-Type", "")
            cache_control = response.headers.get("Cache-Control", "")
            nosniff = response.headers.get("X-Content-Type-Options", "")
            body = response.read(16384).decode("utf-8")
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        fail(f"could not retrieve {PUBLIC_URL}: {exc}")

    if status != 200:
        fail(f"unexpected HTTP status {status}")
    if "text/plain" not in content_type.lower():
        fail(f"unexpected Content-Type {content_type!r}")
    if "no-store" not in cache_control.lower():
        fail(f"Cache-Control must include no-store, got {cache_control!r}")
    if nosniff.lower() != "nosniff":
        fail(f"X-Content-Type-Options must be nosniff, got {nosniff!r}")
    if normalize(body) != normalize(expected):
        fail("live LastWarAI.com payload differs from infrastructure/public-bootstrap-locator.txt")

    print("PASS: live LastWarAI.com Stage-0 locator exactly matches the canonical sanitized repo payload")


if __name__ == "__main__":
    main()
