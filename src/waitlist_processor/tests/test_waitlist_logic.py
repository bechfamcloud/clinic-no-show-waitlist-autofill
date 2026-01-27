from src.waitlist_processor.logic import select_next_patient


def test_select_next_patient_returns_none_when_empty():
    assert select_next_patient([]) is None


def test_select_next_patient_picks_lowest_priority_number():
    waitlist = [
        {"patient_id": "p1", "priority": 3, "requested_at": "2026-01-27T10:10:00Z"},
        {"patient_id": "p2", "priority": 1, "requested_at": "2026-01-27T10:20:00Z"},
        {"patient_id": "p3", "priority": 2, "requested_at": "2026-01-27T10:00:00Z"},
    ]
    chosen = select_next_patient(waitlist)
    assert chosen["patient_id"] == "p2"


def test_select_next_patient_tiebreaker_earliest_requested_at():
    waitlist = [
        {"patient_id": "p1", "priority": 1, "requested_at": "2026-01-27T10:10:00Z"},
        {"patient_id": "p2", "priority": 1, "requested_at": "2026-01-27T10:05:00Z"},
    ]
    chosen = select_next_patient(waitlist)
    assert chosen["patient_id"] == "p2"
