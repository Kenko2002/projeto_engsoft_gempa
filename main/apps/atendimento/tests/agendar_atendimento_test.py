import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.atendimento.models import Atendimento, EnumAtendimentoStatus  # Adjust import path if needed
from apps.socialentity.models import Tecnico, Prestador  # Adjust import path if needed
from datetime import datetime


@pytest.mark.django_db
def test_agendar_atendimento_api_view():
    """Testes para a API View AgendarAtendimentoAPIView."""
    client = APIClient()

    # Cria técnicos e prestadores para o teste
    tecnico = Tecnico.objects.create(user=None) #Substitua None caso necessario
    prestador = Prestador.objects.create(user=None) #Substitua None caso necessario


    # Dados válidos para agendamento
    data_valida = {
        "tecnico": tecnico.id,
        "prestador": prestador.id,
        "horario": datetime(2024, 5, 10, 10, 0, 0).isoformat(),  # Formato ISO 8601
        "motivo": "Teste de agendamento",
        "observacao": "Observação do teste"
    }

    url = reverse('agendar-atendimento')  # Substitua 'agendar-atendimento' pelo nome da sua URL


    response = client.post(url, data=json.dumps(data_valida), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['motivo'] == "Teste de agendamento"
    assert Atendimento.objects.filter(motivo="Teste de agendamento").exists()



    # Dados inválidos (faltando campos obrigatórios)
    data_invalida_faltando_campos = {
        "tecnico": tecnico.id,
        "horario": datetime(2024, 5, 10, 10, 0, 0).isoformat()
    }

    response = client.post(url, data=json.dumps(data_invalida_faltando_campos), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Todos os campos são obrigatórios."}



    # Dados inválidos (IDs inválidos)
    data_invalida_ids = {
        "tecnico": 9999,  # ID de técnico inexistente
        "prestador": prestador.id,
        "horario": datetime(2024, 5, 10, 10, 0, 0).isoformat(),
        "motivo": "Teste de agendamento com ID inválido",
        "observacao": "Observação"
    }

    response = client.post(url, data=json.dumps(data_invalida_ids), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST #O comportamento depende de como seus serializers validam os IDs


    # Dados inválidos (formato de data inválido)
    data_invalida_formato_data = {
        "tecnico": tecnico.id,
        "prestador": prestador.id,
        "horario": "data inválida",  # Formato de data inválido
        "motivo": "Teste de agendamento com formato de data inválido",
        "observacao": "Observação"
    }

    response = client.post(url, data=json.dumps(data_invalida_formato_data), content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST #O comportamento depende de como seus serializers validam o formato de data
