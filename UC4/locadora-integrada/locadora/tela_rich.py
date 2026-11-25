# tela_rich.py — o terminal com a biblioteca rich: cor, tabela com borda e
# barra de verdade.
#
# Tem os mesmos métodos da tela_texto.py; o menu.py usa qualquer uma das duas
# sem saber qual é. Compare as duas: o que muda é só o jeito de mostrar.

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

LARANJA = "#f07300"
BARRA_CHEIA = 30
INSTRUCOES = "Digite o número e aperte Enter. Nos campos, Enter mantém o que está entre parênteses. Ctrl+C sai."


class TelaRich:
    def __init__(self):
        self.console = Console()
        # o aviso do fim de uma ação: aparece no alto da próxima tela, porque
        # a tela é limpa logo depois e ele sumiria sem ninguém ler
        self.recado = ""

    def escolher(self, titulo, opcoes, sair):
        while True:
            self.console.clear()
            self.console.rule(f"[bold]{titulo}")
            if self.recado:
                self.console.print(self.recado)
                self.recado = ""
            self.console.print()
            for numero, opcao in enumerate(opcoes, start=1):
                self.console.print(f"  [bold]{numero}[/] {opcao}")
            self.console.print(f"  [bold]0[/] {sair}")
            self.console.print()
            self.console.print(f"[dim]{INSTRUCOES}[/]")
            # a conferência é a mesma da tela de texto: o choices= do Prompt
            # avisaria o erro em inglês
            texto = Prompt.ask("Escolha").strip()
            if texto == "0":
                return None
            if texto.isdigit() and 1 <= int(texto) <= len(opcoes):
                return int(texto) - 1
            self.recado = f"[bold yellow]![/] Escreva um número de 0 a {len(opcoes)}."

    def perguntar(self, rotulo, padrao=""):
        return Prompt.ask(rotulo, default=padrao, show_default=bool(padrao))

    def confirmar(self, pergunta):
        # o Confirm do rich pergunta [y/n] e só aceita "y"; aqui é s/n
        return Prompt.ask(f"{pergunta} [bold](s/n)[/]").strip().lower() == "s"

    def tabela(self, titulo, colunas, linhas):
        tabela = Table(title=titulo, title_justify="left", header_style="bold")
        for coluna in colunas:
            tabela.add_column(coluna)
        for linha in linhas:
            tabela.add_row(*linha)
        if not linhas:
            tabela.add_row("(nada para mostrar)", *[""] * (len(colunas) - 1))
        self.console.print(tabela)

    def numeros(self, lista):
        self.console.print()
        for valor, rotulo in lista:
            self.console.print(f"  [bold]{valor}[/]  {rotulo}")

    def barras(self, titulo, linhas, maximo):
        self.console.print()
        self.console.print(f"[bold]{titulo}")
        if not linhas:
            self.console.print("  Ainda não houve aluguel.")
            return
        largura = max(len(nome) for nome, valor, texto in linhas)
        for nome, valor, texto in linhas:
            barra = "█" * round(BARRA_CHEIA * valor / maximo)
            # a barra é laranja; o texto continua na cor do terminal
            self.console.print(f"  {nome.ljust(largura)}  [{LARANJA}]{barra}[/] {texto}")

    def aviso(self, texto):
        self.recado = f"[bold yellow]![/] {texto}"

    def sucesso(self, texto):
        self.recado = f"[bold green]✓[/] {texto}"

    def nota(self, texto):
        self.console.print(f"  [dim]{texto}[/]")

    def pausar(self):
        Prompt.ask("\nEnter para voltar ao menu", default="", show_default=False)
