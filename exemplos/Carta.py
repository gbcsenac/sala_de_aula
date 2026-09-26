class Carta:
        
        remetente:str
        destinatario:str
        conteudo:str

def __init___(self,remetente:str, destinatario:str, conteudo:str):

    self.conteudo = conteudo
    self.destinatario = destinatario
    self.remetente = remetente

#Instância
carta = Carta('Joao', 'Pyetra', 'Te amo')

