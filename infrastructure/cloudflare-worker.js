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
const MODULAR_URL = `${PUBLIC_ORIGIN}/modular`;
const SNAPSHOT_BASE_URL = `${PUBLIC_ORIGIN}/snapshot`;
const ABOUT_URL = `${PUBLIC_ORIGIN}/about`;
const SITEMAP_URL = `${PUBLIC_ORIGIN}/sitemap.xml`;
const MODULAR_TRANSPORT_VERSION = "3.3-chatgpt-linked-optin";

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

function isAllowedSnapshotPath(path) {
  if (
    path === "engine/BOOTSTRAP.txt" ||
    path === "engine/BOOTSTRAP_FULL.txt" ||
    path === "engine/MANIFEST.json" ||
    path === "releases/LATEST.json" ||
    path === "releases/MIGRATIONS.json" ||
    path === "schemas/engine-manifest.schema.json"
  ) {
    return true;
  }

  if (/^releases\/20\d{2}-\d{2}-\d{2}\.\d+\.json$/.test(path)) {
    return true;
  }

  return /^engine\/modules\/[A-Za-z0-9._/-]+\.txt$/.test(path);
}

function decodeSnapshotPath(encodedPath) {
  let path;

  try {
    path = decodeURIComponent(encodedPath);
  } catch {
    return null;
  }

  if (
    !path ||
    path.startsWith("/") ||
    path.includes("\\") ||
    path.includes("\0") ||
    path.split("/").some((segment) => !segment || segment === "." || segment === "..") ||
    !isAllowedSnapshotPath(path)
  ) {
    return null;
  }

  return path;
}

function contentTypeForSnapshotPath(path) {
  return path.endsWith(".json")
    ? "application/json; charset=utf-8"
    : "text/plain; charset=utf-8";
}

async function getExactRuntimeFile(sha, path) {
  const source = `${RAW_BASE}/${sha}/${path}`;

  const response = await fetch(source, {
    headers: {
      "User-Agent": "LastWarAI/3.2"
    },
    cf: {
      cacheTtl: 31536000,
      cacheEverything: true
    }
  });

  if (!response.ok) {
    throw new Error(`Runtime file fetch returned ${response.status}: ${path}`);
  }

  return response.text();
}

async function getStage1(sha) {
  const stage1 = await getExactRuntimeFile(sha, "engine/BOOTSTRAP.txt");

  if (
    !stage1.includes("LAST WAR ACCOUNT INTELLIGENCE — PRODUCTION BOOTSTRAP") ||
    !stage1.includes("SANITIZED: YES") ||
    !stage1.includes("ACCOUNT STATE INCLUDED: NO") ||
    !stage1.includes("runtime_mode: modular")
  ) {
    throw new Error("Stage-1 sanity validation failed");
  }

  return stage1;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function exactSnapshotUrl(sha, path) {
  const encoded = path
    .split("/")
    .map((segment) => encodeURIComponent(segment))
    .join("/");
  return `${SNAPSHOT_BASE_URL}/${sha}/${encoded}`;
}

async function getModularIndex(sha) {
  const [stage1, latestText, manifestText] = await Promise.all([
    getStage1(sha),
    getExactRuntimeFile(sha, "releases/LATEST.json"),
    getExactRuntimeFile(sha, "engine/MANIFEST.json")
  ]);

  let latest;
  let manifest;
  try {
    latest = JSON.parse(latestText);
    manifest = JSON.parse(manifestText);
  } catch {
    throw new Error("Modular release metadata is not valid JSON");
  }

  for (const doc of [latest, manifest]) {
    if (
      doc?.channel !== "Production" ||
      doc?.sanitized !== true ||
      doc?.account_state_included !== false
    ) {
      throw new Error("Modular release identity invalid");
    }
  }

  if (
    typeof latest.engine_version !== "string" ||
    latest.engine_version !== manifest.engine_version ||
    latest.engine_api_version !== manifest.engine_api_version ||
    latest.schema_version !== manifest.schema_version ||
    !Array.isArray(manifest.modules)
  ) {
    throw new Error("Modular release metadata mismatch");
  }

  for (const module of manifest.modules) {
    if (
      typeof module?.module_id !== "string" ||
      typeof module?.path !== "string" ||
      !isAllowedSnapshotPath(module.path)
    ) {
      throw new Error("Manifest contains invalid modular resource path");
    }
  }

  return { stage1, latest, manifest };
}

function modularResourceRows(sha, latest, manifest) {
  const base = [
    ["Stage-1 bootstrap", "engine/BOOTSTRAP.txt", "bootstrap"],
    ["Current exact-C release metadata", "releases/LATEST.json", "release"],
    ["Module manifest", "engine/MANIFEST.json", "manifest"],
    ["Migration graph", "releases/MIGRATIONS.json", "migration"],
    ["Manifest schema", "schemas/engine-manifest.schema.json", "schema"],
    ["Versioned release record", `releases/${latest.engine_version}.json`, "release"],
    ["Complete fallback / rollback", "engine/BOOTSTRAP_FULL.txt", "fallback"]
  ];

  const modules = manifest.modules.map((module) => [
    `${module.required ? "Required" : "Optional"} module: ${module.module_id}`,
    module.path,
    module.required ? "required-module" : "optional-module",
    module.integrity?.digest || ""
  ]);

  return [...base, ...modules].map(([label, path, kind, digest = ""]) => ({
    label,
    path,
    kind,
    digest,
    url: exactSnapshotUrl(sha, path)
  }));
}

function renderModularHtml(sha, stage1, latest, manifest) {
  const snapshotBase = `${SNAPSHOT_BASE_URL}/${sha}/`;
  const rows = modularResourceRows(sha, latest, manifest);
  const links = rows.map((row) => {
    const digest = row.digest
      ? ` <small>git blob: <code>${escapeHtml(row.digest)}</code></small>`
      : "";
    return `<li data-lwai-kind="${escapeHtml(row.kind)}" data-lwai-path="${escapeHtml(row.path)}"><a href="${escapeHtml(row.url)}">${escapeHtml(row.label)}</a> — <code>${escapeHtml(row.path)}</code>${digest}</li>`;
  }).join("\n");

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex,follow">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Last War AI — Opt-In Modular Configuration</title>
</head>
<body>
<main>
<h1>Last War AI — Opt-In Modular Configuration</h1>
<p><strong>Experimental / non-default transport.</strong> The normal LastWarAI.com installer is unchanged.</p>
<p>Resolved Production commit: <code>${escapeHtml(sha)}</code></p>
<p><code>RESOLVED_PRODUCTION_COMMIT: ${escapeHtml(sha)}</code><br>
<code>FIRST_PARTY_SNAPSHOT_BASE: ${escapeHtml(snapshotBase)}</code><br>
<code>FIRST_PARTY_RESOURCE_INDEX: ${escapeHtml(MODULAR_URL)}</code></p>

<h2>ChatGPT navigation rule</h2>
<p>Use the clickable exact-commit resource links on this page. Do <strong>not</strong> synthesize, rewrite, search for, or substitute snapshot URLs. Keep the whole bootstrap/update transaction on commit <code>${escapeHtml(sha)}</code>. Never mix commits or substitute GitHub/search results for a resource that is linked here.</p>

<h2>Exact-C runtime resources</h2>
<ol id="lwai-resource-index">
${links}
</ol>

<h2>Stage-1 bootstrap</h2>
<pre id="lwai-stage1">${escapeHtml(stage1)}</pre>
</main>
</body>
</html>`;
}

function renderModularText(sha, stage1, latest, manifest) {
  const snapshotBase = `${SNAPSHOT_BASE_URL}/${sha}/`;
  const rows = modularResourceRows(sha, latest, manifest);
  const index = rows.map((row) => `RESOURCE_LINK: ${row.path} = ${row.url}`).join("\n");

  return `LAST WAR AI — OPT-IN MODULAR CONFIGURATION

STATUS: EXPERIMENTAL / NON-DEFAULT TRANSPORT

Resolved Production commit:
${sha}

RESOLVED_PRODUCTION_COMMIT: ${sha}
FIRST_PARTY_SNAPSHOT_BASE: ${snapshotBase}
FIRST_PARTY_RESOURCE_INDEX: ${MODULAR_URL}

CHATGPT NAVIGATION RULE
Prefer the exact-C resource links exposed by FIRST_PARTY_RESOURCE_INDEX. Do not synthesize or substitute resource URLs. Never mix commits or use search/index results as candidate bytes.

${index}

SANITIZED: YES
ACCOUNT STATE INCLUDED: NO

--- BEGIN LWAI STAGE-1 ---

${stage1}`;
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

async function serveModularConfiguration(asHtml = true) {
  try {
    const sha = await resolveProductionSha();
    const { stage1, latest, manifest } = await getModularIndex(sha);
    const snapshotBase = `${SNAPSHOT_BASE_URL}/${sha}/`;
    const body = asHtml
      ? renderModularHtml(sha, stage1, latest, manifest)
      : renderModularText(sha, stage1, latest, manifest);

    return new Response(body, {
      status: 200,
      headers: {
        ...mutablePublicHeaders(asHtml ? "text/html; charset=utf-8" : "text/plain; charset=utf-8"),
        "X-Robots-Tag": "noindex, follow",
        "X-LWAI-Commit": sha,
        "X-LWAI-Transport-Version": MODULAR_TRANSPORT_VERSION,
        "X-LWAI-Snapshot-Base": snapshotBase,
        "X-LWAI-Resource-Index": MODULAR_URL,
        "ETag": `"lwai-modular-${sha}"`,
        "Link": `<${exactSnapshotUrl(sha, "engine/MANIFEST.json")}>; rel="manifest", <${exactSnapshotUrl(sha, "releases/LATEST.json")}>; rel="alternate"; type="application/json"`
      }
    });
  } catch (error) {
    return new Response(
`LAST WAR AI — OPT-IN MODULAR CONFIGURATION

STATUS: TEMPORARILY UNAVAILABLE

The opt-in modular Production bootstrap could not be safely assembled.
The normal LastWarAI.com installer remains the supported default.
`,
      {
        status: 503,
        headers: {
          ...mutablePublicHeaders(),
          "X-Robots-Tag": "noindex, follow"
        }
      }
    );
  }
}

async function serveSnapshotFile(sha, path) {
  try {
    const body = await getExactRuntimeFile(sha, path);

    return new Response(body, {
      status: 200,
      headers: {
        ...commonHeaders(
          "public, max-age=31536000, immutable",
          contentTypeForSnapshotPath(path)
        ),
        "X-Robots-Tag": "noindex, nofollow",
        "X-LWAI-Commit": sha,
        "X-LWAI-Snapshot-Path": path,
        "X-LWAI-Transport-Version": "3.2-modular-optin"
      }
    });
  } catch (error) {
    return new Response(
      "Requested LWAI snapshot file could not be retrieved.",
      {
        status: 502,
        headers: {
          ...commonHeaders(),
          "X-Robots-Tag": "noindex, nofollow"
        }
      }
    );
  }
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

    if (url.pathname === "/modular") {
      return serveModularConfiguration(true);
    }

    if (url.pathname === "/modular/config.txt") {
      return serveModularConfiguration(false);
    }

    const snapshotMatch = url.pathname.match(/^\/snapshot\/([0-9a-f]{40})\/(.+)$/);

    if (snapshotMatch) {
      const sha = snapshotMatch[1];
      const path = decodeSnapshotPath(snapshotMatch[2]);

      if (!path) {
        return new Response("Not Found", {
          status: 404,
          headers: {
            ...commonHeaders(),
            "X-Robots-Tag": "noindex, nofollow"
          }
        });
      }

      return serveSnapshotFile(sha, path);
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
