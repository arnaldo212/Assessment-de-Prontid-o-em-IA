from __future__ import annotations

from tests.integration.test_auth_and_forms import _auth_headers, _login


def test_me_retorna_dados_do_usuario_logado(client, seeded):
    token = _login(client, "gestor@teste.com")
    resp = client.get("/auth/me", headers=_auth_headers(token))
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["email"] == "gestor@teste.com"
    assert body["role"] == "manager"
    assert body["company_name"] == "Empresa Teste"


def test_me_sem_token_retorna_401(client, seeded):
    resp = client.get("/auth/me")
    assert resp.status_code in (401, 403)  # HTTPBearer sem header retorna 403 por padrão
