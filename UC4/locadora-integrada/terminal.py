# terminal.py — o sistema no terminal, só com print e input.
# No VS Code: abra este arquivo e ▶. A janela é o main.py; com rich, o
# terminal_rich.py. Os três usam as mesmas regras.py e dados.py.

from locadora.conexao import conectar
from locadora.menu import Menu
from locadora.tela_texto import TelaDeTexto


def main():
    conexao = conectar()
    try:
        Menu(conexao, TelaDeTexto()).rodar()
    except (KeyboardInterrupt, EOFError):
        pass   # Ctrl+C ou Ctrl+D saem do sistema, sem a mensagem de erro do Python
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
