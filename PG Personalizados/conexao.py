import psycopg2

def conectar():
    conexao = psycopg2.connect(
        host="localhost",
        database="pavane_greyce",
        user="postgres",
        password="postgres",
        port="5432"
    )

    return conexao
