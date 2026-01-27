import json

from .logic import is_no_show
from src.waitlist_processor.logic import select_next_patient


def handler(event, context):
    """
    Lab 03 - Step 3
    If appointment is a no-show, pick the next patient from the waitlist.

    Expected event shape:
    {
      "appointment_iso": "...",
      "status": "SCHEDULED",
      "now_iso": "...",
      "grace_minutes": 10,
      "waitlist": [ { "patient_id": "...", "priority": 1, "requested_at": "..." }, ... ]
    }
    """

    appointment_iso = event.get("appointment_iso")
    status = event.get("status")
    now_iso = event.get("now_iso")
    grace_minutes = event.get("grace_minutes", 10)

    waitlist = event.get("waitlist", [])

    no_show = is_no_show(appointment_iso, status, now_iso, grace_minutes)

    chosen = select_next_patient(waitlist) if no_show else None

    response = {
        "no_show": no_show,
        "chosen_patient": chosen,  # None if not a no-show OR waitlist empty
        "input_waitlist_count": len(waitlist),
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
