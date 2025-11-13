"""
ViewSet para Chamados - Refatorado e limpo
"""

from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .base import BaseViewSet
from ..models import Chamado
from ..serializers import (
    ChamadoListSerializer, 
    ChamadoDetailSerializer,
    ChamadoCreateSerializer, 
    ChamadoUpdateSerializer,
    ChamadoResponsavelSerializer
)
from ..filters import ChamadoFilter
from ..services.chamado_service import ChamadoService


class ChamadoViewSet(BaseViewSet):
    """
    ViewSet para gerenciamento de Chamados
    
    Endpoints:
    - GET /chamados/ - Lista todos os chamados (com filtros)
    - POST /chamados/ - Cria novo chamado
    - GET /chamados/{id}/ - Detalhe de um chamado
    - PUT/PATCH /chamados/{id}/ - Atualiza chamado
    - DELETE /chamados/{id}/remover/ - Remove chamado
    - GET /chamados/meus_chamados/ - Lista chamados do usuário logado
    - GET /chamados/estatisticas/ - Estatísticas gerais
    - POST /chamados/{id}/atribuir_responsavel/ - Atribui responsável
    - POST /chamados/{id}/alterar_status/ - Altera status do chamado
    """
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['created_at', 'data_sugerida', 'urgencia', 'status']
    ordering = ['-created_at']
    filterset_class = ChamadoFilter
    
    def get_queryset(self):
        """Otimiza queries com select_related e prefetch_related"""
        return Chamado.objects.select_related('solicitante').prefetch_related(
            'ativos',
            'responsaveis__responsavel',
            'historico__user',
            'anexos',
            'notificacoes'
        ).all()
    
    def get_serializer_class(self):
        """Retorna serializer apropriado para cada ação"""
        serializer_map = {
            'create': ChamadoCreateSerializer,
            'update': ChamadoUpdateSerializer,
            'partial_update': ChamadoUpdateSerializer,
            'list': ChamadoListSerializer,
        }
        return serializer_map.get(self.action, ChamadoDetailSerializer)
    
    def perform_create(self, serializer):
        """Cria chamado e notifica administradores"""
        chamado = serializer.save()
        ChamadoService.notificar_administradores(chamado)
    
    # ==========================================
    # AÇÕES CUSTOMIZADAS
    # ==========================================
    
    @action(detail=True, methods=['delete'], url_path='remover')
    def remover(self, request, pk=None):
        """
        Remove um chamado (endpoint customizado para validações adicionais)
        
        DELETE /chamados/{id}/remover/
        """
        chamado = self.get_object()
        
        # Valida permissões
        pode_remover, erro = ChamadoService.pode_remover(chamado, request.user)
        
        if not pode_remover:
            return Response(
                {'error': erro},
                status=status.HTTP_403_FORBIDDEN
            )
        
        chamado.delete()
        return Response(
            {'message': 'Chamado removido com sucesso'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, methods=['post'])
    def atribuir_responsavel(self, request, pk=None):
        """
        Atribui um responsável ao chamado
        
        POST /chamados/{id}/atribuir_responsavel/
        Body: {
            "responsavel_id": int,
            "role": "responsavel_tecnico" (opcional)
        }
        """
        chamado = self.get_object()
        responsavel_id = request.data.get('responsavel_id')
        role = request.data.get('role', 'responsavel_tecnico')
        
        # Validação
        if not responsavel_id:
            return Response(
                {'error': 'responsavel_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            responsavel = User.objects.get(id=responsavel_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Atribui responsável usando o serviço
        chamado_responsavel, created = ChamadoService.atribuir_responsavel(
            chamado=chamado,
            responsavel=responsavel,
            user_atual=request.user,
            role=role
        )
        
        # Resposta
        serializer = ChamadoResponsavelSerializer(chamado_responsavel)
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        return Response(
            serializer.data if created else {'message': 'Responsável já atribuído'},
            status=response_status
        )
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        """
        Altera o status do chamado
        
        POST /chamados/{id}/alterar_status/
        Body: {
            "status": "novo_status",
            "comentario": "Comentário opcional"
        }
        """
        chamado = self.get_object()
        novo_status = request.data.get('status')
        comentario = request.data.get('comentario', '')
        
        # Validação básica
        if not novo_status:
            return Response(
                {'error': 'status é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Altera status usando o serviço
        try:
            ChamadoService.alterar_status(
                chamado=chamado,
                novo_status=novo_status,
                user_atual=request.user,
                comentario=comentario
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(chamado)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def meus_chamados(self, request):
        """
        Lista chamados criados pelo usuário logado
        
        GET /chamados/meus_chamados/
        """
        chamados = self.get_queryset().filter(solicitante=request.user)
        page = self.paginate_queryset(chamados)
        
        if page is not None:
            serializer = ChamadoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ChamadoListSerializer(chamados, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        Retorna estatísticas sobre os chamados
        
        GET /chamados/estatisticas/
        """
        estatisticas = ChamadoService.obter_estatisticas(self.get_queryset())
        return Response(estatisticas)