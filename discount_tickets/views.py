from rest_framework import viewsets

from .models import DiscountTicket
from .serializers import DiscountTicketSerializer


class DiscountTicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiscountTicket.objects.all()
    serializer_class = DiscountTicketSerializer
