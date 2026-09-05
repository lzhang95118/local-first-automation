from pydantic import BaseModel, Field
from typing import Literal



class AutomationEvent(BaseModel):
    event_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    source: Literal["Shortcut", "scriptable", "manual"]
    payload: dict

