from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional


def _parse_iso(ts: str) -> datetime:
    """
    Parse ISO8601 timestamps.
    Supports both:
      - "2026-01-27T10:05:00Z"
      - "2026-01-27T10:05:00+00:00"
    """
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def select_next_patient(waitlist: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Lab 03 – Step 1
    Pure selection logic (no AWS calls).

    Rules:
      1) Lowest numeric priority wins (e.g., 1 beats 2).
      2) If priority ties, earliest requested_at wins.
      3) If waitlist is empty, return None.

    Expected input shape per item:
      {
        "patient_id": "p2",
        "priority": 1,
        "requested_at": "2026-01-27T10:05:00Z"
      }
    """
    if not waitlist:
        return None

    # Sort by (priority asc, requested_at asc)
    sorted_waitlist = sorted(
        waitlist,
        key=lambda p: (int(p.get("priority", 999999)), _parse_iso(p["requested_at"])),
    )

    return sorted_waitlist[0]

