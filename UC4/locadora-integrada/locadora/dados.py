# dados.py — o acesso ao banco: o SQL do sistema, e só ele.
#
# É o CRUD do notebook da UC2, já com a conexão por parâmetro (UC3, Aula 05).
# Cada função devolve o resultado, e não imprime nada: quem decide o que
# mostrar à pessoa é a janela. Toda função que grava termina com commit, e
# se o banco recusar, desfaz (rollback) e devolve o erro para cima.

from decimal import Decimal

import psycopg2 as pg


class Jogo:
    def __init__(self, titulo, genero, ano_lancamento, preco_diaria, id_jogo=None):
        self.id_jogo = id_jogo
        self.titulo = titulo
        self.genero = genero
        self.ano_lancamento = ano_lancamento
        self.preco_diaria = preco_diaria

    def __repr__(self):
        return f"Jogo( {self.id_jogo} - {self.titulo} )"


def _linha_para_jogo(linha):
    return Jogo(linha[1], linha[2], linha[3], linha[4], linha[0])


def _gravar(conexao, comandos):
    """Roda os comandos de uma vez só: ou grava todos, ou nenhum.

    Desfaz e devolve o erro para cima: a janela é que sabe avisar a pessoa;
    aqui embaixo, um print sumiria no terminal.
    """
    cursor = conexao.cursor()
    try:
        for sql, valores in comandos:
            cursor.execute(sql, valores)
        conexao.commit()
    except pg.DatabaseError:
        conexao.rollback()
        raise
    return cursor


# ---------- jogos ----------

def criar_jogo(conexao, titulo, genero, ano_lancamento, preco_diaria):
    """Grava o jogo e devolve-o com o id."""
    cursor = _gravar(conexao, [(
        "INSERT INTO jogo (titulo, genero, ano_lancamento, preco_diaria) "
        "VALUES (%s, %s, %s, %s) RETURNING id_jogo",
        (titulo, genero, ano_lancamento, preco_diaria),
    )])
    id_jogo = cursor.fetchone()[0]
    return Jogo(titulo, genero, ano_lancamento, Decimal(str(preco_diaria)), id_jogo)


def atualizar_jogo(conexao, id_jogo, titulo, genero, ano_lancamento, preco_diaria):
    """Troca os dados do jogo. True se achou o jogo."""
    cursor = _gravar(conexao, [(
        "UPDATE jogo SET titulo = %s, genero = %s, ano_lancamento = %s, preco_diaria = %s "
        "WHERE id_jogo = %s",
        (titulo, genero, ano_lancamento, preco_diaria, id_jogo),
    )])
    return cursor.rowcount > 0


def listar_jogos(conexao, busca=""):
    """Os jogos em ordem de título. Com busca, só os que têm o texto no título."""
    cursor = conexao.cursor()
    # ILIKE é o LIKE sem diferença entre maiúscula e minúscula; o % vai no
    # valor, e não no SQL, para a busca continuar passando pelo %s
    cursor.execute(
        "SELECT id_jogo, titulo, genero, ano_lancamento, preco_diaria "
        "FROM jogo WHERE titulo ILIKE %s ORDER BY titulo",
        ("%" + busca + "%",),
    )
    return [_linha_para_jogo(linha) for linha in cursor.fetchall()]


def buscar_jogo(conexao, id_jogo):
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id_jogo, titulo, genero, ano_lancamento, preco_diaria "
        "FROM jogo WHERE id_jogo = %s",
        (id_jogo,),
    )
    linha = cursor.fetchone()
    return _linha_para_jogo(linha) if linha else None


def deletar_jogo(conexao, id_jogo):
    """Apaga o jogo e o vínculo dele com as plataformas. True se apagou.

    Jogo que já foi alugado não sai: o item_emprestimo aponta para ele, e o
    banco recusa (ForeignKeyViolation). O histórico de aluguéis precisa dele.
    """
    cursor = _gravar(conexao, [
        ("DELETE FROM jogos_plataforma WHERE id_jogo = %s", (id_jogo,)),
        ("DELETE FROM jogo WHERE id_jogo = %s", (id_jogo,)),
    ])
    return cursor.rowcount > 0


def listar_jogos_disponiveis(conexao):
    """Os jogos que não estão na casa de ninguém agora."""
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id_jogo, titulo, genero, ano_lancamento, preco_diaria FROM jogo j "
        "WHERE NOT EXISTS ("
        "  SELECT 1 FROM item_emprestimo i "
        "  JOIN emprestimo e ON e.id_emprestimo = i.id_emprestimo "
        "  WHERE i.id_jogo = j.id_jogo AND e.data_entregue IS NULL"
        ") ORDER BY titulo"
    )
    return [_linha_para_jogo(linha) for linha in cursor.fetchall()]


# ---------- clientes ----------

def criar_cliente(conexao, nome, telefone, email):
    _gravar(conexao, [(
        "INSERT INTO cliente (nome, telefone, email) VALUES (%s, %s, %s)",
        (nome, telefone, email),
    )])


def atualizar_cliente(conexao, id_cliente, nome, telefone, email):
    cursor = _gravar(conexao, [(
        "UPDATE cliente SET nome = %s, telefone = %s, email = %s WHERE id_cliente = %s",
        (nome, telefone, email, id_cliente),
    )])
    return cursor.rowcount > 0


def desativar_cliente(conexao, id_cliente):
    """Tira o cliente das listas sem apagar: os aluguéis antigos apontam para
    ele, e o histórico não pode perder o dono."""
    _gravar(conexao, [("UPDATE cliente SET ativo = FALSE WHERE id_cliente = %s", (id_cliente,))])


def listar_clientes(conexao, busca=""):
    """Os clientes ativos, em ordem de nome, cada um como dicionário."""
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id_cliente, nome, telefone, email FROM cliente "
        "WHERE ativo AND nome ILIKE %s ORDER BY nome",
        ("%" + busca + "%",),
    )
    clientes = []
    for linha in cursor.fetchall():
        clientes.append({"id_cliente": linha[0], "nome": linha[1], "telefone": linha[2], "email": linha[3]})
    return clientes


# ---------- aluguéis ----------

def alugar(conexao, id_cliente, itens, data_retirada, data_prevista):
    """Registra o aluguel. itens é a lista de (id_jogo, preco_pago) que a
    regras.itens_do_aluguel montou."""
    comandos = [(
        "INSERT INTO emprestimo (id_cliente, data_retirada, data_prevista) "
        "VALUES (%s, %s, %s)",
        (id_cliente, data_retirada, data_prevista),
    )]
    # o item procura o empréstimo pela chave natural (cliente e dia), porque o
    # id dele ainda não existe quando a lista de comandos é montada
    for id_jogo, preco_pago in itens:
        comandos.append((
            "INSERT INTO item_emprestimo (id_emprestimo, id_jogo, preco_pago) "
            "SELECT id_emprestimo, %s, %s FROM emprestimo "
            "WHERE id_cliente = %s AND data_retirada = %s",
            (id_jogo, preco_pago, id_cliente, data_retirada),
        ))
    # tudo num commit só: o empréstimo sem os itens não pode ficar gravado
    _gravar(conexao, comandos)


def listar_alugueis_abertos(conexao):
    """Os aluguéis com jogo ainda na casa do cliente, do prazo mais antigo ao
    mais novo. Cada um é um dicionário, com o nome de cada coluna."""
    cursor = conexao.cursor()
    # string_agg junta os títulos do aluguel numa linha só: "Zelda, Mario Kart 8"
    cursor.execute(
        "SELECT e.id_emprestimo, c.nome, c.telefone, e.data_prevista, "
        "       string_agg(j.titulo, ', ' ORDER BY j.titulo) "
        "FROM emprestimo e "
        "JOIN cliente c         ON c.id_cliente = e.id_cliente "
        "JOIN item_emprestimo i ON i.id_emprestimo = e.id_emprestimo "
        "JOIN jogo j            ON j.id_jogo = i.id_jogo "
        "WHERE e.data_entregue IS NULL "
        "GROUP BY e.id_emprestimo, c.nome, c.telefone, e.data_prevista "
        "ORDER BY e.data_prevista, c.nome"
    )
    alugueis = []
    for linha in cursor.fetchall():
        alugueis.append({
            "id_emprestimo": linha[0],
            "cliente": linha[1],
            "telefone": linha[2],
            "data_prevista": linha[3],
            "jogos": linha[4],
        })
    return alugueis


def devolver(conexao, id_emprestimo, data_entregue, multa):
    """Registra a devolução e guarda a multa cobrada.

    A multa fica gravada (UC2, Aula 09): se a regra mudar no ano que vem, o
    que foi cobrado hoje não muda junto.
    """
    _gravar(conexao, [(
        "UPDATE emprestimo SET data_entregue = %s, multa = %s WHERE id_emprestimo = %s",
        (data_entregue, multa, id_emprestimo),
    )])


# ---------- números do resumo ----------

def contar_jogos(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM jogo")
    return cursor.fetchone()[0]


def alugueis_por_genero(conexao):
    """[(gênero, quantos jogos desse gênero já saíram), ...], do maior ao menor."""
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT COALESCE(j.genero, 'Sem gênero'), COUNT(*) "
        "FROM item_emprestimo i JOIN jogo j ON j.id_jogo = i.id_jogo "
        "GROUP BY 1 ORDER BY 2 DESC, 1"
    )
    return cursor.fetchall()


def jogos_mais_alugados(conexao, quantos=5):
    """[(título, quantas vezes saiu), ...], do mais alugado ao menos."""
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT j.titulo, COUNT(*) "
        "FROM item_emprestimo i JOIN jogo j ON j.id_jogo = i.id_jogo "
        "GROUP BY j.titulo ORDER BY 2 DESC, 1 LIMIT %s",
        (quantos,),
    )
    return cursor.fetchall()


# ---------- configurações ----------

def ler_configuracao(conexao):
    """A linha única da tabela configuracao, como dicionário."""
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome_da_locadora, telefone_da_locadora, multa_por_dia, "
        "multa_a_partir_do_dia, dias_padrao FROM configuracao WHERE id = 1"
    )
    linha = cursor.fetchone()
    return {
        "nome_da_locadora": linha[0],
        "telefone_da_locadora": linha[1],
        "multa_por_dia": linha[2],
        "multa_a_partir_do_dia": linha[3],
        "dias_padrao": linha[4],
    }


def salvar_configuracao(conexao, nome, telefone, multa_por_dia, a_partir_do_dia, dias_padrao):
    _gravar(conexao, [(
        "UPDATE configuracao SET nome_da_locadora = %s, telefone_da_locadora = %s, "
        "multa_por_dia = %s, multa_a_partir_do_dia = %s, dias_padrao = %s WHERE id = 1",
        (nome, telefone, multa_por_dia, a_partir_do_dia, dias_padrao),
    )])
