from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from .serializers import ProductCategorySerializer
from .models import ProductCategory


class ProductCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProductCategory.objects.all().prefetch_related('product_set')
    serializer_class = ProductCategorySerializer
    permission_classes = (AllowAny,)
