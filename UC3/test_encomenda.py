#Regra: não aceitar encomenda sem cliente
from datetime import date
import pytest

from encomenda import Encomenda


def test_aceita_encomenda_com_cliente():
    encomenda = Encomenda(
        1,
        date.today(),
        date.today(),
        date.today(),
        "Caneca personalizada"
    )

    assert encomenda.id_cliente == 1


def test_aceita_outro_cliente_valido():
    encomenda = Encomenda(
        5,
        date.today(),
        date.today(),
        date.today(),
        "Camiseta personalizada"
    )

    assert encomenda.id_cliente == 5


def test_nao_aceita_encomenda_sem_cliente():
    with pytest.raises(ValueError):
        Encomenda(
            None,
            date.today(),
            date.today(),
            date.today(),
            "Produto personalizado"
        )
