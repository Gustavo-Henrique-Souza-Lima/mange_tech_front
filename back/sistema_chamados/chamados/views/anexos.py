"""
ViewSet para Anexos
"""

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .base import BaseViewSet
from ..models import Anexo
from ..serializers import AnexoSerializer


class AnexoViewSet(BaseViewSet):
    """
    ViewSet para anexos de chamados
    
    Endpoints:
    - GET /anexos/ - Lista todos os anexos
    - POST /anexos/ - Upload de novo anexo
    - GET /anexos/{id}/ - Detalhe de um anexo
    - DELETE /anexos/{id}/ - Remove anexo
    """
    serializer_class = AnexoSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['data_upload']
    ordering = ['-data_upload']
    filterset_fields = ['chamado', 'mimetype']
    
    def get_queryset(self):
        return Anexo.objects.select_related('chamado', 'usuario_upload').all()
    
    def perform_create(self, serializer):
        """Adiciona usuário automaticamente ao criar anexo"""
        serializer.save(usuario_upload=self.request.user)