# aba_clientes.py — a aba Clientes: cadastrar, buscar, alterar e desativar.
#
# Tem a mesma forma da aba_jogos.py, de propósito: quem leu uma, lê a outra.
# A diferença é o último botão: cliente não se apaga, se desativa.

from tkinter import messagebox, ttk

import psycopg2 as pg

from locadora import dados, regras
from locadora.estilo import listrar


class AbaClientes(ttk.Frame):
    def __init__(self, pai, conexao):
        super().__init__(pai, padding=16)
        self.conexao = conexao
        self.id_escolhido = None   # o cliente clicado na tabela, para alterar
        self.clientes = {}         # id_cliente -> o cliente, como está na tabela

        self.montar_formulario()
        self.montar_tabela()
        self.atualizar()

    # ---------- montagem da tela ----------

    def montar_formulario(self):
        quadro = ttk.Frame(self)
        quadro.grid(row=0, column=0, sticky="n", padx=(0, 32))
        ttk.Label(quadro, text="Cadastrar cliente", style="Secao.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        self.campo_nome = self.criar_campo(quadro, "Nome", 1)
        self.campo_telefone = self.criar_campo(quadro, "Telefone", 2)
        self.campo_email = self.criar_campo(quadro, "E-mail", 3)

        quadro.columnconfigure(1, weight=1)
        botoes = ttk.Frame(quadro)
        botoes.grid(row=4, column=0, columnspan=2, sticky="w", pady=(16, 0))
        ttk.Button(botoes, text="Cadastrar", style="Principal.TButton", command=self.cadastrar).pack(side="left")
        ttk.Button(botoes, text="Salvar alteração", command=self.salvar_alteracao).pack(side="left", padx=8)
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left")

    def criar_campo(self, quadro, rotulo, linha):
        ttk.Label(quadro, text=rotulo).grid(row=linha, column=0, sticky="w", pady=5, padx=(0, 12))
        campo = ttk.Entry(quadro, width=24)
        campo.grid(row=linha, column=1, sticky="ew", pady=5)
        campo.bind("<Return>", lambda evento: self.cadastrar())
        return campo

    def montar_tabela(self):
        lado = ttk.Frame(self)
        lado.grid(row=0, column=1, sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(lado, text="Buscar pelo nome").grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.campo_busca = ttk.Entry(lado, width=26)
        self.campo_busca.grid(row=0, column=1, sticky="w", padx=12, pady=(0, 12))
        self.campo_busca.bind("<KeyRelease>", lambda evento: self.atualizar())

        self.tabela = ttk.Treeview(lado, columns=("nome", "telefone", "email"), show="headings")
        self.tabela.heading("nome", text="Nome", anchor="w")
        self.tabela.heading("telefone", text="Telefone", anchor="w")
        self.tabela.heading("email", text="E-mail", anchor="w")
        self.tabela.column("nome", width=170, stretch=True)
        self.tabela.column("telefone", width=170, stretch=False)
        self.tabela.column("email", width=200, stretch=True)
        self.tabela.grid(row=1, column=0, columnspan=2, sticky="nsew")
        # com muitas linhas, a barra mostra que tem mais para baixo
        barra = ttk.Scrollbar(lado, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        barra.grid(row=1, column=2, sticky="ns")
        self.tabela.bind("<<TreeviewSelect>>", lambda evento: self.escolher())
        lado.columnconfigure(1, weight=1)
        lado.rowconfigure(1, weight=1)

        ttk.Button(lado, text="Desativar o selecionado", command=self.desativar).grid(
            row=2, column=1, sticky="e", pady=(12, 0)
        )

    # ---------- o que os botões fazem ----------

    def atualizar(self):
        self.clientes = {}
        self.tabela.delete(*self.tabela.get_children())
        for cliente in dados.listar_clientes(self.conexao, self.campo_busca.get().strip()):
            self.clientes[cliente["id_cliente"]] = cliente
            self.tabela.insert(
                "", "end", iid=str(cliente["id_cliente"]),
                values=(cliente["nome"], cliente["telefone"] or "", cliente["email"] or ""),
            )
        listrar(self.tabela)

    def ler_campos(self):
        """O que foi digitado, já conferido. None se a regra recusou."""
        problemas, valores = regras.preparar_cliente(
            self.campo_nome.get(), self.campo_telefone.get(), self.campo_email.get()
        )
        if problemas:
            messagebox.showwarning("Confira os dados", "\n".join(problemas), parent=self)
        return valores

    def cadastrar(self):
        campos = self.ler_campos()
        if campos is None:
            return
        nome, telefone, email = campos
        try:
            dados.criar_cliente(self.conexao, nome, telefone, email)
        except pg.errors.UniqueViolation:
            messagebox.showerror("Cliente repetido", "Já existe um cliente com esse e-mail, ou com esse nome e telefone.", parent=self)
            return
        self.limpar()
        self.atualizar()

    def escolher(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        self.id_escolhido = int(selecionado[0])
        cliente = self.clientes[self.id_escolhido]
        self.preencher(cliente["nome"], cliente["telefone"] or "", cliente["email"] or "")

    def salvar_alteracao(self):
        if self.id_escolhido is None:
            messagebox.showinfo("Alterar", "Escolha um cliente na tabela primeiro.", parent=self)
            return
        campos = self.ler_campos()
        if campos is None:
            return
        nome, telefone, email = campos
        try:
            dados.atualizar_cliente(self.conexao, self.id_escolhido, nome, telefone, email)
        except pg.errors.UniqueViolation:
            messagebox.showerror("Cliente repetido", "Já existe outro cliente com esse e-mail, ou com esse nome e telefone.", parent=self)
            return
        self.limpar()
        self.atualizar()

    def desativar(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showinfo("Desativar", "Escolha um cliente na tabela primeiro.", parent=self)
            return
        nome = self.clientes[int(selecionado[0])]["nome"]
        pergunta = f"Desativar {nome}?\n\nEle sai das listas, mas os aluguéis antigos continuam guardados."
        if not messagebox.askyesno("Desativar", pergunta, parent=self):
            return
        dados.desativar_cliente(self.conexao, int(selecionado[0]))
        self.limpar()
        self.atualizar()

    def limpar(self):
        self.id_escolhido = None
        self.preencher("", "", "")
        self.tabela.selection_remove(self.tabela.selection())

    def preencher(self, nome, telefone, email):
        for campo, valor in [(self.campo_nome, nome), (self.campo_telefone, telefone), (self.campo_email, email)]:
            campo.delete(0, "end")
            campo.insert(0, valor)
