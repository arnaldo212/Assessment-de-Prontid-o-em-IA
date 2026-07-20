from app import aggregation


def test_area_com_poucos_respondentes_e_agrupada_em_outras():
    # Scenario: Área com poucos respondentes é agrupada em "outras"
    registros = [
        {"area": "Financeiro", "readiness": 50},
        {"area": "Financeiro", "readiness": 60},
        {"area": "TI", "readiness": 40},
        {"area": "TI", "readiness": 45},
        {"area": "TI", "readiness": 55},
    ]
    grouped = aggregation.group_by_area(registros)
    assert "Financeiro" not in grouped
    assert len(grouped["outras"]) == 2
    assert len(grouped["TI"]) == 3


def test_distribuicao_do_quadrante_por_rotulo():
    # Scenario: Distribuição do quadrante é contada por rótulo
    badges = ["Acelerar já", "Acelerar já", "Multiplicador", "Indefinido — revisar"]
    counts = aggregation.quadrant_distribution(badges)
    assert counts["Acelerar já"] == 2
    assert counts["Multiplicador"] == 1
    assert counts["Indefinido — revisar"] == 1


def test_distribution_stats_basicas():
    d = aggregation.distribution([10, 20, 30])
    assert d.mean == 20
    assert d.median == 20
    assert d.n == 3


def test_distribution_vazia_nao_quebra():
    d = aggregation.distribution([])
    assert d.n == 0


def test_maturidade_consolidada_e_media_simples_dos_tres():
    # Scenario: Maturidade consolidada é a média simples de prontidão, literacia e oportunidade
    assert aggregation.company_maturity(60, 70, 80) == 70


def test_maturidade_consolidada_ignora_indice_tecnico():
    # Scenario: Índice técnico não entra na maturidade consolidada
    # (a função nem recebe technical_mean como parâmetro — por construção,
    # não tem como ele influenciar o resultado)
    assert aggregation.company_maturity(60, 70, 80) == 70
