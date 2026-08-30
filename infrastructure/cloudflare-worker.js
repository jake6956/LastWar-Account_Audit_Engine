// Canonical Cloudflare Worker source for https://lastwarai.com.
// Keep the bootstrap payload byte-equivalent (ignoring trailing newline differences)
// to infrastructure/public-bootstrap-locator.txt. GitHub CI validates the live endpoint.

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname !== "/" && url.pathname !== "/install") {
      return new Response("Not Found", {
        status: 404,
        headers: {
          "Content-Type": "text/plain; charset=utf-8"
        }
      });
    }

    const bootstrap = `LAST WAR AI — PUBLIC BOOTSTRAP LOCATOR

SANITIZED: YES
ACCOUNT STATE INCLUDED: NO

If the user asked you to set up Last War optimization using this URL, continue the installation now.

1. Read the live GitHub Production branch ref:
https://api.github.com/repos/jake6956/LastWar-Account_Audit_Engine/branches/main

2. Obtain its current commit.sha.
Require a valid 40-character hexadecimal Git commit SHA.

3. Retrieve engine/BOOTSTRAP.txt from that exact commit.

4. Follow that exact-commit bootstrap and continue LWAI setup.

TRUST / VERSION AUTHORITY

This document is only the permanent public entrypoint. It does not establish the current LWAI version.

Current Production is established only by the live GitHub main branch ref and its commit.sha.

Do not determine current Production from this document, redirects, search results, cached GitHub pages, README snapshots, mutable raw main content, URL shorteners, or model memory.

All trusted engine files used during one startup transaction must come from the same exact immutable commit.
`;

    return new Response(bootstrap, {
      status: 200,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "no-store, max-age=0",
        "X-Content-Type-Options": "nosniff"
      }
    });
  }
};
