from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import AllowAny

from .serializers import ProductTypeSerializer
from .models import ProductType


@extend_schema_view(list=extend_schema(auth=[]))
class ProductTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = (AllowAny,)
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = ('product',)
