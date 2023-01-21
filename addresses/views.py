from rest_framework import generics

from .models import Address
from .serializers import AddressSerializer


class AddressListCreateAPIView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AddressDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
