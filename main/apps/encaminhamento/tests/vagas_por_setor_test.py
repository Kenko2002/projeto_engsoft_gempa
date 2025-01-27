import pytest
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.db import transaction

# Importe os modelos e serializers necessários
from apps.encaminhamento.models import SetorInstitucional, Vaga, Alocacao # Substitua 'seu_app' pelo nome do seu app
from apps.encaminhamento.serializers import VagaVagasDiponiveisSerializer # Substitua 'seu_app' pelo nome do seu app


@pytest.mark.django_db
def test_vagas_disponiveis_por_setor_api_view():
    """
    Testes para a API View VagasDisponiveisPorSetorAPIView.
    """
    client = APIClient()

    # Cria um setor
    setor = SetorInstitucional.objects.create(nome="Setor de Teste")

    # Cria algumas vagas para o setor
    vaga1 = Vaga.objects.create(setor=setor, nome="Vaga 1")
    vaga2 = Vaga.objects.create(setor=setor, nome="Vaga 2")
    vaga3 = Vaga.objects.create(setor=setor, nome="Vaga 3")


    # Cria uma alocação para uma das vagas
    Alocacao.objects.create(vaga=vaga1)


    url = reverse('vagas-disponiveis-por-setor', kwargs={'setor_id': setor.id}) # Substitua 'vagas-disponiveis-por-setor' pelo nome da sua URL


    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Verifica se as vagas disponíveis estão corretas
    expected_vagas = [vaga2, vaga3]
    assert len(response.json()) == len(expected_vagas)

    # Verifica os dados das vagas retornadas  (ajuste de acordo com seu serializer)
    for i, vaga in enumerate(expected_vagas):
      assert response.json()[i]['nome'] == vaga.nome #Ex: verifica o campo nome da vaga


    # Teste para um setor inexistente
    url_inexistente = reverse('vagas-disponiveis-por-setor', kwargs={'setor_id': 9999}) # Substitua 'vagas-disponiveis-por-setor' pelo nome da sua URL
    response_inexistente = client.get(url_inexistente)
    assert response_inexistente.status_code == status.HTTP_404_NOT_FOUND
    assert response_inexistente.json() == {"error": "Setor não encontrado."}


    # Teste com todas as vagas alocadas.
    Alocacao.objects.create(vaga=vaga2)
    Alocacao.objects.create(vaga=vaga3)

    response_todas_alocadas = client.get(url)
    assert response_todas_alocadas.status_code == status.HTTP_200_OK
    assert len(response_todas_alocadas.json()) == 0 #Deve retornar lista vazia
