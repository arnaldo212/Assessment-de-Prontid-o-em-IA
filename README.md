# Assessment de Prontidão em IA

Aplicação multiusuário para diagnosticar como uma empresa está lidando
com IA hoje. Cada funcionário responde um questionário e a empresa
recebe uma pontuação de maturidade (0-100), individual e agregada.

Desenvolvida com **Spec Driven Development**: toda regra de negócio
está documentada em [`specs/`](./specs) (requisitos + cenários Gherkin)
antes de existir em código, cada uma com teste automatizado. 

## O que a aplicação faz

1. A pessoa faz login e responde o **Formulário 1** (todo mundo):
   estratégia/times/cultura de IA na empresa + um bloco individual de
   literacia e oportunidade de uso no próprio trabalho.
2. Gestores e responsáveis por tecnologia também respondem o
   **Formulário 2** (técnico): dados, governança, ROI.
3. Ao terminar, a pessoa vê na hora o próprio resultado: prontidão,
   literacia, oportunidade (0-100 cada) e um quadrante.
4. Um admin vê o **Dashboard**: maturidade consolidada da empresa
   (0-100), quebra por área, distribuição de quadrante — só com dados
   da própria empresa, nunca misturado com outras.

## Cadastro de pessoas

**Não existe cadastro público.** Só um admin cria contas novas, pela
tela **Pessoas** (`/pessoas`): nome, email, senha temporária, perfil e
área opcional. A pessoa cadastrada já nasce vinculada à empresa do
admin que a criou — impossível cadastrar em outra empresa.

> **Limitação conhecida**: é cadastro manual, um por um — não escala
> bem para empresas grandes. Convite por link/código é o próximo passo
> natural.

## Perfis de acesso

| Perfil | Formulário 1 | Formulário 2 | Dashboard | Cadastra pessoas |
|---|---|---|---|---|
| **collaborator** | ✅ | ❌ | ❌ | ❌ |
| **manager** | ✅ | ✅ | ❌ | ❌ |
| **admin** | ✅ | ✅ | ✅ | ✅ |

Regras aplicadas no backend (403 se tentar via API sem permissão), não
só escondidas na interface.

## Usuários de exemplo (seed)

Depois de rodar o seed (comando abaixo), já existem 7 pessoas na
"Empresa Demo", em 5 áreas — senha de todas: **`trocar123`**

| Email | Perfil | Área |
|---|---|---|
| `colaborador@demo.com` | collaborator | Tecnologia |
| `gestor@demo.com` | manager | Tecnologia |
| `admin@demo.com` | admin | Tecnologia |
| `colaborador2@demo.com` | collaborator | Marketing |
| `colaborador3@demo.com` | collaborator | Vendas |
| `gestor2@demo.com` | manager | Financeiro |
| `colaborador4@demo.com` | collaborator | Operações |

> Troque ou remova essas contas antes de usar com dados reais.

## Como rodar localmente

Pré-requisito: [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando.

```bash
git clone <url-do-seu-repositório>
cd assessment-app
cp .env.example .env   
docker compose up --build
```

Sobe: **db** (Postgres), **migrate** (roda migrations e sai),
**backend** (`localhost:8000`, docs em `/docs`), **frontend**
(`localhost:5173`).

Popule os dados de exemplo:
```bash
docker compose exec backend python -m app.seed
```

Resetar tudo: `docker compose down -v`

## Arquitetura

React (Vite) → FastAPI → PostgreSQL, com Alembic cuidando das
migrations. Auth via JWT (access + refresh), senhas com `bcrypt`.
Docker multi-stage (`dev` com hot reload / `prod` com Nginx servindo o
frontend).

## Testes

```bash
cd backend && pip install -e ".[dev]" && pytest tests/ -v
```

30 testes cobrindo cada cenário das specs: fórmulas de pontuação,
controle de acesso por perfil, isolamento entre empresas, cadastro de
pessoas.
