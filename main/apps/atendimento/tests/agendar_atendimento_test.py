import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.atendimento.models import Atendimento, EnumAtendimentoStatus  # Adjust import path if needed
from apps.socialentity.models import Tecnico, Prestador  # Adjust import path if needed
from datetime import datetime

import json
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_agendar_atendimento_api_view():
    """Testes para a API View AgendarAtendimentoAPIView."""
    client = APIClient()


    user_tecnico = User.objects.create_user(username='tecnicotest', password='testpassword')
    tecnico = Tecnico.objects.create(user=user_tecnico)

    prestador = Prestador.objects.create(nome="Prestador Teste", identificacao="1234567890", ativo=True)
    #atendimento = Atendimento.objects.create(
    #    horario=datetime(2024, 1, 1, 10, 0, 0),
    #    motivo="Motivo Teste",
    #    tecnico=tecnico,
    #    prestador=prestador
    #)
    

    # Dados válidos para agendamento
    data_valida = {
        "tecnico": tecnico.id,
        "prestador": prestador.id,
        "horario": datetime(2024, 5, 10, 10, 0, 0).isoformat(),  # Formato ISO 8601
        "motivo": "Teste de agendamento",
        "observacao": "Observação do teste"
    }

    url = reverse('agendar_atendimento')  # Substitua 'agendar-atendimento' pelo nome da sua URL


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




