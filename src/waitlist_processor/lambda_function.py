import json

from .logic import select_next_patient


def handler(event, context):
    """
    Lab 03 – Step 2
    Thin Lambda-style handler.

    Responsibilities:
    - Receive event
    - Extract waitlist list
    - Delegate selection to pure logic
    - Return a structured JSON response

    No AWS service calls in this step.
    """

    # Expecting event to contain a "waitlist" key with a list of patients
    waitlist = event.get("waitlist", [])

    chosen = select_next_patient(waitlist)

    response = {
        "chosen_patient": chosen,  # will be None if waitlist empty
        "input_waitlist_count": len(waitlist),
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
