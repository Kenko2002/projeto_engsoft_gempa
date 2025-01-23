import pytest
from main.scripts.volume_cilindro import calcular_volume_cilindro
import math

def test_volume_cilindro_valores_validos():
    """Testa o cálculo com valores válidos."""
    raio = 3
    altura = 5
    esperado = math.pi * (raio ** 2) * altura
    resultado = calcular_volume_cilindro(raio, altura)
    assert pytest.approx(resultado, rel=1e-5) == esperado

def test_raio_negativo():
    """Testa se um erro é levantado para raio negativo."""
    with pytest.raises(ValueError, match="O raio e a altura devem ser maiores que zero."):
        calcular_volume_cilindro(-3, 5)

def test_altura_negativa():
    """Testa se um erro é levantado para altura negativa."""
    with pytest.raises(ValueError, match="O raio e a altura devem ser maiores que zero."):
        calcular_volume_cilindro(3, -5)

def test_raio_zero():
    """Testa se um erro é levantado para raio igual a zero."""
    with pytest.raises(ValueError, match="O raio e a altura devem ser maiores que zero."):
        calcular_volume_cilindro(0, 5)

def test_altura_zero():
    """Testa se um erro é levantado para altura igual a zero."""
    with pytest.raises(ValueError, match="O raio e a altura devem ser maiores que zero."):
        calcular_volume_cilindro(3, 0)
