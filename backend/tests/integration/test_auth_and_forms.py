from __future__ import annotations

from tests.integration.payloads import VALID_FORM1_ANSWERS, VALID_FORM2_ANSWERS


def _login(client, email: str, password: str = "senha123") -> str:
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_colaborador_nao_pode_enviar_formulario_2(client, seeded):
    # Scenario: Colaborador comum não pode enviar o Formulário 2
    token = _login(client, "colaborador@teste.com")
    resp = client.post("/forms/form2", json={"answers": VALID_FORM2_ANSWERS}, headers=_auth_headers(token))
    assert resp.status_code == 403


def test_gestor_pode_enviar_formulario_1_e_2(client, seeded):
    # Scenario: Gestor pode enviar o Formulário 1 e o Formulário 2
    token = _login(client, "gestor@teste.com")
    r1 = client.post("/forms/form1", json={"answers": VALID_FORM1_ANSWERS}, headers=_auth_headers(token))
    assert r1.status_code == 201, r1.text
    r2 = client.post("/forms/form2", json={"answers": VALID_FORM2_ANSWERS}, headers=_auth_headers(token))
    assert r2.status_code == 201, r2.text


def test_reenvio_do_mesmo_formulario_e_bloqueado(client, seeded):
    # Scenario: Reenvio do mesmo formulário na mesma versão é bloqueado
    token = _login(client, "gestor@teste.com")
    headers = _auth_headers(token)
    first = client.post("/forms/form1", json={"answers": VALID_FORM1_ANSWERS}, headers=headers)
    assert first.status_code == 201
    second = client.post("/forms/form1", json={"answers": VALID_FORM1_ANSWERS}, headers=headers)
    assert second.status_code == 409


def test_apenas_admin_acessa_dashboard(client, seeded):
    # Scenario: Apenas admin acessa o dashboard agregado
    token = _login(client, "gestor@teste.com")
    resp = client.get("/dashboard", headers=_auth_headers(token))
    assert resp.status_code == 403

    admin_token = _login(client, "admin@teste.com")
    resp_admin = client.get("/dashboard", headers=_auth_headers(admin_token))
    assert resp_admin.status_code == 200


def test_login_com_credenciais_invalidas(client, seeded):
    resp = client.post("/auth/login", json={"email": "gestor@teste.com", "password": "errada"})
    assert resp.status_code == 401
