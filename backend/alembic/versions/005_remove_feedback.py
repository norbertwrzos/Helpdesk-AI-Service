"""Remove feedback table.

Revision ID: 005_remove_feedback
Revises: 004_remove_agent_response
Create Date: 2026-06-10 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "005_remove_feedback"
down_revision: str | None = "004_remove_agent_response"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_table("feedback")


def downgrade() -> None:
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
