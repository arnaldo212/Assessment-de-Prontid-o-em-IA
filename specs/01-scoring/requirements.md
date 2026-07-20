# Módulo 01 — Cálculo de Índices (Scoring)

Portado 1:1 da lógica validada nos protótipos `Formulario_1_Geral.html` e
`Formulario_2_Tecnico.html`. As fórmulas abaixo são a fonte da verdade; o
código em `backend/app/scoring.py` deve implementá-las exatamente como
descrito aqui, e `backend/tests/unit/test_scoring.py` deve cobrir cada regra.

## 1. Normalização

```
norm(raw, min, max) = round((raw - min) / (max - min) * 100)
```

## 2. Módulos 1–3 (Organização / Times / Pessoas) — Formulário 1

Cada módulo tem 5 itens pontuados: `q1, q2, q3` (diretos, 1–5), `q4`
(reverso, 1–5), `q5` (escada, 1–4).

```
raw_modulo   = q1 + q2 + q3 + (6 - q4) + q5      # min 5, max 24
idx_modulo   = norm(raw_modulo, 5, 24)
```

## 3. Prontidão percebida

```
raw_readiness = raw_m1 + raw_m2 + raw_m3          # min 15, max 72
readiness     = norm(raw_readiness, 15, 72)
```

Faixas (`readinessBand`):
- `readiness <= 52` → "Fundamentos"
- `52 < readiness <= 63` → "Zona incerta"
- `readiness > 63` → "Pronto"

## 4. Literacia (peso 50/15/35)

- **Autopercepção (self)**: `a1(1-5) + a2(1-4) + a4..a8(1-5 cada) + (6 - a9)`,
  min 8, max 39 → `self_norm = (self - 8) / (39 - 8) * 100`
- **Amplitude de uso (breadth)**: nº de opções marcadas em `a3`
  (`__none__` conta como 0) / 8 opções totais * 100
- **Acertos objetivos (objective)**: nº de acertos em `c1..c6` / 6 * 100

```
literacy = round(0.50 * self_norm + 0.15 * breadth_norm + 0.35 * objective_norm)
```

Faixas: `>=60` Avançado · `40–59` Intermediário · `<40` Iniciante.

## 5. Oportunidade no trabalho

```
opp_mean    = média(b1..b8)                        # cada item 1–5
opportunity = round((opp_mean - 1) / 4 * 100)
```

Automatabilidade (`b9b`, escada 1–4): `<=2` baixo · `3` médio · `4` alto.
(`b9a` é aberta, não pontuada.)

## 6. Índice Técnico (Módulo 4) — Formulário 2

Itens: `q42, q43, q44, q45, q47` (diretos 1–5), `q48` (reverso 1–5),
`q41, q46` (escadas 1–4).

```
raw_tech = q42+q43+q44+q45+q47 + (6 - q48) + q41 + q46   # min 8, max 38
tech_idx = round((raw_tech - 8) / 30 * 100)
```

Faixas: `<=40` "Base técnica frágil" · `41–65` "Em construção" ·
`>65` "Base técnica sólida".

## 7. Quadrante literacia × oportunidade

**Regra de negócio nova em relação ao protótipo**: no HTML estático, o
corte de "alta/baixa" era fixo em 60/40 sobre o valor absoluto (0–100),
porque uma resposta isolada não tem distribuição de comparação. Na
aplicação, com base de respondentes, o corte passa a ser por **percentil**:

```
nível(x, distribuição) =
    "alta"    se percentil_rank(x, distribuição) >= 60
    "baixa"   se percentil_rank(x, distribuição) <= 40
    "cinzenta" caso contrário
```

A distribuição de referência é o conjunto de respostas já registradas
(escopo: mesma empresa; ver spec 03 para granularidade por área). Com
menos de N respondentes (definir N mínimo, sugestão: 5), a aplicação
deve cair de volta nos cortes fixos do protótipo (60/40 absolutos) e
sinalizar que o quadrante é "provisório — poucos respondentes".

Combinação de níveis → rótulo do quadrante (igual ao protótipo):

| Literacia | Oportunidade | Badge |
|---|---|---|
| alta | alta | Acelerar já |
| alta | baixa | Multiplicador |
| baixa | alta | Prioridade de treinamento |
| baixa | baixa | Menor prioridade agora |
| qualquer "cinzenta" | — | Indefinido — revisar |

## 8. Regras gerais

- Todo item de escala (`likert`, `ladder`, `objective`) é obrigatório para
  o cálculo; itens `open` e `single_unscored` nunca entram na pontuação.
- O cálculo é determinístico e não deve depender de estado além dos
  valores de resposta — por isso vive em funções puras, sem I/O.
