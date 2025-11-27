from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .base import BaseViewSet
from ..models import UserProfile
from ..serializers import UserProfileSerializer


class UserProfileViewSet(BaseViewSet):
    """
    Endpoints:
    - GET /usuarios/ - Lista todos os perfis
    - GET /usuarios/{id}/ - Detalhe de um perfil
    - PUT/PATCH /usuarios/{id}/ - Atualiza perfil (telefone, endereco, nif)
    - GET /usuarios/me/ - Perfil do usuário logado
    - PATCH /usuarios/{id}/update_user/ - Atualiza User (first_name, last_name, email)
    """
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.select_related('user').all()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retorna o perfil do usuário logado
        
        GET /usuarios/me/
        """
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_user(self, request, pk=None):
        """
        Atualiza informações do User (first_name, last_name, email)
        
        PATCH /usuarios/{id}/update_user/
        Body: {
            "first_name": "João",
            "last_name": "Silva",
            "email": "joao@example.com"
        }
        """
        profile = self.get_object()
        user = profile.user
        
        if request.user != user and not request.user.is_staff:
            return Response(
                {'error': 'Você não tem permissão para editar este usuário'},
                status=status.HTTP_403_FORBIDDEN
            )
        

        updated_fields = []
        
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
            updated_fields.append('first_name')
            
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
            updated_fields.append('last_name')
            
        if 'email' in request.data:
 
            email = request.data['email']
            if User.objects.exclude(pk=user.pk).filter(email=email).exists():
                return Response(
                    {'error': 'Este email já está em uso por outro usuário'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.email = email
            updated_fields.append('email')
        
        # Salvar alterações
        if updated_fields:
            user.save(update_fields=updated_fields)
        
    
        serializer = self.get_serializer(profile)
        return Response({
            'message': f'Usuário atualizado com sucesso. Campos alterados: {", ".join(updated_fields)}',
            'data': serializer.data
        })