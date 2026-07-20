Feature: Cálculo de índices de prontidão em IA

  Scenario: Índice de módulo com item reverso e escada
    Given respostas do módulo M1 com q1=4, q2=3, q3=5, q4=2, q5=3
    When calculo o índice do módulo M1
    Then o raw do módulo deve ser 19
    And o índice do módulo deve ser 74

  Scenario: Prontidão percebida agrega os três módulos
    Given raw do módulo M1 igual a 17
    And raw do módulo M2 igual a 15
    And raw do módulo M3 igual a 20
    When calculo a prontidão percebida
    Then a prontidão deve ser 65

  Scenario: Faixa "Zona incerta" da prontidão
    Given prontidão igual a 58
    When busco a faixa de prontidão
    Then a faixa deve ser "Zona incerta"

  Scenario: Literacia combina autopercepção, amplitude e acertos com pesos 50/15/35
    Given autopercepção normalizada de 80
    And amplitude de uso normalizada de 50
    And acertos objetivos normalizados de 100
    When calculo o índice de literacia
    Then o índice de literacia deve ser 82

  Scenario: Oportunidade é a média normalizada dos itens b1 a b8
    Given respostas do bloco B iguais a 3, 4, 3, 5, 2, 4, 3, 4
    When calculo a oportunidade
    Then a oportunidade deve ser 62

  Scenario: Índice técnico do módulo 4
    Given respostas técnicas q42=4, q43=5, q44=3, q45=4, q47=3, q48=2, q41=3, q46=2
    When calculo o índice técnico
    Then o índice técnico deve ser 67

  Scenario: Quadrante com poucos respondentes usa cortes fixos e sinaliza provisório
    Given uma base com 3 respondentes
    And literacia de 70 e oportunidade de 75 para o respondente atual
    When calculo o quadrante
    Then o quadrante deve ser "Acelerar já"
    And o quadrante deve estar marcado como provisório

  Scenario: Quadrante com base suficiente usa percentil
    Given uma base com 20 respondentes onde a literacia do respondente atual está no percentil 30
    And a oportunidade do respondente atual está no percentil 65
    When calculo o quadrante
    Then o quadrante deve ser "Prioridade de treinamento"
    And o quadrante não deve estar marcado como provisório

  Scenario: Zona cinzenta gera quadrante indefinido
    Given uma base com 20 respondentes onde a literacia do respondente atual está no percentil 50
    And a oportunidade do respondente atual está no percentil 80
    When calculo o quadrante
    Then o quadrante deve ser "Indefinido — revisar"
