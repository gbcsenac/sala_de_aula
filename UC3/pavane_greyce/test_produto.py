
from UC3.pavane_greyce.crud_produto import Produto


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