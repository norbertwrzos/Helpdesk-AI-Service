from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TicketMessage(Base):
    """
    Wiadomość w ramach konwersacji powiązanej ze zgłoszeniem.

    Reprezentuje pojedynczą wiadomość wymieniną między agentem
    a użytkownikiem końcowym w kontekście obsługi zgłoszenia.
    """

    __tablename__ = "ticket_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"), nullable=False
    )
    author_role: Mapped[str] = mapped_column(String(50), nullable=False)
    author_name: Mapped[str] = mapped_column(String(255), nullable=False)
    author_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="public"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        Index("ix_ticket_messages_ticket_id", "ticket_id"),
        Index("ix_ticket_messages_created_at", "created_at"),
        Index("ix_ticket_messages_author_role", "author_role"),
    )

    ticket: Mapped["Ticket"] = relationship(back_populates="messages")
