from src.no_show_processor.logic import is_no_show
import datetime

def test_no_show_when_current_time_past_appointment():
    appointment_time = (
        datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
    ).isoformat()

    event = {
        "appointment_time": appointment_time
    }

    assert is_no_show(event) is True


def test_not_no_show_when_appointment_in_future():
    appointment_time = (
        datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    ).isoformat()

    event = {
        "appointment_time": appointment_time
    }

    assert is_no_show(event) is False

