from UC2.conexao import conectar
class Cliente:

    def __init__(self, nome, telefone, email=None, tipo=None, id_cliente=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.tipo = tipo

    def __str__(self):
        return (
            f"ID: {self.id_cliente} | "
            f"Nome: {self.nome} | "
            f"Telefone: {self.telefone} | "
            f"Email: {self.email} | "
            f"Tipo: {self.tipo}"
        )

    def __repr__(self):
        return self.__str__()


class RepositorioCliente:

    def __init__(self, conexao=None):
        self.conexao = conexao if conexao else conectar()

    # CREATE - Inserir cliente
    def inserir_cliente(self, cliente):
        cursor = self.conexao.cursor()

        cursor.execute(
            """
            INSERT INTO cliente (nome, telefone, email, tipo)
            VALUES (%s, %s, %s, %s)
            RETURNING id_cliente
            """,
            (cliente.nome, cliente.telefone, cliente.email, cliente.tipo)
        )

        cliente.id_cliente = cursor.fetchone()[0]
        self.conexao.commit()
        cursor.close()

        return cliente

    # READ - Listar clientes
    def listar_clientes(self):
        cursor = self.conexao.cursor()

        cursor.execute(
            "SELECT id_cliente, nome, telefone, email, tipo FROM cliente"
        )

        resultados = cursor.fetchall()
        cursor.close()

        return [
            Cliente(
                id_cliente=linha[0],
                nome=linha[1],
                telefone=linha[2],
                email=linha[3],
                tipo=linha[4]
            )
            for linha in resultados
        ]

    # UPDATE - Atualizar cliente
    def atualizar_cliente(self, cliente):
        cursor = self.conexao.cursor()

        cursor.execute(
            """
            UPDATE cliente
            SET nome = %s, telefone = %s, email = %s, tipo = %s
            WHERE id_cliente = %s
            """,
            (
                cliente.nome,
                cliente.telefone,
                cliente.email,
                cliente.tipo,
                cliente.id_cliente
            )
        )

        self.conexao.commit()
        atualizado = cursor.rowcount > 0
        cursor.close()

        return atualizado

    # DELETE - Excluir cliente
    def excluir_cliente(self, id_cliente):
        cursor = self.conexao.cursor()

        cursor.execute(
            "DELETE FROM cliente WHERE id_cliente = %s",
            (id_cliente,)
        )

        self.conexao.commit()
        excluido = cursor.rowcount > 0
        cursor.close()

        return excluido