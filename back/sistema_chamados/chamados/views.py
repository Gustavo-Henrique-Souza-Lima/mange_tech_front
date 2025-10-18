# chamados/views.py - VERSÃO LIMPA E ORGANIZADA

from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    ChamadoStatusHistoryReadSerializer,
    AnexoSerializer, NotificacaoSerializer,
    ReadWriteSerializerMixin,
    RegisterSerializer, UserSerializer  # Para autenticação
)
from .filters import ChamadoFilter


# ============================================
# AUTENTICAÇÃO
# ============================================

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Cadastro de novos usuários - POST /api/register/"""
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Usuário cadastrado com sucesso!',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Retorna informações do usuário logado - GET /api/me/"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# ============================================
# USER PROFILE
# ============================================

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


# ============================================
# CATEGORIAS
# ============================================

class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para categorias"""
    queryset = Categoria.objects.prefetch_related('ativos').all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']


# ============================================
# AMBIENTES
# ============================================

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


# ============================================
# ATIVOS
# ============================================

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
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        """Altera o status de um ativo"""
        ativo = self.get_object()
        novo_status = request.data.get('status')
        
        if novo_status not in dict(Ativo.STATUS_CHOICES):
            return Response({'error': 'Status inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        ativo.status = novo_status
        ativo.save()
        serializer = self.get_serializer(ativo)
        return Response(serializer.data)


# ============================================
# CHAMADOS
# ============================================

class ChamadoViewSet(viewsets.ModelViewSet):
    """ViewSet para chamados"""
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
        """Cria chamado e notifica admins"""
        chamado = serializer.save()
        
        # Notificar administradores
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
            return Response({'error': 'responsavel_id é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            responsavel = User.objects.get(id=responsavel_id)
            chamado_responsavel, created = ChamadoResponsavel.objects.get_or_create(
                chamado=chamado,
                responsavel=responsavel,
                defaults={'role': role}
            )
            
            if created:
                chamado.adicionar_log_status(
                    user=request.user,
                    comentario=f'Responsável {responsavel.get_full_name() or responsavel.username} atribuído'
                )
                
                Notificacao.objects.create(
                    texto=f'Você foi atribuído ao chamado: {chamado.titulo}',
                    chamado=chamado,
                    usuario=responsavel
                )
                
                serializer = ChamadoResponsavelSerializer(chamado_responsavel)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Responsável já atribuído'}, status=status.HTTP_200_OK)
                
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        """Altera o status do chamado"""
        chamado = self.get_object()
        novo_status = request.data.get('status')
        comentario = request.data.get('comentario', '')
        
        if not novo_status:
            return Response({'error': 'status é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        if novo_status not in dict(Chamado.STATUS_CHOICES):
            return Response({'error': 'Status inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        chamado.mudar_status(
            novo_status=novo_status,
            user=request.user,
            comentario=comentario or f'Status alterado para {dict(Chamado.STATUS_CHOICES).get(novo_status)}'
        )
        
        # Notificar usuários
        usuarios_notificar = [chamado.solicitante]
        usuarios_notificar.extend([r.responsavel for r in chamado.responsaveis.all()])
        
        for usuario in set(usuarios_notificar):
            if usuario != request.user:
                Notificacao.objects.create(
                    texto=f'Chamado "{chamado.titulo}" teve status alterado para {chamado.get_status_display()}',
                    chamado=chamado,
                    usuario=usuario
                )
        
        serializer = self.get_serializer(chamado)
        return Response(serializer.data)
    
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
    def estatisticas(self, request):
        """Retorna estatísticas sobre os chamados"""
        from django.db.models import Count
        
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
        
        return Response({
            'total': total,
            'por_status': list(por_status),
            'por_urgencia': list(por_urgencia),
            'em_atraso': em_atraso,
            'concluidos_mes_atual': concluidos_mes
        })


# ============================================
# HISTÓRICO
# ============================================

class ChamadoStatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para histórico de status (somente leitura)"""
    queryset = ChamadoStatusHistory.objects.select_related('chamado', 'user').prefetch_related('anexos').all()
    serializer_class = ChamadoStatusHistoryReadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['chamado', 'status', 'user']


# ============================================
# ANEXOS
# ============================================

class AnexoViewSet(viewsets.ModelViewSet):
    """ViewSet para anexos"""
    queryset = Anexo.objects.select_related('chamado', 'usuario_upload').all()
    serializer_class = AnexoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['data_upload']
    ordering = ['-data_upload']
    filterset_fields = ['chamado', 'mimetype']
    
    def perform_create(self, serializer):
        """Adiciona usuário automaticamente ao criar anexo"""
        serializer.save(usuario_upload=self.request.user)


# ============================================
# NOTIFICAÇÕES
# ============================================

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