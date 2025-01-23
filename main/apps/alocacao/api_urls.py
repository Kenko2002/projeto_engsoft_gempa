from django.urls import path, register_converter, include
from rest_framework import routers
from .api_views import (
    AlocacaoViewSet,PresencaViewSet,DiaCombinadoViewSet,CheckinAPIView,
    CheckoutAPIView,AlocacaoBySetorAndStatusView,GetLastPresencaByAlocacaoAPIView
)
router = routers.DefaultRouter()
router.register(r'alocacao', AlocacaoViewSet, basename='alocacao')
router.register(r'presenca', PresencaViewSet, basename='presenca')
router.register(r'diacombinado', DiaCombinadoViewSet, basename='diacombinado')
urlpatterns = [
    path('alocacao/', include(router.urls)),
    path('alocacao/<int:alocacao_id>/checkin/', CheckinAPIView.as_view(), name='checkin'),
    path('alocacao/<int:alocacao_id>/checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('alocacao/setor/<int:setor_id>/status/<str:status>/', AlocacaoBySetorAndStatusView.as_view(), name='alocacao-by-setor-status'),
    path('alocacao/alocacao/<int:alocacao_id>/getlastpresenca/', GetLastPresencaByAlocacaoAPIView.as_view(), name='get-last-presenca'),
]

