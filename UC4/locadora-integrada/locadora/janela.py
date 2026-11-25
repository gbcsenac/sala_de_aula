# janela.py — a janela da locadora: o cabeçalho e as seis abas.
#
# Cada aba mora no seu arquivo (aba_resumo, aba_jogos, aba_clientes,
# aba_alugueis, aba_atrasados e aba_configuracoes) e só fala com a regras.py e a dados.py. Aqui elas só são
# montadas lado a lado.

import sys
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from locadora import dados, estilo
from locadora.formato import em_data
from locadora.aba_alugueis import AbaAlugueis
from locadora.aba_atrasados import AbaAtrasados
from locadora.aba_clientes import AbaClientes
from locadora.aba_configuracoes import AbaConfiguracoes
from locadora.aba_jogos import AbaJogos
from locadora.aba_resumo import AbaResumo

if sys.platform == "win32":
    # Sem isto, no Windows com a tela em 125% ou 150%, o sistema amplia a
    # janela como se fosse uma foto, e a letra fica borrada. Com isto, o
    # Tkinter desenha no tamanho certo da tela.
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


class JanelaDaLocadora(tk.Tk):
    def __init__(self, conexao):
        super().__init__()
        self.conexao = conexao
        self.geometry("1180x640")
        self.minsize(980, 560)
        estilo.aplicar(self)

        # a faixa laranja com o nome, texto preto em cima (6,20:1). O nome e o
        # telefone vêm da tela Configurações
        faixa = tk.Frame(self, background=estilo.LARANJA, padx=20, pady=12)
        faixa.pack(fill="x")
        self.rotulo_nome = tk.Label(faixa, background=estilo.LARANJA, foreground=estilo.PRETO,
                                    font=("TkDefaultFont", 22, "bold"))
        self.rotulo_nome.pack(side="left")
        self.rotulo_telefone = tk.Label(faixa, background=estilo.LARANJA, foreground=estilo.PRETO,
                                        font=("TkDefaultFont", 13))
        self.rotulo_telefone.pack(side="left", padx=14, pady=(8, 0))
        # o atraso depende do dia de hoje: a atendente confere aqui
        tk.Label(faixa, text="hoje, " + em_data(date.today()), background=estilo.LARANJA,
                 foreground=estilo.PRETO, font=("TkDefaultFont", 13, "bold")).pack(side="right")
        self.atualizar_cabecalho()

        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True, padx=16, pady=16)
        self.paginas = [AbaResumo(abas, conexao), AbaJogos(abas, conexao), AbaClientes(abas, conexao),
                        AbaAlugueis(abas, conexao), AbaAtrasados(abas, conexao), AbaConfiguracoes(abas, conexao)]
        nomes = ("Resumo", "Jogos", "Clientes", "Aluguéis", "Atrasados", "Configurações")
        for pagina, nome in zip(self.paginas, nomes):
            abas.add(pagina, text=nome)

        # ao trocar de aba, ela relê o banco: o jogo cadastrado em Jogos já
        # aparece em Aluguéis, a devolução já some de Atrasados, e o nome
        # salvo em Configurações já está no cabeçalho
        abas.bind("<<NotebookTabChanged>>", lambda evento: self.trocou_de_aba(abas.index("current")))

    def report_callback_exception(self, tipo, erro, rastro):
        """O Tkinter chama isto quando um botão dá um erro que ninguém tratou.

        Sem isto, o erro sairia só no terminal, que a atendente nem vê, e o
        botão pareceria não fazer nada: o erro engolido da Aula 03. Os erros
        que a gente conhece (título repetido, jogo já alugado) já viram aviso
        em cada aba; este é o que sobra, e por isso o texto é o técnico.
        """
        # desfaz o que ficou pela metade: com a transação abortada, toda
        # consulta seguinte também falharia, e a janela inteira travaria
        self.conexao.rollback()
        messagebox.showerror("Algo deu errado", f"O sistema não conseguiu terminar:\n\n{erro}", parent=self)

    def trocou_de_aba(self, numero):
        self.atualizar_cabecalho()
        self.paginas[numero].atualizar()

    def atualizar_cabecalho(self):
        configuracao = dados.ler_configuracao(self.conexao)
        self.title(configuracao["nome_da_locadora"] + " — balcão")
        self.rotulo_nome.configure(text=configuracao["nome_da_locadora"])
        self.rotulo_telefone.configure(text=configuracao["telefone_da_locadora"] or "")
