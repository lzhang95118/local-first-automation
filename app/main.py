import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.models import AutomationEvent, EventResult
from app.workflow import process_event
from app.storage import initialise_database


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialise_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/events", response_model=EventResult)
def create_event(event: AutomationEvent):
    try:
        return process_event(event)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )


