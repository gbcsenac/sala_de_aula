# aba_configuracoes.py — a aba Configurações: o que o dono muda sem
# chamar o programador.
#
# Os valores moram na tabela configuracao, que tem uma linha só. Esta aba lê
# essa linha, mostra nos campos e, ao salvar, grava a linha inteira de novo.

from tkinter import messagebox, ttk

from locadora import dados, regras


class AbaConfiguracoes(ttk.Frame):
    def __init__(self, pai, conexao):
        super().__init__(pai, padding=16)
        self.conexao = conexao

        quadro = ttk.Frame(self)
        quadro.grid(row=0, column=0, sticky="nw")
        quadro.columnconfigure(1, weight=1)

        ttk.Label(quadro, text="A locadora", style="Secao.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))
        self.campo_nome = self.criar_campo(quadro, "Nome", 1)
        self.campo_telefone = self.criar_campo(quadro, "Telefone", 2)

        ttk.Label(quadro, text="Multa e aluguel", style="Secao.TLabel").grid(row=3, column=0, columnspan=2, sticky="w", pady=(24, 12))
        self.campo_multa = self.criar_campo(quadro, "Multa por dia (R$)", 4)
        self.campo_a_partir = self.criar_campo(quadro, "A multa começa no dia", 5)
        self.campo_dias = self.criar_campo(quadro, "Dias de aluguel padrão", 6)
        # a frase que explica a multa muda a cada letra digitada nos dois campos
        self.explicacao = ttk.Label(quadro, style="Apoio.TLabel")
        self.explicacao.grid(row=7, column=0, columnspan=2, sticky="w", pady=(8, 0))
        for campo in (self.campo_multa, self.campo_a_partir):
            campo.bind("<KeyRelease>", lambda evento: self.explicar())

        ttk.Button(quadro, text="Salvar", style="Principal.TButton", command=self.salvar).grid(
            row=8, column=0, sticky="w", pady=(20, 0)
        )

        self.atualizar()

    def criar_campo(self, quadro, rotulo, linha):
        ttk.Label(quadro, text=rotulo).grid(row=linha, column=0, sticky="w", pady=5, padx=(0, 12))
        campo = ttk.Entry(quadro, width=24)
        campo.grid(row=linha, column=1, sticky="ew", pady=5)
        return campo

    def atualizar(self):
        configuracao = dados.ler_configuracao(self.conexao)
        valores = [
            (self.campo_nome, configuracao["nome_da_locadora"]),
            (self.campo_telefone, configuracao["telefone_da_locadora"] or ""),
            (self.campo_multa, str(configuracao["multa_por_dia"]).replace(".", ",")),
            (self.campo_a_partir, str(configuracao["multa_a_partir_do_dia"])),
            (self.campo_dias, str(configuracao["dias_padrao"])),
        ]
        for campo, valor in valores:
            campo.delete(0, "end")
            campo.insert(0, valor)
        self.explicar()

    def explicar(self):
        texto = regras.explicar_multa(self.campo_multa.get(), self.campo_a_partir.get())
        self.explicacao.configure(text=texto)

    def salvar(self):
        nome = self.campo_nome.get()
        multa = self.campo_multa.get()
        a_partir = self.campo_a_partir.get()
        dias = self.campo_dias.get()
        problemas = regras.validar_configuracao(nome, multa, a_partir, dias)
        if problemas:
            messagebox.showwarning("Confira as configurações", "\n".join(problemas), parent=self)
            return
        dados.salvar_configuracao(
            self.conexao, nome.strip(), self.campo_telefone.get().strip() or None,
            multa.replace(",", "."), int(a_partir), int(dias),
        )
        messagebox.showinfo("Configurações", "Salvo. A multa nova vale a partir da próxima devolução.", parent=self)
