-- 1. CRIAR O TIPO DE PRODUTO
DO $$
BEGIN
    CREATE TYPE tipo_produto AS ENUM ('caneca', 'camiseta');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- 2. TABELA CLIENTE
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    tipo VARCHAR(50)
);

-- 3. TABELA PRODUTO
CREATE TABLE IF NOT EXISTS produto (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo tipo_produto NOT NULL,
    preco NUMERIC(10,2) NOT NULL,
    quantidade_disponivel INTEGER
);

-- 4. TABELA ENCOMENDA
CREATE TABLE IF NOT EXISTS encomenda (
    id_encomenda SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    data_pedido DATE,
    data_pagamento DATE,
    data_retirada DATE,
    descricao TEXT,
    FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
);

-- 5. TABELA ITEM_ENCOMENDA
CREATE TABLE IF NOT EXISTS item_encomenda (
    id_produto INTEGER,
    id_encomenda INTEGER,
    quantidade INTEGER NOT NULL,
    preco NUMERIC(10,2) NOT NULL,

    PRIMARY KEY (id_produto, id_encomenda),

    FOREIGN KEY (id_produto)
        REFERENCES produto(id_produto),

    FOREIGN KEY (id_encomenda)
        REFERENCES encomenda(id_encomenda)
);
