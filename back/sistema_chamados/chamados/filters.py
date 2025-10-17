import django_filters
from .models import Chamado, Ativo
from django.db.models import Q


class ChamadoFilter(django_filters.FilterSet):
    """Filtros avançados para chamados"""
    
    # Filtros de texto
    titulo = django_filters.CharFilter(lookup_expr='icontains')
    descricao = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros de escolha
    status = django_filters.MultipleChoiceFilter(choices=Chamado.STATUS_CHOICES)
    urgencia = django_filters.MultipleChoiceFilter(choices=Chamado.URGENCIA_CHOICES)
    
    # Filtros de data
    data_abertura_inicio = django_filters.DateTimeFilter(
        field_name='data_abertura', 
        lookup_expr='gte'
    )
    data_abertura_fim = django_filters.DateTimeFilter(
        field_name='data_abertura', 
        lookup_expr='lte'
    )
    data_sugerida_inicio = django_filters.DateTimeFilter(
        field_name='data_sugerida', 
        lookup_expr='gte'
    )
    data_sugerida_fim = django_filters.DateTimeFilter(
        field_name='data_sugerida', 
        lookup_expr='lte'
    )
    
    # Filtros de relacionamento
    solicitante = django_filters.NumberFilter(field_name='solicitante__id')
    responsavel = django_filters.NumberFilter(
        field_name='responsaveis__responsavel__id',
        distinct=True
    )
    ativo = django_filters.NumberFilter(field_name='ativos__id', distinct=True)
    ambiente = django_filters.NumberFilter(
        field_name='ativos__ambiente__id',
        distinct=True
    )
    
    # Filtros booleanos customizados
    em_atraso = django_filters.BooleanFilter(method='filter_em_atraso')
    sem_responsavel = django_filters.BooleanFilter(method='filter_sem_responsavel')
    
    class Meta:
        model = Chamado
        fields = ['status', 'urgencia', 'solicitante']
    
    def filter_em_atraso(self, queryset, name, value):
        """Filtra chamados em atraso"""
        from django.utils import timezone
        
        if value:
            return queryset.filter(
                data_sugerida__lt=timezone.now(),
                status__in=['aberto', 'aguardando_responsaveis', 'em_andamento']
            )
        return queryset
    
    def filter_sem_responsavel(self, queryset, name, value):
        """Filtra chamados sem responsável atribuído"""
        if value:
            return queryset.filter(responsaveis__isnull=True)
        return queryset.exclude(responsaveis__isnull=True)


class AtivoFilter(django_filters.FilterSet):
    """Filtros avançados para ativos"""
    
    # Filtros de texto
    nome = django_filters.CharFilter(lookup_expr='icontains')
    descricao = django_filters.CharFilter(lookup_expr='icontains')
    codigo_patrimonio = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros de escolha
    status = django_filters.MultipleChoiceFilter(choices=Ativo.STATUS_CHOICES)
    
    # Filtros de relacionamento
    ambiente = django_filters.NumberFilter(field_name='ambiente__id')
    categoria = django_filters.NumberFilter(field_name='categoria__id')
    
    # Busca global
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Ativo
        fields = ['status', 'ambiente', 'categoria']
    
    def filter_search(self, queryset, name, value):
        """Busca global em múltiplos campos"""
        return queryset.filter(
            Q(nome__icontains=value) |
            Q(descricao__icontains=value) |
            Q(codigo_patrimonio__icontains=value) |
            Q(ambiente__nome__icontains=value) |
            Q(categoria__nome__icontains=value)
        )