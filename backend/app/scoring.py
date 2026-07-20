"""
Camada de cálculo dos índices de prontidão em IA.

Todas as funções aqui são puras: recebem valores e devolvem valores,
sem tocar em banco, rede ou estado global. Isso é proposital — é o que
torna o módulo 100% testável por spec (ver specs/01-scoring/) e portável
para qualquer front-end ou job de recálculo.

As fórmulas são a implementação literal de specs/01-scoring/requirements.md,
que por sua vez foi extraída da lógica validada nos protótipos
Formulario_1_Geral.html e Formulario_2_Tecnico.html.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Literal, Sequence

Nivel = Literal["alta", "baixa", "cinzenta"]


def norm(raw: float, mn: float, mx: float) -> int:
    """Normaliza um valor bruto para uma escala 0-100."""
    return round((raw - mn) / (mx - mn) * 100)


# ---------------------------------------------------------------------
# Módulos 1-3 (Organização / Times / Pessoas) — Formulário 1
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class ModuleScore:
    raw: int
    idx: int


def score_module(q1: int, q2: int, q3: int, q4_reverso: int, q5_escada: int) -> ModuleScore:
    """q1-q3 diretos (1-5), q4 reverso (1-5), q5 escada (1-4). raw: 5-24."""
    raw = q1 + q2 + q3 + (6 - q4_reverso) + q5_escada
    return ModuleScore(raw=raw, idx=norm(raw, 5, 24))


def readiness_band(readiness: int) -> str:
    if readiness <= 52:
        return "Fundamentos"
    if readiness <= 63:
        return "Zona incerta"
    return "Pronto"


def compute_readiness(m1: ModuleScore, m2: ModuleScore, m3: ModuleScore) -> int:
    raw_total = m1.raw + m2.raw + m3.raw  # min 15, max 72
    return norm(raw_total, 15, 72)


# ---------------------------------------------------------------------
# Literacia (peso 50/15/35)
# ---------------------------------------------------------------------

def self_perception_norm(a1: int, a2: int, a4: int, a5: int, a6: int, a7: int, a8: int, a9_reverso: int) -> float:
    raw = a1 + a2 + a4 + a5 + a6 + a7 + a8 + (6 - a9_reverso)  # min 8, max 39
    return (raw - 8) / (39 - 8) * 100


def breadth_norm(usos_marcados: int, total_opcoes: int = 8) -> float:
    return usos_marcados / total_opcoes * 100


def objective_norm(acertos: int, total: int = 6) -> float:
    return acertos / total * 100


def compute_literacy(self_norm: float, breadth_norm_: float, objective_norm_: float) -> int:
    return round(0.50 * self_norm + 0.15 * breadth_norm_ + 0.35 * objective_norm_)


def literacy_band(literacy: int) -> str:
    if literacy >= 60:
        return "Avançado"
    if literacy >= 40:
        return "Intermediário"
    return "Iniciante"


# ---------------------------------------------------------------------
# Oportunidade
# ---------------------------------------------------------------------

def compute_opportunity(b_items: Sequence[int]) -> int:
    """b_items: b1..b8, cada um 1-5."""
    opp_mean = mean(b_items)
    return round((opp_mean - 1) / 4 * 100)


def automatability_label(b9b_escada: int) -> str:
    if b9b_escada <= 2:
        return "baixo"
    if b9b_escada == 3:
        return "médio"
    return "alto"


# ---------------------------------------------------------------------
# Índice Técnico (Módulo 4) — Formulário 2
# ---------------------------------------------------------------------

def compute_technical(
    q42: int, q43: int, q44: int, q45: int, q47: int,
    q48_reverso: int, q41_escada: int, q46_escada: int,
) -> int:
    raw = (q42 + q43 + q44 + q45 + q47) + (6 - q48_reverso) + q41_escada + q46_escada  # min 8, max 38
    return round((raw - 8) / 30 * 100)


def technical_band(idx: int) -> str:
    if idx <= 40:
        return "Base técnica frágil"
    if idx <= 65:
        return "Em construção"
    return "Base técnica sólida"


# ---------------------------------------------------------------------
# Quadrante literacia x oportunidade
# ---------------------------------------------------------------------

MIN_RESPONDENTES_PERCENTIL = 5


def percentile_rank(valor: float, distribuicao: Sequence[float]) -> float:
    """Percentual de valores na distribuição que são <= valor. 0-100."""
    if not distribuicao:
        return 50.0
    menores_ou_iguais = sum(1 for v in distribuicao if v <= valor)
    return menores_ou_iguais / len(distribuicao) * 100


def _nivel_por_percentil(percentil: float) -> Nivel:
    if percentil >= 60:
        return "alta"
    if percentil <= 40:
        return "baixa"
    return "cinzenta"


def _nivel_por_corte_fixo(valor: float) -> Nivel:
    if valor >= 60:
        return "alta"
    if valor <= 40:
        return "baixa"
    return "cinzenta"


@dataclass(frozen=True)
class Quadrant:
    badge: str
    title: str
    text: str
    provisorio: bool


_QUADRANT_MAP: dict[tuple[Nivel, Nivel], tuple[str, str, str]] = {
    ("alta", "alta"): (
        "Acelerar já", "Alta literacia · alta oportunidade",
        "Perfil pronto para autonomia: dê ferramentas, casos de uso reais e espaço para aplicar.",
    ),
    ("alta", "baixa"): (
        "Multiplicador", "Alta literacia · baixa oportunidade",
        "Ótimo candidato a mentor/embaixador interno de IA, apoiando outras áreas.",
    ),
    ("baixa", "alta"): (
        "Prioridade de treinamento", "Baixa literacia · alta oportunidade",
        "Maior retorno de capacitação: o trabalho pede IA e falta o conhecimento. Priorize treinamento.",
    ),
    ("baixa", "baixa"): (
        "Menor prioridade agora", "Baixa literacia · baixa oportunidade",
        "Basta uma literacia básica de segurança e consciência sobre IA por enquanto.",
    ),
}

_INDEFINIDO = (
    "Indefinido — revisar", "Perto da fronteira",
    "Uma das dimensões ficou na zona intermediária. Vale uma leitura humana antes de classificar — "
    "não force um rótulo automático.",
)


def compute_quadrant(
    literacia: float,
    oportunidade: float,
    distribuicao_literacia: Sequence[float],
    distribuicao_oportunidade: Sequence[float],
) -> Quadrant:
    """
    Usa percentil (corte 40/60) quando há respondentes suficientes na base;
    cai para corte fixo absoluto (igual ao protótipo) com poucos respondentes,
    marcando o resultado como provisório.
    """
    n = len(distribuicao_literacia)
    provisorio = n < MIN_RESPONDENTES_PERCENTIL

    if provisorio:
        nivel_lit = _nivel_por_corte_fixo(literacia)
        nivel_opp = _nivel_por_corte_fixo(oportunidade)
    else:
        pct_lit = percentile_rank(literacia, distribuicao_literacia)
        pct_opp = percentile_rank(oportunidade, distribuicao_oportunidade)
        nivel_lit = _nivel_por_percentil(pct_lit)
        nivel_opp = _nivel_por_percentil(pct_opp)

    if nivel_lit == "cinzenta" or nivel_opp == "cinzenta":
        badge, title, text = _INDEFINIDO
    else:
        badge, title, text = _QUADRANT_MAP[(nivel_lit, nivel_opp)]

    return Quadrant(badge=badge, title=title, text=text, provisorio=provisorio)
