from multa import multa, valor_do_aluguel
import pytest

# MULTA

def test_antes_da_fronteira():
    assert multa(1) == 0.0


def test_na_fronteira_dos_dois_dias():
    assert multa(2) == 0.0


def test_depois_da_fronteira_dos_tres_dias():
    assert multa(3) == 15.0


def test_depois_da_fronteira_dos_quatro_dias():
    assert multa(4) == 20.0


# ALUGUEL

def test_aluguel_por_um_dia():
    assert valor_do_aluguel(10.0, 1) == 10.0


def test_aluguel_por_dois_dias():
    assert valor_do_aluguel(10.0, 2) == 20.0


def test_nao_aceita_aluguel_com_zero_dias():
    with pytest.raises(ValueError):
        valor_do_aluguel(10.0, 0)


def test_nao_aceita_aluguel_com_dias_negativos():
    with pytest.raises(ValueError):
        valor_do_aluguel(10.0, -2)

