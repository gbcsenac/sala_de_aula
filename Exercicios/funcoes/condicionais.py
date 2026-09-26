def fizz_buzz(numero:int):
    if numero % 3 == 0:
        return "Fizz"
    elif numero % 5 == 0:
        return "Buzz"
    elif numero % 3 == 0 and numero % 5 == 0:
        return "FizzBuzz"
    else:
        return numero

#Exercicio 1
def verificar_maioridade(idade:int):
    if idade >= 18:
        return "Maior idade"
    else:
        return "Menor idade"

#Exercicio 2
def verificar_paridade(numero:int):
    if numero % 2 == 0:
        return "Par"
    else:
        return "Ímpar"
    
#Exercicio 3
def classificar_numero(numero:int):
    if numero > 0: 
        return "Positivo"
    elif numero < 0:
        return "Negativo"
    else:
        return "Zero"

#Exercicio 4
def  calcular_resultado(nota1:float, nota2:float):
    media = (nota1 + nota2) / 2
    if media > 7:
        return "Aprovado"
    else:
        return "Reprovado"

#Exercicio 5
def maior_de_dois(a:int, b:int):
    if a > b:
        return "o primeiro é maior"
    if a < b:
        return "o segundo é maior"
    return "São iguais"

def calcular_desconto(valor_compra:float, 
                      cliente_vip:bool):
    if cliente_vip or valor_compra > 200:
        return f"Valor final: R$ {valor_compra*0.85}"
    return f"Valor final: R$ {valor_compra * 0.95}"

def conceito_nota(nota:float):
    if nota >= 9 and nota < 10:
        return "A"
    if nota >= 7 and nota < 9:
        return "B"
    if nota > 5 and nota < 7:
        return "C"
    return "F"

def validar_triangulo(a:float, b:float, c:float):
    if (a+b > c) and (b+c > a) and (a+c > b):
        if a == b == c:
            return "Equilátero"

        if a == b != c:
            return "Isóceles"
        
        if a != b != c:
            return "Escaleno"
    else:
        return "Não é triângulo"

def calcular_imposto(salario:float):
    excedente = salario - 20000
    if salario >= 2000 and salario < 4000:
        return excedente * 0.1
    if salario >= 4000:
        return 200 + (excedente * 0.2)
    return 0

def validador_ano_bissexto(ano:int):
    if ano%4 == 0 and ano%400 == 0:
        return True
    return False


if __name__ == "__main__":
    print("Exercicicio condicionais ======================================\n\n")

    teste = fizz_buzz(15)
    print(teste)

    maioridade = verificar_maioridade(20)
    print(maioridade)
    menoridade = verificar_maioridade(15)
    print(menoridade)
    
    paridade = verificar_paridade(7)
    print(  paridade)
    paridade = verificar_paridade(12)
    print(paridade)

    classificacao = classificar_numero(-5)
    print(classificacao)
    classificacao = classificar_numero(0)
    print(classificacao)

    resultado = calcular_resultado(8, 6)     
    print(resultado)
    resultado = calcular_resultado(4, 3)
    print(resultado)

    maior = maior_de_dois(10, 5)
    print("O segundo é maior")
    menor = maior_de_dois(5,5)
    print("São iguais")





