# test_regras.py — a camada de regras, sem banco e sem janela.

from datetime import date

import pytest

from locadora.regras import (
    atrasados, dias_de_atraso, explicar_multa, itens_do_aluguel, juntar_em_outros, multa,
    preparar_cliente, preparar_jogo, validar_aluguel, validar_cliente, validar_configuracao,
    validar_jogo, valor_do_aluguel,
)


def test_dois_dias_de_atraso_nao_tem_multa():
    assert multa(2) == 0.0


def test_no_terceiro_dia_ja_cobra():
    assert multa(3) == 15.0


def test_aluguel_de_zero_dias_e_recusado():
    with pytest.raises(ValueError):
        valor_do_aluguel(8.0, 0)


def test_jogo_completo_nao_tem_problema():
    assert validar_jogo("Zelda", "2017", "8,50") == []


def test_titulo_em_branco_e_recusado():
    assert validar_jogo("   ", "2017", "8,50") == ["O título não pode ficar em branco."]


def test_ano_nao_numerico_e_recusado():
    assert validar_jogo("Zelda", "dois mil", "8,50") == ["O ano tem de ser um número, como 2017."]


def test_ano_antes_de_1971_e_recusado():
    assert validar_jogo("Pong", "1970", "1") == ["O ano tem de ser depois de 1970."]


def test_ano_pode_ficar_em_branco():
    assert validar_jogo("Zelda", "", "8") == []


def test_preco_negativo_e_recusado():
    assert validar_jogo("Zelda", "2017", "-1") == ["O preço da diária não pode ser negativo."]


def test_preco_com_letra_e_recusado():
    assert validar_jogo("Zelda", "2017", "oito") == [
        "O preço da diária tem de ser um número, como 8,50."
    ]


# ---------- atraso e multa ----------

def test_no_dia_do_prazo_ainda_nao_e_atraso():
    assert dias_de_atraso(date(2026, 11, 13), date(2026, 11, 13)) == 0


def test_no_dia_seguinte_ao_prazo_ja_e_atraso():
    assert dias_de_atraso(date(2026, 11, 13), date(2026, 11, 14)) == 1


def test_multa_com_a_configuracao_da_loja():
    # R$ 10,00 por dia, cobrando desde o 1º dia
    assert multa(1, 10.00, 1) == 10.00


def test_atrasado_de_2_dias_aparece_sem_multa():
    abertos = [{"data_prevista": date(2026, 11, 17)}]
    atrasado = atrasados(abertos, date(2026, 11, 19))[0]
    assert (atrasado["dias"], atrasado["multa"]) == (2, 0)


def test_atrasado_de_3_dias_aparece_com_15_reais():
    abertos = [{"data_prevista": date(2026, 11, 16)}]
    assert atrasados(abertos, date(2026, 11, 19))[0]["multa"] == 15.0


def test_aluguel_no_prazo_nao_e_atrasado():
    abertos = [{"data_prevista": date(2026, 12, 1)}]
    assert atrasados(abertos, date(2026, 11, 19)) == []


def test_a_explicacao_usa_os_numeros_digitados():
    assert explicar_multa("5,00", "3") == (
        "Com 3, quem atrasa de 1 a 2 dias não paga multa; no 3º dia, paga 3 × R$ 5,00 = R$ 15,00."
    )


# ---------- aluguel ----------

def test_aluguel_completo_nao_tem_problema():
    assert validar_aluguel(1, ["um jogo"], "3") == []


def test_aluguel_sem_cliente_sem_jogo_e_sem_dias():
    assert validar_aluguel(None, [], "0") == [
        "Escolha o cliente.",
        "Escolha pelo menos um jogo.",
        "O aluguel precisa ser de pelo menos 1 dia.",
    ]


def test_dias_com_letra_sao_recusados():
    assert validar_aluguel(1, ["um jogo"], "três") == ["Os dias têm de ser um número, como 3."]


class JogoFalso:
    """Dublê do Jogo da dados.py, só com o que a regra lê: sem importar o
    banco num teste de regra (UC3, Aula 04)."""
    def __init__(self, id_jogo, preco_diaria):
        self.id_jogo = id_jogo
        self.preco_diaria = preco_diaria


def test_o_total_soma_a_diaria_de_cada_jogo_pelos_dias():
    jogos = [JogoFalso(1, 8.50), JogoFalso(2, 9.00)]
    itens, total = itens_do_aluguel(jogos, 2)
    assert itens == [(1, 17.00), (2, 18.00)]
    assert total == 35.00


# ---------- do texto digitado para o banco ----------

def test_campos_vazios_do_jogo_viram_nulo_e_virgula_vira_ponto():
    assert preparar_jogo(" Zelda ", "", "", "8,50") == ([], ("Zelda", None, None, "8.50"))


def test_email_sem_arroba_e_recusado():
    assert validar_cliente("Ana", "ana.exemplo.com") == ["O e-mail precisa ter @, como ana@exemplo.com."]


def test_email_vazio_vira_nulo():
    # dois clientes com e-mail "" bateriam no UNIQUE; com NULL, não
    assert preparar_cliente("Ana", "", "") == ([], ("Ana", None, None))


def test_configuracao_com_multa_negativa_e_dia_zero():
    assert validar_configuracao("Locadora", "-1", "0", "3") == [
        "A multa por dia não pode ser negativa.",
        "O dia em que a multa começa tem de ser 1 ou mais.",
    ]


# ---------- resumo ----------

def test_da_sexta_barra_em_diante_vira_outros():
    generos = [("a", 5), ("b", 4), ("c", 3), ("d", 2), ("e", 1), ("f", 1), ("g", 1)]
    assert juntar_em_outros(generos)[-1] == ("Outros", 2)
