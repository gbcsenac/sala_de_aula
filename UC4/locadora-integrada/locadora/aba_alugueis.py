# aba_alugueis.py — a aba Aluguéis: alugar e registrar a devolução.

from datetime import date
from tkinter import messagebox, ttk
import tkinter as tk

import psycopg2 as pg

from locadora import dados, regras
from locadora import estilo
from locadora.estilo import listrar
from locadora.formato import em_data, em_reais


class AbaAlugueis(ttk.Frame):
    def __init__(self, pai, conexao):
        super().__init__(pai, padding=16)
        self.conexao = conexao
        self.clientes = []      # os clientes, na ordem da caixa
        self.disponiveis = []   # os Jogo da lista, na mesma ordem
        self.abertos = {}       # id_emprestimo -> o aluguel, para a devolução

        self.montar_formulario()
        self.montar_tabela()
        self.atualizar()

    # ---------- montagem da tela ----------

    def montar_formulario(self):
        quadro = ttk.Frame(self)
        quadro.grid(row=0, column=0, sticky="n", padx=(0, 32))
        ttk.Label(quadro, text="Novo aluguel", style="Secao.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ttk.Label(quadro, text="Cliente").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 12))
        self.caixa_cliente = ttk.Combobox(quadro, state="readonly", width=24)
        self.caixa_cliente.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(quadro, text="Jogos").grid(row=2, column=0, sticky="nw", pady=5)
        # a lista do próprio tk (e não do ttk) é a que deixa escolher vários
        self.lista_jogos = tk.Listbox(quadro, selectmode="multiple", height=7, width=30,
                                      exportselection=False, activestyle="none",
                                      relief="solid", borderwidth=1, highlightthickness=0,
                                      selectbackground=estilo.LARANJA_CLARO, selectforeground=estilo.PRETO)
        self.lista_jogos.grid(row=2, column=1, sticky="w", pady=5)
        ttk.Label(quadro, text="Clique em cada jogo que vai levar", style="Apoio.TLabel").grid(row=3, column=1, sticky="w")

        ttk.Label(quadro, text="Dias").grid(row=4, column=0, sticky="w", pady=5)
        self.campo_dias = ttk.Entry(quadro, width=6)
        self.campo_dias.grid(row=4, column=1, sticky="w", pady=5)

        ttk.Button(quadro, text="Alugar", style="Principal.TButton", command=self.alugar).grid(
            row=5, column=1, sticky="w", pady=(16, 0)
        )

    def montar_tabela(self):
        lado = ttk.Frame(self)
        lado.grid(row=0, column=1, sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(lado, text="Jogos com o cliente agora", style="Secao.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.tabela = ttk.Treeview(lado, columns=("cliente", "jogos", "prazo"), show="headings")
        self.tabela.heading("cliente", text="Cliente", anchor="w")
        self.tabela.heading("jogos", text="Jogos", anchor="w")
        self.tabela.heading("prazo", text="Devolver até")
        self.tabela.column("cliente", width=170, stretch=False)
        self.tabela.column("jogos", width=220, stretch=True)
        self.tabela.column("prazo", width=160, stretch=False, anchor="center")
        self.tabela.grid(row=1, column=0, sticky="nsew")
        # com muitas linhas, a barra mostra que tem mais para baixo
        barra = ttk.Scrollbar(lado, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        barra.grid(row=1, column=1, sticky="ns")
        lado.columnconfigure(0, weight=1)
        lado.rowconfigure(1, weight=1)

        ttk.Button(lado, text="Registrar devolução", command=self.devolver).grid(
            row=2, column=0, sticky="e", pady=(12, 0)
        )

    # ---------- o que os botões fazem ----------

    def atualizar(self):
        # os dias que já vêm escritos saem da tela Configurações
        self.configuracao = dados.ler_configuracao(self.conexao)
        self.campo_dias.delete(0, "end")
        self.campo_dias.insert(0, str(self.configuracao["dias_padrao"]))

        self.clientes = dados.listar_clientes(self.conexao)
        self.caixa_cliente["values"] = [cliente["nome"] for cliente in self.clientes]

        self.disponiveis = dados.listar_jogos_disponiveis(self.conexao)
        self.lista_jogos.delete(0, "end")
        for jogo in self.disponiveis:
            self.lista_jogos.insert("end", f"{jogo.titulo} — {em_reais(jogo.preco_diaria)} a diária")

        self.abertos = {}
        self.tabela.delete(*self.tabela.get_children())
        for aluguel in dados.listar_alugueis_abertos(self.conexao):
            self.abertos[aluguel["id_emprestimo"]] = aluguel
            self.tabela.insert(
                "", "end", iid=str(aluguel["id_emprestimo"]),
                values=(aluguel["cliente"], aluguel["jogos"], em_data(aluguel["data_prevista"])),
            )
        listrar(self.tabela)

    def alugar(self):
        posicao = self.caixa_cliente.current()     # -1 quando ninguém foi escolhido
        id_cliente = self.clientes[posicao]["id_cliente"] if posicao >= 0 else None
        jogos = [self.disponiveis[i] for i in self.lista_jogos.curselection()]
        dias = self.campo_dias.get()

        problemas = regras.validar_aluguel(id_cliente, jogos, dias)
        if problemas:
            messagebox.showwarning("Confira o aluguel", "\n".join(problemas), parent=self)
            return

        hoje = date.today()
        itens, total = regras.itens_do_aluguel(jogos, int(dias))
        try:
            dados.alugar(self.conexao, id_cliente, itens, hoje, regras.data_prevista(hoje, int(dias)))
        except pg.errors.UniqueViolation:
            # a chave natural do empréstimo (UC2) é cliente + dia: um por dia
            messagebox.showerror(
                "Aluguel repetido",
                "Este cliente já tem um aluguel registrado hoje. Escolha todos os jogos de uma vez.",
                parent=self,
            )
            return
        messagebox.showinfo("Aluguel registrado", f"Total a cobrar: {em_reais(total)}", parent=self)
        self.caixa_cliente.set("")
        self.atualizar()

    def devolver(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showinfo("Devolução", "Escolha um aluguel na tabela primeiro.", parent=self)
            return
        aluguel = self.abertos[int(selecionado[0])]
        hoje = date.today()
        dias = regras.dias_de_atraso(aluguel["data_prevista"], hoje)
        multa = regras.multa(dias, self.configuracao["multa_por_dia"], self.configuracao["multa_a_partir_do_dia"])
        pergunta = f"{aluguel['cliente']} devolveu {aluguel['jogos']}?\n\nMulta: {em_reais(multa)}"
        if not messagebox.askyesno("Devolução", pergunta, parent=self):
            return
        dados.devolver(self.conexao, aluguel["id_emprestimo"], hoje, multa)
        self.atualizar()
