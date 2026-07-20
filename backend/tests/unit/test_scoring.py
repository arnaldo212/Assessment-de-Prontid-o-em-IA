"""
Testes unitários da camada de scoring. Cada teste corresponde a um
Scenario em specs/01-scoring/scoring.feature — os nomes e valores são
os mesmos de propósito, para que quem lê a spec ache o teste fácil.
"""
from app import scoring


def test_indice_de_modulo_com_reverso_e_escada():
    # Scenario: Índice de módulo com item reverso e escada
    r = scoring.score_module(q1=4, q2=3, q3=5, q4_reverso=2, q5_escada=3)
    # raw = 4+3+5+(6-2)+3 = 19; idx = norm(19,5,24) = round(14/19*100) = 74
    assert r.raw == 19
    assert r.idx == 74


def test_prontidao_percebida_agrega_tres_modulos():
    # Scenario: Prontidão percebida agrega os três módulos
    m1 = scoring.ModuleScore(raw=17, idx=0)
    m2 = scoring.ModuleScore(raw=15, idx=0)
    m3 = scoring.ModuleScore(raw=20, idx=0)
    # raw_total = 17+15+20 = 52; norm(52,15,72) = round(37/57*100) = 65
    assert scoring.compute_readiness(m1, m2, m3) == 65


def test_faixa_zona_incerta():
    # Scenario: Faixa "Zona incerta" da prontidão
    assert scoring.readiness_band(58) == "Zona incerta"


def test_faixas_prontidao_limites():
    assert scoring.readiness_band(52) == "Fundamentos"
    assert scoring.readiness_band(63) == "Zona incerta"
    assert scoring.readiness_band(64) == "Pronto"


def test_literacia_combina_pesos_50_15_35():
    # Scenario: Literacia combina autopercepção, amplitude e acertos com pesos 50/15/35
    idx = scoring.compute_literacy(self_norm=80, breadth_norm_=50, objective_norm_=100)
    # 0.50*80 + 0.15*50 + 0.35*100 = 40 + 7.5 + 35 = 82.5 -> round() do Python
    # usa round-half-to-even -> 82
    assert idx == 82


def test_oportunidade_media_normalizada():
    # Scenario: Oportunidade é a média normalizada dos itens b1 a b8
    idx = scoring.compute_opportunity([3, 4, 3, 5, 2, 4, 3, 4])
    # média = 28/8 = 3.5; (3.5-1)/4*100 = 62.5 -> round-half-to-even -> 62
    assert idx == 62


def test_indice_tecnico_modulo_4():
    # Scenario: Índice técnico do módulo 4
    idx = scoring.compute_technical(
        q42=4, q43=5, q44=3, q45=4, q47=3, q48_reverso=2, q41_escada=3, q46_escada=2,
    )
    # raw = (4+5+3+4+3) + (6-2) + 3 + 2 = 19+4+5 = 28; (28-8)/30*100 = 66.67 -> 67
    assert idx == 67


def test_quadrante_poucos_respondentes_usa_corte_fixo_e_marca_provisorio():
    # Scenario: Quadrante com poucos respondentes usa cortes fixos e sinaliza provisório
    distribuicao = [50.0, 55.0, 60.0]  # 3 respondentes < MIN_RESPONDENTES_PERCENTIL
    q = scoring.compute_quadrant(70, 75, distribuicao, distribuicao)
    assert q.badge == "Acelerar já"
    assert q.provisorio is True


def test_quadrante_base_suficiente_usa_percentil_prioridade_treinamento():
    # Scenario: Quadrante com base suficiente usa percentil
    # Prioridade de treinamento = literacia BAIXA (percentil <= 40) + oportunidade ALTA (percentil >= 60)
    dist = list(range(1, 21))  # 20 valores, percentil calculado por posição relativa
    valor_lit = 6    # 6 de 20 valores <= 6 -> percentil 30 (baixa)
    valor_opp = 13   # 13 de 20 valores <= 13 -> percentil 65 (alta)
    q = scoring.compute_quadrant(valor_lit, valor_opp, dist, dist)
    assert q.badge == "Prioridade de treinamento"
    assert q.provisorio is False


def test_quadrante_zona_cinzenta_gera_indefinido():
    # Scenario: Zona cinzenta gera quadrante indefinido
    dist = list(range(1, 21))
    valor_lit = 10   # percentil 50 -> cinzenta
    valor_opp = 16   # percentil 80 -> alta
    q = scoring.compute_quadrant(valor_lit, valor_opp, dist, dist)
    assert q.badge == "Indefinido — revisar"


def test_percentile_rank_basico():
    assert scoring.percentile_rank(13, list(range(1, 21))) == 65.0
    assert scoring.percentile_rank(6, list(range(1, 21))) == 30.0
