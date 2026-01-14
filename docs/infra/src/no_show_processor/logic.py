from __future__ import annotations

from datetime import datetime, timezone


def parse_iso8601_utc(value: str) -> datetime:
    """
    Parse an ISO8601 timestamp string into a timezone-aware UTC datetime.
    Expected input examples:
      - "2026-01-14T12:00:00Z"
      - "2026-01-14T12:00:00+00:00"
    """
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        # If timezone missing, treat as UTC to keep rules deterministic
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def is_no_show(
    appointment_start_iso: str,
    status: str,
    now_iso: str,
    grace_minutes: int = 10,
) -> bool:
    """
    No-show rule (deterministic):
    - appointment is still 'SCHEDULED' (not checked-in / completed / cancelled)
    - AND current time is >= appointment start time + grace_minutes
    """
    if status.strip().upper() != "SCHEDULED":
        return False

    start_dt = parse_iso8601_utc(appointment_start_iso)
    now_dt = parse_iso8601_utc(now_iso)

    grace_seconds = grace_minutes * 60
    return (now_dt - start_dt).total_seconds() >= grace_seconds

