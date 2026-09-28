import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const SHA = "a".repeat(40);
const OTHER_SHA = "b".repeat(40);
const REPO = "jake6956/LastWar-Account_Audit_Engine";
const LIVE_REF = `https://api.github.com/repos/${REPO}/branches/main`;
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}`;

const STAGE1 = `LAST WAR ACCOUNT INTELLIGENCE — PRODUCTION BOOTSTRAP
engine_version: 2099-01-01.1
engine_api_version: 1.0
SANITIZED: YES
ACCOUNT STATE INCLUDED: NO
runtime_mode: modular
END
`;

const FULL = `LAST WAR ACCOUNT INTELLIGENCE — COMPLETE PRODUCTION FALLBACK
SANITIZED: YES
ACCOUNT STATE INCLUDED: NO
STAGE-0 / LIVE PRODUCTION RESOLUTION
generic resolver
ENGINE API / COMPATIBILITY
complete engine
`;

const MANIFEST = JSON.stringify({
  engine_version: "2099-01-01.1",
  engine_api_version: "1.0",
  schema_version: "2.3",
  channel: "Production",
  sanitized: true,
  account_state_included: false,
  modules: [
    {
      module_id: "core.operating",
      path: "engine/modules/core/operating.txt",
      required: true,
      integrity: { algorithm: "git_blob_sha1", digest: "1111111111111111111111111111111111111111" }
    },
    {
      module_id: "domain.example",
      path: "engine/modules/domain/example.txt",
      required: false,
      integrity: { algorithm: "git_blob_sha1", digest: "2222222222222222222222222222222222222222" }
    }
  ]
});

const calls = [];
let mode = "ok";

function rawUrl(sha, path) {
  return `${RAW_BASE}/${sha}/${path}`;
}

globalThis.fetch = async (input) => {
  const url = typeof input === "string" ? input : input.url;
  calls.push(url);

  if (url === LIVE_REF) {
    if (mode === "bad-ref") {
      return new Response(JSON.stringify({ commit: { sha: "not-a-sha" } }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }
    return new Response(JSON.stringify({ commit: { sha: SHA } }), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  }

  if (url === rawUrl(SHA, "engine/BOOTSTRAP.txt")) {
    return new Response(mode === "bad-stage1" ? "invalid" : STAGE1, { status: 200 });
  }
  if (url === rawUrl(SHA, "engine/BOOTSTRAP_FULL.txt")) {
    return new Response(FULL, { status: 200 });
  }
  if (url === rawUrl(SHA, "engine/MANIFEST.json")) {
    return new Response(MANIFEST, { status: 200 });
  }
  if (url === rawUrl(SHA, "releases/LATEST.json")) {
    return new Response(JSON.stringify({
      engine_version: "2099-01-01.1",
      engine_api_version: "1.0",
      schema_version: "2.3",
      channel: "Production",
      sanitized: true,
      account_state_included: false
    }), { status: 200 });
  }
  if (url === rawUrl(SHA, "releases/MIGRATIONS.json")) {
    return new Response('{"edges":[]}', { status: 200 });
  }
  if (url === rawUrl(SHA, "schemas/engine-manifest.schema.json")) {
    return new Response('{"type":"object"}', { status: 200 });
  }
  if (url === rawUrl(SHA, "engine/modules/core/operating.txt")) {
    return new Response("module_id: core.operating\n", { status: 200 });
  }
  if (url === rawUrl(SHA, "engine/modules/domain/example.txt")) {
    return new Response("module_id: domain.example\n", { status: 200 });
  }
  if (url === rawUrl(OTHER_SHA, "engine/MANIFEST.json")) {
    return new Response('{"other":true}', { status: 200 });
  }

  return new Response("missing", { status: 404 });
};

const source = await readFile("infrastructure/cloudflare-worker.js", "utf8");
const workerModule = await import(
  `data:text/javascript;base64,${Buffer.from(source).toString("base64")}`
);
const worker = workerModule.default;

async function request(path) {
  return worker.fetch(new Request(`https://lastwarai.com${path}`));
}

async function body(response) {
  return response.text();
}

function count(url) {
  return calls.filter((item) => item === url).length;
}

// Existing default transport remains complete and unchanged in shape.
calls.length = 0;
mode = "ok";
const root = await request("/");
assert.equal(root.status, 200);
assert.equal(root.headers.get("X-LWAI-Transport-Version"), "3.1");
assert.equal(root.headers.get("X-LWAI-Commit"), SHA);
const rootBody = await body(root);
assert.match(rootBody, /LAST WAR AI — PUBLIC CONFIGURATION/);
assert.match(rootBody, /COMPLETE PRODUCTION FALLBACK/);
assert.doesNotMatch(rootBody, /OPT-IN MODULAR CONFIGURATION/);
assert.equal(count(LIVE_REF), 1);
assert.equal(count(rawUrl(SHA, "engine/BOOTSTRAP_FULL.txt")), 1);

// Opt-in mutable endpoint resolves C once and returns Stage-1 plus a navigable exact-C resource index.
calls.length = 0;
const modular = await request("/modular");
assert.equal(modular.status, 200);
assert.equal(modular.headers.get("X-LWAI-Transport-Version"), "3.3-chatgpt-linked-optin");
assert.equal(modular.headers.get("X-LWAI-Commit"), SHA);
assert.equal(
  modular.headers.get("X-LWAI-Snapshot-Base"),
  `https://lastwarai.com/snapshot/${SHA}/`
);
assert.equal(modular.headers.get("X-LWAI-Resource-Index"), "https://lastwarai.com/modular");
assert.equal(modular.headers.get("X-Robots-Tag"), "noindex, follow");
assert.match(modular.headers.get("Cache-Control") || "", /no-store/);
assert.match(modular.headers.get("Content-Type") || "", /text\/html/);
const modularBody = await body(modular);
assert.match(modularBody, /OPT-IN MODULAR CONFIGURATION/i);
assert.match(modularBody, new RegExp(`Resolved Production commit:\\s*<code>${SHA}</code>`, "i"));
assert.match(modularBody, /ChatGPT navigation rule/);
assert.match(modularBody, /Do <strong>not<\/strong> synthesize/);
assert.match(modularBody, new RegExp(`href="https:\\/\\/lastwarai\\.com\\/snapshot\\/${SHA}\\/engine\\/MANIFEST\\.json"`));
assert.match(modularBody, new RegExp(`href="https:\\/\\/lastwarai\\.com\\/snapshot\\/${SHA}\\/engine\\/modules\\/core\\/operating\\.txt"`));
assert.match(modularBody, new RegExp(`href="https:\\/\\/lastwarai\\.com\\/snapshot\\/${SHA}\\/engine\\/modules\\/domain\\/example\\.txt"`));
assert.match(modularBody, /Required module: core\.operating/);
assert.match(modularBody, /Optional module: domain\.example/);
assert.match(modularBody, /PRODUCTION BOOTSTRAP/);
assert.doesNotMatch(modularBody, /COMPLETE PRODUCTION FALLBACK/);
assert.equal(count(LIVE_REF), 1);
assert.equal(count(rawUrl(SHA, "engine/BOOTSTRAP.txt")), 1);
assert.equal(count(rawUrl(SHA, "releases/LATEST.json")), 1);
assert.equal(count(rawUrl(SHA, "engine/MANIFEST.json")), 1);
assert.equal(count(rawUrl(SHA, "engine/BOOTSTRAP_FULL.txt")), 0);

// Plain-text alias exposes the same exact-C index for compatibility.
const modularAlias = await request("/modular/config.txt");
assert.equal(modularAlias.status, 200);
assert.equal(modularAlias.headers.get("X-LWAI-Commit"), SHA);
assert.match(modularAlias.headers.get("Content-Type") || "", /text\/plain/);
const aliasBody = await body(modularAlias);
assert.match(aliasBody, /OPT-IN MODULAR CONFIGURATION/);
assert.match(aliasBody, /RESOURCE_LINK: engine\/MANIFEST\.json = /);
assert.match(aliasBody, /RESOURCE_LINK: engine\/modules\/core\/operating\.txt = /);
assert.match(aliasBody, /RESOURCE_LINK: engine\/modules\/domain\/example\.txt = /);

// Snapshot reads are exact-SHA, immutable, same-origin transport with no main resolution.
calls.length = 0;
const manifestResponse = await request(`/snapshot/${SHA}/engine/MANIFEST.json`);
assert.equal(manifestResponse.status, 200);
assert.equal(manifestResponse.headers.get("X-LWAI-Commit"), SHA);
assert.equal(manifestResponse.headers.get("X-LWAI-Snapshot-Path"), "engine/MANIFEST.json");
assert.match(manifestResponse.headers.get("Cache-Control") || "", /immutable/);
assert.match(manifestResponse.headers.get("Content-Type") || "", /application\/json/);
assert.equal(await body(manifestResponse), MANIFEST);
assert.equal(count(LIVE_REF), 0);
assert.equal(count(rawUrl(SHA, "engine/MANIFEST.json")), 1);

const moduleResponse = await request(`/snapshot/${SHA}/engine/modules/core/operating.txt`);
assert.equal(moduleResponse.status, 200);
assert.match(moduleResponse.headers.get("Content-Type") || "", /text\/plain/);
assert.equal(await body(moduleResponse), "module_id: core.operating\n");

const fallbackResponse = await request(`/snapshot/${SHA}/engine/BOOTSTRAP_FULL.txt`);
assert.equal(fallbackResponse.status, 200);
assert.match(await body(fallbackResponse), /COMPLETE PRODUCTION FALLBACK/);

// A different immutable SHA is addressable only when it is explicit in the URL.
calls.length = 0;
const other = await request(`/snapshot/${OTHER_SHA}/engine/MANIFEST.json`);
assert.equal(other.status, 200);
assert.equal(other.headers.get("X-LWAI-Commit"), OTHER_SHA);
assert.equal(count(LIVE_REF), 0);
assert.equal(count(rawUrl(OTHER_SHA, "engine/MANIFEST.json")), 1);

// Disallowed repository files and traversal-shaped inputs fail before raw retrieval.
calls.length = 0;
for (const path of [
  `/snapshot/${SHA}/README.md`,
  `/snapshot/${SHA}/engine/modules/%252e%252e/BOOTSTRAP.txt`,
  `/snapshot/${SHA}/engine%5CBOOTSTRAP.txt`,
  `/snapshot/${SHA}/contracts/bootstrap-resolution.md`
]) {
  const response = await request(path);
  assert.equal(response.status, 404, path);
}
assert.equal(calls.length, 0);

// Invalid/missing SHA shapes never become snapshot routes.
const invalidSha = await request("/snapshot/NOT-A-SHA/engine/MANIFEST.json");
assert.equal(invalidSha.status, 404);

// Opt-in endpoint fails closed on invalid live ref or invalid Stage-1.
mode = "bad-ref";
assert.equal((await request("/modular")).status, 503);
mode = "bad-stage1";
assert.equal((await request("/modular")).status, 503);
mode = "ok";

console.log(
  "PASS: opt-in modular Worker preserves default transport, pins one live SHA, " +
  "serves allowlisted immutable same-origin snapshot files, rejects traversal/disallowed paths, " +
  "and fails closed without mixing mutable candidate sources"
);
