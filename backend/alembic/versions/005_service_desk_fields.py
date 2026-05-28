"""Stage 6: service-desk fields and status workflow refactor

Revision ID: 005_service_desk_fields
Revises: 004_feedback
Create Date: 2026-05-28 00:00:00.000000

Changes:
- Replaces ticketstatus enum values:
    new         -> open
    in_analysis -> ai_reviewed
    answered    -> pending
  (resolved and rejected are kept as-is)
- Adds columns: requester_email, requester_name,
                assigned_agent_name, agent_response
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "005_service_desk_fields"
down_revision: str | None = "004_feedback"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── 1. New enum type ──────────────────────────────────────────────
    op.execute(
        "CREATE TYPE ticketstatus_new AS ENUM "
        "('open', 'ai_reviewed', 'pending', 'resolved', 'rejected')"
    )

    # ── 2. Add new columns ────────────────────────────────────────────
    op.add_column(
        "tickets",
        sa.Column("requester_email", sa.String(255), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("requester_name", sa.String(255), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("assigned_agent_name", sa.String(255), nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("agent_response", sa.Text(), nullable=True),
    )

    # ── 3. Temp column with new enum type ─────────────────────────────
    op.execute(
        "ALTER TABLE tickets ADD COLUMN status_new ticketstatus_new"
    )

    # ── 4. Migrate status values ──────────────────────────────────────
    op.execute(
        """
        UPDATE tickets
        SET status_new = CASE
            WHEN status = 'new'         THEN 'open'::ticketstatus_new
            WHEN status = 'in_analysis' THEN 'ai_reviewed'::ticketstatus_new
            WHEN status = 'answered'    THEN 'pending'::ticketstatus_new
            WHEN status = 'resolved'    THEN 'resolved'::ticketstatus_new
            WHEN status = 'rejected'    THEN 'rejected'::ticketstatus_new
            ELSE 'open'::ticketstatus_new
        END
        """
    )

    # ── 5. Constraints on new column ──────────────────────────────────
    op.execute(
        "ALTER TABLE tickets ALTER COLUMN status_new SET NOT NULL"
    )
    op.execute(
        "ALTER TABLE tickets ALTER COLUMN status_new "
        "SET DEFAULT 'open'::ticketstatus_new"
    )

    # ── 6. Swap columns ───────────────────────────────────────────────
    op.execute("ALTER TABLE tickets DROP COLUMN status")
    op.execute("ALTER TABLE tickets RENAME COLUMN status_new TO status")

    # ── 7. Swap enum types ────────────────────────────────────────────
    op.execute("DROP TYPE ticketstatus")
    op.execute("ALTER TYPE ticketstatus_new RENAME TO ticketstatus")


def downgrade() -> None:
    # ── 1. Recreate old enum type ─────────────────────────────────────
    op.execute(
        "CREATE TYPE ticketstatus_old AS ENUM "
        "('new', 'in_analysis', 'answered', 'resolved', 'rejected')"
    )

    # ── 2. Temp column with old enum type ─────────────────────────────
    op.execute(
        "ALTER TABLE tickets ADD COLUMN status_old ticketstatus_old"
    )

    # ── 3. Reverse status migration ───────────────────────────────────
    op.execute(
        """
        UPDATE tickets
        SET status_old = CASE
            WHEN status = 'open'        THEN 'new'::ticketstatus_old
            WHEN status = 'ai_reviewed' THEN 'in_analysis'::ticketstatus_old
            WHEN status = 'pending'     THEN 'answered'::ticketstatus_old
            WHEN status = 'resolved'    THEN 'resolved'::ticketstatus_old
            WHEN status = 'rejected'    THEN 'rejected'::ticketstatus_old
            ELSE 'new'::ticketstatus_old
        END
        """
    )

    op.execute(
        "ALTER TABLE tickets ALTER COLUMN status_old SET NOT NULL"
    )
    op.execute(
        "ALTER TABLE tickets ALTER COLUMN status_old "
        "SET DEFAULT 'new'::ticketstatus_old"
    )

    # ── 4. Swap columns ───────────────────────────────────────────────
    op.execute("ALTER TABLE tickets DROP COLUMN status")
    op.execute("ALTER TABLE tickets RENAME COLUMN status_old TO status")

    # ── 5. Swap enum types ────────────────────────────────────────────
    op.execute("DROP TYPE ticketstatus")
    op.execute("ALTER TYPE ticketstatus_old RENAME TO ticketstatus")

    # ── 6. Drop added columns ─────────────────────────────────────────
    op.drop_column("tickets", "agent_response")
    op.drop_column("tickets", "assigned_agent_name")
    op.drop_column("tickets", "requester_name")
    op.drop_column("tickets", "requester_email")
