"""Add ticket_messages table.

Revision ID: 003_ticket_messages
Revises: 002_knowledge_article_embeddings
Create Date: 2026-06-09 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "003_ticket_messages"
down_revision: str | None = "002_knowledge_article_embeddings"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ticket_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("author_role", sa.String(length=50), nullable=False),
        sa.Column("author_name", sa.String(length=255), nullable=False),
        sa.Column("author_email", sa.String(length=255), nullable=True),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column(
            "message_type",
            sa.String(length=50),
            nullable=False,
            server_default="public",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ticket_messages_ticket_id", "ticket_messages", ["ticket_id"]
    )
    op.create_index(
        "ix_ticket_messages_created_at", "ticket_messages", ["created_at"]
    )
    op.create_index(
        "ix_ticket_messages_author_role", "ticket_messages", ["author_role"]
    )


def downgrade() -> None:
    op.drop_index("ix_ticket_messages_author_role", table_name="ticket_messages")
    op.drop_index("ix_ticket_messages_created_at", table_name="ticket_messages")
    op.drop_index("ix_ticket_messages_ticket_id", table_name="ticket_messages")
    op.drop_table("ticket_messages")
