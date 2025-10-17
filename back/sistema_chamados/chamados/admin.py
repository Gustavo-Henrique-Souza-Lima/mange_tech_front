from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import (
    UserProfile, Categoria, Ambiente, Ativo, Chamado,
    ChamadoResponsavel, ChamadoStatusHistory, Anexo, Notificacao
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefone', 'nif', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'nif']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações de Contato', {
            'fields': ('telefone', 'endereco', 'nif')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'total_ativos', 'created_at']
    search_fields = ['nome', 'descricao']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    
    def total_ativos(self, obj):
        return obj.ativos.count()
    total_ativos.short_description = 'Total de Ativos'


@admin.register(Ambiente)
class AmbienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'responsavel', 'localizacao_ambiente', 'total_ativos', 'created_at']
    search_fields = ['nome', 'localizacao_ambiente', 'responsavel__username']
    list_filter = ['responsavel', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['responsavel']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'localizacao_ambiente')
        }),
        ('Responsável', {
            'fields': ('responsavel',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_ativos(self, obj):
        return obj.ativos.count()
    total_ativos.short_description = 'Total de Ativos'


@admin.register(Ativo)
class AtivoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo_patrimonio', 'categoria', 'ambiente', 'status_badge', 'created_at']
    list_filter = ['status', 'categoria', 'ambiente', 'created_at']
    search_fields = ['nome', 'codigo_patrimonio', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['ambiente', 'categoria']
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'codigo_patrimonio', 'qr_code')
        }),
        ('Classificação', {
            'fields': ('categoria', 'ambiente', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'ativo': 'green',
            'manutencao': 'orange',
            'inativo': 'red',
            'descartado': 'gray'
        }
        color = colors.get(obj.status, 'blue')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


class ChamadoResponsavelInline(admin.TabularInline):
    model = ChamadoResponsavel
    extra = 1
    autocomplete_fields = ['responsavel']
    readonly_fields = ['data_atribuicao']


class ChamadoStatusHistoryInline(admin.TabularInline):
    model = ChamadoStatusHistory
    extra = 0
    readonly_fields = ['user', 'status', 'comentario', 'created_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


class AnexoInline(admin.TabularInline):
    model = Anexo
    extra = 0
    readonly_fields = ['nome_arquivo', 'tamanho_bytes', 'mimetype', 'data_upload', 'usuario_upload']
    fields = ['arquivo', 'nome_arquivo', 'tamanho_bytes', 'mimetype', 'usuario_upload', 'data_upload']


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'solicitante', 'status_badge', 'urgencia_badge', 
                   'data_abertura', 'data_sugerida', 'em_atraso', 'total_responsaveis']
    list_filter = ['status', 'urgencia', 'data_abertura', 'data_sugerida']
    search_fields = ['titulo', 'descricao', 'solicitante__username']
    readonly_fields = ['data_abertura', 'created_at', 'updated_at', 'em_atraso']
    autocomplete_fields = ['solicitante']
    filter_horizontal = ['ativos']
    list_per_page = 25
    date_hierarchy = 'data_abertura'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'solicitante')
        }),
        ('Classificação', {
            'fields': ('status', 'urgencia', 'data_sugerida')
        }),
        ('Ativos Relacionados', {
            'fields': ('ativos',)
        }),
        ('Datas', {
            'fields': ('data_abertura', 'data_conclusao', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ChamadoResponsavelInline, ChamadoStatusHistoryInline, AnexoInline]
    
    def status_badge(self, obj):
        colors = {
            'aberto': '#007bff',
            'aguardando_responsaveis': '#ffc107',
            'em_andamento': '#17a2b8',
            'realizado': '#6c757d',
            'concluido': '#28a745',
            'cancelado': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def urgencia_badge(self, obj):
        colors = {
            'baixa': '#28a745',
            'media': '#ffc107',
            'alta': '#fd7e14',
            'critica': '#dc3545'
        }
        color = colors.get(obj.urgencia, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_urgencia_display()
        )
    urgencia_badge.short_description = 'Urgência'
    
    def em_atraso(self, obj):
        if obj.esta_em_atraso:
            return format_html('<span style="color: red; font-weight: bold;">✘ SIM</span>')
        return format_html('<span style="color: green;">✔ NÃO</span>')
    em_atraso.short_description = 'Em Atraso'
    
    def total_responsaveis(self, obj):
        count = obj.responsaveis.count()
        if count == 0:
            return format_html('<span style="color: red;">0</span>')
        return count
    total_responsaveis.short_description = 'Responsáveis'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('solicitante').prefetch_related('responsaveis', 'ativos')


@admin.register(ChamadoResponsavel)
class ChamadoResponsavelAdmin(admin.ModelAdmin):
    list_display = ['chamado', 'responsavel', 'role', 'data_atribuicao']
    list_filter = ['role', 'data_atribuicao']
    search_fields = ['chamado__titulo', 'responsavel__username']
    readonly_fields = ['data_atribuicao']
    autocomplete_fields = ['chamado', 'responsavel']


@admin.register(ChamadoStatusHistory)
class ChamadoStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['chamado', 'status', 'user', 'created_at', 'tem_anexos']
    list_filter = ['status', 'created_at']
    search_fields = ['chamado__titulo', 'user__username', 'comentario']
    readonly_fields = ['created_at']
    autocomplete_fields = ['chamado', 'user']
    
    fieldsets = (
        ('Informações', {
            'fields': ('chamado', 'user', 'status')
        }),
        ('Detalhes', {
            'fields': ('comentario',)
        }),
        ('Data', {
            'fields': ('created_at',)
        }),
    )
    
    def tem_anexos(self, obj):
        count = obj.anexos.count()
        if count > 0:
            return format_html('<span style="color: green;">✔ {} anexo(s)</span>', count)
        return format_html('<span style="color: gray;">Sem anexos</span>')
    tem_anexos.short_description = 'Anexos'


@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ['nome_arquivo', 'chamado_link', 'tamanho_formatado', 
                   'mimetype', 'usuario_upload', 'data_upload']
    list_filter = ['mimetype', 'data_upload']
    search_fields = ['nome_arquivo', 'chamado__titulo', 'usuario_upload__username']
    readonly_fields = ['nome_arquivo', 'mimetype', 'tamanho_bytes', 
                      'tamanho_formatado', 'data_upload']
    autocomplete_fields = ['chamado', 'chamado_history', 'usuario_upload']
    date_hierarchy = 'data_upload'
    
    fieldsets = (
        ('Arquivo', {
            'fields': ('arquivo', 'nome_arquivo', 'mimetype', 'tamanho_bytes', 'tamanho_formatado')
        }),
        ('Relacionamento', {
            'fields': ('chamado', 'chamado_history', 'usuario_upload')
        }),
        ('Data', {
            'fields': ('data_upload',)
        }),
    )
    
    def chamado_link(self, obj):
        url = reverse('admin:chamados_chamado_change', args=[obj.chamado.id])
        return format_html('<a href="{}">{}</a>', url, obj.chamado.titulo)
    chamado_link.short_description = 'Chamado'


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['texto_resumido', 'chamado_link', 'usuario', 'lida_badge', 'created_at']
    list_filter = ['lida', 'created_at']
    search_fields = ['texto', 'chamado__titulo', 'usuario__username']
    readonly_fields = ['created_at']
    autocomplete_fields = ['chamado', 'usuario']
    date_hierarchy = 'created_at'
    actions = ['marcar_como_lida', 'marcar_como_nao_lida']
    
    fieldsets = (
        ('Conteúdo', {
            'fields': ('texto', 'chamado')
        }),
        ('Destinatário', {
            'fields': ('usuario', 'lida')
        }),
        ('Data', {
            'fields': ('created_at',)
        }),
    )
    
    def texto_resumido(self, obj):
        if len(obj.texto) > 50:
            return f"{obj.texto[:50]}..."
        return obj.texto
    texto_resumido.short_description = 'Texto'
    
    def chamado_link(self, obj):
        url = reverse('admin:chamados_chamado_change', args=[obj.chamado.id])
        return format_html('<a href="{}">{}</a>', url, obj.chamado.titulo)
    chamado_link.short_description = 'Chamado'
    
    def lida_badge(self, obj):
        if obj.lida:
            return format_html('<span style="color: green;">✔ Lida</span>')
        return format_html('<span style="color: orange; font-weight: bold;">✘ Não lida</span>')
    lida_badge.short_description = 'Status'
    
    def marcar_como_lida(self, request, queryset):
        count = queryset.update(lida=True)
        self.message_user(request, f'{count} notificação(ões) marcada(s) como lida(s).')
    marcar_como_lida.short_description = 'Marcar como lida'
    
    def marcar_como_nao_lida(self, request, queryset):
        count = queryset.update(lida=False)
        self.message_user(request, f'{count} notificação(ões) marcada(s) como não lida(s).')
    marcar_como_nao_lida.short_description = 'Marcar como não lida'


# Configuração do site admin    
admin.site.site_header = 'Sistema de Chamados - Administração'
admin.site.site_title = 'Sistema de Chamados'
admin.site.index_title = 'Painel de Controle'