from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.router import api_router
from app.core.config import settings
from app.db.session import async_session, engine
from app.models import Base, Room

AI_ROOM_NAME = "🤖 AI Cave (Talk to Qwen)"
DEFAULT_ROOM_NAME = "Cave 🍌"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed default room
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed AI room and default room if not exists
    async with async_session() as session:
        # Create AI room (always first)
        ai_result = await session.execute(
            select(Room).where(Room.name == AI_ROOM_NAME)
        )
        if not ai_result.scalar_one_or_none():
            ai_room = Room(name=AI_ROOM_NAME)
            session.add(ai_room)
        
        # Create default room
        result = await session.execute(
            select(Room).where(Room.name == DEFAULT_ROOM_NAME)
        )
        if not result.scalar_one_or_none():
            default_room = Room(name=DEFAULT_ROOM_NAME)
            session.add(default_room)
        
        await session.commit()

    yield
    # Shutdown: nothing to clean up


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
