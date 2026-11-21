from cliente import Cliente

class ServicoEncomenda:

    def __init__(self, repositorio_clientes, repositorio_produtos):
        self.repositorio_clientes = repositorio_clientes
        self.repositorio_produtos = repositorio_produtos

    def cliente_cadastrado(self, id_cliente):
        clientes = self.repositorio_clientes.listar_clientes()

        for cliente in clientes:
            if cliente.id_cliente == id_cliente:
                return True

        return False
    
    def estoque_disponivel(self, id_produto, quantidade):
        produto = self.repositorio_produtos.buscar_produto(id_produto)

        if produto is None:
            return False

        return produto.quantidade_disponivel >= quantidade 


    
