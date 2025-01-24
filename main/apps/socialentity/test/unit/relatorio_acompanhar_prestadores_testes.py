import pytest
from django.db import IntegrityError 
from apps.socialentity.models import Telefone

@pytest.mark.django_db
def test_criar_telefone():
    # Instanciando e salvando o telefone
    telefone = Telefone(numero="987654321", ddd="55")
    telefone.save()

    # Recuperando do banco de dados e verificando os valores
    telefone_salvo = Telefone.objects.get(id=telefone.id)
    assert telefone_salvo.numero == "987654321"
    assert telefone_salvo.ddd == "55"
    assert str(telefone_salvo) == "+55 987654321"
    
    # Exibindo o telefone no console
    print(f"Telefone salvo: ID={telefone_salvo.id}, DDD={telefone_salvo.ddd}, Número={telefone_salvo.numero}")
