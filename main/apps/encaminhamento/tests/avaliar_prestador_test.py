import pytest
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from apps.alocacao.models import Alocacao, DiaCombinado
from apps.alocacao.serializers import AlocacaoSerializer #Assumindo que este é o serializer correto
from apps.encaminhamento.models import Vaga #Assumindo que a vaga é necessaria
from datetime import datetime


@pytest.mark.django_db
def test_avaliar_prestador_api_view():
    """Testes para a API View AvaliarPrestadorAPIView."""
    client = APIClient()

    # Cria uma vaga e uma alocação para teste
    vaga = Vaga.objects.create(funcao=None) # Substitua None se Vaga requerer dados em Funcao
    alocacao = Alocacao.objects.create(vaga=vaga, tecnico=None) #Substitua None caso necessario

    # Dados para atualização da alocação
    data = {
        "data_apresentacao": timezone.now().isoformat(), # Use timezone.now() para data/hora válida
        "status": "APROVADO",
        "observacao_avaliacao": "Observação de teste",
        "diascombinados": [
            {
                "dia_semana": "SEGUNDA-FEIRA",
                "horario_entrada": "09:00:00", #Formato mais simples
                "horario_saida": "18:00:00"  # Formato mais simples
            }
        ]
    }

    url = f'/alocacao/{alocacao.id}/avaliar/' #Assumindo que esta é sua url


    # Teste de atualização bem-sucedida
    response = client.put(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['status'] == 'APROVADO'
    assert response.json()['observacao_avaliacao'] == 'Observação de teste'
    assert len(response.json()['diascombinados']) == 1


    # Teste com dados inválidos (status inválido)
    data_invalida = {
        "status": "STATUS_INVALIDO",
        "data_apresentacao": timezone.now().isoformat(),
        "observacao_avaliacao": "Outro Teste",
        "diascombinados": []
    }

    response = client.put(url, data=json.dumps(data_invalida), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST  #verifica se a resposta é de erro

    # Teste com alocação inexistente
    url_inexistente = '/alocacao/9999/avaliar/'
    response = client.put(url_inexistente, data=json.dumps(data), content_type='application/json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Alocação não encontrada."}


    # Teste com data_apresentacao no passado (opcional, dependendo da sua validação)
    data_passada = {
        "data_apresentacao": "2023-10-26T19:12:10.876Z", # data passada
        "status": "APROVADO",
        "observacao_avaliacao": "Data passada",
        "diascombinados": []
    }
    response = client.put(url, data=json.dumps(data_passada), content_type='application/json')
    # O resultado deste teste depende da sua lógica de validação para data_apresentacao
    # Se você tem uma validação para impedir data no passado, deve retornar 400.
    # Caso contrario, deve retornar 200.


    # Teste com horarios invalidos (opcional, dependendo da sua validação)
    data_horarios_invalidos = {
        "data_apresentacao": timezone.now().isoformat(),
        "status": "APROVADO",
        "observacao_avaliacao": "Horarios Invalidos",
        "diascombinados": [
            {
                "dia_semana": "SEGUNDA-FEIRA",
                "horario_entrada": "24:00:00", #horario invalido
                "horario_saida": "18:00:00"
            }
        ]
    }
    response = client.put(url, data=json.dumps(data_horarios_invalidos), content_type='application/json')
    # Similarmente, o resultado depende de sua validação.  Se houver validação de horários, deve ser 400.
