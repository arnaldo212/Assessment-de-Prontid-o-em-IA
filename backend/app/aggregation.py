"""
Funções puras de agregação — recebem listas de valores/registros já
carregados do banco e devolvem estatísticas. Mantidas separadas do
router para poderem ser testadas sem precisar de um Postgres rodando
(ver specs/03-agregacao-dashboard/).
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median, pstdev
from typing import Sequence

MIN_RESPONDENTES_POR_AREA = 3
OUTRAS_LABEL = "outras"


@dataclass(frozen=True)
class Distribution:
    mean: float
    median: float
    stdev: float
    n: int


def distribution(valores: Sequence[float]) -> Distribution:
    if not valores:
        return Distribution(mean=0.0, median=0.0, stdev=0.0, n=0)
    return Distribution(
        mean=round(mean(valores), 2),
        median=round(median(valores), 2),
        stdev=round(pstdev(valores), 2) if len(valores) > 1 else 0.0,
        n=len(valores),
    )


def group_by_area(
    registros: Sequence[dict],
    min_respondentes: int = MIN_RESPONDENTES_POR_AREA,
) -> dict[str, list[dict]]:
    """
    Agrupa registros (cada um precisa ter chave "area") por área.
    Áreas com menos de `min_respondentes` são somadas em OUTRAS_LABEL,
    conforme spec 03 requisito 2 (evitar reidentificar respondente único).
    """
    por_area: dict[str, list[dict]] = {}
    for r in registros:
        por_area.setdefault(r["area"] or OUTRAS_LABEL, []).append(r)

    resultado: dict[str, list[dict]] = {}
    outras: list[dict] = []
    for area, regs in por_area.items():
        if area != OUTRAS_LABEL and len(regs) < min_respondentes:
            outras.extend(regs)
        else:
            resultado[area] = regs
    if outras:
        resultado.setdefault(OUTRAS_LABEL, []).extend(outras)
    return resultado


def quadrant_distribution(badges: Sequence[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for b in badges:
        counts[b] = counts.get(b, 0) + 1
    return counts


def company_maturity(readiness_mean: float, literacy_mean: float, opportunity_mean: float) -> int:
    """
    Número único (0-100) resumindo a maturidade da empresa em IA — média
    simples entre as médias de prontidão, literacia e oportunidade.
    O índice técnico fica fora de propósito (specs/03-agregacao-dashboard/
    requirements.md, item 1.1): sua base amostral é menor e diferente
    (só gestores/tech respondem), então incluí-lo com peso igual
    enviesaria o número.
    """
    return round((readiness_mean + literacy_mean + opportunity_mean) / 3)
