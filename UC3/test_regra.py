from regra import validar_preco

def test_preco_valido():
    assert validar_preco(10.0) == True

def test_preco_valido_com_centavos():
    assert validar_preco(25.50) == True

def test_preco_zero():
    assert validar_preco(0.00) == False

def test_preco_negativo():
    assert validar_preco(-5.0) == False
    
def test_preco_negativo_com_centavos():
    assert validar_preco(-0.50) == False
