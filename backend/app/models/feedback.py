from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Feedback(Base):
    """
    Ocena odpowiedzi AI wystawiona przez użytkownika.

    MVP: jedna ocena na AIResponse (unikalna per ai_response_id).
    Ponowne wysłanie feedbacku dla tej samej ai_response_id aktualizuje
    istniejący rekord zamiast tworzyć duplikat (obsługa w serwisie).
    """

    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"), nullable=False
    )
    ai_response_id: Mapped[int] = mapped_column(
        ForeignKey("ai_responses.id"), nullable=False, unique=True
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    is_helpful: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
