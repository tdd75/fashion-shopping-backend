from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductTypeSerializer
from .models import ProductType


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = ('product',)
