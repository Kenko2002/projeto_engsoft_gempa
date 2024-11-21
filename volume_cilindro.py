import math

def calcular_volume_cilindro(raio, altura):
    """
    Calcula o volume de um cilindro.
    Fórmula: V = π * r² * h
    """
    if raio <= 0 or altura <= 0:
        raise ValueError("O raio e a altura devem ser maiores que zero.")
    return math.pi * (raio ** 2) * altura
