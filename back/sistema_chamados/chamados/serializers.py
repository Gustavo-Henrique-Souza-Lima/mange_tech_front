from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Categoria, Ambiente, Ativo, Chamado, 
    ChamadoResponsavel, ChamadoStatusHistory, Anexo, Notificacao
)
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuário"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para cadastro de usuário"""
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        # Criar usuário com senha criptografada
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    

class ReadWriteSerializerMixin:
    """Mixin para separar serializers de leitura e escrita"""
    read_serializer_class = None
    write_serializer_class = None
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return self.write_serializer_class or self.serializer_class
        return self.read_serializer_class or self.serializer_class


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para usuários"""
    nome_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'nome_completo']
        read_only_fields = fields
    
    def get_nome_completo(self, obj):
        return obj.get_full_name() or obj.username


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfis de usuário"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'telefone', 'endereco', 'nif', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para categorias"""
    total_ativos = serializers.SerializerMethodField()
    
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'total_ativos', 'created_at']
        read_only_fields = ['created_at']
    
    def get_total_ativos(self, obj):
        return obj.ativos.count()


class AmbienteReadSerializer(serializers.ModelSerializer):
    """Serializer de leitura para ambientes"""
    responsavel = UserSerializer(read_only=True)
    total_ativos = serializers.SerializerMethodField()
    
    class Meta:
        model = Ambiente
        fields = ['id', 'nome', 'descricao', 'localizacao_ambiente', 
                 'responsavel', 'total_ativos', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_total_ativos(self, obj):
        return obj.ativos.count()


class AmbienteWriteSerializer(serializers.ModelSerializer):
    """Serializer de escrita para ambientes"""
    class Meta:
        model = Ambiente
        fields = ['nome', 'descricao', 'localizacao_ambiente', 'responsavel']


class AtivoReadSerializer(serializers.ModelSerializer):
    """Serializer de leitura para ativos"""
    ambiente = AmbienteReadSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Ativo
        fields = ['id', 'nome', 'descricao', 'codigo_patrimonio', 'qr_code',
                 'categoria', 'ambiente', 'status', 'status_display', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class AtivoWriteSerializer(serializers.ModelSerializer):
    """Serializer de escrita para ativos"""
    class Meta:
        model = Ativo
        fields = ['nome', 'descricao', 'codigo_patrimonio', 'qr_code',
                 'categoria', 'ambiente', 'status']


class ChamadoResponsavelSerializer(serializers.ModelSerializer):
    """Serializer para responsáveis dos chamados"""
    responsavel = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = ChamadoResponsavel
        fields = ['id', 'responsavel', 'role', 'role_display', 'data_atribuicao']
        read_only_fields = ['data_atribuicao']


class ChamadoStatusHistoryReadSerializer(serializers.ModelSerializer):
    """Serializer de leitura para histórico de status"""
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    anexos = serializers.SerializerMethodField()
    
    class Meta:
        model = ChamadoStatusHistory
        fields = ['id', 'status', 'status_display', 'comentario', 
                 'user', 'created_at', 'anexos']
        read_only_fields = ['created_at']
    
    def get_anexos(self, obj):
        from .serializers import AnexoSerializer
        return AnexoSerializer(obj.anexos.all(), many=True).data


class ChamadoStatusHistoryWriteSerializer(serializers.ModelSerializer):
    """Serializer de escrita para histórico de status"""
    class Meta:
        model = ChamadoStatusHistory
        fields = ['status', 'comentario']


class AnexoSerializer(serializers.ModelSerializer):
    """Serializer para anexos"""
    usuario_upload = UserSerializer(read_only=True)
    tamanho_formatado = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Anexo
        fields = ['id', 'nome_arquivo', 'arquivo', 'mimetype', 'tamanho_bytes',
                 'tamanho_formatado', 'data_upload', 'usuario_upload', 'url']
        read_only_fields = ['nome_arquivo', 'mimetype', 'tamanho_bytes', 
                           'data_upload', 'usuario_upload']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if obj.arquivo and request:
            return request.build_absolute_uri(obj.arquivo.url)
        return None


class ChamadoListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listagem de chamados"""
    solicitante = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    urgencia_display = serializers.CharField(source='get_urgencia_display', read_only=True)
    total_responsaveis = serializers.SerializerMethodField()
    esta_em_atraso = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Chamado
        fields = ['id', 'titulo', 'status', 'status_display', 'urgencia', 
                 'urgencia_display', 'solicitante', 'data_abertura', 
                 'data_sugerida', 'total_responsaveis', 'esta_em_atraso']
        read_only_fields = ['data_abertura']
    
    def get_total_responsaveis(self, obj):
        return obj.responsaveis.count()


class ChamadoDetailSerializer(serializers.ModelSerializer):
    """Serializer detalhado para visualização de chamados"""
    solicitante = UserSerializer(read_only=True)
    ativos = AtivoReadSerializer(many=True, read_only=True)
    responsaveis = ChamadoResponsavelSerializer(many=True, read_only=True)
    historico = ChamadoStatusHistoryReadSerializer(many=True, read_only=True)
    anexos = AnexoSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    urgencia_display = serializers.CharField(source='get_urgencia_display', read_only=True)
    esta_em_atraso = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Chamado
        fields = ['id', 'titulo', 'descricao', 'status', 'status_display', 
                 'urgencia', 'urgencia_display', 'data_sugerida', 'data_abertura',
                 'data_conclusao', 'solicitante', 'ativos', 'responsaveis', 
                 'historico', 'anexos', 'created_at', 'updated_at', 'esta_em_atraso']
        read_only_fields = ['data_abertura', 'created_at', 'updated_at']


class ChamadoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de chamados"""
    ativos_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Chamado
        fields = ['titulo', 'descricao', 'urgencia', 'data_sugerida', 'ativos_ids']
    
    def create(self, validated_data):
        ativos_ids = validated_data.pop('ativos_ids', [])
        validated_data['solicitante'] = self.context['request'].user
        chamado = Chamado.objects.create(**validated_data)
        
        if ativos_ids:
            chamado.ativos.set(ativos_ids)
        
        # Criar histórico inicial
        ChamadoStatusHistory.objects.create(
            chamado=chamado,
            user=validated_data['solicitante'],
            status='aberto',
            comentario='Chamado criado'
        )
        
        return chamado


class ChamadoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de chamados"""
    ativos_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Chamado
        fields = ['titulo', 'descricao', 'urgencia', 'data_sugerida', 'ativos_ids']
    
    def update(self, instance, validated_data):
        ativos_ids = validated_data.pop('ativos_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if ativos_ids is not None:
            instance.ativos.set(ativos_ids)
        
        return instance


class NotificacaoSerializer(serializers.ModelSerializer):
    """Serializer para notificações"""
    chamado = ChamadoListSerializer(read_only=True)
    usuario = UserSerializer(read_only=True)
    
    class Meta:
        model = Notificacao
        fields = ['id', 'texto', 'chamado', 'usuario', 'lida', 'created_at']
        read_only_fields = ['created_at']