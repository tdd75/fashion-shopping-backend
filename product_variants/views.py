from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import ProductVariantSerializer
from .models import ProductVariant


@extend_schema_view(list=extend_schema(auth=[]))
class ProductVariantViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProductVariant.objects.all().select_related('product')
    serializer_class = ProductVariantSerializer
    permission_classes = (AllowAny,)
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = ('product',)


class ProductAdminVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = (IsAdminUser,)
