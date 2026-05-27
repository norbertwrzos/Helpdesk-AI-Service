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
    OPENAI_API_KEY: str = ""

    # Email
    EMAIL_IMPORT_ENABLED: bool = True
    EMAIL_IMAP_HOST: str = "localhost"
    EMAIL_IMAP_PORT: int = 3143
    EMAIL_IMAP_USE_SSL: bool = False
    EMAIL_IMAP_USERNAME: str = "test@localhost"
    EMAIL_IMAP_PASSWORD: str = "test"
    EMAIL_FOLDER: str = "INBOX"


settings = Settings()
