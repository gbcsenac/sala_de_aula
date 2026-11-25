# aba_resumo.py — a aba Resumo: os números do dia, uma pizza e um gráfico
# de barras.
#
# Os gráficos são do matplotlib, a biblioteca de gráficos mais usada do
# Python: a pizza é uma chamada (pie) e as barras, outra (barh). A Figure
# fica dentro da janela pelo FigureCanvasTkAgg, a ponte entre os dois.

from datetime import date
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from locadora import dados, estilo, regras
from locadora.formato import em_reais

# as cores das fatias, sempre nesta ordem: a 1ª fatia é sempre azul, a 2ª
# laranja... Conferidas no validador de paleta para quem não enxerga cor
# (daltonismo). Três delas ficam abaixo de 3:1 sobre o branco, e por isso
# cada fatia tem o nome e o número escritos do lado de fora.
CORES_DA_PIZZA = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]


class AbaResumo(ttk.Frame):
    def __init__(self, pai, conexao):
        super().__init__(pai, padding=16)
        self.conexao = conexao

        # os três números de cima
        numeros = ttk.Frame(self)
        numeros.grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.numero_jogos = self.criar_numero(numeros, "jogos no acervo", 0)
        self.numero_abertos = self.criar_numero(numeros, "aluguéis em aberto", 1)
        self.numero_multa = self.criar_numero(numeros, "de multa a cobrar hoje", 2)

        # uma figura com dois gráficos lado a lado: 1 linha, 2 colunas.
        # "constrained" abre espaço para os rótulos; sem ele, o título do jogo
        # invade a barra
        self.figura = Figure(figsize=(11, 3.8), dpi=100, layout="constrained")
        self.pizza = self.figura.add_subplot(1, 2, 1)
        self.barras = self.figura.add_subplot(1, 2, 2)
        self.tela = FigureCanvasTkAgg(self.figura, master=self)
        self.tela.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.atualizar()

    def criar_numero(self, pai, texto, coluna):
        quadro = ttk.Frame(pai)
        quadro.grid(row=0, column=coluna, sticky="w", padx=(0, 56))
        numero = ttk.Label(quadro, style="Total.TLabel")
        numero.pack(anchor="w")
        ttk.Label(quadro, text=texto, style="Apoio.TLabel").pack(anchor="w")
        return numero

    def atualizar(self):
        abertos = dados.listar_alugueis_abertos(self.conexao)
        multa = 0
        configuracao = dados.ler_configuracao(self.conexao)
        for aluguel in regras.atrasados(abertos, date.today(), configuracao["multa_por_dia"], configuracao["multa_a_partir_do_dia"]):
            multa = multa + aluguel["multa"]
        self.numero_jogos.configure(text=str(dados.contar_jogos(self.conexao)))
        self.numero_abertos.configure(text=str(len(abertos)))
        self.numero_multa.configure(text=em_reais(multa))

        self.desenhar_pizza(regras.juntar_em_outros(dados.alugueis_por_genero(self.conexao)))
        self.desenhar_barras(dados.jogos_mais_alugados(self.conexao))
        self.tela.draw()

    def desenhar_pizza(self, generos):
        self.pizza.clear()
        self.pizza.set_title("Aluguéis por gênero", loc="left", fontsize=14, fontweight="bold")
        if not generos:
            self.pizza.text(0.5, 0.5, "Ainda não houve aluguel.", ha="center")
            self.pizza.axis("off")
            return
        nomes = [f"{genero} ({quantidade})" for genero, quantidade in generos]
        quantidades = [quantidade for genero, quantidade in generos]
        self.pizza.pie(
            quantidades,
            labels=nomes,                         # o nome fora da fatia, em preto
            labeldistance=1.12,
            colors=CORES_DA_PIZZA[:len(generos)],
            startangle=90, counterclock=False,    # começa no alto, gira como relógio
            wedgeprops={"edgecolor": estilo.BRANCO, "linewidth": 2},
            textprops={"fontsize": 12},
        )

    def desenhar_barras(self, jogos):
        self.barras.clear()
        self.barras.set_title("Jogos mais alugados", loc="left", fontsize=14, fontweight="bold")
        if not jogos:
            self.barras.text(0.5, 0.5, "Ainda não houve aluguel.", ha="center")
            self.barras.axis("off")
            return
        titulos = [titulo for titulo, vezes in jogos]
        vezes = [quantas for titulo, quantas in jogos]
        barras = self.barras.barh(titulos, vezes, color=estilo.LARANJA)
        self.barras.invert_yaxis()           # o mais alugado em cima
        self.barras.bar_label(barras, padding=6, fontsize=12)   # o número na ponta
        self.barras.tick_params(labelsize=12, length=0)
        self.barras.set_xticks([])           # o número já está escrito: sem régua
        for lado in ("top", "right", "bottom"):
            self.barras.spines[lado].set_visible(False)
