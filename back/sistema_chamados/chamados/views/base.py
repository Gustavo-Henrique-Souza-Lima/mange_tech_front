"""
Classes base reutilizáveis para ViewSets
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class BaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet base com configurações padrão para todos os endpoints
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Otimiza queries com select_related e prefetch_related
        Sobrescrever em subclasses quando necessário
        """
        return super().get_queryset()


class ReadWriteSerializerMixin:
    """
    Mixin para usar serializers diferentes em leitura e escrita
    
    Usage:
        class MyViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
            read_serializer_class = MyReadSerializer
            write_serializer_class = MyWriteSerializer
    """
    read_serializer_class = None
    write_serializer_class = None
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return self.write_serializer_class or self.serializer_class
        return self.read_serializer_class or self.serializer_class