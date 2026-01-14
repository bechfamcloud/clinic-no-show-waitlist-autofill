import json
import datetime

from .logic import is_no_show


def handler(event, context):
    """
    Lab 02 - Step 2:
    - Pure logic evaluation (no AWS calls yet)
    - Determine if an appointment qualifies as a no-show
    """

    # Minimal input contract (we'll expand later):
    # event = {
    #   "appointment_start": "2026-01-14T12:00:00Z",
    #   "status": "SCHEDULED",
    #   "now": "2026-01-14T12:15:00Z",
    #   "grace_minutes": 10
    # }

    appointment_start = event.get("appointment_start")
    status = event.get("status", "SCHEDULED")
    now = event.get("now") or datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    grace_minutes = int(event.get("grace_minutes", 10))

    if not appointment_start:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required field: appointment_start"})
        }

    no_show = is_no_show(
        appointment_start_iso=appointment_start,
        status=status,
        now_iso=now,
        grace_minutes=grace_minutes,
    )

    result = {
        "no_show": no_show,
        "appointment_start": appointment_start,
        "status": status,
        "now": now,
        "grace_minutes": grace_minutes,
    }

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }

    }
