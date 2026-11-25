# test_dados.py — a camada de dados, no banco de teste de verdade.
#
# Cada teste roda DUAS vezes: uma com o dados.py (psycopg2, o SQL escrito à
# mão) e outra com o dados_peewee.py (o ORM). Quem escolhe é a fixture dados,
# no conftest.py. As duas versões passarem é a prova de que fazem o mesmo.

from datetime import date
from decimal import Decimal

import peewee
import psycopg2 as pg
import pytest

# quando o banco recusa, cada versão avisa com o erro dela: o psycopg2 diz o
# motivo exato; o Peewee embrulha tudo no IntegrityError dele
REPETIDO = (pg.errors.UniqueViolation, peewee.IntegrityError)
AINDA_EM_USO = (pg.errors.ForeignKeyViolation, peewee.IntegrityError)
FORA_DA_REGRA = (pg.errors.CheckViolation, peewee.IntegrityError)

RETIRADA = date(2026, 11, 10)
PRAZO = date(2026, 11, 13)


def alugar_zelda_para_ana(dados, conexao):
    """O aluguel que vários testes usam: a Ana leva o Zelda por 3 dias."""
    zelda = dados.criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")
    dados.criar_cliente(conexao, "Ana", "(51) 90000-0000", None)
    ana = dados.listar_clientes(conexao)[0]
    dados.alugar(conexao, ana["id_cliente"], [(zelda.id_jogo, Decimal("24.00"))], RETIRADA, PRAZO)
    return zelda, ana


def test_cria_e_busca(dados, conexao):
    criado = dados.criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")

    achado = dados.buscar_jogo(conexao, criado.id_jogo)

    assert achado.titulo == "Zelda"
    assert achado.preco_diaria == Decimal("8.00")


def test_lista_em_ordem_de_titulo(dados, conexao):
    dados.criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")
    dados.criar_jogo(conexao, "FIFA 25", "Esporte", 2024, "9.00")

    assert [j.titulo for j in dados.listar_jogos(conexao)] == ["FIFA 25", "Zelda"]


def test_titulo_repetido_e_recusado_pelo_banco(dados, conexao):
    dados.criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")

    with pytest.raises(REPETIDO):
        dados.criar_jogo(conexao, "Zelda", "RPG", 2020, "5.00")


def test_apaga_jogo_que_tem_plataforma(dados, conexao):
    criado = dados.criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO plataforma (nome) VALUES ('Switch') RETURNING id_plataforma")
    cursor.execute(
        "INSERT INTO jogos_plataforma (id_jogo, id_plataforma) VALUES (%s, %s)",
        (criado.id_jogo, cursor.fetchone()[0]),
    )
    conexao.commit()

    assert dados.deletar_jogo(conexao, criado.id_jogo) is True
    assert dados.buscar_jogo(conexao, criado.id_jogo) is None


# ---------- jogos ----------

def test_altera_o_jogo(dados, conexao):
    criado = dados.criar_jogo(conexao, "Zelda", "Aventura", 2017, "8.00")

    dados.atualizar_jogo(conexao, criado.id_jogo, "Zelda", "RPG", 2017, "9.50")

    assert dados.buscar_jogo(conexao, criado.id_jogo).preco_diaria == Decimal("9.50")


def test_busca_pelo_titulo_sem_ligar_para_maiuscula(dados, conexao):
    dados.criar_jogo(conexao, "The Legend of Zelda", "Aventura", 2017, "8.00")
    dados.criar_jogo(conexao, "FIFA 25", "Esporte", 2024, "9.00")

    assert [j.titulo for j in dados.listar_jogos(conexao, "zelda")] == ["The Legend of Zelda"]


def test_jogo_alugado_nao_pode_ser_apagado(dados, conexao):
    zelda, ana = alugar_zelda_para_ana(dados, conexao)

    with pytest.raises(AINDA_EM_USO):
        dados.deletar_jogo(conexao, zelda.id_jogo)


# ---------- clientes ----------

def test_cliente_desativado_sai_da_lista(dados, conexao):
    dados.criar_cliente(conexao, "Ana", None, None)
    ana = dados.listar_clientes(conexao)[0]

    dados.desativar_cliente(conexao, ana["id_cliente"])

    assert dados.listar_clientes(conexao) == []


def test_email_repetido_e_recusado_pelo_banco(dados, conexao):
    dados.criar_cliente(conexao, "Ana", None, "ana@exemplo.com")

    with pytest.raises(REPETIDO):
        dados.criar_cliente(conexao, "Ana Souza", None, "ana@exemplo.com")


# ---------- aluguéis ----------

def test_jogo_alugado_some_dos_disponiveis(dados, conexao):
    alugar_zelda_para_ana(dados, conexao)
    dados.criar_jogo(conexao, "FIFA 25", "Esporte", 2024, "9.00")

    assert [j.titulo for j in dados.listar_jogos_disponiveis(conexao)] == ["FIFA 25"]


def test_aluguel_aparece_em_aberto_com_o_prazo(dados, conexao):
    alugar_zelda_para_ana(dados, conexao)

    aberto = dados.listar_alugueis_abertos(conexao)[0]

    assert (aberto["cliente"], aberto["jogos"], aberto["data_prevista"]) == ("Ana", "Zelda", PRAZO)


def test_devolucao_tira_dos_abertos_e_guarda_a_multa(dados, conexao):
    zelda, ana = alugar_zelda_para_ana(dados, conexao)
    aberto = dados.listar_alugueis_abertos(conexao)[0]

    dados.devolver(conexao, aberto["id_emprestimo"], date(2026, 11, 16), Decimal("15.00"))

    assert dados.listar_alugueis_abertos(conexao) == []
    cursor = conexao.cursor()
    cursor.execute("SELECT multa FROM emprestimo WHERE id_emprestimo = %s", (aberto["id_emprestimo"],))
    assert cursor.fetchone()[0] == Decimal("15.00")
    # e o jogo volta para a prateleira
    assert [j.titulo for j in dados.listar_jogos_disponiveis(conexao)] == ["Zelda"]


def test_o_mesmo_cliente_nao_aluga_duas_vezes_no_mesmo_dia(dados, conexao):
    zelda, ana = alugar_zelda_para_ana(dados, conexao)

    # a chave natural do empréstimo (UC2): cliente e dia de retirada
    with pytest.raises(REPETIDO):
        dados.alugar(conexao, ana["id_cliente"], [(zelda.id_jogo, Decimal("8.00"))], RETIRADA, PRAZO)


# ---------- resumo e configuração ----------

def test_os_numeros_do_resumo(dados, conexao):
    alugar_zelda_para_ana(dados, conexao)

    assert dados.alugueis_por_genero(conexao) == [("Aventura", 1)]
    assert dados.jogos_mais_alugados(conexao) == [("Zelda", 1)]


def test_configuracao_salva_e_lida(dados, conexao):
    dados.salvar_configuracao(conexao, "Game Over", "(51) 3333-0000", "10.00", 1, 2)

    configuracao = dados.ler_configuracao(conexao)

    assert configuracao["multa_por_dia"] == Decimal("10.00")
    assert configuracao["multa_a_partir_do_dia"] == 1


def test_configuracao_com_multa_negativa_e_recusada_pelo_banco(dados, conexao):
    with pytest.raises(FORA_DA_REGRA):
        dados.salvar_configuracao(conexao, "Locadora", None, "-1", 3, 3)
