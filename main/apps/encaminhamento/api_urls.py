from django.urls import path, register_converter, include
from rest_framework import routers
from .api_views import (
    InstituicaoViewSet,
    UnidadeOrganizacionalViewSet,
    SetorInstitucionalViewSet,
    VagaViewSet,
    FuncaoViewSet,UseCaseIncluirInstituicaoComUnidadeSetorEVagaAPIView,AvaliarPrestadorAPIView,
    AlocacaoCreateView,NovoEncaminhamentoAPIView,VagasDisponiveisPorSetorAPIView,SetorPorFuncaoAPIView,SetorPorBairroAPIView,SetorPorCidadeAPIView
    ,SetoresInstitucionaisPorResponsavelAPIView
)
from ..socialentity.api_views import ToggleAtivoView

from .models import *

router = routers.DefaultRouter()

router.register(r'instituicao', InstituicaoViewSet, basename='instituicao')
router.register(r'unidadeorganizacional', UnidadeOrganizacionalViewSet, basename='unidadeorganizacional')
router.register(r'setorinstitucional', SetorInstitucionalViewSet, basename='setorinstitucional')
router.register(r'vaga', VagaViewSet, basename='vaga')
router.register(r'funcao', FuncaoViewSet, basename='funcao')

urlpatterns = [
    path('encaminhamento/', include(router.urls)),
    path('cadastro/instituicao/',UseCaseIncluirInstituicaoComUnidadeSetorEVagaAPIView.as_view(), name='instituicao-create'),
    
    path('setor-institucional/get-setor-by-responsavel/<int:responsavel_id>/',SetoresInstitucionaisPorResponsavelAPIView.as_view(),name='setores-institucionais-por-responsavel'),
    
    path('socialentity/instituicao/<int:pk>/toggle-ativo/', ToggleAtivoView.as_view(model_class=Instituicao), name='instituicao_toggle_ativo'),
    path('socialentity/unidade-organizacional/<int:pk>/toggle-ativo/', ToggleAtivoView.as_view(model_class=UnidadeOrganizacional), name='unidade_organizacional_toggle_ativo'),
    path('encaminhamento/avaliar-prestador/<int:alocacao_id>/', AvaliarPrestadorAPIView.as_view(), name='avaliar-prestador'),

    path('encaminhamento/encaminhar-instituicao/', AlocacaoCreateView.as_view(), name='encaminhar-instituicao'),
    path ('encaminhamento/novo-encaminhamento/',NovoEncaminhamentoAPIView.as_view(), name='reencaminhamento'),
    path("setor/<int:setor_id>/getvagasdisponiveis/",VagasDisponiveisPorSetorAPIView.as_view(), name="getall_vagasdisponiveis_by_setor" ),
    
    path('alocacao/setor/funcao/<str:funcao_nome>/', SetorPorFuncaoAPIView.as_view(), name='setores-funcao'),
    path('alocacao/setor/bairro/<str:bairro_nome>/', SetorPorBairroAPIView.as_view(), name='setores-bairro'),
    path('alocacao/setor/cidade/<str:cidade_nome>/', SetorPorCidadeAPIView.as_view(), name='setores-cidade'),
    
]
