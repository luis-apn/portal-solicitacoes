CREATE DATABASE IF NOT EXISTS portal 
    CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE portal;

/*Tabela de usuarios*/
CREATE TABLE IF NOT EXISTS users(
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    role ENUM('SOLICITANTE', 'ATENDENTE') NOT NULL DEFAULT 'SOLICITANTE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username)
) ENGINE=InnoDB;

/*Tabela de categorias*/
CREATE TABLE IF NOT EXISTS categories(
    id INT not null AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_categories_name (name)
) ENGINE=InnoDB;

/*Tabela de solicitações*/
CREATE TABLE IF NOT EXISTS requests(
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    requester_id INT NOT NULL,
    category_id INT NOT NULL,
    status ENUM('ABERTO', 'EM_ATENDIMENTO', 'CONCLUIDO') NOT NULL DEFAULT 'ABERTO',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_requests_status (status),
    KEY ix_requests_created_at (created_at),
    CONSTRAINT fk_requests_category  FOREIGN KEY (category_id)  REFERENCES categories (id) ON DELETE RESTRICT,
    CONSTRAINT fk_requests_requester FOREIGN KEY (requester_id) REFERENCES users (id)      ON DELETE RESTRICT
) ENGINE=InnoDB;
