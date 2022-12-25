from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductTypeSerializer
from .models import ProductType


class ProductTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = ('product',)


class ProductTypeDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    lookup_field = 'pk'
