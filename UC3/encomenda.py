from datetime import date

class Encomenda:
    id_encomenda: int
    id_cliente: int
    data_pedido: date
    data_pagamento: date
    data_retirada: date
    descricao: str

    def __init__(self, id_cliente: int, data_pedido: date, data_pagamento: date, data_retirada: date, descricao: str):

        if id_cliente is None:
            raise ValueError("A encomenda precisa de um cliente.")

        self.id_encomenda = None
        self.id_cliente = id_cliente
        self.data_pedido = data_pedido
        self.data_pagamento = data_pagamento
        self.data_retirada = data_retirada
        self.descricao = descricao

    def __str__(self):
        return f"Encomenda(id_encomenda={self.id_encomenda}, id_cliente={self.id_cliente}, data_pedido={self.data_pedido}, data_pagamento={self.data_pagamento}, data_retirada={self.data_retirada}, descricao={self.descricao})"

    def __repr__(self):
        return self.__str__()