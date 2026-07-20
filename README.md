# Assessment de Prontidão em IA

Aplicação multiusuário para diagnosticar como uma empresa está lidando
com Inteligência Artificial hoje — cada funcionário responde um
questionário e a empresa recebe uma pontuação de maturidade (0 a 100),
individual e agregada.

O projeto nasceu de dois protótipos HTML estáticos (formulário +
cálculo de pontuação no navegador, sem banco de dados nem multiusuário)
e evoluiu para uma aplicação real: login, banco de dados, isolamento
por empresa e um dashboard agregado — tudo dockerizado, pronto para
rodar em qualquer nuvem.

Desenvolvida com **Spec Driven Development**: toda regra de negócio
está documentada em [`specs/`](./specs) (requisitos em `.md` + cenários
de aceitação em Gherkin `.feature`) **antes** de existir em código, e
cada cenário tem um teste automatizado correspondente. Hoje são 30
testes passando, cobrindo desde as fórmulas de pontuação até o
isolamento de dados entre empresas diferentes.

---

## Sumário

- [O que a aplicação faz](#o-que-a-aplicação-faz)
- [Como funciona o cadastro de pessoas](#como-funciona-o-cadastro-de-pessoas)
- [Perfis de acesso](#perfis-de-acesso)
- [Usuários já cadastrados de exemplo (seed)](#usuários-já-cadastrados-de-exemplo-seed)
- [Como rodar localmente](#como-rodar-localmente)
- [Como rodar em produção / nuvem](#como-rodar-em-produção--nuvem)
- [Arquitetura e stack](#arquitetura-e-stack)
- [Como funciona a pontuação](#como-funciona-a-pontuação)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Testes](#testes)
- [Decisões de design importantes](#decisões-de-design-importantes)
- [O que falta / próximos passos](#o-que-falta--próximos-passos)

---

## O que a aplicação faz

1. Uma pessoa faz login e responde o **Formulário 1** (geral — todo
   mundo responde): perguntas sobre como a empresa lida com IA em
   estratégia, times e cultura, mais um bloco individual sobre
   literacia e oportunidade de uso de IA no próprio trabalho.
2. Gestores e responsáveis por tecnologia também respondem o
   **Formulário 2** (técnico): dados, governança, ROI.
3. Ao terminar, a pessoa vê o próprio resultado na hora: prontidão,
   literacia, oportunidade (cada um 0-100) e um quadrante
   (ex: "Prioridade de treinamento", "Acelerar já").
4. Um admin acessa o **Dashboard** e vê o resultado agregado de todos
   os respondentes da própria empresa: um número único de
   **maturidade consolidada (0-100)**, quebra por área, e distribuição
   de quadrante.

Cada empresa só enxerga os próprios dados — nunca há mistura entre
empresas diferentes, mesmo que compartilhem o mesmo banco.

## Como funciona o cadastro de pessoas

**Não existe cadastro público.** Ninguém consegue criar a própria
conta sozinho digitando um formulário de "criar conta" — isso é
proposital, para impedir que qualquer pessoa de fora responda o
questionário de uma empresa que não é a dela.

O fluxo é:

1. Um usuário com perfil **admin** entra na tela **Pessoas**
   (`/pessoas`).
2. Preenche nome, email, uma senha temporária, o perfil
   (colaborador / gestor / admin) e, opcionalmente, a área/departamento
   da pessoa.
3. A pessoa cadastrada já nasce vinculada à **mesma empresa** do admin
   que a cadastrou — não tem como cadastrar alguém em outra empresa.
4. Essa pessoa já pode fazer login imediatamente com o email e a senha
   que o admin definiu.

Se a área informada ainda não existir, ela é criada automaticamente —
não precisa cadastrar áreas antes.

> **Limitação conhecida:** hoje isso é cadastro manual, um por um. Para
> empresas grandes (dezenas ou centenas de funcionários), esse fluxo
> não escala bem. Um convite por link/código (autocadastro vinculado
> automaticamente à empresa certa) está mapeado como próximo passo —
> ver a seção final.

## Perfis de acesso

| Perfil | Pode responder Formulário 1 | Pode responder Formulário 2 | Vê o Dashboard agregado | Cadastra pessoas |
|---|---|---|---|---|
| **collaborator** (colaborador comum) | ✅ | ❌ | ❌ | ❌ |
| **manager** (gestor / liderança / tech) | ✅ | ✅ | ❌ | ❌ |
| **admin** | ✅ | ✅ | ✅ | ✅ |

Essas regras são aplicadas no backend (não só escondidas na
interface): se um colaborador tentar enviar o Formulário 2 via API
diretamente, recebe erro 403. Mesma coisa para acessar o dashboard ou
cadastrar pessoas sem ser admin.

## Usuários já cadastrados de exemplo (seed)

Depois de subir a aplicação, rodando o comando de seed (explicado
abaixo), a aplicação já vem com **7 pessoas de exemplo**, todas da
mesma empresa ("Empresa Demo"), espalhadas em 5 áreas diferentes —
suficiente para já testar o dashboard e o mapa por área sem precisar
cadastrar ninguém na mão.

Senha de todos: **`trocar123`**

| Nome | Email | Perfil | Área |
|---|---|---|---|
| Ana Colaboradora | `colaborador@demo.com` | collaborator | Tecnologia |
| Bruno Gestor | `gestor@demo.com` | manager | Tecnologia |
| Carla Admin | `admin@demo.com` | admin | Tecnologia |
| Diego Marketing | `colaborador2@demo.com` | collaborator | Marketing |
| Elisa Vendas | `colaborador3@demo.com` | collaborator | Vendas |
| Fabio Financeiro | `gestor2@demo.com` | manager | Financeiro |
| Gabriela Operações | `colaborador4@demo.com` | collaborator | Operações |

> Troque ou remova essas contas antes de usar a aplicação com dados
> reais — elas existem só para facilitar teste e demonstração.

## Como rodar localmente

Pré-requisito: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
instalado e rodando.

```bash
git clone <url-do-seu-repositório>
cd assessment-app

cp .env.example .env
# abra o .env e edite pelo menos JWT_SECRET (qualquer string longa e
# aleatória serve para desenvolvimento local)

docker compose up --build
```

Isso sobe quatro serviços:
- **db** — Postgres, com os dados guardados num volume Docker
  (não fica salvo dentro da pasta do projeto)
- **migrate** — roda as migrations do banco e encerra
- **backend** — API FastAPI em `http://localhost:8000`
  (documentação interativa em `http://localhost:8000/docs`)
- **frontend** — aplicação React em `http://localhost:5173`

Depois que os containers estiverem de pé, popule os dados de exemplo
(a tabela de usuários da seção anterior):

```bash
docker compose exec backend python -m app.seed
```

Abra `http://localhost:5173` no navegador e faça login com qualquer um
dos emails de exemplo.

Para reiniciar do zero (apagando também os dados do banco):
```bash
docker compose down -v
```

## Como rodar em produção / nuvem

```bash
cp .env.example .env
# preencha DB_USER, DB_PASSWORD, DB_NAME com valores reais,
# JWT_SECRET com uma string longa e aleatória (ex: openssl rand -hex 32),
# e principalmente:
#   PUBLIC_API_URL=https://<domínio onde o backend vai responder>
#   CORS_ORIGINS=https://<domínio onde o frontend vai responder>

docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

Pontos de atenção específicos de produção:

- **`PUBLIC_API_URL` é obrigatória**: o React grava a URL da API
  dentro do arquivo `.js` **no momento do build**, não em tempo de
  execução. Se o domínio do backend mudar depois, é preciso
  rebuildar o frontend (`docker compose build frontend`), não só
  reiniciar o container.
- **HTTPS não vem pronto**: nem o Nginx do frontend nem o Uvicorn do
  backend fazem TLS. Isso normalmente é resolvido pelo load balancer
  do provedor de nuvem (ALB, Cloud Load Balancing, etc.) ou por um
  reverse proxy com Let's Encrypt na frente dos dois serviços. Sem
  HTTPS, tokens de login trafegam sem criptografia — não é recomendado
  para dados reais sem isso.
- **Banco gerenciado**: por padrão sobe um Postgres em container com
  volume local — ótimo para testar rápido numa única VM, mas sem
  backup automático. Para produção real, considere um Postgres
  gerenciado (RDS, Cloud SQL etc.) e aponte `DB_HOST` para ele.

## Arquitetura e stack

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI    │─────▶│  PostgreSQL │
│  (Vite)     │      │              │      │             │
└─────────────┘      └──────────────┘      └─────────────┘
                             │
                      ┌──────┴──────┐
                      │   Alembic   │ (migrations)
                      └─────────────┘
```

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL,
  autenticação JWT (access + refresh token), senhas com `bcrypt`
- **Frontend**: React 18, Vite, React Router — sem framework de CSS,
  estilos simples e diretos
- **Infra**: Docker multi-stage (`dev` com hot reload, `prod` com
  build otimizado + Nginx servindo o frontend), `docker-compose`
  separado por ambiente

## Como funciona a pontuação

Resumo — a fórmula completa e testada está em
[`specs/01-scoring/requirements.md`](./specs/01-scoring/requirements.md):

- **Prontidão** (0-100): média de 3 módulos (Organização, Times,
  Pessoas), cada um com perguntas de escala 1-5 (algumas invertidas) e
  uma pergunta de "escada" de maturidade.
- **Literacia** (0-100): combina autopercepção (peso 50%), amplitude
  de uso de ferramentas de IA (peso 15%) e acertos num teste objetivo
  de conhecimento (peso 35%).
- **Oportunidade** (0-100): o quanto o trabalho da pessoa tem tarefas
  automatizáveis por IA.
- **Índice Técnico** (0-100, só quem responde o Formulário 2): dados,
  governança, ROI.
- **Quadrante individual**: cruza literacia × oportunidade da pessoa
  (ex: alta literacia + baixa oportunidade = "Multiplicador" — bom
  candidato a mentor interno). Usa percentil sobre a base de
  respondentes da empresa quando há dados suficientes (≥5 pessoas);
  com poucos dados, cai para um corte fixo e sinaliza o resultado como
  provisório.
- **Maturidade consolidada da empresa** (0-100, no dashboard): média
  simples entre as médias da empresa de prontidão, literacia e
  oportunidade. O índice técnico fica de fora dessa conta porque tem
  uma base amostral menor e diferente (só gestores respondem).

## Estrutura de pastas

```
specs/                        # requisitos + testes de aceitação (Gherkin)
  01-scoring/                   # fórmulas dos índices
  02-auth-perfis/                # perfis, controle de acesso, cadastro
  03-agregacao-dashboard/         # dashboard, agregação, maturidade

backend/
  app/
    scoring.py                   # cálculo dos índices (funções puras)
    scoring_service.py            # traduz respostas brutas -> scoring.py
    aggregation.py                # estatísticas do dashboard
    models.py                     # tabelas do banco (SQLAlchemy)
    routers/
      auth.py                      # login, refresh, /me
      forms.py                     # submissão dos dois formulários
      people.py                    # cadastro e listagem de pessoas
      dashboard.py                 # agregado por empresa
  tests/
    unit/                        # scoring.py e aggregation.py isolados
    integration/                   # API real via TestClient (SQLite em memória)
  alembic/                      # migrations do banco

frontend/
  src/
    formSchemas/                 # perguntas dos dois formulários
    pages/                       # Login, Formulário 1/2, Dashboard, Pessoas
    components/                  # NavBar, QuestionField
```

## Testes

```bash
cd backend
pip install -e ".[dev]"   # ou: poetry install
pytest tests/ -v
```

30 testes cobrindo cada cenário documentado em `specs/`, incluindo:
- Cada fórmula de pontuação (com os valores exatos calculados na mão)
- Controle de acesso por perfil (403/409 nos lugares certos)
- Isolamento de dados entre empresas diferentes
- Cadastro de pessoas escopado por empresa

## Decisões de design importantes

- **Isolamento por empresa em toda query de agregação** — nunca dados
  de duas empresas aparecem misturados, mesmo estando no mesmo banco.
- **Quadrante por percentil, não corte fixo** — com base de
  respondentes suficiente, o corte "alta/baixa" de literacia e
  oportunidade é calculado sobre a distribuição real da empresa, não
  um valor absoluto fixo.
- **Versionamento do instrumento** — pesos, cortes e âncoras vivem em
  uma tabela própria (`InstrumentVersion`). Recalibrar não sobrescreve
  dados antigos: cria uma nova versão, e respostas já enviadas
  continuam referenciando a versão vigente no momento do envio.
- **Nenhuma resposta aberta (texto livre) aparece em agregações
  automáticas** — só no resultado individual do próprio respondente.

## O que falta / próximos passos

- **Convite por link/código por empresa** — para não depender de
  cadastro manual pessoa por pessoa em empresas grandes.
- **Rate limiting no login** — hoje não há proteção contra tentativas
  repetidas de senha.
- **Testes end-to-end de navegador** (Playwright) — hoje a cobertura é
  toda no nível de API; a interface foi validada manualmente.
- **Exportação do dashboard** (CSV/PDF).
- **`poetry.lock` versionado** — hoje o build resolve as versões do
  `pyproject.toml` no momento do build, o que funciona mas não é
  100% reprodutível.
