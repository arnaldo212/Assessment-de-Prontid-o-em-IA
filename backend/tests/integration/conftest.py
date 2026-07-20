from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Area, Company, InstrumentVersion, Role, User
from app.security import hash_password


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def seeded(db_session):
    company = Company(name="Empresa Teste")
    db_session.add(company)
    db_session.flush()

    area = Area(company_id=company.id, name="Tecnologia")
    db_session.add(area)
    db_session.flush()

    version = InstrumentVersion(label="v1", weights={}, is_active=True)
    db_session.add(version)

    users = {}
    for email, role in [
        ("colaborador@teste.com", Role.collaborator),
        ("gestor@teste.com", Role.manager),
        ("admin@teste.com", Role.admin),
    ]:
        u = User(
            company_id=company.id,
            area_id=area.id,
            email=email,
            hashed_password=hash_password("senha123"),
            role=role,
        )
        db_session.add(u)
        db_session.flush()
        users[role.value] = u

    db_session.commit()
    return {"company": company, "area": area, "version": version, "users": users}
