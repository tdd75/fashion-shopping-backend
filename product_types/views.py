from rest_framework import generics

from .serializers import ProductTypeSerializer
from .models import ProductType


class ProductTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class ProductTypeDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    lookup_field = 'pk'
