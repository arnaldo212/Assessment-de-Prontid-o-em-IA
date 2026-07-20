# Módulo 02 — Autenticação e Perfis de Acesso

## Perfis

- **collaborator** (colaborador comum): responde apenas o Formulário 1
  (Geral).
- **manager** (liderança/tech: gestores, diretores, sócios, responsáveis
  por tecnologia): responde o Formulário 1 **e** o Formulário 2 (Técnico).
- **admin**: além de responder, acessa o dashboard agregado da empresa.

## Regras

1. Toda resposta pertence a um usuário autenticado, uma empresa
   (`company_id`) e uma área/departamento opcional (`area`).
2. Um usuário só pode responder cada formulário **uma vez por versão do
   instrumento** (`instrument_version_id`). Reenvio deve ser bloqueado
   pela API com erro 409, não escondido silenciosamente na UI.
3. O Formulário 2 só é exibido/aceito para usuários com perfil `manager`
   ou `admin`. Tentativa de um `collaborator` enviar respostas do
   Formulário 2 deve retornar 403.
4. `admin` pode ver o dashboard agregado (spec 03); `collaborator` e
   `manager` só veem o próprio resultado individual.
5. Login via email + senha (hash com bcrypt), token JWT de curta duração
   + refresh token. Fora de escopo nesta fase: SSO/OAuth (anotar como
   extensão futura).
6. Cadastro de usuário é feito por convite/admin (não há self-signup
   público) — evita respostas de fora da empresa contaminando a
   distribuição usada no cálculo por percentil.
7. **Cadastro de pessoas (`POST /people`, só `admin`)**: cria uma nova
   pessoa (nome, email, senha temporária, perfil e área opcional) já
   vinculada à empresa do admin que está cadastrando — nunca é possível
   cadastrar alguém em outra empresa. Se a área informada não existir
   ainda, é criada automaticamente. Email duplicado retorna 409.
8. **Listagem de pessoas (`GET /people`, só `admin`)**: retorna somente
   pessoas da própria empresa do admin.

## Fora de escopo (v1)

- Múltiplas empresas no mesmo banco com isolamento total (multi-tenant
  "hard") — nesta fase, `company_id` é só uma coluna de filtro, não um
  schema separado. Documentar como possível evolução.
