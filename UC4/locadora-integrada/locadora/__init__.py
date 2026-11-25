"""O sistema da locadora, em três camadas.

    janela.py  — a interface: o que a pessoa vê e clica
    regras.py  — as regras do negócio: o que pode e o que não pode
    dados.py   — o acesso ao banco: o SQL, e só ele

Cada camada só conversa com a de baixo. A janela nunca escreve SQL, e o
SQL nunca abre janela — é isso que deixa trocar uma sem quebrar a outra,
e testar a regra sem banco nem tela.
"""
