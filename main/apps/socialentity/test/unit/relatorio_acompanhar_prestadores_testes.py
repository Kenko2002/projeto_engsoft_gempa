import pytest
import requests
from datetime import timedelta, datetime

import os
diretorio_atual = os.getcwd()
print(f"Diretório atual: {os.getcwd()}")
diretorio_superior = diretorio_atual
for _ in range(4):
    diretorio_superior = os.path.dirname(diretorio_superior)

print(f"Diretório 4 níveis acima: {diretorio_superior}")

from ....atendimento.models import Condicao, HistoricoCargaHoraria, Execucao # Importe os models necessários
from ....alocacao.models import Alocacao, Presenca
from ....encaminhamento.models import Vaga, Instituicao, SetorInstitucional, UnidadeOrganizacional, Funcao
from ....socialentity.models import Prestador, Tecnico, Endereco, Telefone, Usuario

# ... (seu código de teste anterior)

@pytest.mark.django_db  # Adiciona esta linha para usar o banco de dados de teste
def test_condicao_endpoint():
    """Testa o endpoint /area-tecnico/condicao/."""

    # Criação de objetos de teste
    usuario_prestador = Usuario.objects.create_user(username='prestador', password='password')
    prestador = Prestador.objects.create(user=usuario_prestador)
    usuario_tecnico = Usuario.objects.create_user(username='tecnico', password='password')
    tecnico = Tecnico.objects.create(user=usuario_tecnico)


    instituicao = Instituicao.objects.create(nome="Instituicao Teste")
    setor = SetorInstitucional.objects.create(nome="Setor Teste", instituicao=instituicao)
    unidade = UnidadeOrganizacional.objects.create(nome="Unidade Teste")
    funcao = Funcao.objects.create(nome="Funcao Teste")

    vaga = Vaga.objects.create(
        titulo="Vaga Teste",
        descricao = "descricao teste",
        quantidade_vagas = 10,
        requisitos = "requisitos teste",
        publico_alvo = "publico alvo teste",
        escolaridade = "escolaridade teste",
        carga_horaria_semanal = 40,
        salario = 1000.00,
        beneficios = "beneficios teste",
        data_limite_inscricao = datetime.now().date(),
        instituicao = instituicao,
        setor_institucional = setor,
        unidade_organizacional = unidade,
        funcao = funcao,
    )

    historico = HistoricoCargaHoraria.objects.create(carga_horaria_total=40, data_inicio=datetime.now().date())
    condicao = Condicao.objects.create(horas_minimas=20, horas_maximas=40, periodo_dias=30, tipo_processual='PRD')
    condicao.historico_carga_horaria.add(historico)

    execucao = Execucao.objects.create(num_processo="12345", rji="67890", prestador=prestador, status="ATIVA")
    execucao.condicoes.add(condicao)

    alocacao = Alocacao.objects.create(
        prazo_apresentacao=datetime.now().date(),
        vigencia_inicio=datetime.now().date(),
        vigencia_fim=datetime.now().date(),
        status='AGUARDANDO_ENTREVISTA',
        tecnico=tecnico,
        vaga=vaga
    )
    alocacao.condicoes.add(condicao)

    presenca = Presenca.objects.create(checkin=datetime.now(), checkout=datetime.now() + timedelta(hours=8))
    alocacao.presencas.add(presenca)

    url = "http://localhost:8000/area-tecnico/condicao/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Resposta do servidor:")
        print(response.text)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0, "A lista não deveria estar vazia"  # Nova asserção

        # Adicione mais asserções para verificar o conteúdo da lista

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        assert False, f"Erro na requisição: {e}"
