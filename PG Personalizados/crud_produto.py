import psycopg2 as pg

class Produto:
    id_produto: int
    nome: str
    tipo: str
    preco: float
    quantidade_disponivel: int

    def __init__(self, nome: str, tipo: str, preco: float, quantidade_disponivel: int):
        self.id_produto = None
        self.nome = nome
        self.tipo = tipo
        self.preco = preco
        self.quantidade_disponivel = quantidade_disponivel

    def __str__(self):
        return f"Produto(id_produto={self.id_produto}, nome={self.nome}, tipo={self.tipo}, preco={self.preco}, quantidade_disponivel={self.quantidade_disponivel})"

    def __repr__(self):
        return self.__str__()

    
    # Inserir produto
    def inserir_produto(self, conexao):
        cursor = None

        try:
            cursor = conexao.cursor()

            sql = """INSERT INTO produto (nome, tipo, preco, quantidade_disponivel)
                     VALUES (%s, %s, %s, %s)
                     RETURNING id_produto;"""

            valores = (self.nome, self.tipo, self.preco, self.quantidade_disponivel)

            cursor.execute(sql, valores)
            self.id_produto = cursor.fetchone()[0]

            conexao.commit()

            print("Produto cadastrado com sucesso!")
            return self

        except Exception as erro:
            conexao.rollback()
            print(f"Erro ao cadastrar produto: {erro}")
            return None

        finally:
            if cursor:
                cursor.close()

    # Listar produtos
    @staticmethod
    def listar_produtos(conexao):
        cursor = None

        try:
            cursor = conexao.cursor()

            sql = """SELECT id_produto, nome, tipo, preco, quantidade_disponivel
                     FROM produto
                     ORDER BY id_produto;"""

            cursor.execute(sql)
            resultados = cursor.fetchall()

            produtos = []

            for registro in resultados:
                produto = Produto(
                    nome=registro[1],
                    tipo=registro[2],
                    preco=registro[3],
                    quantidade_disponivel=registro[4]
                )
                produto.id_produto = registro[0]
                produtos.append(produto)

            return produtos

        except Exception as erro:
            print(f"Erro ao listar produtos: {erro}")
            return []

        finally:
            if cursor:
                cursor.close()

    # Atualizar produto
    def atualizar_produto(self, conexao):
        cursor = None

        try:
            cursor = conexao.cursor()

            sql = """UPDATE produto
                     SET nome = %s, tipo = %s, preco = %s,
                         quantidade_disponivel = %s
                     WHERE id_produto = %s;"""

            valores = (
                self.nome,
                self.tipo,
                self.preco,
                self.quantidade_disponivel,
                self.id_produto
            )

            cursor.execute(sql, valores)
            alteradas = cursor.rowcount
            conexao.commit()

            if alteradas > 0:
                print("Produto atualizado com sucesso!")
                return True

            print("Produto não encontrado.")
            return False

        except Exception as erro:
            conexao.rollback()
            print(f"Erro ao atualizar produto: {erro}")
            return False

        finally:
            if cursor:
                cursor.close()

    # Excluir produto
    @staticmethod
    def excluir_produto(id_produto: int, conexao):
        cursor = None

        try:
            cursor = conexao.cursor()

            sql = """DELETE FROM produto WHERE id_produto = %s"""
            cursor.execute(sql, (id_produto,))

            apagadas = cursor.rowcount
            conexao.commit()

            if apagadas > 0:
                print("Produto excluído com sucesso!")
                return True

            print("Produto não encontrado.")
            return False

        except Exception as erro:
            conexao.rollback()
            print(f"Erro ao excluir produto: {erro}")
            return False

        finally:
            if cursor:
                cursor.close()
    
