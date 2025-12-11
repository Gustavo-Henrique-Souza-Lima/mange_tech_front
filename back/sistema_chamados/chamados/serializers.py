from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Categoria, Ambiente, Ativo, Chamado, 
    ChamadoResponsavel, ChamadoStatusHistory, Anexo, Notificacao
)

class UserSerializer(serializers.ModelSerializer):
    nome_completo = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'nome_completo']
    
    def get_nome_completo(self, obj):
        return obj.get_full_name() or obj.username

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'telefone', 'endereco', 'nif', 'created_at']

class CategoriaSerializer(serializers.ModelSerializer):
    total_ativos = serializers.SerializerMethodField()
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'total_ativos', 'created_at']
    
    def get_total_ativos(self, obj):
        return obj.ativos.count()

class AmbienteReadSerializer(serializers.ModelSerializer):
    responsavel = UserSerializer(read_only=True)
    total_ativos = serializers.SerializerMethodField()
    class Meta:
        model = Ambiente
        fields = ['id', 'nome', 'descricao', 'localizacao_ambiente', 'responsavel', 'total_ativos']
    
    def get_total_ativos(self, obj):
        return obj.ativos.count()

class AmbienteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente
        fields = ['nome', 'descricao', 'localizacao_ambiente', 'responsavel']

class AtivoReadSerializer(serializers.ModelSerializer):
    ambiente = AmbienteReadSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Ativo
        fields = ['id', 'nome', 'descricao', 'codigo_patrimonio', 'qr_code', 'categoria', 'ambiente', 'status', 'status_display']

class AtivoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ativo
        # GARANTINDO QUE qr_code ESTÁ AQUI
        fields = ['nome', 'descricao', 'codigo_patrimonio', 'qr_code', 'categoria', 'ambiente', 'status']

class ChamadoResponsavelSerializer(serializers.ModelSerializer):
    responsavel = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    class Meta:
        model = ChamadoResponsavel
        fields = ['id', 'responsavel', 'role', 'role_display', 'data_atribuicao']

class AnexoSerializer(serializers.ModelSerializer):
    usuario_upload = UserSerializer(read_only=True)
    tamanho_formatado = serializers.CharField(read_only=True)
    url = serializers.SerializerMethodField()
    class Meta:
        model = Anexo
        fields = ['id', 'nome_arquivo', 'arquivo', 'mimetype', 'tamanho_bytes', 'tamanho_formatado', 'data_upload', 'usuario_upload', 'url']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if obj.arquivo and request:
            return request.build_absolute_uri(obj.arquivo.url)
        return None

class ChamadoStatusHistoryReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    anexos = serializers.SerializerMethodField()
    class Meta:
        model = ChamadoStatusHistory
        fields = ['id', 'status', 'status_display', 'comentario', 'user', 'created_at', 'anexos']
    
    def get_anexos(self, obj):
        return AnexoSerializer(obj.anexos.all(), many=True, context=self.context).data

class ChamadoListSerializer(serializers.ModelSerializer):
    solicitante = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    urgencia_display = serializers.CharField(source='get_urgencia_display', read_only=True)
    total_responsaveis = serializers.SerializerMethodField()
    esta_em_atraso = serializers.BooleanField(read_only=True)
    class Meta:
        model = Chamado
        fields = ['id', 'titulo', 'status', 'status_display', 'urgencia', 'urgencia_display', 'solicitante', 'data_abertura', 'data_sugerida', 'total_responsaveis', 'esta_em_atraso']
    
    def get_total_responsaveis(self, obj):
        return obj.responsaveis.count()

class ChamadoDetailSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'titulo', 'descricao', 'status', 'status_display', 'urgencia', 'urgencia_display', 'data_sugerida', 'data_abertura', 'data_conclusao', 'solicitante', 'ativos', 'responsaveis', 'historico', 'anexos', 'created_at', 'esta_em_atraso']

class ChamadoCreateSerializer(serializers.ModelSerializer):
    ativos_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    class Meta:
        model = Chamado
        fields = ['titulo', 'descricao', 'urgencia', 'data_sugerida', 'ativos_ids']
    
    def create(self, validated_data):
        ativos_ids = validated_data.pop('ativos_ids', [])
        validated_data['solicitante'] = self.context['request'].user
        chamado = Chamado.objects.create(**validated_data)
        if ativos_ids:
            chamado.ativos.set(ativos_ids)
            # AQUI ESTÁ A MÁGICA: Mudar status dos ativos para manutenção
            chamado.ativos.update(status='manutencao')
            
        ChamadoStatusHistory.objects.create(chamado=chamado, user=validated_data['solicitante'], status='aberto', comentario='Chamado criado')
        return chamado

class ChamadoUpdateSerializer(serializers.ModelSerializer):
    ativos_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
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
    chamado = ChamadoListSerializer(read_only=True)
    usuario = UserSerializer(read_only=True)
    class Meta:
        model = Notificacao
        fields = ['id', 'texto', 'chamado', 'usuario', 'lida', 'created_at']