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







@pytest.mark.django_db
def test_setor_por_bairro_api_view():
    """Testes para a API View SetorPorBairroAPIView."""
    client = APIClient()

    # Cria um Endereço e uma Unidade
    endereco1 = Endereco.objects.create(bairro="Bairro A")
    unidade1 = UnidadeOrganizacional.objects.create(nome="Unidade 1", enderecos=endereco1)
    setor1 = SetorInstitucional.objects.create(nome="Setor 1", responsavel=None)
    unidade1.setores_institucionais.add(setor1)

    # Cria outro Endereço e Unidade em outro bairro
    endereco2 = Endereco.objects.create(bairro="Bairro B")
    unidade2 = UnidadeOrganizacional.objects.create(nome="Unidade 2",enderecos=endereco2)
    setor2 = SetorInstitucional.objects.create(nome="Setor 2", responsavel=None)
    unidade2.setores_institucionais.add(setor2)


    # URL para teste
    url = reverse('setor-bairro', kwargs={'bairro_nome': 'Bairro A'}) #'setor-por-bairro' deve ser o nome da sua url


    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['setores']) == 1  # Apenas setor1 deve ser retornado
    assert response.json()['unidades'] == [unidade1.id]


    #Teste sem bairro
    url_sem_bairro = reverse('setor-bairro', kwargs={'bairro_nome': ''})
    response = client.get(url_sem_bairro)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Nome do bairro é obrigatório.'}
