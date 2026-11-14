#Parte A — o cliente fiel, na locadora
import pytest
class Cliente:
    def __init__(self, nome, total_emprestimos):
        self.nome = nome
        self.total_emprestimos = total_emprestimos

    def limite_de_jogos(self):
        if self.total_emprestimos > 10:
            return 4
        return 3

class Emprestimo:
    def __init__(self, cliente):
        self.cliente = cliente
        self.jogos = []

    def adicionar(self, jogo):
        if not jogo.strip():
            raise ValueError("Título não pode ser vazio")
        
        if jogo in self.jogos:
            raise ValueError("Jogo já adicionado")

        if len(self.jogos) >= self.cliente.limite_de_jogos():
            raise ValueError("Limite de jogos atingido")

        self.jogos.append(jogo)


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
    
