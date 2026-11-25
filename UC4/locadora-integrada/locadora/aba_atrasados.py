# aba_atrasados.py — a aba Atrasados: quem está com jogo vencido, e a multa.
#
# É a história que responde "como saber que resolveu": a atendente abre esta
# aba e vê, em segundos, quem cobrar e quanto.

from datetime import date
from tkinter import ttk

from locadora import dados, regras
from locadora.estilo import listrar
from locadora.formato import em_data, em_reais


class AbaAtrasados(ttk.Frame):
    def __init__(self, pai, conexao):
        super().__init__(pai, padding=16)
        self.conexao = conexao

        # o número grande: é a primeira coisa que a atendente procura
        self.rotulo_total = ttk.Label(self, style="Total.TLabel")
        self.rotulo_total.grid(row=0, column=0, sticky="w")
        self.rotulo_resumo = ttk.Label(self, style="Apoio.TLabel")
        self.rotulo_resumo.grid(row=1, column=0, sticky="w", pady=(0, 12))

        colunas = ("cliente", "telefone", "jogos", "prazo", "dias", "multa")
        self.tabela = ttk.Treeview(self, columns=colunas, show="headings")
        for coluna, titulo in zip(colunas, ("Cliente", "Telefone", "Jogos", "Prazo", "Dias de atraso", "Multa")):
            self.tabela.heading(coluna, text=titulo, anchor="w" if coluna in ("cliente", "telefone", "jogos") else "center")
        self.tabela.column("cliente", width=170, stretch=False)
        self.tabela.column("telefone", width=170, stretch=False)
        self.tabela.column("jogos", width=240, stretch=True)
        self.tabela.column("prazo", width=120, stretch=False, anchor="center")
        self.tabela.column("dias", width=175, stretch=False, anchor="center")
        self.tabela.column("multa", width=110, stretch=False, anchor="e")
        self.tabela.grid(row=2, column=0, sticky="nsew")
        # com muitas linhas, a barra mostra que tem mais para baixo
        barra = ttk.Scrollbar(self, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        barra.grid(row=2, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.atualizar()

    def atualizar(self):
        configuracao = dados.ler_configuracao(self.conexao)
        atrasados = regras.atrasados(dados.listar_alugueis_abertos(self.conexao), date.today(),
                                     configuracao["multa_por_dia"], configuracao["multa_a_partir_do_dia"])

        self.tabela.delete(*self.tabela.get_children())
        total = 0
        for aluguel in atrasados:
            self.tabela.insert("", "end", values=(
                aluguel["cliente"], aluguel["telefone"] or "", aluguel["jogos"],
                em_data(aluguel["data_prevista"]), aluguel["dias"], em_reais(aluguel["multa"]),
            ))
            total = total + aluguel["multa"]
        listrar(self.tabela)

        # sem ninguém atrasado, a tela diz isso, e não fica em branco
        if not atrasados:
            self.rotulo_total.configure(text="Nenhum atraso hoje")
            self.rotulo_resumo.configure(text="Todos os jogos alugados estão dentro do prazo.")
        else:
            self.rotulo_total.configure(text=f"Total a cobrar: {em_reais(total)}")
            quantos = "1 aluguel" if len(atrasados) == 1 else f"{len(atrasados)} aluguéis"
            self.rotulo_resumo.configure(text=f"{quantos} com o prazo vencido")
