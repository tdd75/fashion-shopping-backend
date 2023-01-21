from rest_framework import generics

from .models import DiscountTicket
from .serializers import DiscountTicketSerializer


class DiscountTicketListCreateAPIView(generics.ListAPIView):
    queryset = DiscountTicket.objects.all()
    serializer_class = DiscountTicketSerializer


class DiscountTicketDetailUpdateDeleteAPIView(generics.RetrieveAPIView):
    queryset = DiscountTicket.objects.all()
    serializer_class = DiscountTicketSerializer
    lookup_field = 'pk'
