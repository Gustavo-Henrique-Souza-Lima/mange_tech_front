"""
Exporta todos os ViewSets e funções para manter compatibilidade
com urls.py sem precisar mudar os imports
"""

from .auth import register_user, current_user
from .perfis import UserProfileViewSet
from .ativos import CategoriaViewSet, AmbienteViewSet, AtivoViewSet
from .chamados import ChamadoViewSet
from .historico import ChamadoStatusHistoryViewSet
from .anexos import AnexoViewSet
from .notificacoes import NotificacaoViewSet

__all__ = [
    # Autenticação
    'register_user',
    'current_user',
    
    # ViewSets
    'UserProfileViewSet',
    'CategoriaViewSet',
    'AmbienteViewSet',
    'AtivoViewSet',
    'ChamadoViewSet',
    'ChamadoStatusHistoryViewSet',
    'AnexoViewSet',
    'NotificacaoViewSet',
]