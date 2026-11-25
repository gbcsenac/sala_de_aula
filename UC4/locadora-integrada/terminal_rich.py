# terminal_rich.py — o sistema no terminal, com a biblioteca rich.
# No VS Code: abra este arquivo e ▶. A janela é o main.py; sem rich, o
# terminal.py. Os três usam as mesmas regras.py e dados.py.

from locadora.conexao import conectar
from locadora.menu import Menu
from locadora.tela_rich import TelaRich


def main():
    conexao = conectar()
    try:
        Menu(conexao, TelaRich()).rodar()
    except (KeyboardInterrupt, EOFError):
        pass   # Ctrl+C ou Ctrl+D saem do sistema, sem a mensagem de erro do Python
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
