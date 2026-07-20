"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-20

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

# Usado só para criar o tipo explicitamente uma vez (checkfirst=True).
role_enum_create = postgresql.ENUM("collaborator", "manager", "admin", name="role_enum")
# Usado na coluna da tabela — create_type=False evita que create_table()
# tente criar o mesmo tipo de novo (o que quebraria com "already exists",
# já que o create_table do Alembic não faz checkfirst nessa criação automática).
role_enum_column = postgresql.ENUM(
    "collaborator", "manager", "admin", name="role_enum", create_type=False
)


def upgrade() -> None:
    role_enum_create.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "areas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.UniqueConstraint("company_id", "name", name="uq_area_company_name"),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("area_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("areas.id"), nullable=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", role_enum_column, nullable=False, server_default="collaborator"),
        sa.Column("is_active", sa.Boolean, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "instrument_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("label", sa.String(50), nullable=False, unique=True),
        sa.Column("weights", sa.JSON, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "form1_responses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("instrument_version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("instrument_versions.id"), nullable=False),
        sa.Column("answers", sa.JSON, nullable=False),
        sa.Column("m1_raw", sa.Integer, nullable=False),
        sa.Column("m1_idx", sa.Integer, nullable=False),
        sa.Column("m2_raw", sa.Integer, nullable=False),
        sa.Column("m2_idx", sa.Integer, nullable=False),
        sa.Column("m3_raw", sa.Integer, nullable=False),
        sa.Column("m3_idx", sa.Integer, nullable=False),
        sa.Column("readiness", sa.Integer, nullable=False),
        sa.Column("literacy", sa.Integer, nullable=False),
        sa.Column("opportunity", sa.Integer, nullable=False),
        sa.Column("objective_correct", sa.Integer, nullable=False),
        sa.Column("automatability_label", sa.String(20), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "instrument_version_id", name="uq_form1_user_version"),
    )

    op.create_table(
        "form2_responses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("instrument_version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("instrument_versions.id"), nullable=False),
        sa.Column("answers", sa.JSON, nullable=False),
        sa.Column("technical_idx", sa.Integer, nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "instrument_version_id", name="uq_form2_user_version"),
    )


def downgrade() -> None:
    op.drop_table("form2_responses")
    op.drop_table("form1_responses")
    op.drop_table("instrument_versions")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_table("areas")
    op.drop_table("companies")
    role_enum_create.drop(op.get_bind(), checkfirst=True)
