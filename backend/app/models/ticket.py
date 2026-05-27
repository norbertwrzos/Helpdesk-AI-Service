import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SAEnum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TicketStatus(str, enum.Enum):
    new = "new"
    in_analysis = "in_analysis"
    answered = "answered"
    resolved = "resolved"
    rejected = "rejected"


class TicketSource(str, enum.Enum):
    manual = "manual"
    email = "email"
    csv = "csv"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(TicketStatus, name="ticketstatus"),
        default=TicketStatus.new,
        nullable=False,
    )
    source: Mapped[TicketSource] = mapped_column(
        SAEnum(TicketSource, name="ticketsource"),
        default=TicketSource.manual,
        nullable=False,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    priority_id: Mapped[int | None] = mapped_column(
        ForeignKey("priorities.id"), nullable=True
    )
    classification_confidence: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    priority_confidence: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    classification_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
