"""
Views de autenticação e registro de usuários
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import UserProfile
from ..serializers import RegisterSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Cadastro de novos usuários
    
    POST /api/register/
    Body: {
        "username": "string",
        "email": "string",
        "password": "string",
        "first_name": "string" (opcional),
        "last_name": "string" (opcional)
    }
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Cria perfil automaticamente
        UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Usuário cadastrado com sucesso!',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Retorna informações do usuário autenticado
    
    GET /api/me/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)