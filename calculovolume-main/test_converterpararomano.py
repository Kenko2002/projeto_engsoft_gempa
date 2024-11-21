import pytest
from romano import converter_para_romano

def test_valores_validos():
    """Testa números dentro do intervalo válido."""
    assert converter_para_romano(1) == "I"
    assert converter_para_romano(4) == "IV"
    assert converter_para_romano(9) == "IX"
    assert converter_para_romano(40) == "XL"
    assert converter_para_romano(90) == "XC"
    assert converter_para_romano(400) == "CD"
    assert converter_para_romano(900) == "CM"
    assert converter_para_romano(3999) == "MMMCMXCIX"

def test_limite_inferior():
    """Testa o limite inferior inválido."""
    with pytest.raises(ValueError, match="O número deve estar entre 1 e 3999."):
        converter_para_romano(0)

def test_limite_superior():
    """Testa o limite superior inválido."""
    with pytest.raises(ValueError, match="O número deve estar entre 1 e 3999."):
        converter_para_romano(4000)

def test_numeros_intermediarios():
    """Testa números intermediários."""
    assert converter_para_romano(58) == "LVIII"
    assert converter_para_romano(1987) == "MCMLXXXVII"

def test_numeros_pequenos():
    """Testa números pequenos."""
    assert converter_para_romano(2) == "II"
    assert converter_para_romano(3) == "III"
