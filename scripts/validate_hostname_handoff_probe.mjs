import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const SHA = "a".repeat(40);
const REPO = "jake6956/LastWar-Account_Audit_Engine";
const LIVE_REF = `https://api.github.com/repos/${REPO}/branches/main`;
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}`;

const FULL = `LAST WAR ACCOUNT INTELLIGENCE — COMPLETE PRODUCTION FALLBACK
engine_version: 2099-01-01.1
engine_api_version: 1.0
SANITIZED: YES
ACCOUNT STATE INCLUDED: NO
STAGE-0 / LIVE PRODUCTION RESOLUTION
ENGINE API / COMPATIBILITY
`;

globalThis.fetch = async (input) => {
  const url = typeof input === "string" ? input : input.url;
  if (url === LIVE_REF) {
    return new Response(JSON.stringify({commit:{sha:SHA}}), {
      status:200,
      headers:{"Content-Type":"application/json"}
    });
  }
  if (url === `${RAW_BASE}/${SHA}/engine/BOOTSTRAP_FULL.txt`) {
    return new Response(FULL,{status:200});
  }
  return new Response("missing",{status:404});
};

const source = await readFile("infrastructure/cloudflare-worker.js","utf8");
const workerModule = await import(
  `data:text/javascript;base64,${Buffer.from(source).toString("base64")}`
);
const worker = workerModule.default;

async function request(url) {
  return worker.fetch(new Request(url));
}

const root = await request("https://lastwarai.com/");
assert.equal(root.status,200);
assert.equal(root.headers.get("X-LWAI-Transport-Version"),"3.1");
const rootBody = await root.text();
assert.match(rootBody,/COMPLETE PRODUCTION FALLBACK/);
assert.doesNotMatch(rootBody,/HOSTNAME_COMPATIBILITY_ENTRY/);
assert.doesNotMatch(rootBody,/HOSTNAME HANDOFF PROBE/);

const handoff = await request("https://handoff.lastwarai.com/");
assert.equal(handoff.status,200);
assert.equal(handoff.headers.get("X-LWAI-Commit"),SHA);
assert.equal(handoff.headers.get("X-LWAI-Transport-Probe"),"hostname-handoff-source");
assert.equal(handoff.headers.get("X-Robots-Tag"),"noindex, nofollow");
const handoffBody = await handoff.text();
assert.match(handoffBody,/LAST WAR AI — HOSTNAME HANDOFF PROBE/);
assert.match(handoffBody,/STATUS: HANDOFF_READY/);
assert.match(handoffBody,/HOSTNAME_COMPATIBILITY_ENTRY: https:\/\/probe\.lastwarai\.com/);
assert.match(handoffBody,new RegExp(`RESOLVED_PRODUCTION_COMMIT: ${SHA}`));

const probe = await request("https://probe.lastwarai.com/");
assert.equal(probe.status,200);
assert.equal(probe.headers.get("X-LWAI-Commit"),SHA);
assert.equal(probe.headers.get("X-LWAI-Transport-Probe"),"hostname-handoff-target");
assert.equal(probe.headers.get("X-Robots-Tag"),"noindex, nofollow");
const probeBody = await probe.text();
assert.match(probeBody,/LAST WAR AI — HOSTNAME TRANSPORT PROBE TARGET/);
assert.match(probeBody,/PROBE_STATUS: REACHED/);
assert.match(probeBody,new RegExp(`RESOLVED_PRODUCTION_COMMIT: ${SHA}`));
assert.doesNotMatch(probeBody,/COMPLETE PRODUCTION FALLBACK/);

const handoffPath = await request("https://handoff.lastwarai.com/not-root");
assert.equal(handoffPath.status,404);
const probePath = await request("https://probe.lastwarai.com/not-root");
assert.equal(probePath.status,404);

console.log("PASS: production root is unchanged and one bare probe host exposes a same-SHA page-provided bare-host handoff to a second isolated probe host");
