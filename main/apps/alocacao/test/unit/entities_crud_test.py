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



# Alocacao
@pytest.mark.django_db
def test_alocacao_crud():
    user_tecnico = User.objects.create_user(username='tecnicotest', password='testpassword')
    tecnico = Tecnico.objects.create(user=user_tecnico)
    funcao = Funcao.objects.create(nome="Função Teste")
    vaga = Vaga.objects.create(funcao=funcao)

    alocacao = Alocacao.objects.create(
        prazo_apresentacao=datetime.now().date(),
        tecnico=tecnico,
        vaga=vaga
    )

    # Teste de update
    alocacao.prazo_apresentacao = datetime(2024, 12, 31).date()
    alocacao.save()
    alocacao_atualizada = Alocacao.objects.get(id=alocacao.id)
    assert alocacao_atualizada.prazo_apresentacao == datetime(2024, 12, 31).date()


    # Teste de delete
    alocacao.delete()
    vaga.delete()
    funcao.delete()
    tecnico.delete()
    user_tecnico.delete()
    with pytest.raises(Alocacao.DoesNotExist):
        Alocacao.objects.get(id=alocacao.id)



@pytest.mark.django_db
def test_presenca_crud():

    presenca = Presenca.objects.create(
        checkin = datetime.now(),
        checkout= datetime.now()+timedelta(hours=8)
    )

    # Teste de update
    novo_checkin=datetime.now()+timedelta(days=1)
    presenca.checkin = novo_checkin
    presenca.save()
    presenca_atualizada = Presenca.objects.get(id=presenca.id)
    assert presenca_atualizada.checkin == novo_checkin

    # Teste de delete
    presenca.delete()
    with pytest.raises(Presenca.DoesNotExist):
        Presenca.objects.get(id=presenca.id)


@pytest.mark.django_db
def test_dia_combinado_crud():
    dia_combinado = DiaCombinado.objects.create(
        dia_semana=EnumDiaDaSemana.SEGUNDA_FEIRA,
        horario_entrada=time(8,0),
        horario_saida=time(12,0)
    )


    # Teste de update
    dia_combinado.horario_saida = time(13,0)
    dia_combinado.save()
    dia_combinado_atualizado = DiaCombinado.objects.get(id=dia_combinado.id)
    assert dia_combinado_atualizado.horario_saida == time(13,0)

    # Teste de delete
    dia_combinado.delete()
    with pytest.raises(DiaCombinado.DoesNotExist):
        DiaCombinado.objects.get(id=dia_combinado.id)
