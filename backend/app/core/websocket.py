from fastapi import WebSocket

from app.schemas.websocket import WebSocketMessage


class ConnectionManager:
    """Manage WebSocket connections per room."""

    def __init__(self):
        # room_id -> list of websocket connections
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast_to_room(self, room_id: int, message: WebSocketMessage):
        """Send message to all connections in a room."""
        if room_id in self.active_connections:
            message_json = message.model_dump_json()
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_text(message_json)
                except Exception:
                    # Connection might be dead, will be cleaned up on disconnect
                    pass


# Singleton instance
manager = ConnectionManager()
