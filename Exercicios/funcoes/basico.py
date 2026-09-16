
# Exercicio 1
import math


def formatar_saudacao(nome:str, cidade:str)-> str:
    return f"Olá {nome}, seja bem-vindo(a) a {cidade}!"
   
 #Exercicio 2
def calcular_perimetro(largura:float, altura:float)-> float:
    perimetro = 2 * (largura + altura)
    return perimetro

# Exercicio 3
def fahrenheit_para_celsius(temp_f: float)-> float:
    temp_celsius = (temp_f - 32) * 5/9
    return temp_celsius

# Exercicio 4
def calcular_gorjeta_por_pessoa(conta: float, porcentagem_gorjeta: float, pessoas: int) -> float:
    gorjeta = (conta * (porcentagem_gorjeta / 100)) / pessoas
    return gorjeta

# Exercicio 5
def calcular_area_circulo(raio: float) -> float:
    pi = 3.14159
    area = pi * (raio ** 2)
    return f"Um circulo com raio {raio} tem uma área de {area:.2f}."

# Exercicio 6
def resumo_juros_basico(capital_inicial: float, taxa_juros: float, anos: int):
    m = capital_inicial * (1 + taxa_juros/100) **anos
    return f"Após {anos} anos, R${capital_inicial:.2f} cresce para R${m:.2f}."

# Exercicio 7 
def metricas_cilindro(raio: float, altura: float):
    volume = math.pi * (raio ** 2) * altura
    area_superficie = 2 * math.pi * raio * (raio + altura)
    return f"Um cilindro com raio {raio} e altura {altura} tem um volume de {volume:.2f} e uma área de superfície de {area_superficie:.2f}."      
    

if __name__ == '__main__':
    print("EXERCICIOS ======================================\n\n")

    saudacao = formatar_saudacao("Alice", "Porto Alegre")
    print(f"1 - {saudacao}")    

    perimetro = calcular_perimetro(altura=10, largura=5)
    print(f"2 - {perimetro}")

    temperatura = fahrenheit_para_celsius(68)
    print(f"3 - {temperatura}")

    gorjeta = calcular_gorjeta_por_pessoa(100, 15, 3)
    print(f"4 - {gorjeta}")

    area = calcular_area_circulo(3)
    print(f"5 - {area}")

    juros = resumo_juros_basico(1000, 5, 3)
    print(f"6 - {juros}")

    volume = metricas_cilindro(2.0, 5.0)
    print(f"7 - {volume}")
