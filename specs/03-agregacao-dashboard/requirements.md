# Módulo 03 — Agregação e Dashboard por Área

## Objetivo

Dar ao `admin` uma visão agregada que os HTMLs estáticos não conseguem
oferecer sozinhos: distribuição de respostas, comparação entre áreas, e
o quadrante calculado por percentil (ver spec 01, seção 7).

## Requisitos

0. **Isolamento por empresa**: toda agregação (distribuições gerais, mapa
   por área, distribuição de quadrante, índice técnico) é escopada pela
   empresa do `admin` que faz a requisição — nunca mistura dados de
   empresas diferentes, mesmo que estejam no mesmo banco (spec 02,
   "Fora de escopo: multi-tenant *hard*" — o isolamento aqui é feito por
   filtro de `company_id` em toda query de agregação, não por schema
   separado).
1. **Distribuição geral**: média, mediana e desvio-padrão de `readiness`,
   `literacy`, `opportunity` e `technical_idx` para toda a empresa.
1.1. **Maturidade consolidada da empresa**: um único número (0-100) que
   resume o resultado da empresa inteira, para uso direto em relatório.
   Calculado como a média simples (peso igual) entre as médias da
   empresa de `readiness`, `literacy` e `opportunity`:

   ```
   maturidade_empresa = round(
       (media_empresa(readiness) + media_empresa(literacy) + media_empresa(opportunity)) / 3
   )
   ```

   O `technical_idx` fica **fora** dessa conta — continua reportado à
   parte (requisito 4), porque sua base amostral é menor e diferente
   (só gestores/tech respondem), o que enviesaria a média se fosse
   somado com peso igual aos outros três.
2. **Mapa por área**: as mesmas métricas quebradas por `area`
   (departamento). Áreas com menos de 3 respondentes devem ser omitidas
   do detalhamento individual e agrupadas em "outras" — evita reidentificar
   respondente único.
3. **Distribuição do quadrante**: contagem de respondentes em cada um dos
   5 rótulos de quadrante (4 quadrantes + indefinido), geral e por área.
4. **Índice técnico separado**: reportado à parte dos índices do
   Formulário 1, com nota de que a base amostral tende a ser menor
   (só gestores/tech respondem).
5. **Recalibração**: endpoint administrativo para registrar uma nova
   `instrument_version` com pesos/cortes ajustados, mantendo o histórico
   das versões anteriores (nunca sobrescrever dados já calculados — toda
   resposta referencia a versão do instrumento vigente no momento do
   envio).
6. Nenhuma resposta aberta (`open`) deve ser exposta em agregações
   automáticas — apenas em uma visão individual, quando aplicável ao
   próprio respondente ou explicitamente liberada por ele.

## Fora de escopo (v1)

- Exportação para BI externo (CSV/PDF) — anotar como extensão futura.
- Comparação entre empresas (benchmarking cross-tenant).
