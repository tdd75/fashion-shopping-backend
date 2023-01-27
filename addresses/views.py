from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Address
from .serializers import AddressSerializer
from .swagger import ADDRESS_EXAMPLES
from . import services


@extend_schema_view(create=extend_schema(examples=ADDRESS_EXAMPLES), set_default=extend_schema(request=None))
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    filterset_fields = ('is_default',)

    def get_queryset(self):
        return Address.objects.filter(owner_id=self.request.user.id)

    @action(detail=True, methods=['post'], url_path='set-default')
    def set_default(self, request, pk=None):
        services.set_default(address=self.get_object(),
                             user_id=request.user.id)
        return Response({'message': 'Update succssful1ly.'}, status=status.HTTP_200_OK)
