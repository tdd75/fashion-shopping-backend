from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import DiscountTicket
from .serializers import DiscountTicketSerializer


@extend_schema_view(save_ticket=extend_schema(request=None))
class DiscountTicketViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = DiscountTicket.objects.all()
    serializer_class = DiscountTicketSerializer

    @action(detail=True, methods=['post'], url_path='save-ticket')
    def save_ticket(self, request, pk=None):
        ticket = self.get_object()
        ticket.saved_users.add(request.user.id)
        return Response({'message': 'Save succssfully.'}, status=status.HTTP_200_OK)
