import app.storage as storage


def test_mark_event_processed():
    event_id = "storage_evt_001"

    assert storage.is_event_processed(event_id) is False

    storage.mark_event_processed(event_id)

    assert storage.is_event_processed(event_id) is True

