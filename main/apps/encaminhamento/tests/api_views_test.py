import pytest
import requests
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from django.utils.timezone import localtime, make_aware, timedelta
from rest_framework import status
from apps.socialentity.models import (
    Telefone, Endereco, EntidadeSocial, Usuario, Prestador,
    Tecnico, Fiscal, Coordenador, Responsavel, UnidadeOrganizacional,
    EnumSexoBiologico, EnumPrestadorNaturalidade,
    EnumPrestadorCor, EnumPrestadorReligiao
)
from apps.atendimento.models import Execucao, Condicao
from apps.alocacao.models import Alocacao, Presenca, DiaCombinado
from apps.encaminhamento.models import SetorInstitucional, Vaga, Funcao
from apps.encaminhamento.serializers import SetorSerializer, VagaVagasDiponiveisSerializer # Importe os serializers
from datetime import datetime


@pytest.mark.django_db
def test_setores_institucionais_por_responsavel_api_view(client):
    responsavel = Responsavel.objects.create(nome="Responsável Teste")
    setor1 = SetorInstitucional.objects.create(nome="Setor 1", responsavel=responsavel)
    setor2 = SetorInstitucional.objects.create(nome="Setor 2", responsavel=responsavel)

    response = client.get(f"/setor-institucional/get-setor-by-responsavel/{responsavel.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert any(setor['nome'] == "Setor 1" for setor in response.json())
    assert any(setor['nome'] == "Setor 2" for setor in response.json())

    # Teste com responsável inexistente
    response = client.get("/setor-institucional/get-setor-by-responsavel/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Responsável não encontrado."}



@pytest.mark.django_db
def test_vagas_disponiveis_por_setor_api_view(client):
    setor = SetorInstitucional.objects.create(nome="Setor Teste")
    funcao = Funcao.objects.create(nome="Função Teste")
    vaga1 = Vaga.objects.create(funcao=funcao)
    vaga2 = Vaga.objects.create(funcao=funcao)
    setor.vagas.add(vaga1, vaga2)

    # Cria uma alocação para vaga1 (tornando-a indisponível)
    tecnico = Tecnico.objects.create(nome="Técnico Teste")
    alocacao = Alocacao.objects.create(vaga=vaga1, tecnico=tecnico)

    response = client.get(f"/setor/{setor.id}/getvagasdisponiveis/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1  # Apenas vaga2 deve estar disponível
    assert response.json()[0]['id'] == vaga2.id


    # Teste com setor inexistente
    response = client.get("/setor/999/getvagasdisponiveis/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Setor não encontrado."}



@pytest.mark.django_db
def test_avaliar_prestador_api_view(client):

    funcao = Funcao.objects.create(nome="Função Teste")
    vaga = Vaga.objects.create(funcao=funcao)
    user_tecnico = User.objects.create_user(username='tecnico', password='testpassword')
    tecnico = Tecnico.objects.create(user=user_tecnico, nome='Teste')
    prestador = Prestador.objects.create(nome="Prestador Teste")
    alocacao = Alocacao.objects.create(tecnico=tecnico, prestador=prestador)


    data = {
        "data_apresentacao": "2024-12-20T12:00:00Z",
        "status": "APROVADO",
        "vaga": vaga.id, # Passando o ID da vaga
        "observacao_avaliacao": "Teste de observação", #corrigido nome do campo
        "diascombinados": [
            {"dia_semana": "SEGUNDA-FEIRA", "horario_entrada": "08:00:00Z", "horario_saida": "17:00:00Z"}
        ]
    }

    response = client.put(f"/encaminhamento/avaliar-prestador/{alocacao.id}/", data=data, content_type='application/json')


    assert response.status_code == status.HTTP_200_OK
    alocacao.refresh_from_db()
    assert alocacao.status == "APROVADO"
    assert alocacao.vaga == vaga
    assert alocacao.observacao_avaliacao == "Teste de observação"
    assert alocacao.data_apresentacao == datetime(2024, 12, 20, 12, 0, tzinfo=timedelta(0))
    assert DiaCombinado.objects.filter(alocacao=alocacao).exists()


    # Teste com alocação inexistente
    response = client.put("/encaminhamento/avaliar-prestador/999/", data=data, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Alocação não encontrada."}





@pytest.mark.django_db
def test_alocacao_create_view(client):
    tecnico = Tecnico.objects.create(nome="Técnico Teste")
    condicao = Condicao.objects.create(horas_maximas=100)
    funcao = Funcao.objects.create(nome='Funcao Teste')
    vaga = Vaga.objects.create(funcao=funcao)
    setor = SetorInstitucional.objects.create(nome="Setor Teste")
    setor.vagas.add(vaga)


    data = {
        "condicao": condicao.id,
        "prazo_apresentacao": "2024-01-01",
        "tecnico": tecnico.id,
        "vaga": vaga.id,
        "setor_id": setor.id

    }

    response = client.post("/encaminhamento/encaminhar-instituicao/", data=data, content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['message'] == 'Encaminhado com sucesso!'
    assert 'alocacao_id' in response.json()  # Verifica se a chave 'alocacao_id' existe na resposta

    # Verificar se a alocação foi criada corretamente no banco de dados
    alocacao_id = response.json()['alocacao_id']
    alocacao = Alocacao.objects.get(id=alocacao_id)
    assert alocacao.condicao == condicao
    assert alocacao.tecnico == tecnico
    assert alocacao.vaga == vaga





@pytest.mark.django_db
def test_novo_encaminhamento_api_view(client):
    condicao = Condicao.objects.create(horas_maximas=100)
    tecnico = Tecnico.objects.create(nome="Técnico Teste")
    

    data = {
        "id_condicao": condicao.id,
        "id_tecnico": tecnico.id,
        "prazo_apresentacao": "2024-01-10",
        "vigencia_inicio": "2024-01-01",
        "vigencia_fim": "2024-02-01"
    }

    response = client.post('/encaminhamento/novo-encaminhamento/', data=data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

    # Teste com condição inexistente
    data["id_condicao"] = 999  # ID inválido
    response = client.post('/encaminhamento/novo-encaminhamento/', data=data, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == {'id_condicao': 'Condição não encontrada.'}


    # Teste com técnico inexistente (restaurando o id_condicao)
    data["id_condicao"] = condicao.id
    data["id_tecnico"] = 999
    response = client.post('/encaminhamento/novo-encaminhamento/', data=data, content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == {'id_tecnico': 'Técnico não encontrado.'}


@pytest.mark.django_db
def test_setor_por_funcao_api_view(client):
    funcao = Funcao.objects.create(nome="Função Teste")
    setor1 = SetorInstitucional.objects.create(nome="Setor 1")
    setor2 = SetorInstitucional.objects.create(nome="Setor 2")
    vaga1 = Vaga.objects.create(funcao=funcao)
    vaga2 = Vaga.objects.create(funcao=funcao)
    setor1.vagas.add(vaga1)
    setor2.vagas.add(vaga2)

    response = client.get(f"/alocacao/setor/funcao/{funcao.nome}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2 #setor1 e setor2

    #testando com função inexistente
    response = client.get("/alocacao/setor/funcao/FuncaoInexistente/")
    assert response.status_code == status.HTTP_404_NOT_FOUND #funcao nao encontrada



@pytest.mark.django_db
def test_setor_por_bairro_api_view(client):
    endereco1 = Endereco.objects.create(bairro="Bairro Teste 1", cidade = "Cidade")
    endereco2 = Endereco.objects.create(bairro="Bairro Teste 2", cidade="Cidade")

    unidade1 = UnidadeOrganizacional.objects.create(nome = "Unidade 1")
    unidade2 = UnidadeOrganizacional.objects.create(nome = "Unidade 2")
    unidade1.enderecos.add(endereco1)
    unidade2.enderecos.add(endereco2)

    setor1 = SetorInstitucional.objects.create(nome="Setor 1", unidade_organizacional=unidade1)
    setor2 = SetorInstitucional.objects.create(nome="Setor 2", unidade_organizacional=unidade2)


    response = client.get(f"/alocacao/setor/bairro/{endereco1.bairro}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['setores']) == 1 
    assert response.json()['setores'][0]['nome'] == setor1.nome # setor1 pertence a unidade1 que pertence ao endereco1 com "Bairro teste 1"
    assert response.json()['unidades'] == [unidade1.id]


    response = client.get("/alocacao/setor/bairro/BairroInexistente/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['setores'] == [] #enderecos não encontrados



@pytest.mark.django_db
def test_setor_por_cidade_api_view(client):
    endereco1 = Endereco.objects.create(cidade="Cidade Teste 1", bairro="Bairro")
    endereco2 = Endereco.objects.create(cidade="Cidade Teste 2", bairro="Bairro")
    unidade1 = UnidadeOrganizacional.objects.create(nome = "Unidade 1")
    unidade2 = UnidadeOrganizacional.objects.create(nome = "Unidade 2")

    unidade1.enderecos.add(endereco1)
    unidade2.enderecos.add(endereco2)


    setor1 = SetorInstitucional.objects.create(nome="Setor 1", unidade_organizacional=unidade1)
    setor2 = SetorInstitucional.objects.create(nome="Setor 2", unidade_organizacional=unidade2)


    response = client.get(f"/alocacao/setor/cidade/{endereco1.cidade}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['setores']) == 1 
    assert response.json()['setores'][0]['nome'] == setor1.nome # setor1 pertence a unidade1 que pertence ao endereco1 com "Cidade teste 1"
    assert response.json()['unidades'] == [unidade1.id]

    response = client.get("/alocacao/setor/cidade/CidadeInexistente/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['setores'] == [] #enderecos não encontrados
