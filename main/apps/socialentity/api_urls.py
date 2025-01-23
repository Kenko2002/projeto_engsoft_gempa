from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .api_views import (
    PrestadorViewSet,
    TecnicoViewSet,
    FiscalViewSet,
    CoordenadorViewSet,
    ResponsavelViewSet,
    PrimeiraEntrevistaIncluirPrestadorAPIView,
    CadastroCoordenadorAPIView,
    CadastroFiscalAPIView,
    CadastroTecnicoAPIView,
    CadastroResponsavelAPIView,LoginAPIView,
    EnderecoViewSet,TelefoneViewSet,
    
    ToggleAtivoPrestadorView,
    ToggleAtivoTecnicoView,
    ToggleAtivoFiscalView,
    ToggleAtivoCoordenadorView,
    ToggleAtivoResponsavelView,
    AreaAdminCondicaoDetailView
)
from .models import *

# Registrar apenas os ViewSets completos no roteador
router = DefaultRouter()
router.register(r'prestador', PrestadorViewSet, basename='prestador')
router.register(r'tecnico', TecnicoViewSet, basename='tecnico')
router.register(r'fiscal', FiscalViewSet, basename='fiscal')
router.register(r'coordenador', CoordenadorViewSet, basename='coordenador')
router.register(r'responsavel', ResponsavelViewSet, basename='responsavel')

router.register(r'endereco', EnderecoViewSet, basename='endereco')
router.register(r'telefone', TelefoneViewSet, basename='telefone')

# URLs
urlpatterns = [
    path('socialentity/', include(router.urls)),  # Inclui os endpoints do roteador
    path(
        'cadastro/prestador/primeiroatendimento/',
        PrimeiraEntrevistaIncluirPrestadorAPIView.as_view(),
        name='prestador-execucao-condicao-create',
    ),  # Endpoint adicional para prestador
    # Endpoints de cadastro apenas para criação
    path('cadastro/coordenador/', CadastroCoordenadorAPIView.as_view(), name="coordenador-cadastro"),
    path('cadastro/tecnico/', CadastroTecnicoAPIView.as_view(), name="tecnico-cadastro"),
    path('cadastro/fiscal/', CadastroFiscalAPIView.as_view(), name="fiscal-cadastro"),
    path('cadastro/responsavel/', CadastroResponsavelAPIView.as_view(), name="responsavel-cadastro"),
    path('login/',LoginAPIView.as_view(), name="login"),
    
    path('socialentity/prestador/<int:pk>/toggle-ativo/', ToggleAtivoPrestadorView.as_view(model_class=Prestador), name='prestador_toggle_ativo'),
    path('socialentity/tecnico/<int:pk>/toggle-ativo/', ToggleAtivoTecnicoView.as_view(model_class=Tecnico), name='tecnico_toggle_ativo'),
    path('socialentity/fiscal/<int:pk>/toggle-ativo/', ToggleAtivoFiscalView.as_view(model_class=Fiscal), name='fiscal_toggle_ativo'),
    path('socialentity/coordenador/<int:pk>/toggle-ativo/', ToggleAtivoCoordenadorView.as_view(model_class=Coordenador), name='coordenador_toggle_ativo'),
    path('socialentity/responsavel/<int:pk>/toggle-ativo/', ToggleAtivoResponsavelView.as_view(model_class=Responsavel), name='responsavel_toggle_ativo'),
    path('area-tecnico/condicao/', AreaAdminCondicaoDetailView.as_view(), name='condicao-list'),
    path('area-tecnico/condicao/<int:id>/', AreaAdminCondicaoDetailView.as_view(), name='condicao-detail'),
]
