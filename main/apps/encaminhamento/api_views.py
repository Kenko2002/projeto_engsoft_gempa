from .models import (
    Instituicao,
    UnidadeOrganizacional,
    SetorInstitucional,
    Vaga,
    Funcao,
)
from .serializers import (
    InstituicaoReadSerializer, InstituicaoWriteSerializer,
    UnidadeOrganizacionalReadSerializer, UnidadeOrganizacionalWriteSerializer,
    SetorInstitucionalReadSerializer, SetorInstitucionalWriteSerializer,
    VagaReadSerializer, VagaWriteSerializer,
    FuncaoReadSerializer, FuncaoWriteSerializer,SetorSerializer,
    CondicaoAlocacaoSerializer,AvaliacaoSerializer,VagaVagasDiponiveisSerializer,NovoEncaminhamentoSerializer, NovoEncaminhamentoResponseSerializer
    ,SetorInstitucionalSerializer
)

from apps.socialentity.models import Responsavel
from datetime import datetime
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
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class InstituicaoViewSet(ModelViewSet):
    queryset = Instituicao.objects.all()
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
            return InstituicaoReadSerializer
        return InstituicaoWriteSerializer

class UnidadeOrganizacionalViewSet(ModelViewSet):
    queryset = UnidadeOrganizacional.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['hora_abertura', 'hora_fechamento', 'latitude', 'longitude']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return UnidadeOrganizacionalReadSerializer
        return UnidadeOrganizacionalWriteSerializer



class SetoresInstitucionaisPorResponsavelAPIView(APIView):
    """
    API View para buscar todos os setores institucionais associados a um responsável.
    """
    
    def get(self, request, responsavel_id, *args, **kwargs):
        try:
            # Filtrar setores institucionais associados ao responsável pelo ID
            responsavel = Responsavel.objects.get(id=responsavel_id)
            setores = SetorInstitucional.objects.filter(responsavel=responsavel)
            
            # Serializar os resultados
            serializer = SetorInstitucionalSerializer(setores, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Responsavel.DoesNotExist:
            return Response(
                {"error": "Responsável não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )


    
class SetorInstitucionalViewSet(ModelViewSet):
    '''
    é possível desligar a paginação através do seguinte argumento passado via URL:
        http://localhost:8000/encaminhamento/setorinstitucional/?no_pagination=true/
    é possível passar o id de responsável para fazer a busca por responsável também
        GET http://localhost:8000/encaminhamento/setorinstitucional/?id_responsavel=6&no_pagination=true/
    '''
    queryset = SetorInstitucional.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [AllowAny]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    )
    filterset_fields = '__all__'
    search_fields = ['nome']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_queryset(self):
        """
        Sobrescreve o método get_queryset para permitir o filtro por id_responsavel.
        """
        queryset = super().get_queryset()
        
        # Obtém o parâmetro id_responsavel da query string
        id_responsavel = self.request.query_params.get('id_responsavel')
        
        if id_responsavel:
            queryset = queryset.filter(responsavel_id=id_responsavel)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return SetorInstitucionalReadSerializer
        return SetorInstitucionalWriteSerializer
    
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
    
    
    
    

class VagaViewSet(ModelViewSet):
    queryset = Vaga.objects.all()
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
            return VagaReadSerializer
        return VagaWriteSerializer

class FuncaoViewSet(ModelViewSet):
    queryset = Funcao.objects.all()
    pagination_class = CustomPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [ AllowAny ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend
    )
    filterset_fields = '__all__'
    search_fields = ['nome']
    ordering_fields = '__all__'
    ordering = ["id"]
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return FuncaoReadSerializer
        return FuncaoWriteSerializer










from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Instituicao, UnidadeOrganizacional, SetorInstitucional, Vaga, Funcao
from apps.socialentity.models import Endereco,Telefone

#============CADASTRO DE INSTITUIÇÃO=============#
#codigo morto, não é usado pra nada nessa versão.
        
class UseCaseIncluirInstituicaoComUnidadeSetorEVagaAPIView(APIView):
    
    # Definindo o corpo da requisição para documentação com Swagger
    @swagger_auto_schema(
        operation_description="Cadastrar uma instituição, suas unidades organizacionais, setores e vagas.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'instituicao': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nome': openapi.Schema(type=openapi.TYPE_STRING, description="Nome da Instituição"),
                        'email_contato': openapi.Schema(type=openapi.TYPE_STRING, description="Email de contato"),
                        'identificacao': openapi.Schema(type=openapi.TYPE_STRING, description="Identificação única da Instituição"),
                        'ativo': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Se a Instituição está ativa"),
                        'enderecos': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'logradouro': openapi.Schema(type=openapi.TYPE_STRING),
                                    'numero': openapi.Schema(type=openapi.TYPE_STRING),
                                    'bairro': openapi.Schema(type=openapi.TYPE_STRING),
                                    'cidade': openapi.Schema(type=openapi.TYPE_STRING),
                                    'estado': openapi.Schema(type=openapi.TYPE_STRING),
                                    'cep': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        ),
                        'telefones': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'ddd': openapi.Schema(type=openapi.TYPE_STRING),
                                    'numero': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        ),
                        'unidades_organizacionais': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'nome': openapi.Schema(type=openapi.TYPE_STRING),
                                    'hora_abertura': openapi.Schema(type=openapi.TYPE_STRING),
                                    'hora_fechamento': openapi.Schema(type=openapi.TYPE_STRING),
                                    'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'email_contato': openapi.Schema(type=openapi.TYPE_STRING, description="Email de contato"),
                                    'identificacao': openapi.Schema(type=openapi.TYPE_STRING, description="Identificação única da Instituição"),
                                    'enderecos': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'logradouro': openapi.Schema(type=openapi.TYPE_STRING),
                                                'numero': openapi.Schema(type=openapi.TYPE_STRING),
                                                'bairro': openapi.Schema(type=openapi.TYPE_STRING),
                                                'cidade': openapi.Schema(type=openapi.TYPE_STRING),
                                                'estado': openapi.Schema(type=openapi.TYPE_STRING),
                                                'cep': openapi.Schema(type=openapi.TYPE_STRING)
                                            }
                                        )
                                    ),
                                    'telefones': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'ddd': openapi.Schema(type=openapi.TYPE_STRING),
                                                'numero': openapi.Schema(type=openapi.TYPE_STRING)
                                            }
                                        )
                                    ),
                                    'setores_institucionais': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'nome': openapi.Schema(type=openapi.TYPE_STRING),
                                                'vagas': openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(
                                                        type=openapi.TYPE_OBJECT,
                                                        properties={
                                                            'funcao_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                                                        }
                                                    )
                                                )
                                            }
                                        )
                                    )
                                }
                            )
                        )
                    }
                )
            }
        ),
        responses={201: "Instituição criada com sucesso"}
    )
    def post(self, request, *args, **kwargs):
        if request.data and 'instituicao' in request.data:
            instituicao_data = request.data['instituicao']
            unidades_data = instituicao_data.get('unidades_organizacionais', [])
            enderecos_data = instituicao_data.get('enderecos', [])
            telefones_data = instituicao_data.get('telefones', [])

            # Cria a Instituição e preenche os campos herdados de EntidadeSocial
            instituicao = Instituicao.objects.create(
                nome=instituicao_data.get('nome'),
                email_contato=instituicao_data.get('email_contato'),
                identificacao=instituicao_data.get('identificacao'),
                ativo=instituicao_data.get('ativo'),
            )

            # Cria e associa os endereços
            for endereco_data in enderecos_data:
                endereco = Endereco.objects.create(**endereco_data)
                instituicao.enderecos.add(endereco)

            # Cria e associa os telefones
            for telefone_data in telefones_data:
                telefone = Telefone.objects.create(**telefone_data)
                instituicao.telefones.add(telefone)

            for unidade_data in unidades_data:
                unidade = UnidadeOrganizacional.objects.create(
                    nome=unidade_data.get('nome'),
                    hora_abertura=unidade_data.get('hora_abertura'),
                    hora_fechamento=unidade_data.get('hora_fechamento'),
                    latitude=unidade_data.get('latitude'),
                    longitude=unidade_data.get('longitude'),
                    email_contato=unidade_data.get('email_contato'),
                    identificacao=unidade_data.get('identificacao'),
                    ativo=unidade_data.get('ativo'),
                )

                # Cria e associa os endereços e telefones para a unidade
                for endereco_data in unidade_data.get('enderecos', []):
                    endereco = Endereco.objects.create(**endereco_data)
                    unidade.enderecos.add(endereco)

                for telefone_data in unidade_data.get('telefones', []):
                    telefone = Telefone.objects.create(**telefone_data)
                    unidade.telefones.add(telefone)

                for setor_data in unidade_data.get('setores_institucionais', []):
                    setor = SetorInstitucional.objects.create(
                        nome=setor_data.get('nome'),
                    )

                    for vaga_data in setor_data.get('vagas', []):
                        funcao = Funcao.objects.get(id=vaga_data.get('funcao_id'))
                        vaga = Vaga.objects.create(
                            funcao=funcao,
                        )
                        setor.vagas.add(vaga)

                    unidade.setores_institucionais.add(setor)

                instituicao.unidades_organizacionais.add(unidade)

            return Response({"message": "Instituição criada com sucesso!"}, status=status.HTTP_201_CREATED)

        return Response({"error": "'instituicao' não encontrada no corpo da requisição"}, status=status.HTTP_400_BAD_REQUEST)
#====================FIM CADASTRO DE INSTITUICAO=======================#


#=====FILTRO VAGAS DISPONIVEIS POR SETOR=====#


class VagasDisponiveisPorSetorAPIView(APIView):
    """
    API View para listar todas as vagas disponíveis de um setor.
    """

    def get(self, request, setor_id):
        try:
            # Obtém o setor institucional pelo ID
            setor = SetorInstitucional.objects.get(id=setor_id)
        except SetorInstitucional.DoesNotExist:
            return Response({"error": "Setor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtém todas as vagas do setor
        todas_vagas_do_setor = setor.vagas.all()

        # IDs das vagas que possuem alocações
        vagas_com_alocacao_ids = Alocacao.objects.filter(vaga__in=todas_vagas_do_setor).values_list('vaga_id', flat=True)

        # Vagas disponíveis são aquelas que NÃO estão presentes nas vagas_com_alocacao_ids
        vagas_disponiveis = todas_vagas_do_setor.exclude(id__in=vagas_com_alocacao_ids)
        
        # Serializa as vagas disponíveis
        serializer = VagaVagasDiponiveisSerializer(vagas_disponiveis, many=True, context={"include_funcao": True})

        return Response(serializer.data, status=status.HTTP_200_OK)


#===== FIM FILTRO VAGAS DISPONIVEIS POR SETOR===#

#=====================AVALIAR PRESTADOR==============================#
from .serializers import AlocacaoSerializer,DiaCombinadoSerializer
from apps.alocacao.models import DiaCombinado,Alocacao

class AvaliarPrestadorAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Atualiza a alocação, incluindo o status, data de apresentação, vaga e dias combinados.",
        request_body=AvaliacaoSerializer,
        responses={
            200: AvaliacaoSerializer,
            400: 'Bad Request',
            404: 'Alocação não encontrada'
        },
        examples={
            'application/json': {
                "data_apresentacao": "2024-11-26T19:12:10.876Z",
                "status": "RECUSADO",
                "vaga": 5,
                "bservacao_avaliacao":"Texto",
                "diascombinados": [
                    {
                        "dia_semana": "SEGUNDA-FEIRA",
                        "horario_entrada": "19:12:10.876Z",
                        "horario_saida": "22:12:10.876Z"
                    }
                ]
            }
        }
    )
    def put(self, request, alocacao_id):
        try:
            # Recupera a Alocacao pelo id
            alocacao = Alocacao.objects.get(id=alocacao_id)
        except Alocacao.DoesNotExist:
            return Response({"detail": "Alocação não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        # Cria o serializer com os dados do request
        serializer = AvaliacaoSerializer(alocacao, data=request.data)
        
        if serializer.is_valid():
            # Atualiza a Alocacao
            updated_alocacao = serializer.save()
            return Response(AvaliacaoSerializer(updated_alocacao).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#==========================FIM AVALIAR PRESTADOR==========================#




#=====================ENCAMINHAR PARA INSTITUICAO=====================#
class AlocacaoCreateView(APIView):
    @swagger_auto_schema(
        request_body=CondicaoAlocacaoSerializer,
        responses={
            201: "Encaminhado com sucesso!",
            400: "Erro de validação de dados"
        },
        operation_description="Cria uma alocação associada a uma condição, com uma vaga associada ao setor institucional.",
        operation_summary="Alocar alocação e criar vaga fantasma em Setor"
    )
    
    def post(self, request, *args, **kwargs):
        serializer = CondicaoAlocacaoSerializer(data=request.data)
        
        if serializer.is_valid():
            alocacao = serializer.save()
            return Response({
                'message': 'Encaminhado com sucesso!',
                'alocacao_id': alocacao.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#=================FIM ENCAMINHAR PARA INSTITUICAO=====================#








#=================NOVO ENCAMINHAMENTO========================#
from apps.socialentity.models import Tecnico
from apps.atendimento.models import Condicao
from rest_framework.exceptions import NotFound

class NovoEncaminhamentoAPIView(APIView):
    '''Essa API View serve para atender ao fluxo alternativo onde o prestador
    é recusado inicialmente pela primeira instituição pra onde ele é mandado, e então é feito
    um novo encaminhamento.
    Caso esse Novo encaminhamento seja feito sem desativar um anterior que esteja como CUMPRINDO e pertença
    a mesma Condição, esse EndPoint irá desativar-lo imediatamente ao criar uma Alocacao nova.
    '''
    @swagger_auto_schema(
        request_body=NovoEncaminhamentoSerializer,
        responses={
            201: NovoEncaminhamentoResponseSerializer,
            400: "Validation errors or missing fields",
            404: "Condicao or Tecnico not found"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = NovoEncaminhamentoSerializer(data=request.data)
        if serializer.is_valid():
            id_condicao = serializer.validated_data["id_condicao"]
            id_tecnico = serializer.validated_data["id_tecnico"]

            try:
                condicao = Condicao.objects.get(id=id_condicao)
            except Condicao.DoesNotExist:
                raise NotFound(detail={"id_condicao": "Condição não encontrada."})

            try:
                tecnico = Tecnico.objects.get(id=id_tecnico)
            except Tecnico.DoesNotExist:
                raise NotFound(detail={"id_tecnico": "Técnico não encontrado."})

            # Verificar se já existe alguma Alocacao com status "CUMPRINDO" para essa condicao
            alocacao_cumprindo = condicao.alocacoes.filter(status="CUMPRINDO").first()


            if alocacao_cumprindo:
                # Atualizar a alocação existente conforme descrito no Evento 44
                # Ao fazer um novo encaminhamento, deve-se verificar os anteriores
                # se estão Cumprindo e tornar-los Inativos, deve-se atualizar sua vigencia.
                alocacao_cumprindo.vigencia_fim = datetime.now()
                alocacao_cumprindo.status = "Inativa"
                alocacao_cumprindo.save()


            # Criação da alocação
            alocacao = Alocacao.objects.create(
                prazo_apresentacao=serializer.validated_data["prazo_apresentacao"],
                vigencia_inicio=serializer.validated_data["vigencia_inicio"],
                vigencia_fim=serializer.validated_data["vigencia_fim"],
                status="Aguardando Entrevista",
                tecnico=tecnico
            )

            # Associar a alocação à condição
            condicao.alocacoes.add(alocacao)

            response_serializer = NovoEncaminhamentoResponseSerializer(alocacao)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#=============GET SETOR BY FUNCAO=================#
class SetorPorFuncaoAPIView(APIView):

    
    @swagger_auto_schema(
        operation_description="Retorna todos os setores que possuem vagas de uma determinada função",
        responses={200: SetorSerializer(many=True)},
        # Passando o nome da função como parâmetro da URL
        manual_parameters=[
            openapi.Parameter('funcao_nome', openapi.IN_PATH, description="Nome da função", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, funcao_nome):
        # Obtém o nome da função da URL
        if not funcao_nome:
            return Response({'detail': 'Nome da função é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Busca a função pelo nome
            funcao = Funcao.objects.get(nome=funcao_nome)
        except Funcao.DoesNotExist:
            return Response({'detail': 'Função não encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtém todos os setores que têm vagas para a função
        setores = SetorInstitucional.objects.filter(vagas__funcao=funcao).distinct()

        # Serializa os setores encontrados
        serializer = SetorSerializer(setores, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
#=========FIM GET SETOR BY FUNCAO===================#



#==========GET SETOR BY BAIRRO=====================#

class SetorPorBairroAPIView(APIView):

    
    @swagger_auto_schema(
        operation_description="Retorna todos os setores que pertençam a unidades em um determinado bairro",
        responses={200: SetorSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('bairro_nome', openapi.IN_PATH, description="Nome do bairro", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, bairro_nome):
        # Obtém o nome da função da URL
        if not bairro_nome:
            return Response({'detail': 'Nome do bairro é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Busca Enderecos por Bairro
            enderecos = Endereco.objects.filter(bairro=bairro_nome)
        except Endereco.DoesNotExist:
            return Response({'detail': 'Endereco não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtém todas as unidades que têm esses Enderecos
        unidades_encontradas = []
        # Itera sobre os endereços para buscar as unidades associadas
        for endereco in enderecos:
            unidades = UnidadeOrganizacional.objects.filter(enderecos=endereco)
            unidades_encontradas.extend(unidades)  # Adiciona as unidades encontradas à lista

        if not unidades_encontradas:
            return Response({'detail': 'Nenhuma unidade encontrada para os endereços fornecidos.'}, status=status.HTTP_404_NOT_FOUND)

        # Cria uma lista para armazenar os setores encontrados
        setores = []
        for unidade in unidades_encontradas:
            setores.extend(unidade.setores_institucionais.all())  # Adiciona os setores de cada unidade à lista de setores

        if not setores:
            return Response({'detail': 'Nenhum setor encontrado para as unidades.'}, status=status.HTTP_404_NOT_FOUND)

        # Serializa os setores encontrados
        serializer = SetorSerializer(setores, many=True)
        response_data = {
                    'unidades': [unidade.id for unidade in unidades_encontradas],  # Retorna apenas os IDs das unidades, pode incluir outros campos aqui
                    'setores': serializer.data
                }

        return Response(response_data, status=status.HTTP_200_OK)
#==========fim GET SETOR BY BAIRRO=================#



#==========GET SETOR BY Cidade=====================#

class SetorPorCidadeAPIView(APIView):

    
    @swagger_auto_schema(
        operation_description="Retorna todos os setores que pertençam a unidades em um determinado bairro",
        responses={200: SetorSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('cidade_nome', openapi.IN_PATH, description="Nome do bairro", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, cidade_nome):
        # Obtém o nome da função da URL
        if not cidade_nome:
            return Response({'detail': 'Nome do cidade é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Busca Enderecos por cidade
            enderecos = Endereco.objects.filter(cidade=cidade_nome)
        except Endereco.DoesNotExist:
            return Response({'detail': 'Endereco não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtém todas as unidades que têm esses Enderecos
        unidades_encontradas = []
        # Itera sobre os endereços para buscar as unidades associadas
        for endereco in enderecos:
            unidades = UnidadeOrganizacional.objects.filter(enderecos=endereco)
            unidades_encontradas.extend(unidades)  # Adiciona as unidades encontradas à lista

        if not unidades_encontradas:
            return Response({'detail': 'Nenhuma unidade encontrada para os endereços fornecidos.'}, status=status.HTTP_404_NOT_FOUND)

        # Cria uma lista para armazenar os setores encontrados
        setores = []
        for unidade in unidades_encontradas:
            setores.extend(unidade.setores_institucionais.all())  # Adiciona os setores de cada unidade à lista de setores

        if not setores:
            return Response({'detail': 'Nenhum setor encontrado para as unidades.'}, status=status.HTTP_404_NOT_FOUND)

        # Serializa os setores encontrados
        serializer = SetorSerializer(setores, many=True)
        response_data = {
                    'unidades': [unidade.id for unidade in unidades_encontradas],  # Retorna apenas os IDs das unidades, pode incluir outros campos aqui
                    'setores': serializer.data
                }

        return Response(response_data, status=status.HTTP_200_OK)
#==========fim GET SETOR BY Cidade=================#
