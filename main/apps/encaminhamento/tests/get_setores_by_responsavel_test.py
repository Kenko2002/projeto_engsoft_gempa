import pytest
import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.db import transaction
from apps.socialentity.models import Responsavel # Importe o modelo Responsavel


@pytest.mark.django_db
def test_cadastro_and_login_responsavel(client: APIClient):  # Adicione tipo para client
    with transaction.atomic():
        cadastro_data = {
            "identificacao": "12345678901",  # CPF - Único
            "email_contato": "responsavel@teste.com",  # Email - Único
            "password": "testpassword",
            "first_name": "NomeResponsavel",
            "last_name": "SobrenomeResponsavel",
        }

        url = "/cadastro/responsavel/"  # URL correta

        response = client.post(url, data=json.dumps(cadastro_data), content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED, f"Resposta inesperada: {response.content}"
        assert Responsavel.objects.filter(email_contato=cadastro_data["email_contato"]).exists()

        # Login
        login_data = {
            "username": cadastro_data["first_name"] + " " + cadastro_data["last_name"],
            "password": cadastro_data["password"],
        }

        url_login =  "/login"  # Ou o nome da sua URL de login se diferente
        response_login = client.post(url_login, data=json.dumps(login_data), content_type="application/json")

        assert response_login.status_code == status.HTTP_200_OK
        assert "token" in response_login.json()
