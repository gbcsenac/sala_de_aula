"""Empréstimo do balcão da locadora — ponto de partida da Aula 03 da UC3.

Este arquivo não tem teste nenhum, e é de propósito: hoje o teste nasce
ANTES do código. Crie o test_emprestimo.py nesta mesma pasta. O painel
Testing do VS Code só encontra arquivo cujo nome começa com test_, e é
por estar na mesma pasta que o "from emprestimo import ..." funciona.
"""

"""Empréstimo do balcão da locadora — UC3."""


class Cliente:
    """Representa um cliente da locadora."""

    def __init__(self, nome, total_emprestimos=0):
        self.nome = nome
        self.total_emprestimos = total_emprestimos

    def limite_de_jogos(self):
        if self.total_emprestimos > 10:
            return 4
        return 3


class Emprestimo:
    """Representa um empréstimo de jogos."""

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
