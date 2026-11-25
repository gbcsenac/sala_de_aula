# dados_peewee.py — o mesmo acesso ao banco do dados.py, escrito com o Peewee.
#
# É para COMPARAR, lado a lado com o dados.py: as mesmas funções, com os
# mesmos parâmetros e o mesmo retorno, e a mesma suíte de testes passa nas
# duas. O sistema usa o dados.py; este arquivo é o opcional da Aula 03.
#
# O que muda: em vez de escrever o SQL, cada tabela vira uma classe (o
# Model), e o Peewee escreve o SQL a partir dela. O que não muda: as tabelas
# são as mesmas do criar_tabelas.sql. O Peewee não as cria; só as usa.
#
# Cada função recebe a conexao, como no dados.py, para as duas terem a mesma
# cara e a mesma suíte de testes. Aqui ela quase não é usada: o Model já
# sabe o banco, que o conectar() ligou. Só o atomic() precisa dela.
#
# Uma diferença que aparece nos testes: quando o banco recusa, o Peewee
# avisa com o erro dele (peewee.IntegrityError), e não com o do psycopg2.

from peewee import (
    AutoField, BooleanField, CharField, CompositeKey, DatabaseProxy, DateField,
    DecimalField, ForeignKeyField, IntegerField, Model, PostgresqlDatabase, fn,
)

from locadora.conexao import dados_de_conexao

# o banco de verdade só é conhecido no conectar(); até lá, um "lugar guardado"
banco = DatabaseProxy()


def conectar(banco_da_variavel="PG_BANCO"):
    """A mesma leitura do .env da conexao.py, devolvendo o banco do Peewee."""
    parametros = dados_de_conexao(banco_da_variavel)
    conexao = PostgresqlDatabase(
        parametros["dbname"], user=parametros["user"], password=parametros["password"],
        host=parametros["host"], port=parametros["port"],
    )
    banco.initialize(conexao)
    return conexao


# ---------- as tabelas, como classes ----------

class Base(Model):
    class Meta:
        database = banco


class Plataforma(Base):
    id_plataforma = AutoField()
    nome = CharField(unique=True)
    fabricante = CharField(null=True)

    class Meta:
        table_name = "plataforma"


class Jogo(Base):
    # no dados.py, a classe Jogo e o _linha_para_jogo são escritos à mão;
    # aqui, o model já é o Jogo
    id_jogo = AutoField()
    titulo = CharField(unique=True)
    genero = CharField(null=True)
    ano_lancamento = IntegerField(null=True)
    preco_diaria = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = "jogo"


class JogosPlataforma(Base):
    jogo = ForeignKeyField(Jogo, column_name="id_jogo")
    plataforma = ForeignKeyField(Plataforma, column_name="id_plataforma")

    class Meta:
        table_name = "jogos_plataforma"
        primary_key = CompositeKey("jogo", "plataforma")


class Cliente(Base):
    id_cliente = AutoField()
    nome = CharField()
    telefone = CharField(null=True)
    email = CharField(null=True, unique=True)
    data_cadastro = DateField(null=True)   # o banco preenche (DEFAULT)
    ativo = BooleanField(null=True)        # o banco preenche (DEFAULT TRUE)

    class Meta:
        table_name = "cliente"


class Emprestimo(Base):
    id_emprestimo = AutoField()
    cliente = ForeignKeyField(Cliente, column_name="id_cliente")
    data_retirada = DateField()
    data_prevista = DateField()
    data_entregue = DateField(null=True)
    multa = DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        table_name = "emprestimo"


class ItemEmprestimo(Base):
    emprestimo = ForeignKeyField(Emprestimo, column_name="id_emprestimo")
    jogo = ForeignKeyField(Jogo, column_name="id_jogo")
    preco_pago = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = "item_emprestimo"
        primary_key = CompositeKey("emprestimo", "jogo")


class Configuracao(Base):
    id = IntegerField(primary_key=True)
    nome_da_locadora = CharField()
    telefone_da_locadora = CharField(null=True)
    multa_por_dia = DecimalField(max_digits=10, decimal_places=2)
    multa_a_partir_do_dia = IntegerField()
    dias_padrao = IntegerField()

    class Meta:
        table_name = "configuracao"


# ---------- jogos ----------

def criar_jogo(conexao, titulo, genero, ano_lancamento, preco_diaria):
    """Grava o jogo e devolve-o com o id."""
    return Jogo.create(titulo=titulo, genero=genero, ano_lancamento=ano_lancamento,
                       preco_diaria=preco_diaria)


def atualizar_jogo(conexao, id_jogo, titulo, genero, ano_lancamento, preco_diaria):
    """Troca os dados do jogo. True se achou o jogo."""
    linhas = (Jogo.update(titulo=titulo, genero=genero, ano_lancamento=ano_lancamento,
                          preco_diaria=preco_diaria)
              .where(Jogo.id_jogo == id_jogo)
              .execute())
    return linhas > 0


def listar_jogos(conexao, busca=""):
    """Os jogos em ordem de título. Com busca, só os que têm o texto no título."""
    # contains() vira o ILIKE '%...%' do dados.py
    return list(Jogo.select().where(Jogo.titulo.contains(busca)).order_by(Jogo.titulo))


def buscar_jogo(conexao, id_jogo):
    return Jogo.get_or_none(Jogo.id_jogo == id_jogo)


def deletar_jogo(conexao, id_jogo):
    """Apaga o jogo e o vínculo dele com as plataformas. True se apagou."""
    # atomic(): os dois DELETE de uma vez só, ou nenhum — o commit/rollback
    # que o dados.py escreve à mão
    with conexao.atomic():
        JogosPlataforma.delete().where(JogosPlataforma.jogo == id_jogo).execute()
        linhas = Jogo.delete().where(Jogo.id_jogo == id_jogo).execute()
    return linhas > 0


def listar_jogos_disponiveis(conexao):
    """Os jogos que não estão na casa de ninguém agora."""
    na_casa_de_alguem = (ItemEmprestimo.select(ItemEmprestimo.jogo)
                         .join(Emprestimo)
                         .where(Emprestimo.data_entregue.is_null()))
    return list(Jogo.select().where(Jogo.id_jogo.not_in(na_casa_de_alguem)).order_by(Jogo.titulo))


# ---------- clientes ----------

def criar_cliente(conexao, nome, telefone, email):
    Cliente.create(nome=nome, telefone=telefone, email=email)


def atualizar_cliente(conexao, id_cliente, nome, telefone, email):
    linhas = (Cliente.update(nome=nome, telefone=telefone, email=email)
              .where(Cliente.id_cliente == id_cliente)
              .execute())
    return linhas > 0


def desativar_cliente(conexao, id_cliente):
    Cliente.update(ativo=False).where(Cliente.id_cliente == id_cliente).execute()


def listar_clientes(conexao, busca=""):
    """Os clientes ativos, em ordem de nome, cada um como dicionário."""
    consulta = (Cliente.select(Cliente.id_cliente, Cliente.nome, Cliente.telefone, Cliente.email)
                .where(Cliente.ativo & Cliente.nome.contains(busca))
                .order_by(Cliente.nome))
    return list(consulta.dicts())   # dicts(): cada linha já vem como dicionário


# ---------- aluguéis ----------

def alugar(conexao, id_cliente, itens, data_retirada, data_prevista):
    """Registra o aluguel. itens é a lista de (id_jogo, preco_pago)."""
    with conexao.atomic():
        # o create devolve o empréstimo já com o id: o item usa direto, sem a
        # subconsulta que o dados.py precisa
        emprestimo = Emprestimo.create(cliente=id_cliente, data_retirada=data_retirada,
                                       data_prevista=data_prevista)
        for id_jogo, preco_pago in itens:
            ItemEmprestimo.create(emprestimo=emprestimo, jogo=id_jogo, preco_pago=preco_pago)


def listar_alugueis_abertos(conexao):
    """Os aluguéis com jogo ainda na casa do cliente, do prazo mais antigo ao
    mais novo. Cada um é um dicionário, com o nome de cada coluna."""
    consulta = (ItemEmprestimo.select(ItemEmprestimo, Emprestimo, Cliente, Jogo)
                .join(Emprestimo).join(Cliente)
                .switch(ItemEmprestimo).join(Jogo)
                .where(Emprestimo.data_entregue.is_null())
                .order_by(Emprestimo.data_prevista, Cliente.nome, Jogo.titulo))
    # uma linha por jogo; o dados.py junta os títulos no SQL (string_agg),
    # aqui eles são juntados em Python
    alugueis = {}
    for item in consulta:
        emprestimo = item.emprestimo
        if emprestimo.id_emprestimo not in alugueis:
            alugueis[emprestimo.id_emprestimo] = {
                "id_emprestimo": emprestimo.id_emprestimo,
                "cliente": emprestimo.cliente.nome,
                "telefone": emprestimo.cliente.telefone,
                "data_prevista": emprestimo.data_prevista,
                "jogos": [],
            }
        alugueis[emprestimo.id_emprestimo]["jogos"].append(item.jogo.titulo)
    for aluguel in alugueis.values():
        aluguel["jogos"] = ", ".join(aluguel["jogos"])
    return list(alugueis.values())


def devolver(conexao, id_emprestimo, data_entregue, multa):
    """Registra a devolução e guarda a multa cobrada."""
    (Emprestimo.update(data_entregue=data_entregue, multa=multa)
     .where(Emprestimo.id_emprestimo == id_emprestimo)
     .execute())


# ---------- números do resumo ----------

def contar_jogos(conexao):
    return Jogo.select().count()


def alugueis_por_genero(conexao):
    """[(gênero, quantos jogos desse gênero já saíram), ...], do maior ao menor."""
    genero = fn.COALESCE(Jogo.genero, "Sem gênero")
    quantos = fn.COUNT(ItemEmprestimo.jogo)
    consulta = (ItemEmprestimo.select(genero, quantos).join(Jogo)
                .group_by(genero).order_by(quantos.desc(), genero))
    return list(consulta.tuples())


def jogos_mais_alugados(conexao, quantos=5):
    """[(título, quantas vezes saiu), ...], do mais alugado ao menos."""
    vezes = fn.COUNT(ItemEmprestimo.jogo)
    consulta = (ItemEmprestimo.select(Jogo.titulo, vezes).join(Jogo)
                .group_by(Jogo.titulo).order_by(vezes.desc(), Jogo.titulo).limit(quantos))
    return list(consulta.tuples())


# ---------- configurações ----------

def ler_configuracao(conexao):
    """A linha única da tabela configuracao, como dicionário."""
    consulta = Configuracao.select(
        Configuracao.nome_da_locadora, Configuracao.telefone_da_locadora, Configuracao.multa_por_dia,
        Configuracao.multa_a_partir_do_dia, Configuracao.dias_padrao,
    ).where(Configuracao.id == 1)
    return consulta.dicts().get()


def salvar_configuracao(conexao, nome, telefone, multa_por_dia, a_partir_do_dia, dias_padrao):
    (Configuracao.update(nome_da_locadora=nome, telefone_da_locadora=telefone, multa_por_dia=multa_por_dia,
                         multa_a_partir_do_dia=a_partir_do_dia, dias_padrao=dias_padrao)
     .where(Configuracao.id == 1)
     .execute())
