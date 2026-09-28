"""add applications

Revision ID: 3f4c8e2a1b77
Revises: 88105034caf5
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "3f4c8e2a1b77"
down_revision: Union[str, Sequence[str], None] = "88105034caf5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "applications",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("candidate_id", sa.String(length=36), nullable=False),
        sa.Column("resume_id", sa.String(length=36), nullable=False),
        sa.Column("cover_note", sa.Text(), nullable=True),
        sa.Column("status", sa.Enum("applied", "shortlisted", "rejected", "hired", name="applicationstatus"), nullable=False),
        sa.Column("match_score", sa.Float(), nullable=True),
        sa.Column("applied_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["candidate_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["resume_id"], ["resumes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id", "candidate_id", name="uq_application_job_candidate"),
    )
    op.create_index("ix_applications_job_id", "applications", ["job_id"])
    op.create_index("ix_applications_candidate_id", "applications", ["candidate_id"])


def downgrade() -> None:
    op.drop_index("ix_applications_candidate_id", table_name="applications")
    op.drop_index("ix_applications_job_id", table_name="applications")
    op.drop_table("applications")
