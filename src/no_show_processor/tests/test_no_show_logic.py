import datetime
import inspect

from src.no_show_processor.logic import is_no_show


def _call_is_no_show(*, appointment_iso: str, status: str, now_iso: str, grace_minutes: int):
    """
    Calls is_no_show() while adapting to the actual parameter names in logic.py.
    This avoids you having to manually edit tests when the function signature changes.
    """
    sig = inspect.signature(is_no_show)
    params = set(sig.parameters.keys())

    # Map our known values to whichever parameter names your is_no_show() uses.
    kwargs = {}

    # appointment time parameter name variants we can support safely
    appt_param_candidates = [
        "appointment_start_iso",
        "appointment_time",
        "appointment_time_iso",
        "appointment_iso",
        "appointment_start",
    ]
    appt_param = next((p for p in appt_param_candidates if p in params), None)
    if appt_param is None:
        raise AssertionError(
            f"Cannot find appointment time parameter in is_no_show(). "
            f"Expected one of {appt_param_candidates}, got {sorted(params)}"
        )
    kwargs[appt_param] = appointment_iso

    # status param (we know your function requires this because pytest said it's missing)
    if "status" in params:
        kwargs["status"] = status
    else:
        raise AssertionError(f"is_no_show() does not have 'status' parameter. Got {sorted(params)}")

    # now param (we know your function requires now_iso because pytest said it's missing)
    now_param_candidates = ["now_iso", "now", "current_time_iso", "current_time"]
    now_param = next((p for p in now_param_candidates if p in params), None)
    if now_param is None:
        raise AssertionError(
            f"Cannot find current-time parameter in is_no_show(). "
            f"Expected one of {now_param_candidates}, got {sorted(params)}"
        )
    kwargs[now_param] = now_iso

    # grace minutes might be required or optional; only pass it if the function accepts it
    grace_param_candidates = ["grace_minutes", "grace", "grace_period_minutes"]
    grace_param = next((p for p in grace_param_candidates if p in params), None)
    if grace_param is not None:
        kwargs[grace_param] = grace_minutes

    return is_no_show(**kwargs)


def test_no_show_when_current_time_past_appointment():
    now = datetime.datetime.now(datetime.timezone.utc)
    now_iso = now.isoformat()

    appointment_start_iso = (now - datetime.timedelta(minutes=30)).isoformat()

    result = _call_is_no_show(
        appointment_iso=appointment_start_iso,
        status="SCHEDULED",
        now_iso=now_iso,
        grace_minutes=10,
    )
    assert result is True


def test_not_no_show_when_appointment_in_future():
    now = datetime.datetime.now(datetime.timezone.utc)
    now_iso = now.isoformat()

    appointment_start_iso = (now + datetime.timedelta(minutes=30)).isoformat()

    result = _call_is_no_show(
        appointment_iso=appointment_start_iso,
        status="SCHEDULED",
        now_iso=now_iso,
        grace_minutes=10,
    )
    assert result is False
