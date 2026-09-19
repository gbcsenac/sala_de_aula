def dobrar(numeros:[]):
    for i in range(len(numeros)):
        numeros[i] = numeros[i] * 2
        print(numeros[i])

#Exercício 1: Filtrar Números Pares
def filtar_pares(numeros:list):
    pares = [] # ou pares = list()

    for numero in numeros:
        if numero % 2 == 0:
            pares.append(numero)
            

#Exercício 2: Contador de Números Negativos
def contar_negativos(numeros:list):
      quantidade = 0
      for numero in numeros:
        if numero < 0:
            quantidade += 1
      return quantidade 
        

#Exercício 3: Soma de Valores Maiores que um Limite
def somar_maiores_que(numeros: list, limite: float):
    soma = 0
    for numero in numeros:
        if numero > limite:
            soma += numero
    return soma

#Exercício 4
def zerar_negativos(numeros:list):
    aux = numeros.copy()

    for numero in numeros:
        if numero < 0:
            indice = numeros.index(numero)
            aux[indice] = 0

    return aux

#Exercício 5
def contem_valor(lista: list, alvo):
   while(Index < len(lista)):
        if lista[Index] == alvo:
            return True
        Index += 1
    return False

#Exercício 6
def contar_aprovados(notas: list):
    count = 0
    for nota in notas:
        if nota >= 7:
            count += 1
    return count

def filtrar_palavras_curtas(palavras: list, tamanho_maximo: int):
  

            
    
    
if __name__ == "__main__":
    print("Exercicicio loop while ======================================\n\n")

    lista = [1, 2, 3, 4, 5]
    dobrar(lista)

    numeros_pares = filtar_pares([1, 2, 3, 4, 5])
    print(numeros_pares)

   
    





    