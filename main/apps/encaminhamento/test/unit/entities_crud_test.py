import pytest
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from apps.socialentity.models import (
    Telefone, Endereco, EntidadeSocial, Usuario, Prestador,
    Tecnico, Fiscal, Coordenador, Responsavel
)
from apps.encaminhamento.models import (
    Instituicao, UnidadeOrganizacional, SetorInstitucional,
    Vaga, Funcao
)
from apps.atendimento.models import (
    Atendimento, Observacao, Execucao, Condicao,
    HistoricoCargaHoraria, EnumAtendimentoStatus, EnumPrestacaoStatus, EnumTipoProcessual
)
from apps.alocacao.models import (
    Alocacao, Presenca, DiaCombinado, EnumStatusAlocacao, EnumDiaDaSemana
)
from datetime import timedelta, time, datetime

# Encaminhamento


@pytest.mark.django_db
def test_instituicao_crud():
    instituicao = Instituicao.objects.create(nome="Instituição Teste", identificacao="1234567890", ativo=True)

    # Teste de update
    instituicao.nome = "Novo Nome Instituição"
    instituicao.save()
    instituicao_atualizada = Instituicao.objects.get(id=instituicao.id)
    assert instituicao_atualizada.nome == "Novo Nome Instituição"

    # Teste de delete
    instituicao.delete()
    with pytest.raises(Instituicao.DoesNotExist):
        Instituicao.objects.get(id=instituicao.id)


@pytest.mark.django_db
def test_unidade_organizacional_crud():
    unidade = UnidadeOrganizacional.objects.create(
        nome="Unidade Teste", identificacao="1234567890", ativo=True,
        hora_abertura=time(8, 0), hora_fechamento=time(17, 0)
    )

    # Teste de update
    unidade.nome = "Nova Unidade"
    unidade.save()
    unidade_atualizada = UnidadeOrganizacional.objects.get(id=unidade.id)
    assert unidade_atualizada.nome == "Nova Unidade"

    # Teste de delete
    unidade.delete()
    with pytest.raises(UnidadeOrganizacional.DoesNotExist):
        UnidadeOrganizacional.objects.get(id=unidade.id)


@pytest.mark.django_db
def test_setor_institucional_crud():
    user = User.objects.create_user(username='testuser', password='testpassword')
    responsavel = Responsavel.objects.create(user=user)
    setor = SetorInstitucional.objects.create(nome="Setor Teste", responsavel=responsavel)


    # Teste de update
    setor.nome = "Novo Setor"
    setor.save()
    setor_atualizado = SetorInstitucional.objects.get(id=setor.id)
    assert setor_atualizado.nome == "Novo Setor"

    # Teste de delete
    setor.delete()
    responsavel.delete()
    user.delete()

    with pytest.raises(SetorInstitucional.DoesNotExist):
        SetorInstitucional.objects.get(id=setor.id)

@pytest.mark.django_db
def test_vaga_crud():
    funcao = Funcao.objects.create(nome="Função Teste")
    vaga = Vaga.objects.create(funcao=funcao)


    # Teste de update
    funcao.nome="Nova função"
    funcao.save()

    vaga.refresh_from_db()
    assert vaga.funcao.nome == "Nova função"

    # Teste de delete
    vaga.delete()
    funcao.delete()
    with pytest.raises(Vaga.DoesNotExist):
        Vaga.objects.get(id=vaga.id)


@pytest.mark.django_db
def test_funcao_crud():
    funcao = Funcao.objects.create(nome="Função Teste")


    # Teste de update
    funcao.nome = "Nova Função"
    funcao.save()
    funcao_atualizada = Funcao.objects.get(id=funcao.id)
    assert funcao_atualizada.nome == "Nova Função"

    # Teste de delete
    funcao.delete()
    with pytest.raises(Funcao.DoesNotExist):
        Funcao.objects.get(id=funcao.id)
