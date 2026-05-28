from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EmailImportLog(Base):
    """Log pojedynczego importu wiadomości e-mail."""

    __tablename__ = "email_import_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)
    sender: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # status: imported | skipped | error
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    ticket_id: Mapped[int | None] = mapped_column(
        ForeignKey("tickets.id", ondelete="SET NULL"), nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
