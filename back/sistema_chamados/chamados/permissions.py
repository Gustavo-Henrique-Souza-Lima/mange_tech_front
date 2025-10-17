from rest_framework import permissions
from django.contrib.auth.models import User, Group


def check_group(group_name, user_id):
    """Verifica se um usuário pertence a um grupo específico"""
    try:
        custom_user = User.objects.get(id=user_id)
        return custom_user.groups.filter(name=group_name).exists()
    except User.DoesNotExist:
        return False

        
def is_admin(user_id):
    """Verifica se o usuário é admin"""
    return check_group('ADMIN', user_id)


def is_tecnico(user_id):
    """Verifica se o usuário é técnico"""
    return check_group('TECNICO', user_id)


def is_supervisor(user_id):
    """Verifica se o usuário é supervisor"""
    return check_group('SUPERVISOR', user_id)


class IsAdminUser(permissions.BasePermission):
    """Permissão para apenas administradores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or is_admin(request.user.id)
        )


class IsTecnicoOrAdmin(permissions.BasePermission):
    """Permissão para técnicos e administradores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            is_tecnico(request.user.id) or 
            is_admin(request.user.id) or 
            request.user.is_staff
        )


class IsSupervisorOrAdmin(permissions.BasePermission):
    """Permissão para supervisores e administradores"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            is_supervisor(request.user.id) or 
            is_admin(request.user.id) or 
            request.user.is_staff
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas o dono do objeto possa editá-lo.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissões de escrita apenas para o dono do objeto
        return obj.solicitante == request.user


class IsChamadoSolicitanteOrResponsavel(permissions.BasePermission):
    """
    Permissão para solicitantes e responsáveis do chamado
    """
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.is_staff or is_admin(request.user.id):
            return True
        
        # Solicitante tem acesso
        if hasattr(obj, 'solicitante') and obj.solicitante == request.user:
            return True
        
        # Responsáveis têm acesso
        if hasattr(obj, 'responsaveis'):
            responsaveis_ids = obj.responsaveis.values_list('responsavel_id', flat=True)
            if request.user.id in responsaveis_ids:
                return True
        
        return False


class CanChangeStatus(permissions.BasePermission):
    """
    Permissão para alterar status do chamado
    """
    def has_object_permission(self, request, view, obj):
        # Administradores podem alterar qualquer status
        if request.user.is_staff or is_admin(request.user.id):
            return True
        
        # Responsáveis podem alterar status
        if hasattr(obj, 'responsaveis'):
            responsaveis_ids = obj.responsaveis.values_list('responsavel_id', flat=True)
            if request.user.id in responsaveis_ids:
                return True
        
        # Supervisores podem alterar status
        if is_supervisor(request.user.id):
            return True
        
        return False


class CanAtribuirResponsavel(permissions.BasePermission):
    """
    Permissão para atribuir responsáveis aos chamados
    """
    def has_permission(self, request, view):
        # Apenas supervisores e administradores podem atribuir responsáveis
        return request.user and request.user.is_authenticated and (
            is_supervisor(request.user.id) or 
            is_admin(request.user.id) or 
            request.user.is_staff
        )


# Função helper para criar grupos padrão
def create_default_groups():
    """Cria os grupos padrão do sistema"""
    groups = ['ADMIN', 'SUPERVISOR', 'TECNICO', 'USUARIO']
    
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
    
    print("Grupos padrão criados com sucesso!")