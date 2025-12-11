from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, User
from django.db import transaction

from .base import BaseViewSet
from ..models import UserProfile
from ..serializers import UserProfileSerializer, UserSerializer 
from ..permissions import IsAdminUser, IsOwnerOrReadOnly # Mantendo suas permissões

class UserProfileViewSet(BaseViewSet):
    """
    Endpoints para gestão de perfis e usuários.
    """
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        # Usar prefetch_related para groups e select_related para user é crucial para performance
        return UserProfile.objects.select_related('user').prefetch_related('user__groups').all()
    
    def get_permissions(self):
        # 🚨 CORREÇÃO DE PERMISSÕES: Priorizar regras de nível mais alto
        # Retorna a lista de objetos de permissão
        
        # Permissões mais permissivas ou específicas de nível de objeto:
        if self.action in ['retrieve', 'update', 'partial_update', 'update_user']:
            # Apenas o dono ou um Admin/Supervisor pode editar.
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        
        # Permissões de nível de lista/criação/destruição:
        if self.action in ['list', 'destroy']:
            # Apenas AdminUser pode listar ou destruir
            return [IsAdminUser()] # Usando a sua permissão IsAdminUser, se ela existir
        
        # Endpoint 'me'
        if self.action == 'me':
            return [IsAuthenticated()]
        
        # Criação (Qualquer um pode criar, mas a lógica de cargo é checada internamente)
        if self.action == 'create':
            return [IsAuthenticated()]
            
        return [IsAuthenticated()] # Padrão para qualquer ação não listada (como 'create' ou outras customizadas)


    # ----------------------------------------------------
    # CREATE (Criação de Usuário)
    # ----------------------------------------------------
    def create(self, request, *args, **kwargs):
        data = request.data
        
        # 🚨 Otimização: Define padrão para evitar KeyError
        cargo_solicitado = data.get('cargo', 'USUARIO').upper() # Garante que está em caixa alta
        quem_cria = request.user
        
        # Checagem de permissão para criar cargos elevados (ADMIN/SUPERVISOR)
        e_admin_supremo = quem_cria.is_superuser or quem_cria.groups.filter(name='ADMIN').exists()
        
        if cargo_solicitado in ['ADMIN', 'SUPERVISOR'] and not e_admin_supremo:
            return Response(
                {'error': 'Apenas Administradores podem criar usuários com nível Admin ou Supervisor.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # 🚨 Validação de campos obrigatórios antes do transaction.atomic
        required_fields = ['username', 'email', 'password']
        if not all(data.get(field) for field in required_fields):
             return Response(
                 {'error': 'Campos obrigatórios (username, email, password) estão faltando.'},
                 status=status.HTTP_400_BAD_REQUEST
             )
        
        try:
            with transaction.atomic():
                
                # Checagem de Unicidade
                if User.objects.filter(username=data['username']).exists():
                    return Response({'error': 'Nome de usuário já existe.'}, status=status.HTTP_400_BAD_REQUEST)
                if User.objects.filter(email=data['email']).exists():
                    return Response({'error': 'Email já cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)

                # Criação do Usuário
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data.get('first_name', ''),
                    last_name=data.get('last_name', '')
                )

                # Atribuição de Grupos e Flags
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
                    user.is_staff = True 
                    g, _ = Group.objects.get_or_create(name='TECNICO')
                    user.groups.add(g)
                
                user.save()

                # Criação do Perfil
                profile = UserProfile.objects.create(
                    user=user,
                    telefone=data.get('telefone', ''),
                    endereco=data.get('endereco', ''),
                    nif=data.get('nif', '')
                )
                
                # 🚨 ATENÇÃO: Se o frontend não envia 'telefone', 'endereco', 'nif', 
                # use o serializer para validar e criar se preferir. 
                # Aqui estamos fazendo a criação manual.

                serializer = self.get_serializer(profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # 🚨 Tratamento de erro mais específico
            return Response(
                {'error': f'Erro interno ao criar usuário. Tente novamente. Detalhe: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ----------------------------------------------------
    # ME (Solução para o Frontend)
    # ----------------------------------------------------
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retorna os dados do User logado, usando o UserSerializer (Plano) 
        para garantir que 'is_superuser' e 'groups' estejam no nível superior do JSON.
        Isso resolve o problema do Frontend que não conseguia ler a permissão.
        """
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    # ----------------------------------------------------
    # UPDATE_USER (Atualização de Dados e Cargo)
    # ----------------------------------------------------
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
        
        # 🚨 Otimização: Use um UserSerializer para lidar com dados do User.
        # No entanto, mantendo sua lógica atual para ser mais direto:

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

        # Lógica de Flags e Cargo (Apenas para Admin/Supervisor)
        if eh_admin_ou_supervisor:
            if 'is_active' in data:
                # ... (Lógica de desativação)
                # O restante da lógica de 'is_active' está correta.
                
                novo_status = data['is_active']
                if user == request.user and novo_status is False:
                     return Response(
                         {'error': 'Você não pode desativar seu próprio usuário.'},
                         status=status.HTTP_400_BAD_REQUEST
                     )
                user.is_active = novo_status
                updated_fields.append('is_active')

            if 'cargo' in data:
                novo_cargo = data['cargo'].upper()
                quem_edita = request.user
                e_admin_supremo = quem_edita.is_superuser or quem_edita.groups.filter(name='ADMIN').exists()

                if novo_cargo in ['ADMIN', 'SUPERVISOR'] and not e_admin_supremo:
                     return Response({'error': 'Apenas Administradores podem promover para Admin ou Supervisor.'}, status=status.HTTP_403_FORBIDDEN)

                # 🚨 Lógica de Limpeza de Grupos e Flags (Correta e Necessária)
                user.groups.clear()
                user.is_superuser = False
                user.is_staff = False 
                
                # Atribuição de novo cargo (Lógica correta, use .get_or_create)
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
                    
                updated_fields.append('groups')
                updated_fields.append('is_superuser')
                updated_fields.append('is_staff')

        # 🚨 Otimização de Save (Corrige o problema de save desnecessário/incorreto)
        if updated_fields:
            # Salva o User
            user.save() 
            
            # Se for para atualizar campos do Profile, use o serializer principal (UserProfileSerializer)
            profile_serializer = self.get_serializer(profile, data=data, partial=True)
            if profile_serializer.is_valid(raise_exception=True):
                 profile_serializer.save()
            
            # 🚨 Usamos o serializer do Profile para retornar
            serializer_return = self.get_serializer(profile)
            return Response({
                'message': 'Usuário e Perfil atualizados com sucesso.',
                'campos_alterados': updated_fields,
                'data': serializer_return.data
            })
        
        # Caso não haja campos de User ou Profile para atualizar
        return Response({'message': 'Nenhum campo de usuário ou perfil foi fornecido para atualização.'}, status=status.HTTP_200_OK)