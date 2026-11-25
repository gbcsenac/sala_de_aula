# estilo.py — as cores e as letras da janela.
#
# Fica num arquivo só para as três abas ficarem iguais: mudou aqui, muda em
# todas. O laranja é o do material do curso, e só aparece como FUNDO com texto
# preto em cima: preto sobre #f07300 dá 6,20:1. Texto branco sobre ele daria
# 2,93:1, abaixo do mínimo de 4,5:1 para ler.

from tkinter import font, ttk

LARANJA = "#f07300"
LARANJA_FORTE = "#ff8a1f"   # botão com o mouse em cima
LARANJA_CLARO = "#ffd9b3"   # a linha escolhida na tabela
CINZA_CLARO = "#f3f3f3"     # botão comum, cabeçalho da tabela, linha par
CINZA_BORDA = "#8a8a8a"     # contorno do campo de digitar: 3,4:1 sobre o branco
CINZA_TEXTO = "#4a4a4a"     # texto de apoio: 8,9:1 sobre o branco
BRANCO = "#ffffff"
PRETO = "#000000"


def aplicar(janela):
    # letra maior que o padrão do Tkinter (9 ou 10): a janela vai ser usada
    # no balcão e mostrada no projetor
    for nome in ("TkDefaultFont", "TkTextFont", "TkHeadingFont"):
        font.nametofont(nome).configure(size=13)

    janela.configure(background=BRANCO)
    estilo = ttk.Style(janela)
    # "clam" é o único tema que vem em todo Tkinter e aceita trocar a cor
    estilo.theme_use("clam")
    estilo.configure(".", background=BRANCO, foreground=PRETO)

    # sem moldura nem relevo: as bordas cinza de tudo eram o que deixava a
    # janela com cara de programa antigo
    plano = {"bordercolor": BRANCO, "lightcolor": BRANCO, "darkcolor": BRANCO}

    estilo.configure("TNotebook", borderwidth=0, tabmargins=(0, 0, 0, 0), **plano)
    estilo.configure("TNotebook.Tab", padding=(24, 10), background=CINZA_CLARO, **plano)
    # a aba aberta é a laranja, com texto preto
    estilo.map("TNotebook.Tab",
               background=[("selected", LARANJA)],
               lightcolor=[("selected", LARANJA)],
               # o clam dá à aba escolhida um espaçamento menor, e ela desce em
               # relação às outras; aqui ela fica com o mesmo das outras
               padding=[("selected", (24, 10))],
               expand=[("selected", (0, 0, 0, 0))])

    estilo.configure("Secao.TLabel", font=("TkDefaultFont", 16, "bold"))
    estilo.configure("Apoio.TLabel", foreground=CINZA_TEXTO)
    estilo.configure("Total.TLabel", font=("TkDefaultFont", 26, "bold"))

    estilo.configure("TEntry", padding=6, fieldbackground=BRANCO,
                     bordercolor=CINZA_BORDA, lightcolor=CINZA_BORDA, darkcolor=CINZA_BORDA)
    estilo.configure("TCombobox", padding=6, arrowsize=16,
                     bordercolor=CINZA_BORDA, lightcolor=CINZA_BORDA, darkcolor=CINZA_BORDA)
    # a caixa de escolher cliente é "readonly", e o clam a pinta de cinza,
    # como se estivesse desligada
    estilo.map("TCombobox", fieldbackground=[("readonly", BRANCO)],
               selectbackground=[("readonly", BRANCO)], selectforeground=[("readonly", PRETO)])
    # o campo onde se está digitando ganha contorno preto: o foco tem de se ver
    for campo in ("TEntry", "TCombobox"):
        estilo.map(campo, bordercolor=[("focus", PRETO)], lightcolor=[("focus", PRETO)])

    estilo.configure("TButton", padding=(16, 8), background=CINZA_CLARO, **plano)
    estilo.map("TButton", background=[("active", "#e2e2e2")], bordercolor=[("focus", PRETO)])
    # o botão principal de cada aba: o que a atendente mais aperta
    estilo.configure("Principal.TButton", background=LARANJA, font=("TkDefaultFont", 13, "bold"))
    estilo.map("Principal.TButton", background=[("active", LARANJA_FORTE)])

    # a barra de rolagem plana, sem o relevo cinza do Tkinter antigo
    estilo.configure("Vertical.TScrollbar", background=CINZA_CLARO, troughcolor=BRANCO,
                     arrowcolor=PRETO, gripcount=0, **plano)
    estilo.map("Vertical.TScrollbar", background=[("active", "#e2e2e2")])
    # e a seta da caixa de escolher cliente, no mesmo cinza dos botões
    estilo.configure("TCombobox", background=CINZA_CLARO, arrowcolor=PRETO)

    estilo.configure("Treeview", rowheight=34, borderwidth=0, **plano)
    estilo.configure("Treeview.Heading", padding=(8, 8), background=CINZA_CLARO,
                     font=("TkDefaultFont", 13, "bold"), relief="flat", **plano)
    estilo.map("Treeview.Heading", background=[("active", CINZA_CLARO)])
    estilo.map("Treeview", background=[("selected", LARANJA_CLARO)], foreground=[("selected", PRETO)])


def listrar(tabela):
    """Linha sim, linha não com fundo cinza: o olho não pula de linha."""
    tabela.tag_configure("par", background=CINZA_CLARO)
    for numero, linha in enumerate(tabela.get_children()):
        if numero % 2 == 1:
            tabela.item(linha, tags=("par",))
