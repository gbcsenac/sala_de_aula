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
def verificar_idade(idade:int):
    if idade >= 20:
        return "Maior idade"
    elif idade < 15:
        return "Idade inválida"
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
    if numero % 2 == 0: 
        return "Positivo"
    elif numero < 0:
        return "Negativo"
    else:
        return "Zero"

if __name__ == "__main__":
    print("Exercicicio condicionais ======================================\n\n")

    teste = fizz_buzz(15)
    print(teste)

    teste_idade = verificar_idade(20)
    print(teste_idade)
    teste_idade = verificar_idade(15)
    print(teste_idade)

    teste_paridade = verificar_paridade(7)
    print(teste_paridade)
    teste_paridade = verificar_paridade(10)
    print(teste_paridade)



