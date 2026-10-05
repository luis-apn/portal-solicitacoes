# Memorial Técnico de Desenvolvimento

**Projeto:** Portal de Solicitações Internas
**Candidato:** Luis Alves de Paiva Neto
**Processo seletivo:** Desenvolvedor(a) de Sistemas Júnior, bit Soluções (09/2026)

---

## 1. Visão geral

O Portal de Solicitações permite que colaboradores registrem demandas internas e acompanhem a evolução delas até a conclusão. A solução é composta por três partes independentes:

- **Backend**: API REST em Python/Flask, responsável pelas regras de negócio, validações, autenticação e acesso ao banco.
- **Frontend**: aplicação React (SPA) que consome a API.
- **Banco de dados**: MySQL 8, com scripts SQL de criação e carga inicial.

O objetivo foi entregar uma solução **simples, funcional e organizada**, priorizando o cumprimento dos requisitos, a separação de responsabilidades e a clareza do código, em vez de usar tecnologias ou padrões mais complexos do que o problema exige.

---

## 2. Tecnologias utilizadas e justificativa técnica

### 2.1 Python + Flask (backend)

- **Motivo da escolha:** é a linguagem e o framework com os quais tenho mais experiência (projeto Compreens.IA e ferramentas de automação).
- **Benefícios para o cenário:** Flask é um microframework: começa pequeno e permite montar exatamente as camadas necessárias, sem estrutura obrigatória excessiva. Para uma API com poucos recursos, é suficiente e fácil de entender.
- **Vantagens em relação a alternativas:** o *Django* traz admin, ORM e templates prontos, mas impõe mais estrutura do que o projeto precisa. O *FastAPI* tem validação automática e documentação OpenAPI, mas é orientado a programação assíncrona, que não traz ganho aqui. Optei pelo framework que domino melhor, para reduzir o risco no prazo.
- **Impacto:** a organização com *Application Factory* e *Blueprints* permite adicionar novos módulos (ex.: comentários, anexos) sem alterar o que existe.

### 2.2 Flask-SQLAlchemy / SQLAlchemy (ORM)

- **Motivo:** mapeia as tabelas em classes Python, evitando SQL escrito à mão espalhado pelo código.
- **Benefícios:** consultas com parâmetros (protege contra *SQL Injection*), relacionamentos (`solicitacao.category.name`) e troca de banco sem mudar o código. Isso foi usado nos testes, que rodam com SQLite em memória.
- **Alternativa:** SQL puro com PyMySQL. Seria mais trabalhoso e mais propenso a erro na montagem dos filtros dinâmicos.

### 2.3 Flask-Login (autenticação)

- **Motivo:** o requisito pede *login, controle de sessão e logout*. O Flask-Login implementa exatamente isso com sessão por cookie.
- **Benefícios:** decorator `@login_required` nas rotas, `current_user` disponível em qualquer lugar e integração com o cookie de sessão assinado do Flask.
- **Alternativa:** JWT (ex.: Flask-JWT-Extended). JWT é útil para APIs consumidas por vários clientes ou serviços, mas exige decidir onde guardar o token no navegador e como renová-lo. Para um único frontend web, a sessão por cookie é mais simples e segura (cookie `HttpOnly`, inacessível ao JavaScript).

### 2.4 Werkzeug Security (hash de senhas)

- Já vem com o Flask. `generate_password_hash` gera hash **scrypt com salt**; a senha nunca é armazenada.

### 2.5 PyMySQL + cryptography (driver MySQL)

- PyMySQL é um driver 100% Python: instala com `pip` sem compilar nada, em qualquer sistema operacional. O pacote `cryptography` é necessário para o método de autenticação padrão do MySQL 8.

### 2.6 Flask-Cors

- Libera a API apenas para a origem do frontend configurada em `CORS_ORIGINS`. No desenvolvimento, o proxy do Vite já evita CORS, mas a configuração fica pronta caso o frontend seja servido em outro domínio.

### 2.7 python-dotenv

- Carrega as variáveis do arquivo `.env`. Segredos (senha do banco, `SECRET_KEY`) ficam fora do código e fora do Git.

### 2.8 MySQL 8 (banco de dados)

- **Motivo:** banco relacional maduro, muito usado no mercado, com suporte a chaves estrangeiras, `ENUM` e transações (InnoDB).
- **Benefícios:** os dados do problema são claramente relacionais (usuário → solicitação ← categoria), então um banco SQL garante integridade com chaves estrangeiras.
- **Alternativa:** PostgreSQL seria igualmente adequado. SQLite é ótimo para testes, mas não é indicado para uso concorrente em produção.

### 2.9 React + Vite + React Router (frontend)

- **React:** é a biblioteca que utilizo no projeto PIBIC. Componentes reutilizáveis (ex.: `StatusBadge`, `Navbar`) e estado com hooks (`useState`, `useEffect`).
- **Vite:** ferramenta de build rápida e simples de configurar. O *proxy* do Vite repassa `/api` para o Flask, então frontend e API ficam na mesma origem no navegador, e o cookie de sessão funciona sem configuração extra. O *Create React App* foi descontinuado, por isso não foi usado.
- **React Router:** navegação entre páginas sem recarregar e rotas protegidas (`PrivateRoute`).
- **fetch nativo** em vez de Axios: uma função `api()` de 30 linhas cobre tudo o que o projeto precisa, sem dependência extra.
- **CSS puro** em vez de framework (Bootstrap, Tailwind): o layout é simples, e um único arquivo CSS com uma *media query* resolve a responsividade.

### 2.10 pytest (testes automatizados)

- Testa as regras de negócio pela API (login, permissões, fluxo de status, filtros, dashboard) usando o *test client* do Flask com SQLite em memória. Os testes rodam em segundos e não dependem do MySQL.

### 2.11 Docker e Docker Compose

- Um único comando (`docker compose up --build`) sobe MySQL, backend e frontend, já com o banco criado e populado. Elimina o problema de "na minha máquina funciona" e atende ao requisito de executar sem adaptações.

---

## 3. Justificativa conceitual (arquitetura)

### 3.1 Estrutura geral

Arquitetura **cliente-servidor** com frontend e backend separados e comunicação via **API REST com JSON**:

```
[React (navegador)] --HTTP/JSON--> [Flask API] --SQLAlchemy--> [MySQL]
```

### 3.2 Organização em camadas (backend)

| Camada | Pasta | Responsabilidade |
|---|---|---|
| Rotas | `app/routes/` | Recebem a requisição HTTP, chamam a validação e o service, devolvem JSON. Não têm regra de negócio |
| Validação | `app/validators.py` | Conferem os dados de entrada (obrigatoriedade, tamanho, formato) |
| Serviços | `app/services/` | Regras de negócio (quem pode editar, fluxo de status etc.). Não conhecem HTTP |
| Modelos | `app/models/` | Representação das tabelas e conversão para dicionário (`to_dict`) |
| Erros | `app/errors.py` | `AppError` e handlers globais que padronizam as respostas de erro |

Essa separação deixa cada arquivo com uma responsabilidade clara e facilita os testes e a manutenção: uma mudança de regra fica só no service, e uma mudança de URL só na rota.

### 3.3 Modelagem de dados

Três tabelas: `users`, `categories` e `requests` (detalhes no [dicionário de dados](../databases/dicionario_dados.md)).

- **Categoria como tabela** (e não texto livre): evita variações como "TI", "ti" e "T.I.", garante integridade por chave estrangeira e permite incluir novas categorias sem alterar código.
- **Status como `ENUM`**: são três valores fixos que fazem parte da regra de negócio; o banco rejeita qualquer outro valor. A contrapartida é que um novo status exige `ALTER TABLE`, o que é aceitável para este escopo.
- **Chaves estrangeiras com `ON DELETE RESTRICT`**: impedem excluir um usuário ou categoria que possua solicitações, evitando registros órfãos.
- **Índices** em `status` e `created_at`, colunas usadas nos filtros e no dashboard.
- **Campos automáticos**: `created_at`, `status = ABERTO` e `requester_id` (usuário logado) são definidos pelo backend, nunca enviados pelo cliente.
- **Charset `utf8mb4`**: suporte completo a acentos e caracteres especiais.

### 3.4 Padrões de projeto utilizados

- **Application Factory** (`create_app`): a aplicação é criada por uma função, o que permite usar configurações diferentes (MySQL em execução normal, SQLite nos testes).
- **Blueprints**: cada grupo de endpoints (auth, requests, categories, dashboard) fica em seu próprio módulo.
- **Service Layer**: regras de negócio isoladas das rotas.
- **Tratamento centralizado de erros**: os services lançam `AppError(mensagem, status)` e um único handler converte em JSON.
- **Context API (React)**: o usuário logado fica em um contexto global (`AuthContext`), acessível por qualquer componente.

### 3.5 Estratégia de autenticação

1. O usuário envia usuário e senha para `POST /api/auth/login`.
2. O backend busca o usuário e confere a senha com `check_password_hash` (as senhas ficam salvas apenas como hash scrypt).
3. Se estiver correto, o Flask-Login grava o id do usuário na **sessão**, um cookie assinado com a `SECRET_KEY`. Sem a chave não é possível forjar um cookie de outro usuário.
4. O cookie é `HttpOnly` (o JavaScript não consegue lê-lo) e `SameSite=Lax` (não é enviado em requisições de escrita vindas de outros sites).
5. Todas as rotas protegidas usam `@login_required`; sem sessão, a API responde `401`.
6. Ao abrir o site, o frontend chama `GET /api/auth/me` para saber se já existe sessão. O componente `PrivateRoute` redireciona para `/login` quando não há usuário.
7. A mensagem de erro do login é a mesma para usuário inexistente e senha errada, para não revelar quais usuários existem.

**Autorização (perfis):**

- **SOLICITANTE** cria solicitações e edita/exclui **as próprias**, somente enquanto estão *Abertas*.
- **ATENDENTE** pode, além disso, alterar o status de qualquer solicitação.

As regras são validadas **no backend**. O frontend apenas esconde os botões que o usuário não pode usar, mas isso é só uma questão de usabilidade, não de segurança.

### 3.6 Comunicação entre frontend e backend

- API REST com JSON e verbos HTTP coerentes: `GET` (consultar), `POST` (criar), `PUT` (editar), `PATCH` (alterar só o status), `DELETE` (excluir).
- Códigos HTTP semânticos: `200`, `201` (criado), `400` (dados inválidos), `401` (não logado), `403` (sem permissão), `404` (não encontrado), `409` (ação não permitida no status atual).
- Formato único de erro: `{"error": "mensagem", "details": {"campo": "mensagem"}}`. O frontend mostra `error` em destaque e `details` abaixo de cada campo do formulário.
- No frontend, toda chamada passa pela função `api()` (`src/api.js`), que envia o cookie, converte JSON e trata erros num lugar só.
- Em desenvolvimento, o proxy do Vite repassa `/api/*` para o Flask, então o navegador enxerga uma única origem (`localhost:5173`).

### 3.7 Organização do código-fonte

- Nomes de código em inglês (padrão de mercado) e textos da interface em português.
- Backend: `snake_case` para funções e variáveis, `PascalCase` para classes.
- Frontend: componentes em `PascalCase` (um por arquivo), separados em `pages/` (telas) e `components/` (partes reutilizáveis).
- Constantes para status e perfis (`STATUS_ABERTO`, `ROLE_ATENDENTE`), evitando textos repetidos pelo código.

---

## 4. Regras de negócio e interpretação dos requisitos

| Requisito | Implementação |
|---|---|
| Campos automáticos (data, solicitante, status) | Definidos no backend; o cliente não consegue informá-los |
| Editar/excluir apenas solicitação aberta | Backend retorna `409` se o status não for ABERTO |
| Alterar status | Fluxo `ABERTO → EM_ATENDIMENTO → CONCLUIDO`, sem pular nem voltar etapas |
| Filtro por período | `date_from` e `date_to` inclusivos (o dia final é considerado inteiro) |
| Filtro por texto | Busca parcial no título, sem diferenciar maiúsculas/minúsculas |

**Pontos em que o enunciado não é explícito e a decisão tomada:**

1. **Quem pode alterar o status?** O enunciado não define. Foi criado o perfil **ATENDENTE**, pois não faria sentido o próprio solicitante marcar sua demanda como concluída.
2. **Quem pode editar/excluir?** Apenas o **próprio solicitante**, para que um colaborador não altere a demanda de outro.
3. **Quem vê quais solicitações?** Todos os usuários logados veem todas as solicitações, já que a listagem pedida possui a coluna "Solicitante". Em um cenário real, isso poderia ser restrito (ver Análise Crítica).
4. **Cadastro de usuários** não foi pedido; os usuários de demonstração são criados pelo `seed.sql`.

---

## 5. Testes

- **Automatizados (pytest):** 15 testes cobrindo login (sucesso, senha errada, campos vazios), proteção das rotas, logout, criação e validações, edição, exclusão, permissão do dono, bloqueio fora do status Aberto, fluxo de status, filtros, dashboard e categorias.
- **Manuais:** fluxo completo no navegador com os dois perfis (prints em `docs/evidencias/`).

---

## 6. Análise crítica

### 6.1 Limitações da solução

- **Sem paginação** na listagem: com milhares de registros a tela ficaria lenta.
- **Sem cadastro/gerenciamento de usuários** pela interface (apenas via seed).
- **Sem histórico de alterações de status** (quem alterou e quando); só é guardado o status atual e o `updated_at`.
- **Estrutura do banco duplicada** entre `schema.sql` e os models do SQLAlchemy: uma alteração precisa ser feita nos dois lugares.
- **Sem limite de tentativas de login** (proteção contra força bruta).
- **Datas armazenadas no horário local do servidor**, sem informação de fuso.
- O ambiente Docker roda o frontend em modo de desenvolvimento (servidor do Vite).

### 6.2 Melhorias futuras

- Paginação e ordenação por coluna na listagem.
- Tabela de histórico (`request_history`) registrando cada mudança de status, com usuário e data.
- Campo de responsável (atendente) e comentários na solicitação.
- Cadastro de usuários e perfil de administrador.
- Notificações por e-mail ao mudar o status.
- Testes de frontend (Vitest + React Testing Library) e testes de ponta a ponta.

### 6.3 Requisitos que poderiam ser aperfeiçoados

- Definir explicitamente os perfis de usuário e as permissões de cada um (quem altera status, quem vê o quê).
- Definir se o solicitante pode cancelar uma solicitação já em atendimento.
- Definir se a categoria é fixa ou cadastrável pelo usuário.
- Incluir prioridade e prazo (SLA) nas solicitações.

### 6.4 O que seria diferente em um ambiente corporativo de produção

- **Migrations** (Alembic/Flask-Migrate) em vez de script SQL manual, versionando cada alteração do banco.
- **Servidor de produção** (Gunicorn) para o Flask e build estático do React servido por Nginx, com **HTTPS** e `SESSION_COOKIE_SECURE=1`.
- **Proteção CSRF** com token e **rate limiting** no login.
- **Segredos** em um cofre (ex.: AWS Secrets Manager) em vez de arquivo `.env`.
- **Logs estruturados e monitoramento** de erros.
- **CI/CD** (ex.: GitHub Actions) rodando os testes a cada push e fazendo o deploy automaticamente.
- **Usuário do banco com permissões mínimas**, em vez do usuário `root`.
- Integração com o login corporativo (LDAP/Active Directory ou SSO).
