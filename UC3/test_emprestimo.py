#Parte A — o cliente fiel, na locadora
import pytest
from UC3.emprestimo import Cliente, Emprestimo


def test_cliente_com_10_ainda_leva_3():
    cliente = Cliente("Caio", 10)
    assert cliente.limite_de_jogos() == 3


def test_cliente_com_11_leva_4():
    cliente = Cliente("Ana", 11)
    assert cliente.limite_de_jogos() == 4


def test_cliente_com_10_ainda_leva_3_no_emprestimo():
    emprestimo = Emprestimo(Cliente("Caio", 10))

    for jogo in ["Zelda", "FIFA 25", "Hades"]:
        emprestimo.adicionar(jogo)

    with pytest.raises(ValueError):
        emprestimo.adicionar("Celeste")


def test_cliente_fiel_pode_levar_4_jogos():
    emprestimo = Emprestimo(Cliente("Ana", 11))

    for jogo in ["Zelda", "FIFA 25", "Hades", "Celeste"]:
        emprestimo.adicionar(jogo)

    assert len(emprestimo.jogos) == 4


def test_cliente_fiel_nao_pode_levar_5_jogos():
    emprestimo = Emprestimo(Cliente("Ana", 11))

    for jogo in ["Zelda", "FIFA 25", "Hades", "Celeste"]:
        emprestimo.adicionar(jogo)

    with pytest.raises(ValueError):
        emprestimo.adicionar("Mario Kart")


def test_nao_aceita_titulo_vazio():
    emprestimo = Emprestimo(Cliente("Ana", 0))

    with pytest.raises(ValueError):
        emprestimo.adicionar("")


def test_nao_aceita_o_mesmo_jogo_duas_vezes():
    emprestimo = Emprestimo(Cliente("Ana", 0))

    emprestimo.adicionar("Zelda")

    with pytest.raises(ValueError):
        emprestimo.adicionar("Zelda")

    assert emprestimo.jogos == ["Zelda"]