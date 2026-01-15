import json
from .logic import is_no_show


def handler(event, context):
    """
    Lab 02 – Step 4
    Thin Lambda handler.

    Responsibilities:
    - Receive event
    - Delegate no-show evaluation to pure logic
    - Return structured response

    No AWS service calls in this step.
    """

    no_show_detected = is_no_show(event)

    response = {
        "no_show_detected": no_show_detected,
        "input_event": event
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }

