"""Pure, provider-neutral bounded recovery-ledger projection. No storage or user state."""
from datetime import datetime, timedelta, timezone

HOT_TTL_HOURS = 72
MAX_RECENT = 32
UNRESOLVED = frozenset(("OPEN", "WAITING_USER", "RECOVERY_REQUIRED"))


def _utc(value):
    dt = value if isinstance(value, datetime) else datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timezone required")
    return dt.astimezone(timezone.utc)


def project_recovery(events, checkpoints, *, active_account_id=None, now=None, max_recent=MAX_RECENT):
    """Make the read-only hot view; provider compacts expired events on next verified write."""
    now = _utc(now or datetime.now(timezone.utc))
    if max_recent < 1 or max_recent > MAX_RECENT:
        raise ValueError("invalid event budget")
    active = []
    for cp in checkpoints:
        if cp["status"] not in UNRESOLVED:
            continue
        if cp.get("account_id") and cp["account_id"] != active_account_id:
            continue
        if cp.get("scope") == "ACCOUNT" and not cp.get("account_id"):
            raise ValueError("missing account_id on account checkpoint")
        active.append(dict(cp))
    pinned_ids = {cp["checkpoint_id"] for cp in active}
    cutoff = now - timedelta(hours=HOT_TTL_HOURS)
    seen = {}
    visible = []
    for item in events:
        eid = item["event_id"]
        scope = item["scope"]
        if scope == "ACCOUNT":
            if not item.get("account_id"):
                raise ValueError("missing account_id on account event")
            if item["account_id"] != active_account_id:
                continue
        elif scope != "WORKSPACE":
            raise ValueError("invalid event scope")
        if eid in seen:
            if seen[eid] != item:
                raise ValueError("conflicting event_id")
            continue
        seen[eid] = item
        when = _utc(item["occurred_at"])
        if when > now:
            raise ValueError("event from the future")
        if when < cutoff and item.get("checkpoint_id") not in pinned_ids:
            continue
        required = ("event_type", "action", "result", "verified", "next_action")
        if any(key not in item for key in required) or not isinstance(item["verified"], bool):
            raise ValueError("invalid event envelope")
        fields = ("event_id", "occurred_at", "scope", "account_id", "checkpoint_id",
                  "event_type", "action", "result", "verified", "evidence_ref", "next_action")
        visible.append((when, {k: item.get(k) for k in fields}))
    visible.sort(key=lambda pair: (pair[0], pair[1]["event_id"]), reverse=True)
    pinned = [item for _, item in visible if item["checkpoint_id"] in pinned_ids]
    ordinary = [item for _, item in visible if item["checkpoint_id"] not in pinned_ids][:max_recent]
    return {"as_of": now.isoformat(), "retention_hours": HOT_TTL_HOURS,
            "open_checkpoints": active, "recent_events": pinned + ordinary}
