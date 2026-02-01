from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models import Room
from app.schemas import RoomCreate, RoomResponse

router = APIRouter()


@router.get("", response_model=list[RoomResponse])
async def get_rooms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).order_by(Room.created_at))
    rooms = list(result.scalars().all())
    
    # Sort to ensure AI room is first
    ai_rooms = [r for r in rooms if "AI Cave" in r.name or "🤖" in r.name]
    other_rooms = [r for r in rooms if r not in ai_rooms]
    
    return ai_rooms + other_rooms


@router.post("", response_model=RoomResponse)
async def create_room(room: RoomCreate, db: AsyncSession = Depends(get_db)):
    # Check if room name already exists
    existing = await db.execute(select(Room).where(Room.name == room.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Room with this name already exists")

    db_room = Room(name=room.name)
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room


@router.delete("/{room_id}")
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    await db.execute(delete(Room).where(Room.id == room_id))
    await db.commit()
    return {"message": "Room deleted"}
