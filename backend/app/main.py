from app.core.config import settings
from fastapi import FastAPI

from app.api.routes import health

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Serwis do zautomatyzowanego rozwiązywania zgłoszeń technicznych z wykorzystaniem AI",
)

app.include_router(health.router, tags=["system"])
