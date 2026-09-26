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
    return pares
            

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

#Exercício 4:  Substituir Negativos por Zero
def zerar_negativos(numeros:list):
    aux = numeros.copy()

    for numero in numeros:
        if numero < 0:
            indice = numeros.index(numero)
            aux[indice] = 0

    return aux

#Exercício 5: Busca de Elemento com `while`
def contem_valor(lista: list, alvo):
   while(Index < len(lista)):
        if lista[Index] == alvo:
            return True
        Index += 1

    return False


#Exercício 6 : Classificar Notas de Alunos
def contar_aprovados(notas: list):
    count = 0
    for nota in notas:
        if nota >= 7:
            count += 1
    return count


#Exercício 7: Separador de Textos Curtos e Longos
def filtrar_palavras_curtas(palavras: list, tamanho_maximo: int):
   for palavra in palavras:
        if len(palavra) <= tamanho_maximo:
            filtro.append(palavra)

    return filtro

#Exercício 8: Separador de Pares e Ímpares
def separar_pares_impares(numeros:list):
    pares, impares = 0

    for numero in numeros:
        if numero % 2 != 0:
            impares+=1
        else:
            pares+=1
    
    return f"Pares: {pares} | Ímpares: {impares}"


#Exercício 9: Maior e Menor Valor Sem Funções Nativas
def encontrar_extremos(numeros: list):
    maior, menor = 0

    for numero in numeros:
        if numero > maior:
            maior = numero
        
        if numero < menor:
            menor = numero
        
    return (menor, maior)


#Exercício 10: Processamento de Caixa Eletrônico com `while`
def simular_saque(saldo_inicial:float, saques: list):

    index = 0
    permitidos = []
    negados = []

    while (index < len(saques)):
        if saldo_inicial - saques[index] >= 0:
            permitidos.append(saques[index])
            saldo_inicial-=saques[index]
        else:
            negados.append(saques[index])
        index+=1
    
    return saldo_inicial


#Exercício 11: Remover Duplicados Mantedor de Ordem
def remover_duplicados(lista: list):

    not_duplicados = []
        
    for numero in lista:
        if numero not in not_duplicados:
            not_duplicados.append(numero)
    
    return not_duplicados


#Exercício 12: Média dos Positivos
def media_positivos(numeros: list):
    if not numeros: #verifica se len(numeros) == 0
        return 0.0
    
    divisor = 0
    valor = 0
    for numero in numeros:
        if numero > 0:
            valor += numero
            divisor += 1
    
    return valor/divisor

#Exercício 13: Validador de Senhas em Lista
def validador_senha(senhas:list[str]):
    validas = []
    for senha in senhas:
        if len(senha) > 8:
            validas.append(senha)

    return validas
#Exercício 14: Busca do Primeiro Elemento Fora do Padrão (`while`)
def primeiro_impar(numeros: list):

    index = 0

    while (index < len(numeros)):
        if numeros[index] % 2 != 0:
            return numeros[index]
    
    return None

#Exercício 15: Contagem de Frequência de um Elemento
def contar_ocorrencias(lista:list, target):
    ocurrences = 0
    for element in lista:
        if element == target:
            ocurrences+=1

    return ocurrences

#Exercício 16: Análise de Sequência Crescente
def is_estritamente_crescente(palavras: list):

    index = 1

    while (index < len(palavras) - 1):
        if len(palavras[index] > len(palavras[index-1])):
            pass
        else:
            return False
    
    return True

#Exercício 17: Condensador de Lista (Compressão de Nulos/Zeros)
def mover_zeros_para_o_final(numeros: list):
    zeros_final = numeros.copy()

    for numero in zeros_final:
        #TODO: 

#Exercício 18: Simulador de Fila de Atendimento Preferencial

#Exercício 19: Detector de Picos Em Sequências

#Exercício 20: Algoritmo de Validação de Sequência de Transações (Jogo de Saldo)





if __name__ == '__main__':
    print("Exercicios_listas_lacos ======================================\n\n")

    print(filtrar_pares([1, 2, 3, 4, 5, 6]))

    print(contar_negativos([10, -3, 0, -5, 8, -1]))

    print(somar_maiores_que([10, 5, 20, 3, 15], 8))
                 
    not_duplicados = remover_duplicados([1, 3, 2, 3, 1, 4, 2])
    print(not_duplicados)

    zero_final = mover_zeros_para_o_final([0, 1, 0, 3, 12, 0, 5])
    print(zero_final)
    
