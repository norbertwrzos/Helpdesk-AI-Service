"""Stage 4: add email fields to tickets, add email_import_logs table

Revision ID: 003_email_import
Revises: 002_analysis_pipeline
Create Date: 2026-05-28 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "003_email_import"
down_revision: str | None = "002_analysis_pipeline"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Tabela logów importu e-mail
    op.create_table(
        "email_import_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("message_id", sa.String(length=500), nullable=True),
        sa.Column("sender", sa.String(length=255), nullable=True),
        sa.Column("subject", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["ticket_id"], ["tickets.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_email_import_logs_message_id",
        "email_import_logs",
        ["message_id"],
        unique=False,
    )

    # Nowe pola e-mail w tabeli tickets
    op.add_column(
        "tickets",
        sa.Column("email_sender", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("email_subject", sa.String(length=500), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("email_message_id", sa.String(length=500), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("email_received_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_tickets_email_message_id",
        "tickets",
        ["email_message_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_tickets_email_message_id", table_name="tickets")
    op.drop_column("tickets", "email_received_at")
    op.drop_column("tickets", "email_message_id")
    op.drop_column("tickets", "email_subject")
    op.drop_column("tickets", "email_sender")
    op.drop_index(
        "ix_email_import_logs_message_id", table_name="email_import_logs"
    )
    op.drop_table("email_import_logs")
