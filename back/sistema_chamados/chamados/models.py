from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    """Perfil estendido do usuário com informações adicionais"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    nif = models.CharField(max_length=15, unique=True, null=True, blank=True, 
                          verbose_name="NIF/CPF")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Categoria(models.Model):
    """Categorias para classificação de ativos"""
    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Ambiente(models.Model):
    """Ambientes/Locais onde os ativos estão localizados"""
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    localizacao_ambiente = models.CharField(max_length=200, blank=True, null=True)
    responsavel = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ambientes_responsaveis'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ambiente"
        verbose_name_plural = "Ambientes"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Ativo(models.Model):
    """Ativos/Equipamentos do patrimônio"""
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('manutencao', 'Manutenção'),
        ('inativo', 'Inativo'),
        ('descartado', 'Descartado'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    codigo_patrimonio = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True, 
        null=True,
        verbose_name="Código de Patrimônio"
    )
    qr_code = models.CharField(
        max_length=100, 
        unique=True, 
        blank=True, 
        null=True,
        verbose_name="QR Code"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ativos'
    )
    ambiente = models.ForeignKey(
        Ambiente, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ativos'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['codigo_patrimonio']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.nome} - {self.codigo_patrimonio}"


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Chamado(models.Model):
    """Chamados/Tickets de manutenção ou solicitações"""
    URGENCIA_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('aguardando_responsaveis', 'Aguardando Responsáveis'),
        ('em_andamento', 'Em Andamento'),
        ('realizado', 'Realizado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    urgencia = models.CharField(max_length=20, choices=URGENCIA_CHOICES, default='media')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='aberto')
    data_sugerida = models.DateTimeField(blank=True, null=True)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(blank=True, null=True)
    solicitante = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='chamados_solicitados'
    )
    ativos = models.ManyToManyField('Ativo', blank=True, related_name='chamados')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['urgencia']),
            models.Index(fields=['solicitante']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"

    @property
    def esta_em_atraso(self):
        """Verifica se o chamado está em atraso baseado na data sugerida"""
        from django.utils import timezone
        if self.data_sugerida and self.status not in ['concluido', 'cancelado']:
            return timezone.now() > self.data_sugerida
        return False

    def adicionar_log_status(self, user, comentario=""):
        """Adiciona um registro no histórico de status"""
        ChamadoStatusHistory.objects.create(
            chamado=self,
            user=user,
            status=self.status,
            comentario=comentario
        )

    def mudar_status(self, novo_status, user, comentario=""):
        """Método para mudar o status com registro automático no histórico"""
        from django.utils import timezone
        
        status_anterior = self.status
        self.status = novo_status
        
        # Atualiza data_conclusao se necessário
        if novo_status in ['concluido', 'cancelado'] and not self.data_conclusao:
            self.data_conclusao = timezone.now()
        
        self.save()
        
        # Cria o log no histórico
        self.adicionar_log_status(user, comentario)
        
        return status_anterior


class ChamadoResponsavel(models.Model):
    """Responsáveis atribuídos aos chamados"""
    ROLE_CHOICES = [
        ('responsavel_tecnico', 'Responsável Técnico'),
        ('supervisor', 'Supervisor'),
        ('colaborador', 'Colaborador'),
    ]
    
    chamado = models.ForeignKey(
        Chamado, 
        on_delete=models.CASCADE,
        related_name='responsaveis'
    )
    responsavel = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='chamados_atribuidos'
    )
    data_atribuicao = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='responsavel_tecnico')

    class Meta:
        verbose_name = "Responsável do Chamado"
        verbose_name_plural = "Responsáveis dos Chamados"
        unique_together = ['chamado', 'responsavel']
        ordering = ['-data_atribuicao']

    def __str__(self):
        return f"{self.chamado.titulo} - {self.responsavel.username} ({self.get_role_display()})"


class ChamadoStatusHistory(models.Model):
    """Histórico de mudanças de status dos chamados"""
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('aguardando_responsaveis', 'Aguardando Responsáveis'),
        ('em_andamento', 'Em Andamento'),
        ('realizado', 'Realizado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    chamado = models.ForeignKey(
        Chamado, 
        on_delete=models.CASCADE,
        related_name='historico'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='historico_alteracoes'
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    comentario = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de Status"
        verbose_name_plural = "Histórico de Status"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['chamado', '-created_at']),
        ]

    def __str__(self):
        return f"{self.chamado.titulo} - {self.get_status_display()} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"


# ============================================
# SIGNALS - Log automático de mudanças
# ============================================

@receiver(post_save, sender=Chamado)
def criar_log_inicial(sender, instance, created, **kwargs):
    """Cria o primeiro registro no histórico quando o chamado é criado"""
    if created:
        ChamadoStatusHistory.objects.create(
            chamado=instance,
            user=instance.solicitante,
            status=instance.status,
            comentario="Chamado criado"
        )


# Variável global para rastrear mudanças de status
_chamado_status_anterior = {}

@receiver(pre_save, sender=Chamado)
def rastrear_mudanca_status(sender, instance, **kwargs):
    """Captura o status anterior antes de salvar"""
    if instance.pk:
        try:
            chamado_anterior = Chamado.objects.get(pk=instance.pk)
            _chamado_status_anterior[instance.pk] = chamado_anterior.status
        except Chamado.DoesNotExist:
            pass


@receiver(post_save, sender=Chamado)
def registrar_mudanca_status(sender, instance, created, **kwargs):
    """Registra mudança de status automaticamente no histórico"""
    if not created and instance.pk in _chamado_status_anterior:
        status_anterior = _chamado_status_anterior[instance.pk]
        
        # Se o status mudou, cria um log
        if status_anterior != instance.status:
            # Tenta pegar o usuário da requisição atual (você precisará passar isso)
            # Por padrão, usa o solicitante
            user = getattr(instance, '_current_user', instance.solicitante)
            comentario = getattr(instance, '_status_comentario', f"Status alterado de {dict(Chamado.STATUS_CHOICES).get(status_anterior)} para {instance.get_status_display()}")
            
            ChamadoStatusHistory.objects.create(
                chamado=instance,
                user=user,
                status=instance.status,
                comentario=comentario
            )
        
        # Limpa o cache
        del _chamado_status_anterior[instance.pk]

class Anexo(models.Model):
    """Anexos/Imagens vinculados aos chamados e histórico"""
    ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx']
    
    nome_arquivo = models.CharField(max_length=255, blank=True)
    arquivo = models.FileField(
        upload_to='anexos/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    mimetype = models.CharField(max_length=100, blank=True)
    tamanho_bytes = models.IntegerField(null=True, blank=True)
    chamado_history = models.ForeignKey(
        ChamadoStatusHistory, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='anexos'
    )
    chamado = models.ForeignKey(
        Chamado, 
        on_delete=models.CASCADE,
        related_name='anexos'
    )
    data_upload = models.DateTimeField(auto_now_add=True)
    usuario_upload = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='anexos_uploaded'
    )

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = ['-data_upload']

    def save(self, *args, **kwargs):
        if self.arquivo:
            self.nome_arquivo = self.arquivo.name
            self.tamanho_bytes = self.arquivo.size
            # Tenta obter o mimetype
            try:
                self.mimetype = getattr(self.arquivo.file, 'content_type', 'application/octet-stream')
            except:
                self.mimetype = 'application/octet-stream'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_arquivo} - {self.chamado.titulo}"

    @property
    def tamanho_formatado(self):
        """Retorna o tamanho do arquivo formatado"""
        # ✅ CORREÇÃO: Verificar se tamanho_bytes não é None
        if self.tamanho_bytes is None:
            return "0 B"
        
        bytes_size = float(self.tamanho_bytes)
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        
        return f"{bytes_size:.1f} TB"
    
class Notificacao(models.Model):
    """Notificações para usuários sobre chamados"""
    texto = models.CharField(max_length=500)
    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    lida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', 'lida', '-created_at']),
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.chamado.titulo}"

    def marcar_como_lida(self):
        """Marca a notificação como lida"""
        self.lida = True
        self.save()