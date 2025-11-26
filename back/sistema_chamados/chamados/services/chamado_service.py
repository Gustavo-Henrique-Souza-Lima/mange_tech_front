"""
Lógica de negócio relacionada a Chamados
Extrai lógica complexa das views para facilitar testes e reutilização
"""

from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count

from ..models import Chamado, ChamadoResponsavel, Notificacao


class ChamadoService:
    """Serviço para operações de negócio em Chamados"""
    
    @staticmethod
    def notificar_administradores(chamado):
        """
        Notifica todos os administradores sobre um novo chamado
        
        Args:
            chamado: Instância de Chamado
        """
        admins = User.objects.filter(is_staff=True)
        
        notificacoes = [
            Notificacao(
                texto=f'Novo chamado criado: {chamado.titulo}',
                chamado=chamado,
                usuario=admin
            )
            for admin in admins
        ]
        
        Notificacao.objects.bulk_create(notificacoes)
    
    @staticmethod
    def atribuir_responsavel(chamado, responsavel, user_atual, role='responsavel_tecnico'):
        """
        Atribui um responsável ao chamado
        
        Args:
            chamado: Instância de Chamado
            responsavel: User a ser atribuído
            user_atual: User que está fazendo a atribuição
            role: Tipo de responsabilidade (padrão: 'responsavel_tecnico')
            
        Returns:
            tuple: (ChamadoResponsavel, bool) - (instância, foi_criado)
        """
        chamado_responsavel, created = ChamadoResponsavel.objects.get_or_create(
            chamado=chamado,
            responsavel=responsavel,
            defaults={'role': role}
        )
        
        if created:
            # Registra no histórico
            chamado.adicionar_log_status(
                user=user_atual,
                comentario=f'Responsável {responsavel.get_full_name() or responsavel.username} atribuído'
            )
            
            # Notifica o responsável
            Notificacao.objects.create(
                texto=f'Você foi atribuído ao chamado: {chamado.titulo}',
                chamado=chamado,
                usuario=responsavel
            )
        
        return chamado_responsavel, created
    
    @staticmethod
    def alterar_status(chamado, novo_status, user_atual, comentario=''):
        """
        Altera o status do chamado e notifica usuários relacionados
        
        Args:
            chamado: Instância de Chamado
            novo_status: Novo status (string)
            user_atual: User que está alterando o status
            comentario: Comentário sobre a mudança (opcional)
        """
        # Valida se o status é válido
        status_validos = dict(Chamado.STATUS_CHOICES).keys()
        if novo_status not in status_validos:
            raise ValueError(f'Status inválido: {novo_status}')
        
        # Muda o status
        status_display = dict(Chamado.STATUS_CHOICES).get(novo_status)
        comentario_final = comentario or f'Status alterado para {status_display}'
        
        chamado.mudar_status(
            novo_status=novo_status,
            user=user_atual,
            comentario=comentario_final
        )
        
        # Notifica usuários relacionados
        ChamadoService._notificar_mudanca_status(chamado, user_atual)
    
    @staticmethod
    def _notificar_mudanca_status(chamado, user_atual):
        """
        Notifica solicitante e responsáveis sobre mudança de status
        
        Args:
            chamado: Instância de Chamado
            user_atual: User que fez a mudança (não será notificado)
        """
        # Lista usuários a notificar (sem duplicatas)
        usuarios_notificar = {chamado.solicitante}
        usuarios_notificar.update(
            r.responsavel for r in chamado.responsaveis.select_related('responsavel').all()
        )
        
        # Remove o usuário que fez a mudança
        usuarios_notificar.discard(user_atual)
        
        # Cria notificações em lote
        notificacoes = [
            Notificacao(
                texto=f'Chamado "{chamado.titulo}" teve status alterado para {chamado.get_status_display()}',
                chamado=chamado,
                usuario=usuario
            )
            for usuario in usuarios_notificar
        ]
        
        Notificacao.objects.bulk_create(notificacoes)
    
    @staticmethod
    def obter_estatisticas(queryset):
        """
        Calcula estatísticas sobre chamados
        
        Args:
            queryset: QuerySet de Chamado
            
        Returns:
            dict: Dicionário com estatísticas
        """
        total = queryset.count()
        
        # Estatísticas por status
        por_status = list(
            queryset.values('status').annotate(total=Count('id'))
        )
        
        # Estatísticas por urgência
        por_urgencia = list(
            queryset.values('urgencia').annotate(total=Count('id'))
        )
        
        # Chamados em atraso
        em_atraso = queryset.filter(
            data_sugerida__lt=timezone.now(),
            status__in=['aberto', 'aguardando_responsaveis', 'em_andamento']
        ).count()
        
        # Concluídos no mês atual
        now = timezone.now()
        concluidos_mes = queryset.filter(
            data_conclusao__month=now.month,
            data_conclusao__year=now.year,
            status='concluido'
        ).count()
        
        return {
            'total': total,
            'por_status': por_status,
            'por_urgencia': por_urgencia,
            'em_atraso': em_atraso,
            'concluidos_mes_atual': concluidos_mes
        }
    
    @staticmethod
    def pode_remover(chamado, user):
        """
        Verifica se o usuário pode remover o chamado
        
        Args:
            chamado: Instância de Chamado
            user: User que quer remover
            
        Returns:
            tuple: (bool, str) - (pode_remover, mensagem_erro)
        """
        # Admin pode remover qualquer chamado
        if user.is_staff:
            return True, None
        
        # Solicitante pode remover próprios chamados
        if chamado.solicitante == user:
            return True, None
        
        return False, 'Você não tem permissão para remover este chamado'