"""
ViewSet para Histórico de Status
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import ChamadoStatusHistory
from ..serializers import ChamadoStatusHistoryReadSerializer


class ChamadoStatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para histórico de status (somente leitura)
    
    Endpoints:
    - GET /historico/ - Lista todo o histórico
    - GET /historico/{id}/ - Detalhe de um registro
    """
    serializer_class = ChamadoStatusHistoryReadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['chamado', 'status', 'user']
    
    def get_queryset(self):
        return ChamadoStatusHistory.objects.select_related(
            'chamado', 'user'
        ).prefetch_related('anexos').all()