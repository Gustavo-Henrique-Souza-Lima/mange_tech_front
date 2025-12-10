from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    ChamadoViewSet, 
    AtivoViewSet, 
    CategoriaViewSet,
    AmbienteViewSet,
    UserProfileViewSet,
    AnexoViewSet, 
    register_user,
    current_user,
)

router = DefaultRouter()
router.register(r'chamados', ChamadoViewSet, basename='chamado')
router.register(r'ativos', AtivoViewSet, basename='ativo')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'ambientes', AmbienteViewSet, basename='ambiente')
router.register(r'usuarios', UserProfileViewSet, basename='usuario')
router.register(r'anexos', AnexoViewSet, basename='anexo') # <--- ADICIONE ESTA LINHA

urlpatterns = [
    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Cadastro e usuário atual
    path('register/', register_user, name='register'),
    path('me/', current_user, name='current_user'),
    
    # Router URLs
    path('', include(router.urls)),
]