
from unittest.mock import Mock

from cliente import Cliente
from regras_encomenda import ServicoEncomenda


def criar_servico_mock():
    repositorio_clientes = Mock()
    repositorio_produtos = Mock()

    servico = ServicoEncomenda(
        repositorio_clientes,
        repositorio_produtos
    )

    return servico, repositorio_clientes, repositorio_produtos


# REGRA 1 - CLIENTE CADASTRADO

def test_cliente_cadastrado_permite_encomenda():

    servico, repositorio_clientes, repositorio_produtos = criar_servico_mock()

    cliente = Cliente(
        nome="Maria",
        telefone="51999999999",
        id_cliente=1
    )

    repositorio_clientes.listar_clientes.return_value = [cliente]

    resultado = servico.cliente_cadastrado(1)

    repositorio_clientes.listar_clientes.assert_called_once()

    assert resultado is True


def test_cliente_nao_cadastrado_impede_encomenda():

    servico, repositorio_clientes, repositorio_produtos = criar_servico_mock()

    repositorio_clientes.listar_clientes.return_value = []

    resultado = servico.cliente_cadastrado(2)

    repositorio_clientes.listar_clientes.assert_called_once()

    assert resultado is False


# REGRA 2 - ESTOQUE DISPONIVEL

def test_estoque_suficiente_permite_encomenda():

    servico, repositorio_clientes, repositorio_produtos = criar_servico_mock()

    produto = Mock()
    produto.quantidade_disponivel = 10

    repositorio_produtos.buscar_produto.return_value = produto

    resultado = servico.estoque_disponivel(1, 10)

    repositorio_produtos.buscar_produto.assert_called_once_with(1)

    assert resultado is True


def test_estoque_insuficiente_impede_encomenda():

    servico, repositorio_clientes, repositorio_produtos = criar_servico_mock()

    produto = Mock()
    produto.quantidade_disponivel = 5

    repositorio_produtos.buscar_produto.return_value = produto

    resultado = servico.estoque_disponivel(1, 8)

    repositorio_produtos.buscar_produto.assert_called_once_with(1)

    assert resultado is False

def test_produto_nao_encontrado_impede_encomenda():

    servico, repositorio_clientes, repositorio_produtos = criar_servico_mock()

    repositorio_produtos.buscar_produto.return_value = None

    resultado = servico.estoque_disponivel(99, 2)

    repositorio_produtos.buscar_produto.assert_called_once_with(99)

    assert resultado is False

