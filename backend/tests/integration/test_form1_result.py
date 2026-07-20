from __future__ import annotations

from tests.integration.payloads import VALID_FORM1_ANSWERS
from tests.integration.test_auth_and_forms import _auth_headers, _login


def test_submissao_form1_retorna_indices_calculados(client, seeded):
    token = _login(client, "colaborador@teste.com")
    resp = client.post("/forms/form1", json={"answers": VALID_FORM1_ANSWERS}, headers=_auth_headers(token))
    assert resp.status_code == 201, resp.text
    body = resp.json()

    assert 0 <= body["readiness"] <= 100
    assert 0 <= body["literacy"] <= 100
    assert 0 <= body["opportunity"] <= 100
    assert body["readiness_band"] in {"Fundamentos", "Zona incerta", "Pronto"}
    assert body["literacy_band"] in {"Iniciante", "Intermediário", "Avançado"}
    assert body["quadrant_badge"] in {
        "Acelerar já", "Multiplicador", "Prioridade de treinamento",
        "Menor prioridade agora", "Indefinido — revisar",
    }
    # base tem 1 respondente só -> deve cair no modo provisório (corte fixo)
    assert body["quadrant_provisional"] is True
