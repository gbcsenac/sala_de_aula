# conexao.py — abre a conexão com o banco, a partir do .env.
#
# A senha mora no .env, que o .gitignore deixa fora do repositório. É a ideia
# do config_local.py da UC3 (Aula 07) no formato que o mercado usa: um arquivo
# de texto CHAVE=valor, que o Python, o Docker e o GitHub Actions sabem ler.
# Este arquivo só sabe ONDE a senha está, não qual é.

import os

import psycopg2 as pg
from dotenv import load_dotenv


def dados_de_conexao(banco_da_variavel="PG_BANCO"):
    """Os parâmetros do psycopg2, lidos do .env. O teste usa PG_BANCO_DE_TESTE."""
    # load_dotenv() não sobrescreve variável que já existe no ambiente: no
    # GitHub Actions a senha vem dos segredos do repositório, e não de arquivo
    load_dotenv()
    faltando = [
        chave
        for chave in ("PG_HOST", "PG_PORTA", "PG_USUARIO", "PG_SENHA", banco_da_variavel)
        if not os.getenv(chave)
    ]
    if faltando:
        # o erro mais comum de quem acabou de clonar: diz o que fazer, em vez
        # de um erro de conexão que ninguém entende
        raise SystemExit(
            "Falta configurar " + ", ".join(faltando) + ". Copie o .env.exemplo, "
            "renomeie para .env e ponha a senha do seu PostgreSQL."
        )
    return {
        "host": os.getenv("PG_HOST"),
        "port": os.getenv("PG_PORTA"),
        "user": os.getenv("PG_USUARIO"),
        "password": os.getenv("PG_SENHA"),
        "dbname": os.getenv(banco_da_variavel),
    }


def conectar(banco_da_variavel="PG_BANCO"):
    return pg.connect(**dados_de_conexao(banco_da_variavel))
