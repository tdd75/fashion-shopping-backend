from rest_framework import generics

from .models import DiscountTicket
from .serializers import DiscountTicketSerializer


class DiscountTicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = DiscountTicket.objects.all()
    serializer_class = DiscountTicketSerializer


class DiscountTicketDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscountTicket.objects.all()
    serializer_class = DiscountTicketSerializer
    lookup_field = 'pk'
