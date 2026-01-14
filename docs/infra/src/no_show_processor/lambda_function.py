import json
import datetime


def handler(event, context):
    """
    Lambda entry point for no-show detection.
    Placeholder for Lab 02 – logic added in later steps.
    """

    timestamp = datetime.datetime.utcnow().isoformat()

    response = {
        "message": "No-show processor invoked",
        "timestamp": timestamp,
        "input_event": event
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
