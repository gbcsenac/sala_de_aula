
# Exercicio 1
def formatar_saudacao(nome:str, cidade:str):
    return f"Olá {nome}, seja bem-vindo(a) a {cidade}!"

if __name__ == '__main__':
     saudacao = formatar_saudacao("Alice", "Porto Alegre")
    print(saudacao)

 #Exercicio 2
 def calcular_perimetro(comprimento:float, largura:float):
    return 2 * (comprimento + largura)

if __name__ == '__main__':
    saudacao = formatar_saudacao("Alice", "Porto Alegre")
    print(F"1 - {saudacao}")    
    perimetro = calcular_perimetro(altura=10, largura=5)
    print(f"2 - {perimetro}")    
    print("================================================================")