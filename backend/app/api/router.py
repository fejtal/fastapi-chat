from app.api.routes import messages, ollama, rooms, ws
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(ws.router, prefix="/ws", tags=["websocket"])
api_router.include_router(ollama.router, prefix="/ollama", tags=["ollama"])
