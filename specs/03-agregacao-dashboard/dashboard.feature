Feature: Agregação e dashboard por área

  Scenario: Maturidade consolidada é a média simples de prontidão, literacia e oportunidade
    Given a empresa tem média de prontidão 60, média de literacia 70 e média de oportunidade 80
    When calculo a maturidade consolidada da empresa
    Then a maturidade deve ser 70

  Scenario: Índice técnico não entra na maturidade consolidada
    Given a empresa tem média de prontidão 60, média de literacia 70 e média de oportunidade 80
    And média de índice técnico 20
    When calculo a maturidade consolidada da empresa
    Then a maturidade deve ser 70

  Scenario: Dashboard não mistura dados de empresas diferentes
    Given a Empresa A tem 5 respondentes do Formulário 1
    And a Empresa B tem 3 respondentes do Formulário 1
    When o admin da Empresa A solicita o dashboard agregado
    Then o total de respondentes deve ser 5
    And nenhum dado da Empresa B deve aparecer no resultado

  Scenario: Área com poucos respondentes é agrupada em "outras"
    Given uma área "Financeiro" com 2 respondentes
    When calculo o mapa por área
    Then "Financeiro" não deve aparecer detalhada
    And "Financeiro" deve estar somada em "outras"

  Scenario: Distribuição do quadrante é contada por rótulo
    Given respondentes com quadrantes: "Acelerar já", "Acelerar já", "Multiplicador", "Indefinido — revisar"
    When calculo a distribuição do quadrante
    Then a contagem de "Acelerar já" deve ser 2
    And a contagem de "Multiplicador" deve ser 1
    And a contagem de "Indefinido — revisar" deve ser 1

  Scenario: Nova versão do instrumento não altera respostas já calculadas
    Given uma resposta calculada com a versão de instrumento "v1"
    When uma nova versão "v2" é registrada com pesos diferentes
    Then a resposta original deve continuar referenciando "v1"
    And o índice já calculado da resposta original não deve mudar
