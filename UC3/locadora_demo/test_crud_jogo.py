from decimal import Decimal
from crud_jogo import criar_jogo, buscar_jogo, buscar_por_titulo
from crud_jogo import criar_jogo, buscar_jogo, buscar_por_titulo, deletar_jogo



def test_cria_e_busca_pelo_id(conexao):
    criado = criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")
    achado = buscar_jogo(conexao, criado.id_jogo)

    assert achado.titulo == "Zelda"
    assert achado.preco_diaria == Decimal("8.00")

def test_busca_jogo_pelo_titulo(conexao):
    criar_jogo(conexao, "Mario", "Aventura", 2020, "10.00")

    achado = buscar_por_titulo(conexao, "Mario")

    assert achado.titulo == "Mario"

def test_apaga_jogo(conexao):
    criado = criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")

    assert deletar_jogo(conexao, criado.id_jogo) is True
    assert buscar_jogo(conexao, criado.id_jogo) is None

def test_deleta_jogo_com_plataforma(conexao):
    criado = criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")

    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO plataforma (nome) VALUES ('Switch') RETURNING id_plataforma"
    )
    id_plataforma = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO jogos_plataforma (id_jogo, id_plataforma) VALUES (%s, %s)",
        (criado.id_jogo, id_plataforma)
    )
    conexao.commit()

    assert deletar_jogo(conexao, criado.id_jogo) is True

def test_banco_recusa_preco_negativo(conexao):
    assert criar_jogo(conexao, "Zelda", "Aventura", 2017, "-1.00") is None


def test_banco_recusa_titulo_repetido(conexao):
    criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")
    assert criar_jogo(conexao, "Zelda", "RPG", 2020, "5.00") is None
