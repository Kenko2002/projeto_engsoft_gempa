import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from socialentity.models import Prestador
from socialentity.serializers import PrestadorSerializer
from faker import Faker
import random

class PrestadorTests(TestCase):
    def setUp(self):
        self.faker = Faker('pt_BR')
        self.client = Client()

        self.prestador_1 = Prestador.objects.create(foto = self.faker.first_name(), rg = self.faker.first_name(), nome_social = self.faker.first_name(), escolaridade = self.faker.first_name(), situacao_economica = self.faker.first_name(), descricao_avaliacao_psicosocial = self.faker.first_name())
        self.prestador_2 = Prestador.objects.create(foto = self.faker.first_name(), rg = self.faker.first_name(), nome_social = self.faker.first_name(), escolaridade = self.faker.first_name(), situacao_economica = self.faker.first_name(), descricao_avaliacao_psicosocial = self.faker.first_name())
        self.prestador_3 = Prestador.objects.create(foto = self.faker.first_name(), rg = self.faker.first_name(), nome_social = self.faker.first_name(), escolaridade = self.faker.first_name(), situacao_economica = self.faker.first_name(), descricao_avaliacao_psicosocial = self.faker.first_name())

        self.valid_payload = {
            'foto' : self.faker.first_name(),'rg' : self.faker.first_name(),'nome_social' : self.faker.first_name(),'escolaridade' : self.faker.first_name(),'situacao_economica' : self.faker.first_name(),'descricao_avaliacao_psicosocial' : self.faker.first_name()
        }
        self.invalid_payload = {
            'foto' : self.faker.first_name(),'rg' : self.faker.first_name(),'nome_social' : self.faker.first_name(),'escolaridade' : self.faker.first_name(),'situacao_economica' : self.faker.first_name(),'descricao_avaliacao_psicosocial' : self.faker.first_name()
        }

    def test_valid_create(self):
        response = self.client.post(
            reverse('prestador-api-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create(self):
        response = self.client.post(
            reverse('prestador-api-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_upload(self):
        response = self.client.put(
            reverse('prestador-detail',
            kwargs={'pk': self.prestador_1.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_upload(self):
        response = self.client.put(
            reverse('prestador-detail',
            kwargs={'pk': self.prestador_1.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # retornando todos os elementos    
    def test_retrieve_all(self):
        response   = self.client.get(reverse('prestador-api-list'))
        data       = Prestador.objects.all()
        serializer = PrestadorSerializer(data, context={'request': None}, many=True)
        # Aqui deve comparar todos os compos do objeto com serialização
        self.assertEqual(response.data, serializer.data)

        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retornando um elemento
    def test_valid_get_element(self):
        response = self.client.get(reverse('prestador-detail',kwargs={'pk': self.prestador_1.id}))
        data = Prestador.objects.get(pk=self.condicao_1.id)
        # Aqui deve comparar todos os campos do objeto com serialização
        self.assertEqual(str(data.uuid),response.data['uuid'])
        self.assertIsNotNone(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # erro ao retornar um elemento invalido
    def test_invalid_get_element(self):
        response = self.client.get(reverse('prestador-detail',kwargs={'pk': 666}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Delete um elemento valido
    def test_valid_delete(self):
        response = self.client.delete(reverse('prestador-detail',kwargs={'pk': self.prestador_1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Delete um elemento valido
    def test_invalid_delete(self):
        response = self.client.delete(reverse('prestador-detail',kwargs={'pk': 666}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
