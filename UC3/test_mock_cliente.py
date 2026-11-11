
from unittest.mock import Mock, MagicMock
from UC2.cliente import Cliente, RepositorioCliente


def criar_repositorio_mock():
    # Cria conexão e cursor simulados
    mock_conexao = MagicMock()
    mock_cursor = MagicMock()

    mock_conexao.cursor.return_value = mock_cursor

    # Cria o repositório usando a conexão simulada
    repositorio = RepositorioCliente(conexao=mock_conexao)

    return repositorio, mock_conexao, mock_cursor


# TESTE 1 - INSERT
def test_inserir_cliente():

    repositorio, conexao, cursor = criar_repositorio_mock()

    cliente = Cliente(
        nome="Maria",
        telefone="51999999999",
        email="maria@email.com",
        tipo="Aluno"
    )

    cursor.fetchone.return_value = (1,)

    resultado = repositorio.inserir_cliente(cliente)

    cursor.execute.assert_called_once()
    conexao.commit.assert_called_once()

    assert resultado.id_cliente == 1
    assert resultado.nome == "Maria"


# TESTE 2 - SELECT
def test_listar_clientes():

    repositorio, conexao, cursor = criar_repositorio_mock()

    cursor.fetchall.return_value = [
        (1, "Maria", "51999999999", "maria@email.com", "Aluno"),
        (2, "João", "51988888888", "joao@email.com", "Professor")
    ]

    resultado = repositorio.listar_clientes()

    cursor.execute.assert_called_once()

    assert len(resultado) == 2
    assert resultado[0].nome == "Maria"
    assert resultado[1].nome == "João"


# TESTE 3 - UPDATE
def test_atualizar_cliente():

    repositorio, conexao, cursor = criar_repositorio_mock()

    cliente = Cliente(
        nome="Maria Atualizada",
        telefone="51999999999",
        email="maria@email.com",
        tipo="Aluno",
        id_cliente=1
    )

    cursor.rowcount = 1

    resultado = repositorio.atualizar_cliente(cliente)

    cursor.execute.assert_called_once()
    conexao.commit.assert_called_once()

    assert resultado is True


# TESTE 4 - DELETE
def test_excluir_cliente():

    repositorio, conexao, cursor = criar_repositorio_mock()

    cursor.rowcount = 1

    resultado = repositorio.excluir_cliente(1)

    cursor.execute.assert_called_once()
    conexao.commit.assert_called_once()

    assert resultado is True


# Regra: Cliente cadastrado utilizando o CRUD.
# PASS = passou ✅
# FAIL = falhou ❌
# ERROR = erro na execução ⚠️

# test_inserir_cliente: PASS
# test_listar_clientes: PASS
# test_atualizar_cliente: PASS
# test_excluir_cliente: PASS