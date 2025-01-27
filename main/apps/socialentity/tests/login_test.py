import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from apps.socialentity.models import Tecnico  # Importe o modelo Tecnico
from django.urls import reverse


@pytest.mark.django_db
def test_login_successful(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    usuario = Tecnico.objects.create(user=user, nome="Teste Nome", ativo=True)  # Crie um Técnico associado
    group, created = Group.objects.get_or_create(name="Coordenador")
    user.groups.add(group)

    data = {'username': 'testuser', 'password': 'testpassword'}
    url = reverse('login')  # Use reverse para obter a URL
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert response.data['message'] == 'Login successful'
    assert response.data['user_group'] == ['Coordenador']
    assert response.data['id'] == usuario.id
    assert response.data['nome'] == usuario.nome



@pytest.mark.django_db
def test_login_invalid_credentials(client):
    data = {'username': 'testuser', 'password': 'wrongpassword'}
    url = reverse('login')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == {'detail': 'Username or Password is incorrect'}



@pytest.mark.django_db
def test_login_missing_fields(client):
    url = reverse('login')
    response = client.post(url, {}, format='json')  # Dados vazios

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'detail': 'Username and Password are required!'}




@pytest.mark.django_db
def test_login_inactive_user(client):
    user = User.objects.create_user(username='inactiveuser', password='testpassword')
    Tecnico.objects.create(user=user, nome="Teste Nome", ativo=False)

    data = {'username': 'inactiveuser', 'password': 'testpassword'}
    url = reverse('login')
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {'detail': 'Esse Usuário está Inativo. Contate o SSP'}



@pytest.mark.django_db
def test_cadastro_tecnico_successful(client):
    url = reverse('cadastro-tecnico-list') # Nome da URL invertido
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email_contato": "john.doe@example.com",  # Adicione o email
        "password": "testpassword",  # Inclua a senha
        # ... other fields ...
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="John Doe").exists()
    assert Tecnico.objects.filter(user__username="John Doe").exists()
    user = User.objects.get(username="John Doe")
    assert user.groups.filter(name='Tecnico').exists()



@pytest.mark.django_db
def test_cadastro_tecnico_missing_password(client):
    url = reverse('cadastro-tecnico-list')
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email_contato": "john.doe@example.com",
        # "password" field missing
        # ... other fields ...
    }
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password' in response.data  # Verifique se o erro está relacionado à senha
    assert response.data['password'] == ['A senha é obrigatória para criar um Técnico.']
