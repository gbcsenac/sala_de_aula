-- criar_tabelas.sql — as tabelas que este módulo usa.
--
-- Rode no pgAdmin, no Query Tool, uma vez no banco "locadora" e outra no
-- "locadora_teste". Pode rodar de novo sem estragar nada: só cria o que
-- ainda não existe (PADRAO-SQL da UC2).

CREATE TABLE IF NOT EXISTS plataforma (
    id_plataforma  SERIAL       PRIMARY KEY,
    nome           VARCHAR(50)  NOT NULL UNIQUE,
    fabricante     VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS jogo (
    id_jogo         SERIAL         PRIMARY KEY,
    titulo          VARCHAR(150)   NOT NULL UNIQUE,
    genero          VARCHAR(40),
    ano_lancamento  INTEGER        CHECK (ano_lancamento > 1970),
    preco_diaria    NUMERIC(10,2)  CHECK (preco_diaria >= 0)
);

CREATE TABLE IF NOT EXISTS jogos_plataforma (
    id_jogo        INTEGER  NOT NULL REFERENCES jogo(id_jogo),
    id_plataforma  INTEGER  NOT NULL REFERENCES plataforma(id_plataforma),
    PRIMARY KEY (id_jogo, id_plataforma)
);

-- As três de baixo são as do aluguel, iguais às do locadora-demo.sql da UC2.
-- Cliente antes de emprestimo, e emprestimo antes de item_emprestimo: quem é
-- apontado vem antes de quem aponta.

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente     SERIAL        PRIMARY KEY,
    nome           VARCHAR(100)  NOT NULL,
    -- telefone é texto: tem traço, parêntese e zero à esquerda
    telefone       VARCHAR(20),
    email          VARCHAR(120)  UNIQUE,
    data_cadastro  DATE          DEFAULT CURRENT_DATE,
    ativo          BOOLEAN       DEFAULT TRUE,
    CONSTRAINT cliente_natural_uk UNIQUE (nome, telefone)
);

CREATE TABLE IF NOT EXISTS emprestimo (
    id_emprestimo   SERIAL   PRIMARY KEY,
    id_cliente      INTEGER  NOT NULL REFERENCES cliente(id_cliente),
    data_retirada   DATE     NOT NULL,
    data_prevista   DATE     NOT NULL CHECK (data_prevista >= data_retirada),
    -- nulo quer dizer "ainda não devolveu"
    data_entregue   DATE,
    -- guardada na devolução: se a regra mudar, o que foi cobrado não muda junto
    multa           NUMERIC(10,2)  DEFAULT 0  CHECK (multa >= 0),
    CONSTRAINT emprestimo_natural_uk UNIQUE (id_cliente, data_retirada)
);

CREATE TABLE IF NOT EXISTS item_emprestimo (
    id_emprestimo  INTEGER        NOT NULL REFERENCES emprestimo(id_emprestimo),
    id_jogo        INTEGER        NOT NULL REFERENCES jogo(id_jogo),
    -- o que foi cobrado neste aluguel; o preco_diaria do jogo é o de hoje
    preco_pago     NUMERIC(10,2)  NOT NULL CHECK (preco_pago >= 0),
    PRIMARY KEY (id_emprestimo, id_jogo)
);

-- As configurações do sistema: uma tabela de UMA linha só, com uma coluna por
-- configuração. Cada uma tem o tipo dela e um CHECK, e o banco recusa sozinho
-- multa negativa ou aluguel de zero dias. O CHECK (id = 1) impede a segunda
-- linha: configuração é uma só para a loja inteira.
CREATE TABLE IF NOT EXISTS configuracao (
    id                     INTEGER        PRIMARY KEY CHECK (id = 1),
    nome_da_locadora       VARCHAR(80)    NOT NULL,
    telefone_da_locadora   VARCHAR(20),
    multa_por_dia          NUMERIC(10,2)  NOT NULL CHECK (multa_por_dia >= 0),
    multa_a_partir_do_dia  INTEGER        NOT NULL CHECK (multa_a_partir_do_dia >= 1),
    dias_padrao            INTEGER        NOT NULL CHECK (dias_padrao >= 1)
);

-- os valores de fábrica; rodar de novo não apaga o que a loja já mudou
INSERT INTO configuracao (id, nome_da_locadora, telefone_da_locadora, multa_por_dia,
                          multa_a_partir_do_dia, dias_padrao)
VALUES (1, 'Locadora', NULL, 5.00, 3, 3)
ON CONFLICT DO NOTHING;
