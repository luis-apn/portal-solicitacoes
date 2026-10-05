# Dicionário de Dados

Banco: **MySQL 8**, database `portal`, charset `utf8mb4`, collation `utf8mb4_0900_ai_ci`, engine InnoDB.
Scripts: `schema.sql` (estrutura) e `seed.sql` (dados iniciais).

## Diagrama (entidades e relacionamentos)

```
users (1) ────< (N) requests (N) >──── (1) categories
```

- Um usuário pode abrir várias solicitações; cada solicitação tem um único solicitante.
- Uma categoria pode ter várias solicitações; cada solicitação tem uma única categoria.

## Tabela `users`

Usuários que acessam o sistema.

| Coluna | Tipo | Nulo | Padrão | Restrições | Descrição |
|---|---|---|---|---|---|
| id | INT | Não | AUTO_INCREMENT | PK | Identificador do usuário |
| username | VARCHAR(50) | Não | | UNIQUE | Login usado para entrar no sistema |
| password_hash | VARCHAR(255) | Não | | | Hash da senha (scrypt com salt, gerado pelo Werkzeug). A senha nunca é armazenada |
| full_name | VARCHAR(120) | Não | | | Nome exibido nas telas |
| role | ENUM('SOLICITANTE','ATENDENTE') | Não | 'SOLICITANTE' | | Perfil. ATENDENTE pode alterar o status das solicitações |
| created_at | DATETIME | Não | CURRENT_TIMESTAMP | | Data de cadastro |

## Tabela `categories`

Categorias das solicitações (TI, RH, Compras, Financeiro, Infraestrutura).

| Coluna | Tipo | Nulo | Padrão | Restrições | Descrição |
|---|---|---|---|---|---|
| id | INT | Não | AUTO_INCREMENT | PK | Identificador da categoria |
| name | VARCHAR(50) | Não | | UNIQUE | Nome da categoria |

## Tabela `requests`

Solicitações internas registradas pelos colaboradores.

| Coluna | Tipo | Nulo | Padrão | Restrições | Descrição |
|---|---|---|---|---|---|
| id | INT | Não | AUTO_INCREMENT | PK | Código da solicitação (exibido como "#id") |
| title | VARCHAR(150) | Não | | | Título (3 a 150 caracteres, validado na API) |
| description | TEXT | Não | | | Descrição detalhada (10 a 5000 caracteres, validado na API) |
| requester_id | INT | Não | | FK → users.id (ON DELETE RESTRICT) | Usuário que abriu a solicitação. Preenchido automaticamente com o usuário logado |
| category_id | INT | Não | | FK → categories.id (ON DELETE RESTRICT) | Categoria da solicitação |
| status | ENUM('ABERTO','EM_ATENDIMENTO','CONCLUIDO') | Não | 'ABERTO' | Índice | Situação atual. Sempre nasce como ABERTO |
| created_at | DATETIME | Não | CURRENT_TIMESTAMP | Índice | Data de abertura. Preenchida automaticamente |
| updated_at | DATETIME | Não | CURRENT_TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Data da última alteração |

### Índices

| Índice | Coluna | Motivo |
|---|---|---|
| PRIMARY | id | Chave primária |
| ix_requests_status | status | Filtro por status e contagens do dashboard |
| ix_requests_created_at | created_at | Filtro por período e ordenação da lista |
| fk_requests_requester | requester_id | Criado automaticamente pelo MySQL para a FK |
| fk_requests_category | category_id | Criado automaticamente pelo MySQL para a FK (filtro por categoria) |

### Valores de `status`

| Valor no banco | Exibição | Significado |
|---|---|---|
| ABERTO | Aberto | Registrada, aguardando atendimento. Pode ser editada/excluída pelo solicitante |
| EM_ATENDIMENTO | Em Atendimento | Um atendente começou a tratar a demanda |
| CONCLUIDO | Concluído | Demanda finalizada |

Fluxo permitido: `ABERTO → EM_ATENDIMENTO → CONCLUIDO` (não é possível pular etapas nem voltar).

## Usuários de demonstração (seed.sql)

| Usuário | Senha | Perfil |
|---|---|---|
| ana | senha123 | SOLICITANTE |
| carlos | senha123 | SOLICITANTE |
| bruno | senha123 | ATENDENTE |
