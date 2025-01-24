import pytest
from django.db import IntegrityError 
from django.contrib.auth.models import User
from apps.socialentity.models import (
    Telefone, Endereco, EntidadeSocial, Usuario, Prestador,
    Tecnico, Fiscal, Coordenador, Responsavel,
    EnumSexoBiologico, EnumPrestadorNaturalidade,
    EnumPrestadorCor, EnumPrestadorReligiao
)

@pytest.mark.django_db
def test_criar_telefone():
    # Instanciando e salvando o telefone
    telefone = Telefone(numero="987654321", ddd="55")
    telefone.save()

    # Recuperando do banco de dados e verificando os valores
    telefone_salvo = Telefone.objects.get(id=telefone.id)
    assert telefone_salvo.numero == "987654321"
    assert telefone_salvo.ddd == "55"
    assert str(telefone_salvo) == "+55 987654321"
    
    # Exibindo o telefone no console
    print(f"Telefone salvo: ID={telefone_salvo.id}, DDD={telefone_salvo.ddd}, Número={telefone_salvo.numero}")

@pytest.mark.django_db
def test_criar_endereco():
    endereco = Endereco(
        logradouro="Rua Teste", numero="123", complemento="Apto 4",
        bairro="Bairro Teste", cidade="Cidade Teste", estado="CE", cep="60000000"
    )
    endereco.save()

    endereco_salvo = Endereco.objects.get(id=endereco.id)
    assert str(endereco_salvo) == "Rua Teste, 123 - Bairro Teste, Cidade Teste/CE"

@pytest.mark.django_db
def test_criar_prestador():
    prestador = Prestador(
        nome="Prestador Teste", identificacao="1234567890", ativo=True,
        email_contato="prestador@teste.com", rg="987654321",
        nome_social="Nome Social Teste", escolaridade="Ensino Médio",
        situacao_economica="Empregado",
        descricao_avaliacao_psicosocial="Avaliação Psicosocial Teste",
        naturalidade=EnumPrestadorNaturalidade.BRASILEIRO,
        cor=EnumPrestadorCor.PARDO,
        religiao=EnumPrestadorReligiao.EVANGELICO,
        sexo_biologico=EnumSexoBiologico.MASCULINO
    )
    prestador.save()

    prestador_salvo = Prestador.objects.get(id=prestador.id)
    assert str(prestador_salvo) == "Prestador Teste"


@pytest.mark.django_db
def test_criar_usuario_e_subtipos():
    user = User.objects.create_user(username='testuser', password='testpassword')

    def criar_e_testar_usuario(tipo_usuario, expected_str):
        usuario = tipo_usuario(user=user)
        usuario.save()
        usuario_salvo = tipo_usuario.objects.get(id=usuario.id)
        assert str(usuario_salvo) == expected_str
        user.delete() #remove o usuário após o teste

    criar_e_testar_usuario(Usuario, 'testuser')
    user = User.objects.create_user(username='testuser', password='testpassword') #cria novamente
    criar_e_testar_usuario(Tecnico, "Técnico: testuser")
    user = User.objects.create_user(username='testuser', password='testpassword') #cria novamente
    criar_e_testar_usuario(Fiscal, "Fiscal: testuser")
    user = User.objects.create_user(username='testuser', password='testpassword') #cria novamente
    criar_e_testar_usuario(Coordenador, "Coordenador: testuser")
    user = User.objects.create_user(username='testuser', password='testpassword') #cria novamente
    criar_e_testar_usuario(Responsavel, "Responsável: testuser")



@pytest.mark.django_db
def test_entidade_social_relacionamentos():
    endereco = Endereco.objects.create(logradouro="Rua Teste", numero="123")
    telefone = Telefone.objects.create(numero="987654321", ddd="85")
    prestador = Prestador.objects.create(nome="Prestador Teste")

    prestador.enderecos.add(endereco)
    prestador.telefones.add(telefone)
    prestador.save()

    prestador_salvo = Prestador.objects.get(id=prestador.id)
    assert endereco in prestador_salvo.enderecos.all()
    assert telefone in prestador_salvo.telefones.all()
