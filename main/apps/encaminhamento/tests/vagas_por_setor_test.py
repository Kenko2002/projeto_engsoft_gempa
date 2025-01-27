import pytest
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.db import transaction

# Importe os modelos e serializers necessários
from apps.encaminhamento.models import SetorInstitucional, Vaga
from apps.encaminhamento.serializers import VagaVagasDiponiveisSerializer # Substitua 'seu_app' pelo nome do seu app
from apps.alocacao.models import Alocacao


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


    url = f'/setor/{setor.id}/getvagasdisponiveis/'  # Substitua 'vagas-disponiveis-por-setor' pelo nome da sua URL


    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Verifica se as vagas disponíveis estão corretas
    expected_vagas = [vaga2, vaga3]
    assert len(response.json()) == len(expected_vagas)

