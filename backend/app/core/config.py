from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Helpdesk AI Service"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True

    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Database
    POSTGRES_DB: str = "helpdesk_ai"
    POSTGRES_USER: str = "helpdesk"
    POSTGRES_PASSWORD: str = "helpdesk"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = "postgresql+psycopg://helpdesk:helpdesk@localhost:5432/helpdesk_ai"

    # Security
    SECRET_KEY: str = "change-me"

    # AI
    AI_PROVIDER: str = "mock"
    AI_GENERATION_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    OPENAI_RESPONSE_TEMPERATURE: float = 0.2
    OPENAI_MAX_OUTPUT_TOKENS: int = 1200
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    RAG_TOP_K: int = 5
    RAG_MIN_SCORE: float = 0.0
    RAG_EMBEDDING_PROVIDER: str = "openai"


settings = Settings()
