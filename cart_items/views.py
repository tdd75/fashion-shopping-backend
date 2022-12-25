from rest_framework import generics

from .models import CartItem
from .serializers import CartItemSerializer


class CartItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CartItemDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = 'pk'
