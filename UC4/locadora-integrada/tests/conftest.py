# conftest.py — a conexão com o banco de TESTE, limpa antes de cada teste.
#
# É a fixture da UC3, Aula 05. A senha vem do .env, pela mesma função que a
# janela usa — só muda o banco: PG_BANCO_DE_TESTE, nunca o de verdade.

import pytest

from locadora import dados as dados_psycopg2
from locadora import dados_peewee
from locadora.conexao import conectar


@pytest.fixture(params=["psycopg2", "peewee"])
def dados(request):
    """A camada de dados, uma versão de cada vez: o teste que pede esta
    fixture roda duas vezes, e o nome da versão aparece no relatório."""
    if request.param == "peewee":
        return dados_peewee
    return dados_psycopg2


@pytest.fixture
def conexao(dados):
    if dados is dados_peewee:
        conexao = dados_peewee.conectar("PG_BANCO_DE_TESTE")
    else:
        conexao = conectar("PG_BANCO_DE_TESTE")
    cursor = conexao.cursor()
    # CASCADE leva junto quem aponta para elas: jogos_plataforma, emprestimo
    # e item_emprestimo
    cursor.execute("TRUNCATE jogo, plataforma, cliente RESTART IDENTITY CASCADE")
    # a configuração não se apaga: o sistema conta com a linha dela. Volta aos
    # valores de fábrica, para um teste não herdar a multa que outro mudou
    cursor.execute(
        "UPDATE configuracao SET nome_da_locadora = 'Locadora', telefone_da_locadora = NULL, "
        "multa_por_dia = 5.00, multa_a_partir_do_dia = 3, dias_padrao = 3 WHERE id = 1"
    )
    conexao.commit()
    yield conexao
    conexao.close()
