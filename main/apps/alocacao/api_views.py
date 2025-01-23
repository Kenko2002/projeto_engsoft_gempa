from .models import (
    Alocacao,Presenca,DiaCombinado
)
from .serializers import (
    AlocacaoReadSerializer, AlocacaoWriteSerializer, 
    PresencaReadSerializer, PresencaWriteSerializer, 
    DiaCombinadoReadSerializer,DiaCombinadoWriteSerializer, CheckinSerializer,
    CheckoutSerializer,AlocacaoSerializer,CheckoutComHoraSerializer,PrestadorSerializer
)

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
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.utils.timezone import localdate
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

from apps.encaminhamento.models import SetorInstitucional

from rest_framework import status as http_status



        
class AlocacaoBySetorAndStatusView(APIView):
    '''
    Lista todos os Prestadores encaminhados a um Setor com seus IDs de alocação, execução e condição associados.
    Recebe Id do setor e qual é o Status buscado, e retorna os detalhes necessários.
    '''
    def get(self, request, *args, **kwargs):
        setor_id = kwargs.get('setor_id')
        status_alocacao = kwargs.get('status')
        
        try:
            setor = SetorInstitucional.objects.get(id=setor_id)
        except SetorInstitucional.DoesNotExist:
            return Response({"detail": "Setor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        alocacoes = Alocacao.objects.filter(
            vaga__setores_institucionais=setor,
            status=status_alocacao
        )

        if not alocacoes.exists():
            return Response({"detail": "Nenhuma alocação encontrada para este setor e status."}, status=status.HTTP_404_NOT_FOUND)

        from apps.atendimento.models import Execucao, Condicao

        prestador_detalhes = []
        for alocacao in alocacoes:
            condicoes = Condicao.objects.filter(alocacoes=alocacao)
            for condicao in condicoes:
                execucoes = Execucao.objects.filter(condicoes=condicao)
                for execucao in execucoes:
                    if execucao.prestador:
                        prestador_detalhes.append({
                            "prestador_id": execucao.prestador.id,
                            "alocacao_id": alocacao.id,
                            "execucao_id": execucao.id,
                            "condicao_id": condicao.id,
                            "nome_social": execucao.prestador.nome_social,
                            "foto": execucao.prestador.foto if execucao.prestador.foto else None,
                            "rg": execucao.prestador.rg,
                            "escolaridade": execucao.prestador.escolaridade,
                            "situacao_economica": execucao.prestador.situacao_economica,
                        })

        if not prestador_detalhes:
            return Response({'detail': 'Nenhum prestador encontrado para as alocações filtradas.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(prestador_detalhes, status=status.HTTP_200_OK)
    


class AlocacaoViewSet(ModelViewSet):
    queryset = Alocacao.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, 
                              SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['prazo_apresentacao', 'data_apresentacao', 
                     'vigencia_inicio', 'vigencia_fim']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return AlocacaoReadSerializer
        return AlocacaoWriteSerializer

class PresencaViewSet(ModelViewSet):
    queryset = Presenca.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['checkin', 'checkout', 'observacao_checkin', 'observacao_checkout']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PresencaReadSerializer
        return PresencaWriteSerializer


class DiaCombinadoViewSet(ModelViewSet):
    queryset = DiaCombinado.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['dia_semana', 'horario_entrada', 'horario_saida']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return DiaCombinadoReadSerializer
        return DiaCombinadoWriteSerializer



#===============CHECKIN CHECKOUT API VIEW==================#

class CheckinAPIView(APIView):
    """
    API para registrar um check-in associado a uma alocação.
    """
    model_class = None  # Defina a classe do modelo na subclasse

    @swagger_auto_schema(
        operation_description="Faz Check In de uma Alocação de um Prestador",
        request_body=CheckinSerializer,  # Define o formato do corpo da requisição
        responses={
            200: openapi.Response(
                description="Checkin criado com Sucesso.",
                examples={
                    "application/json": {"id": 1}
                }
            ),
            400: "Erro na validação dos dados.",
            404: "Entidade não encontrada.",
        },
    )
    def post(self, request, alocacao_id):
        try:
            alocacao = Alocacao.objects.get(id=alocacao_id)

            # Verifica se o último check-in da alocação já tem um check-out
            ultima_presenca = alocacao.presencas.filter(checkout__isnull=True).last()
            if ultima_presenca:
                return Response(
                    {"error": "O último check-in não possui check-out. Faça o check-out antes de registrar um novo check-in."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Captura os dados do corpo da requisição
            data = request.data
            checkin_time = data.get('checkin', None)
            observacao_checkin = data.get('observacao_checkin', '')
            hora_cadastro_checkin=now()

            # Define o horário de check-in como o atual se não for fornecido
            if not checkin_time:
                checkin_time = now()

            # Criação do objeto de Presença
            presenca = Presenca.objects.create(
                checkin=checkin_time,
                observacao_checkin=observacao_checkin,
                hora_cadastro_checkin= hora_cadastro_checkin
            )
            alocacao.presencas.add(presenca)
            alocacao.save()

            # Serializa os dados da presença criada
            serializer = CheckinSerializer(presenca)

            return Response(
                {"message": "Check-in registrado com sucesso.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Alocacao.DoesNotExist:
            return Response(
                {"error": "Alocação não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": f"Ocorreu um erro ao registrar o check-in: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



import pytz
from datetime import datetime
class CheckoutAPIView(APIView):
    """
    API para registrar o check-out associado ao último check-in de uma alocação na data atual.
    Esse endpoint permite edição de hora.
    """
    def post(self, request, alocacao_id):
        from datetime import timedelta
        try:
            alocacao = Alocacao.objects.get(id=alocacao_id)

            # Busca da última Presença com checkin
            presenca = alocacao.presencas.order_by('-id').first()

            if not presenca:
                return Response(
                    {"error": "Nenhum check-in encontrado para hoje nessa alocação."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if presenca.checkout:
                return Response(
                    {"error": "Esse Checkout Já foi Fechado!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Captura observações do corpo da requisição
            observacao_checkout = request.data.get('observacao_checkout', '')
            tempo_intervalo = request.data.get('tempo_intervalo')  # Espera um valor em HH:MM:SS
            checkout = request.data.get("checkout")
            hora_cadastro_checkout = now()

            if tempo_intervalo:
                try:
                    # Parseando o tempo fornecido no formato HH:MM:SS
                    horas, minutos, segundos = map(int, tempo_intervalo.split(":"))
                    tempo_intervalo = timedelta(hours=horas, minutes=minutos, seconds=segundos)
                except ValueError:
                    return Response(
                        {"error": "Formato de 'tempo_intervalo' inválido. Use o formato HH:MM:SS."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Convertendo o campo checkout para o fuso horário de São Paulo
            if checkout:
                # Converte para datetime (assumindo que o 'checkout' esteja no formato ISO 8601)
                checkout_utc = datetime.fromisoformat(checkout.replace("Z", "+00:00"))  # UTC timezone
                sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
                checkout_sao_paulo = checkout_utc.astimezone(sao_paulo_tz)
                checkout = checkout_sao_paulo

            # Atualiza o horário de checkout e a observação
            presenca.checkout = checkout
            presenca.observacao_checkout = observacao_checkout
            presenca.hora_cadastro_checkout = hora_cadastro_checkout
            presenca.tempo_intervalo = tempo_intervalo  # Atribuindo o timedelta

            # Atualizações para calcular o tempo trabalhado
            if isinstance(presenca.checkin, str):
                presenca.checkin = datetime.fromisoformat(presenca.checkin)
            if isinstance(presenca.checkout, str):
                presenca.checkout = datetime.fromisoformat(presenca.checkout)

            if isinstance(tempo_intervalo, str):
                horas, minutos, segundos = map(int, tempo_intervalo.split(':'))
                presenca.tempo_intervalo = timedelta(hours=horas, minutes=minutos, seconds=segundos)

            # Calcula o tempo trabalhado
            tempo_trabalhado = presenca.checkout - presenca.checkin - presenca.tempo_intervalo

            # Verifica se o tempo trabalhado é negativo
            if tempo_trabalhado.total_seconds() < 0:
                return Response(
                    {"error": "O tempo trabalhado não pode ser negativo."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Formatação do tempo trabalhado
            total_seconds = int(tempo_trabalhado.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            tempo_trabalhado_formatado = {"horas": hours, "minutos": minutes, "segundos": seconds}

            # Verifica se o tempo trabalhado é inferior a 8 horas
            if tempo_trabalhado > timedelta(hours=8):
                return Response(
                    {"error": "O tempo trabalhado não deve ser igual ou maior a 8 horas.", "checkin": presenca.checkin, "tempo_total": tempo_trabalhado_formatado},
                    status=status.HTTP_400_BAD_REQUEST
                )

            presenca.save()

            # Serializa os dados da presença atualizada
            serializer = CheckoutSerializer(presenca)

            return Response(
                {"message": "Check-out registrado com sucesso.", "tempo_trabalhado": tempo_trabalhado_formatado, "data": serializer.data},
                status=status.HTTP_200_OK
            )

        except Alocacao.DoesNotExist:
            return Response(
                {"error": "Alocação não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": f"Ocorreu um erro ao registrar o check-out: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
#===============FIM CHECKIN CHECKOUT API VIEW==================#


#===============GET ULTIMA PRESENCA BY ALOCACAO API VIEW=========#
class GetLastPresencaByAlocacaoAPIView(APIView):
    """
    API View para, dado uma Alocacao, Encontrar a Última presença dela.
    """
    @swagger_auto_schema(
        operation_description="API View para, dado uma Alocacao, Encontrar a Última presença dela.",
         # Define o formato do corpo da requisição
        responses={
            200: openapi.Response(
                description="Presenca encontrada!",
                examples={
                    "application/json": {"id": 1}
                }
            ),
            400: "Erro na validação dos dados.",
            404: "Entidade não encontrada.",
        },
    )
    
    def get(self, request, alocacao_id):
        try:
            alocacao = Alocacao.objects.get(id=alocacao_id)

            if not alocacao:
                return Response(
                    {"error": "Nenhuma Alocacao encontrada com esse ID."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Busca da última Presença com checkin na data atual
            hoje = localdate()
            presenca = alocacao.presencas.order_by('-id').first()

            if not presenca:
                return Response(
                    {"error": "Nenhum check-in encontrado nessa alocação."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            #checkin=datetime.strptime(presenca.checkin,"%Y-%m-%dT%H:%M:%S.%fZ")
            #checkout=datetime.strptime(presenca.checkout,"%Y-%m-%dT%H:%M:%S.%fZ")
            
            return Response(
                {"message": "PresencaEncontrada","presenca": {
                                                                "id":presenca.id,
                                                                "checkin":presenca.checkin.isoformat() if presenca.checkin else None,
                                                                "checkout":presenca.checkin.isoformat() if presenca.checkout else None,
                                                                "observacao_checkin":presenca.observacao_checkin,
                                                                "observacao_checkout":presenca.observacao_checkout,
                                                                "tempo_intervalo":f"{presenca.tempo_intervalo}"
                                                                }},
                status=status.HTTP_200_OK
            )

        except Alocacao.DoesNotExist:
            return Response(
                {"error": "Alocação não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": f"Ocorreu um erro ao buscar a informação: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
#===============FIM GET ULTIMA PRESENCA BY ALOCACAO VIEW=========#









