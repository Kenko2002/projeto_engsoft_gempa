from django.urls import path, register_converter, include
from rest_framework import routers
from .api_views import (
    AtendimentoViewSet,
    ObservacaoViewSet,
    ExecucaoViewSet,
    CondicaoViewSet,
    HistoricoCargaHorariaViewSet,AgendarAtendimentoAPIView,CheckAvailabilityView,GetTecnicoDisponivelPorHorario
)



router = routers.DefaultRouter()

router.register(r'atendimento', AtendimentoViewSet, basename='atendimento')
router.register(r'observacao', ObservacaoViewSet, basename='observacao')
router.register(r'execucao', ExecucaoViewSet, basename='execucao')
router.register(r'condicao', CondicaoViewSet, basename='condicao')
router.register(r'historicocargahoraria', HistoricoCargaHorariaViewSet, basename='historicocargahoraria')

urlpatterns = [
    path('atendimento/', include(router.urls)),
    path('agendar_atendimento/', AgendarAtendimentoAPIView.as_view(), name='agendar_atendimento'),
    path('atendimento/check-availability/<int:tecnico_id>/<str:horario>/', CheckAvailabilityView.as_view(), name='check-availability'),
    path('atendimento/get-tecnico-disponivel/horario/<str:horario>/', GetTecnicoDisponivelPorHorario.as_view(), name='get-tecnico-disponivel-por-horario'),

]
