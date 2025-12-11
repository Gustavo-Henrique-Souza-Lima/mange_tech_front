from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, User
from django.db import transaction

from .base import BaseViewSet
from ..models import UserProfile
from ..serializers import UserProfileSerializer, UserSerializer 
from ..permissions import IsAdminUser, IsOwnerOrReadOnly 

class UserProfileViewSet(BaseViewSet):
    """
    Endpoints para gestão de perfis e usuários.
    """
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.select_related('user').all()
    
    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            return [IsAuthenticated()] 
        
        if self.action == 'create':
            return [IsAuthenticated()] 
            
        if self.action in ['retrieve', 'update', 'partial_update', 'update_user', 'me']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
            
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        data = request.data
        
        cargo_solicitado = data.get('cargo', 'USUARIO')
        quem_cria = request.user
        
        e_admin = quem_cria.is_superuser or quem_cria.groups.filter(name='ADMIN').exists()
        
        if cargo_solicitado in ['ADMIN', 'SUPERVISOR'] and not e_admin:
            return Response(
                {'error': 'Apenas Administradores podem criar usuários com nível Admin ou Supervisor.'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            with transaction.atomic():
                
                if User.objects.filter(username=data.get('username')).exists():
                    return Response({'error': 'Nome de usuário já existe.'}, status=400)
                if User.objects.filter(email=data.get('email')).exists():
                    return Response({'error': 'Email já cadastrado.'}, status=400)

                user = User.objects.create_user(
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password'),
                    first_name=data.get('first_name', ''),
                    last_name=data.get('last_name', '')
                )

                if cargo_solicitado == 'ADMIN':
                    user.is_superuser = True
                    user.is_staff = True
                    g, _ = Group.objects.get_or_create(name='ADMIN')
                    user.groups.add(g)
                elif cargo_solicitado == 'SUPERVISOR':
                    user.is_staff = True
                    g, _ = Group.objects.get_or_create(name='SUPERVISOR')
                    user.groups.add(g)
                elif cargo_solicitado == 'TECNICO':
                    user.is_staff = True # Opcional
                    g, _ = Group.objects.get_or_create(name='TECNICO')
                    user.groups.add(g)
                
                user.save()

                
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.telefone = data.get('telefone', '')
                profile.endereco = data.get('endereco', '')
                profile.nif = data.get('nif', '')
                profile.save()

                serializer = self.get_serializer(profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Erro ao criar usuário: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retorna os dados do User logado,
        forçando o uso do UserSerializer para incluir 'is_superuser' e 'groups'
        no nível superior do JSON.
        """
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_user(self, request, pk=None):
        profile = self.get_object()
        user = profile.user
        data = request.data
        
        eh_admin_ou_supervisor = request.user.is_superuser or request.user.groups.filter(name__in=['ADMIN', 'SUPERVISOR']).exists()
        eh_dono = request.user == user

        if not eh_dono and not eh_admin_ou_supervisor:
            return Response(
                {'error': 'Você não tem permissão para editar este usuário.'},
                status=status.HTTP_403_FORBIDDEN
            )

        updated_fields = []
        
        if 'first_name' in data:
            user.first_name = data['first_name']
            updated_fields.append('first_name')
            
        if 'last_name' in data:
            user.last_name = data['last_name']
            updated_fields.append('last_name')
            
        if 'email' in data:
            email = data['email']
            if User.objects.exclude(pk=user.pk).filter(email=email).exists():
                return Response(
                    {'error': 'Este email já está em uso por outro usuário.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.email = email
            updated_fields.append('email')

        if eh_admin_ou_supervisor:
            if 'is_active' in data:
                novo_status = data['is_active']
                if user == request.user and novo_status is False:
                    return Response(
                        {'error': 'Você não pode desativar seu próprio usuário.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user.is_active = novo_status
                updated_fields.append('is_active')

            if 'cargo' in data:
                novo_cargo = data['cargo']
                quem_edita = request.user
                e_admin_supremo = quem_edita.is_superuser or quem_edita.groups.filter(name='ADMIN').exists()

                if novo_cargo in ['ADMIN', 'SUPERVISOR'] and not e_admin_supremo:
                     return Response({'error': 'Apenas Administradores podem promover para Admin ou Supervisor.'}, status=403)

                user.groups.clear()
                user.is_superuser = False
                user.is_staff = False 
                
                if novo_cargo == 'ADMIN':
                    user.is_superuser = True
                    user.is_staff = True
                    grupo, _ = Group.objects.get_or_create(name='ADMIN')
                    user.groups.add(grupo)
                    
                elif novo_cargo == 'SUPERVISOR':
                    user.is_staff = True 
                    grupo, _ = Group.objects.get_or_create(name='SUPERVISOR')
                    user.groups.add(grupo)
                    
                elif novo_cargo == 'TECNICO':
                    user.is_staff = True 
                    grupo, _ = Group.objects.get_or_create(name='TECNICO')
                    user.groups.add(grupo)
                    
                elif novo_cargo == 'padrao' or novo_cargo == 'USUARIO':
                    pass
                
                updated_fields.append('groups')
                updated_fields.append('is_superuser')
                updated_fields.append('is_staff')

        if 'groups' in updated_fields:
            user.save() 
        elif updated_fields:
            user.save(update_fields=[f for f in updated_fields if f not in ['groups']])
        
        serializer = self.get_serializer(profile)
        return Response({
            'message': 'Usuário atualizado com sucesso.',
            'campos_alterados': updated_fields,
            'data': serializer.data
        })