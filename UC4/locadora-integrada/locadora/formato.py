# formato.py — como o dinheiro e a data aparecem para a pessoa.
#
# Fica separado do estilo.py porque este não importa o Tkinter: o terminal, a
# janela e a frase da regras.py usam o mesmo R$, e o terminal não precisa
# carregar a janela para isso.


def em_reais(valor):
    """8.5 -> "R$ 8,50": o balcão lê vírgula, não ponto."""
    return f"R$ {valor:.2f}".replace(".", ",")


def em_data(dia):
    """2026-11-13 -> "13/11/2026"."""
    return dia.strftime("%d/%m/%Y")
