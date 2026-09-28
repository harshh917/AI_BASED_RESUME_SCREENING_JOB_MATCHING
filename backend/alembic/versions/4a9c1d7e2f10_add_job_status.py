"""add job status

Revision ID: 4a9c1d7e2f10
Revises: 3f4c8e2a1b77
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "4a9c1d7e2f10"
down_revision: Union[str, Sequence[str], None] = "3f4c8e2a1b77"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column("jobs", sa.Column("status", sa.String(length=20), nullable=False, server_default="active"))
    op.create_index("ix_jobs_status", "jobs", ["status"])

def downgrade() -> None:
    op.drop_index("ix_jobs_status", table_name="jobs")
    op.drop_column("jobs", "status")
