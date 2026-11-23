
from crud_produto import Produto

def test_inserir_produto(conexao):
    produto = Produto(
        nome="Caneca personalizada",
        tipo="caneca",
        preco=35.00,
        quantidade_disponivel=10
    )

    resultado = produto.inserir_produto(conexao)

    assert resultado is not None
    assert resultado.id_produto is not None

def test_listar_produtos(conexao):
    produto = Produto(
        nome="Camiseta personalizada",
        tipo="camiseta",
        preco=50.00,
        quantidade_disponivel=5
    )

    produto.inserir_produto(conexao)

    produtos = Produto.listar_produtos(conexao)

    assert len(produtos) == 1
    assert produtos[0].nome == "Camiseta personalizada"

def test_atualizar_produto(conexao):
    produto = Produto(
        nome="Caneca personalizada",
        tipo="caneca",
        preco=35.00,
        quantidade_disponivel=10
    )

    produto.inserir_produto(conexao)

    produto.preco = 40.00

    resultado = produto.atualizar_produto(conexao)

    assert resultado is True

    produtos = Produto.listar_produtos(conexao)

    assert produtos[0].preco == 40.00

def test_excluir_produto(conexao):
    produto = Produto(
        nome="Caneca personalizada",
        tipo="caneca",
        preco=35.00,
        quantidade_disponivel=10
    )

    produto.inserir_produto(conexao)

    resultado = Produto.excluir_produto(produto.id_produto, conexao)

    assert resultado is True

    produtos = Produto.listar_produtos(conexao)

    assert len(produtos) == 0

def test_banco_recusa_preco_zero(conexao):
    produto = Produto(
        nome="Caneca inválida",
        tipo="caneca",
        preco=0.00,
        quantidade_disponivel=10
    )

    resultado = produto.inserir_produto(conexao)

    assert resultado is None


def test_banco_impede_excluir_produto_vinculado_a_encomenda(conexao):
    cursor = conexao.cursor()

    # 1. Cadastrar cliente
    cursor.execute("""
        INSERT INTO cliente (nome, telefone, email, tipo)
        VALUES (%s, %s, %s, %s)
        RETURNING id_cliente;
    """, ("Cliente Teste", "51999990000", "teste@email.com", "aluno"))

    id_cliente = cursor.fetchone()[0]

    # 2. Cadastrar encomenda
    cursor.execute("""
        INSERT INTO encomenda (id_cliente)
        VALUES (%s)
        RETURNING id_encomenda;
    """, (id_cliente,))

    id_encomenda = cursor.fetchone()[0]
    conexao.commit()

    # 3. Cadastrar produto
    produto = Produto(
        nome="Caneca vinculada",
        tipo="caneca",
        preco=35.00,
        quantidade_disponivel=10
    )

    produto.inserir_produto(conexao)

    # 4. Vincular produto à encomenda
    cursor.execute("""
        INSERT INTO item_encomenda
            (id_produto, id_encomenda, quantidade, preco)
        VALUES (%s, %s, %s, %s);
    """, (produto.id_produto, id_encomenda, 1, 35.00))

    conexao.commit()

    # 5. Tentar excluir o produto
    resultado = Produto.excluir_produto(produto.id_produto, conexao)

    assert resultado is False

    # 6. Confirmar que o produto continua cadastrado
    cursor.execute(
        "SELECT id_produto FROM produto WHERE id_produto = %s;",
        (produto.id_produto,)
    )

    assert cursor.fetchone() is not None

    cursor.close()
