import pytest
import json
from django.db import transaction
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from apps.socialentity.models import Tecnico



@pytest.mark.django_db
def test_cadastro_and_login(client):
    with transaction.atomic():
        cadastro_data = {
            "identificacao": "1234567890",
            "email_contato": "tecnico@teste.com",
            "password": "testpassword",
            "first_name": "Nome",
            "last_name": "Sobrenome",
        }

        url = reverse("cadastro_tecnico")  # Use reverse para obter a URL

        response = client.post(url, data=json.dumps(cadastro_data), content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED, f"Resposta inesperada: {response.content}" #Asserção completa
        assert Tecnico.objects.filter(email_contato=cadastro_data["email_contato"]).exists()
        assert User.objects.filter(username=cadastro_data["email_contato"]).exists()

        # Parte do login (adicionada do exemplo anterior)
        login_data = {
            "username": cadastro_data["email_contato"],
            "password": cadastro_data["password"],
        }
        url_login = reverse("login")  # Substitua 'login' pelo nome da URL de login
        response_login = client.post(
            url_login, data=json.dumps(login_data), content_type="application/json"
        )
        assert response_login.status_code == status.HTTP_200_OK
        assert "token" in response_login.json()
