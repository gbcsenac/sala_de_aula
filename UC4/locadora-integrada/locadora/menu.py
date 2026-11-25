# menu.py — o sistema inteiro no terminal: os mesmos menus para os dois
# jeitos de mostrar (texto puro ou rich).
#
# Como a janela, ele não tem regra nem SQL: pede à regras.py e à dados.py. O
# que ele não sabe é COMO mostrar: isso é da tela que ele recebe
# (TelaDeTexto ou TelaRich). As duas têm os mesmos métodos — tabela,
# perguntar, escolher, aviso... —, e o menu nem sabe qual das duas está usando.

from datetime import date

import psycopg2 as pg

from locadora import dados, regras
from locadora.formato import em_data, em_reais


class Menu:
    def __init__(self, conexao, tela):
        self.conexao = conexao
        self.tela = tela

    def rodar(self):
        opcoes = [
            ("Resumo", self.resumo),
            ("Jogos", self.jogos),
            ("Clientes", self.clientes),
            ("Aluguéis", self.alugueis),
            ("Atrasados", self.atrasados),
            ("Configurações", self.configuracoes),
        ]
        while True:
            nome = dados.ler_configuracao(self.conexao)["nome_da_locadora"]
            escolha = self.tela.escolher(f"{nome} — hoje, {em_data(date.today())}", [n for n, f in opcoes], "Sair")
            if escolha is None:
                return
            try:
                opcoes[escolha][1]()
            except pg.DatabaseError as erro:
                # o erro que nenhuma opção tratou: avisa, em vez de derrubar o
                # sistema. O texto é o técnico do banco (defeito conhecido)
                self.conexao.rollback()
                self.tela.aviso(f"O sistema não conseguiu terminar: {erro}")

    # ---------- ajudantes ----------

    def numero_da_lista(self, pergunta, tamanho):
        """Pede um número da lista mostrada. Devolve a posição (0, 1, ...) ou None."""
        texto = self.tela.perguntar(pergunta)
        if not texto.strip().isdigit() or not 1 <= int(texto) <= tamanho:
            self.tela.aviso(f"Escreva um número de 1 a {tamanho}.")
            return None
        return int(texto) - 1

    def multa_configurada(self):
        configuracao = dados.ler_configuracao(self.conexao)
        return configuracao["multa_por_dia"], configuracao["multa_a_partir_do_dia"]

    # ---------- Resumo ----------

    def resumo(self):
        abertos = dados.listar_alugueis_abertos(self.conexao)
        multa = 0
        valor, a_partir = self.multa_configurada()
        for aluguel in regras.atrasados(abertos, date.today(), valor, a_partir):
            multa = multa + aluguel["multa"]
        self.tela.numeros([
            (str(dados.contar_jogos(self.conexao)), "jogos no acervo"),
            (str(len(abertos)), "aluguéis em aberto"),
            (em_reais(multa), "de multa a cobrar hoje"),
        ])

        generos = regras.juntar_em_outros(dados.alugueis_por_genero(self.conexao))
        total = sum(quantidade for genero, quantidade in generos)
        linhas = [(g, q, f"{q} ({round(100 * q / total)}%)") for g, q in generos]
        self.tela.barras("Aluguéis por gênero", linhas, total)

        jogos = dados.jogos_mais_alugados(self.conexao)
        linhas = [(t, v, "1 vez" if v == 1 else f"{v} vezes") for t, v in jogos]
        self.tela.barras("Jogos mais alugados", linhas, jogos[0][1] if jogos else 0)
        self.tela.pausar()

    # ---------- Jogos ----------

    def jogos(self):
        opcoes = [("Ver e buscar", self.ver_jogos), ("Cadastrar", self.cadastrar_jogo),
                  ("Alterar", self.alterar_jogo), ("Apagar", self.apagar_jogo)]
        while True:
            escolha = self.tela.escolher("Jogos", [n for n, f in opcoes], "Voltar")
            if escolha is None:
                return
            opcoes[escolha][1]()

    def mostrar_jogos(self, jogos):
        linhas = []
        for numero, jogo in enumerate(jogos, start=1):
            linhas.append([str(numero), jogo.titulo, jogo.genero or "",
                           str(jogo.ano_lancamento or ""), em_reais(jogo.preco_diaria)])
        self.tela.tabela("Jogos", ["Nº", "Título", "Gênero", "Ano", "Diária"], linhas)

    def ver_jogos(self):
        busca = self.tela.perguntar("Buscar pelo título (Enter mostra todos)")
        self.mostrar_jogos(dados.listar_jogos(self.conexao, busca.strip()))
        self.tela.pausar()

    def escolher_jogo(self):
        jogos = dados.listar_jogos(self.conexao)
        self.mostrar_jogos(jogos)
        posicao = self.numero_da_lista("Número do jogo", len(jogos))
        return None if posicao is None else jogos[posicao]

    def ler_jogo(self, titulo="", genero="", ano="", preco=""):
        """Pergunta os quatro campos; Enter mantém o que já estava."""
        problemas, valores = regras.preparar_jogo(
            self.tela.perguntar("Título", titulo), self.tela.perguntar("Gênero", genero),
            self.tela.perguntar("Ano", ano), self.tela.perguntar("Diária (R$)", preco),
        )
        if problemas:
            self.tela.aviso("\n".join(problemas))
        return valores

    def cadastrar_jogo(self):
        valores = self.ler_jogo()
        if valores is None:
            return
        titulo, genero, ano, preco = valores
        try:
            dados.criar_jogo(self.conexao, titulo, genero, ano, preco)
        except pg.errors.UniqueViolation:
            self.tela.aviso("Já existe um jogo com esse título.")
            return
        self.tela.sucesso(f"{titulo} cadastrado.")

    def alterar_jogo(self):
        jogo = self.escolher_jogo()
        if jogo is None:
            return
        valores = self.ler_jogo(jogo.titulo, jogo.genero or "", str(jogo.ano_lancamento or ""),
                                str(jogo.preco_diaria).replace(".", ","))
        if valores is None:
            return
        titulo, genero, ano, preco = valores
        try:
            dados.atualizar_jogo(self.conexao, jogo.id_jogo, titulo, genero, ano, preco)
        except pg.errors.UniqueViolation:
            self.tela.aviso("Já existe outro jogo com esse título.")
            return
        self.tela.sucesso(f"{titulo} alterado.")

    def apagar_jogo(self):
        jogo = self.escolher_jogo()
        if jogo is None or not self.tela.confirmar(f"Apagar {jogo.titulo}?"):
            return
        try:
            dados.deletar_jogo(self.conexao, jogo.id_jogo)
        except pg.errors.ForeignKeyViolation:
            self.tela.aviso(f"{jogo.titulo} já foi alugado, e o histórico dos aluguéis precisa dele.")
            return
        self.tela.sucesso(f"{jogo.titulo} apagado.")

    # ---------- Clientes ----------

    def clientes(self):
        opcoes = [("Ver e buscar", self.ver_clientes), ("Cadastrar", self.cadastrar_cliente),
                  ("Alterar", self.alterar_cliente), ("Desativar", self.desativar_cliente)]
        while True:
            escolha = self.tela.escolher("Clientes", [n for n, f in opcoes], "Voltar")
            if escolha is None:
                return
            opcoes[escolha][1]()

    def mostrar_clientes(self, clientes):
        linhas = []
        for numero, cliente in enumerate(clientes, start=1):
            linhas.append([str(numero), cliente["nome"], cliente["telefone"] or "", cliente["email"] or ""])
        self.tela.tabela("Clientes", ["Nº", "Nome", "Telefone", "E-mail"], linhas)

    def ver_clientes(self):
        busca = self.tela.perguntar("Buscar pelo nome (Enter mostra todos)")
        self.mostrar_clientes(dados.listar_clientes(self.conexao, busca.strip()))
        self.tela.pausar()

    def escolher_cliente(self):
        clientes = dados.listar_clientes(self.conexao)
        self.mostrar_clientes(clientes)
        posicao = self.numero_da_lista("Número do cliente", len(clientes))
        return None if posicao is None else clientes[posicao]

    def ler_cliente(self, nome="", telefone="", email=""):
        problemas, valores = regras.preparar_cliente(
            self.tela.perguntar("Nome", nome), self.tela.perguntar("Telefone", telefone),
            self.tela.perguntar("E-mail", email),
        )
        if problemas:
            self.tela.aviso("\n".join(problemas))
        return valores

    def cadastrar_cliente(self):
        valores = self.ler_cliente()
        if valores is None:
            return
        nome, telefone, email = valores
        try:
            dados.criar_cliente(self.conexao, nome, telefone, email)
        except pg.errors.UniqueViolation:
            self.tela.aviso("Já existe um cliente com esse e-mail, ou com esse nome e telefone.")
            return
        self.tela.sucesso(f"{nome} cadastrado.")

    def alterar_cliente(self):
        cliente = self.escolher_cliente()
        if cliente is None:
            return
        valores = self.ler_cliente(cliente["nome"], cliente["telefone"] or "", cliente["email"] or "")
        if valores is None:
            return
        nome, telefone, email = valores
        try:
            dados.atualizar_cliente(self.conexao, cliente["id_cliente"], nome, telefone, email)
        except pg.errors.UniqueViolation:
            self.tela.aviso("Já existe outro cliente com esse e-mail, ou com esse nome e telefone.")
            return
        self.tela.sucesso(f"{nome} alterado.")

    def desativar_cliente(self):
        cliente = self.escolher_cliente()
        if cliente is None:
            return
        pergunta = f"Desativar {cliente['nome']}? Ele sai das listas, mas os aluguéis antigos ficam."
        if not self.tela.confirmar(pergunta):
            return
        dados.desativar_cliente(self.conexao, cliente["id_cliente"])
        self.tela.sucesso(f"{cliente['nome']} desativado.")

    # ---------- Aluguéis ----------

    def alugueis(self):
        opcoes = [("Ver os aluguéis em aberto", self.ver_alugueis), ("Alugar", self.alugar),
                  ("Registrar devolução", self.devolver)]
        while True:
            escolha = self.tela.escolher("Aluguéis", [n for n, f in opcoes], "Voltar")
            if escolha is None:
                return
            opcoes[escolha][1]()

    def mostrar_alugueis(self, alugueis):
        linhas = []
        for numero, aluguel in enumerate(alugueis, start=1):
            linhas.append([str(numero), aluguel["cliente"], aluguel["jogos"], em_data(aluguel["data_prevista"])])
        self.tela.tabela("Jogos com o cliente agora", ["Nº", "Cliente", "Jogos", "Devolver até"], linhas)

    def ver_alugueis(self):
        self.mostrar_alugueis(dados.listar_alugueis_abertos(self.conexao))
        self.tela.pausar()

    def alugar(self):
        cliente = self.escolher_cliente()
        if cliente is None:
            return
        disponiveis = dados.listar_jogos_disponiveis(self.conexao)
        self.mostrar_jogos(disponiveis)
        # vários jogos de uma vez: "1, 3" leva o primeiro e o terceiro
        texto = self.tela.perguntar("Números dos jogos, separados por vírgula")
        jogos = []
        for parte in texto.split(","):
            if parte.strip().isdigit() and 1 <= int(parte) <= len(disponiveis):
                jogo = disponiveis[int(parte) - 1]
                # "1, 1" é o mesmo jogo duas vezes: o banco recusaria o item
                if jogo not in jogos:
                    jogos.append(jogo)
        dias = self.tela.perguntar("Dias", str(dados.ler_configuracao(self.conexao)["dias_padrao"]))

        problemas = regras.validar_aluguel(cliente["id_cliente"], jogos, dias)
        if problemas:
            self.tela.aviso("\n".join(problemas))
            return
        hoje = date.today()
        itens, total = regras.itens_do_aluguel(jogos, int(dias))
        try:
            dados.alugar(self.conexao, cliente["id_cliente"], itens, hoje, regras.data_prevista(hoje, int(dias)))
        except pg.errors.UniqueViolation:
            self.tela.aviso("Este cliente já tem um aluguel registrado hoje. Escolha todos os jogos de uma vez.")
            return
        self.tela.sucesso(f"Aluguel registrado. Total a cobrar: {em_reais(total)}")

    def devolver(self):
        abertos = dados.listar_alugueis_abertos(self.conexao)
        self.mostrar_alugueis(abertos)
        posicao = self.numero_da_lista("Número do aluguel", len(abertos))
        if posicao is None:
            return
        aluguel = abertos[posicao]
        hoje = date.today()
        valor, a_partir = self.multa_configurada()
        multa = regras.multa(regras.dias_de_atraso(aluguel["data_prevista"], hoje), valor, a_partir)
        if not self.tela.confirmar(f"{aluguel['cliente']} devolveu {aluguel['jogos']}? Multa: {em_reais(multa)}"):
            return
        dados.devolver(self.conexao, aluguel["id_emprestimo"], hoje, multa)
        self.tela.sucesso("Devolução registrada.")

    # ---------- Atrasados ----------

    def atrasados(self):
        valor, a_partir = self.multa_configurada()
        lista = regras.atrasados(dados.listar_alugueis_abertos(self.conexao), date.today(), valor, a_partir)
        if not lista:
            # aparece no alto do menu, logo depois da limpeza da tela
            self.tela.sucesso("Nenhum atraso hoje. Todos os jogos alugados estão dentro do prazo.")
            return
        linhas = []
        total = 0
        for aluguel in lista:
            linhas.append([aluguel["cliente"], aluguel["telefone"] or "", aluguel["jogos"],
                           em_data(aluguel["data_prevista"]), str(aluguel["dias"]), em_reais(aluguel["multa"])])
            total = total + aluguel["multa"]
        self.tela.numeros([(em_reais(total), "a cobrar hoje")])
        self.tela.tabela("Atrasados", ["Cliente", "Telefone", "Jogos", "Prazo", "Dias de atraso", "Multa"], linhas)
        self.tela.pausar()

    # ---------- Configurações ----------

    def configuracoes(self):
        atual = dados.ler_configuracao(self.conexao)
        self.tela.tabela("Configurações", ["O quê", "Valor"], [
            ["Nome", atual["nome_da_locadora"]],
            ["Telefone", atual["telefone_da_locadora"] or ""],
            ["Multa por dia", em_reais(atual["multa_por_dia"])],
            ["A multa começa no dia", str(atual["multa_a_partir_do_dia"])],
            ["Dias de aluguel padrão", str(atual["dias_padrao"])],
        ])
        if not self.tela.confirmar("Alterar?"):
            return
        nome = self.tela.perguntar("Nome", atual["nome_da_locadora"])
        telefone = self.tela.perguntar("Telefone", atual["telefone_da_locadora"] or "")
        multa = self.tela.perguntar("Multa por dia (R$)", str(atual["multa_por_dia"]).replace(".", ","))
        a_partir = self.tela.perguntar("A multa começa no dia", str(atual["multa_a_partir_do_dia"]))
        self.tela.nota(regras.explicar_multa(multa, a_partir))
        dias = self.tela.perguntar("Dias de aluguel padrão", str(atual["dias_padrao"]))

        problemas = regras.validar_configuracao(nome, multa, a_partir, dias)
        if problemas:
            self.tela.aviso("\n".join(problemas))
            return
        dados.salvar_configuracao(self.conexao, nome.strip(), telefone.strip() or None,
                                  multa.replace(",", "."), int(a_partir), int(dias))
        self.tela.sucesso("Salvo. A multa nova vale a partir da próxima devolução.")
