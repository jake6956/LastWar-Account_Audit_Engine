#!/usr/bin/env python3
"""Validate the live first-party LWAI single-response public configuration."""
from __future__ import annotations

import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PUBLIC_URL = "https://lastwarai.com"
CONFIG_URL = f"{PUBLIC_URL}/config.txt"
ABOUT_URL = f"{PUBLIC_URL}/about"
ROBOTS_URL = f"{PUBLIC_URL}/robots.txt"
SITEMAP_URL = f"{PUBLIC_URL}/sitemap.xml"
LIVE_REF = "https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    print(f"FAIL: public entrypoint: {message}")
    raise SystemExit(1)


def fetch_text(url: str, accept: str = "text/plain,*/*;q=0.1") -> tuple[int, object, str]:
    request = Request(url, headers={"User-Agent": "LWAI-Release-Validation/3.1", "Accept": accept})
    try:
        with urlopen(request, timeout=20) as response:
            return getattr(response, "status", 200), response.headers, response.read(262144).decode("utf-8")
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        fail(f"could not retrieve {url}: {exc}")


def require_mutable_freshness_headers(headers: object, label: str) -> None:
    cache_control = headers.get("Cache-Control", "").lower()
    for token in ("no-store", "no-cache", "must-revalidate", "max-age=0"):
        if token not in cache_control:
            fail(f"{label} Cache-Control missing {token!r}: {cache_control!r}")
    for header in ("CDN-Cache-Control", "Cloudflare-CDN-Cache-Control", "Surrogate-Control"):
        if "no-store" not in headers.get(header, "").lower():
            fail(f"{label} {header} must include no-store")
    if headers.get("Pragma", "").lower() != "no-cache":
        fail(f"{label} Pragma must be no-cache")
    if headers.get("Expires", "") != "0":
        fail(f"{label} Expires must be 0")


def validate_configuration(url: str) -> tuple[str, str]:
    status, headers, body = fetch_text(url)
    if status != 200:
        fail(f"{url} returned unexpected HTTP status {status}")
    if "text/plain" not in headers.get("Content-Type", "").lower():
        fail(f"{url} returned unexpected Content-Type {headers.get('Content-Type', '')!r}")
    require_mutable_freshness_headers(headers, url)
    if headers.get("X-Content-Type-Options", "").lower() != "nosniff":
        fail(f"{url} X-Content-Type-Options must be nosniff")
    if headers.get("X-LWAI-Transport-Version", "") != "3.1":
        fail(f"{url} transport version is not 3.1")

    sha = headers.get("X-LWAI-Commit", "")
    if not SHA_RE.fullmatch(sha):
        fail(f"{url} X-LWAI-Commit is not a valid 40-lowercase-hex SHA")

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
            fail(f"{url} configuration missing required token: {token}")

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
            fail(f"{url} still contains deprecated transport instruction: {token}")

    return sha, body


def main() -> None:
    sha, body = validate_configuration(PUBLIC_URL)
    config_sha, config_body = validate_configuration(CONFIG_URL)
    if config_sha != sha or config_body != body:
        fail("/config.txt does not match the root public configuration")

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
        f"Sitemap: {SITEMAP_URL}",
    ):
        if token not in robots_body:
            fail(f"robots.txt missing required discovery token: {token.splitlines()[0]}")

    sitemap_status, sitemap_headers, sitemap_body = fetch_text(SITEMAP_URL, "application/xml,text/xml,*/*;q=0.1")
    if sitemap_status != 200:
        fail(f"sitemap.xml returned {sitemap_status}")
    if "xml" not in sitemap_headers.get("Content-Type", "").lower():
        fail("sitemap.xml is not XML")
    for url in (PUBLIC_URL + "/", ABOUT_URL, CONFIG_URL):
        if f"<loc>{url}</loc>" not in sitemap_body:
            fail(f"sitemap.xml missing {url}")

    about_status, about_headers, about_body = fetch_text(ABOUT_URL, "text/html,*/*;q=0.1")
    if about_status != 200:
        fail(f"about page returned {about_status}")
    if "text/html" not in about_headers.get("Content-Type", "").lower():
        fail("about page is not HTML")
    for token in (
        "Last War AI — Last War: Survival Account Optimization",
        "Set up Last War optimization using the instructions at https://lastwarai.com",
        CONFIG_URL,
        f"https://github.com/jake6956/LastWar-Account_Audit_Engine",
    ):
        if token not in about_body:
            fail(f"about page missing discovery token: {token}")

    print(
        "PASS: LastWarAI.com serves one transparent complete configuration, "
        "exposes a matching /config.txt alias, strong mutable no-cache headers, "
        "crawler-friendly robots/sitemap/about discovery, and matches Production SHA "
        f"{sha}"
    )


if __name__ == "__main__":
    main()
