-- Dados iniciais: categorias, usuários de demonstração e algumas solicitações de exemplo.
-- Execute APENAS UMA VEZ, depois do schema.sql (as solicitações de exemplo seriam duplicadas).
-- Senha de todos os usuários de demonstração: senha123

SET NAMES utf8mb4;
USE portal;

INSERT IGNORE INTO categories (name) VALUES
  ('TI'), ('RH'), ('Compras'), ('Financeiro'), ('Infraestrutura');

-- O password_hash foi gerado com werkzeug.security.generate_password_hash('senha123')
INSERT IGNORE INTO users (username, password_hash, full_name, role) VALUES
  ('ana', 'scrypt:32768:8:1$HRiM812dv1G21eVC$a2dbb6b981cd25804b1278e356f9b82f1fd0e1012de57a82dd312da46958a4392dc596f831cdc293f4ea05a11d20e66fe4959cda8b6e9d0c4d0db6c88dcaeacb', 'Ana Souza', 'SOLICITANTE'),
  ('carlos', 'scrypt:32768:8:1$RYLiRGl6SarTIrSn$e3a6765c028bf2b1c140945966d53b02220ed64ab047addc538c66fabb5c9d1fd1ece25f5e573217acffd20b7a87da50d74b3af3ca044bdff4ceba667ac9cc1f', 'Carlos Pereira', 'SOLICITANTE'),
  ('bruno', 'scrypt:32768:8:1$nk72IByfsadUxjix$e46c6b2649896033423442a76848a95a7ae839d5f2ead66552662e04de65a6137d72397c4e4ba4e1e1c2754a0eeac849c4973e857ccae0f1a5b9f1120c82d1e5', 'Bruno Lima', 'ATENDENTE');

INSERT INTO requests (title, description, requester_id, category_id, status, created_at, updated_at) VALUES
  ('Notebook não liga', 'O notebook da recepção não liga desde ontem.',
    (SELECT id FROM users WHERE username = 'ana'), (SELECT id FROM categories WHERE name = 'TI'),
    'ABERTO', NOW() - INTERVAL 1 DAY, NOW() - INTERVAL 1 DAY),
  ('Solicitação de férias', 'Gostaria de agendar minhas férias para o mês de dezembro.',
    (SELECT id FROM users WHERE username = 'ana'), (SELECT id FROM categories WHERE name = 'RH'),
    'EM_ATENDIMENTO', NOW() - INTERVAL 3 DAY, NOW() - INTERVAL 2 DAY),
  ('Compra de cadeiras', 'Precisamos de 4 cadeiras novas para a sala de reunião.',
    (SELECT id FROM users WHERE username = 'carlos'), (SELECT id FROM categories WHERE name = 'Compras'),
    'ABERTO', NOW() - INTERVAL 5 DAY, NOW() - INTERVAL 5 DAY),
  ('Reembolso de viagem', 'Reembolso das despesas da viagem a Recife em setembro.',
    (SELECT id FROM users WHERE username = 'carlos'), (SELECT id FROM categories WHERE name = 'Financeiro'),
    'CONCLUIDO', NOW() - INTERVAL 10 DAY, NOW() - INTERVAL 7 DAY),
  ('Ar-condicionado com vazamento', 'O ar-condicionado da sala 2 está pingando água no chão.',
    (SELECT id FROM users WHERE username = 'ana'), (SELECT id FROM categories WHERE name = 'Infraestrutura'),
    'EM_ATENDIMENTO', NOW() - INTERVAL 12 DAY, NOW() - INTERVAL 11 DAY);
