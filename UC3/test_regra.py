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

# RESULTADO DOS TESTES:
# Teste 1: preço positivo (10.00) - PASS
# Teste 2: preço positivo com centavos (25.50) - PASS
# Teste 3: preço zero (0.00) - PASS
# Teste 4: preço negativo (-5.00) - PASS
# Teste 5: preço negativo com centavos (-0.50) - PASS
#
# Conclusão:
# Todos os testes passaram.
# A função validar_preco() aceita somente valores maiores que zero.