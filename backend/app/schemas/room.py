from datetime import datetime

from pydantic import BaseModel


class RoomCreate(BaseModel):
    name: str


class RoomResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
