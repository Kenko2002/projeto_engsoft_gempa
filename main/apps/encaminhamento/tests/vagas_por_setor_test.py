import pytest
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.db import transaction

# Importe os modelos e serializers necessários
from apps.encaminhamento.models import SetorInstitucional, Vaga,Funcao
from apps.encaminhamento.serializers import VagaVagasDiponiveisSerializer # Substitua 'seu_app' pelo nome do seu app
from apps.alocacao.models import Alocacao


@pytest.mark.django_db
def test_vagas_disponiveis_por_setor_api_view():
    """
    Testes para a API View VagasDisponiveisPorSetorAPIView.
    """
    client = APIClient()

    funcao1 = Funcao.objects.create(nome="Analista de Dados")
    funcao2 = Funcao.objects.create(nome="Desenvolvedor Frontend")

    # Cria um setor
    setor = SetorInstitucional.objects.create(nome="Setor de Teste")

    # Cria algumas vagas para o setor
    vaga1 = Vaga.objects.create(funcao=funcao1) # Adicionei 'titulo', supondo que sua Vaga tem este campo.
    vaga2 = Vaga.objects.create(funcao=funcao2) 
    vaga3 = Vaga.objects.create(funcao=funcao1)
    setor.vagas.add(vaga1, vaga2, vaga3)

    # Cria uma alocação para uma das vagas
    alocacao1 = Alocacao.objects.create(vaga=vaga1, tecnico=None) 


    url = f'/setor/{setor.id}/getvagasdisponiveis/'  # Substitua 'vagas-disponiveis-por-setor' pelo nome da sua URL


    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Verifica se as vagas disponíveis estão corretas
    expected_vagas = [vaga2, vaga3]
    assert len(response.json()) == len(expected_vagas)

