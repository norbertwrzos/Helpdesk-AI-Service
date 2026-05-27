"""Stage 3: add knowledge_articles, ai_responses tables; extend tickets

Revision ID: 002_analysis_pipeline
Revises: 001_initial
Create Date: 2026-05-27 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "002_analysis_pipeline"
down_revision: str | None = "001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "knowledge_articles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("tags", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "ai_responses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("response_text", sa.Text(), nullable=False),
        sa.Column(
            "model_name",
            sa.String(length=100),
            nullable=False,
            server_default="mock-ai-generator",
        ),
        sa.Column(
            "provider_name",
            sa.String(length=100),
            nullable=False,
            server_default="mock",
        ),
        sa.Column("sources_used", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column(
        "tickets",
        sa.Column("classification_confidence", sa.Float(), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("priority_confidence", sa.Float(), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("classification_explanation", sa.Text(), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("priority_explanation", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tickets", "priority_explanation")
    op.drop_column("tickets", "classification_explanation")
    op.drop_column("tickets", "priority_confidence")
    op.drop_column("tickets", "classification_confidence")
    op.drop_table("ai_responses")
    op.drop_table("knowledge_articles")
