import logging

from fastapi import FastAPI, HTTPException

from app.models import AutomationEvent
from app.workflow import process_event
from app.storage import initialise_database


logging.basicConfig


app = FastAPI()

initialise_database()


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/events")
def create_event(event: AutomationEvent):
    try:
        return process_event(event)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )


