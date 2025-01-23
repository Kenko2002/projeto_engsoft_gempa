from .models import (
    Atendimento,
    Observacao,
    Execucao,
    Condicao,
    HistoricoCargaHoraria,
)
from .serializers import (
    AtendimentoReadSerializer, AtendimentoWriteSerializer,
    ObservacaoReadSerializer, ObservacaoWriteSerializer,
    ExecucaoReadSerializer, ExecucaoWriteSerializer,
    CondicaoReadSerializer, CondicaoWriteSerializer,
    HistoricoCargaHorariaReadSerializer, HistoricoCargaHorariaWriteSerializer,AtendimentoSerializer
)


from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_condition import And, Or
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from .pagination import CustomPagination
from rest_framework import generics
from rest_framework import filters
import django_filters.rest_framework
from rest_framework import status




class AtendimentoViewSet(ModelViewSet):
    '''
    é possível desligar a paginação através do seguinte argumento passado via URL:
        atendimento/?no_pagination=true
    '''
    
    #queryset = Atendimento.objects.all()
    queryset = Atendimento.objects.prefetch_related(
        'prestador__enderecos', 'prestador__telefones'
    )
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['horario', 'motivo', 'observacao', 'justificativa_cancelamento']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return AtendimentoReadSerializer
        return AtendimentoWriteSerializer
    
    def get_paginated_response(self, data):
        # Mantém compatibilidade caso a paginação seja desativada.
        if not self.paginator:
            return Response(data)
        return super().get_paginated_response(data)

    def list(self, request, *args, **kwargs):
        # Verifica o parâmetro `no_pagination` na URL.
        no_pagination = request.query_params.get('no_pagination', 'false').lower() == 'true'
        if no_pagination:
            self.pagination_class = None
        return super().list(request, *args, **kwargs)
    

class ObservacaoViewSet(ModelViewSet):
    queryset = Observacao.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['texto', 'link_arquivo']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ObservacaoReadSerializer
        return ObservacaoWriteSerializer

class ExecucaoViewSet(ModelViewSet):
    queryset = Execucao.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['num_processo', 'rji']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ExecucaoReadSerializer
        return ExecucaoWriteSerializer

class CondicaoViewSet(ModelViewSet):
    queryset = Condicao.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['horas_cumpridas_totais', 'flexivel_dia', 'flexivel_horario', 'horas_minimas', 'horas_maximas', 'periodo_dias']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CondicaoReadSerializer
        return CondicaoWriteSerializer
    
    

class HistoricoCargaHorariaViewSet(ModelViewSet):
    queryset = HistoricoCargaHoraria.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['carga_horaria_total', 'data_inicio']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return HistoricoCargaHorariaReadSerializer
        return HistoricoCargaHorariaWriteSerializer



#=============ATENDIMENTO===============#
class AgendarAtendimentoAPIView(APIView):
    """
    API View para agendar um atendimento, associando um técnico e prestador
    a um horário, motivo e observação.
    """
    @swagger_auto_schema(
        request_body=AtendimentoSerializer,
        responses={201: AtendimentoSerializer, 400: 'Bad Request'},
        operation_description="Agendar atendimento entre técnico e prestador",
        operation_summary="Agendar Atendimento"
    )

    def post(self, request):
        # Extração dos dados da requisição
        tecnico_id = request.data.get('tecnico')
        prestador_id = request.data.get('prestador')
        horario = request.data.get('horario')
        motivo = request.data.get('motivo')
        observacao = request.data.get('observacao')

        # Validação dos dados necessários
        if not all([tecnico_id, prestador_id, horario, motivo]):
            return Response({"detail": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Criação do atendimento
        atendimento = Atendimento(
            tecnico_id=tecnico_id,
            prestador_id=prestador_id,
            horario=horario,
            motivo=motivo,
            observacao=observacao,
            status="AGENDADO"  # Status padrão é 'AGENDADO'
        )
        atendimento.save()

        # Serializar a resposta
        serializer = AtendimentoSerializer(atendimento)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
#===================================================#



#==============API VIEW CheckDisponibilidadeTecnico============#

from django.utils.dateparse import parse_datetime
from django.db.models import Q
from apps.socialentity.models import Tecnico
from .models import EnumAtendimentoStatus
from datetime import timedelta

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
import pytz
class CheckAvailabilityView(APIView):
    """
    Verifica a disponibilidade de um técnico para um horário específico.
    Exemplo de entrada:
    tecnico: 2
    horario: 2024-12-05T14:00:00
    """

    def get(self, request, *args, **kwargs):
        # Pega o tecnico_id diretamente da URL
        tecnico_id = kwargs.get('tecnico_id')
        # Pega o horário da query (parâmetros de consulta)
        horario = kwargs.get('horario')

        if not tecnico_id or not horario:
            return Response(
                {"detail": "Parâmetros 'tecnico_id' e 'horario' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Converte o horário recebido para datetime
            horario = parse_datetime(horario)
            if not horario:
                raise ValueError("Formato de horário inválido.")

            # Obtém o técnico pelo ID
            tecnico = Tecnico.objects.get(id=tecnico_id)

            # Converte o horário para o fuso horário de Brasília (UTC-3)
            brasilia_tz = pytz.timezone('America/Sao_Paulo')
            horario_brasilia = horario.astimezone(brasilia_tz)

            # Define o intervalo de verificação (1 hora)
            inicio_intervalo = horario_brasilia
            fim_intervalo = horario_brasilia + timedelta(hours=1)

            # Obtém todos os atendimentos do técnico
            atendimentos = Atendimento.objects.filter(tecnico=tecnico)

            # Verifica se há conflito com os horários de atendimento do técnico
            has_conflict = False
            atendimento_ocupante = None
            
            for atendimento in atendimentos:
                atendimento_fim = atendimento.horario + timedelta(hours=1)

                # Verifica se os horários se sobrepõem
                if (
                    (inicio_intervalo >= atendimento.horario and inicio_intervalo < atendimento_fim) or
                    (fim_intervalo > atendimento.horario and fim_intervalo <= atendimento_fim) or
                    (inicio_intervalo <= atendimento.horario and fim_intervalo >= atendimento_fim)
                ):
                    has_conflict = True
                    atendimento_ocupante=atendimento.id
                    break

            # Formata os horários para exibição com fuso horário
            periodo_verificado_inicio = inicio_intervalo.strftime("%d/%m/%Y - %H:%M:%S")
            periodo_verificado_fim = fim_intervalo.strftime("%d/%m/%Y - %H:%M:%S")



            return Response({
                "disponivel": not has_conflict,
                "periodo_verificado_inicio": periodo_verificado_inicio,
                "periodo_verificado_fim": periodo_verificado_fim,
                "atendimento_ocupante": atendimento_ocupante
            }, status=status.HTTP_200_OK)

        except Tecnico.DoesNotExist:
            return Response(
                {"detail": "Técnico não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "Ocorreu um erro ao processar sua solicitação."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
#==============================================================#





#===========GET TECNICO DISPONIVEL POR HORARIO==================#



class GetTecnicoDisponivelPorHorario(APIView):
    """
    Retorna uma lista de técnicos disponíveis para um horário específico.
    Exemplo de entrada: 2024-12-04T14:00:00
    """

    def get(self, request, *args, **kwargs):
        # Obtém o horário da query (parâmetro de consulta)
        horario =  kwargs.get('horario')
        
        if not horario:
            return Response(
                {"detail": "O parâmetro 'horario' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Converte o horário recebido para datetime
            horario = parse_datetime(horario)
            if not horario:
                raise ValueError("Formato de horário inválido.")

            # Converte o horário para o fuso horário de Brasília (UTC-3)
            brasilia_tz = pytz.timezone('America/Sao_Paulo')
            horario_brasilia = horario.astimezone(brasilia_tz)

            # Define o intervalo de verificação (1 hora)
            inicio_intervalo = horario_brasilia
            fim_intervalo = horario_brasilia + timedelta(hours=1)

            # Obtém todos os técnicos
            tecnicos = Tecnico.objects.all()
            tecnicos_disponiveis = []

            for tecnico in tecnicos:
                # Obtém todos os atendimentos do técnico
                atendimentos = Atendimento.objects.filter(tecnico=tecnico)

                # Verifica se há conflito com os horários de atendimento do técnico
                has_conflict = any(
                    (inicio_intervalo >= atendimento.horario and inicio_intervalo < (atendimento.horario + timedelta(hours=1))) or
                    (fim_intervalo > atendimento.horario and fim_intervalo <= (atendimento.horario + timedelta(hours=1))) or
                    (inicio_intervalo <= atendimento.horario and fim_intervalo >= (atendimento.horario + timedelta(hours=1)))
                    for atendimento in atendimentos
                )

                # Adiciona o técnico à lista de disponíveis se não houver conflitos
                if not has_conflict:
                    tecnicos_disponiveis.append({
                        "id": tecnico.id,
                        "nome": tecnico.nome,
                    })

            return Response({
                "intervalo_verificado": horario_brasilia.strftime("%d/%m/%Y-%H:%M:%S")+' a '+fim_intervalo.strftime("%d/%m/%Y-%H:%M:%S"),
                "tecnicos_disponiveis": tecnicos_disponiveis,
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "Ocorreu um erro ao processar sua solicitação."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



#=========fim GET TECNICO DISPONIVEL POR HORARIO=================#



