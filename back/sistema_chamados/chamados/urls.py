from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet, CategoriaViewSet, AmbienteViewSet, AtivoViewSet,
    ChamadoViewSet, ChamadoStatusHistoryViewSet, AnexoViewSet, NotificacaoViewSet
)

# Criar router
router = DefaultRouter()

# Registrar ViewSets
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'ambientes', AmbienteViewSet, basename='ambiente')
router.register(r'ativos', AtivoViewSet, basename='ativo')
router.register(r'chamados', ChamadoViewSet, basename='chamado')
router.register(r'historico', ChamadoStatusHistoryViewSet, basename='historico')
router.register(r'anexos', AnexoViewSet, basename='anexo')
router.register(r'notificacoes', NotificacaoViewSet, basename='notificacao')

# URLs da aplicação
urlpatterns = [
    path('api/', include(router.urls)),
]