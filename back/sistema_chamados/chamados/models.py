from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

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
        if self.data_sugerida and self.status not in ['concluido', 'cancelado']:
            return timezone.now() > self.data_sugerida
        return False

    def adicionar_log_status(self, user, comentario=""):
        """Adiciona log e RETORNA o objeto histórico criado"""
        return ChamadoStatusHistory.objects.create(
            chamado=self,
            user=user,
            status=self.status,
            comentario=comentario
        )

    def mudar_status(self, novo_status, user, comentario=""):
        """Muda status e RETORNA o objeto histórico criado"""
        self.status = novo_status
        
        if novo_status in ['concluido', 'cancelado'] and not self.data_conclusao:
            self.data_conclusao = timezone.now()
        
        self.save()
        
        # Agora retorna o histórico para podermos vincular anexos a ele
        return self.adicionar_log_status(user, comentario)


class ChamadoResponsavel(models.Model):
    ROLE_CHOICES = [
        ('responsavel_tecnico', 'Responsável Técnico'),
        ('supervisor', 'Supervisor'),
        ('colaborador', 'Colaborador'),
    ]
    
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='responsaveis')
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chamados_atribuidos')
    data_atribuicao = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='responsavel_tecnico')

    class Meta:
        unique_together = ['chamado', 'responsavel']


class ChamadoStatusHistory(models.Model):
    STATUS_CHOICES = Chamado.STATUS_CHOICES
    
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='historico')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_alteracoes')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    comentario = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Anexo(models.Model):
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
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='anexos')
    data_upload = models.DateTimeField(auto_now_add=True)
    usuario_upload = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-data_upload']

    def save(self, *args, **kwargs):
        if self.arquivo:
            self.nome_arquivo = self.arquivo.name
            self.tamanho_bytes = self.arquivo.size
            try:
                self.mimetype = getattr(self.arquivo.file, 'content_type', 'application/octet-stream')
            except:
                self.mimetype = 'application/octet-stream'
        super().save(*args, **kwargs)

    @property
    def tamanho_formatado(self):
        if self.tamanho_bytes is None: return "0 B"
        bytes_size = float(self.tamanho_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0: return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"

class Notificacao(models.Model):
    texto = models.CharField(max_length=500)
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='notificacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    lida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']