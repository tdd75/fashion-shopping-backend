from rest_framework import generics
from drf_spectacular.utils import OpenApiExample, extend_schema_view, extend_schema

from .models import Product
from .serializers import ProductSerializer


@extend_schema_view(
    post=extend_schema(summary='multipart/form-data')
)
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
