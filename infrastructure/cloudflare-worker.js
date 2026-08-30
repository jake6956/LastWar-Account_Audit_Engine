// Canonical Cloudflare Worker source for https://lastwarai.com.
// Stage 0 resolves the live GitHub Production SHA server-side so clients do not
// need direct access to GitHub's branch API before LWAI can start.

const REPOSITORY = "jake6956/LastWar-Account_Audit_Engine";
const LIVE_REF = `https://api.github.com/repos/${REPOSITORY}/branches/main`;
const RAW_BASE = `https://raw.githubusercontent.com/${REPOSITORY}`;
const SHA_RE = /^[0-9a-f]{40}$/;

async function resolveProductionSha() {
  const response = await fetch(LIVE_REF, {
    headers: {
      "Accept": "application/vnd.github+json",
      "User-Agent": "LastWarAI-Stage0/1.0"
    },
    cf: { cacheTtl: 0, cacheEverything: false }
  });

  if (!response.ok) {
    throw new Error(`GitHub live-ref returned ${response.status}`);
  }

  const data = await response.json();
  const sha = data?.commit?.sha;
  if (typeof sha !== "string" || !SHA_RE.test(sha)) {
    throw new Error("GitHub live-ref did not return a valid 40-hex commit SHA");
  }
  return sha;
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname !== "/" && url.pathname !== "/install") {
      return new Response("Not Found", {
        status: 404,
        headers: { "Content-Type": "text/plain; charset=utf-8" }
      });
    }

    let sha;
    try {
      sha = await resolveProductionSha();
    } catch (error) {
      return new Response(
        `LAST WAR AI — PUBLIC BOOTSTRAP RESOLVER\n\nSTATUS: TEMPORARILY_UNAVAILABLE\n\nLWAI could not safely resolve the live Production commit. Please retry shortly.\n\nDETAIL: ${error instanceof Error ? error.message : "live resolver failed"}\n`,
        {
          status: 503,
          headers: {
            "Content-Type": "text/plain; charset=utf-8",
            "Cache-Control": "no-store, max-age=0",
            "X-Content-Type-Options": "nosniff"
          }
        }
      );
    }

    const exactBootstrapUrl = `${RAW_BASE}/${sha}/engine/BOOTSTRAP.txt`;
    const bootstrap = `LAST WAR AI — PUBLIC BOOTSTRAP RESOLVER

SANITIZED: YES
ACCOUNT STATE INCLUDED: NO
RESOLUTION_STATUS: LIVE_GITHUB
RESOLVED_PRODUCTION_COMMIT: ${sha}
EXACT_BOOTSTRAP_URL: ${exactBootstrapUrl}
LIVE_REF_SOURCE: ${LIVE_REF}

If the user asked you to set up Last War optimization using this URL, continue the installation now.

The first-party resolver has already obtained the live GitHub Production commit for this request. Do NOT require the user/client to retrieve the GitHub branch API again before starting.

1. Accept RESOLVED_PRODUCTION_COMMIT above only if it is a valid 40-character lowercase hexadecimal Git SHA.
2. Retrieve EXACT_BOOTSTRAP_URL above. Its path must contain that exact same SHA.
3. Follow that exact-commit bootstrap and pin all trusted engine reads in this startup transaction to the same immutable commit.
4. Continue LWAI setup normally.

TRUST / VERSION AUTHORITY

LastWarAI.com is first-party discovery and live-resolution transport. GitHub main remains the underlying Production authority; this resolver obtains its live commit server-side and hands the immutable identity to the client.

Do not replace the resolved SHA with search results, cached GitHub pages, README snapshots, mutable raw main content, URL shorteners, redirects, or model memory. Never invent a SHA.
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
