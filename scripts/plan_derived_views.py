#!/usr/bin/env python3
"""Plan non-destructive Sheets alias repairs from caller-supplied, account-scoped cell data.

No connector auth or provider browsing occurs here. The caller must verify the
selected LWAI workspace, spreadsheet, schema, tab metadata and write privileges.
This pure planner never applies writes or asserts migration success.
"""
from __future__ import annotations

import json
import sys
from typing import Any

ALIASES = {
    "Wall defense position 1": "Default Tank",
    "Wall defense position 2": "Default Missile",
    "Wall defense position 3": "Default Air",
    "Observed Tank lineup (current exact)": "Default Tank",
    "Observed Missile lineup (current exact)": "Default Missile",
    "Observed Air lineup (current exact)": "Default Air",
}


def _value(cell: Any) -> Any:
    if isinstance(cell, dict):
        entered = cell.get("userEnteredValue", {})
        if "formulaValue" in entered:
            return entered["formulaValue"]
        return entered.get("numberValue", entered.get("stringValue"))
    return cell


def _safe(cell: Any) -> bool:
    return not (isinstance(cell, dict) and
                (cell.get("dataValidation") is not None or
                 cell.get("protected") or cell.get("readOnly")))


def plan_preset_alias_links(sheet_id: int, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Return Sheets batchUpdate requests; leave conflicts unchanged.

    Each row: {"row": <1-based sheet row>, "label": <Presets A>,
               "power": <CellData or scalar from Presets B>}.
    No positional assumption is made about which row contains each label.
    """
    if not isinstance(sheet_id, int) or sheet_id < 0:
        raise ValueError("verified numeric sheet_id required")
    index: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if not isinstance(row.get("row"), int) or row["row"] < 1:
            raise ValueError("invalid one-based row")
        label = row.get("label")
        if isinstance(label, str):
            index.setdefault(label, []).append(row)

    requests: list[dict[str, Any]] = []
    conflicts: list[dict[str, str]] = []
    for alias, canonical in ALIASES.items():
        target_rows, source_rows = index.get(alias, []), index.get(canonical, [])
        if not target_rows:
            continue
        if len(target_rows) != 1 or len(source_rows) != 1:
            conflicts.append({"alias": alias, "reason": "missing or ambiguous canonical row"})
            continue
        target, source = target_rows[0], source_rows[0]
        power, current = _value(source.get("power")), _value(target.get("power"))
        expected = f"=B{source['row']}"
        if isinstance(current, str) and current.startswith("="):
            if current != expected:
                conflicts.append({"alias": alias, "reason": "existing different formula"})
            continue
        if not _safe(target.get("power")):
            conflicts.append({"alias": alias, "reason": "protected or validated target"})
            continue
        if (isinstance(power, bool) or isinstance(current, bool)
                or not isinstance(power, (int, float))
                or not isinstance(current, (int, float)) or abs(power - current) > 1e-9):
            conflicts.append({"alias": alias, "reason": "non-identical or nonnumeric observation"})
            continue
        requests.append({
            "updateCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": target["row"] - 1,
                    "endRowIndex": target["row"],
                    "startColumnIndex": 1,
                    "endColumnIndex": 2,
                },
                "rows": [{"values": [{"userEnteredValue": {"formulaValue": expected}}]}],
                "fields": "userEnteredValue",
            }
        })
    return {"requests": requests, "conflicts": conflicts, "revision": 1,
            "verified": False, "mark_revision_after_readback": True}


def main() -> None:
    source = json.load(sys.stdin)
    output = plan_preset_alias_links(source["sheet_id"], source["rows"])
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
