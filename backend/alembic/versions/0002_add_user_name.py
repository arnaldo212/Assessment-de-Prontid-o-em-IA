"""add name column to users

Revision ID: 0002_add_user_name
Revises: 0001_initial
Create Date: 2026-07-20

"""
from alembic import op
import sqlalchemy as sa

revision = "0002_add_user_name"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("name", sa.String(150), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_column("users", "name")
