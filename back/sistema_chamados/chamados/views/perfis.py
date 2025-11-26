"""
ViewSet para Perfis de Usuário
"""

from rest_framework.decorators import action
from rest_framework.response import Response

from .base import BaseViewSet
from ..models import UserProfile
from ..serializers import UserProfileSerializer


class UserProfileViewSet(BaseViewSet):
    """
    ViewSet para perfis de usuário
    
    Endpoints:
    - GET /usuarios/ - Lista todos os perfis
    - GET /usuarios/{id}/ - Detalhe de um perfil
    - PUT/PATCH /usuarios/{id}/ - Atualiza perfil
    - GET /usuarios/me/ - Perfil do usuário logado
    """
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.select_related('user').all()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna o perfil do usuário logado"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)