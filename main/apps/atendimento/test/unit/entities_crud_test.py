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


# Atendimento


@pytest.mark.django_db
def test_atendimento_crud():
    user_tecnico = User.objects.create_user(username='tecnicotest', password='testpassword')
    tecnico = Tecnico.objects.create(user=user_tecnico)

    prestador = Prestador.objects.create(nome="Prestador Teste", identificacao="1234567890", ativo=True)
    atendimento = Atendimento.objects.create(
        horario=datetime(2024, 1, 1, 10, 0, 0),
        motivo="Motivo Teste",
        tecnico=tecnico,
        prestador=prestador
    )


    # Teste de update
    atendimento.motivo = "Novo Motivo"
    atendimento.save()
    atendimento_atualizado = Atendimento.objects.get(id=atendimento.id)
    assert atendimento_atualizado.motivo == "Novo Motivo"

    # Teste de delete
    atendimento.delete()
    prestador.delete()
    tecnico.delete()
    user_tecnico.delete()

    with pytest.raises(Atendimento.DoesNotExist):
        Atendimento.objects.get(id=atendimento.id)


@pytest.mark.django_db
def test_observacao_crud():
    observacao = Observacao.objects.create(texto="Observação Teste")


    # Teste de update
    observacao.texto = "Nova Observação"
    observacao.save()
    observacao_atualizada = Observacao.objects.get(id=observacao.id)
    assert observacao_atualizada.texto == "Nova Observação"

    # Teste de delete
    observacao.delete()
    with pytest.raises(Observacao.DoesNotExist):
        Observacao.objects.get(id=observacao.id)


@pytest.mark.django_db
def test_execucao_crud():
    prestador = Prestador.objects.create(nome="Prestador Teste", identificacao="1234567890", ativo=True)

    execucao = Execucao.objects.create(
        num_processo="1234567890",
        prestador=prestador
    )


    # Teste de update
    execucao.num_processo = "0987654321"
    execucao.save()
    execucao_atualizada = Execucao.objects.get(id=execucao.id)
    assert execucao_atualizada.num_processo == "0987654321"

    # Teste de delete
    execucao.delete()
    prestador.delete()
    with pytest.raises(Execucao.DoesNotExist):
        Execucao.objects.get(id=execucao.id)


@pytest.mark.django_db
def test_condicao_crud():
    condicao = Condicao.objects.create(horas_minimas=20, horas_maximas=40)

    # Teste de update
    condicao.horas_minimas = 30
    condicao.save()
    condicao_atualizada = Condicao.objects.get(id=condicao.id)
    assert condicao_atualizada.horas_minimas == 30

    # Teste de delete
    condicao.delete()
    with pytest.raises(Condicao.DoesNotExist):
        Condicao.objects.get(id=condicao.id)



@pytest.mark.django_db
def test_historico_carga_horaria_crud():
    historico = HistoricoCargaHoraria.objects.create(
        carga_horaria_total=100,
        data_inicio=datetime.now().date()
    )



    # Teste de update
    historico.carga_horaria_total = 120
    historico.save()
    historico_atualizado = HistoricoCargaHoraria.objects.get(id=historico.id)
    assert historico_atualizado.carga_horaria_total == 120

    # Teste de delete
    historico.delete()
    with pytest.raises(HistoricoCargaHoraria.DoesNotExist):
        HistoricoCargaHoraria.objects.get(id=historico.id)


