import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.encaminhamento.models import SetorInstitucional, Vaga, Funcao,UnidadeOrganizacional
from apps.socialentity.models import Responsavel, Endereco # Assuming you have these models
import json
from django.db import transaction

@pytest.mark.django_db
def test_setor_por_funcao_api_view():
    """Testes para a API View SetorPorFuncaoAPIView."""
    client = APIClient()

    # Cria uma Função
    funcao = Funcao.objects.create(nome="Analista de Dados")

    # Cria um Setor com Vagas
    setor1 = SetorInstitucional.objects.create(nome="Setor 1", responsavel=None)  # Substitua None se necessário
    vaga1 = Vaga.objects.create(funcao=funcao)
    setor1.vagas.add(vaga1)


    #Cria um setor sem vagas para essa função
    setor2 = SetorInstitucional.objects.create(nome="Setor 2", responsavel=None)

    # URL para teste
    url = reverse('setores-funcao', kwargs={'funcao_nome': 'Analista de Dados'}) # 'setor-por-funcao' deve ser o nome da sua URL



    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1  # Apenas o setor1 deve ser retornado


    # Teste com função inexistente
    url_inexistente = reverse('setores-funcao', kwargs={'funcao_nome': 'Função Inexistente'})
    response = client.get(url_inexistente)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Função não encontrada.'}


