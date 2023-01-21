from rest_framework import generics, filters
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer, ProductFavoriteSerializer
from .filter_set import ProductFilterSet


@extend_schema_view(
    post=extend_schema(summary='multipart/form-data')
)
class ProductListCreateAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = ProductFilterSet
    search_fields = ('name', 'description')
    ordering_fields = ('price', 'rating')
    ordering = ('id',)


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ProductFavoriteAPIView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductFavoriteSerializer
    lookup_field = 'pk'
