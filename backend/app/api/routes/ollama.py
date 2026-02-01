from fastapi import APIRouter, HTTPException

from app.services.ollama import ollama_service

router = APIRouter()


@router.get("/models")
async def list_models():
    """List available Ollama models."""
    try:
        models = await ollama_service.list_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch models: {str(e)}"
        )
