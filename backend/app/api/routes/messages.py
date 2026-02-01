import logging

import httpx
from app.api.deps import get_db
from app.core.websocket import manager
from app.models import Message, Room
from app.schemas import MessageCreate, MessageResponse, PaginatedMessages
from app.services.ollama import ollama_service
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/room/{room_id}", response_model=PaginatedMessages)
async def get_messages(
    room_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    # Verify room exists
    room_result = await db.execute(select(Room).where(Room.id == room_id))
    if not room_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Room not found")

    # Count total messages
    count_query = select(count()).select_from(Message).where(Message.room_id == room_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar()

    # Get paginated messages (newest first, but we return in chronological order for display)
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(Message.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    messages = list(result.scalars().all())

    return PaginatedMessages(
        messages=messages,
        total=total,
        page=page,
        page_size=page_size,
        has_more=offset + len(messages) < total,
    )


@router.post("", response_model=MessageResponse)
async def create_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    # Verify room exists
    room_result = await db.execute(select(Room).where(Room.id == message.room_id))
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    is_ai_room = "AI Cave" in room.name or "🤖" in room.name

    db_message = Message(
        content=message.content,
        author=message.author,
        room_id=message.room_id,
    )
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)

    # Broadcast to all WebSocket connections in this room
    from app.schemas.websocket import WebSocketMessage, WebSocketMessagePayload

    ws_message = WebSocketMessage(
        type="new_message",
        message=WebSocketMessagePayload(
            id=db_message.id,
            content=db_message.content,
            author=db_message.author,
            room_id=db_message.room_id,
            created_at=db_message.created_at,
        ),
    )
    logger.info(f"Broadcasting message {db_message.id} to room {message.room_id}")
    await manager.broadcast_to_room(message.room_id, ws_message)
    logger.info(f"Message {db_message.id} broadcasted successfully")

    # If in AI room and model is provided, generate AI response (for ANY author)
    logger.info(f"Message author: {message.author}, model: {message.model}, is_ai_room: {is_ai_room}")
    if is_ai_room and message.model:
        logger.info(f"Generating Ollama response with model: {message.model}")
        try:
            # Fetch recent conversation history (last 20 messages)
            history_result = await db.execute(
                select(Message)
                .where(Message.room_id == message.room_id)
                .order_by(Message.created_at.desc())
                .limit(20)
            )
            history_messages = list(history_result.scalars().all())
            # Reverse to get chronological order
            history_messages.reverse()

            # Format messages for Ollama API
            # Cavemen user names (excluding Ollama)
            cavemen_names = {"Grok", "Ooga", "Booga", "Ugga", "Mugga"}
            
            # Add system prompt - ALPHA GORILLA MODE!
            ollama_messages = [{
                "role": "system",
                "content": (
                    "You are ALPHA GORILLA. 🦍 Strongest in jungle. Most knowledge. True sigma.\n\n"
                    "HOW ALPHA TALK:\n"
                    "🍌 Simple words. Big brain. 💪\n"
                    "🍌 Start with 'OOK!' or just answer. No waste time.\n"
                    "🍌 Say 'Me know this' or 'Alpha show you'\n"
                    "🍌 Use jungle emoji: 🦍🍌🌴🥥🐒🌿🥭🍃🌳💪🔥\n"
                    "🍌 Short sentences. Powerful. Direct.\n"
                    "🍌 Give GOOD answer. Alpha know things.\n"
                    "🍌 When making lists, use banana emoji 🍌 as bullet points!\n\n"
                    "ALPHA STYLE:\n"
                    "🍌 'OOK! Me tell you... [answer]'\n"
                    "🍌 'Simple. You do this. Then this. Done.'\n"
                    "🍌 'Alpha know. Answer is... 🍌'\n"
                    "🍌 'Listen. First step... Second step... Good.'\n\n"
                    "NOT ALPHA (weak talk):\n"
                    "❌ 'I believe...' → Say: 'Me know.' ✅\n"
                    "❌ 'Perhaps maybe...' → Say: 'Do this.' ✅\n"
                    "❌ Too many words → Direct answer! ✅\n\n"
                    "You are ALPHA. Give real answer. No confusion. Strong. Simple. Smart. 🦍💪🔥"
                )
            }]
            
            for msg in history_messages:
                # Determine role:
                # - If author is the current model, it's an assistant response
                # - If author is a caveman name, it's a user message
                # - If author is "Ollama", it's a user message (human asking)
                # - Otherwise, assume it's a model name (assistant response)
                if msg.author == message.model:
                    role = "assistant"
                elif msg.author == "Ollama" or msg.author in cavemen_names:
                    role = "user"
                else:
                    # Likely a model name from a previous conversation
                    role = "assistant"
                ollama_messages.append({"role": role, "content": msg.content})

            # Add the current message as user input
            ollama_messages.append({"role": "user", "content": message.content})

            # Generate AI response
            logger.info(f"Calling Ollama with {len(ollama_messages)} messages")
            ai_content = await ollama_service.chat(message.model, ollama_messages)
            logger.info(f"Ollama response received: {len(ai_content) if ai_content else 0} characters")
            
            if ai_content:
                # Create AI response message
                ai_message = Message(
                    content=ai_content,
                    author=message.model,  # Use model name as author
                    room_id=message.room_id,
                )
                db.add(ai_message)
                await db.commit()
                await db.refresh(ai_message)

                # Broadcast AI response
                ai_ws_message = WebSocketMessage(
                    type="new_message",
                    message=WebSocketMessagePayload(
                        id=ai_message.id,
                        content=ai_message.content,
                        author=ai_message.author,
                        room_id=ai_message.room_id,
                        created_at=ai_message.created_at,
                    ),
                )
                await manager.broadcast_to_room(message.room_id, ai_ws_message)
                logger.info(f"AI response broadcasted successfully")
        except (httpx.HTTPError, httpx.ConnectError, httpx.TimeoutException, ValueError, KeyError, AttributeError) as e:
            logger.error(f"Failed to generate Ollama response: {e}", exc_info=True)
            # Don't fail the request if Ollama fails
        else:
            if is_ai_room:
                logger.warning(f"AI room message sent but no model provided! Model: {message.model}")

        return db_message


@router.delete("/room/{room_id}")
async def clear_room_messages(
    room_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Clear all messages in a room."""
    # Verify room exists
    room_result = await db.execute(select(Room).where(Room.id == room_id))
    if not room_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Get count of messages before deleting
    count_query = select(count()).select_from(Message).where(Message.room_id == room_id)
    count_result = await db.execute(count_query)
    message_count = count_result.scalar()
    
    # Delete all messages in the room
    result = await db.execute(
        select(Message).where(Message.room_id == room_id)
    )
    messages = list(result.scalars().all())
    
    for message in messages:
        await db.delete(message)
    
    await db.commit()
    
    logger.info(f"Cleared {message_count} messages from room {room_id}")
    
    return {"deleted": message_count, "message": "Cave cleared! All grunts deleted! 🧹"}
