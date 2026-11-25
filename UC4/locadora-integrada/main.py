# main.py — por onde o sistema começa. No VS Code: abra este arquivo e ▶.
#
# Ele só liga as peças: abre a conexão, entrega à janela, e fecha a conexão
# quando a janela fecha — mesmo que algo dê errado no meio.

from locadora.conexao import conectar
from locadora.janela import JanelaDaLocadora


def main():
    conexao = conectar()
    try:
        JanelaDaLocadora(conexao).mainloop()
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
