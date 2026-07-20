from __future__ import annotations

from app.models import Area, Company, InstrumentVersion, Role, User
from app.security import hash_password
from tests.integration.payloads import VALID_FORM1_ANSWERS
from tests.integration.test_auth_and_forms import _auth_headers, _login


def _make_company_with_users(db_session, label: str, n_collaborators: int):
    company = Company(name=f"Empresa {label}")
    db_session.add(company)
    db_session.flush()

    area = Area(company_id=company.id, name="Geral")
    db_session.add(area)
    db_session.flush()

    admin = User(
        company_id=company.id, area_id=area.id,
        email=f"admin-{label.lower()}@teste.com",
        hashed_password=hash_password("senha123"), role=Role.admin,
    )
    db_session.add(admin)

    collaborators = []
    for i in range(n_collaborators):
        u = User(
            company_id=company.id, area_id=area.id,
            email=f"colab-{label.lower()}-{i}@teste.com",
            hashed_password=hash_password("senha123"), role=Role.collaborator,
        )
        db_session.add(u)
        collaborators.append(u)

    db_session.commit()
    return company, admin, collaborators


def test_dashboard_nao_mistura_dados_de_empresas_diferentes(client, db_session):
    # Scenario: Dashboard não mistura dados de empresas diferentes
    version = InstrumentVersion(label="v1", weights={}, is_active=True)
    db_session.add(version)
    db_session.commit()

    company_a, admin_a, collabs_a = _make_company_with_users(db_session, "A", 5)
    company_b, admin_b, collabs_b = _make_company_with_users(db_session, "B", 3)

    for u in collabs_a + collabs_b:
        token = _login(client, u.email)
        resp = client.post("/forms/form1", json={"answers": VALID_FORM1_ANSWERS}, headers=_auth_headers(token))
        assert resp.status_code == 201, resp.text

    admin_a_token = _login(client, admin_a.email)
    resp = client.get("/dashboard", headers=_auth_headers(admin_a_token))
    assert resp.status_code == 200
    body = resp.json()

    assert body["total_respondents"] == 5
    assert 0 <= body["maturity"] <= 100
