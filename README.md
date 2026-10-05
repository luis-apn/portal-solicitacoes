# Portal de Solicitações Internas

Sistema web para colaboradores registrarem demandas internas (TI, RH, Compras, Financeiro e Infraestrutura) e acompanharem o andamento até a conclusão.

Projeto desenvolvido para a 2ª etapa do processo seletivo de Desenvolvedor(a) Júnior da bit Soluções.

## Funcionalidades

- **Autenticação**: login com usuário e senha, controle de sessão e logout. Só usuários logados acessam o sistema.
- **Solicitações**: criar, editar e excluir (somente o próprio solicitante e somente enquanto o status for *Aberto*).
- **Gerenciamento**: listagem com código, título, categoria, solicitante, data de abertura e status; tela de detalhes; alteração de status pelo atendente (*Aberto → Em Atendimento → Concluído*).
- **Filtros**: período, categoria, status e texto livre no título.
- **Dashboard**: total de solicitações, abertas, em atendimento e concluídas.
- **Extras**: Docker Compose, testes automatizados (pytest) e layout responsivo.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12+, Flask 3, Flask-SQLAlchemy, Flask-Login, Flask-Cors, PyMySQL |
| Frontend | React 19, React Router 7, Vite |
| Banco de dados | MySQL 8 |
| Testes | pytest |
| Containers | Docker e Docker Compose |

## Estrutura do projeto

```
portal-solicitacoes/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # create_app(): monta a aplicação
│   │   ├── config.py         # configurações (lidas do .env)
│   │   ├── extensions.py     # db, login_manager, cors
│   │   ├── errors.py         # AppError e tratamento global de erros
│   │   ├── validators.py     # validação dos dados de entrada
│   │   ├── models/           # tabelas (User, Category, ServiceRequest)
│   │   ├── services/         # regras de negócio
│   │   └── routes/           # endpoints da API (Blueprints)
│   ├── tests/                # testes automatizados (pytest)
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── frontend/
│   └── src/
│       ├── api.js            # função única de acesso à API
│       ├── AuthContext.jsx   # usuário logado (login/logout)
│       ├── components/       # Navbar, PrivateRoute, StatusBadge
│       └── pages/            # Login, Dashboard, Lista, Formulário, Detalhes
├── databases/
│   ├── schema.sql            # criação das tabelas
│   ├── seed.sql              # categorias, usuários de teste e exemplos
│   └── dicionario_dados.md
├── docs/
│   ├── MEMORIAL_TECNICO.md
│   └── evidencias/           # prints da aplicação funcionando
└── docker-compose.yml
```

## Usuários de teste

| Usuário | Senha | Perfil | O que pode fazer |
|---|---|---|---|
| `ana` | `senha123` | Solicitante | Criar, editar e excluir as próprias solicitações abertas |
| `carlos` | `senha123` | Solicitante | Idem |
| `bruno` | `senha123` | Atendente | Tudo acima + alterar o status de qualquer solicitação |

---

## Opção 1: executar com Docker (recomendado)

**Pré-requisito:** Docker Desktop instalado e aberto.

```bash
docker compose up --build
```

Aguarde as mensagens do backend e do frontend e acesse **http://localhost:5173**.

- O banco é criado e populado automaticamente (`schema.sql` + `seed.sql`) na primeira execução.
- Para parar: `Ctrl + C`. Para apagar também os dados do banco: `docker compose down -v`.
- Portas usadas: 5173 (frontend), 5001 (backend), 3307 (MySQL). Se alguma já estiver em uso no seu computador, pare o outro serviço antes.

---

## Opção 2: executar manualmente

### Pré-requisitos

- **Python** 3.10 ou superior
- **Node.js** 20.19 ou superior (ou 22.12+) e npm
- **MySQL** 8 (instalado localmente ou via Docker)

### 1. Banco de dados

Subindo o MySQL com Docker (se não tiver MySQL instalado):

```bash
docker run --name portal-mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0
```

Criando as tabelas e os dados iniciais (rodar a partir da raiz do projeto):

```bash
docker exec -i portal-mysql mysql -uroot -proot < databases/schema.sql
docker exec -i portal-mysql mysql -uroot -proot < databases/seed.sql
```

Com MySQL instalado localmente: `mysql -u root -p < databases/schema.sql` e depois o `seed.sql`.

> O `seed.sql` deve ser executado apenas uma vez (as solicitações de exemplo seriam duplicadas).

### 2. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # ajuste se necessário
flask --app run run --port 5001 --debug
```

A API fica disponível em `http://localhost:5001/api`.

> No macOS a porta 5000 é usada pelo AirPlay, por isso usamos a 5001.

### 3. Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Acesse **http://localhost:5173**.

O Vite repassa as chamadas `/api` para o backend (`http://localhost:5001`), configurado em `vite.config.js`.

### 4. Testes automatizados

```bash
cd backend
source .venv/bin/activate
pytest
```

Os testes usam SQLite em memória, então não precisam do MySQL rodando.

---

## Variáveis de ambiente (backend/.env)

| Variável | Exemplo | Descrição |
|---|---|---|
| `SECRET_KEY` | uma frase longa e aleatória | Chave usada para assinar o cookie de sessão. Deve ser secreta |
| `DATABASE_URL` | `mysql+pymysql://root:root@127.0.0.1:3306/portal?charset=utf8mb4` | Conexão com o MySQL |
| `CORS_ORIGINS` | `http://localhost:5173` | Origens autorizadas a chamar a API diretamente |
| `SESSION_COOKIE_SECURE` | `0` | Use `1` em produção com HTTPS |

## Endpoints da API

Todas as rotas, exceto o login, exigem usuário logado (senão retornam `401`).

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth/login` | Login. Corpo: `{"username": "...", "password": "..."}` |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Usuário logado |
| GET | `/api/requests` | Lista. Filtros: `q`, `category_id`, `status`, `date_from`, `date_to` (AAAA-MM-DD) |
| POST | `/api/requests` | Cria. Corpo: `{"title", "description", "category_id"}` |
| GET | `/api/requests/<id>` | Detalhes |
| PUT | `/api/requests/<id>` | Edita (dono + status Aberto) |
| DELETE | `/api/requests/<id>` | Exclui (dono + status Aberto) |
| PATCH | `/api/requests/<id>/status` | Altera status (atendente). Corpo: `{"status": "EM_ATENDIMENTO"}` |
| GET | `/api/categories` | Lista de categorias |
| GET | `/api/dashboard` | Indicadores |

Formato de erro: `{"error": "mensagem", "details": {"campo": "mensagem"}}`, com os códigos 400 (dados inválidos), 401 (não logado), 403 (sem permissão), 404 (não encontrado) e 409 (ação não permitida no status atual).

## Documentação

- [Memorial Técnico de Desenvolvimento](docs/MEMORIAL_TECNICO.md)
- [Dicionário de Dados](databases/dicionario_dados.md)
- [Evidências](docs/evidencias/)
