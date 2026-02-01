from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.websocket import manager
from app.models import Room

router = APIRouter()


@router.websocket("/room/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Verify room exists
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        await websocket.close(code=4004, reason="Room not found")
        return

    await manager.connect(websocket, room_id)
    try:
        while True:
            # Keep connection alive, we only use this for server -> client messages
            # Client sends messages via REST API
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
