from typing import Literal

from pydantic import BaseModel, Field


class AutomationEvent(BaseModel):
    event_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    source: Literal["client", "local_app", "manual"]
    payload: dict

class EventResult(BaseModel):
    status: Literal["processed", "duplicate"]
    event_id: str
    event_type: str | None = None