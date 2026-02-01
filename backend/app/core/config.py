from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Chat"
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/app"
    cors_origins: list[str] = ["http://localhost:5173"]
    ollama_url: str = "http://localhost:11434"

    class Config:
        env_file = ".env"


settings = Settings()
