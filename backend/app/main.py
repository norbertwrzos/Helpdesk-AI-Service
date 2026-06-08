from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ai, categories, feedback, health, knowledge, priorities, quality_metrics, tickets
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Serwis do zautomatyzowanego rozwiązywania zgłoszeń technicznych z wykorzystaniem AI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["system"])
app.include_router(tickets.router, tags=["tickets"])
app.include_router(ai.router, tags=["ai"])
app.include_router(feedback.router, tags=["feedback"])
app.include_router(quality_metrics.router, tags=["quality"])
app.include_router(categories.router, tags=["categories"])
app.include_router(priorities.router, tags=["priorities"])
app.include_router(knowledge.router, tags=["knowledge"])


