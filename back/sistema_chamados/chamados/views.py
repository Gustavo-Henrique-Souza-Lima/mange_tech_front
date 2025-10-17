from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    UserProfile, Categoria, Ambiente, Ativo, Chamado, 
    ChamadoResponsavel, ChamadoStatusHistory, Anexo, Notificacao
)
from .serializers import (
    UserProfileSerializer, CategoriaSerializer,
    AmbienteReadSerializer, AmbienteWriteSerializer,
    AtivoReadSerializer, AtivoWriteSerializer,
    ChamadoListSerializer, ChamadoDetailSerializer, 
    ChamadoCreateSerializer, ChamadoUpdateSerializer,
    ChamadoResponsavelSerializer,
    ChamadoStatusHistoryReadSerializer, ChamadoStatusHistoryWriteSerializer,
    AnexoSerializer, NotificacaoSerializer, ReadWriteSerializerMixin
)
from .filters import ChamadoFilter


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para perfis de usuário"""
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna o perfil do usuário logado"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para categorias"""
    queryset = Categoria.objects.prefetch_related('ativos').all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']


class AmbienteViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """ViewSet para ambientes"""
    queryset = Ambiente.objects.select_related('responsavel').prefetch_related('ativos').all()
    read_serializer_class = AmbienteReadSerializer
    write_serializer_class = AmbienteWriteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'localizacao_ambiente']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']
    
    @action(detail=True, methods=['get'])
    def ativos(self, request, pk=None):
        """Lista todos os ativos de um ambiente"""
        ambiente = self.get_object()
        ativos = ambiente.ativos.select_related('categoria', 'ambiente')
        serializer = AtivoReadSerializer(ativos, many=True)
        return Response(serializer.data)


class AtivoViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """ViewSet para ativos"""
    queryset = Ativo.objects.select_related('ambiente', 'categoria').all()
    read_serializer_class = AtivoReadSerializer
    write_serializer_class = AtivoWriteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'codigo_patrimonio', 'descricao']
    ordering_fields = ['nome', 'created_at', 'status']
    ordering = ['-created_at']
    filterset_fields = ['status', 'ambiente', 'categoria']
    
    @action(detail=False, methods=['get'])
    def por_ambiente(self, request):
        """Filtra ativos por ambiente"""
        ambiente_id = request.query_params.get('ambiente_id')
        if not ambiente_id:
            return Response(
                {'error': 'ambiente_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ativos = self.queryset.filter(ambiente_id=ambiente_id)
        serializer = self.get_serializer(ativos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Filtra ativos por categoria"""
        categoria_id = request.query_params.get('categoria_id')
        if not categoria_id:
            return Response(
                {'error': 'categoria_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ativos = self.queryset.filter(categoria_id=categoria_id)
        serializer = self.get_serializer(ativos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        """Altera o status de um ativo"""
        ativo = self.get_object()
        novo_status = request.data.get('status')
        
        if novo_status not in dict(Ativo.STATUS_CHOICES):
            return Response(
                {'error': 'Status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ativo.status = novo_status
        ativo.save()
        serializer = self.get_serializer(ativo)
        return Response(serializer.data)


class ChamadoViewSet(viewsets.ModelViewSet):
    """ViewSet para chamados com sistema de log automático"""
    queryset = Chamado.objects.select_related('solicitante').prefetch_related(
        'ativos', 'responsaveis__responsavel', 'historico__user', 'anexos', 'notificacoes'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['created_at', 'data_sugerida', 'urgencia', 'status']
    ordering = ['-created_at']
    filterset_class = ChamadoFilter
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ChamadoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ChamadoUpdateSerializer
        elif self.action == 'list':
            return ChamadoListSerializer
        return ChamadoDetailSerializer
    
    def perform_create(self, serializer):
        """
        Sobrescreve a criação para adicionar lógica adicional.
        O log inicial é criado automaticamente pelo signal post_save.
        """
        chamado = serializer.save()
        
        # Criar notificação para administradores
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notificacao.objects.create(
                texto=f'Novo chamado criado: {chamado.titulo}',
                chamado=chamado,
                usuario=admin
            )
    
    @action(detail=True, methods=['post'])
    def atribuir_responsavel(self, request, pk=None):
        """Atribui um responsável ao chamado"""
        chamado = self.get_object()
        responsavel_id = request.data.get('responsavel_id')
        role = request.data.get('role', 'responsavel_tecnico')
        
        if not responsavel_id:
            return Response(
                {'error': 'responsavel_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            responsavel = User.objects.get(id=responsavel_id)
            chamado_responsavel, created = ChamadoResponsavel.objects.get_or_create(
                chamado=chamado,
                responsavel=responsavel,
                defaults={'role': role}
            )
            
            if created:
                # Adicionar log manualmente (não muda status, apenas registra a ação)
                chamado.adicionar_log_status(
                    user=request.user,
                    comentario=f'Responsável {responsavel.get_full_name() or responsavel.username} atribuído como {dict(ChamadoResponsavel.ROLE_CHOICES).get(role)}'
                )
                
                # Criar notificação para o responsável
                Notificacao.objects.create(
                    texto=f'Você foi atribuído ao chamado: {chamado.titulo}',
                    chamado=chamado,
                    usuario=responsavel
                )
                
                serializer = ChamadoResponsavelSerializer(chamado_responsavel)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'message': 'Responsável já atribuído ao chamado'}, 
                    status=status.HTTP_200_OK
                )
                
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remover_responsavel(self, request, pk=None):
        """Remove um responsável do chamado"""
        chamado = self.get_object()
        responsavel_id = request.data.get('responsavel_id')
        
        if not responsavel_id:
            return Response(
                {'error': 'responsavel_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            responsavel = User.objects.get(id=responsavel_id)
            chamado_responsavel = ChamadoResponsavel.objects.filter(
                chamado=chamado,
                responsavel=responsavel
            ).first()
            
            if chamado_responsavel:
                chamado_responsavel.delete()
                
                # Adicionar log manualmente (não muda status, apenas registra a ação)
                chamado.adicionar_log_status(
                    user=request.user,
                    comentario=f'Responsável {responsavel.get_full_name() or responsavel.username} removido'
                )
                
                return Response(
                    {'message': 'Responsável removido com sucesso'}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Responsável não encontrado no chamado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuário não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        """
        Altera o status do chamado usando o método mudar_status().
        O log é criado automaticamente.
        """
        chamado = self.get_object()
        novo_status = request.data.get('status')
        comentario = request.data.get('comentario', '')
        
        if not novo_status:
            return Response(
                {'error': 'status é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if novo_status not in dict(Chamado.STATUS_CHOICES):
            return Response(
                {'error': 'Status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Usa o método mudar_status que já cria o log automaticamente
        status_anterior = chamado.mudar_status(
            novo_status=novo_status,
            user=request.user,
            comentario=comentario or f'Status alterado para {dict(Chamado.STATUS_CHOICES).get(novo_status)}'
        )
        
        # Notificar solicitante e responsáveis
        usuarios_notificar = [chamado.solicitante]
        usuarios_notificar.extend([r.responsavel for r in chamado.responsaveis.all()])
        
        for usuario in set(usuarios_notificar):
            if usuario != request.user:  # Não notificar quem fez a alteração
                Notificacao.objects.create(
                    texto=f'Chamado "{chamado.titulo}" teve status alterado para {chamado.get_status_display()}',
                    chamado=chamado,
                    usuario=usuario
                )
        
        serializer = self.get_serializer(chamado)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """Retorna o histórico completo de mudanças de status do chamado"""
        chamado = self.get_object()
        historico = chamado.historico.all()
        serializer = ChamadoStatusHistoryReadSerializer(historico, many=True)
        return Response({
            'chamado_id': chamado.id,
            'chamado_titulo': chamado.titulo,
            'status_atual': chamado.status,
            'total_registros': historico.count(),
            'historico': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def adicionar_comentario(self, request, pk=None):
        """Adiciona um comentário ao chamado sem mudar o status"""
        chamado = self.get_object()
        comentario = request.data.get('comentario', '')
        
        if not comentario:
            return Response(
                {'error': 'comentario é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Adiciona log com o status atual (não muda status)
        chamado.adicionar_log_status(
            user=request.user,
            comentario=comentario
        )
        
        # Notificar solicitante e responsáveis sobre o novo comentário
        usuarios_notificar = [chamado.solicitante]
        usuarios_notificar.extend([r.responsavel for r in chamado.responsaveis.all()])
        
        for usuario in set(usuarios_notificar):
            if usuario != request.user:
                Notificacao.objects.create(
                    texto=f'Novo comentário no chamado "{chamado.titulo}"',
                    chamado=chamado,
                    usuario=usuario
                )
        
        return Response({
            'message': 'Comentário adicionado com sucesso',
            'chamado_id': chamado.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def meus_chamados(self, request):
        """Lista chamados criados pelo usuário logado"""
        chamados = self.queryset.filter(solicitante=request.user)
        page = self.paginate_queryset(chamados)
        
        if page is not None:
            serializer = ChamadoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ChamadoListSerializer(chamados, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def atribuidos_a_mim(self, request):
        """Lista chamados atribuídos ao usuário logado"""
        chamados = self.queryset.filter(
            responsaveis__responsavel=request.user
        ).distinct()
        page = self.paginate_queryset(chamados)
        
        if page is not None:
            serializer = ChamadoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ChamadoListSerializer(chamados, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def em_atraso(self, request):
        """Lista chamados em atraso"""
        chamados = self.queryset.filter(
            data_sugerida__lt=timezone.now(),
            status__in=['aberto', 'aguardando_responsaveis', 'em_andamento']
        )
        page = self.paginate_queryset(chamados)
        
        if page is not None:
            serializer = ChamadoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ChamadoListSerializer(chamados, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas sobre os chamados"""
        from django.db.models import Count, Q, Avg
        from datetime import timedelta
        
        total = self.queryset.count()
        por_status = self.queryset.values('status').annotate(total=Count('id'))
        por_urgencia = self.queryset.values('urgencia').annotate(total=Count('id'))
        
        em_atraso = self.queryset.filter(
            data_sugerida__lt=timezone.now(),
            status__in=['aberto', 'aguardando_responsaveis', 'em_andamento']
        ).count()
        
        concluidos_mes = self.queryset.filter(
            data_conclusao__month=timezone.now().month,
            data_conclusao__year=timezone.now().year,
            status='concluido'
        ).count()
        
        # Estatísticas adicionais sobre o histórico
        total_mudancas_status = ChamadoStatusHistory.objects.filter(
            chamado__in=self.queryset
        ).count()
        
        # Chamados mais ativos (com mais mudanças de status)
        chamados_mais_ativos = self.queryset.annotate(
            num_mudancas=Count('historico')
        ).order_by('-num_mudancas')[:5]
        
        return Response({
            'total': total,
            'por_status': list(por_status),
            'por_urgencia': list(por_urgencia),
            'em_atraso': em_atraso,
            'concluidos_mes_atual': concluidos_mes,
            'total_mudancas_status': total_mudancas_status,
            'chamados_mais_ativos': [
                {
                    'id': c.id,
                    'titulo': c.titulo,
                    'num_mudancas': c.num_mudancas
                } for c in chamados_mais_ativos
            ]
        })


class ChamadoStatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para histórico de status (somente leitura).
    Os registros são criados automaticamente pelos signals no model.
    """
    queryset = ChamadoStatusHistory.objects.select_related('chamado', 'user').prefetch_related('anexos').all()
    serializer_class = ChamadoStatusHistoryReadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['chamado', 'status', 'user']
    
    @action(detail=False, methods=['get'])
    def ultimas_mudancas(self, request):
        """Retorna as últimas mudanças de status de todos os chamados"""
        limit = int(request.query_params.get('limit', 20))
        historico = self.queryset.all()[:limit]
        serializer = self.get_serializer(historico, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_usuario(self, request):
        """Lista histórico de mudanças feitas pelo usuário logado"""
        historico = self.queryset.filter(user=request.user)
        page = self.paginate_queryset(historico)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(historico, many=True)
        return Response(serializer.data)


class AnexoViewSet(viewsets.ModelViewSet):
    """ViewSet para anexos"""
    queryset = Anexo.objects.select_related('chamado', 'usuario_upload', 'chamado_history').all()
    serializer_class = AnexoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['data_upload']
    ordering = ['-data_upload']
    filterset_fields = ['chamado', 'mimetype']
    
    def create(self, request, *args, **kwargs):
        """Sobrescreve a criação para adicionar o usuário do upload"""
        chamado_id = request.data.get('chamado')
        if not chamado_id:
            return Response(
                {'error': 'chamado é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            chamado = Chamado.objects.get(id=chamado_id)
            serializer = self.get_serializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save(
                    chamado=chamado, 
                    usuario_upload=request.user
                )
                
                # Criar histórico se tiver chamado_history_id
                chamado_history_id = request.data.get('chamado_history')
                if chamado_history_id:
                    try:
                        history = ChamadoStatusHistory.objects.get(id=chamado_history_id)
                        anexo = Anexo.objects.get(id=serializer.data['id'])
                        anexo.chamado_history = history
                        anexo.save()
                    except ChamadoStatusHistory.DoesNotExist:
                        pass
                
                # Adiciona log sobre o anexo
                chamado.adicionar_log_status(
                    user=request.user,
                    comentario=f'Anexo adicionado: {serializer.data.get("nome_arquivo", "arquivo")}'
                )
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Chamado.DoesNotExist:
            return Response(
                {'error': 'Chamado não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class NotificacaoViewSet(viewsets.ModelViewSet):
    """ViewSet para notificações"""
    queryset = Notificacao.objects.select_related('chamado', 'usuario').all()
    serializer_class = NotificacaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['lida']
    
    def get_queryset(self):
        """Retorna apenas notificações do usuário logado"""
        return self.queryset.filter(usuario=self.request.user)
    
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