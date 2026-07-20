Feature: Autenticação e controle de acesso por perfil

  Scenario: Colaborador comum não pode enviar o Formulário 2
    Given um usuário autenticado com perfil "collaborator"
    When ele envia respostas do Formulário 2
    Then a API deve responder com status 403

  Scenario: Gestor pode enviar o Formulário 1 e o Formulário 2
    Given um usuário autenticado com perfil "manager"
    When ele envia respostas do Formulário 1
    Then a API deve responder com status 201
    When ele envia respostas do Formulário 2
    Then a API deve responder com status 201

  Scenario: Reenvio do mesmo formulário na mesma versão é bloqueado
    Given um usuário autenticado com perfil "manager"
    And ele já enviou respostas do Formulário 1 na versão atual do instrumento
    When ele tenta enviar o Formulário 1 novamente na mesma versão
    Then a API deve responder com status 409

  Scenario: Apenas admin acessa o dashboard agregado
    Given um usuário autenticado com perfil "manager"
    When ele solicita o dashboard agregado da empresa
    Then a API deve responder com status 403

  Scenario: Admin cadastra uma nova pessoa na própria empresa
    Given um usuário autenticado com perfil "admin"
    When ele cadastra uma pessoa com nome, email, senha, perfil e área
    Then a API deve responder com status 201
    And a pessoa cadastrada pertence à mesma empresa do admin

  Scenario: Apenas admin cadastra pessoas
    Given um usuário autenticado com perfil "manager"
    When ele tenta cadastrar uma nova pessoa
    Then a API deve responder com status 403

  Scenario: Cadastro com email já existente é bloqueado
    Given um usuário autenticado com perfil "admin"
    And já existe uma pessoa cadastrada com o email "duplicado@teste.com"
    When ele tenta cadastrar outra pessoa com o mesmo email
    Then a API deve responder com status 409

  Scenario: Listagem de pessoas é escopada por empresa
    Given um usuário autenticado com perfil "admin"
    And existe uma pessoa cadastrada em uma empresa diferente
    When ele solicita a lista de pessoas
    Then a pessoa de outra empresa não deve aparecer na lista
