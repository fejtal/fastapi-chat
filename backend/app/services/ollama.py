import logging

from ollama import AsyncClient

from app.core.config import settings

logger = logging.getLogger(__name__)


class OllamaService:
    """Service for interacting with Ollama API."""

    def __init__(self):
        self.client = AsyncClient(host=settings.ollama_url)

    async def list_models(self) -> list[str]:
        """Fetch list of available Ollama models."""
        try:
            response = await self.client.list()
            # Handle both dict and object responses
            models_data = response.get("models", []) if isinstance(response, dict) else getattr(response, "models", [])
            
            # Extract model names - try multiple approaches
            models = []
            for model in models_data:
                try:
                    if isinstance(model, dict):
                        models.append(model["name"])
                    elif hasattr(model, "model"):
                        models.append(model.model)
                    elif hasattr(model, "name"):
                        models.append(model.name)
                    else:
                        # Fallback: convert to dict and get name
                        if hasattr(model, "model_dump"):
                            model_dict = model.model_dump()
                            models.append(model_dict.get("name", model_dict.get("model", str(model))))
                        else:
                            logger.warning(f"Unknown model object type: {type(model)}, attributes: {dir(model)}")
                            # Try to get string representation
                            models.append(str(model))
                except Exception as model_error:
                    logger.error(f"Failed to extract model name from {model}: {model_error}")
                    continue
            
            logger.info(f"Successfully loaded {len(models)} Ollama models")
            return models
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")
            return []

    async def chat(
        self, model: str, messages: list[dict[str, str]]
    ) -> str | None:
        """Generate chat completion using Ollama."""
        try:
            logger.info(f"Starting chat with model {model}, {len(messages)} messages")
            response = await self.client.chat(model=model, messages=messages)
            content = response.get("message", {}).get("content") if isinstance(response, dict) else getattr(response.message, "content", None)
            logger.info(f"Chat response received: {len(content) if content else 0} characters")
            return content
        except Exception as e:
            logger.error(f"Failed to generate Ollama chat response: {e}", exc_info=True)
            return None


# Singleton instance
ollama_service = OllamaService()
