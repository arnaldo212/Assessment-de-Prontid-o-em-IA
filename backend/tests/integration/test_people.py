from __future__ import annotations

from app.models import Company, Role, User
from app.security import hash_password
from tests.integration.test_auth_and_forms import _auth_headers, _login


def test_admin_cadastra_nova_pessoa(client, seeded):
    admin_token = _login(client, "admin@teste.com")
    resp = client.post(
        "/people",
        json={
            "name": "Nova Pessoa",
            "email": "nova@teste.com",
            "password": "senha123",
            "role": "collaborator",
            "area_name": "Marketing",
        },
        headers=_auth_headers(admin_token),
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["name"] == "Nova Pessoa"
    assert body["area_name"] == "Marketing"

    # a pessoa cadastrada já consegue logar
    login_resp = client.post("/auth/login", json={"email": "nova@teste.com", "password": "senha123"})
    assert login_resp.status_code == 200


def test_apenas_admin_cadastra_pessoas(client, seeded):
    gestor_token = _login(client, "gestor@teste.com")
    resp = client.post(
        "/people",
        json={"name": "X", "email": "x@teste.com", "password": "senha123", "role": "collaborator"},
        headers=_auth_headers(gestor_token),
    )
    assert resp.status_code == 403


def test_cadastro_com_email_duplicado_retorna_409(client, seeded):
    admin_token = _login(client, "admin@teste.com")
    headers = _auth_headers(admin_token)
    payload = {
        "name": "Duplicado",
        "email": "duplicado@teste.com",
        "password": "senha123",
        "role": "collaborator",
    }
    first = client.post("/people", json=payload, headers=headers)
    assert first.status_code == 201
    second = client.post("/people", json=payload, headers=headers)
    assert second.status_code == 409


def test_listar_pessoas_e_escopado_por_empresa(client, db_session, seeded):
    other_company = Company(name="Outra Empresa")
    db_session.add(other_company)
    db_session.flush()
    db_session.add(
        User(
            company_id=other_company.id,
            name="Pessoa de Outra Empresa",
            email="outra@empresa.com",
            hashed_password=hash_password("senha123"),
            role=Role.collaborator,
        )
    )
    db_session.commit()

    admin_token = _login(client, "admin@teste.com")
    resp = client.get("/people", headers=_auth_headers(admin_token))
    assert resp.status_code == 200
    emails = [p["email"] for p in resp.json()]
    assert "outra@empresa.com" not in emails
    assert "admin@teste.com" in emails
