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
    """Testes para a API View VagasDisponiveisPorSetorAPIView."""
    client = APIClient()

    # Cenário 1: Setor com vagas, algumas alocadas
    funcao1 = Funcao.objects.create(nome="Analista de Dados")
    funcao2 = Funcao.objects.create(nome="Desenvolvedor Frontend")
    setor1 = SetorInstitucional.objects.create(nome="Setor 1")
    vaga1 = Vaga.objects.create(funcao=funcao1)
    vaga2 = Vaga.objects.create(funcao=funcao2)
    vaga3 = Vaga.objects.create(funcao=funcao1)
    setor1.vagas.add(vaga1, vaga2, vaga3)
    Alocacao.objects.create(vaga=vaga1)

    url = f'/setor/{setor1.id}/getvagasdisponiveis/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2  # Duas vagas disponíveis (vaga2 e vaga3)


    # Cenário 2: Setor sem vagas
    setor2 = SetorInstitucional.objects.create(nome="Setor 2")
    url = f'/setor/{setor2.id}/getvagasdisponiveis/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0  # Nenhuma vaga disponível


    # Cenário 3: Setor inexistente
    url = '/setor/9999/getvagasdisponiveis/'  # ID de setor inexistente
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Setor não encontrado."}


    # Cenário 4: Todas as vagas alocadas
    Alocacao.objects.create(vaga=vaga2)
    Alocacao.objects.create(vaga=vaga3)
    url = f'/setor/{setor1.id}/getvagasdisponiveis/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0 #Nenhuma vaga disponivel


    #Cenario 5: Testando com o serializer
    serializer = VagaVagasDiponiveisSerializer(vaga2, context={"include_funcao": True})
    assert serializer.data['funcao']['nome'] == funcao2.nome

