# regras.py — as regras do negócio da locadora.
#
# Nenhuma linha aqui sabe que existe banco ou janela. Por isso estas funções
# se testam com o pytest puro, em milissegundos (Aulas 01 a 03 da UC3).

from datetime import timedelta

from locadora.formato import em_reais

def multa(dias_atraso, valor_por_dia=5.00, a_partir_do_dia=3):
    """A partir do 3º dia de atraso, R$ 5,00 por dia — todos os dias.

    Os dois números vêm da tela Configurações; sem eles, valem os de fábrica,
    que são os da UC3.
    """
    if dias_atraso >= a_partir_do_dia:
        return dias_atraso * valor_por_dia
    # zero inteiro, e não 0.0: o valor do banco chega como Decimal, e somar
    # Decimal com float dá TypeError no total da aba Atrasados
    return 0


def valor_do_aluguel(diaria, dias):
    """A diária vezes os dias. Aluguel de zero dias, ou menos, não existe."""
    if dias <= 0:
        raise ValueError("o aluguel precisa ser de pelo menos 1 dia")
    return diaria * dias


def validar_jogo(titulo, ano, preco_diaria):
    """Confere o que a pessoa digitou antes de ir ao banco.

    Recebe o texto dos campos, como veio da tela, e devolve a lista de
    problemas em português — vazia quando está tudo certo. A janela mostra a
    lista; o banco nem é chamado.
    """
    problemas = []
    if not titulo.strip():
        problemas.append("O título não pode ficar em branco.")
    if ano.strip():
        if not ano.strip().isdigit():
            problemas.append("O ano tem de ser um número, como 2017.")
        elif int(ano) <= 1970:
            # a mesma regra do CHECK da tabela jogo (UC2, Aula 11): avisar
            # aqui é avisar em português, antes do erro do banco
            problemas.append("O ano tem de ser depois de 1970.")
    try:
        preco = float(preco_diaria.replace(",", "."))
    except ValueError:
        problemas.append("O preço da diária tem de ser um número, como 8,50.")
    else:
        if preco < 0:
            problemas.append("O preço da diária não pode ser negativo.")
    return problemas


def dias_de_atraso(data_prevista, hoje):
    """Quantos dias passaram do prazo. No dia do prazo, ainda não é atraso."""
    dias = (hoje - data_prevista).days
    if dias < 0:
        return 0
    return dias


def validar_aluguel(id_cliente, jogos_escolhidos, dias):
    """Confere o aluguel antes de ir ao banco, como o validar_jogo.

    Devolve a lista de problemas em português, vazia quando está tudo certo.
    """
    problemas = []
    if id_cliente is None:
        problemas.append("Escolha o cliente.")
    if not jogos_escolhidos:
        problemas.append("Escolha pelo menos um jogo.")
    if not dias.strip().isdigit():
        problemas.append("Os dias têm de ser um número, como 3.")
    elif int(dias) == 0:
        problemas.append("O aluguel precisa ser de pelo menos 1 dia.")
    return problemas


def itens_do_aluguel(jogos, dias):
    """Para cada Jogo, o (id_jogo, preço a cobrar). E o total, para o aviso."""
    itens = []
    total = 0
    for jogo in jogos:
        preco = valor_do_aluguel(jogo.preco_diaria, dias)
        itens.append((jogo.id_jogo, preco))
        total = total + preco
    return itens, total


def data_prevista(data_retirada, dias):
    return data_retirada + timedelta(days=dias)


def atrasados(alugueis, hoje, valor_por_dia=5.00, a_partir_do_dia=3):
    """Dos aluguéis abertos, só os com prazo vencido, com os dias e a multa."""
    lista = []
    for aluguel in alugueis:
        dias = dias_de_atraso(aluguel["data_prevista"], hoje)
        if dias > 0:
            aluguel["dias"] = dias
            aluguel["multa"] = multa(dias, valor_por_dia, a_partir_do_dia)
            lista.append(aluguel)
    return lista


def validar_cliente(nome, email):
    """Confere o cliente antes de ir ao banco. O telefone é livre: tem traço,
    parêntese e espaço, e cada um escreve de um jeito."""
    problemas = []
    if not nome.strip():
        problemas.append("O nome não pode ficar em branco.")
    if email.strip() and "@" not in email:
        problemas.append("O e-mail precisa ter @, como ana@exemplo.com.")
    return problemas


def juntar_em_outros(contagens, maximo=6):
    """Mais de 6 barras de gênero ninguém compara de olho: da 6ª em diante,
    vira "Outros".

    Recebe [(nome, quantidade), ...] do maior ao menor e devolve no mesmo
    formato, com no máximo `maximo` itens.
    """
    if len(contagens) <= maximo:
        return contagens
    primeiras = contagens[:maximo - 1]
    resto = 0
    for nome, quantidade in contagens[maximo - 1:]:
        resto = resto + quantidade
    return primeiras + [("Outros", resto)]


def validar_configuracao(nome, multa_por_dia, a_partir_do_dia, dias_padrao):
    """Confere a tela Configurações antes de ir ao banco."""
    problemas = []
    if not nome.strip():
        problemas.append("O nome da locadora não pode ficar em branco.")
    try:
        if float(multa_por_dia.replace(",", ".")) < 0:
            problemas.append("A multa por dia não pode ser negativa.")
    except ValueError:
        problemas.append("A multa por dia tem de ser um número, como 5,00.")
    if not a_partir_do_dia.strip().isdigit() or int(a_partir_do_dia) < 1:
        problemas.append("O dia em que a multa começa tem de ser 1 ou mais.")
    if not dias_padrao.strip().isdigit() or int(dias_padrao) < 1:
        problemas.append("Os dias de aluguel padrão têm de ser 1 ou mais.")
    return problemas


# ---------- do texto digitado para o banco ----------
#
# A janela e os dois terminais recebem tudo como texto. Estas funções conferem
# e convertem num lugar só, para as três telas gravarem igual.

def preparar_jogo(titulo, genero, ano, preco_diaria):
    """(problemas, valores): valores é o que o dados.criar_jogo recebe, ou
    None se algum problema impediu."""
    problemas = validar_jogo(titulo, ano, preco_diaria)
    if problemas:
        return problemas, None
    ano = int(ano) if ano.strip() else None
    return [], (titulo.strip(), genero.strip() or None, ano, preco_diaria.replace(",", "."))


def preparar_cliente(nome, telefone, email):
    problemas = validar_cliente(nome, email)
    if problemas:
        return problemas, None
    # campo vazio vai como NULL, e não como texto vazio: o UNIQUE do e-mail
    # aceita vários NULL, mas recusaria dois clientes com e-mail ""
    return [], (nome.strip(), telefone.strip() or None, email.strip() or None)


def explicar_multa(valor_por_dia, a_partir_do_dia):
    """A frase da tela Configurações, com os números digitados.

    A própria multa() calcula o exemplo, e a frase nunca discorda do sistema.
    """
    try:
        valor = float(valor_por_dia.replace(",", "."))
    except ValueError:
        return "Escreva a multa por dia como um número, como 5,00."
    if not a_partir_do_dia.strip().isdigit() or int(a_partir_do_dia) < 1:
        return "Escreva o dia em que a multa começa, como 3."
    dia = int(a_partir_do_dia)
    por_dia = em_reais(valor)
    cobrado = em_reais(multa(dia, valor, dia))
    if dia == 1:
        return f"Com 1, qualquer atraso já paga: 1 dia custa {cobrado}."
    if dia == 2:
        return f"Com 2, quem atrasa 1 dia não paga multa; no 2º dia, paga 2 × {por_dia} = {cobrado}."
    return (f"Com {dia}, quem atrasa de 1 a {dia - 1} dias não paga multa; "
            f"no {dia}º dia, paga {dia} × {por_dia} = {cobrado}.")
