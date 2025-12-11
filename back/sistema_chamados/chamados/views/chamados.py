"""
ViewSet para Chamados - Refatorado e limpo
"""
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .base import BaseViewSet
from ..models import Chamado, Anexo
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
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['created_at', 'data_sugerida', 'urgencia', 'status']
    ordering = ['-created_at']
    filterset_class = ChamadoFilter
    
    def get_queryset(self):
        return Chamado.objects.select_related('solicitante').prefetch_related(
            'ativos',
            'responsaveis__responsavel',
            'historico__user',
            'anexos',
            'notificacoes'
        ).all()
    
    def get_serializer_class(self):
        serializer_map = {
            'create': ChamadoCreateSerializer,
            'update': ChamadoUpdateSerializer,
            'partial_update': ChamadoUpdateSerializer,
            'list': ChamadoListSerializer,
        }
        return serializer_map.get(self.action, ChamadoDetailSerializer)
    
    def perform_create(self, serializer):
        chamado = serializer.save()
        ChamadoService.notificar_administradores(chamado)
    
    # --- AÇÕES CUSTOMIZADAS ---
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        chamado = self.get_object()
        novo_status = request.data.get('status')
        comentario = request.data.get('comentario', '')
        arquivo = request.FILES.get('arquivo')
        
        if not novo_status:
            return Response({'error': 'status é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Muda o status e recebe o histórico criado
            historico = chamado.mudar_status(
                novo_status=novo_status,
                user=request.user,
                comentario=comentario
            )

            # LÓGICA INTELIGENTE DE ATIVOS
            if novo_status in ['concluido', 'cancelado', 'realizado']:
                # Libera os ativos (Status volta para 'ativo')
                chamado.ativos.update(status='ativo')
            elif novo_status in ['em_andamento', 'aguardando_responsaveis']:
                # Trava os ativos em manutenção
                chamado.ativos.update(status='manutencao')

            # Salva o anexo se existir
            if arquivo:
                Anexo.objects.create(
                    chamado=chamado,
                    chamado_history=historico,
                    arquivo=arquivo,
                    usuario_upload=request.user
                )

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(chamado)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def comentar(self, request, pk=None):
        """
        Adiciona comentário/anexo sem alterar status
        POST /chamados/{id}/comentar/
        Form-Data: comentario, arquivo (opcional)
        """
        chamado = self.get_object()
        comentario = request.data.get('comentario')
        arquivo = request.FILES.get('arquivo') # Captura o arquivo
        
        # Agora permite apenas arquivo se não tiver texto
        if not comentario and not arquivo:
            return Response(
                {'error': 'É necessário enviar um comentário ou um arquivo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # ALTERADO: Capturamos o histórico retornado
        historico = chamado.adicionar_log_status(
            user=request.user,
            comentario=comentario or "Anexo adicionado"
        )

        # ADICIONADO: Se tiver arquivo, cria o anexo vinculado
        if arquivo:
            Anexo.objects.create(
                chamado=chamado,
                chamado_history=historico,
                arquivo=arquivo,
                usuario_upload=request.user
            )
        
        return Response({'message': 'Comentário/Anexo adicionado com sucesso'})
    
    @action(detail=False, methods=['get'])
    def meus_chamados(self, request):
        chamados = self.get_queryset().filter(solicitante=request.user)
        page = self.paginate_queryset(chamados)
        
        if page is not None:
            serializer = ChamadoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ChamadoListSerializer(chamados, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        estatisticas = ChamadoService.obter_estatisticas(self.get_queryset())
        return Response(estatisticas)