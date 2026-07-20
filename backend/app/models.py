from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Uuid,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Uuid (sqlalchemy.Uuid) é portável entre Postgres e SQLite — usamos SQLite
# nos testes de integração (rápido, sem infraestrutura) e Postgres em
# dev/produção via o mesmo metadata.
UUID = Uuid

from app.database import Base


def _uuid() -> uuid.UUID:
    return uuid.uuid4()


class Role(str, enum.Enum):
    collaborator = "collaborator"
    manager = "manager"
    admin = "admin"


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    areas: Mapped[list["Area"]] = relationship(back_populates="company")
    users: Mapped[list["User"]] = relationship(back_populates="company")


class Area(Base):
    __tablename__ = "areas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    company: Mapped["Company"] = relationship(back_populates="areas")
    users: Mapped[list["User"]] = relationship(back_populates="area")

    __table_args__ = (UniqueConstraint("company_id", "name", name="uq_area_company_name"),)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    area_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("areas.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, server_default="")
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, name="role_enum"), nullable=False, default=Role.collaborator)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    company: Mapped["Company"] = relationship(back_populates="users")
    area: Mapped["Area | None"] = relationship(back_populates="users")
    form1_responses: Mapped[list["Form1Response"]] = relationship(back_populates="user")
    form2_responses: Mapped[list["Form2Response"]] = relationship(back_populates="user")


class InstrumentVersion(Base):
    """
    Versão do instrumento de avaliação: pesos, cortes e âncoras vigentes.
    Nunca é editada após ativa — recalibrações criam uma nova linha, e
    respostas antigas continuam referenciando a versão em que foram enviadas
    (spec 03, requisito 5).
    """

    __tablename__ = "instrument_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    label: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)  # ex: "v1", "v2-recalibrado-2026Q3"
    weights: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)  # pesos/cortes/âncoras
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Form1Response(Base):
    __tablename__ = "form1_responses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    instrument_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instrument_versions.id"), nullable=False)

    answers: Mapped[dict] = mapped_column(JSON, nullable=False)  # respostas brutas por item id

    m1_raw: Mapped[int] = mapped_column(Integer, nullable=False)
    m1_idx: Mapped[int] = mapped_column(Integer, nullable=False)
    m2_raw: Mapped[int] = mapped_column(Integer, nullable=False)
    m2_idx: Mapped[int] = mapped_column(Integer, nullable=False)
    m3_raw: Mapped[int] = mapped_column(Integer, nullable=False)
    m3_idx: Mapped[int] = mapped_column(Integer, nullable=False)
    readiness: Mapped[int] = mapped_column(Integer, nullable=False)
    literacy: Mapped[int] = mapped_column(Integer, nullable=False)
    opportunity: Mapped[int] = mapped_column(Integer, nullable=False)
    objective_correct: Mapped[int] = mapped_column(Integer, nullable=False)
    automatability_label: Mapped[str] = mapped_column(String(20), nullable=False)

    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="form1_responses")

    __table_args__ = (
        UniqueConstraint("user_id", "instrument_version_id", name="uq_form1_user_version"),
    )


class Form2Response(Base):
    __tablename__ = "form2_responses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    instrument_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instrument_versions.id"), nullable=False)

    answers: Mapped[dict] = mapped_column(JSON, nullable=False)
    technical_idx: Mapped[int] = mapped_column(Integer, nullable=False)

    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="form2_responses")

    __table_args__ = (
        UniqueConstraint("user_id", "instrument_version_id", name="uq_form2_user_version"),
    )
