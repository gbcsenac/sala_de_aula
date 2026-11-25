# aba_jogos.py — a aba Jogos: cadastrar, buscar, alterar e apagar.
#
# Esta camada não tem regra nem SQL. Ela pede à regras.py para conferir o que
# foi digitado e à dados.py para gravar; o que sobra aqui é só tela.

from tkinter import messagebox, ttk

import psycopg2 as pg

from locadora import dados, regras
from locadora.estilo import listrar
from locadora.formato import em_reais


class AbaJogos(ttk.Frame):
    def __init__(self, pai, conexao):
        super().__init__(pai, padding=16)
        self.conexao = conexao
        self.id_escolhido = None   # o jogo clicado na tabela, para alterar

        self.montar_formulario()
        self.montar_tabela()
        self.atualizar()

    # ---------- montagem da tela ----------

    def montar_formulario(self):
        quadro = ttk.Frame(self)
        quadro.grid(row=0, column=0, sticky="n", padx=(0, 32))
        ttk.Label(quadro, text="Cadastrar jogo", style="Secao.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.campo_titulo = self.criar_campo(quadro, "Título", 1)
        self.campo_genero = self.criar_campo(quadro, "Gênero", 2)
        self.campo_ano = self.criar_campo(quadro, "Ano", 3)
        self.campo_preco = self.criar_campo(quadro, "Diária (R$)", 4)

        quadro.columnconfigure(1, weight=1)
        botoes = ttk.Frame(quadro)
        botoes.grid(row=5, column=0, columnspan=2, sticky="w", pady=(16, 0))
        ttk.Button(botoes, text="Cadastrar", style="Principal.TButton", command=self.cadastrar).pack(side="left")
        ttk.Button(botoes, text="Salvar alteração", command=self.salvar_alteracao).pack(side="left", padx=8)
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left")

    def criar_campo(self, quadro, rotulo, linha):
        ttk.Label(quadro, text=rotulo).grid(row=linha, column=0, sticky="w", pady=5, padx=(0, 12))
        campo = ttk.Entry(quadro, width=24)
        campo.grid(row=linha, column=1, sticky="ew", pady=5)
        # Enter cadastra: quem digita não precisa ir até o mouse
        campo.bind("<Return>", lambda evento: self.cadastrar())
        return campo

    def montar_tabela(self):
        lado = ttk.Frame(self)
        lado.grid(row=0, column=1, sticky="nsew")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(lado, text="Buscar pelo título").grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.campo_busca = ttk.Entry(lado, width=26)
        self.campo_busca.grid(row=0, column=1, sticky="w", padx=12, pady=(0, 12))
        # a tabela filtra a cada letra digitada
        self.campo_busca.bind("<KeyRelease>", lambda evento: self.atualizar())

        self.tabela = ttk.Treeview(lado, columns=("titulo", "genero", "ano", "preco"), show="headings")
        self.tabela.heading("titulo", text="Título", anchor="w")
        self.tabela.heading("genero", text="Gênero", anchor="w")
        self.tabela.heading("ano", text="Ano")
        self.tabela.heading("preco", text="Diária")
        # o título estica; as outras têm largura fixa, para a Diária não sumir
        self.tabela.column("titulo", width=200, stretch=True)
        self.tabela.column("genero", width=120, stretch=False)
        self.tabela.column("ano", width=80, stretch=False, anchor="center")
        self.tabela.column("preco", width=120, stretch=False, anchor="e")
        self.tabela.grid(row=1, column=0, columnspan=2, sticky="nsew")
        # com muitas linhas, a barra mostra que tem mais para baixo
        barra = ttk.Scrollbar(lado, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        barra.grid(row=1, column=2, sticky="ns")
        self.tabela.bind("<<TreeviewSelect>>", lambda evento: self.escolher())
        lado.columnconfigure(1, weight=1)
        lado.rowconfigure(1, weight=1)

        ttk.Button(lado, text="Apagar o selecionado", command=self.apagar).grid(
            row=2, column=1, sticky="e", pady=(12, 0)
        )

    # ---------- o que os botões fazem ----------

    def atualizar(self):
        self.tabela.delete(*self.tabela.get_children())
        for jogo in dados.listar_jogos(self.conexao, self.campo_busca.get().strip()):
            self.tabela.insert(
                "", "end", iid=str(jogo.id_jogo),
                values=(jogo.titulo, jogo.genero or "", jogo.ano_lancamento or "", em_reais(jogo.preco_diaria)),
            )
        listrar(self.tabela)

    def ler_campos(self):
        """O que foi digitado, já conferido. None se a regra recusou."""
        problemas, valores = regras.preparar_jogo(
            self.campo_titulo.get(), self.campo_genero.get(), self.campo_ano.get(), self.campo_preco.get()
        )
        if problemas:
            messagebox.showwarning("Confira os dados", "\n".join(problemas), parent=self)
        return valores

    def cadastrar(self):
        campos = self.ler_campos()                       # 1. a regra confere
        if campos is None:
            return
        titulo, genero, ano, preco = campos
        try:
            dados.criar_jogo(self.conexao, titulo, genero, ano, preco)   # 2. os dados gravam
        except pg.errors.UniqueViolation:
            messagebox.showerror("Jogo repetido", "Já existe um jogo com esse título.", parent=self)
            return
        self.limpar()
        self.atualizar()                                 # 3. a tela mostra

    def escolher(self):
        """Clicou numa linha: o jogo vai para o formulário, pronto para alterar."""
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        self.id_escolhido = int(selecionado[0])
        jogo = dados.buscar_jogo(self.conexao, self.id_escolhido)
        self.preencher(jogo.titulo, jogo.genero or "", jogo.ano_lancamento or "", str(jogo.preco_diaria).replace(".", ","))

    def salvar_alteracao(self):
        if self.id_escolhido is None:
            messagebox.showinfo("Alterar", "Escolha um jogo na tabela primeiro.", parent=self)
            return
        campos = self.ler_campos()
        if campos is None:
            return
        titulo, genero, ano, preco = campos
        try:
            dados.atualizar_jogo(self.conexao, self.id_escolhido, titulo, genero, ano, preco)
        except pg.errors.UniqueViolation:
            messagebox.showerror("Jogo repetido", "Já existe outro jogo com esse título.", parent=self)
            return
        self.limpar()
        self.atualizar()

    def apagar(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showinfo("Apagar", "Escolha um jogo na tabela primeiro.", parent=self)
            return
        titulo = self.tabela.item(selecionado[0], "values")[0]
        if not messagebox.askyesno("Apagar", f"Apagar {titulo}?", parent=self):
            return
        try:
            dados.deletar_jogo(self.conexao, int(selecionado[0]))
        except pg.errors.ForeignKeyViolation:
            messagebox.showerror(
                "Não dá para apagar",
                f"{titulo} já foi alugado, e o histórico dos aluguéis precisa dele.",
                parent=self,
            )
            return
        self.limpar()
        self.atualizar()

    def limpar(self):
        self.id_escolhido = None
        self.preencher("", "", "", "")
        self.tabela.selection_remove(self.tabela.selection())

    def preencher(self, titulo, genero, ano, preco):
        for campo, valor in [(self.campo_titulo, titulo), (self.campo_genero, genero),
                             (self.campo_ano, ano), (self.campo_preco, preco)]:
            campo.delete(0, "end")
            campo.insert(0, valor)
