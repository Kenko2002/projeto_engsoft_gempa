

import pytest
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from django.utils.timezone import localtime, make_aware, timedelta
from apps.socialentity.models import (
    Telefone, Endereco, EntidadeSocial, Usuario, Prestador,
    Tecnico, Fiscal, Coordenador, Responsavel,
    EnumSexoBiologico, EnumPrestadorNaturalidade,
    EnumPrestadorCor, EnumPrestadorReligiao
)
from apps.atendimento.models import Execucao, Condicao
from apps.alocacao.models import Alocacao, Presenca
from apps.encaminhamento.models import SetorInstitucional, Vaga, Funcao


@pytest.mark.django_db
def test_criar_prestador_completo():
    try:
        with transaction.atomic():  # Para garantir que tudo seja criado ou nada
            # Criando entidades relacionadas
            funcao = Funcao.objects.create(nome="Função Teste")
            vaga = Vaga.objects.create(funcao=funcao)
            setor = SetorInstitucional.objects.create(nome="Setor Teste")
            setor.vagas.add(vaga)
            user_tecnico = User.objects.create_user(username='tecnico', password='testpassword')
            tecnico = Tecnico.objects.create(user=user_tecnico)

            prestador = Prestador.objects.create(
                nome="Renzo",
                # ... outros campos do prestador ...
            )

            condicao = Condicao.objects.create(horas_maximas=100)  # 100 horas na condição
            execucao = Execucao.objects.create(prestador=prestador)
            execucao.condicoes.add(condicao)

            alocacao = Alocacao.objects.create(
                vaga=vaga,
                tecnico=tecnico,
                # ... outros campos da alocação ...
            )

            # Adicionando presenças (5h cada, totalizando 50h - metade da condição)

            #checkin_inicial = make_aware(localtime().replace(hour=8, minute=0, second=0, microsecond=0)) #checkin as 8 da manha
            checkin_inicial = localtime().replace(hour=8, minute=0, second=0, microsecond=0)

            for i in range(10):
                checkin = checkin_inicial + timedelta(days=i)
                checkout = checkin + timedelta(hours=5)  # checkout às 13h
                # Cria a presença
                presenca = Presenca.objects.create(checkin=checkin, checkout=checkout)
                # Adiciona a presença à alocação
                alocacao.presencas.add(presenca)
            alocacao.save()
            
            # Relacionando tudo
            prestador.save()

            # Printando o prestador (o __str__ deve funcionar corretamente)
            print("Nome do prestador criado: ")
            print(prestador)
            print("Nome da alocação criada:")
            print(alocacao)
            print("Presenças criadas:")
            print(alocacao.presencas)
            

    except Exception as e:
        print(f"Erro durante a criação do prestador completo: {e}")
        pytest.fail("Falha ao criar o prestador completo.")  # Falha no teste se houver erro
