"""
ViewSet para Notificações
"""

from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .base import BaseViewSet
from ..models import Notificacao
from ..serializers import NotificacaoSerializer


class NotificacaoViewSet(BaseViewSet):
    """
    ViewSet para notificações do usuário
    
    Endpoints:
    - GET /notificacoes/ - Lista notificações do usuário logado
    - GET /notificacoes/{id}/ - Detalhe de uma notificação
    - DELETE /notificacoes/{id}/ - Remove notificação
    - GET /notificacoes/nao_lidas/ - Lista não lidas
    - POST /notificacoes/{id}/marcar_lida/ - Marca como lida
    - POST /notificacoes/marcar_todas_lidas/ - Marca todas como lidas
    """
    serializer_class = NotificacaoSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['lida']
    
    def get_queryset(self):
        """Retorna apenas notificações do usuário logado"""
        return Notificacao.objects.select_related(
            'chamado', 'usuario'
        ).filter(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def nao_lidas(self, request):
        """Lista notificações não lidas"""
        notificacoes = self.get_queryset().filter(lida=False)
        serializer = self.get_serializer(notificacoes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):
        """Marca uma notificação como lida"""
        notificacao = self.get_object()
        notificacao.marcar_como_lida()
        serializer = self.get_serializer(notificacao)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def marcar_todas_lidas(self, request):
        """Marca todas as notificações como lidas"""
        self.get_queryset().filter(lida=False).update(lida=True)
        return Response({'message': 'Todas as notificações foram marcadas como lidas'})