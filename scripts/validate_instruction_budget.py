#!/usr/bin/env python3
"""Measure LWAI instruction footprint and fail only on explicit hard budgets."""
from __future__ import annotations

from pathlib import Path
import json
import math
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "contracts/instruction-budget.json"

FIRST_RUN_PROMPT = (
    "Would you like me to save your LWAI setup in your own cloud storage so I can pick up "
    "where we left off in future chats? Recommended, but optional. Reply yes or no."
)
COMPACT_REASSURANCE = (
    "LWAI will use only its dedicated Last War/LWAI workspace; everything else in your connected "
    "storage is off-limits. Connect through the provider/ChatGPT UI, and never paste passwords or login codes here."
)


def fail(message: str) -> None:
    print(f"FAIL: instruction budget: {message}")
    raise SystemExit(1)


def read_bytes(path: str) -> bytes:
    return (ROOT / path).read_bytes()


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def approx_tokens(byte_count: int) -> int:
    return math.ceil(byte_count / 4)


def git_show(ref: str, path: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        capture_output=True,
    )
    return proc.stdout if proc.returncode == 0 else None


def module_bytes(manifest: dict, required: bool, ref: str | None = None) -> int | None:
    total = 0
    for entry in manifest.get("modules") or []:
        if bool(entry.get("required")) != required:
            continue
        path = entry.get("path")
        if not path:
            continue
        body = git_show(ref, path) if ref else read_bytes(path)
        if body is None:
            return None
        total += len(body)
    return total


def base_metrics(ref: str = "origin/main") -> dict[str, int] | None:
    manifest_raw = git_show(ref, "engine/MANIFEST.json")
    loader = git_show(ref, "engine/BOOTSTRAP.txt")
    full = git_show(ref, "engine/BOOTSTRAP_FULL.txt")
    if not manifest_raw or loader is None or full is None:
        return None
    try:
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except Exception:
        return None
    mandatory = module_bytes(manifest, True, ref)
    optional = module_bytes(manifest, False, ref)
    if mandatory is None or optional is None:
        return None
    return {
        "stage1_loader": len(loader),
        "bootstrap_full": len(full),
        "mandatory_modules": mandatory,
        "optional_modules": optional,
    }


def current_metrics() -> dict[str, int]:
    manifest = read_json("engine/MANIFEST.json")
    return {
        "stage1_loader": len(read_bytes("engine/BOOTSTRAP.txt")),
        "bootstrap_full": len(read_bytes("engine/BOOTSTRAP_FULL.txt")),
        "mandatory_modules": module_bytes(manifest, True) or 0,
        "optional_modules": module_bytes(manifest, False) or 0,
    }


def check_budgets(metrics: dict[str, int], config: dict) -> None:
    budgets = config["budgets"]
    base = base_metrics()
    for name, size in metrics.items():
        budget = budgets[name]
        soft = int(budget["soft_bytes"])
        hard = int(budget["hard_bytes"])
        delta = None if base is None else size - base[name]
        delta_text = "n/a" if delta is None else f"{delta:+d} B vs origin/main"
        print(
            f"BUDGET {name}: {size} B (~{approx_tokens(size)} tokens heuristic); "
            f"soft={soft} hard={hard}; delta={delta_text}"
        )
        if size > hard:
            fail(f"{name} is {size} B, above hard limit {hard} B")
        if size > soft:
            print(f"::warning::instruction budget soft limit exceeded: {name} {size} B > {soft} B")


def check_duplication(config: dict) -> None:
    paths = [
        "engine/BOOTSTRAP_FULL.txt",
        "engine/modules/core/guidance.txt",
        "engine/modules/core/persistence.txt",
        "engine/modules/adapters/storage.txt",
        "contracts/user-experience.md",
        "contracts/storage-adapter.md",
    ]
    corpus = "\n".join((ROOT / p).read_text(encoding="utf-8") for p in paths)
    checks = {
        "first_run_persistence_prompt": FIRST_RUN_PROMPT,
        "compact_storage_reassurance": COMPACT_REASSURANCE,
    }
    softs = config.get("duplication_soft_occurrences") or {}
    for name, phrase in checks.items():
        count = corpus.count(phrase)
        soft = int(softs.get(name, 999999))
        print(f"DUPLICATION {name}: {count} exact occurrences; soft={soft}")
        if count > soft:
            print(f"::warning::instruction duplication increased: {name} occurs {count} times (soft {soft})")
        if count == 0:
            fail(f"canonical phrase missing: {name}")


def main() -> None:
    config = read_json("contracts/instruction-budget.json")
    metrics = current_metrics()
    check_budgets(metrics, config)
    check_duplication(config)
    print("PASS: instruction footprint is measured and within hard budgets")


if __name__ == "__main__":
    main()
