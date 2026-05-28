"""Stage 5: add feedback table

Revision ID: 004_feedback
Revises: 003_email_import
Create Date: 2026-05-28 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "004_feedback"
down_revision: str | None = "003_email_import"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("ai_response_id", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("is_helpful", sa.Boolean(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"]),
        sa.ForeignKeyConstraint(["ai_response_id"], ["ai_responses.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ai_response_id", name="uq_feedback_ai_response_id"),
    )
    op.create_index(
        "ix_feedback_ticket_id", "feedback", ["ticket_id"], unique=False
    )
    op.create_index(
        "ix_feedback_ai_response_id", "feedback", ["ai_response_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_feedback_ai_response_id", table_name="feedback")
    op.drop_index("ix_feedback_ticket_id", table_name="feedback")
    op.drop_table("feedback")
