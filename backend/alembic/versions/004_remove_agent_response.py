"""Remove legacy agent_response from tickets.

Revision ID: 004_remove_agent_response
Revises: 003_ticket_messages
Create Date: 2026-06-10 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "004_remove_agent_response"
down_revision: str | None = "003_ticket_messages"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("tickets", "agent_response")


def downgrade() -> None:
    op.add_column(
        "tickets",
        sa.Column("agent_response", sa.Text(), nullable=True),
    )
