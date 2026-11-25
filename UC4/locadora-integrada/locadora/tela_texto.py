# tela_texto.py — o terminal com print e input, sem biblioteca nenhuma.
#
# Tem os mesmos métodos da tela_rich.py; o menu.py usa qualquer uma das duas
# sem saber qual é.

import os

BARRA_CHEIA = 30   # quantos caracteres tem a barra do maior valor
# código ANSI: apaga a tela e põe o cursor no alto. O terminal do VS Code e o
# Windows Terminal entendem; o cmd, depois do os.system("") lá embaixo. O
# end="" evita uma linha em branco no topo
LIMPAR = "\033[2J\033[H"
INSTRUCOES = "Digite o número e aperte Enter. Nos campos, Enter mantém o que está entre colchetes. Ctrl+C sai."


class TelaDeTexto:
    def __init__(self):
        # No cmd do Windows, o código ANSI do LIMPAR sai como texto na tela, em
        # vez de limpar. Rodar um comando qualquer pelo sistema liga o ANSI no
        # console; o "" não faz nada além disso. Em Linux e Mac, não muda nada.
        os.system("")
        # o aviso do fim de uma ação: aparece no alto da próxima tela, porque
        # a tela é limpa logo depois e ele sumiria sem ninguém ler
        self.recado = ""

    def escolher(self, titulo, opcoes, sair):
        """Mostra as opções numeradas. Devolve a posição (0, 1, ...) ou None para sair."""
        while True:
            print(LIMPAR, end="")
            print(f"== {titulo} ==")
            if self.recado:
                print(self.recado)
                self.recado = ""
            print()
            for numero, opcao in enumerate(opcoes, start=1):
                print(f"  {numero} - {opcao}")
            print(f"  0 - {sair}")
            print()
            print(INSTRUCOES)
            texto = input("Escolha: ").strip()
            if texto == "0":
                return None
            if texto.isdigit() and 1 <= int(texto) <= len(opcoes):
                return int(texto) - 1
            self.recado = f"! Escreva um número de 0 a {len(opcoes)}."

    def perguntar(self, rotulo, padrao=""):
        """Enter sem digitar nada devolve o padrão (o valor que já estava)."""
        if padrao:
            texto = input(f"{rotulo} [{padrao}]: ")
            return texto if texto.strip() else padrao
        return input(f"{rotulo}: ")

    def confirmar(self, pergunta):
        return input(f"{pergunta} (s/n): ").strip().lower() == "s"

    def tabela(self, titulo, colunas, linhas):
        print()
        print(titulo)
        if not linhas:
            print("  (nada para mostrar)")
            return
        # a largura de cada coluna é a do texto mais comprido dela
        larguras = []
        for posicao, coluna in enumerate(colunas):
            larguras.append(max([len(coluna)] + [len(linha[posicao]) for linha in linhas]))
        print("  " + "  ".join(c.ljust(l) for c, l in zip(colunas, larguras)))
        print("  " + "  ".join("-" * l for l in larguras))
        for linha in linhas:
            print("  " + "  ".join(c.ljust(l) for c, l in zip(linha, larguras)))

    def numeros(self, lista):
        print()
        for valor, rotulo in lista:
            print(f"  {valor}  {rotulo}")

    def barras(self, titulo, linhas, maximo):
        print()
        print(titulo)
        if not linhas:
            print("  Ainda não houve aluguel.")
            return
        largura = max(len(nome) for nome, valor, texto in linhas)
        for nome, valor, texto in linhas:
            barra = "█" * round(BARRA_CHEIA * valor / maximo)
            print(f"  {nome.ljust(largura)}  {barra} {texto}")

    def aviso(self, texto):
        self.recado = f"! {texto}"

    def sucesso(self, texto):
        self.recado = f"✓ {texto}"

    def nota(self, texto):
        print(f"  {texto}")

    def pausar(self):
        input("\nEnter para voltar ao menu...")
