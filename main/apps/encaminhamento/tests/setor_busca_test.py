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
def test_get_setor_by_bairro():
    client = APIClient()

    # Create test data
    bairro = "Test Bairro"
    endereco1 = Endereco.objects.create(bairro=bairro)
    endereco2 = Endereco.objects.create(bairro=bairro)
    unidade1 = UnidadeOrganizacional.objects.create(nome="Unidade 1",hora_abertura="06:00:00",hora_fechamento="18:00:00")
    unidade2 = UnidadeOrganizacional.objects.create(nome="Unidade 2",hora_abertura="06:00:00",hora_fechamento="18:00:00")
    setor1 = SetorInstitucional.objects.create(nome="Setor 1")
    setor2 = SetorInstitucional.objects.create(nome="Setor 2")

    # Correct way to add many-to-many relationships
    unidade1.enderecos.add(endereco1)
    unidade2.enderecos.add(endereco2)

    unidade1.setores_institucionais.add(setor1)
    unidade2.setores_institucionais.add(setor2)


    url = f"/alocacao/setor/bairro/{bairro}/"

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['setores']) == 2  # Check for two sectors
    assert len(response.json()['unidades']) == 2 # Check for two units

    #Test with non-existent bairro
    url = "/alocacao/setor/bairro/NonExistentBairro/"
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND




@pytest.mark.django_db
def test_get_setor_by_cidade():
    client = APIClient()

    # Create test data
    cidade = "Test City"
    endereco1 = Endereco.objects.create(cidade=cidade)
    endereco2 = Endereco.objects.create(cidade=cidade)
    unidade1 = UnidadeOrganizacional.objects.create(nome="Unidade 1",hora_abertura="06:00:00",hora_fechamento="18:00:00")
    unidade2 = UnidadeOrganizacional.objects.create(nome="Unidade 2",hora_abertura="06:00:00",hora_fechamento="18:00:00")
    setor1 = SetorInstitucional.objects.create(nome="Setor 1")
    setor2 = SetorInstitucional.objects.create(nome="Setor 2")

    # Correctly add Enderecos to Unidades using .add()
    unidade1.enderecos.add(endereco1)
    unidade2.enderecos.add(endereco2)

    # Correctly add Setores to Unidades (assuming this is also ManyToMany)
    unidade1.setores_institucionais.add(setor1)
    unidade2.setores_institucionais.add(setor2)

    url = f"/alocacao/setor/cidade/{cidade}/"

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['setores']) == 2  # Check for two sectors
    assert len(response.json()['unidades']) == 2 # Check for two units

    #Test with non-existent city
    url = "/alocacao/setor/cidade/NonExistentCity/"
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


