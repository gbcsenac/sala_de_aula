
import pytest
import psycopg2 as pg


BANCO_DE_TESTE = {
    "host": "localhost",
    "port": 5432,
    "dbname": "pavane_greyce_teste",
    "user": "postgres",
    "password": "postgres",
}


@pytest.fixture
def conexao():
    conexao = pg.connect(**BANCO_DE_TESTE)

    cursor = conexao.cursor()

    cursor.execute("""
        TRUNCATE TABLE
            item_encomenda,
            encomenda,
            produto,
            cliente
        RESTART IDENTITY CASCADE;
    """)

    conexao.commit()
    cursor.close()

    yield conexao

    conexao.close()
