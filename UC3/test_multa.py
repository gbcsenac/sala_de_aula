from multa import multa, valor_do_aluguel
import pytest

#multa
def test_antes_da_fronteira():
    assert multa(1) == 0.0

def test_na_fronteira_dos_dois_dias():
    assert multa(2) == 0.0

def test_depois_da_fronteira_dos_tres_dias():
    assert multa(3) == 15.0

def test_depois_da_fronteira_dos_quatro_dias():
    assert multa(4) == 20.0

MULTA_POR_DIA = 5.00

def multa(dias_atraso):
    """Multa pela devolução atrasada, em reais."""
    if dias_atraso > 2:
        return dias_atraso * MULTA_POR_DIA
    return 0.0

#aluguel
def test_aluguel_por_um_dia():
    assert valor_do_aluguel(10.0, 1) == 10.0


def test_aluguel_por_dois_dias():
    assert valor_do_aluguel(10.0, 2) == 20.0


def test_nao_aceita_zero_dias():
    with pytest.raises(ValueError):
        valor_do_aluguel(10.0, 0)


def test_nao_aceita_dias_negativos():
    with pytest.raises(ValueError):
        valor_do_aluguel(10.0, -1)

def valor_do_aluguel(diaria, dias):
    """Quanto o cliente paga ao retirar o jogo."""
    if dias <= 0:
        raise ValueError("A quantidade de dias deve ser maior que zero.")
    return diaria * dias