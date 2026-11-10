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

#Teste	O que verifica	Resultado esperado
#test_aceita_encomenda_com_cliente	Cliente com ID 1	PASS
#test_aceita_encomenda_com_outro_cliente	Cliente com ID 2	PASS
#test_nao_aceita_encomenda_sem_cliente	Cliente sem ID (None)	PASS, se lançar ValueError

# TDD - Testes da classe Encomenda
# Regra: não aceitar encomenda sem cliente.
# Resultado: 3 testes aprovados (3 passed).
# A classe Encomenda aceita clientes válidos
# e rejeita encomendas sem cliente (ValueError).