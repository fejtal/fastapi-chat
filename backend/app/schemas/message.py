from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str
    author: str
    room_id: int
    model: str | None = None


class MessageResponse(BaseModel):
    id: int
    content: str
    author: str
    room_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaginatedMessages(BaseModel):
    messages: list[MessageResponse]
    total: int
    page: int
    page_size: int
    has_more: bool
