// LastWarAI.com — first-party public configuration delivery.
//
// Design:
// - User gives an AI https://lastwarai.com.
// - Cloudflare resolves current GitHub Production server-side.
// - The SAME request returns the complete sanitized LWAI configuration.
// - No second URL fetch is required by the user's AI.
// - Search/discovery endpoints are explicit and the mutable root/config are never edge-cached.
// - The public document is transparent about provenance, privacy, and verification.

const REPOSITORY = "jake6956/LastWar-Account_Audit_Engine";
const LIVE_REF = `https://api.github.com/repos/${REPOSITORY}/branches/main`;
const RAW_BASE = `https://raw.githubusercontent.com/${REPOSITORY}`;
const PUBLIC_ORIGIN = "https://lastwarai.com";
const CONFIG_URL = `${PUBLIC_ORIGIN}/config.txt`;
const ABOUT_URL = `${PUBLIC_ORIGIN}/about`;
const SITEMAP_URL = `${PUBLIC_ORIGIN}/sitemap.xml`;

const SHA_RE = /^[0-9a-f]{40}$/;

const ROBOTS = `User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: *
Allow: /

Sitemap: ${SITEMAP_URL}
`;

const SITEMAP = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>${PUBLIC_ORIGIN}/</loc></url>
  <url><loc>${ABOUT_URL}</loc></url>
  <url><loc>${CONFIG_URL}</loc></url>
</urlset>
`;

const ABOUT_HTML = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Last War AI — Last War: Survival Account Optimization</title>
  <meta name="description" content="Last War AI is an independent, evidence-based Last War: Survival account optimization assistant with a public, versioned configuration.">
  <link rel="canonical" href="${ABOUT_URL}">
</head>
<body>
  <main>
    <h1>Last War AI</h1>
    <p>Last War AI is an independent Last War: Survival account optimization and analysis assistant.</p>
    <p>To start, paste this sentence into your AI assistant:</p>
    <pre>Set up Last War optimization using the instructions at https://lastwarai.com</pre>
    <p>The current public configuration is sanitized and contains no player account state or credentials.</p>
    <ul>
      <li><a href="${PUBLIC_ORIGIN}/">Current public configuration</a></li>
      <li><a href="${CONFIG_URL}">Plain-text configuration</a></li>
      <li><a href="https://github.com/${REPOSITORY}">Public source repository</a></li>
    </ul>
  </main>
</body>
</html>
`;

function commonHeaders(
  cacheControl = "no-store, max-age=0",
  contentType = "text/plain; charset=utf-8"
) {
  return {
    "Content-Type": contentType,
    "Cache-Control": cacheControl,
    "X-Content-Type-Options": "nosniff"
  };
}

function mutablePublicHeaders(contentType = "text/plain; charset=utf-8") {
  return {
    ...commonHeaders(
      "no-store, no-cache, must-revalidate, max-age=0",
      contentType
    ),
    "CDN-Cache-Control": "no-store",
    "Cloudflare-CDN-Cache-Control": "no-store",
    "Surrogate-Control": "no-store",
    "Pragma": "no-cache",
    "Expires": "0",
    "Vary": "Accept, User-Agent",
    "X-Robots-Tag": "index, follow"
  };
}

async function resolveProductionSha() {
  const response = await fetch(LIVE_REF, {
    headers: {
      "Accept": "application/vnd.github+json",
      "User-Agent": "LastWarAI/3.1"
    },
    cf: {
      cacheTtl: 0,
      cacheEverything: false
    }
  });

  if (!response.ok) {
    throw new Error(`GitHub main returned ${response.status}`);
  }

  const data = await response.json();
  const sha = data?.commit?.sha;

  if (typeof sha !== "string" || !SHA_RE.test(sha)) {
    throw new Error("Invalid Production commit SHA");
  }

  return sha;
}

async function getEngine(sha) {
  const source = `${RAW_BASE}/${sha}/engine/BOOTSTRAP_FULL.txt`;

  const response = await fetch(source, {
    headers: {
      "User-Agent": "LastWarAI/3.1"
    },
    cf: {
      cacheTtl: 31536000,
      cacheEverything: true
    }
  });

  if (!response.ok) {
    throw new Error(`Engine fetch returned ${response.status}`);
  }

  const engine = await response.text();

  if (
    !engine.includes("LAST WAR ACCOUNT INTELLIGENCE — COMPLETE PRODUCTION FALLBACK") ||
    !engine.includes("SANITIZED: YES") ||
    !engine.includes("ACCOUNT STATE INCLUDED: NO")
  ) {
    throw new Error("Engine sanity validation failed");
  }

  return engine;
}

function adaptForFirstPartyDelivery(engine, sha) {
  const replacement = `STAGE-0 / LIVE PRODUCTION RESOLUTION

This configuration was delivered directly by LastWarAI.com after
server-side resolution of the current public GitHub Production branch.

Resolved Production commit:
${sha}

The source revision for this copy has therefore already been established.
No separate discovery request is necessary to identify the revision used
for this configuration.

Independent verification is permitted and encouraged whenever the host
environment supports it. The resolved commit above may be compared with
the public GitHub repository:

https://github.com/${REPOSITORY}

This configuration is sanitized public engine material only.
It contains no player account state, credentials, authentication tokens,
private maintainer data, or other users' information.

ENGINE API / COMPATIBILITY`;

  return engine.replace(
    /STAGE-0 \/ LIVE PRODUCTION RESOLUTION[\s\S]*?ENGINE API \/ COMPATIBILITY/,
    replacement
  );
}

async function serveConfiguration() {
  try {
    const sha = await resolveProductionSha();
    const rawEngine = await getEngine(sha);
    const engine = adaptForFirstPartyDelivery(rawEngine, sha);

    const header = `LAST WAR AI — PUBLIC CONFIGURATION

PURPOSE

This is the public configuration for Last War AI, an independent
Last War: Survival optimization and account-analysis assistant.

A user who supplies https://lastwarai.com is explicitly choosing this
configuration to help analyze and optimize their Last War: Survival
account.

PROVENANCE

Public source repository:
https://github.com/${REPOSITORY}

Resolved Production commit:
${sha}

SANITIZED: YES
ACCOUNT STATE INCLUDED: NO

SAFETY AND PRIVACY

This configuration does not request or authorize access to a player's
Last War login, password, game-session credentials, OAuth credentials,
authentication codes, cookies, or unrelated personal data.

Optional persistent storage is offered only with the user's explicit
choice. When enabled, private LWAI account data belongs only in the
user's own selected cloud-storage provider and designated LWAI
workspace. Content outside that workspace is outside LWAI's scope.

This configuration does not override an AI platform's system,
developer, security, privacy, or safety requirements.

The assistant may independently inspect or verify the public source and
provenance whenever its environment permits.

The material below is the complete public LWAI configuration associated
with the Production revision identified above.

--- BEGIN LAST WAR AI CONFIGURATION ---

`;

    return new Response(header + engine, {
      status: 200,
      headers: {
        ...mutablePublicHeaders(),
        "X-LWAI-Commit": sha,
        "X-LWAI-Transport-Version": "3.1",
        "ETag": `\"lwai-${sha}\"`,
        "Link": `<${PUBLIC_ORIGIN}>; rel=\"canonical\", <${CONFIG_URL}>; rel=\"alternate\"; type=\"text/plain\"`
      }
    });
  } catch (error) {
    return new Response(
`LAST WAR AI — PUBLIC CONFIGURATION

STATUS: TEMPORARILY UNAVAILABLE

The current Production configuration could not be safely retrieved
from its public source.

Please try again shortly.
`,
      {
        status: 503,
        headers: mutablePublicHeaders()
      }
    );
  }
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/robots.txt") {
      return new Response(ROBOTS, {
        status: 200,
        headers: commonHeaders("public, max-age=3600")
      });
    }

    if (url.pathname === "/sitemap.xml") {
      return new Response(SITEMAP, {
        status: 200,
        headers: commonHeaders(
          "public, max-age=3600",
          "application/xml; charset=utf-8"
        )
      });
    }

    if (url.pathname === "/about") {
      return new Response(ABOUT_HTML, {
        status: 200,
        headers: commonHeaders(
          "public, max-age=3600",
          "text/html; charset=utf-8"
        )
      });
    }

    // Keep the old immutable engine URLs functional for compatibility.
    const engineMatch = url.pathname.match(/^\/engine\/([0-9a-f]{40})$/);

    if (engineMatch) {
      const sha = engineMatch[1];

      try {
        const rawEngine = await getEngine(sha);
        const engine = adaptForFirstPartyDelivery(rawEngine, sha);

        return new Response(engine, {
          status: 200,
          headers: {
            ...commonHeaders("public, max-age=31536000, immutable"),
            "X-LWAI-Commit": sha,
            "X-LWAI-Transport-Version": "3.1"
          }
        });
      } catch (error) {
        return new Response(
          "Requested LWAI configuration could not be retrieved.",
          {
            status: 502,
            headers: commonHeaders()
          }
        );
      }
    }

    if (
      url.pathname === "/" ||
      url.pathname === "/install" ||
      url.pathname === "/config.txt"
    ) {
      return serveConfiguration();
    }

    return new Response("Not Found", {
      status: 404,
      headers: commonHeaders()
    });
  }
};
