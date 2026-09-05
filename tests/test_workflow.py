import app.workflow as workflow
from app.models import AutomationEvent, EventResult



def test_perform_processing_returns_processed_result():
    event = AutomationEvent(
        event_id="workflow_evt_001",
        event_type="sample_event",
        source="client",
        payload={"message": "example"},
    )

    result = workflow.perform_processing(event)

    assert result.status == "processed"
    assert result.event_id == "workflow_evt_001"
    assert result.event_type == "sample_event"


def test_process_event_returns_duplicate_result():
    event = AutomationEvent(
        event_id="workflow_duplicate_evt_001",
        event_type="sample_event",
        source="client",
        payload={},
    )

    first_result = workflow.process_event(event)
    second_result = workflow.process_event(event)

    assert first_result.status == "processed"
    assert second_result.status == "duplicate"


def test_process_event_retries_transient_failures(monkeypatch):
    event = AutomationEvent(
        event_id="workflow_retry_evt_001",
        event_type="sample_event",
        source="client",
        payload={},
    )

    attempts = {"count": 0}

    def fake_processing(event: AutomationEvent) -> EventResult:
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise RuntimeError("Temporary failure")

        return EventResult(
            status="processed",
            event_id=event.event_id,
            event_type=event.event_type,
        )

    monkeypatch.setattr(
        workflow, 
        "perform_processing", 
        fake_processing
    )

    monkeypatch.setattr(
        workflow.time, 
        "sleep", 
        lambda _: None
    )

    result = workflow.process_event(event)

    assert result.status == "processed"
    assert attempts["count"] == 3