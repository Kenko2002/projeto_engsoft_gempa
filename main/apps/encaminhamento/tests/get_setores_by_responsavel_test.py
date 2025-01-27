
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from apps.encaminhamento.models import SetorInstitucional
from apps.socialentity.models import Responsavel
from apps.encaminhamento.serializers import SetorInstitucionalSerializer  # Certifique-se de importar o serializer correto


@pytest.mark.django_db
def test_get_setores_institucionais_por_responsavel_sucesso(client: APIClient):
    """
    Testa o sucesso da API ao buscar setores institucionais por um responsável existente.
    """
    responsavel = Responsavel.objects.create(nome="Responsável Teste")
    setor1 = SetorInstitucional.objects.create(nome="Setor 1", responsavel=responsavel)
    setor2 = SetorInstitucional.objects.create(nome="Setor 2", responsavel=responsavel)

    url = f"/api/setores-institucionais/responsavel/{responsavel.id}/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_data = SetorInstitucionalSerializer([setor1, setor2], many=True).data
    assert response.json() == expected_data


@pytest.mark.django_db
def test_get_setores_institucionais_por_responsavel_nao_encontrado(client: APIClient):
    """
    Testa o comportamento da API quando o responsável não é encontrado.
    """
    responsavel_id_inexistente = 999
    url = f"/api/setores-institucionais/responsavel/{responsavel_id_inexistente}/"
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Responsável não encontrado."}


@pytest.mark.django_db
def test_get_setores_institucionais_por_responsavel_sem_setores(client: APIClient):
    """
    Testa o comportamento da API quando o responsável existe, mas não possui setores institucionais associados.
    """
    responsavel = Responsavel.objects.create(nome="Responsável Teste")
    url = f"/api/setores-institucionais/responsavel/{responsavel.id}/"
    response = client.get(url)


    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [] # Deve retornar uma lista vazia
