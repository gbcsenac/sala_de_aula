#Encomenda: não aceitar encomenda sem cliente
import pytest
from UC2.encomenda import Encomenda

def test_aceita_encomenda_com_cliente():
    encomenda = Encomenda(
        1, None, None, None, None
    )
    assert encomenda.id_cliente == 1


def test_aceita_encomenda_com_outro_cliente():
    encomenda = Encomenda(
        2, None, None, None, None
    )
    assert encomenda.id_cliente == 2


def test_nao_aceita_encomenda_sem_cliente():
    with pytest.raises(ValueError):
        Encomenda(None, None, None, None, None)