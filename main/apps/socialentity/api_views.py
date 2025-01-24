from .models import (
    EntidadeSocial,
    Prestador,
    Tecnico,
    Fiscal,
    Coordenador,
    Responsavel,
)
from .serializers import (
    EntidadeSocialReadSerializer, EntidadeSocialWriteSerializer,
    PrestadorReadSerializer, PrestadorWriteSerializer,
    TecnicoReadSerializer, TecnicoWriteSerializer,
    FiscalReadSerializer, FiscalWriteSerializer,
    CoordenadorReadSerializer, CoordenadorWriteSerializer,
    ResponsavelReadSerializer, ResponsavelWriteSerializer,PrimeiraEntrevistaIncluirPrestadorAPIViewSerializer,
    CadastroResponsavelWriteSerializer,CadastroCoordenadorWriteSerializer,CadastroFiscalWriteSerializer,CadastroTecnicoWriteSerializer,
    EntidadeSocialAtivarDesativarSerializer,EnderecoReadSerializer,EnderecoWriteSerializer,TelefoneWriteSerializer,TelefoneReadSerializer
)

from apps.socialentity.models import Usuario,Endereco,Telefone
from apps.encaminhamento.models import Instituicao,UnidadeOrganizacional

from apps.encaminhamento.serializers import InstituicaoReadSerializer,UnidadeOrganizacionalReadSerializer, InstituicaoWriteSerializer,UnidadeOrganizacionalWriteSerializer
        
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_condition import And, Or
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from .pagination import CustomPagination
from rest_framework import generics
from rest_framework import filters
import django_filters.rest_framework
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User, Group

        
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from drf_yasg import openapi

'''
class EntidadeSocialViewSet(ModelViewSet):
    queryset = EntidadeSocial.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['nome', 'identificacao', 'ativo', 'email_contato']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return EntidadeSocialReadSerializer
        return EntidadeSocialWriteSerializer
'''

class InsertDataView(APIView):
    def post(self, request, *args, **kwargs):
        # Script SQL de inserção
        sql_script = """
        
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_script)
            return Response({"message": "Dados inseridos com sucesso!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





class EnderecoViewSet(ModelViewSet):
    queryset = Endereco.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['numero','bairro','cidade','estado','cep','complemento','logradouro']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return EnderecoReadSerializer
        return EnderecoWriteSerializer


class TelefoneViewSet(ModelViewSet):
    queryset = Telefone.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['numero','ddd']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TelefoneReadSerializer
        return TelefoneWriteSerializer




class PrestadorViewSet(ModelViewSet):
    '''
    é possível desligar a paginação através do seguinte argumento passado via URL:
        setor_institucional/?no_pagination=true
    '''
    queryset = Prestador.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['foto', 'rg', 'nome_social', 'escolaridade', 'situacao_economica', 'descricao_avaliacao_psicosocial']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PrestadorReadSerializer
        return PrestadorWriteSerializer

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





from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
class PrimeiraEntrevistaIncluirPrestadorAPIView(APIView):
    @swagger_auto_schema(request_body=PrimeiraEntrevistaIncluirPrestadorAPIViewSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PrimeiraEntrevistaIncluirPrestadorAPIViewSerializer(data=request.data)
        
        if serializer.is_valid():
            
            
            # Extração dos dados necessários
            horas_minimas = serializer.validated_data.get("horas_minimas", 0)
            horas_maximas = serializer.validated_data.get("horas_maximas", 0)
            periodo_dias = serializer.validated_data.get("periodo_dias", 1)  # Evitar divisão por zero
            if periodo_dias==0:
                periodo_dias=7
            
            # Limite semanal em horas por dia
            limite_diario = 44 / 7

            # Validação
            if (horas_minimas / periodo_dias) > limite_diario:
                return Response(
                    {"error": "Horas mínimas excedem o limite permitido de 44h semanais."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if (horas_maximas / periodo_dias) > limite_diario:
                return Response(
                    {"error": "Horas máximas excedem o limite permitido de 44h semanais."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
                
                
            # Captura dos objetos criados
            prestador, execucao, condicao, alocacao ,carga_horaria = serializer.save()
            
            # Construção da resposta com IDs relevantes
            response_data = {
                'message': 'Prestador, execução, condição e alocação criados com sucesso',
                'prestador_id': prestador.id,
                'execucao_id': execucao.id,
                'condicao_id': condicao.id,
                'alocacao_id': alocacao.id,
                'carga_horaria_id':carga_horaria.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TecnicoViewSet(ModelViewSet):
    queryset = Tecnico.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TecnicoReadSerializer
        return TecnicoWriteSerializer

class FiscalViewSet(ModelViewSet):
    queryset = Fiscal.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return FiscalReadSerializer
        return FiscalWriteSerializer


class CoordenadorViewSet(ModelViewSet):
    queryset = Coordenador.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CoordenadorReadSerializer
        return CoordenadorWriteSerializer

class ResponsavelViewSet(ModelViewSet):
    queryset = Responsavel.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ResponsavelReadSerializer
        return ResponsavelWriteSerializer
    
    
#===API VIEW DE ATIVAÇÃO E DESATIVAÇÃO DE ENTIDADE===#

   
from django.shortcuts import get_object_or_404
from .serializers import AtivoSerializer
class ToggleAtivoView(APIView):
    model_class = None  # Defina a classe do modelo na subclasse

    @swagger_auto_schema(
        operation_description="Atualiza o atributo 'ativo' de uma entidade especificada.",
        request_body=AtivoSerializer,  # Define o formato do corpo da requisição
        responses={
            200: openapi.Response(
                description="Status atualizado com sucesso.",
                examples={
                    "application/json": {"id": 1, "ativo": True}
                }
            ),
            400: "Erro na validação dos dados.",
            404: "Entidade não encontrada.",
        },
    )
    def post(self, request, pk, *args, **kwargs):
        """
        Define o valor do campo 'ativo' da entidade especificada com base na entrada.
        """
        if not self.model_class:
            return Response({"detail": "Classe do modelo não definida."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar a entrada usando o serializador
        serializer = AtivoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Obter a instância do modelo
        model_instance = get_object_or_404(self.model_class, pk=pk)

        # Atualizar o valor de 'ativo'
        model_instance.ativo = serializer.validated_data['ativo']
        model_instance.save()

        # Retornar o novo estado de 'ativo'
        return Response(
            {"id": model_instance.pk, "ativo": model_instance.ativo},
            status=status.HTTP_200_OK,
        )

# Subclasses específicas para cada tipo de entidade
class ToggleAtivoPrestadorView(ToggleAtivoView):
    model_class = Prestador

class ToggleAtivoTecnicoView(ToggleAtivoView):
    model_class = Tecnico

class ToggleAtivoFiscalView(ToggleAtivoView):
    model_class = Fiscal

class ToggleAtivoCoordenadorView(ToggleAtivoView):
    model_class = Coordenador

class ToggleAtivoResponsavelView(ToggleAtivoView):
    model_class = Responsavel


#====================================================#    
    
    
    
#===API_VIEWS DE CADASTROS DE ENTIDADES===#    

class CadastroCoordenadorAPIView(CreateAPIView):
    queryset = Coordenador.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CoordenadorReadSerializer
        return CadastroCoordenadorWriteSerializer

    def perform_create(self, serializer):
        """
        Sobrescreve o método de criação para:
        - Criar um User associado ao Coordenador.
        - Definir o status "ativo" como True.
        """
        # Verifica se a senha foi fornecida na requisição
        password = self.request.data.get('password')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        email_contato=self.request.data.get("email_contato")
        if not password:
            raise ValidationError({'password': 'A senha é obrigatória para criar um Coordenador.'})

        # Cria o usuário do Django
        nome = serializer.validated_data.get('first_name', 'Coordenador')+" "+serializer.validated_data.get('last_name', 'Coordenador')
        username = nome
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email_contato
        )
        
        group, created = Group.objects.get_or_create(name="Coordenador")
        user.groups.add(group)

        # Define "ativo" como True e associa o Coordenador ao User
        serializer.save(user=user, ativo=True)


class CadastroTecnicoAPIView(CreateAPIView):
    queryset = Tecnico.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return TecnicoReadSerializer
        return CadastroTecnicoWriteSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        email_contato=self.request.data.get("email_contato")
        
        if not password:
            raise ValidationError({'password': 'A senha é obrigatória para criar um Técnico.'})

        nome = serializer.validated_data.get('first_name', 'Tecnico')+" "+serializer.validated_data.get('last_name', 'Tecnico')
        username = nome
        user = User.objects.create_user(
            username=username, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email_contato
            )
        
        group, created = Group.objects.get_or_create(name="Tecnico")
        user.groups.add(group)

        serializer.save(user=user, ativo=True)


class CadastroFiscalAPIView(CreateAPIView):
    queryset = Fiscal.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return FiscalReadSerializer
        return CadastroFiscalWriteSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        email_contato=self.request.data.get("email_contato")
        
        if not password:
            raise ValidationError({'password': 'A senha é obrigatória para criar um Fiscal.'})

        nome = serializer.validated_data.get('first_name', 'Fiscal')+" "+serializer.validated_data.get('last_name', 'Fiscal')
        username = nome
        user = User.objects.create_user(
            username=username, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email_contato
            )
        
        group, created = Group.objects.get_or_create(name="Fiscal")
        user.groups.add(group)

        serializer.save(user=user, ativo=True)


class CadastroResponsavelAPIView(CreateAPIView):
    queryset = Responsavel.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    )
    filterset_fields = '__all__'
    search_fields = []
    ordering_fields = '__all__'
    ordering = ["id"]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ResponsavelReadSerializer
        return CadastroResponsavelWriteSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        email_contato=self.request.data.get("email_contato")
        
        if not password:
            raise ValidationError({'password': 'A senha é obrigatória para criar um Responsável.'})

        nome = serializer.validated_data.get('first_name', 'Responsável')+" "+serializer.validated_data.get('last_name', 'Responsável')
        username = nome
        user = User.objects.create_user(
            username=username, 
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email_contato
            )
        
        group, created = Group.objects.get_or_create(name="Responsavel")
        user.groups.add(group)

        serializer.save(user=user, ativo=True)
        
#==========================================#



#===API_VIEWS DE LOGIN===#
        

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email of the user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user')
            }
        ),
        responses={
            200: openapi.Response(
                description='Login successful',
                examples={
                    'application/json': {
                        'message': 'Login successful',
                        'token': 'JWT_TOKEN_HERE',
                        'user_group': 'Coordenador'  # Example group name
                    }
                }
            ),
            401: openapi.Response(
                description='Invalid credentials',
                examples={
                    'application/json': {'detail': 'Username or Password is incorrect'}
                }
            ),
            400: openapi.Response(
                description='Invalid input',
                examples={
                    'application/json': {'username': ['This field is required.'], 'password': ['This field is required.']}
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username and Password are required!'}, status=status.HTTP_400_BAD_REQUEST)

        # Autentica o usuário usando django.contrib.auth.authenticate
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': 'Username or Password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)


        usuario = getattr(user, 'usuario', None)  # Get the related Usuario instance
        if usuario and not usuario.ativo:  # Check if "ativo" is False
            return Response(
                {'detail': 'Esse Usuário está Inativo. Contate o SSP'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Gera o token do usuário
        token, created = Token.objects.get_or_create(user=user)

        # Obtém os grupos do usuário
        user_groups = user.groups.values_list('name', flat=True)

        # Retorna a resposta com o token e os grupos do usuário
        response_data = {
            'message': 'Login successful',
            'token': token.key,  # Token gerado para o usuário
            'user_group': list(user_groups),  # Lista de grupos do usuário
            'id': usuario.id,
            'nome': usuario.nome
        }
        return Response(response_data, status=status.HTTP_200_OK)

#=========================#





#===================AREA DO ADMIN API VIEW==============#
from .serializers import (
    AreaAdminAlocacaoSerializer,AreaAdminSetorInstitucionalSerializer,AreaAdminVagaSerializer,AreaAdminFuncaoSerializer,
    AreaAdminHistoricoCargaHorariaSerializer,AreaAdminExecucaoSerializer,AreaAdminPresencaSerializer
)
from apps.atendimento.models import Execucao,Condicao
from datetime import timedelta
from django.utils.timezone import now

class AreaAdminCondicaoDetailView(APIView):
    """
    API View que atende a necessidade de listagem de todos os prestadores com suas condições,
    execuções, e demais informações relevantes para o painel de controle do técnico.
    """

    def get(self, request, id=None, *args, **kwargs):
        if id:
            condicao = get_object_or_404(Condicao, pk=id)
            condicoes = [condicao]
        else:
            # Se nenhum ID for fornecido, busca todas as condições
            condicoes = Condicao.objects.all()
        resultado = []

        for condicao in condicoes:
            # Serializa o histórico de carga horária
            historico_carga_horaria = AreaAdminHistoricoCargaHorariaSerializer(
                condicao.historico_carga_horaria.all(), many=True
            ).data

            # Obtém a execução e o prestador associado
            execucao = Execucao.objects.filter(condicoes=condicao).first()
            execucao_data = AreaAdminExecucaoSerializer(execucao).data if execucao else None

            # Serializa as alocações e calcula total de horas cumpridas
            alocacoes = condicao.alocacoes.all()
            alocacao_data = AreaAdminAlocacaoSerializer(alocacoes, many=True).data

            # Calcula total de horas cumpridas
            total_horas = timedelta()
            total_horas_intervalo=timedelta()
            
            #adiciona ao total de horas cumpridas o tempo que o prestador cumpriu antes de ser cadastrado no sistema
            total_horas +=condicao.ch_cumprida_anterior_cadastro or timedelta(0)
            
            for alocacao in alocacoes:
                for presenca in alocacao.presencas.all():
                    checkin = presenca.checkin
                    checkout = presenca.checkout or now()
                    tempo_intervalo = presenca.tempo_intervalo
                    total_horas += (checkout - checkin)
                    if (tempo_intervalo):
                        total_horas_intervalo+=tempo_intervalo
                    
                    

            # Converte timedelta em horas e minutos
            total_horas_em_horas = total_horas.total_seconds() // 3600
            total_horas_intervalo_em_horas = total_horas_intervalo.total_seconds() // 3600
            
            #descontando o tempo de intervalo
            total_horas_em_horas=total_horas_em_horas-total_horas_intervalo_em_horas
            
            total_minutos = (total_horas.total_seconds() % 3600) // 60
            total_segundos = total_minutos // 60
            
            total_minutos=int(total_minutos)
            total_horas_em_horas=int(total_horas_em_horas)
            
            resultado.append({
                "condicao_id": condicao.id,
                "horas_minimas": condicao.horas_minimas,
                "horas_maximas": condicao.horas_maximas,
                "periodo_dias": condicao.periodo_dias,
                "flexivel_dia": condicao.flexivel_dia,
                "flexivel_horario": condicao.flexivel_horario,
                "tipo_processual": condicao.tipo_processual,
                "historico_carga_horaria": historico_carga_horaria,
                "execucao": execucao_data,
                "alocacoes": alocacao_data,
                "total_horas_cumpridas": str(total_horas_em_horas)+"h "+str(total_minutos)+"min",
            })

        if resultado.length==0:
            resultado.append("condicao_id",condicao.id)
            return Response(resultado, status=status.HTTP_200_OK)
        return Response(resultado, status=status.HTTP_200_OK)
#=============FIM AREA DO ADMIN API VIEW=================#
