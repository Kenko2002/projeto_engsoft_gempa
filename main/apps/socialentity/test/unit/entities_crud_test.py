import pytest
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from apps.socialentity.models import (
    Telefone, Endereco, EntidadeSocial, Usuario, Prestador,
    Tecnico, Fiscal, Coordenador, Responsavel,
    EnumSexoBiologico, EnumPrestadorNaturalidade,
    EnumPrestadorCor, EnumPrestadorReligiao
)



@pytest.mark.django_db
def test_telefone_crud():
    telefone = Telefone.objects.create(numero="987654321", ddd="55")

    # Teste de leitura (já feito na criação)
    assert telefone.numero == "987654321"

    # Teste de update
    telefone.numero = "123456789"
    telefone.save()
    telefone_atualizado = Telefone.objects.get(id=telefone.id)
    assert telefone_atualizado.numero == "123456789"

    # Teste de delete
    telefone.delete()
    with pytest.raises(Telefone.DoesNotExist):
        Telefone.objects.get(id=telefone.id)



@pytest.mark.django_db
def test_endereco_crud():
    endereco = Endereco.objects.create(logradouro="Rua Teste", numero="123", cidade="Cidade Teste")

    # Teste de leitura (já feito na criação)

    # Teste de update
    endereco.logradouro = "Av. Principal"
    endereco.save()
    endereco_atualizado = Endereco.objects.get(id=endereco.id)
    assert endereco_atualizado.logradouro == "Av. Principal"

    # Teste de delete
    endereco.delete()
    with pytest.raises(Endereco.DoesNotExist):
        Endereco.objects.get(id=endereco.id)




@pytest.mark.django_db
def test_prestador_crud():
    prestador = Prestador.objects.create(
        nome="Prestador Teste", identificacao="1234567890", ativo=True
    )


    # Teste de update
    prestador.nome = "Novo Nome Prestador"
    prestador.save()
    prestador_atualizado = Prestador.objects.get(id=prestador.id)
    assert prestador_atualizado.nome == "Novo Nome Prestador"

    # Teste de delete
    prestador.delete()
    with pytest.raises(Prestador.DoesNotExist):
        Prestador.objects.get(id=prestador.id)


@pytest.mark.django_db
def test_usuario_crud():
    user = User.objects.create_user(username='testuser', password='testpassword')
    usuario = Usuario.objects.create(user=user)
    
    # Teste de update
    user.username = "novousuario"
    user.save()
    usuario.refresh_from_db() #atualiza a instancia do usuario com os dados do banco de dados
    assert usuario.user.username == "novousuario"

    # Teste de delete
    usuario.delete()
    user.delete()
    with pytest.raises(Usuario.DoesNotExist):
        Usuario.objects.get(id=usuario.id)
    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=user.id)
    assert telefone in prestador_salvo.telefones.all()
