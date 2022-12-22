from rest_framework import generics
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import CartItem
from .serializers import CartItemSerializer


@extend_schema_view(
    post=extend_schema(summary='multipart/form-data')
)
class CartItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'pk'
