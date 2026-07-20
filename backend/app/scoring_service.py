"""
Traduz o dicionário de respostas brutas (como chega da API, com as mesmas
chaves de item usadas nos protótipos: m1q1, a1, b3, q42 etc.) para chamadas
às funções puras de app.scoring. Fica isolado aqui para que app.scoring
continue sem nenhum conhecimento de "formato de request".
"""
from __future__ import annotations

from app import scoring

# Gabarito das questões objetivas do bloco de literacia (Formulário 1),
# índice da alternativa correta — igual ao protótipo (campo `correct`).
OBJECTIVE_ANSWER_KEY = {
    "c1": 1,
    "c2": 2,
    "c3": 1,
    "c4": 0,
    "c5": 1,
    "c6": 1,
}

TOTAL_USO_OPCOES = 8  # opções em a3, sem contar "__none__"


def _module_score(answers: dict, prefix: str) -> scoring.ModuleScore:
    return scoring.score_module(
        q1=answers[f"{prefix}q1"],
        q2=answers[f"{prefix}q2"],
        q3=answers[f"{prefix}q3"],
        q4_reverso=answers[f"{prefix}q4"],
        q5_escada=answers[f"{prefix}q5"],
    )


def compute_form1(answers: dict) -> dict:
    m1 = _module_score(answers, "m1")
    m2 = _module_score(answers, "m2")
    m3 = _module_score(answers, "m3")
    readiness = scoring.compute_readiness(m1, m2, m3)

    self_norm = scoring.self_perception_norm(
        a1=answers["a1"], a2=answers["a2"],
        a4=answers["a4"], a5=answers["a5"], a6=answers["a6"],
        a7=answers["a7"], a8=answers["a8"], a9_reverso=answers["a9"],
    )
    usos = answers.get("a3") or []
    usos_marcados = 0 if "__none__" in usos else len(usos)
    breadth_norm = scoring.breadth_norm(usos_marcados, TOTAL_USO_OPCOES)

    acertos = sum(
        1 for item_id, correta in OBJECTIVE_ANSWER_KEY.items()
        if answers.get(item_id) == correta
    )
    objective_norm = scoring.objective_norm(acertos, total=len(OBJECTIVE_ANSWER_KEY))

    literacy = scoring.compute_literacy(self_norm, breadth_norm, objective_norm)

    b_items = [answers[f"b{i}"] for i in range(1, 9)]
    opportunity = scoring.compute_opportunity(b_items)
    automatability = scoring.automatability_label(answers["b9b"])

    return {
        "m1": m1, "m2": m2, "m3": m3,
        "readiness": readiness,
        "readiness_band": scoring.readiness_band(readiness),
        "literacy": literacy,
        "literacy_band": scoring.literacy_band(literacy),
        "objective_correct": acertos,
        "opportunity": opportunity,
        "automatability_label": automatability,
    }


def compute_form2(answers: dict) -> dict:
    technical_idx = scoring.compute_technical(
        q42=answers["q42"], q43=answers["q43"], q44=answers["q44"],
        q45=answers["q45"], q47=answers["q47"], q48_reverso=answers["q48"],
        q41_escada=answers["q41"], q46_escada=answers["q46"],
    )
    return {
        "technical_idx": technical_idx,
        "technical_band": scoring.technical_band(technical_idx),
    }
