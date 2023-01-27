from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DiscountTicket
from .serializers import DiscountTicketSerializer
from . import services

class DiscountTicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiscountTicket.objects.all()
    serializer_class = DiscountTicketSerializer

    @action(detail=True, methods=['post'], url_path='set-default')
    def add_ticket(self, request, pk=None):
        services.set_default(address=self.get_object(),
                             user_id=request.user.id)
        return Response({'message': 'Update succssfully.'}, status=status.HTTP_200_OK)
