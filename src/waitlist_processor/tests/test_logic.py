from src.waitlist_processor.logic import select_next_patient


def test_select_next_patient_returns_none_when_empty():
    assert select_next_patient([]) is None
