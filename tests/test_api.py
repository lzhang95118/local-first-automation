def test_health_check(client):
    response = client.get("/health")


    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_event(client):
    response = client.post(
        "/events",
        json={
            "event_id": "test_evt_001",
            "event_type": "sample_event",
            "source": "client",
            "payload": {
                "message": "example"
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "processed"
    assert response.json()["event_id"] == "test_evt_001"


def test_duplicate_event(client):
    event = {
        "event_id": "test_evt_duplicate",
        "event_type": "sample_event",
        "source": "client",
        "payload": {
            "message": "example"
        },
    }

    first_response = client.post("/events", json=event)
    second_response = client.post("/events", json=event)

    assert first_response.status_code == 200
    assert first_response.json()["status"] == "processed"

    assert second_response.status_code == 200
    assert second_response.json()["status"] == "duplicate"


def test_invalid_source_returns_422(client):
    response = client.post(
        "/events",
        json={
            "event_id": "test_evt_invalid_source",
            "event_type": "sample_event",
            "source": "unknown",
            "payload": {
                "message": "example"
            },
        },
    )

    assert response.status_code == 422

