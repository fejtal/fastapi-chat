from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class WebSocketMessagePayload(BaseModel):
    id: int
    content: str
    author: str
    room_id: int
    created_at: datetime


class WebSocketMessage(BaseModel):
    type: Literal["new_message"]
    message: WebSocketMessagePayload
