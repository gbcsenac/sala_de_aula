
erDiagram
    CLIENTE ||--o{ ENCOMENDA : realiza
    ENCOMENDA ||--o{ ITEM_ENCOMENDA : possui
    PRODUTO ||--o{ ITEM_ENCOMENDA : compoe

    CLIENTE {
        int id_cliente PK
        varchar nome
        varchar telefone
        varchar email
        varchar tipo
    }

    PRODUTO {
        int id_produto PK
        varchar nome
        tipo_produto tipo
        decimal preco
        int quantidade_disponivel
    }

    ENCOMENDA {
        int id_encomenda PK
        int id_cliente FK
        date data_pedido
        date data_pagamento
        date data_retirada
        text descricao
    }

    ITEM_ENCOMENDA {
        int id_encomenda PK, FK
        int id_produto PK, FK
        int quantidade
        decimal preco
    }
