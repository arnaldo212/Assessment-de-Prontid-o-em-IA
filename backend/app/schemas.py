from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import Role


# ---------------- Auth ----------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: Role
    company_id: uuid.UUID
    company_name: str
    area_id: uuid.UUID | None

    model_config = ConfigDict(from_attributes=True)


# ---------------- Cadastro de pessoas (admin) ----------------

class PersonCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role
    area_name: str | None = None


class PersonOut(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: Role
    area_name: str | None


# ---------------- Formulário 1 ----------------

class Form1SubmitRequest(BaseModel):
    answers: dict[str, int | list[str] | str]


class Form1ResultOut(BaseModel):
    m1_idx: int
    m2_idx: int
    m3_idx: int
    readiness: int
    readiness_band: str
    literacy: int
    literacy_band: str
    objective_correct: int
    opportunity: int
    automatability_label: str
    quadrant_badge: str
    quadrant_title: str
    quadrant_text: str
    quadrant_provisional: bool


# ---------------- Formulário 2 ----------------

class Form2SubmitRequest(BaseModel):
    answers: dict[str, int | str]


class Form2ResultOut(BaseModel):
    technical_idx: int
    technical_band: str


# ---------------- Dashboard ----------------

class DistributionOut(BaseModel):
    mean: float
    median: float
    stdev: float
    n: int


class AreaBreakdownOut(BaseModel):
    area: str
    readiness: DistributionOut
    literacy: DistributionOut
    opportunity: DistributionOut


class QuadrantCountOut(BaseModel):
    badge: str
    count: int


class DashboardOut(BaseModel):
    total_respondents: int
    maturity: int
    readiness: DistributionOut
    literacy: DistributionOut
    opportunity: DistributionOut
    technical: DistributionOut | None
    by_area: list[AreaBreakdownOut]
    quadrant_distribution: list[QuadrantCountOut]
