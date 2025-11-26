"""
ViewSets para Categorias, Ambientes e Ativos
"""

from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .base import BaseViewSet, ReadWriteSerializerMixin
from ..models import Categoria, Ambiente, Ativo
from ..serializers import (
    CategoriaSerializer,
    AmbienteReadSerializer,
    AmbienteWriteSerializer,
    AtivoReadSerializer,
    AtivoWriteSerializer
)


class CategoriaViewSet(BaseViewSet):
    """
    ViewSet para Categorias de Ativos
    
    Endpoints:
    - GET /categorias/ - Lista todas as categorias
    - POST /categorias/ - Cria nova categoria
    - GET /categorias/{id}/ - Detalhe de uma categoria
    - PUT/PATCH /categorias/{id}/ - Atualiza categoria
    - DELETE /categorias/{id}/ - Remove categoria
    """
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']
    
    def get_queryset(self):
        """Otimiza queries com prefetch dos ativos relacionados"""
        return Categoria.objects.prefetch_related('ativos').all()


class AmbienteViewSet(ReadWriteSerializerMixin, BaseViewSet):
    """
    ViewSet para Ambientes/Locais
    
    Endpoints:
    - GET /ambientes/ - Lista todos os ambientes
    - POST /ambientes/ - Cria novo ambiente
    - GET /ambientes/{id}/ - Detalhe de um ambiente
    - PUT/PATCH /ambientes/{id}/ - Atualiza ambiente
    - DELETE /ambientes/{id}/ - Remove ambiente
    - GET /ambientes/{id}/ativos/ - Lista ativos do ambiente
    """
    read_serializer_class = AmbienteReadSerializer
    write_serializer_class = AmbienteWriteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'localizacao_ambiente']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']
    
    def get_queryset(self):
        """Otimiza queries com select_related e prefetch_related"""
        return Ambiente.objects.select_related('responsavel').prefetch_related('ativos').all()
    
    @action(detail=True, methods=['get'])
    def ativos(self, request, pk=None):
        """
        Lista todos os ativos de um ambiente específico
        
        GET /ambientes/{id}/ativos/
        """
        ambiente = self.get_object()
        ativos = ambiente.ativos.select_related('categoria', 'ambiente')
        serializer = AtivoReadSerializer(ativos, many=True)
        return Response(serializer.data)


class AtivoViewSet(ReadWriteSerializerMixin, BaseViewSet):
    """
    ViewSet para Ativos/Equipamentos
    
    Endpoints:
    - GET /ativos/ - Lista todos os ativos (com filtros)
    - POST /ativos/ - Cria novo ativo
    - GET /ativos/{id}/ - Detalhe de um ativo
    - PUT/PATCH /ativos/{id}/ - Atualiza ativo
    - DELETE /ativos/{id}/ - Remove ativo
    - POST /ativos/{id}/alterar_status/ - Altera status do ativo
    """
    read_serializer_class = AtivoReadSerializer
    write_serializer_class = AtivoWriteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'codigo_patrimonio', 'descricao']
    ordering_fields = ['nome', 'created_at', 'status']
    ordering = ['-created_at']
    filterset_fields = ['status', 'ambiente', 'categoria']
    
    def get_queryset(self):
        """Otimiza queries com select_related"""
        return Ativo.objects.select_related('ambiente', 'categoria').all()
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        """
        Altera o status de um ativo
        
        POST /ativos/{id}/alterar_status/
        Body: {
            "status": "novo_status"
        }
        """
        ativo = self.get_object()
        novo_status = request.data.get('status')
        
        # Validação
        if not novo_status:
            return Response(
                {'error': 'status é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if novo_status not in dict(Ativo.STATUS_CHOICES):
            return Response(
                {'error': f'Status inválido. Opções: {", ".join(dict(Ativo.STATUS_CHOICES).keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualiza status
        ativo.status = novo_status
        ativo.save()
        
        serializer = self.get_serializer(ativo)
        return Response(serializer.data)
